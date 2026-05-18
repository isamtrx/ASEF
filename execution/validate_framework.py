#!/usr/bin/env python3
"""
validate_framework.py — Aggregate all ASEF validators and produce a structured report.

Usage:
  python execution/validate_framework.py
  python execution/validate_framework.py --json     # output JSON report

Exit 0 if ALL validators pass (status=PASS).
Exit 1 if any validator fails (status=FAIL or PARTIAL).
Exit 2 if a validator is missing but the corresponding layer exists.

Output format:
  FRAMEWORK VALIDATION REPORT
  Status: PASS / FAIL / PARTIAL
  Validators: ...
  Errors: ...
  Warnings: ...
  Next Actions: ...
"""
import json
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows (cp1252 terminals choke on ✓/✗)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent

VALIDATORS = [
    ("validate_directives",   ROOT / "execution" / "validate_directives.py",   ROOT / "directives"),
    ("validate_agents",       ROOT / "execution" / "validate_agents.py",        ROOT / "agents"),
    ("validate_skills",       ROOT / "execution" / "validate_skills.py",        ROOT / "skills"),
    ("validate_tools",        ROOT / "execution" / "validate_tools.py",         ROOT / "tools"),
    ("validate_contracts",    ROOT / "execution" / "validate_contracts.py",     ROOT / "contracts"),
    ("validate_schemas",      ROOT / "execution" / "validate_schemas.py",       ROOT / "schemas"),
    ("validate_registry",     ROOT / "execution" / "validate_registry.py",      ROOT / "registry"),
    ("validate_policies",     ROOT / "execution" / "validate_policies.py",      ROOT / "policies"),
    ("validate_orchestration",ROOT / "execution" / "validate_orchestration.py", ROOT / "orchestration"),
]

# Required files that must exist at root level
REQUIRED_GOVERNANCE_FILES = [
    "AGENTS.md",
    "SCOPE.md",
    "MEMORY.md",
    "DECISIONS.md",
    "directives/00_MASTER.md",
    "registry/agents.registry.json",
    "registry/skills.registry.json",
]


def run_validator(name: str, script: Path) -> tuple[str, list[str], list[str]]:
    """Run a validator script. Returns (status, errors, warnings)."""
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    output = (result.stdout + result.stderr).strip()
    errors = []
    warnings = []

    if result.returncode != 0:
        status = "FAIL"
        for line in output.splitlines():
            if line.strip():
                errors.append(line.strip())
    else:
        status = "PASS"
        for line in output.splitlines():
            if "warning" in line.lower():
                warnings.append(line.strip())

    return status, errors, warnings


def check_governance_files() -> list[str]:
    """Check that mandatory governance files exist."""
    missing = []
    for rel in REQUIRED_GOVERNANCE_FILES:
        if not (ROOT / rel).exists():
            missing.append(f"MISSING: {rel}")
    return missing


def main() -> int:
    output_json = "--json" in sys.argv

    results = {}
    all_errors: list[str] = []
    all_warnings: list[str] = []

    # Check governance files first
    gov_missing = check_governance_files()
    if gov_missing:
        for m in gov_missing:
            all_errors.append(m)

    # Run each validator
    for name, script, layer_dir in VALIDATORS:
        if not script.exists():
            if layer_dir.exists():
                results[name] = "MISSING (layer exists — validator needed)"
                all_warnings.append(f"MISSING_VALIDATOR: {name} — layer {layer_dir.name}/ exists")
            else:
                results[name] = "MISSING (layer absent)"
            continue

        status, errors, warnings = run_validator(name, script)
        results[name] = status
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    # Compute overall status
    statuses = list(results.values())
    has_fail = any("FAIL" in s for s in statuses)
    has_missing = any("MISSING" in s for s in statuses)
    has_gov_errors = bool(gov_missing)

    if has_fail or has_gov_errors:
        overall = "FAIL"
        exit_code = 1
    elif has_missing:
        overall = "PARTIAL"
        exit_code = 2
    else:
        overall = "PASS"
        exit_code = 0

    # Build next actions
    next_actions = []
    for name, status in results.items():
        if "FAIL" in status:
            next_actions.append(f"Fix {name} failures (see errors above)")
        elif "MISSING" in status and "layer exists" in status:
            next_actions.append(f"Create {name}.py validator for existing layer")
    for m in gov_missing:
        next_actions.append(f"Restore governance file: {m.replace('MISSING: ', '')}")
    if not next_actions:
        next_actions.append("All validators pass — run benchmarks to validate routing")

    if output_json:
        report = {
            "status": overall,
            "validators": results,
            "errors": all_errors,
            "warnings": all_warnings,
            "next_actions": next_actions,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("FRAMEWORK VALIDATION REPORT")
        print("=" * 60)
        print(f"\nStatus: {overall}\n")
        print("Validators:")
        for name, status in results.items():
            mark = "✓" if status == "PASS" else "✗"
            print(f"  {mark} {name}: {status}")
        if all_errors:
            print("\nErrors:")
            for e in all_errors:
                print(f"  - {e}")
        if all_warnings:
            print("\nWarnings:")
            for w in all_warnings:
                print(f"  ~ {w}")
        print("\nNext Actions:")
        for a in next_actions:
            print(f"  → {a}")
        print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
