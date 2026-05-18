# Copilot CLI Prompt -- T-778777c0

**task_id**: T-778777c0
**task_type**: bugfix
**generated_at**: 2026-05-17T14:13:08.489123+00:00

## Task Objective

Fix import error in gates module

## Directives to Respect

Refer to the following directives before generating any code:
- directives/00_MASTER.md (mandatory)
- directives/11_TESTING.md (if adding tests)
- directives/12_QA.md (if QA task)
- directives/13_SECURITY.md (if security-relevant)

## Agents Assigned

orchestrator, developer, qa, security, docs

## Skills Required

code_review, test_generation, security_review, memory_update, documentation_update

## Tools Allowed

read_file, write_file, run_command, escalate

## Gates That Will Run

G0, G1, G3, G4, G5, G6

## Contracts

(none specified)

## Allowed Files (ONLY modify these)

(none declared -- check mission Scope.Allowed)

## Forbidden Files (NEVER modify)

- AGENTS.md
- SCOPE.md
- PROJECT.md
- docs/security/SECURITY.md
- asef/__init__.py

## Required Tests

- Any new function must have at least one test
- Tests must fail on invalid input before passing on valid input
- Do not delete existing tests

## Rejection Criteria

- Copilot touches a forbidden file -> REJECT
- Copilot removes existing tests -> REJECT
- Copilot adds hardcoded secrets or credentials -> REJECT
- Copilot suggests "delete all" or destructive commands -> REJECT
- Patch adds > 150 lines unrelated to the objective -> REJECT
- Copilot claims tests pass without showing real output -> REJECT

## Expected Output Format

- Python code for test file (if test task)
- Minimal diff -- only the files needed
- Explanation of what was changed and why

## Risk Notes

- regression risk if tests incomplete

## Instruction

Generate a MINIMAL, TARGETED patch that addresses the objective above.
Do NOT modify any file outside the Allowed Files list.
Do NOT claim tests pass without showing their output.
Do NOT add features beyond the stated objective.
Do NOT commit automatically.
Do NOT change package dependencies.
