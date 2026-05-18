#!/usr/bin/env python3
"""
run_task.py -- Run a task through the full ASEF pipeline via asef/orchestrator.py.

Usage:
  python execution/run_task.py "Fix the bug in gates.py"
  python execution/run_task.py --task-type bugfix "Fix the bug in gates.py"
  python execution/run_task.py --dry-run "Fix the bug in gates.py"
  python execution/run_task.py --task missions/active/MISSION-001-repo-audit.md --dry-run
  python execution/run_task.py --task missions/active/MISSION-002.md --mode dry-run
  python execution/run_task.py --task missions/active/MISSION-002.md --mode assisted
  python execution/run_task.py --task missions/active/MISSION-002.md --mode audit-only

Exit 0 on success, non-zero on failure.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Add project root to path so asef/ can be imported
sys.path.insert(0, str(ROOT))


# Sensitive keywords that force approval_required for documentation_update tasks
_SENSITIVE_KEYWORDS: list[str] = [
    "policies/", "registry/", "schemas/", "execution/", "runtime/",
    ".env", "secrets", "delete", "remove", "overwrite", "destructive",
]


def _check_sensitive_paths(
    task_type: str,
    allowed_files: list[str],
    description: str,
) -> tuple[bool, str]:
    """Return (approval_required, reason) for documentation_update tasks.
    Checks allowed_files list and description for sensitive keywords.
    """
    if task_type != "documentation_update":
        return False, ""
    haystack = " ".join(allowed_files + [description]).lower()
    for kw in _SENSITIVE_KEYWORDS:
        if kw in haystack:
            return True, f"Sensitive path or destructive keyword detected: '{kw}'"
    return False, ""


def _write_memory(
    task_id: str,
    task_type: str,
    description: str,
    status: str,
    artifact_path: str | None = None,
    **extra: object,
) -> None:
    """Write task trace to memory/task_history.jsonl."""
    entry: dict = {
        "id": task_id,
        "date": datetime.now(timezone.utc).date().isoformat(),
        "task_id": task_id,
        "task_type": task_type,
        "description": description,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "artifact_path": artifact_path or "",
    }
    entry.update(extra)
    target = ROOT / "memory" / "task_history.jsonl"
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Memory  : written to memory/task_history.jsonl (id={task_id})")


def _write_artifact(task_id: str, task_type: str, plan: dict) -> Path:
    """Write orchestration plan artifact to artifacts/reports/."""
    today = datetime.now(timezone.utc).date().isoformat()
    reports_dir = ROOT / "artifacts" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = reports_dir / f"{today}_{task_id}_plan.json"
    artifact_file.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    rel = artifact_file.relative_to(ROOT).as_posix()
    print(f"Artifact: {rel}")
    return artifact_file


def _write_copilot_prompt(task_id: str, task_type: str, description: str,
                          plan: dict, mission_path: Path | None = None) -> Path:
    """Generate a scoped Copilot CLI prompt and save to artifacts/prompts/.

    Uses plan["allowed_files"] and plan["forbidden_files"] directly.
    Falls back to re-parsing the mission file only if both are absent from plan.
    """
    prompts_dir = ROOT / "artifacts" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = prompts_dir / f"{task_id}-copilot-prompt.md"

    agents = ", ".join(plan.get("planned_agents", []))
    skills = ", ".join(plan.get("planned_skills", []))
    tools = ", ".join(plan.get("planned_tools", []))
    gates = ", ".join(plan.get("planned_gates", []))
    contracts = ", ".join(plan.get("planned_contracts", []))
    risks = "\n".join(f"- {r}" for r in plan.get("risks", []))

    # Priority: use pre-parsed allowed_files from the plan (avoids re-parsing headings)
    _allowed = plan.get("allowed_files")
    if _allowed is not None:
        allowed_section = "\n".join(f"- {f}" for f in _allowed) if _allowed else ""
    elif mission_path and mission_path.exists():
        # Fallback: parse Scope section from mission file
        text = mission_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        in_scope = False
        in_allowed = False
        scope_lines: list[str] = []
        for line in lines:
            s = line.strip().lstrip("\\")
            if s.lower().startswith("## scope"):
                in_scope = True
                continue
            if in_scope and s.lstrip("\\").startswith("## "):
                break
            if not in_scope:
                continue
            sl = s.lower()
            if sl.startswith("allowed"):
                in_allowed = True
                continue
            if sl.startswith("forbidden"):
                in_allowed = False
                continue
            if in_allowed and s:
                scope_lines.append(s.lstrip("-").strip())
        allowed_section = "\n".join(f"- {f}" for f in scope_lines) if scope_lines else ""
    else:
        allowed_section = ""

    # Forbidden files: use plan value or fallback to hardcoded defaults
    _forbidden = plan.get("forbidden_files")
    if _forbidden:
        forbidden_section = "\n".join(f"- {f}" for f in _forbidden)
    else:
        forbidden_section = (
            "- AGENTS.md\n- SCOPE.md\n- PROJECT.md\n"
            "- docs/security/SECURITY.md\n- asef/__init__.py"
        )

    content = f"""# Copilot CLI Prompt -- {task_id}

