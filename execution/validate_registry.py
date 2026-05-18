#!/usr/bin/env python3
"""
validate_registry.py — Validate all registry/*.json files:
  1. Are valid JSON
  2. Match registry.schema.json structure
  3. Every "path" entry in each registry corresponds to an existing file

Exit 0 if all checks pass, non-zero otherwise.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
REGISTRY_DIR = ROOT / "registry"

REGISTRY_FILES = [
    "agents.registry.json",
    "skills.registry.json",
    "tools.registry.json",
    "workflows.registry.json",
    "directives.registry.json",
    "policies.registry.json",
    "gates.registry.json",
]

REQUIRED_ITEM_FIELDS = {"id", "name", "path", "status"}


def validate_registry_file(path: Path) -> list[str]:
    errors = []
    rel = path.relative_to(ROOT).as_posix()

    # 1. Valid JSON
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON in {rel}: {e}")
        return errors

    # 2. Required top-level fields
    for field in ("version", "items"):
        if field not in data:
            errors.append(f"MISSING FIELD '{field}' in {rel}")

    items = data.get("items", [])
    if not isinstance(items, list):
        errors.append(f"'items' must be an array in {rel}")
        return errors

    # 3. Each item has required fields and file exists
    for i, item in enumerate(items):
        missing = REQUIRED_ITEM_FIELDS - set(item.keys())
        if missing:
            errors.append(
                f"  item[{i}] missing fields {missing} in {rel}"
            )

        item_path_str = item.get("path", "")
        if item_path_str and not item_path_str.startswith("http"):
            # Anchored references like "orchestration/WORKFLOWS.md#SECTION"
            file_path_str = item_path_str.split("#")[0]
            file_path = ROOT / file_path_str
            if not file_path.exists():
                errors.append(
                    f"  FILE NOT FOUND: {item_path_str} (item id={item.get('id', i)}) in {rel}"
                )

    return errors


def main() -> int:
    all_errors = []

    if not REGISTRY_DIR.exists():
        print(f"ERROR: registry/ directory not found at {REGISTRY_DIR}")
        return 1

    found = 0
    for registry_name in REGISTRY_FILES:
        path = REGISTRY_DIR / registry_name
        if not path.exists():
            all_errors.append(f"MISSING REGISTRY FILE: {registry_name}")
            continue
        found += 1
        errors = validate_registry_file(path)
        all_errors.extend(errors)

    if all_errors:
        print("REGISTRY VALIDATION FAILED:")
        for err in all_errors:
            print(err)
        return 1

    print(f"OK — {found}/{len(REGISTRY_FILES)} registry files validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
