"""Tests for execution/run_task.py.

Covers:
1.  --dry-run generates plan and writes PLANNED_NOT_EXECUTED to memory
2.  --mode dry-run behaves identically to --dry-run (status PLANNED_NOT_EXECUTED)
3.  --mode assisted writes ASSISTED_PLAN_READY and creates prompt file
4.  --mode audit-only writes AUDIT_ONLY and executed_changes=false
5.  --dry-run and --mode together produce error (mutual exclusion)
6.  documentation_update task type is accepted by --task-type
7.  Live run without working orchestrator returns BLOCKED_RUNTIME_MISSING JSON
8.  --task flag reads Objective and Task Type from markdown file
9.  Prompt file contains Allowed/Forbidden sections
10. Sensitive keywords in allowed_files trigger approval_required=True
11. python -s isolation test: run_task.py works without site-packages side effects
12. Memory entry written by --dry-run has executed_changes=false field
13. Plan JSON includes allowed_files, forbidden_files, artifact_plan, memory_update_plan
"""  # noqa: W605
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

EXEC_DIR = Path(__file__).parent.parent / "execution"
RUN = EXEC_DIR / "run_task.py"
ROOT = Path(__file__).parent.parent
MEMORY_FILE = ROOT / "memory" / "task_history.jsonl"


def _run(*args: str, cwd: Path = ROOT, use_s: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable]
    if use_s:
        cmd.append("-s")
    cmd += [str(RUN), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def _last_memory_entry() -> dict:
    """Read the last line of memory/task_history.jsonl."""
    lines = MEMORY_FILE.read_text(encoding="utf-8").strip().splitlines()
    return json.loads(lines[-1])


# ──────────────────────────────────────────────────────────────────────────────
# 1. --dry-run generates plan and writes PLANNED_NOT_EXECUTED
# ──────────────────────────────────────────────────────────────────────────────
def test_dry_run_writes_planned_not_executed() -> None:
    result = _run("--dry-run", "Fix import error in gates module")
    assert result.returncode == 0, result.stderr
    assert "DRY RUN" in result.stdout
    assert "PLANNED_NOT_EXECUTED" not in result.stdout  # status is in memory, not stdout
    entry = _last_memory_entry()
    assert entry["status"] == "PLANNED_NOT_EXECUTED"
    assert entry.get("executed_changes") is False
    assert entry.get("mode") == "dry-run"


# ──────────────────────────────────────────────────────────────────────────────
# 2. --mode dry-run behaves identically to --dry-run
# ──────────────────────────────────────────────────────────────────────────────
def test_mode_dryrun_same_as_flag() -> None:
    result = _run("--mode", "dry-run", "Fix import error in gates module")
    assert result.returncode == 0, result.stderr
    assert "DRY RUN" in result.stdout
    entry = _last_memory_entry()
    assert entry["status"] == "PLANNED_NOT_EXECUTED"
    assert entry.get("executed_changes") is False


# ──────────────────────────────────────────────────────────────────────────────
# 3. --mode assisted writes ASSISTED_PLAN_READY and creates prompt file
# ──────────────────────────────────────────────────────────────────────────────
def test_mode_assisted_writes_plan_and_prompt() -> None:
    result = _run("--mode", "assisted", "Add test coverage for gates module")
    assert result.returncode == 0, result.stderr
    assert "ASSISTED" in result.stdout
    entry = _last_memory_entry()
    assert entry["status"] == "ASSISTED_PLAN_READY"
    assert entry.get("executed_changes") is False
    prompt_path = entry.get("prompt_path", "")
    assert prompt_path, "prompt_path must be set in memory entry"
    full_prompt = ROOT / prompt_path
    assert full_prompt.exists(), f"Prompt file not found: {full_prompt}"


# ──────────────────────────────────────────────────────────────────────────────
# 4. --mode audit-only writes AUDIT_ONLY and executed_changes=false
# ──────────────────────────────────────────────────────────────────────────────
def test_mode_audit_only() -> None:
    result = _run("--mode", "audit-only", "Audit documentation quality gaps")
    assert result.returncode == 0, result.stderr
    assert "AUDIT ONLY" in result.stdout
    entry = _last_memory_entry()
    assert entry["status"] == "AUDIT_ONLY"
    assert entry.get("executed_changes") is False


# ──────────────────────────────────────────────────────────────────────────────
# 5. --dry-run and --mode together are mutually exclusive
# ──────────────────────────────────────────────────────────────────────────────
def test_dry_run_and_mode_are_mutually_exclusive() -> None:
    result = _run("--dry-run", "--mode", "dry-run", "Fix bug in scheduler")
    assert result.returncode != 0
    assert "mutually exclusive" in result.stderr.lower() or "mutually exclusive" in result.stdout.lower()


# ──────────────────────────────────────────────────────────────────────────────
# 6. documentation_update is accepted as --task-type
# ──────────────────────────────────────────────────────────────────────────────
def test_documentation_update_task_type_accepted() -> None:
    result = _run("--task-type", "documentation_update", "--dry-run",
                  "Update CHANGELOG and MEMORY files")
    assert result.returncode == 0, result.stderr
    import re
    match = re.search(r"(\{[\s\S]+\})", result.stdout)
    assert match, "No JSON plan found in stdout"
    plan = json.loads(match.group(1))
    assert plan["task_type"] == "documentation_update"


# ──────────────────────────────────────────────────────────────────────────────
# 7. Live run without working orchestrator returns BLOCKED_RUNTIME_MISSING JSON
# ──────────────────────────────────────────────────────────────────────────────
def test_live_run_blocked_when_orchestrator_missing(tmp_path: Path, monkeypatch) -> None:
    """Test BLOCKED_RUNTIME_MISSING by temporarily making Orchestrator unimportable."""
    import importlib
    import sys as _sys

    # Create a fake asef package that raises ImportError for orchestrator
    fake_asef = tmp_path / "asef"
    fake_asef.mkdir()
    (fake_asef / "__init__.py").write_text("", encoding="utf-8")
    (fake_asef / "orchestrator.py").write_text(
        "raise ImportError('test: orchestrator not available')",
        encoding="utf-8",
    )
    # Patch sys.path so our fake asef shadows the real one
    env = {
        "PYTHONPATH": str(tmp_path),
        "PATH": __import__("os").environ.get("PATH", ""),
    }
    result = subprocess.run(
        [sys.executable, str(RUN), "Fix bug in scheduler"],
        capture_output=True, text=True, cwd=str(ROOT), env=env,
    )
    assert result.returncode != 0
    # Either BLOCKED_RUNTIME_MISSING in stdout or ERROR in stderr
    combined = result.stdout + result.stderr
    assert "BLOCKED_RUNTIME_MISSING" in combined or "ERROR" in combined


# ──────────────────────────────────────────────────────────────────────────────
# 8. --task flag reads Objective and Task Type from markdown file
# ──────────────────────────────────────────────────────────────────────────────
def test_task_flag_reads_md_file(tmp_path: Path) -> None:
    md = tmp_path / "MISSION.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Update changelog and memory documentation files.

        ## Task Type
        documentation_update

        ## Scope
        Allowed:
        - CHANGELOG.md
        - MEMORY.md
        Forbidden:
        - AGENTS.md
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md), "--dry-run")
    assert result.returncode == 0, result.stderr
    import re
    match = re.search(r"(\{[\s\S]+\})", result.stdout)
    assert match, "No JSON plan found in stdout"
    plan = json.loads(match.group(1))
    assert plan["task_type"] == "documentation_update"
    assert plan["description"] == "Update changelog and memory documentation files."


