#!/usr/bin/env python3
"""
asef_doctor.py — Diagnose the local state of the ASEF framework.

Usage:
  python execution/asef_doctor.py [options]

Exit 0 if PASS, 1 if PARTIAL or FAIL, 2 if internal error or invalid root.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="asef_doctor",
        description="Diagnose the state of an ASEF framework installation.",
    )
    parser.add_argument(
        "--root",
        default=None,
        metavar="PATH",
        help="Root path of the ASEF repo to diagnose (default: parent of this script).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output a machine-readable JSON report.",
    )
    parser.add_argument(
        "--skip-validators",
        action="store_true",
        help="Do not invoke execution/validate_framework.py.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return FAIL instead of PARTIAL when there are important warnings.",
    )
    parser.add_argument(
        "--capabilities",
        action="store_true",
        help=(
            "Check runtime execution capabilities: "
            "whether run_task.py exposes --mode, "
            "artifacts/prompts/ is writable, "
            "memory/task_history.jsonl is accessible."
        ),
    )
    return parser.parse_args()


def load_manifest(root: Path) -> tuple[dict | None, str | None]:
    """Load and validate asef.manifest.json. Returns (data, error_string)."""
    manifest_path = root / "asef.manifest.json"
    if not manifest_path.exists():
        return None, f"asef.manifest.json not found at {manifest_path}"
    try:
        with manifest_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as exc:
        return None, f"asef.manifest.json is invalid JSON: {exc}"


def load_profiles(root: Path) -> tuple[dict[str, dict], list[str]]:
    """Load all JSON files in profiles/. Returns (name->data, errors)."""
    profiles_dir = root / "profiles"
    results: dict[str, dict] = {}
    errors: list[str] = []
    if not profiles_dir.exists():
        errors.append("profiles/ directory not found")
        return results, errors
    for json_file in sorted(profiles_dir.glob("*.json")):
        try:
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
            results[json_file.stem] = data
        except json.JSONDecodeError as exc:
            errors.append(f"profiles/{json_file.name}: invalid JSON — {exc}")
    return results, errors


def check_required_layers(root: Path, manifest: dict) -> tuple[list[str], list[str]]:
    """Check presence of required layers. Returns (passes, failures)."""
    passes: list[str] = []
    failures: list[str] = []
    for layer in manifest.get("required_layers", []):
        path = root / layer
        if path.exists():
            passes.append(layer)
        else:
            failures.append(layer)
    return passes, failures


def check_required_scripts(root: Path, manifest: dict) -> tuple[list[str], list[str]]:
    """Check presence of required scripts. Returns (passes, failures)."""
    passes: list[str] = []
    failures: list[str] = []
    for script in manifest.get("required_scripts", []):
        path = root / script
        if path.exists():
            passes.append(script)
        else:
            failures.append(script)
    return passes, failures


def run_validators(root: Path) -> tuple[str, list[str]]:
    """
    Run execution/validate_framework.py if present.
    Returns (status: PASS|PARTIAL|FAIL|SKIPPED, details).
    """
    validator = root / "execution" / "validate_framework.py"
    if not validator.exists():
        return "SKIPPED", ["validate_framework.py not found — skipped"]

    try:
        result = subprocess.run(
            [sys.executable, str(validator)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(root),
        )
        output_lines = (result.stdout + result.stderr).strip().splitlines()
        if result.returncode == 0:
            return "PASS", output_lines
        else:
            return "FAIL", output_lines
    except subprocess.TimeoutExpired:
        return "FAIL", ["validate_framework.py timed out after 60s"]
    except Exception as exc:
        return "FAIL", [f"validate_framework.py raised exception: {exc}"]


def compute_overall_status(
    manifest_ok: bool,
    profiles_ok: bool,
    layers_ok: bool,
    scripts_ok: bool,
    validators_status: str,
    errors: list[str],
    warnings: list[str],
    strict: bool,
) -> str:
    if errors:
        return "FAIL"
    all_ok = manifest_ok and profiles_ok and layers_ok and scripts_ok
    if not all_ok:
        return "FAIL"
    if validators_status in ("FAIL",):
        return "PARTIAL"
    if validators_status == "PARTIAL":
        return "PARTIAL"
    if warnings and strict:
        return "FAIL"
    if warnings:
        return "PARTIAL"
    return "PASS"


def check_capabilities(root: Path) -> tuple[list[str], list[str], list[str]]:
    """Check runtime execution capabilities of run_task.py.

    Returns (passes, warnings, failures).
    """
    passes: list[str] = []
    warnings_list: list[str] = []
    failures: list[str] = []

    run_task = root / "execution" / "run_task.py"
    if not run_task.exists():
        failures.append("execution/run_task.py not found")
        return passes, warnings_list, failures

    src = run_task.read_text(encoding="utf-8")

    # Check --mode flag is declared
    if '"--mode"' in src or "'--mode'" in src:
        passes.append("run_task.py declares --mode flag")
    else:
        failures.append("run_task.py does not declare --mode flag")

    # Check --dry-run mutual exclusion
    if "mutually exclusive" in src:
        passes.append("run_task.py enforces --dry-run/--mode mutual exclusion")
    else:
        warnings_list.append("run_task.py may not enforce --dry-run/--mode mutual exclusion")

    # Check memory statuses
    for status in ("PLANNED_NOT_EXECUTED", "ASSISTED_PLAN_READY", "AUDIT_ONLY"):
        if status in src:
            passes.append(f"run_task.py uses memory status: {status}")
        else:
            failures.append(f"run_task.py missing memory status: {status}")

    # Check BLOCKED_RUNTIME_MISSING
    if "BLOCKED_RUNTIME_MISSING" in src:
        passes.append("run_task.py returns BLOCKED_RUNTIME_MISSING for missing orchestrator")
    else:
        warnings_list.append("run_task.py may not return structured BLOCKED_RUNTIME_MISSING JSON")

    # Check executed_changes field
    if "executed_changes" in src:
        passes.append("run_task.py writes executed_changes field to memory")
    else:
        failures.append("run_task.py does not write executed_changes field to memory")

    # Check artifacts/prompts/ directory is creatable
    prompts_dir = root / "artifacts" / "prompts"
    if prompts_dir.exists():
        passes.append("artifacts/prompts/ directory exists")
    else:
        try:
            prompts_dir.mkdir(parents=True, exist_ok=True)
            passes.append("artifacts/prompts/ directory created")
        except OSError as e:
            failures.append(f"Cannot create artifacts/prompts/: {e}")

    # Check memory/task_history.jsonl is accessible
    history = root / "memory" / "task_history.jsonl"
    if history.exists():
        passes.append("memory/task_history.jsonl exists and is accessible")
    else:
        parent = history.parent
        if parent.exists():
            warnings_list.append("memory/task_history.jsonl does not exist yet (will be created on first run)")
        else:
            failures.append("memory/ directory not found — task history cannot be written")

    return passes, warnings_list, failures


def run_doctor(args: argparse.Namespace) -> int:
    # Resolve root
    if args.root:
        root = Path(args.root).resolve()
    else:
        root = Path(__file__).parent.parent.resolve()

    if not root.exists() or not root.is_dir():
        msg = f"Root path does not exist or is not a directory: {root}"
        if args.output_json:
            print(json.dumps({"status": "FAIL", "error": msg}, indent=2))
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, str] = {}

    # 1. Manifest
    manifest, manifest_err = load_manifest(root)
    if manifest_err:
        errors.append(manifest_err)
        checks["manifest"] = "FAIL"
        manifest_ok = False
    else:
        checks["manifest"] = "PASS"
        manifest_ok = True

    version = manifest.get("version", "unknown") if manifest else "unknown"

    # 2. Profiles
    profiles_data, profile_errors = load_profiles(root)
    if profile_errors:
        for e in profile_errors:
            errors.append(e)
        checks["profiles"] = "FAIL" if not profiles_data else "PARTIAL"
        profiles_ok = len(profile_errors) == 0
    elif not profiles_data:
        errors.append("profiles/ exists but contains no valid JSON profiles")
        checks["profiles"] = "FAIL"
        profiles_ok = False
    else:
        checks["profiles"] = "PASS"
        profiles_ok = True

    # Check manifest references valid profiles
    if manifest and profiles_data:
        for pname in manifest.get("profiles", []):
            if pname not in profiles_data:
                warnings.append(
                    f"Manifest references profile '{pname}' but profiles/{pname}.json not found"
                )

    # 3. Required layers
    layers_pass, layers_fail = [], []
    if manifest:
        layers_pass, layers_fail = check_required_layers(root, manifest)
    if layers_fail:
        for layer in layers_fail:
            errors.append(f"Required layer missing: {layer}")
        checks["required_layers"] = "FAIL"
        layers_ok = False
    else:
        checks["required_layers"] = "PASS"
        layers_ok = True

    # 4. Required scripts
    scripts_pass, scripts_fail = [], []
    if manifest:
        scripts_pass, scripts_fail = check_required_scripts(root, manifest)
    if scripts_fail:
        for script in scripts_fail:
            errors.append(f"Required script missing: {script}")
        checks["required_scripts"] = "FAIL"
        scripts_ok = False
    else:
        checks["required_scripts"] = "PASS"
        scripts_ok = True

    # 5. Memory
    memory_path = root / "memory"
    if memory_path.exists():
        checks["memory"] = "PASS"
    else:
        errors.append("memory/ directory not found")
        checks["memory"] = "FAIL"

    # 6. Artifacts
    artifacts_path = root / "artifacts"
    if artifacts_path.exists():
        checks["artifacts"] = "PASS"
    else:
        errors.append("artifacts/ directory not found")
        checks["artifacts"] = "FAIL"

    # 7. Validators
    if args.skip_validators:
        checks["validators"] = "SKIPPED"
        validators_status = "SKIPPED"
        validators_details: list[str] = ["--skip-validators flag set — skipped"]
    else:
        validators_status, validators_details = run_validators(root)
        checks["validators"] = validators_status
        if validators_status == "FAIL":
            warnings.append("validate_framework.py returned non-zero exit code")

    # 8. Capabilities (optional — only when --capabilities flag set)
    cap_passes: list[str] = []
    cap_warnings: list[str] = []
    cap_failures: list[str] = []
    if getattr(args, "capabilities", False):
        cap_passes, cap_warnings, cap_failures = check_capabilities(root)
        checks["capabilities"] = "FAIL" if cap_failures else ("PARTIAL" if cap_warnings else "PASS")
        for f in cap_failures:
            errors.append(f"[capabilities] {f}")
        for w in cap_warnings:
            warnings.append(f"[capabilities] {w}")

    # Compute overall status
    status = compute_overall_status(
        manifest_ok, profiles_ok, layers_ok, scripts_ok,
        validators_status, errors, warnings, args.strict,
    )

    # Next actions
    next_actions: list[str] = []
    if not manifest_ok:
        next_actions.append("Create asef.manifest.json (see asef.manifest.json template)")
    if not profiles_ok:
        next_actions.append("Fix or create profiles/*.json")
    if layers_fail:
        next_actions.append(f"Create missing layers: {', '.join(layers_fail)}")
    if scripts_fail:
        next_actions.append(f"Implement missing scripts: {', '.join(scripts_fail)}")
    if validators_status == "FAIL":
        next_actions.append("Fix validate_framework.py failures (run with --skip-validators to isolate)")
    if not next_actions and status == "PASS":
        next_actions.append("No action required — framework is healthy")

    # --- Output ---
    if args.output_json:
        report = {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "root": str(root),
            "version": version,
            "profile_support": list(profiles_data.keys()),
            "checks": checks,
            "errors": errors,
            "warnings": warnings,
            "next_actions": next_actions,
            "details": {
                "layers_present": layers_pass,
                "layers_missing": layers_fail,
                "scripts_present": scripts_pass,
                "scripts_missing": scripts_fail,
                "validators": validators_details,
            },
        }
        if getattr(args, "capabilities", False):
            report["capabilities"] = {
                "passes": cap_passes,
                "warnings": cap_warnings,
                "failures": cap_failures,
            }
        print(json.dumps(report, indent=2))
    else:
        print("ASEF DOCTOR REPORT")
        print()
        print(f"Status: {status}")
        print()
        print(f"Root:            {root}")
        print(f"Version:         {version}")
        print(f"Profile support: {', '.join(profiles_data.keys()) or 'none'}")
        print()
        print("Checks:")
        for check_name, check_status in checks.items():
            print(f"  - {check_name}: {check_status}")
        if errors:
            print()
            print("Errors:")
            for e in errors:
                print(f"  - {e}")
        if warnings:
            print()
            print("Warnings:")
            for w in warnings:
                print(f"  - {w}")
        if getattr(args, "capabilities", False):
            print()
            print("Capabilities:")
            for item in cap_passes:
                print(f"  [PASS] {item}")
            for item in cap_warnings:
                print(f"  [WARN] {item}")
            for item in cap_failures:
                print(f"  [FAIL] {item}")
        print()
        print("Next Actions:")
        for action in next_actions:
            print(f"  - {action}")

    if status == "PASS":
        return 0
    return 1


def main() -> None:
    args = parse_args()
    sys.exit(run_doctor(args))


if __name__ == "__main__":
    main()
