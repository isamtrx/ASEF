#!/usr/bin/env python3
"""
bootstrap_framework.py — Install or prepare a controlled ASEF installation in a target repo.

This script inspects the target repo, auto-detects the stack, selects a profile,
and installs only the required layers — never overwriting existing files without backup.

Usage:
  python execution/bootstrap_framework.py --target PATH
  python execution/bootstrap_framework.py --target PATH --profile minimal
  python execution/bootstrap_framework.py --target PATH --dry-run
  python execution/bootstrap_framework.py --target PATH --force
  python execution/bootstrap_framework.py --target PATH --json

Exit 0 PASS, 1 PARTIAL/conflicts, 2 FAIL/invalid paths.
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bootstrap_framework",
        description="Install ASEF layers in a target repository according to a profile.",
    )
    parser.add_argument(
        "--target",
        required=True,
        metavar="PATH",
        help="Target repository root path.",
    )
    parser.add_argument(
        "--profile",
        default=None,
        metavar="NAME",
        help="ASEF profile to apply (minimal|frontend|backend|fullstack|agentic|enterprise). "
             "If omitted, auto-detected from target stack.",
    )
    parser.add_argument(
        "--source",
        default=None,
        metavar="PATH",
        help="ASEF source repository (default: parent of this script).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not modify anything — show what would be done.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow controlled overwrites of conflicting files (backup is created first).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output a machine-readable JSON report.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="WARNING: disable automatic backups (not recommended outside dry-run).",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Stack detection
# ---------------------------------------------------------------------------

def detect_stack(target: Path) -> dict[str, bool]:
    """Inspect target directory and return detected technology flags."""
    return {
        "python": any(
            (target / f).exists()
            for f in ("pyproject.toml", "requirements.txt", "setup.py")
        ),
        "node": (target / "package.json").exists(),
        "frontend": any(
            (target / f).exists()
            for f in (
                "vite.config.js", "vite.config.ts",
                "next.config.js", "next.config.ts",
                "nuxt.config.ts", "tailwind.config.js", "tailwind.config.ts",
            )
        ) or any(
            (target / d).is_dir() for d in ("src", "app", "pages")
        ),
        "backend": any(
            (target / f).exists()
            for f in ("pyproject.toml", "requirements.txt", "setup.py")
        ) or any(
            (target / d).is_dir() for d in ("api", "server")
        ),
        "git": (target / ".git").exists(),
        "tests": any(
            (target / d).is_dir() for d in ("tests", "test", "__tests__")
        ),
        "docs": (target / "README.md").exists() or (target / "docs").is_dir(),
        "existing_agents": any(
            (target / f).exists()
            for f in (
                "AGENTS.md", "CLAUDE.md", "COPILOT.md",
                ".github/copilot-instructions.md",
            )
        ),
    }


def auto_select_profile(stack: dict[str, bool]) -> str:
    """Return the best profile name based on detected stack."""
    if stack["frontend"] and stack["backend"]:
        return "fullstack"
    if stack["frontend"] and not stack["backend"]:
        return "frontend"
    if stack["backend"] and not stack["frontend"]:
        return "backend"
    return "minimal"


# ---------------------------------------------------------------------------
# Profile loading
# ---------------------------------------------------------------------------

def load_profile(source: Path, profile_name: str) -> tuple[dict | None, str | None]:
    """Load a profile JSON from source/profiles/. Returns (data, error)."""
    profile_path = source / "profiles" / f"{profile_name}.json"
    if not profile_path.exists():
        return None, f"Profile '{profile_name}' not found at {profile_path}"
    try:
        with profile_path.open(encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as exc:
        return None, f"Profile '{profile_name}' has invalid JSON: {exc}"


# ---------------------------------------------------------------------------
# Installation helpers
# ---------------------------------------------------------------------------

def _backup_path(target: Path, rel_path: str, timestamp: str) -> Path:
    return target / ".asef" / "backups" / timestamp / rel_path


def _ensure_dir(path: Path, dry_run: bool) -> None:
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)


def _write_state(target: Path, state: dict, dry_run: bool) -> None:
    if dry_run:
        return
    state_dir = target / ".asef"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / "bootstrap-state.json"
    with state_file.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _write_report(target: Path, report_content: str, dry_run: bool) -> Path | None:
    if dry_run:
        return None
    reports_dir = target / "artifacts" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = reports_dir / "bootstrap-report.md"
    with report_file.open("w", encoding="utf-8") as f:
        f.write(report_content)
    return report_file


def install_layer(
    source: Path,
    target: Path,
    layer: str,
    timestamp: str,
    dry_run: bool,
    force: bool,
    no_backup: bool,
) -> tuple[list[str], list[str], list[str], list[str]]:
    """
    Install a single layer from source into target.

    Returns (created, preserved, conflicts, backups).
    """
    created: list[str] = []
    preserved: list[str] = []
    conflicts: list[str] = []
    backups: list[str] = []

    # Layer is either a file (e.g. "AGENTS.md") or a directory
    src = source / layer
    dst = target / layer

    if not src.exists():
        # Source layer does not exist — skip silently (source may not have it)
        return created, preserved, conflicts, backups

    if src.is_file():
        if dst.exists():
            if force and not no_backup:
                backup = _backup_path(target, layer, timestamp)
                if not dry_run:
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dst, backup)
                backups.append(str(backup))
                if not dry_run:
                    shutil.copy2(src, dst)
                conflicts.append(layer)
            else:
                preserved.append(layer)
        else:
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            created.append(layer)

    elif src.is_dir():
        # Walk and copy files (skip Python cache artifacts)
        for src_file in sorted(src.rglob("*")):
            if src_file.is_dir():
                continue
            if "__pycache__" in src_file.parts or src_file.suffix == ".pyc":
                continue
            rel = src_file.relative_to(source)
            dst_file = target / rel
            rel_str = rel.as_posix()

            if dst_file.exists():
                if force and not no_backup:
                    backup = _backup_path(target, rel_str, timestamp)
                    if not dry_run:
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(dst_file, backup)
                    backups.append(str(backup))
                    if not dry_run:
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                    conflicts.append(rel_str)
                else:
                    preserved.append(rel_str)
            else:
                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                created.append(rel_str)

    return created, preserved, conflicts, backups


# ---------------------------------------------------------------------------
# Bootstrap report
# ---------------------------------------------------------------------------

def build_report(
    target: Path,
    source: Path,
    profile_name: str,
    stack: dict[str, bool],
    created: list[str],
    preserved: list[str],
    conflicts: list[str],
    backups: list[str],
    dry_run: bool,
) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    mode = "DRY-RUN" if dry_run else "APPLIED"
    detected_stack = [k for k, v in stack.items() if v]

    lines = [
        "# ASEF Bootstrap Report",
        "",
        f"Generated: {timestamp}",
        f"Mode: {mode}",
        "",
        "## Summary",
        f"Profile `{profile_name}` applied to `{target}` from `{source}`.",
        "",
        "## Target Repo",
        f"- Path: `{target}`",
        "",
        "## Detected Stack",
    ]
    for item in detected_stack:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Selected Profile",
        f"- `{profile_name}`",
        "",
        "## Files Created",
    ]
    lines += [f"- `{f}`" for f in created] or ["- (none)"]
    lines += ["", "## Files Preserved"]
    lines += [f"- `{f}`" for f in preserved] or ["- (none)"]
    lines += ["", "## Conflicts"]
    lines += [f"- `{f}`" for f in conflicts] or ["- (none)"]
    lines += ["", "## Backups"]
    lines += [f"- `{f}`" for f in backups] or ["- (none)"]
    lines += [
        "",
        "## Validators Available",
        "- Run `python execution/asef_doctor.py` in the target repo to verify installation.",
        "- Run `python execution/asef_doctor.py --capabilities` to check runtime mode support.",
        "",
        "## Runtime Execution Modes",
        "After installation, run_task.py supports four execution modes:",
        "",
        "| Mode | Command | Memory Status | Changes Applied |",
        "|------|---------|--------------|-----------------|",
        "| Dry-run | `--dry-run` or `--mode dry-run` | PLANNED_NOT_EXECUTED | No |",
        "| Assisted | `--mode assisted` | ASSISTED_PLAN_READY | No (Copilot prompt only) |",
        "| Audit-only | `--mode audit-only` | AUDIT_ONLY | No |",
        "| Live | (no flag) | completed / failed | Yes (requires orchestrator) |",
        "",
        "Example — generate a plan without executing agents:",
        "```bash",
        'python execution/run_task.py --task missions/active/MY-MISSION.md --dry-run',
        "```",
        "",
        "## Next Commands",
        "```powershell",
        f"cd {target}",
        "python execution/asef_doctor.py --skip-validators",
        "python execution/validate_framework.py",
        "```",
        "",
        "## Limitations",
        "- Only layers present in the source ASEF repo are copied.",
        "- Registry entries and memory files are not automatically updated for the target.",
        "- Tests in the source repo are not copied — add your own in tests/.",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_bootstrap(args: argparse.Namespace) -> int:
    # Resolve paths
    target = Path(args.target).resolve()
    source = Path(args.source).resolve() if args.source else Path(__file__).parent.parent.resolve()

    errors: list[str] = []

    if not target.exists() or not target.is_dir():
        msg = f"Target path does not exist or is not a directory: {target}"
        if args.output_json:
            print(json.dumps({"status": "FAIL", "error": msg}, indent=2))
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 2

    if not source.exists() or not source.is_dir():
        msg = f"Source path does not exist or is not a directory: {source}"
        if args.output_json:
            print(json.dumps({"status": "FAIL", "error": msg}, indent=2))
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 2

    if args.no_backup and not args.dry_run:
        print(
            "WARNING: --no-backup is set without --dry-run. "
            "Existing files may be overwritten without backup when --force is used.",
            file=sys.stderr,
        )

    # Detect stack
    stack = detect_stack(target)

    # Select profile
    profile_name = args.profile if args.profile else auto_select_profile(stack)
    profile_data, profile_err = load_profile(source, profile_name)
    if profile_err:
        msg = profile_err
        if args.output_json:
            print(json.dumps({"status": "FAIL", "error": msg}, indent=2))
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 2

    # Gather layers to install
    required_layers: list[str] = profile_data.get("required_layers", [])
    optional_layers: list[str] = profile_data.get("optional_layers", [])
    all_layers = required_layers + [
        l for l in optional_layers if (source / l).exists()
    ]

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    all_created: list[str] = []
    all_preserved: list[str] = []
    all_conflicts: list[str] = []
    all_backups: list[str] = []

    for layer in all_layers:
        created, preserved, conflicts, backups = install_layer(
            source=source,
            target=target,
            layer=layer,
            timestamp=timestamp,
            dry_run=args.dry_run,
            force=args.force,
            no_backup=args.no_backup,
        )
        all_created.extend(created)
        all_preserved.extend(preserved)
        all_conflicts.extend(conflicts)
        all_backups.extend(backups)

    # Also copy required scripts
    for script_rel in profile_data.get("required_scripts", []):
        created, preserved, conflicts, backups = install_layer(
            source=source,
            target=target,
            layer=script_rel,
            timestamp=timestamp,
            dry_run=args.dry_run,
            force=args.force,
            no_backup=args.no_backup,
        )
        all_created.extend(created)
        all_preserved.extend(preserved)
        all_conflicts.extend(conflicts)
        all_backups.extend(backups)

    # Copy manifest and profiles
    for extra in ("asef.manifest.json", "profiles"):
        created, preserved, conflicts, backups = install_layer(
            source=source,
            target=target,
            layer=extra,
            timestamp=timestamp,
            dry_run=args.dry_run,
            force=args.force,
            no_backup=args.no_backup,
        )
        all_created.extend(created)
        all_preserved.extend(preserved)
        all_conflicts.extend(conflicts)
        all_backups.extend(backups)

    # Determine status
    status = "PASS"
    if errors:
        status = "FAIL"
    elif all_conflicts:
        status = "PARTIAL"

    # Next actions
    next_actions: list[str] = []
    if args.dry_run:
        next_actions.append(
            f"Re-run without --dry-run to apply: "
            f"python execution/bootstrap_framework.py --target {target} --profile {profile_name}"
        )
    else:
        next_actions.append(
            f"Verify installation: cd {target} && python execution/asef_doctor.py --skip-validators"
        )
    if all_conflicts:
        next_actions.append(
            "Conflicts detected — review .asef/conflicts/ or re-run with --force to overwrite with backup"
        )

    # Build and write report
    report_content = build_report(
        target=target,
        source=source,
        profile_name=profile_name,
        stack=stack,
        created=all_created,
        preserved=all_preserved,
        conflicts=all_conflicts,
        backups=all_backups,
        dry_run=args.dry_run,
    )
    report_path = _write_report(target, report_content, args.dry_run)

    # Write bootstrap state
    state = {
        "timestamp": timestamp,
        "source": str(source),
        "profile": profile_name,
        "status": status,
        "created": all_created,
        "preserved": all_preserved,
        "conflicts": all_conflicts,
        "backups": all_backups,
    }
    _write_state(target, state, args.dry_run)

    # --- Output ---
    if args.output_json:
        output = {
            "status": status,
            "target": str(target),
            "source": str(source),
            "profile": profile_name,
            "detected_stack": stack,
            "dry_run": args.dry_run,
            "created": all_created,
            "preserved": all_preserved,
            "conflicts": all_conflicts,
            "backups": all_backups,
            "report_path": str(report_path) if report_path else None,
            "next_actions": next_actions,
            "errors": errors,
        }
        print(json.dumps(output, indent=2))
    else:
        mode_label = "[DRY-RUN] " if args.dry_run else ""
        print(f"{mode_label}ASEF BOOTSTRAP REPORT")
        print()
        print(f"Status:   {status}")
        print(f"Target:   {target}")
        print(f"Source:   {source}")
        print(f"Profile:  {profile_name}")
        print()
        detected_str = ", ".join(k for k, v in stack.items() if v)
        print(f"Detected stack: {detected_str or 'unknown'}")
        print()
        print(f"Files created:   {len(all_created)}")
        for f in all_created:
            print(f"  + {f}")
        print(f"Files preserved: {len(all_preserved)}")
        for f in all_preserved[:10]:
            print(f"  = {f}")
        if len(all_preserved) > 10:
            print(f"  ... and {len(all_preserved) - 10} more")
        if all_conflicts:
            print(f"Conflicts:       {len(all_conflicts)}")
            for f in all_conflicts:
                print(f"  ! {f}")
        if all_backups:
            print(f"Backups:         {len(all_backups)}")
        if errors:
            print()
            print("Errors:")
            for e in errors:
                print(f"  - {e}")
        if report_path:
            print()
            print(f"Report written: {report_path}")
        print()
        print("Next Actions:")
        for action in next_actions:
            print(f"  - {action}")

    if status == "FAIL":
        return 2
    if status == "PARTIAL":
        return 1
    return 0


def main() -> None:
    args = parse_args()
    sys.exit(run_bootstrap(args))


if __name__ == "__main__":
    main()
