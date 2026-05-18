"""Tests for execution/route_task.py.

Covers:
1. Known task_type from --task-type is respected and routed correctly
2. documentation_update is present in ROUTING_TABLE and has correct agents
3. extract_from_md reads Task Type from markdown file
4. extract_from_md handles backslash-escaped headings (backslash## Task Type)
5. Unknown task_type from CLI --task-type produces a non-zero exit and error message
6. Unknown task_type from markdown file produces a non-zero exit and error message
"""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

EXEC_DIR = Path(__file__).parent.parent / "execution"
ROUTE = EXEC_DIR / "route_task.py"
ROOT = Path(__file__).parent.parent


def _run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROUTE), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


# ──────────────────────────────────────────────────────────────────────────────
# 1. Known task_type from --task-type is respected
# ──────────────────────────────────────────────────────────────────────────────
def test_explicit_task_type_is_routed(tmp_path: Path) -> None:
    result = _run("--task-type", "bugfix", "Fix authentication race condition")
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["task_type"] == "bugfix"
    assert "developer" in plan["planned_agents"]


# ──────────────────────────────────────────────────────────────────────────────
# 2. documentation_update present in ROUTING_TABLE with correct agents
# ──────────────────────────────────────────────────────────────────────────────
def test_documentation_update_in_routing_table() -> None:
    from execution.route_task import ROUTING_TABLE  # noqa: PLC0415

    assert "documentation_update" in ROUTING_TABLE, (
        "documentation_update must be present in ROUTING_TABLE"
    )
    route = ROUTING_TABLE["documentation_update"]
    assert "docs" in route["planned_agents"]
    assert "qa" in route["planned_agents"]
    assert len(route["planned_gates"]) >= 2


# ──────────────────────────────────────────────────────────────────────────────
# 3. extract_from_md reads Task Type from a well-formed markdown file
# ──────────────────────────────────────────────────────────────────────────────
def test_extract_task_type_from_md(tmp_path: Path) -> None:
    md = tmp_path / "TASK.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Update the changelog and README files.

        ## Task Type
        documentation_update
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md))
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["task_type"] == "documentation_update"


# ──────────────────────────────────────────────────────────────────────────────
# 4. extract_from_md handles backslash-escaped headings
# ──────────────────────────────────────────────────────────────────────────────
def test_extract_task_type_backslash_escaped(tmp_path: Path) -> None:
    md = tmp_path / "TASK_ESCAPED.md"
    md.write_text(
        textwrap.dedent(r"""
        \## Objective
        Update the changelog and README files.

        \## Task Type
        documentation\_update
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md))
    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["task_type"] == "documentation_update"


# ──────────────────────────────────────────────────────────────────────────────
# 5. Unknown task_type via --task-type → non-zero exit + error message
# ──────────────────────────────────────────────────────────────────────────────
def test_unknown_task_type_cli_fails() -> None:
    # argparse choices= will reject this before even reaching our custom check
    result = _run("--task-type", "nonexistent_type_xyz", "Some description")
    assert result.returncode != 0


# ──────────────────────────────────────────────────────────────────────────────
# 6. Unknown task_type from markdown → non-zero exit + "Unknown task_type" in stderr
# ──────────────────────────────────────────────────────────────────────────────
def test_unknown_task_type_from_md_fails(tmp_path: Path) -> None:
    md = tmp_path / "UNKNOWN.md"
    md.write_text(
        textwrap.dedent("""\
        ## Objective
        Do something unusual.

        ## Task Type
        totally_unknown_type
        """),
        encoding="utf-8",
    )
    result = _run("--task", str(md))
    assert result.returncode != 0
    assert "Unknown task_type" in result.stderr or "Unknown task_type" in result.stdout
