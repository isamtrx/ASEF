"""Concrete gate executors for the ASEF pipeline.

Each gate maps to a real, executable check. A gate is a callable that
returns a `GateOutcome`. The orchestrator runs them in order and stops
at the first blocking failure (unless an EXCEPTIONS.md entry overrides).

Gate inventory (mirrors docs/quality/QUALITY_GATES.md):
  G0 — Intake recevable
  G1 — Scope validé
  G2 — Architecture validée (skip if no structural decision)
  G3 — Code conforme aux standards (linters)
  G4 — Tests passés (zero red)
  G5 — Sécurité (secrets, SAST, deps)
  G6 — Documentation & evidence package
  G7 — Validation finale (human approval required)
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class GateOutcome:
    """Result of one gate."""

    gate_id: str
    passed: bool
    blocking: bool = True
    summary: str = ""
    details: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: datetime | None = None
    requires_human: bool = False


class GateRunner:
    """Runs the pipeline gates against the project root."""

    def __init__(self, project_root: Path) -> None:
        self.root = project_root

    # ------------------------------------------------------------ utilities
    def _run(self, cmd: list[str], timeout: int = 180) -> tuple[int, str, str]:
        """Run a command in the project root, capture output."""
        try:
            proc = subprocess.run(
                cmd,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            return proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            return 124, "", f"timeout after {timeout}s"
        except FileNotFoundError:
            return 127, "", f"command not found: {cmd[0]}"

    def _has(self, binary: str) -> bool:
        return shutil.which(binary) is not None

    def _finish(self, gate: GateOutcome) -> GateOutcome:
        gate.ended_at = datetime.now()
        return gate

    # ------------------------------------------------------------- G0 intake
    def gate_0_intake(self, task: str) -> GateOutcome:
        """A task must have a non-trivial description (≥ 5 words)."""
        gate = GateOutcome(gate_id="G0", passed=False, summary="")
        words = re.findall(r"\w+", task)
        if len(words) < 5:
            gate.summary = "Task description too short (need ≥ 5 words)."
            return self._finish(gate)
        if not (self.root / "SCOPE.md").exists():
            gate.summary = "SCOPE.md missing — bootstrap incomplete."
            return self._finish(gate)
        gate.passed = True
        gate.summary = f"Intake accepted ({len(words)} words)."
        return self._finish(gate)

    # -------------------------------------------------------------- G1 scope
    def gate_1_scope(self, scope_decision: dict) -> GateOutcome:
        """The scope decision is made by the orchestrator using an LLM call.

        This gate just records the decision returned by the orchestrator.
        """
        gate = GateOutcome(
            gate_id="G1",
            passed=scope_decision.get("in_scope", False),
            summary=scope_decision.get("reason", ""),
        )
        if not gate.passed:
            gate.summary = f"Out of scope: {gate.summary}"
        return self._finish(gate)

    # -------------------------------------------------------- G2 architecture
    def gate_2_architecture(self, requires_adr: bool, adr_path: Path | None) -> GateOutcome:
        """If the task is structural, an ADR must exist."""
        gate = GateOutcome(gate_id="G2", passed=True, summary="No structural decision required.")
        if requires_adr:
            if adr_path and adr_path.exists():
                gate.summary = f"ADR present at {adr_path.relative_to(self.root)}"
            else:
                gate.passed = False
                gate.summary = "Structural decision detected but no ADR was created."
        return self._finish(gate)

    # ------------------------------------------------------- G3 lint / format
    def gate_3_standards(self) -> GateOutcome:
        """Run all configured linters / formatters."""
        gate = GateOutcome(gate_id="G3", passed=True, summary="")
        runs: list[str] = []

        # Python — ruff is fast and ubiquitous.
        if list(self.root.rglob("*.py")) and self._has("ruff"):
            code, out, err = self._run(["ruff", "check", "."])
            runs.append(f"ruff: exit={code}")
            if code != 0:
                gate.passed = False
                gate.details += f"\n--- ruff ---\n{out}{err}"

        # JS/TS — eslint via npx if a package.json declares it.
        pkg = self.root / "package.json"
        if pkg.exists() and self._has("npx"):
            try:
                config = json.loads(pkg.read_text())
            except json.JSONDecodeError:
                config = {}
            deps = {**config.get("dependencies", {}), **config.get("devDependencies", {})}
            if "eslint" in deps:
                code, out, err = self._run(["npx", "--no-install", "eslint", "."])
                runs.append(f"eslint: exit={code}")
                if code != 0:
                    gate.passed = False
                    gate.details += f"\n--- eslint ---\n{out}{err}"

        if not runs:
            gate.summary = "No linter configured for the languages present."
        else:
            gate.summary = "; ".join(runs)
        return self._finish(gate)

    # ------------------------------------------------------------- G4 tests
    def gate_4_tests(self) -> GateOutcome:
        """Run the test suite. Zero red is mandatory."""
        gate = GateOutcome(gate_id="G4", passed=True, summary="")
        runs: list[str] = []

        if list(self.root.rglob("test_*.py")) or list(self.root.rglob("*_test.py")):
            if self._has("pytest"):
                code, out, err = self._run(["pytest", "-q"])
                runs.append(f"pytest: exit={code}")
                if code != 0:
                    gate.passed = False
                    gate.details += f"\n--- pytest ---\n{out}{err}"
            else:
                gate.passed = False
                gate.details += "pytest not installed but test files exist."

        pkg = self.root / "package.json"
        if pkg.exists():
            try:
                config = json.loads(pkg.read_text())
            except json.JSONDecodeError:
                config = {}
            if "test" in config.get("scripts", {}) and self._has("npm"):
                code, out, err = self._run(["npm", "test", "--silent"])
                runs.append(f"npm test: exit={code}")
                if code != 0:
                    gate.passed = False
                    gate.details += f"\n--- npm test ---\n{out}{err}"

        if not runs:
            gate.summary = "No test suite detected."
            # Not having tests is a warning, not a hard fail at G4.
            gate.blocking = False
        else:
            gate.summary = "; ".join(runs)
        return self._finish(gate)

    # ---------------------------------------------------------- G5 security
    def gate_5_security(self) -> GateOutcome:
        """Run secret scan + dependency audit + SAST (best-effort)."""
        gate = GateOutcome(gate_id="G5", passed=True, summary="")
        runs: list[str] = []

        if self._has("gitleaks"):
            code, out, _ = self._run(["gitleaks", "detect", "--no-banner", "--redact", "-v"])
            runs.append(f"gitleaks: exit={code}")
            if code != 0:
                gate.passed = False
                gate.details += f"\n--- gitleaks ---\n{out}"
        else:
            # Fallback: in-process regex scan.
            from asef.tools import _detect_secret  # type: ignore

            offending: list[str] = []
            for path in self.root.rglob("*"):
                if not path.is_file() or path.stat().st_size > 1_000_000:
                    continue
                if any(part.startswith(".") for part in path.relative_to(self.root).parts):
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                hit = _detect_secret(text)
                if hit:
                    offending.append(f"{path.relative_to(self.root)} — {hit}")
            if offending:
                gate.passed = False
                gate.details += "\n--- secret scan ---\n" + "\n".join(offending)
            runs.append(f"secret-scan (fallback): {len(offending)} hits")

        if self._has("semgrep"):
            code, out, _ = self._run(["semgrep", "--config", "auto", "--error", "--quiet", "."], timeout=300)
            runs.append(f"semgrep: exit={code}")
            if code not in (0, 1):  # 1 = findings, still report; treat >1 as failure
                gate.passed = False
                gate.details += f"\n--- semgrep ---\n{out}"
            elif code == 1:
                gate.passed = False
                gate.details += f"\n--- semgrep findings ---\n{out}"

        if (self.root / "requirements.txt").exists() and self._has("pip-audit"):
            code, out, _ = self._run(["pip-audit", "-r", "requirements.txt"])
            runs.append(f"pip-audit: exit={code}")
            if code != 0:
                gate.passed = False
                gate.details += f"\n--- pip-audit ---\n{out}"

        gate.summary = "; ".join(runs) or "No security tooling detected."
        return self._finish(gate)

    # ---------------------------------------------------- G6 docs & evidence
    def gate_6_docs(self, files_touched: list[str]) -> GateOutcome:
        """CHANGELOG.md must have an Unreleased entry; SESSION_LOG.md present."""
        gate = GateOutcome(gate_id="G6", passed=True, summary="")
        missing: list[str] = []

        changelog = self.root / "CHANGELOG.md"
        if not changelog.exists():
            missing.append("CHANGELOG.md")
        else:
            content = changelog.read_text(encoding="utf-8")
            if "## [Unreleased]" not in content:
                missing.append("CHANGELOG.md missing [Unreleased] section")
            else:
                # Heuristic: Unreleased section must have at least one bullet
                # if files were modified.
                if files_touched:
                    unreleased = content.split("## [Unreleased]", 1)[1].split("##", 1)[0]
                    if not re.search(r"^\s*[-*]\s+\S", unreleased, re.MULTILINE):
                        missing.append("CHANGELOG.md [Unreleased] has no entry")

        session = self.root / "SESSION_LOG.md"
        if not session.exists() or session.stat().st_size < 10:
            missing.append("SESSION_LOG.md is empty or missing")

        if missing:
            gate.passed = False
            gate.summary = "; ".join(missing)
        else:
            gate.summary = "Docs and session journal up to date."
        return self._finish(gate)

    # ---------------------------------------------- G7 final human approval
    def gate_7_validation(self, require_human: bool) -> GateOutcome:
        """The orchestrator surfaces this gate — the human resolves it."""
        gate = GateOutcome(
            gate_id="G7",
            passed=not require_human,
            requires_human=require_human,
            summary=("Awaiting human approval." if require_human else "Auto-approved (non-critical)."),
        )
        return self._finish(gate)
