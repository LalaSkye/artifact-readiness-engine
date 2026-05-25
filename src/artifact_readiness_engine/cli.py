"""CLI entry point for the Proof Structure Inspector."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .digest import compute_report_sha256, verify_report_digest
from .inspector import inspect_file
from .manifest import (
    ManifestError,
    assert_manifest_valid,
    load_manifest,
    resolve_proof_pack_reference,
)
from .report import format_json, format_text
from .validation import validate_proof_pack


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="artifact-readiness",
        description="Proof Structure Inspector — checks whether a proof pack supports a bounded claim.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect", help="Inspect a proof-pack JSON file or @manifest-id.")
    inspect_cmd.add_argument("file", help="Path to proof-pack JSON, or @id from examples/manifest.json")
    inspect_cmd.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    validate_cmd = sub.add_parser("validate", help="Validate proof-pack JSON or @manifest-id against the canonical schema.")
    validate_cmd.add_argument("file", help="Path to proof-pack JSON, or @id from examples/manifest.json")

    verify_report_cmd = sub.add_parser("verify-report", help="Verify a report JSON file carries a valid report_digest.")
    verify_report_cmd.add_argument("file", help="Path to report JSON with report_digest")
    verify_report_cmd.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    manifest_cmd = sub.add_parser("manifest", help="Inspect the canonical examples manifest.")
    manifest_cmd.add_argument(
        "--check",
        action="store_true",
        help="Run manifest integrity checks.",
    )
    manifest_cmd.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for manifest listing (default: text).",
    )

    args = parser.parse_args()

    if args.command == "inspect":
        try:
            resolved_file = resolve_proof_pack_reference(args.file)
            result = inspect_file(resolved_file)
        except FileNotFoundError:
            print(f"Error: file not found — {args.file}", file=sys.stderr)
            sys.exit(2)
        except ManifestError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        output = format_json(result) if args.format == "json" else format_text(result)
        print(output)
        sys.exit(0 if result["status"] == "PASS" else 1)

    if args.command == "validate":
        try:
            resolved_file = resolve_proof_pack_reference(args.file)
            data = json.loads(Path(resolved_file).read_text(encoding="utf-8"))
            validate_proof_pack(data)
        except FileNotFoundError:
            print(f"Error: file not found — {args.file}", file=sys.stderr)
            sys.exit(2)
        except ManifestError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        print(f"PASS: {resolved_file} matches the canonical proof-pack schema.")
        sys.exit(0)

    if args.command == "verify-report":
        try:
            report = json.loads(Path(args.file).read_text(encoding="utf-8"))
            ok = verify_report_digest(report)
            result = {
                "file": args.file,
                "valid": ok,
                "algorithm": report.get("report_digest", {}).get("algorithm")
                if isinstance(report.get("report_digest"), dict)
                else None,
                "expected": report.get("report_digest", {}).get("value")
                if isinstance(report.get("report_digest"), dict)
                else None,
                "actual": compute_report_sha256(report),
            }
        except FileNotFoundError:
            print(f"Error: file not found — {args.file}", file=sys.stderr)
            sys.exit(2)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if ok:
                print(f"PASS: {args.file} report_digest verified ({result['actual']}).")
            else:
                print(f"FAIL: {args.file} report_digest mismatch.")
                print(f"expected: {result['expected']}")
                print(f"actual  : {result['actual']}")
        sys.exit(0 if ok else 1)

    if args.command == "manifest":
        try:
            entries = assert_manifest_valid() if args.check else load_manifest()
        except FileNotFoundError:
            print("Error: examples/manifest.json not found", file=sys.stderr)
            sys.exit(2)
        except ManifestError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        if args.format == "json":
            print(json.dumps([entry.__dict__ for entry in entries], indent=2))
        else:
            if args.check:
                print("PASS: examples/manifest.json passed integrity checks.")
            for entry in entries:
                print(f"{entry.expected_status:<4} @{entry.id} :: {entry.path}")
        sys.exit(0)


if __name__ == "__main__":
    main()
