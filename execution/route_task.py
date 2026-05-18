#!/usr/bin/env python3
"""
route_task.py — Accept a task description and output a JSON orchestration plan.

Usage:
  python execution/route_task.py "Fix the authentication bug in asef/gates.py"
  python execution/route_task.py --task-type feature "Add retry logic to LLM calls"
  python execution/route_task.py --json-input task.json

Exit 0 with JSON output on stdout, non-zero on failure.
"""
import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent

ROUTING_TABLE: dict[str, dict] = {
    "destructive_action": {
        "planned_agents": [],
        "planned_skills": [],
        "planned_tools": [],
        "planned_gates": ["G0"],
        "approval_required": True,
        "estimated_steps": 0,
        "risks": ["BLOCKED — destructive actions require explicit human approval"],
        "status": "BLOCKED_BY_APPROVAL_REQUIRED",
        "blocking_policies": [
            "policies/DESTRUCTIVE_ACTIONS.md",
            "policies/HUMAN_APPROVAL.md",
            "policies/TOOL_ACCESS.md",
        ],
    },
    "bugfix": {
        "planned_agents": ["orchestrator", "developer", "qa", "security", "docs"],
        "planned_skills": ["code_review", "test_generation", "security_review", "memory_update", "documentation_update"],
        "planned_tools": ["read_file", "write_file", "run_command", "escalate"],
        "planned_gates": ["G0", "G1", "G3", "G4", "G5", "G6"],
        "approval_required": False,
        "estimated_steps": 7,
        "risks": ["regression risk if tests incomplete"],
    },
    "feature": {
        "planned_agents": ["orchestrator", "architect", "developer", "qa", "security", "docs"],
        "planned_skills": ["code_review", "test_generation", "security_review", "memory_update", "documentation_update"],
        "planned_tools": ["read_file", "write_file", "run_command", "escalate"],
        "planned_gates": ["G0", "G1", "G2", "G3", "G4", "G5", "G6"],
        "approval_required": False,
        "estimated_steps": 9,
        "risks": ["ADR required if structural decision", "scope creep risk"],
    },
    "review": {
        "planned_agents": ["orchestrator", "qa", "docs"],
        "planned_skills": ["code_review", "documentation_update"],
        "planned_tools": ["read_file", "list_directory"],
        "planned_gates": ["G0", "G1", "G3"],
        "approval_required": False,
        "estimated_steps": 4,
        "risks": [],
    },
    "audit": {
        "planned_agents": ["orchestrator", "qa", "security", "docs"],
        "planned_skills": ["repo_audit", "security_review", "documentation_update"],
        "planned_tools": ["read_file", "list_directory", "run_command", "write_file"],
        "planned_gates": ["G0", "G1", "G3", "G4", "G5"],
        "approval_required": False,
        "estimated_steps": 6,
        "risks": ["audit findings may require follow-up tasks"],
    },
    "release": {
        "planned_agents": ["orchestrator", "qa", "security", "docs"],
        "planned_skills": ["security_review", "documentation_update", "memory_update"],
        "planned_tools": ["read_file", "list_directory", "run_command", "write_file"],
        "planned_gates": ["G0", "G1", "G3", "G4", "G5", "G6", "G7"],
        "approval_required": True,
        "estimated_steps": 10,
        "risks": ["G7 human approval always required", "no automated release"],
    },
    "security": {
        "planned_agents": ["orchestrator", "security", "docs"],
        "planned_skills": ["security_review", "documentation_update"],
        "planned_tools": ["read_file", "list_directory", "run_command", "write_file", "escalate"],
        "planned_gates": ["G0", "G1", "G5"],
        "approval_required": False,
        "estimated_steps": 5,
        "risks": ["critical findings trigger immediate escalation"],
    },
    "documentation": {
        "planned_agents": ["orchestrator", "docs"],
        "planned_skills": ["documentation_update", "memory_update"],
        "planned_tools": ["read_file", "write_file"],
        "planned_gates": ["G0", "G1", "G6"],
        "approval_required": False,
        "estimated_steps": 4,
        "risks": [],
    },
    "documentation_update": {
        "planned_agents": ["orchestrator", "docs", "qa"],
        "planned_skills": ["documentation_update", "memory_update"],
        "planned_tools": ["read_file", "write_file"],
        "planned_gates": ["scope_gate", "documentation_quality_gate", "memory_update_gate", "diff_review_gate"],
        "approval_required": False,
        "estimated_steps": 4,
        "risks": ["approval required if policies, security, registry, schemas, or destructive action are touched"],
    },
    "governance": {
        "planned_agents": ["orchestrator", "architect", "docs"],
        "planned_skills": ["memory_update", "documentation_update"],
        "planned_tools": ["read_file", "write_file", "escalate"],
        "planned_gates": ["G0", "G1", "G2"],
        "approval_required": True,
        "estimated_steps": 5,
        "risks": ["ADR required", "human approval required for protected files"],
    },
    "add_test_coverage": {
        "planned_agents": ["orchestrator", "qa", "docs"],
        "planned_skills": ["test_generation", "code_review"],
        "planned_tools": ["read_file", "write_file", "run_command"],
        "planned_gates": ["G0", "G1", "G4", "G6"],
        "planned_contracts": ["contracts/QA_REPORT_CONTRACT.md"],
        "approval_required": False,
        "estimated_steps": 5,
        "risks": ["test must not modify production logic", "test must fail on invalid input before passing"],
    },
}

