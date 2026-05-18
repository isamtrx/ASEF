#!/usr/bin/env python3
"""Validate all skill files against required sections and registry."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY_PATH = ROOT / "registry" / "skills.registry.json"

REQUIRED_SECTIONS = [
    "**id**",
    "**version**",
    "**agents**",
    "**tools_required**",
]

REQUIRED_EITHER = [
    ("## steps", "## rules"),  # at least one must be present
]

errors = []

# Load registry
if not REGISTRY_PATH.exists():
    print(f"MISSING: {REGISTRY_PATH}", file=sys.stderr)
    sys.exit(1)

with open(REGISTRY_PATH, encoding="utf-8") as f:
    registry = json.load(f)

registry_ids = {item["id"] for item in registry.get("items", [])}
registry_paths = {item["path"] for item in registry.get("items", [])}

# Validate each skill file
skill_files = list(SKILLS_DIR.glob("*.skill.md"))
if not skill_files:
    print("WARN: no .skill.md files found in skills/")

for skill_file in skill_files:
    content = skill_file.read_text(encoding="utf-8").lower()
    rel = skill_file.relative_to(ROOT).as_posix()

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"MISSING_SECTION: {rel} — '{section}'")

    for alt_a, alt_b in REQUIRED_EITHER:
        if alt_a not in content and alt_b not in content:
            errors.append(f"MISSING_SECTION: {rel} — needs '{alt_a}' or '{alt_b}'")

    # Check skill is in registry by path
    if rel not in registry_paths:
        errors.append(f"NOT_IN_REGISTRY: {rel}")

# Check registry paths exist
for item in registry.get("items", []):
    path = ROOT / item["path"]
    if not path.exists():
        errors.append(f"REGISTRY_DEAD_REF: {item['path']} (id={item['id']})")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print(f"OK — {len(skill_files)} skills validated, {len(registry_ids)} in registry")
