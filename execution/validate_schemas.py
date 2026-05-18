#!/usr/bin/env python3
"""
validate_schemas.py — Validate that all schemas/*.json files are valid JSON Schema.

Requires: jsonschema (pip install jsonschema)

Exit 0 if all checks pass, non-zero otherwise.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = ROOT / "schemas"

REQUIRED_SCHEMAS = [
    "task.schema.json",
    "agent_output.schema.json",
    "orchestration_plan.schema.json",
    "tool_call.schema.json",
    "skill_output.schema.json",
    "memory_entry.schema.json",
    "registry.schema.json",
]


def validate_schema_file(path: Path) -> list[str]:
    errors = []
    rel = path.relative_to(ROOT).as_posix()

    # 1. Valid JSON
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON in {rel}: {e}")
        return errors

    # 2. Has $schema field
    if "$schema" not in schema:
        errors.append(f"MISSING '$schema' field in {rel}")

    # 3. Has type or $ref or oneOf/anyOf
    if not any(k in schema for k in ("type", "$ref", "oneOf", "anyOf", "allOf")):
        errors.append(f"MISSING type definition in {rel}")

    # 4. Try to validate with jsonschema if available
    try:
        import jsonschema
        jsonschema.Draft7Validator.check_schema(schema)
    except ImportError:
        errors.append(f"  WARN: jsonschema not installed, skipping meta-validation for {rel}")
    except jsonschema.SchemaError as e:
        errors.append(f"INVALID SCHEMA in {rel}: {e.message}")

    return errors


def main() -> int:
    all_errors = []
    warnings = []

    if not SCHEMAS_DIR.exists():
        print(f"ERROR: schemas/ directory not found at {SCHEMAS_DIR}")
        return 1

    # Check required schemas exist
    for required in REQUIRED_SCHEMAS:
        path = SCHEMAS_DIR / required
        if not path.exists():
            all_errors.append(f"MISSING REQUIRED SCHEMA: {required}")

    # Validate all schema files found
    schema_files = list(SCHEMAS_DIR.glob("*.json"))
    validated = 0
    for schema_file in sorted(schema_files):
        errors = validate_schema_file(schema_file)
        real_errors = [e for e in errors if not e.startswith("  WARN:")]
        warns = [e for e in errors if e.startswith("  WARN:")]
        all_errors.extend(real_errors)
        warnings.extend(warns)
        if not real_errors:
            validated += 1

    for w in warnings:
        print(w)

    if all_errors:
        print("SCHEMA VALIDATION FAILED:")
        for err in all_errors:
            print(err)
        return 1

    print(f"OK — {validated}/{len(schema_files)} schemas validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