CLASSIFICATION_RULES: list[tuple[str, list[str]]] = [
    ("destructive_action", ["rm -rf", "drop table", "delete all", "wipe", "destroy", "force push", "reset --hard", "destructive"]),
    ("add_test_coverage", ["add test", "test coverage", "improve test", "missing test", "add coverage", "write test", "ajoute test", "couverture"]),
    ("bugfix", ["bug", "fix", "correction", "corrig", "erreur", "error", "issue", "broken", "crash", "regression"]),
    ("release", ["release", "version", "deploy", "publier", "livrer", "tag v", "bump version"]),
    ("security", ["secur", "cve", "vulnerab", "vuln", "secret", "scan", "gitleaks", "semgrep", "audit sécurité"]),
    ("governance", ["adr", "décision", "governance", "scope.md", "agents.md", "décision structurante", "constitution"]),
    ("audit", ["audit", "revue complète", "analyse", "rapport", "check"]),
    ("documentation", ["doc", "documentation", "readme", "changelog", "session_log"]),
    ("review", ["review", "revue", "relecture", "PR", "pull request"]),
    ("feature", ["feature", "ajout", "add", "implémente", "implement", "nouveau", "new"]),
]


def classify_task(description: str) -> str:
    """Classify task based on keyword matching. Returns task_type."""
    lower = description.lower()
    for task_type, keywords in CLASSIFICATION_RULES:
        if any(kw in lower for kw in keywords):
            return task_type
    return "feature"  # default


def generate_task_id() -> str:
    return f"T-{uuid.uuid4().hex[:8]}"


def extract_from_md(path: Path) -> tuple[str, str | None]:
    """Extract description and optional task_type from a markdown task file.

    Looks for:
      ## Objective  → first non-empty line after heading = description
      ## Task Type  → next non-empty line = task_type

    Handles backslash-escaped markdown (e.g. \\## heading, documentation\\_update).
    Preserves unknown task_type values so main() can emit a proper error.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    description = ""
    task_type_from_md = None
    i = 0
    while i < len(lines):
        # Strip leading backslashes (some markdown generators escape # as \#)
        line = lines[i].strip().lstrip("\\")
        if line.lower().startswith("## objective"):
            # grab first non-empty line after heading
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines):
                description = lines[i].strip().lstrip("\\").strip()
        elif line.lower().startswith("## task type") or line.lower().startswith("## task_type"):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines):
                raw = lines[i].strip()
                # Remove backslash escapes (e.g. documentation\_update → documentation_update)
                raw = raw.replace("\\", "")
                candidate = raw.lower().lstrip("-").strip()
                # Normalize whitespace to underscores
                candidate = re.sub(r"\s+", "_", candidate)
                if candidate:
                    task_type_from_md = candidate  # preserved even if unknown
        i += 1
    # Fall back to file stem if no objective found
    if not description:
        description = path.stem.replace("_", " ").replace("-", " ")
    return description, task_type_from_md


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Route a task description to a JSON orchestration plan"
    )
    parser.add_argument("description", nargs="?", help="Task description")
    parser.add_argument("--task", type=Path, help="Markdown task file (extracts Objective + Task Type)")
    parser.add_argument("--task-type", choices=list(ROUTING_TABLE.keys()),
                        help="Force task type (overrides ## Task Type in mission file)")
    parser.add_argument("--json-input", type=Path, help="Input task JSON file (task.schema.json)")
    parser.add_argument("--task-id", help="Override task ID")
    args = parser.parse_args()

    # Load from file or args
    if args.json_input:
        if not args.json_input.exists():
            print(f"ERROR: File not found: {args.json_input}", file=sys.stderr)
            return 1
        task = json.loads(args.json_input.read_text(encoding="utf-8"))
        description = task.get("description", "")
        task_type = task.get("task_type") or args.task_type
        task_id = task.get("task_id") or args.task_id or generate_task_id()
    elif args.task:
        if not args.task.exists():
            print(f"ERROR: Task file not found: {args.task}", file=sys.stderr)
            return 1
        description, task_type_from_md = extract_from_md(args.task)
        task_type = args.task_type or task_type_from_md
        task_id = args.task_id or generate_task_id()
    elif args.description:
        description = args.description
        task_type = args.task_type
        task_id = args.task_id or generate_task_id()
    else:
        print("ERROR: Provide a description, --task <file>, or --json-input", file=sys.stderr)
        parser.print_help(sys.stderr)
        return 1

    if len(description.split()) < 2:
        print("ERROR: Description too short (minimum 2 words)", file=sys.stderr)
        return 1

    # Check SCOPE.md exists
    scope_file = ROOT / "SCOPE.md"
    if not scope_file.exists():
        print("ERROR: SCOPE.md not found — cannot validate scope", file=sys.stderr)
        return 1

    # Classify if not forced
    if not task_type:
        task_type = classify_task(description)

    if task_type not in ROUTING_TABLE:
        known = ", ".join(ROUTING_TABLE.keys())
        print(
            f"ERROR: Unknown task_type '{task_type}'. "
            f"Known types: {known}",
            file=sys.stderr,
        )
        return 1

    route = ROUTING_TABLE[task_type]

    plan = {
        "task_id": task_id,
        "task_type": task_type,
        "description": description,
        "classified_at": datetime.now(timezone.utc).isoformat(),
        "planned_agents": route["planned_agents"],
        "planned_skills": route["planned_skills"],
        "planned_tools": route["planned_tools"],
        "planned_gates": route["planned_gates"],
        "approval_required": route["approval_required"],
        "estimated_steps": route["estimated_steps"],
        "risks": route["risks"],
    }

    # Add blocking info for destructive actions
    if "status" in route:
        plan["status"] = route["status"]
    if "blocking_policies" in route:
        plan["blocking_policies"] = route["blocking_policies"]

    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
