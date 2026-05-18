"""Memory layer for the ASEF runtime.

Encapsulates reading and writing the canonical markdown files defined in
AGENTS.md section 8 (Règles de mémoire). All writes append; the runtime
never overwrites historical content.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TaskRecord:
    """A single completed task, ready to be journaled."""

    task_id: str
    description: str
    files_touched: list[str]
    gates_passed: list[str]
    started_at: dt.datetime
    ended_at: dt.datetime
    outcome: str  # "success" | "blocked" | "escalated" | "rejected"
    notes: str = ""


class MemoryStore:
    """File-backed memory for the project.

    All paths are resolved against the project root. Methods are safe to
    call even if a file does not exist yet — a sensible default header is
    written on first append.
    """

    def __init__(self, project_root: Path) -> None:
        self.root = project_root

    # ------------------------------------------------------------------ read
    def read_bootstrap_bundle(self) -> str:
        """Concatenate the docs every agent must read at bootstrap.

        Returns a single string, with clear section markers, suitable to be
        inserted into a system prompt.
        """
        parts: list[str] = []
        for name in [
            "AGENTS.md",
            "MEMORY.md",
            "SCOPE.md",
            "DECISIONS.md",
            "PROJECT.md",
        ]:
            content = self._read_optional(self.root / name)
            if content:
                parts.append(f"===== BEGIN {name} =====\n{content}\n===== END {name} =====")
        return "\n\n".join(parts)

    def read(self, relative_path: str) -> str:
        """Read a file relative to project root. Returns '' if missing."""
        return self._read_optional(self.root / relative_path)

    # ----------------------------------------------------------------- write
    def append_session_log(self, record: TaskRecord) -> None:
        """Append a session entry to SESSION_LOG.md."""
        path = self.root / "SESSION_LOG.md"
        self._ensure_header(
            path,
            "# Session Log\n\nChronological journal of all ASEF runtime sessions.\n",
        )
        entry = (
            f"\n## {record.started_at:%Y-%m-%d %H:%M} — {record.task_id}\n\n"
            f"- **Objectif** : {record.description}\n"
            f"- **Durée** : {(record.ended_at - record.started_at).total_seconds():.0f}s\n"
            f"- **Outcome** : {record.outcome}\n"
            f"- **Gates passés** : {', '.join(record.gates_passed) or '—'}\n"
            f"- **Fichiers modifiés** : {', '.join(record.files_touched) or '—'}\n"
        )
        if record.notes:
            entry += f"- **Notes** : {record.notes}\n"
        with path.open("a", encoding="utf-8") as f:
            f.write(entry)

    def append_changelog(self, line: str) -> None:
        """Append an entry to the Unreleased section of CHANGELOG.md."""
        path = self.root / "CHANGELOG.md"
        self._ensure_header(
            path,
            "# Changelog\n\nAll notable changes follow [Keep a Changelog](https://keepachangelog.com).\n\n## [Unreleased]\n",
        )
        content = path.read_text(encoding="utf-8")
        marker = "## [Unreleased]"
        if marker not in content:
            content += f"\n{marker}\n"
        # Insert just after the marker.
        idx = content.index(marker) + len(marker)
        content = content[:idx] + f"\n- {line}" + content[idx:]
        path.write_text(content, encoding="utf-8")

    def append_lesson(self, error: str, cause: str, rule: str) -> None:
        """Append a lesson to LESSONS_LEARNED.md."""
        path = self.root / "LESSONS_LEARNED.md"
        self._ensure_header(
            path,
            "# Lessons Learned\n\nFormat: Erreur → Cause → Règle nouvelle.\n",
        )
        ts = dt.datetime.now().strftime("%Y-%m-%d")
        entry = f"\n## {ts}\n\n- **Erreur** : {error}\n- **Cause** : {cause}\n- **Règle** : {rule}\n"
        with path.open("a", encoding="utf-8") as f:
            f.write(entry)

    def update_memory(self, new_state: str) -> None:
        """Replace the MEMORY.md content with the latest stabilised state.

        MEMORY.md is intentionally a snapshot, not a log — per AGENTS.md §8.
        """
        path = self.root / "MEMORY.md"
        header = (
            "# MEMORY — État courant du projet\n\n"
            f"_Dernière mise à jour : {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
        )
        path.write_text(header + new_state.strip() + "\n", encoding="utf-8")

    def append_decision(self, adr_number: int, title: str, body: str) -> Path:
        """Create an ADR file and register it in DECISIONS.md."""
        adr_dir = self.root / "docs" / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        adr_path = adr_dir / f"ADR-{adr_number:04d}-{_slugify(title)}.md"
        adr_path.write_text(body, encoding="utf-8")

        registry = self.root / "DECISIONS.md"
        self._ensure_header(
            registry,
            "# Decisions Registry\n\nIndex of all Architecture Decision Records.\n\n| ID | Titre | Statut | Date |\n|---|---|---|---|\n",
        )
        ts = dt.datetime.now().strftime("%Y-%m-%d")
        with registry.open("a", encoding="utf-8") as f:
            f.write(f"| ADR-{adr_number:04d} | {title} | Proposé | {ts} |\n")
        return adr_path

    def next_adr_number(self) -> int:
        """Return the next available ADR number."""
        adr_dir = self.root / "docs" / "adr"
        if not adr_dir.exists():
            return 1
        numbers = [
            int(p.stem.split("-")[1])
            for p in adr_dir.glob("ADR-*.md")
            if p.stem.split("-")[1].isdigit()
        ]
        return (max(numbers) + 1) if numbers else 1

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _read_optional(path: Path) -> str:
        if not path.exists():
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return ""

    @staticmethod
    def _ensure_header(path: Path, header: str) -> None:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(header, encoding="utf-8")


def _slugify(text: str) -> str:
    """Conservative slug generator for ADR filenames."""
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "-", "_"):
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:60] or "untitled"
