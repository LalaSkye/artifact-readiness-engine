"""CLI entry point for the artifact readiness engine."""

import argparse
import sys

from .inspector import inspect_proof_pack
from .report import render_text, render_json


def main():
    parser = argparse.ArgumentParser(
        prog="artifact-readiness",
        description=(
            "Proof Structure Inspection Mode — checks whether a governance "
            "artefact can support a bounded claim. Does NOT certify compliance, "
            "safety, legality, or production readiness."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    inspect_parser = subparsers.add_parser(
        "inspect", help="Inspect a proof pack JSON file."
    )
    inspect_parser.add_argument("proof_pack", help="Path to proof-pack JSON file.")
    inspect_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )

    args = parser.parse_args()

    if args.command == "inspect":
        result = inspect_proof_pack(args.proof_pack)
        if args.format == "json":
            print(render_json(result))
        else:
            print(render_text(result))
        # Exit with non-zero if not PASS
        if result.overall_status == "PASS":
            sys.exit(0)
        elif result.overall_status == "HOLD":
            sys.exit(1)
        else:
            sys.exit(2)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
