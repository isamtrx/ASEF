# Copilot CLI Prompt — T-eb549fdf

**task_id**: T-eb549fdf
**task_type**: add_test_coverage
**generated_at**: 2026-05-17T04:44:41.957035+00:00

## Task Objective

Add or improve a test ensuring registry references point to existing files and invalid references are detected.

## Directives to Respect

Refer to the following directives before generating any code:
- directives/00_MASTER.md (mandatory)
- directives/11_TESTING.md (if adding tests)
- directives/12_QA.md (if QA task)
- directives/13_SECURITY.md (if security-relevant)

## Agents Assigned

orchestrator, qa, docs

## Skills Required

test_generation, code_review

## Tools Allowed

read_file, write_file, run_command

## Gates That Will Run

G0, G1, G4, G6

## Contracts

contracts/QA_REPORT_CONTRACT.md

## Allowed Files (ONLY modify these)

Target files:
- execution/validate_registry.py
- tests/test_validate_registry.py (create if absent)

Do not modify:
- unrelated business code
- unrelated directives
- unrelated runtime files
- asef/*.py (protected runtime)
- AGENTS.md, SCOPE.md, PROJECT.md, docs/security/SECURITY.md

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

- Copilot touches a forbidden file → REJECT
- Copilot removes existing tests → REJECT
- Copilot adds hardcoded secrets or credentials → REJECT
- Copilot suggests "delete all" or destructive commands → REJECT
- Patch adds > 150 lines unrelated to the objective → REJECT

## Expected Output Format

- Python code for test file (if test task)
- Minimal diff — only the files needed
- Explanation of what was changed and why

## Risk Notes

- test must not modify production logic
- test must fail on invalid input before passing

## Instruction

Generate a MINIMAL, TARGETED patch that addresses the objective above.
Do NOT modify any file outside the Allowed Files list.
Do NOT claim tests pass without showing their output.
Do NOT add features beyond the stated objective.
