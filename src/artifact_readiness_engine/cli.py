"""CLI entry point for the Proof Structure Inspector."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .inspector import inspect_file
from .report import format_json, format_text
from .validation import validate_proof_pack


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="artifact-readiness",
        description="Proof Structure Inspector — checks whether a proof pack supports a bounded claim.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect", help="Inspect a proof-pack JSON file.")
    inspect_cmd.add_argument("file", help="Path to proof-pack JSON")
    inspect_cmd.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    validate_cmd = sub.add_parser("validate", help="Validate proof-pack JSON against the canonical schema.")
    validate_cmd.add_argument("file", help="Path to proof-pack JSON")

    args = parser.parse_args()

    if args.command == "inspect":
        try:
            result = inspect_file(args.file)
        except FileNotFoundError:
            print(f"Error: file not found — {args.file}", file=sys.stderr)
            sys.exit(2)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        output = format_json(result) if args.format == "json" else format_text(result)
        print(output)
        sys.exit(0 if result["status"] == "PASS" else 1)

    if args.command == "validate":
        try:
            data = json.loads(Path(args.file).read_text(encoding="utf-8"))
            validate_proof_pack(data)
        except FileNotFoundError:
            print(f"Error: file not found — {args.file}", file=sys.stderr)
            sys.exit(2)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

        print(f"PASS: {args.file} matches the canonical proof-pack schema.")
        sys.exit(0)


if __name__ == "__main__":
    main()
