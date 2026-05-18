#!/usr/bin/env python3
"""
append_memory.py — Append entries to memory/*.jsonl files.

Usage:
  python execution/append_memory.py --file memory/task_history.jsonl --json '{"id": "T-001", ...}'
  python execution/append_memory.py --file memory/lessons.jsonl --json-file lesson.json

Exit 0 on success, non-zero on failure.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent

ALLOWED_FILES = {
    "memory/task_history.jsonl",
    "memory/decisions.jsonl",
    "memory/lessons.jsonl",
    "memory/risks.jsonl",
    "memory/agent_runs.jsonl",
    "memory/tool_calls.jsonl",
}


def validate_entry(entry: dict, filename: str) -> list[str]:
    """Validate entry has minimum required fields."""
    errors = []
    if "id" not in entry:
        errors.append("Entry missing required 'id' field")
    if "date" not in entry:
        errors.append("Entry missing required 'date' field")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a JSON entry to a memory JSONL file"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Relative path to JSONL file (e.g., memory/task_history.jsonl)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", help="JSON string to append")
    group.add_argument("--json-file", type=Path, help="JSON file to read and append")
    args = parser.parse_args()

    # Normalize path
    rel_path = args.file.replace("\\", "/").lstrip("/")
    if rel_path not in ALLOWED_FILES:
        print(
            f"ERROR: '{rel_path}' is not an allowed memory file.\n"
            f"Allowed: {sorted(ALLOWED_FILES)}",
            file=sys.stderr,
        )
        return 1

    target = ROOT / rel_path
    if not target.parent.exists():
        print(f"ERROR: Directory not found: {target.parent}", file=sys.stderr)
        return 1

    # Parse input
    if args.json:
        try:
            entry = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
            return 1
    else:
        if not args.json_file.exists():
            print(f"ERROR: JSON file not found: {args.json_file}", file=sys.stderr)
            return 1
        try:
            entry = json.loads(args.json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {args.json_file}: {e}", file=sys.stderr)
            return 1

    # Auto-inject date if missing
    if "date" not in entry:
        entry["date"] = date.today().isoformat()

    # Validate entry
    errors = validate_entry(entry, rel_path)
    if errors:
        print("ERROR: Entry validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    # Append (JSONL = one JSON object per line)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"OK — Appended entry id={entry.get('id')} to {rel_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
