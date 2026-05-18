# Copilot CLI Prompt -- T-a4fd931c

**task_id**: T-a4fd931c
**task_type**: documentation_update
**generated_at**: 2026-05-17T14:08:37.899004+00:00

## Task Objective

Update changelog and memory documentation files.

## Directives to Respect

Refer to the following directives before generating any code:
- directives/00_MASTER.md (mandatory)
- directives/11_TESTING.md (if adding tests)
- directives/12_QA.md (if QA task)
- directives/13_SECURITY.md (if security-relevant)

## Agents Assigned

orchestrator, docs, qa

## Skills Required

documentation_update, memory_update

## Tools Allowed

read_file, write_file

## Gates That Will Run

scope_gate, documentation_quality_gate, memory_update_gate, diff_review_gate

## Contracts

(none specified)

## Allowed Files (ONLY modify these)

- CHANGELOG.md
- MEMORY.md

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

- approval required if policies, security, registry, schemas, or destructive action are touched

## Instruction

Generate a MINIMAL, TARGETED patch that addresses the objective above.
Do NOT modify any file outside the Allowed Files list.
Do NOT claim tests pass without showing their output.
Do NOT add features beyond the stated objective.
Do NOT commit automatically.
Do NOT change package dependencies.
