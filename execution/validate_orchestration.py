#!/usr/bin/env python3
"""Validate orchestration files: verify all cross-references exist."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).parent.parent
ORCHESTRATION_DIR = ROOT / "orchestration"
REGISTRY_DIR = ROOT / "registry"

errors = []

def load_registry(name):
    path = REGISTRY_DIR / f"{name}.registry.json"
    if not path.exists():
        errors.append(f"MISSING_REGISTRY: {path}")
        return set()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {item["id"] for item in data.get("items", [])}

agent_ids = load_registry("agents")
skill_ids = load_registry("skills")
gate_ids = load_registry("gates")

# Check all orchestration files exist
required_files = [
    "ROUTING.md",
    "STATE_MACHINE.md",
    "WORKFLOWS.md",
    "ESCALATION.md",
    "TASK_LIFECYCLE.md",
]
for fname in required_files:
    fpath = ORCHESTRATION_DIR / fname
    if not fpath.exists():
        errors.append(f"MISSING_FILE: orchestration/{fname}")

# Check ROUTING.md references valid agents/skills/gates
routing_path = ORCHESTRATION_DIR / "ROUTING.md"
if routing_path.exists():
    content = routing_path.read_text(encoding="utf-8")
    # Extract agent references like `architect`, `developer`, etc.
    found_agents = set(re.findall(r"`(orchestrator|architect|developer|qa|security|docs)`", content))
    for agent in found_agents:
        if agent not in agent_ids:
            errors.append(f"ROUTING_UNKNOWN_AGENT: {agent}")

    # Extract gate references like G0, G1, ... G7
    found_gates = set(re.findall(r"\b(G[0-7])\b", content))
    for gate in found_gates:
        if gate not in gate_ids:
            errors.append(f"ROUTING_UNKNOWN_GATE: {gate}")

# Check WORKFLOWS.md references valid agents/gates
workflows_path = ORCHESTRATION_DIR / "WORKFLOWS.md"
if workflows_path.exists():
    content = workflows_path.read_text(encoding="utf-8")
    found_gates = set(re.findall(r"\b(G[0-7])\b", content))
    for gate in found_gates:
        if gate not in gate_ids:
            errors.append(f"WORKFLOWS_UNKNOWN_GATE: {gate}")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print(f"OK — orchestration validated ({len(required_files)} files, cross-refs OK)")
