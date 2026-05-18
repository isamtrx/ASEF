"""Command-line interface for the ASEF runtime.

Usage:
    asef run "<task description>"
    asef status
    asef bootstrap         # write missing governance file stubs
    asef gates             # run gates G3-G6 only (no agent)
    asef show-config

The CLI uses only the stdlib (argparse) to keep startup fast.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from asef.config import Config
from asef.gates import GateRunner
from asef.memory import MemoryStore
from asef.orchestrator import Orchestrator, PipelineResult

# ANSI colours, kept minimal so the runtime works in CI logs too.
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _print_gate(gate) -> None:
    icon = f"{GREEN}✓{RESET}" if gate.passed else f"{RED}✗{RESET}"
    label = f"{BOLD}{gate.gate_id}{RESET}"
    print(f"  {icon} {label}: {gate.summary}")
    if gate.details:
        print(f"    {gate.details.strip()[:500]}")


def _print_summary(result: PipelineResult) -> int:
    print()
    print(f"{BOLD}=== Pipeline summary ==={RESET}")
    print(f"Task ID: {result.task_id}")
    print(f"Description: {result.description}")
    print(f"Outcome: {_colour_outcome(result.outcome)}")
    duration = (result.ended_at - result.started_at).total_seconds() if result.ended_at else 0
    print(f"Duration: {duration:.1f}s")
    print(f"Files touched: {', '.join(result.files_touched) or '(none)'}")
    print()
    print(f"{BOLD}Gates:{RESET}")
    for g in result.gates:
        _print_gate(g)
    print()
    print(f"{BOLD}Agent runs:{RESET}")
    for a in result.agent_runs:
        flag = f"{RED}escalated{RESET}" if a.escalation else f"{GREEN}ok{RESET}"
        print(
            f"  - {a.role}: {flag} | iters={a.iterations} "
            f"| tokens in={a.tokens_in} out={a.tokens_out}"
        )
        if a.escalation:
            print(f"    reason: {a.escalation.get('reason', '')}")
    if result.escalation_reason:
        print()
        print(f"{YELLOW}Note:{RESET} {result.escalation_reason}")
    return 0 if result.outcome == "success" else 1


def _colour_outcome(outcome: str) -> str:
    if outcome == "success":
        return f"{GREEN}{outcome}{RESET}"
    if outcome in ("blocked", "rejected"):
        return f"{RED}{outcome}{RESET}"
    return f"{YELLOW}{outcome}{RESET}"


# ---------------------------------------------------------------- commands
def cmd_run(args: argparse.Namespace) -> int:
    config = Config.from_env(args.root)
    orch = Orchestrator(config)
    result = orch.run_task(args.task)
    return _print_summary(result)


def cmd_status(args: argparse.Namespace) -> int:
    config = Config.from_env(args.root)
    memory = MemoryStore(config.project_root)
    print(f"{BOLD}ASEF project: {config.project_root}{RESET}")
    files = config.governance_files()
    for label, path in files.items():
        present = "✓" if path.exists() else "✗"
        colour = GREEN if path.exists() else RED
        size = path.stat().st_size if path.exists() else 0
        print(f"  {colour}{present}{RESET} {label} ({size} bytes)")
    print()
    print(f"{BOLD}Recent session entries:{RESET}")
    log = memory.read("SESSION_LOG.md")
    if log:
        # Print the last 600 chars.
        tail = log[-600:]
        print(tail)
    else:
        print("  (empty)")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    """Write missing governance file stubs. Idempotent."""
    root = (args.root or Path.cwd()).resolve()
    template_dir = Path(__file__).resolve().parent.parent / "_templates"
    if not template_dir.exists():
        # Templates are written by the project author; if missing we just
        # create minimal placeholders. Real templates ship in the repo root.
        print(f"{YELLOW}No _templates directory — using minimal placeholders.{RESET}")

    created = 0
    minimal = {
        "AGENTS.md": "# AGENTS — see https://github.com/isamtrx/ASEF for the canonical version.\n",
        "PROJECT.md": "# Project\n\nMission, vision, principles.\n",
        "SCOPE.md": "# Scope\n\n## IN\n- TODO\n\n## OUT\n- TODO\n",
        "MEMORY.md": "# Memory — current state\n\n_TODO_\n",
        "DECISIONS.md": "# Decisions Registry\n\n| ID | Titre | Statut | Date |\n|---|---|---|---|\n",
        "CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n",
        "SESSION_LOG.md": "# Session Log\n",
        "LESSONS_LEARNED.md": "# Lessons Learned\n",
    }
    for name, content in minimal.items():
        path = root / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created += 1
            print(f"  {GREEN}+{RESET} {name}")
    print(f"\n{created} file(s) created.")
    return 0


def cmd_gates(args: argparse.Namespace) -> int:
    """Run the executable gates (G3-G6) without involving any agent."""
    config = Config.from_env(args.root)
    runner = GateRunner(config.project_root)
    results = [
        runner.gate_3_standards(),
        runner.gate_4_tests(),
        runner.gate_5_security(),
        runner.gate_6_docs(files_touched=[]),
    ]
    all_passed = True
    for g in results:
        _print_gate(g)
        if not g.passed and g.blocking:
            all_passed = False
    return 0 if all_passed else 1


def cmd_show_config(args: argparse.Namespace) -> int:
    config = Config.from_env(args.root)
    print(f"provider               = {config.provider}")
    print(f"project_root           = {config.project_root}")
    print(f"require_human_approval = {config.require_human_approval}")
    print(f"max_iterations_per_gate= {config.max_iterations_per_gate}")
    print(f"sandbox_prefix         = {config.sandbox_command_prefix}")
    if config.provider == "github":
        token_set = bool(config.github_token)
        print(f"github_token           = {'(set)' if token_set else '(not set)'}")
        print(f"github_models_endpoint = {config.github_models_endpoint or '(default)'}")
    print(f"architect_model        = {config.architect_model}")
    print(f"developer_model        = {config.developer_model}")
    print(f"qa_model               = {config.qa_model}")
    print(f"security_model         = {config.security_model}")
    print(f"docs_model             = {config.docs_model}")
    print(f"orchestrator_model     = {config.orchestrator_model}")
    return 0


# ---------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asef",
        description="ASEF runtime — agentic software engineering pipeline.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Project root directory (default: current working directory).",
    )
    subs = parser.add_subparsers(dest="command", required=True)

    p_run = subs.add_parser("run", help="Run a task through the full pipeline.")
    p_run.add_argument("task", help="Task description (≥ 5 words).")
    p_run.set_defaults(func=cmd_run)

    p_status = subs.add_parser("status", help="Print governance status and recent activity.")
    p_status.set_defaults(func=cmd_status)

    p_boot = subs.add_parser("bootstrap", help="Create missing governance file stubs.")
    p_boot.set_defaults(func=cmd_bootstrap)

    p_gates = subs.add_parser("gates", help="Run the executable gates only.")
    p_gates.set_defaults(func=cmd_gates)

    p_show = subs.add_parser("show-config", help="Print the resolved config.")
    p_show.set_defaults(func=cmd_show_config)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except RuntimeError as exc:
        print(f"{RED}Error:{RESET} {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
