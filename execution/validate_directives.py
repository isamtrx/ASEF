#!/usr/bin/env python3
"""
validate_directives.py — Validate that all directives/ files are well-formed
and referenced in registry/directives.registry.json.

Exit 0 if all checks pass, non-zero otherwise.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Mandatory Rules",
]

REQUIRED_DIRECTIVES = [
    "directives/00_MASTER.md",
]

REGISTRY_FILE = ROOT / "registry" / "directives.registry.json"
DIRECTIVES_DIR = ROOT / "directives"


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        print(f"ERROR: registry not found: {REGISTRY_FILE}")
        sys.exit(1)
    with REGISTRY_FILE.open() as f:
        return json.load(f)


def check_directive_file(path: Path, registry_paths: set) -> list[str]:
    errors = []
    content = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"  MISSING SECTION '{section}' in {rel}")

    if rel not in registry_paths:
        errors.append(f"  NOT IN REGISTRY: {rel}")

    return errors


def main() -> int:
    registry = load_registry()
    registry_paths = {item["path"] for item in registry.get("items", [])}

    all_errors = []

    # Check required directives exist
    for req in REQUIRED_DIRECTIVES:
        path = ROOT / req
        if not path.exists():
            all_errors.append(f"MISSING REQUIRED DIRECTIVE: {req}")

    # Check all .md files in directives/
    if not DIRECTIVES_DIR.exists():
        print(f"ERROR: directives/ directory not found at {DIRECTIVES_DIR}")
        return 1

    directive_files = list(DIRECTIVES_DIR.glob("*.md"))
    if not directive_files:
        print("WARNING: No directive files found in directives/")
        return 0

    for directive_file in sorted(directive_files):
        errors = check_directive_file(directive_file, registry_paths)
        all_errors.extend(errors)

    # Check registry entries have corresponding files
    for item in registry.get("items", []):
        path = ROOT / item["path"]
        if not path.exists():
            all_errors.append(
                f"REGISTRY ENTRY WITHOUT FILE: {item['path']}"
            )

    if all_errors:
        print("DIRECTIVE VALIDATION FAILED:")
        for err in all_errors:
            print(err)
        return 1

    print(
        f"OK — {len(directive_files)} directives validated, "
        f"{len(registry.get('items', []))} in registry"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
