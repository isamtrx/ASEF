#!/usr/bin/env python3
"""
validate_agents.py — Validate that all agents/ files are well-formed
and referenced in registry/agents.registry.json.

Exit 0 if all checks pass, non-zero otherwise.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_SECTIONS = [
    "## Mission",
    "## Scope",
    "## Allowed Tasks",
    "## Forbidden Tasks",
    "## Required Directives",
    "## Allowed Tools",
    "## Input Contract",
    "## Output Contract",
    "## Escalation Rules",
    "## Rejection Criteria",
]

REQUIRED_AGENTS = [
    "agents/ORCHESTRATOR.agent.md",
    "agents/ARCHITECT.agent.md",
    "agents/DEVELOPER.agent.md",
    "agents/QA.agent.md",
    "agents/SECURITY.agent.md",
    "agents/DOCS.agent.md",
]

REGISTRY_FILE = ROOT / "registry" / "agents.registry.json"
AGENTS_DIR = ROOT / "agents"


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        print(f"ERROR: registry not found: {REGISTRY_FILE}")
        sys.exit(1)
    with REGISTRY_FILE.open() as f:
        return json.load(f)


def check_agent_file(path: Path, registry_paths: set) -> list[str]:
    errors = []
    content = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"  MISSING SECTION '{section}' in {rel}")

    if rel not in registry_paths:
        errors.append(f"  NOT IN REGISTRY: {rel}")

    return errors


def main() -> int:
    registry = load_registry()
    registry_paths = {item["path"] for item in registry.get("items", [])}

    all_errors = []

    # Check required agents exist
    for req in REQUIRED_AGENTS:
        path = ROOT / req
        if not path.exists():
            all_errors.append(f"MISSING REQUIRED AGENT: {req}")

    # Check all .agent.md files in agents/
    if not AGENTS_DIR.exists():
        print(f"ERROR: agents/ directory not found at {AGENTS_DIR}")
        return 1

    agent_files = list(AGENTS_DIR.glob("*.agent.md"))
    if not agent_files:
        print("ERROR: No agent files found in agents/")
        return 1

    for agent_file in sorted(agent_files):
        errors = check_agent_file(agent_file, registry_paths)
        all_errors.extend(errors)

    # Check registry entries have corresponding files
    for item in registry.get("items", []):
        path = ROOT / item["path"]
        if not path.exists():
            all_errors.append(
                f"REGISTRY ENTRY WITHOUT FILE: {item['path']}"
            )

    if all_errors:
        print("AGENT VALIDATION FAILED:")
        for err in all_errors:
            print(err)
        return 1

    print(
        f"OK — {len(agent_files)} agents validated, "
        f"{len(registry.get('items', []))} in registry"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