# ──────────────────────────────────────────────────────────────────────────────
# 9. Prompt file contains Allowed/Forbidden sections
# ──────────────────────────────────────────────────────────────────────────────
def test_prompt_contains_allowed_forbidden_sections(tmp_path: Path) -> None:
    md = tmp_path / "MISSION_PROMPT.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Update changelog and memory documentation files.

        ## Task Type
        documentation_update

        ## Scope
        Allowed:
        - CHANGELOG.md
        - MEMORY.md
        Forbidden:
        - AGENTS.md
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md), "--mode", "assisted")
    assert result.returncode == 0, result.stderr

    entry = _last_memory_entry()
    prompt_path = ROOT / entry.get("prompt_path", "")
    assert prompt_path.exists(), f"Prompt file missing: {prompt_path}"

    prompt_text = prompt_path.read_text(encoding="utf-8")
    assert "Allowed Files" in prompt_text
    assert "Forbidden Files" in prompt_text
    assert "CHANGELOG.md" in prompt_text


# ──────────────────────────────────────────────────────────────────────────────
# 10. Sensitive keywords in allowed_files trigger approval_required=True
# ──────────────────────────────────────────────────────────────────────────────
def test_sensitive_paths_trigger_approval(tmp_path: Path) -> None:
    md = tmp_path / "SENSITIVE.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Update policies and registry configuration.

        ## Task Type
        documentation_update

        ## Scope
        Allowed:
        - policies/DESTRUCTIVE_ACTIONS.md
        - registry/agent_registry.json
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md), "--dry-run")
    assert result.returncode == 0, result.stderr
    import re
    match = re.search(r"(\{[\s\S]+\})", result.stdout)
    assert match, "No JSON plan found in stdout"
    plan = json.loads(match.group(1))
    assert plan.get("approval_required") is True
    assert "approval_reason" in plan


# ──────────────────────────────────────────────────────────────────────────────
# 11. python -s isolation test
# ──────────────────────────────────────────────────────────────────────────────
def test_isolation_with_s_flag() -> None:
    """python -s suppresses site-packages additions via .pth files; script must still work."""
    result = _run("--dry-run", "Fix import error in gates module", use_s=True)
    assert result.returncode == 0, (
        f"run_task.py failed with -s flag:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "DRY RUN" in result.stdout


# ──────────────────────────────────────────────────────────────────────────────
# 12. Memory entry has executed_changes=false on --dry-run
# ──────────────────────────────────────────────────────────────────────────────
def test_dry_run_memory_executed_changes_false() -> None:
    result = _run("--dry-run", "Audit security gates configuration")
    assert result.returncode == 0, result.stderr
    entry = _last_memory_entry()
    assert entry.get("executed_changes") is False, (
        f"expected executed_changes=False, got: {entry.get('executed_changes')!r}"
    )


# ──────────────────────────────────────────────────────────────────────────────
# 13. Plan JSON includes allowed_files, forbidden_files, artifact_plan, memory_update_plan
# ──────────────────────────────────────────────────────────────────────────────
def test_plan_includes_required_fields(tmp_path: Path) -> None:
    md = tmp_path / "FIELDS.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Update changelog and memory documentation files.

        ## Task Type
        documentation_update

        ## Scope
        Allowed:
        - CHANGELOG.md
        - MEMORY.md
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md), "--dry-run")
    assert result.returncode == 0, result.stderr
    import re
    match = re.search(r"(\{[\s\S]+\})", result.stdout)
    assert match, "No JSON plan found in stdout"
    plan = json.loads(match.group(1))
    assert "allowed_files" in plan
    assert "forbidden_files" in plan
    assert "artifact_plan" in plan
    assert "memory_update_plan" in plan
    assert "CHANGELOG.md" in plan["allowed_files"]
    assert "AGENTS.md" in plan["forbidden_files"]
