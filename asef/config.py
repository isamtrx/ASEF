"""Configuration loader for the ASEF runtime.

Reads from environment variables and the project root layout. Keep this
module dependency-light — it must work before any agent is invoked.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Default model identifiers — Anthropic backend.
DEFAULT_ARCHITECT_MODEL = "claude-opus-4-7"
DEFAULT_DEVELOPER_MODEL = "claude-sonnet-4-6"
DEFAULT_QA_MODEL = "claude-sonnet-4-6"
DEFAULT_SECURITY_MODEL = "claude-sonnet-4-6"
DEFAULT_DOCS_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_ORCHESTRATOR_MODEL = "claude-sonnet-4-6"

# Default model identifier for GitHub Models backend.
# Overridden per-role via ASEF_MODEL_<ROLE> env var.
GITHUB_DEFAULT_MODEL = "claude-sonnet-4-6"


@dataclass
class Config:
    """Runtime configuration.

    Every path is absolute. Models can be overridden per-role via env
    variables `ASEF_MODEL_<ROLE>` (e.g. ASEF_MODEL_DEVELOPER).
    """

    project_root: Path
    anthropic_api_key: str
    require_human_approval: bool = True
    max_iterations_per_gate: int = 3
    sandbox_command_prefix: list[str] = field(default_factory=list)

    # LLM provider: "anthropic" (default) | "github"
    provider: str = "anthropic"
    github_token: str = ""
    github_models_endpoint: str = ""

    architect_model: str = DEFAULT_ARCHITECT_MODEL
    developer_model: str = DEFAULT_DEVELOPER_MODEL
    qa_model: str = DEFAULT_QA_MODEL
    security_model: str = DEFAULT_SECURITY_MODEL
    docs_model: str = DEFAULT_DOCS_MODEL
    orchestrator_model: str = DEFAULT_ORCHESTRATOR_MODEL

    @classmethod
    def from_env(cls, project_root: Path | None = None) -> Config:
        """Build a Config from environment variables.

        Looks for a .env file at project_root and loads it if present.
        Falls back to current working directory for project_root.
        """
        root = (project_root or Path.cwd()).resolve()
        _load_dotenv(root / ".env")

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        provider = os.environ.get("ASEF_PROVIDER", "anthropic")
        github_token = os.environ.get("GITHUB_TOKEN", "")
        github_endpoint = os.environ.get("ASEF_GITHUB_ENDPOINT", "")

        require_human = os.environ.get("ASEF_REQUIRE_HUMAN_APPROVAL", "1") != "0"
        max_iter = int(os.environ.get("ASEF_MAX_ITERATIONS", "3"))
        sandbox = os.environ.get("ASEF_SANDBOX_PREFIX", "").split()

        # When using the GitHub Models backend, fall back to GITHUB_DEFAULT_MODEL
        # for any role whose specific env var is not explicitly set.
        if provider == "github":
            gh = os.environ.get("ASEF_GITHUB_DEFAULT_MODEL", GITHUB_DEFAULT_MODEL)
            _model = lambda key, _ant: os.environ.get(key, gh)  # noqa: E731
        else:
            _model = lambda key, ant: os.environ.get(key, ant)  # noqa: E731

        # Validate that the required credential is present before any agent is invoked.
        # Fail-secure: raise at startup rather than midway through the pipeline.
        if provider == "anthropic" and not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is required when ASEF_PROVIDER=anthropic. "
                "Copy .env.example to .env and fill in your key."
            )
        if provider == "github" and not github_token:
            raise RuntimeError(
                "GITHUB_TOKEN is required when ASEF_PROVIDER=github. "
                "Set GITHUB_TOKEN in your environment or .env file."
            )

        return cls(
            project_root=root,
            anthropic_api_key=api_key,
            provider=provider,
            github_token=github_token,
            github_models_endpoint=github_endpoint,
            require_human_approval=require_human,
            max_iterations_per_gate=max_iter,
            sandbox_command_prefix=sandbox,
            architect_model=_model("ASEF_MODEL_ARCHITECT", DEFAULT_ARCHITECT_MODEL),
            developer_model=_model("ASEF_MODEL_DEVELOPER", DEFAULT_DEVELOPER_MODEL),
            qa_model=_model("ASEF_MODEL_QA", DEFAULT_QA_MODEL),
            security_model=_model("ASEF_MODEL_SECURITY", DEFAULT_SECURITY_MODEL),
            docs_model=_model("ASEF_MODEL_DOCS", DEFAULT_DOCS_MODEL),
            orchestrator_model=_model("ASEF_MODEL_ORCHESTRATOR", DEFAULT_ORCHESTRATOR_MODEL),
        )

    def governance_files(self) -> dict[str, Path]:
        """Return the canonical map of governance file -> path.

        These are the files an agent must read at bootstrap, per AGENTS.md.
        """
        return {
            "AGENTS.md": self.project_root / "AGENTS.md",
            "PROJECT.md": self.project_root / "PROJECT.md",
            "SCOPE.md": self.project_root / "SCOPE.md",
            "MEMORY.md": self.project_root / "MEMORY.md",
            "DECISIONS.md": self.project_root / "DECISIONS.md",
            "CHANGELOG.md": self.project_root / "CHANGELOG.md",
            "SESSION_LOG.md": self.project_root / "SESSION_LOG.md",
            "LESSONS_LEARNED.md": self.project_root / "LESSONS_LEARNED.md",
            "docs/ARCHITECTURE.md": self.project_root / "docs" / "ARCHITECTURE.md",
            "docs/quality/QUALITY_GATES.md": self.project_root
            / "docs"
            / "quality"
            / "QUALITY_GATES.md",
            "docs/security/SECURITY.md": self.project_root / "docs" / "security" / "SECURITY.md",
        }


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader to avoid an extra dependency."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Don't override values already in the environment.
        os.environ.setdefault(key, value)
