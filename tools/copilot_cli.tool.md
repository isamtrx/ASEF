**id**: copilot_cli
**version**: 1.0.0
**implementation**: external — GitHub Copilot CLI (`gh copilot suggest` / `gh copilot explain`)
**category**: ai_assistant
**status**: declared

## Purpose

Copilot CLI is a controlled tool available to the ASEF framework for generating targeted code patches or suggestions. It is NOT the orchestrator. It does NOT have autonomous file access. It receives a structured, scoped prompt and returns a suggestion that must be inspected, tested, and approved before application.

## Permission Level

RESTRICTED — can only be invoked via an explicit playbook step after routing and dry-run are complete.

## Input

- Structured prompt with: objective, task_type, directives_to_respect, allowed_files, forbidden_files, required_tests, rejection_criteria
- Task context: task_id, task_type, planned_gates
- Never receives: full repo contents, secrets, credentials, unrestricted instructions

## Output

- Code patch suggestion (diff format or file content)
- Must be reviewed before application
- Must be tested before memory + artifact write

## Allowed Use

- Generate a minimal patch scoped to allowed_files
- Explain existing code in a read-only capacity
- Suggest test cases from a specification
- Review a diff for obvious issues

## Forbidden Use

- Acting as orchestrator or decision-maker
- Receiving a prompt of the form "do everything" or "fix all issues"
- Accessing files not in allowed_files list
- Modifying protected files (AGENTS.md, SCOPE.md, PROJECT.md, docs/security/SECURITY.md)
- Executing destructive actions
- Committing code without human review
- Bypassing quality gates

## Allowed Agents

- qa
- developer
- security (read-only review only)

## Logging Requirements

- Prompt must be saved to artifacts/prompts/<task_id>-copilot-prompt.md before invocation
- Diff/patch must be saved to artifacts/patches/<task_id>-copilot-patch.diff after invocation
- Memory entry must record: invoked=true, prompt_path, patch_path, review_status

## Risks

- Copilot may generate code that passes superficially but breaks unrelated functionality
- Copilot may modify more files than declared in allowed_files if prompted loosely
- Copilot suggestions are probabilistic — require deterministic validation (tests + gates)
- Must never be used without allowed_files / forbidden_files declared

## Related Policies

- policies/TOOL_ACCESS.md
- policies/HUMAN_APPROVAL.md

## Related Playbook

- playbooks/use_copilot_cli_for_patch.playbook.md
