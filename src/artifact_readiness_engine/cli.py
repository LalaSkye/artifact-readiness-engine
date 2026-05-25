"""CLI entry point for the Proof Structure Inspector."""
from __future__ import annotations
import argparse
import sys

from .inspector import inspect_file
from .report import format_text, format_json


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


if __name__ == "__main__":
    main()
