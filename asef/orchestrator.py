"""Orchestrator — the pipeline that runs G0 → G7.

This is the heart of the ASEF runtime. It implements the workflow defined
in AGENTS.md §5, dispatching to the appropriate agent role at each step
and validating the corresponding quality gate.

Design notes:
- The orchestrator itself is deterministic Python — it does NOT use an
  LLM to decide gate ordering. LLM calls happen inside the agents.
- Scope validation (G1) and structural-decision detection use a single
  LLM call each, with a strict JSON output contract.
- Every transition is logged. On any blocking failure, the run halts and
  writes a postmortem entry to LESSONS_LEARNED.md.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from asef.agents import Agent, AgentResult
from asef.config import Config
from asef.gates import GateOutcome, GateRunner
from asef.memory import MemoryStore, TaskRecord
from asef.provider import LLMProvider, make_provider


@dataclass
class PipelineResult:
    """Final outcome of a full pipeline run."""

    task_id: str
    description: str
    outcome: str  # success | blocked | escalated | rejected
    gates: list[GateOutcome] = field(default_factory=list)
    agent_runs: list[AgentResult] = field(default_factory=list)
    files_touched: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: datetime | None = None
    escalation_reason: str | None = None

    def gates_passed(self) -> list[str]:
        return [g.gate_id for g in self.gates if g.passed]


SCOPE_DECISION_PROMPT = """You are the ASEF orchestrator's scope validator.

Decide whether the requested task is IN scope according to SCOPE.md and
the project description. Reply ONLY with a single JSON object, no prose,
no markdown fences:

{
  "in_scope": true | false,
  "reason": "<one sentence>",
  "is_structural": true | false,
  "structural_reason": "<one sentence or empty string>"
}

