"""Smoke tests for the ASEF runtime.

These tests cover the deterministic parts of the system — gates, tools,
memory store — without invoking the Anthropic API. The agent loop itself
is exercised via a mocked client in test_orchestrator_smoke.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ----------------------------------------------------------------- fixtures
@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """A minimal ASEF project on disk."""
    (tmp_path / "SCOPE.md").write_text("# Scope\n\n## IN\n- demo\n\n## OUT\n- prod deploy\n")
    (tmp_path / "PROJECT.md").write_text("# Project\n\nDemo.\n")
    (tmp_path / "AGENTS.md").write_text("# AGENTS\n\nMinimal stub.\n")
    (tmp_path / "MEMORY.md").write_text("# Memory\n\nNew project.\n")
    (tmp_path / "DECISIONS.md").write_text("# Decisions\n")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n")
    (tmp_path / "SESSION_LOG.md").write_text("# Session Log\n")
    (tmp_path / "LESSONS_LEARNED.md").write_text("# Lessons\n")
    return tmp_path


# ----------------------------------------------------------------------- tools
def test_tools_reject_destructive_command(tmp_project: Path) -> None:
    from asef.tools import ToolExecutor

    ex = ToolExecutor(tmp_project)
    result = ex.dispatch("run_command", {"command": "rm -rf /"})
    assert result.is_error
    assert "destructive" in result.content.lower()


def test_tools_reject_protected_file_write(tmp_project: Path) -> None:
    from asef.tools import ToolExecutor

    ex = ToolExecutor(tmp_project)
    result = ex.dispatch("write_file", {"path": "AGENTS.md", "content": "hacked"})
    assert result.is_error
    assert "protected" in result.content.lower()


def test_tools_reject_path_escape(tmp_project: Path) -> None:
    from asef.tools import ToolExecutor

    ex = ToolExecutor(tmp_project)
    result = ex.dispatch("read_file", {"path": "../../etc/passwd"})
    assert result.is_error


def test_tools_reject_secret_in_write(tmp_project: Path) -> None:
    from asef.tools import ToolExecutor

    ex = ToolExecutor(tmp_project)
    poison = "ANTHROPIC_KEY = 'sk-ant-" + "A" * 40 + "'"
    result = ex.dispatch("write_file", {"path": "config.py", "content": poison})
    assert result.is_error
    assert "secret" in result.content.lower()


def test_tools_allow_normal_write_and_read(tmp_project: Path) -> None:
    from asef.tools import ToolExecutor

    ex = ToolExecutor(tmp_project)
    w = ex.dispatch("write_file", {"path": "hello.txt", "content": "world"})
    assert not w.is_error
    r = ex.dispatch("read_file", {"path": "hello.txt"})
    assert not r.is_error
    assert r.content == "world"


# ----------------------------------------------------------------------- gates
def test_gate_0_rejects_short_task(tmp_project: Path) -> None:
    from asef.gates import GateRunner

    g = GateRunner(tmp_project).gate_0_intake("too short")
    assert not g.passed


def test_gate_0_accepts_long_task(tmp_project: Path) -> None:
    from asef.gates import GateRunner

    g = GateRunner(tmp_project).gate_0_intake("Add a function that returns hello world")
    assert g.passed


def test_gate_5_fallback_detects_secret(tmp_project: Path) -> None:
    from asef.gates import GateRunner

    (tmp_project / "leak.txt").write_text("sk-ant-" + "B" * 40)
    g = GateRunner(tmp_project).gate_5_security()
    # If gitleaks is installed it'll report; if not, the fallback regex will.
    assert not g.passed


def test_gate_6_passes_with_unreleased_entry(tmp_project: Path) -> None:
    from asef.gates import GateRunner

    changelog = tmp_project / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [Unreleased]\n- did something\n")
    g = GateRunner(tmp_project).gate_6_docs(files_touched=["foo.py"])
    assert g.passed


def test_gate_6_fails_when_unreleased_empty_and_files_touched(tmp_project: Path) -> None:
    from asef.gates import GateRunner

    g = GateRunner(tmp_project).gate_6_docs(files_touched=["foo.py"])
    assert not g.passed


# --------------------------------------------------------------------- memory
def test_memory_appends_session_log(tmp_project: Path) -> None:
    import datetime as dt

    from asef.memory import MemoryStore, TaskRecord

    store = MemoryStore(tmp_project)
    record = TaskRecord(
        task_id="T-123",
        description="demo",
        files_touched=["a.py"],
        gates_passed=["G0", "G3"],
        started_at=dt.datetime.now(),
        ended_at=dt.datetime.now(),
        outcome="success",
    )
    store.append_session_log(record)
    content = (tmp_project / "SESSION_LOG.md").read_text(encoding="utf-8")
    assert "T-123" in content
    assert "success" in content


def test_memory_creates_adr(tmp_project: Path) -> None:
    from asef.memory import MemoryStore

    store = MemoryStore(tmp_project)
    n = store.next_adr_number()
    path = store.append_decision(n, "Test decision", "# ADR body\n")
    assert path.exists()
    registry = (tmp_project / "DECISIONS.md").read_text(encoding="utf-8")
    assert f"ADR-{n:04d}" in registry


# -------------------------------------------------------------------- config
def test_config_requires_api_key(tmp_project: Path) -> None:
    """Config.from_env() raises RuntimeError when no credential is set (fail-secure)."""
    from asef.config import Config

    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("GITHUB_TOKEN", None)
        os.environ.pop("ASEF_PROVIDER", None)
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY is required"):
            Config.from_env(tmp_project)


def test_config_loads_from_env(tmp_project: Path) -> None:
    from asef.config import Config

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        cfg = Config.from_env(tmp_project)
        assert cfg.anthropic_api_key == "sk-ant-test"
        assert cfg.require_human_approval is True
        assert cfg.architect_model.startswith("claude-")


# ----------------------------------------------------------- orchestrator smoke
def test_orchestrator_rejects_out_of_scope(tmp_project: Path) -> None:
    """G1 returns in_scope=false → outcome is 'rejected', no agent call."""
    from asef.config import Config
    from asef.orchestrator import Orchestrator
    from asef.provider import LLMResponse

    fake_response = LLMResponse(
        text='{"in_scope": false, "reason": "Deployment is OUT", "is_structural": false}',
        tool_calls=[],
        tokens_in=10,
        tokens_out=20,
    )
    fake_provider = MagicMock()
    fake_provider.complete.return_value = fake_response

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        cfg = Config.from_env(tmp_project)
        orch = Orchestrator(cfg)
        orch.provider = fake_provider  # inject mock

        result = orch.run_task("Deploy the runtime to production immediately")
        assert result.outcome == "rejected"
        # Only the orchestrator scope-decision call should have happened.
        assert fake_provider.complete.call_count == 1
