"""Tests for validate_registry.py — MISSION-002.

Tests cover:
1. Valid registry state — all checks pass
2. Invalid file reference detected — validate_registry_file returns error
3. Malformed JSON detected — validate_registry_file returns error
4. Missing required field detected — item missing 'status' triggers error
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest


def _make_valid_registry(tmp_path: Path) -> tuple[Path, Path]:
    """Create a minimal valid registry and a referenced file."""
    referenced = tmp_path / "agents" / "orchestrator.agent.md"
    referenced.parent.mkdir(parents=True, exist_ok=True)
    referenced.write_text("# Orchestrator agent\n", encoding="utf-8")

    registry_dir = tmp_path / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    registry_file = registry_dir / "agents.registry.json"
    registry_file.write_text(
        json.dumps({
            "version": "1.0",
            "items": [
                {
                    "id": "orchestrator",
                    "name": "Orchestrator",
                    "path": "agents/orchestrator.agent.md",
                    "status": "active",
                }
            ],
        }),
        encoding="utf-8",
    )
    return registry_file, referenced


def _call_validate(tmp_path: Path, registry_file: Path) -> list[str]:
    """Call validate_registry_file with ROOT patched to tmp_path."""
    import importlib, sys

    # Import fresh copy with ROOT overridden
    spec = importlib.util.spec_from_file_location(
        "validate_registry",
        Path(__file__).parent.parent / "execution" / "validate_registry.py",
    )
    mod = importlib.util.module_from_spec(spec)
    # Patch ROOT before exec
    mod.__dict__["__builtins__"] = __builtins__
    spec.loader.exec_module(mod)
    original_root = mod.ROOT
    mod.ROOT = tmp_path  # type: ignore[attr-defined]
    try:
        return mod.validate_registry_file(registry_file)
    finally:
        mod.ROOT = original_root


# ----------------------------------------------------------------- test 1
def test_valid_registry_passes(tmp_path: Path) -> None:
    """A registry with all required fields and an existing file must return no errors."""
    registry_file, _ = _make_valid_registry(tmp_path)

    import importlib

    spec = importlib.util.spec_from_file_location(
        "validate_registry_ok",
        Path(__file__).parent.parent / "execution" / "validate_registry.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = tmp_path  # type: ignore[attr-defined]

    errors = mod.validate_registry_file(registry_file)
    assert errors == [], f"Expected no errors but got: {errors}"


# ----------------------------------------------------------------- test 2
def test_missing_file_detected(tmp_path: Path) -> None:
    """A registry item referencing a non-existent file must produce an error."""
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    registry_file = registry_dir / "agents.registry.json"
    registry_file.write_text(
        json.dumps({
            "version": "1.0",
            "items": [
                {
                    "id": "ghost",
                    "name": "Ghost Agent",
                    "path": "agents/ghost.agent.md",  # does NOT exist
                    "status": "active",
                }
            ],
        }),
        encoding="utf-8",
    )

    import importlib

    spec = importlib.util.spec_from_file_location(
        "validate_registry_missing",
        Path(__file__).parent.parent / "execution" / "validate_registry.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = tmp_path  # type: ignore[attr-defined]

    errors = mod.validate_registry_file(registry_file)
    assert any("FILE NOT FOUND" in e for e in errors), (
        f"Expected FILE NOT FOUND error, got: {errors}"
    )


# ----------------------------------------------------------------- test 3
def test_invalid_json_detected(tmp_path: Path) -> None:
    """A registry file with malformed JSON must produce an INVALID JSON error."""
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    registry_file = registry_dir / "agents.registry.json"
    registry_file.write_text("{ this is not valid json }", encoding="utf-8")

    import importlib

    spec = importlib.util.spec_from_file_location(
        "validate_registry_json",
        Path(__file__).parent.parent / "execution" / "validate_registry.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = tmp_path  # type: ignore[attr-defined]

    errors = mod.validate_registry_file(registry_file)
    assert any("INVALID JSON" in e for e in errors), (
        f"Expected INVALID JSON error, got: {errors}"
    )


# ----------------------------------------------------------------- test 4
def test_missing_required_field_detected(tmp_path: Path) -> None:
    """An item missing the 'status' required field must produce an error."""
    referenced = tmp_path / "agents" / "minimal.agent.md"
    referenced.parent.mkdir(parents=True, exist_ok=True)
    referenced.write_text("# Minimal\n", encoding="utf-8")

    registry_dir = tmp_path / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    registry_file = registry_dir / "agents.registry.json"
    registry_file.write_text(
        json.dumps({
            "version": "1.0",
            "items": [
                {
                    "id": "minimal",
                    "name": "Minimal",
                    "path": "agents/minimal.agent.md",
                    # 'status' deliberately omitted
                }
            ],
        }),
        encoding="utf-8",
    )

    import importlib

    spec = importlib.util.spec_from_file_location(
        "validate_registry_field",
        Path(__file__).parent.parent / "execution" / "validate_registry.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = tmp_path  # type: ignore[attr-defined]

    errors = mod.validate_registry_file(registry_file)
    assert any("missing fields" in e for e in errors), (
        f"Expected missing fields error, got: {errors}"
    )