Definitions:
- IN scope = the task fits the IN list in SCOPE.md and does not match the OUT list.
- Structural = the task modifies architecture, security, scope, or adds a major dependency.
"""


class Orchestrator:
    """Runs the full ASEF pipeline for a single task."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.memory = MemoryStore(config.project_root)
        self.gates = GateRunner(config.project_root)
        self.provider: LLMProvider = make_provider(config)

    # ============================================================== entry point
    def run_task(self, description: str) -> PipelineResult:
        result = PipelineResult(
            task_id=f"T-{uuid.uuid4().hex[:8]}",
            description=description,
            outcome="in_progress",
        )

        # ---------------------------------------------------------- G0 intake
        g0 = self.gates.gate_0_intake(description)
        result.gates.append(g0)
        if not g0.passed:
            return self._finalise(result, "rejected", g0.summary)

        # ----------------------------------------------------------- G1 scope
        scope_call = self._llm_scope_decision(description)
        g1 = self.gates.gate_1_scope(scope_call)
        result.gates.append(g1)
        if not g1.passed:
            return self._finalise(result, "rejected", g1.summary)

        # --------------------------------------------------- G2 architecture
        adr_path: Path | None = None
        requires_adr = scope_call.get("is_structural", False)
        if requires_adr:
            arch_run = self._run_agent(
                "architect",
                f"Task: {description}\n\nThis task has been flagged as structural "
                f"({scope_call.get('structural_reason', '')}). Produce an ADR per "
                f"AGENTS.md §9 and write it via the write_file tool to "
                f"docs/adr/ADR-<NNNN>-<slug>.md. Then call report_done.",
            )
            result.agent_runs.append(arch_run)
            if arch_run.escalation:
                return self._finalise(result, "escalated", arch_run.escalation.get("reason", ""))
            # Find the most recently created ADR.
            adr_dir = self.config.project_root / "docs" / "adr"
            if adr_dir.exists():
                adrs = sorted(adr_dir.glob("ADR-*.md"), key=lambda p: p.stat().st_mtime)
                if adrs:
                    adr_path = adrs[-1]

        g2 = self.gates.gate_2_architecture(requires_adr, adr_path)
        result.gates.append(g2)
        if not g2.passed:
            return self._finalise(result, "blocked", g2.summary)

        # ---------------------------------------------------- developer agent
        dev_run = self._run_agent("developer", description)
        result.agent_runs.append(dev_run)
        if dev_run.escalation:
            return self._finalise(result, "escalated", dev_run.escalation.get("reason", ""))
        result.files_touched.extend(dev_run.files_touched)

        # ---------------------------------------------------- G3 standards
        g3 = self.gates.gate_3_standards()
        result.gates.append(g3)
        if not g3.passed and g3.blocking:
            return self._finalise(result, "blocked", f"G3 failed: {g3.summary}\n{g3.details[:1000]}")

        # ---------------------------------------------------- G4 tests
        g4 = self.gates.gate_4_tests()
        result.gates.append(g4)
        if not g4.passed and g4.blocking:
            return self._finalise(result, "blocked", f"G4 failed: {g4.summary}\n{g4.details[:1000]}")

        # ---------------------------------------------------- G5 security
        g5 = self.gates.gate_5_security()
        result.gates.append(g5)
        if not g5.passed and g5.blocking:
            return self._finalise(result, "blocked", f"G5 failed: {g5.summary}\n{g5.details[:1000]}")

        # ---------------------------------------------------- docs agent
        docs_run = self._run_agent(
            "docs",
            f"Task just completed: {description}\n\n"
            f"Files touched: {result.files_touched}\n\n"
            f"Update CHANGELOG.md (Unreleased section) with one line "
            f"summarising the change. Call report_done when done.",
        )
        result.agent_runs.append(docs_run)

        # ---------------------------------------------------- G6 docs/evidence
        g6 = self.gates.gate_6_docs(result.files_touched)
        result.gates.append(g6)
        if not g6.passed:
            return self._finalise(result, "blocked", f"G6 failed: {g6.summary}")

        # ---------------------------------------------------- G7 validation
        require_human = self.config.require_human_approval or self._is_critical(
            result, scope_call
        )
        g7 = self.gates.gate_7_validation(require_human)
        result.gates.append(g7)

        outcome = "success" if (g7.passed or g7.requires_human) else "blocked"
        return self._finalise(result, outcome, "Pipeline complete.")

    # =========================================================== helpers
    def _run_agent(self, role: str, task: str) -> AgentResult:
        agent = Agent(role=role, config=self.config, memory=self.memory)
        return agent.run(task)

    def _llm_scope_decision(self, description: str) -> dict:
        """Ask the orchestrator model to classify the task."""
        bundle = self.memory.read_bootstrap_bundle()
        response = self.provider.complete(
            model=self.config.orchestrator_model,
            system=SCOPE_DECISION_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"# Governance bundle\n{bundle}\n\n# Task\n{description}",
                }
            ],
            tools=[],
            max_tokens=512,
        )
        text = response.text
        # Be robust to accidental fences.
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {"in_scope": False, "reason": "Scope validator returned no JSON.", "is_structural": False}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"in_scope": False, "reason": "Scope validator JSON malformed.", "is_structural": False}

    # Files whose modification always requires human approval, regardless of
    # what the LLM scope-validator returned. Substring-matched against touched paths.
    _ALWAYS_CRITICAL_PATHS = (
        "tools.py",       # security filter — modifying bypasses agent controls
        "gates.py",       # gate implementation — modifying bypasses quality gates
        "config.py",      # config loader — touches API key handling
        "pyproject.toml", # supply chain — dependency changes
        ".gitignore",     # protection integrity — removal exposes .env
        "registry/",      # agent routing and policy
    )

    def _is_critical(self, result: PipelineResult, scope: dict) -> bool:
        """A task is critical if it is structural or touches sensitive paths."""
        if scope.get("is_structural"):
            return True
        # Deterministic path-based check — not LLM-dependent (prevents bypass via
        # prompt injection that forces is_structural=false in the scope call).
        for touched in result.files_touched:
            if any(marker in touched for marker in self._ALWAYS_CRITICAL_PATHS):
                return True
        sensitive_markers = ("auth", "security", "payment", "secret", "credential", "permission")
        return any(any(m in f.lower() for m in sensitive_markers) for f in result.files_touched)

    def _finalise(self, result: PipelineResult, outcome: str, note: str) -> PipelineResult:
        result.outcome = outcome
        result.ended_at = datetime.now()
        result.escalation_reason = note if outcome in ("escalated", "blocked", "rejected") else None

        # Always journal.
        self.memory.append_session_log(
            TaskRecord(
                task_id=result.task_id,
                description=result.description,
                files_touched=result.files_touched,
                gates_passed=result.gates_passed(),
                started_at=result.started_at,
                ended_at=result.ended_at,
                outcome=outcome,
                notes=note,
            )
        )

        # On failure, append a lesson so the system learns.
        if outcome in ("blocked", "escalated"):
            self.memory.append_lesson(
                error=f"Task {result.task_id} ended with outcome={outcome}",
                cause=note,
                rule="Review and adjust SCOPE.md, gates configuration, or task framing.",
            )

        return result
