"""Tests for asef_doctor.py and bootstrap_framework.py.

Covers:
1. --help works for both scripts
2. asef_doctor --json --skip-validators returns valid JSON
3. asef_doctor detects missing manifest in a temp repo
4. asef_doctor does not return PASS when required scripts are missing
5. bootstrap_framework --dry-run does not create files in target
6. bootstrap_framework selects minimal profile when stack is unknown
7. bootstrap_framework detects frontend when package.json + vite.config.js present
8. bootstrap_framework does not overwrite AGENTS.md without --force
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

EXEC_DIR = Path(__file__).parent.parent / "execution"
DOCTOR = EXEC_DIR / "asef_doctor.py"
BOOTSTRAP = EXEC_DIR / "bootstrap_framework.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(script: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=check,
    )


# ---------------------------------------------------------------------------
# asef_doctor tests
# ---------------------------------------------------------------------------

class TestAsefDoctorHelp:
    def test_help_exits_zero(self):
        result = run(DOCTOR, "--help")
        assert result.returncode == 0

    def test_help_mentions_skip_validators(self):
        result = run(DOCTOR, "--help")
        assert "skip-validators" in result.stdout


class TestAsefDoctorJson:
    def test_json_output_is_valid_json(self, tmp_path):
        """--json --skip-validators must produce parseable JSON."""
        # Use the actual repo root as the root under test — it has a manifest now
        repo_root = EXEC_DIR.parent
        result = run(DOCTOR, "--json", "--skip-validators", "--root", str(repo_root))
        # May be PASS or PARTIAL depending on state — but must be valid JSON
        data = json.loads(result.stdout)
        assert "status" in data
        assert "checks" in data

    def test_json_contains_required_keys(self, tmp_path):
        repo_root = EXEC_DIR.parent
        result = run(DOCTOR, "--json", "--skip-validators", "--root", str(repo_root))
        data = json.loads(result.stdout)
        for key in ("status", "checks", "errors", "warnings", "next_actions", "root"):
            assert key in data, f"Missing key: {key}"


class TestAsefDoctorMissingManifest:
    def test_fail_on_empty_repo(self, tmp_path):
        """An empty directory has no manifest — doctor must not return PASS."""
        result = run(DOCTOR, "--skip-validators", "--root", str(tmp_path))
        # Should return FAIL or PARTIAL — never 0 (PASS)
        assert result.returncode != 0

    def test_json_fail_on_empty_repo(self, tmp_path):
        result = run(DOCTOR, "--json", "--skip-validators", "--root", str(tmp_path))
        data = json.loads(result.stdout)
        assert data["status"] in ("FAIL", "PARTIAL")


class TestAsefDoctorMissingScripts:
    def test_fail_when_scripts_missing(self, tmp_path):
        """Doctor must not return PASS when required scripts listed in manifest are absent."""
        # Create a minimal manifest referencing a non-existent script
        manifest = {
            "framework": "ASEF",
            "version": "0.2.0",
            "required_layers": [],
            "optional_layers": [],
            "required_scripts": ["execution/nonexistent_script.py"],
            "minimum_proof": [],
            "profiles": [],
        }
        (tmp_path / "asef.manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        result = run(DOCTOR, "--json", "--skip-validators", "--root", str(tmp_path))
        data = json.loads(result.stdout)
        assert data["status"] in ("FAIL", "PARTIAL")
        assert result.returncode != 0


# ---------------------------------------------------------------------------
# bootstrap_framework tests
# ---------------------------------------------------------------------------

class TestBootstrapHelp:
    def test_help_exits_zero(self):
        result = run(BOOTSTRAP, "--help")
        assert result.returncode == 0

    def test_help_mentions_dry_run(self):
        result = run(BOOTSTRAP, "--help")
        assert "dry-run" in result.stdout


class TestBootstrapDryRun:
    def test_dry_run_creates_no_files(self, tmp_path):
        """--dry-run must not create any file in the target directory."""
        target = tmp_path / "target-repo"
        target.mkdir()
        repo_root = EXEC_DIR.parent
        result = run(
            BOOTSTRAP,
            "--target", str(target),
            "--profile", "minimal",
            "--dry-run",
            "--source", str(repo_root),
        )
        # Only .asef/ state and artifacts/ are allowed to be created in real mode
        # In dry-run, nothing should be created
        created = list(target.rglob("*"))
        assert created == [], f"dry-run created files: {created}"

    def test_dry_run_exit_zero_on_success(self, tmp_path):
        target = tmp_path / "target-repo"
        target.mkdir()
        repo_root = EXEC_DIR.parent
        result = run(
            BOOTSTRAP,
            "--target", str(target),
            "--profile", "minimal",
            "--dry-run",
            "--source", str(repo_root),
        )
        assert result.returncode in (0, 1)  # 0=PASS, 1=PARTIAL (preserved files)


class TestBootstrapProfileAutodetect:
    def test_minimal_selected_when_no_stack(self, tmp_path):
        """An empty repo with no stack indicators defaults to minimal."""
        target = tmp_path / "target-repo"
        target.mkdir()
        repo_root = EXEC_DIR.parent
        result = run(
            BOOTSTRAP,
            "--target", str(target),
            "--json",
            "--dry-run",
            "--source", str(repo_root),
        )
        data = json.loads(result.stdout)
        assert data["profile"] == "minimal"

    def test_frontend_detected_with_vite(self, tmp_path):
        """package.json + vite.config.js should trigger frontend profile."""
        target = tmp_path / "target-repo"
        target.mkdir()
        (target / "package.json").write_text('{"name": "app"}', encoding="utf-8")
        (target / "vite.config.js").write_text("export default {}", encoding="utf-8")
        repo_root = EXEC_DIR.parent
        result = run(
            BOOTSTRAP,
            "--target", str(target),
            "--json",
            "--dry-run",
            "--source", str(repo_root),
        )
        data = json.loads(result.stdout)
        # Auto-detected profile should be frontend (no backend stack)
        assert data["profile"] == "frontend"


class TestBootstrapNoOverwrite:
    def test_agents_md_preserved_without_force(self, tmp_path):
        """Existing AGENTS.md must not be overwritten unless --force is passed."""
        target = tmp_path / "target-repo"
        target.mkdir()
        original_content = "# Original AGENTS.md\nDo not overwrite me.\n"
        agents_md = target / "AGENTS.md"
        agents_md.write_text(original_content, encoding="utf-8")
        repo_root = EXEC_DIR.parent
        run(
            BOOTSTRAP,
            "--target", str(target),
            "--profile", "minimal",
            "--source", str(repo_root),
        )
        assert agents_md.read_text(encoding="utf-8") == original_content