**task_id**: {task_id}
**task_type**: {task_type}
**generated_at**: {datetime.now(timezone.utc).isoformat()}

## Task Objective

{description}

## Directives to Respect

Refer to the following directives before generating any code:
- directives/00_MASTER.md (mandatory)
- directives/11_TESTING.md (if adding tests)
- directives/12_QA.md (if QA task)
- directives/13_SECURITY.md (if security-relevant)

## Agents Assigned

{agents}

## Skills Required

{skills}

## Tools Allowed

{tools}

## Gates That Will Run

{gates}

## Contracts

{contracts or "(none specified)"}

## Allowed Files (ONLY modify these)

{allowed_section or "(none declared -- check mission Scope.Allowed)"}

## Forbidden Files (NEVER modify)

{forbidden_section}

## Required Tests

- Any new function must have at least one test
- Tests must fail on invalid input before passing on valid input
- Do not delete existing tests

## Rejection Criteria

- Copilot touches a forbidden file -> REJECT
- Copilot removes existing tests -> REJECT
- Copilot adds hardcoded secrets or credentials -> REJECT
- Copilot suggests "delete all" or destructive commands -> REJECT
- Patch adds > 150 lines unrelated to the objective -> REJECT
- Copilot claims tests pass without showing real output -> REJECT

## Expected Output Format

- Python code for test file (if test task)
- Minimal diff -- only the files needed
- Explanation of what was changed and why

## Risk Notes

{risks or "(none)"}

## Instruction

