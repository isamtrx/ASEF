#!/usr/bin/env python3
"""Validate all tool files against required sections and registry."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent.parent
TOOLS_DIR = ROOT / "tools"
REGISTRY_PATH = ROOT / "registry" / "tools.registry.json"

REQUIRED_SECTIONS = [
    "**id**",
    "**implementation**",
    "## input",
    "## output",
]

errors = []

# Load registry
if not REGISTRY_PATH.exists():
    print(f"MISSING: {REGISTRY_PATH}", file=sys.stderr)
    sys.exit(1)

with open(REGISTRY_PATH, encoding="utf-8") as f:
    registry = json.load(f)

registry_paths = {item["path"] for item in registry.get("items", [])}

# Validate each tool file
tool_files = list(TOOLS_DIR.glob("*.tool.md"))
if not tool_files:
    print("WARN: no .tool.md files found in tools/")

for tool_file in tool_files:
    content = tool_file.read_text(encoding="utf-8").lower()
    rel = tool_file.relative_to(ROOT).as_posix()

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"MISSING_SECTION: {rel} — '{section}'")

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

print(f"OK — {len(tool_files)} tools validated, {len(registry_paths)} in registry")
