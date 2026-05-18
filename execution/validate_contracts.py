#!/usr/bin/env python3
"""Validate all contract files against required sections and referenced schemas."""
from pathlib import Path
import sys
import re

ROOT = Path(__file__).parent.parent
CONTRACTS_DIR = ROOT / "contracts"
SCHEMAS_DIR = ROOT / "schemas"

REQUIRED_SECTIONS = [
    "## description",
    "## champs obligatoires",
    "## exemple",
]

errors = []

contract_files = list(CONTRACTS_DIR.glob("*_CONTRACT.md"))
if not contract_files:
    print("WARN: no CONTRACT files found in contracts/")

for contract_file in contract_files:
    content = contract_file.read_text(encoding="utf-8")
    content_lower = content.lower()
    rel = contract_file.relative_to(ROOT).as_posix()

    for section in REQUIRED_SECTIONS:
        if section not in content_lower:
            errors.append(f"MISSING_SECTION: {rel} — '{section}'")

    # Check referenced schema exists
    schema_refs = re.findall(r"schemas/[\w_]+\.schema\.json", content)
    for schema_ref in schema_refs:
        schema_path = ROOT / schema_ref
        if not schema_path.exists():
            errors.append(f"DEAD_SCHEMA_REF: {rel} references {schema_ref} which does not exist")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print(f"OK — {len(contract_files)} contracts validated")