Generate a MINIMAL, TARGETED patch that addresses the objective above.
Do NOT modify any file outside the Allowed Files list.
Do NOT claim tests pass without showing their output.
Do NOT add features beyond the stated objective.
Do NOT commit automatically.
Do NOT change package dependencies.
"""

    prompt_file.write_text(content, encoding="utf-8")
    rel = prompt_file.relative_to(ROOT).as_posix()
    print(f"Prompt  : {rel}")
    return prompt_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a task through the ASEF G0->G7 pipeline"
    )
    parser.add_argument("description", nargs="?", help="Task description")
    parser.add_argument("--task", type=Path, help="Markdown task file")
    parser.add_argument(
        "--task-type",
        choices=[
            "bugfix", "feature", "review", "audit", "release", "security",
            "documentation", "documentation_update", "governance",
            "destructive_action", "add_test_coverage",
        ],
        help="Override task type classification",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate orchestration plan, write memory+artifact, do not execute agents "
             "(equivalent to --mode dry-run)",
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "assisted", "audit-only"],
        help=(
            "Execution mode: dry-run (plan only, equivalent to --dry-run), "
            "assisted (plan + controlled Copilot prompt, no patch applied), "
            "audit-only (read-only analysis, artifact written, memory=AUDIT_ONLY)"
        ),
    )
    args = parser.parse_args()

    # Resolve effective execution mode -- --dry-run and --mode are mutually exclusive
    if args.dry_run and args.mode:
        print(
            "ERROR: --dry-run and --mode are mutually exclusive. Use --mode dry-run.",
            file=sys.stderr,
        )
        return 1
    if args.dry_run:
        effective_mode: str | None = "dry-run"
    elif args.mode:
        effective_mode = args.mode
    else:
        effective_mode = None  # live run

    # Resolve description + task_type
    from execution.route_task import classify_task, generate_task_id, ROUTING_TABLE, extract_from_md

    if args.task:
        if not args.task.exists():
            print(f"ERROR: Task file not found: {args.task}", file=sys.stderr)
            return 1
        description, task_type_from_md = extract_from_md(args.task)
        task_type = args.task_type or task_type_from_md
    elif args.description:
        description = args.description
        task_type = args.task_type
    else:
        print("ERROR: Provide a description or --task <file>", file=sys.stderr)
        return 1

    if len(description.split()) < 2:
        print("ERROR: Description too short (minimum 2 words)", file=sys.stderr)
        return 1

    task_id = generate_task_id()
    if not task_type:
        task_type = classify_task(description)

    if task_type not in ROUTING_TABLE:
        known = ", ".join(ROUTING_TABLE.keys())
        print(f"ERROR: Unknown task_type '{task_type}'. Known types: {known}", file=sys.stderr)
        return 1

    route = ROUTING_TABLE[task_type]

    plan: dict = {
        "task_id": task_id,
        "task_type": task_type,
        "description": description,
        "planned_agents": route["planned_agents"],
        "planned_gates": route["planned_gates"],
        "approval_required": route["approval_required"],
        "planned_skills": route["planned_skills"],
        "planned_tools": route["planned_tools"],
        "risks": route["risks"],
    }
    if "planned_contracts" in route:
        plan["planned_contracts"] = route["planned_contracts"]
    if "status" in route:
        plan["status"] = route["status"]
    if "blocking_policies" in route:
        plan["blocking_policies"] = route["blocking_policies"]

    # Parse allowed_files from mission Scope section
    allowed_files: list[str] = []
    forbidden_always: list[str] = [
        "AGENTS.md", "SCOPE.md", "PROJECT.md",
        "docs/security/SECURITY.md", "asef/__init__.py",
    ]
    if args.task and args.task.exists():
        _text = args.task.read_text(encoding="utf-8")
        _in_scope = False
        _in_allowed = False
        for _ln in _text.splitlines():
            _s = _ln.strip().lstrip("\\")
            if _s.lower().startswith("## scope"):
                _in_scope = True
                continue
            if _in_scope and _s.lstrip("\\").startswith("## "):
                break  # next top-level section -- exit scope
            if not _in_scope:
                continue
            _sl = _s.lower()
            if _sl.startswith("allowed"):
                _in_allowed = True
                continue
            if _sl.startswith("forbidden"):
                _in_allowed = False
                continue
            if _in_allowed and _s:
                allowed_files.append(_s.lstrip("-").strip())

    today = datetime.now(timezone.utc).date().isoformat()
    plan["allowed_files"] = allowed_files
    plan["forbidden_files"] = forbidden_always
    plan["artifact_plan"] = f"artifacts/reports/{today}_{task_id}_plan.json"
    plan["memory_update_plan"] = {
        "file": "memory/task_history.jsonl",
        "entry": {"task_id": task_id, "task_type": task_type, "description": description},
    }

    # Override approval_required for documentation_update if sensitive paths found
    sensitive, sensitive_reason = _check_sensitive_paths(task_type, allowed_files, description)
    if sensitive:
        plan["approval_required"] = True
        plan["approval_reason"] = sensitive_reason

    print(f"Task ID    : {task_id}")
    print(f"Task Type  : {task_type}")
    print(f"Description: {description}")
    print(f"Gates      : {', '.join(route['planned_gates'])}")
    print(f"Agents     : {', '.join(route['planned_agents']) or '(none -- blocked)'}")
    print(f"Approval   : {'YES -- BLOCKED' if plan['approval_required'] else 'no'}")
    if effective_mode:
        print(f"Mode       : {effective_mode}")

    if effective_mode == "dry-run":
        artifact_path = _write_artifact(task_id, task_type, plan)
        _write_copilot_prompt(task_id, task_type, description, plan,
                              mission_path=args.task if args.task else None)
        _write_memory(
            task_id, task_type, description, "PLANNED_NOT_EXECUTED",
            artifact_path.relative_to(ROOT).as_posix(),
            mode="dry-run",
            executed_changes=False,
        )
        print("\nDRY RUN -- Plan generated, memory+artifact+prompt written, no agents executed.")
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0

    elif effective_mode == "assisted":
        artifact_path = _write_artifact(task_id, task_type, plan)
        prompt_path = _write_copilot_prompt(
            task_id, task_type, description, plan,
            mission_path=args.task if args.task else None,
        )
        _write_memory(
            task_id, task_type, description, "ASSISTED_PLAN_READY",
            artifact_path.relative_to(ROOT).as_posix(),
            executed_changes=False,
            prompt_path=prompt_path.relative_to(ROOT).as_posix(),
        )
        print("\nASSISTED -- Plan + Copilot prompt generated. No patch applied automatically.")
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        print(f"\n--- Copilot Prompt ({prompt_path.relative_to(ROOT).as_posix()}) ---")
        _prompt_text = prompt_path.read_text(encoding="utf-8")
        _out_enc = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
        print(_prompt_text.encode(_out_enc, errors="replace").decode(_out_enc))
        return 0

    elif effective_mode == "audit-only":
        artifact_path = _write_artifact(task_id, task_type, plan)
        _write_memory(
            task_id, task_type, description, "AUDIT_ONLY",
            artifact_path.relative_to(ROOT).as_posix(),
            executed_changes=False,
        )
        print("\nAUDIT ONLY -- Read-only analysis. Artifact written, memory status=AUDIT_ONLY, no patch.")
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0

    # Live run -- requires asef.orchestrator
    try:
        from asef.orchestrator import Orchestrator
    except ImportError:
        blocked = {
            "status": "BLOCKED_RUNTIME_MISSING",
            "reason": "Live execution requires asef.orchestrator -- module not found",
            "safe_alternatives": ["--mode dry-run", "--mode assisted", "--mode audit-only"],
        }
        print(json.dumps(blocked, indent=2, ensure_ascii=False))
        return 1

    try:
        orchestrator = Orchestrator()
        result = orchestrator.run(task_id=task_id, description=description)

        if result.get("status") == "completed":
            artifact_path = _write_artifact(task_id, task_type, plan)
            _write_memory(task_id, task_type, description, "completed",
                          artifact_path.relative_to(ROOT).as_posix())
            print(f"\nOK -- Task {task_id} completed")
            gates_passed = result.get("gates_passed", [])
            print(f"Gates passed: {', '.join(gates_passed)}")
            return 0
        else:
            _write_memory(task_id, task_type, description, "failed")
            print(f"\nFAILED -- Task {task_id} did not complete")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 1

    except Exception as e:
        print(f"ERROR: Pipeline execution failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())