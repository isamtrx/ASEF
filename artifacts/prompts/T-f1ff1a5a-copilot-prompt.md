# Copilot CLI Prompt -- T-f1ff1a5a

**task_id**: T-f1ff1a5a
**task_type**: add_test_coverage
**generated_at**: 2026-05-17T14:09:14.736652+00:00

## Task Objective

Add test coverage for gates module

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

- test must not modify production logic
- test must fail on invalid input before passing

## Instruction

Generate a MINIMAL, TARGETED patch that addresses the objective above.
Do NOT modify any file outside the Allowed Files list.
Do NOT claim tests pass without showing their output.
Do NOT add features beyond the stated objective.
Do NOT commit automatically.
Do NOT change package dependencies.
