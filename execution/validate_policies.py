#!/usr/bin/env python3
"""Validate all policy files against required fields and registry."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent.parent
POLICIES_DIR = ROOT / "policies"
REGISTRY_PATH = ROOT / "registry" / "policies.registry.json"

REQUIRED_FIELDS = [
    "**id**",
    "**source**",
    "**statut**",
]

errors = []

# Load registry
if not REGISTRY_PATH.exists():
    print(f"MISSING: {REGISTRY_PATH}", file=sys.stderr)
    sys.exit(1)

with open(REGISTRY_PATH, encoding="utf-8") as f:
    registry = json.load(f)

registry_paths = {item["path"] for item in registry.get("items", [])}

# Validate each policy file
policy_files = list(POLICIES_DIR.glob("*.md"))
if not policy_files:
    print("WARN: no .md files found in policies/")

for policy_file in policy_files:
    content = policy_file.read_text(encoding="utf-8").lower()
    rel = policy_file.relative_to(ROOT).as_posix()

    for field in REQUIRED_FIELDS:
        if field.lower() not in content:
            errors.append(f"MISSING_FIELD: {rel} — '{field}'")

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

print(f"OK — {len(policy_files)} policies validated, {len(registry_paths)} in registry")
