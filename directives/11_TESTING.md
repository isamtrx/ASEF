# DIRECTIVE-11 — TESTING

## Purpose

Règles de test pour le runtime ASEF. Garantit que tout code livré est couvert,
que les gates de test sont exécutés réellement et que les résultats sont prouvés.

Pourquoi elle existe : les tests non exécutés ou contournés sont une dette critique.
Quand elle est utilisée : toute tâche `feature`, `bugfix`, `refactor`.
Quelle décision elle encadre : ce qui doit être testé et comment prouver que ça passe.
Quelle mauvaise action elle empêche : affirmation de succès sans test exécuté.

## Scope

Couvre : `tests/`, `asef/` (code à tester).
Ne couvre pas : tests d'intégration avec l'API Anthropic (mocker uniquement).
Quand consulter une autre directive : 06_BACKEND.md pour le code, 12_QA.md pour la validation.

## Mandatory Rules

1. [TEST-001] Jamais prétendre qu'un test passe sans l'avoir exécuté.
   - Why: auto-certification interdite par AGENTS.md §4.
   - Blocks: rapport QA sans exit code de pytest.
   - Evidence: output complet de `pytest -q` avec exit code 0.

2. [TEST-002] Tout nouveau code dans asef/ doit avoir un test correspondant.
   - Why: couverture cible 80% sur le code applicatif.
   - Blocks: PR sans tests pour le nouveau code.
   - Evidence: `pytest --tb=short -q` vert + diff montrant tests ajoutés.

3. [TEST-003] Ne jamais désactiver un test sans raison documentée.
   - Why: `@pytest.mark.skip` sans raison = dette silencieuse.
   - Blocks: skip non justifié.
   - Evidence: si skip nécessaire, commentaire `# REASON:` obligatoire.

4. [TEST-004] Ne jamais appeler l'API Anthropic dans les tests.
   - Why: flakiness, coût, sécurité.
   - Blocks: test sans mock pour `anthropic.Anthropic`.
   - Evidence: `ANTHROPIC_API_KEY=dummy pytest -q` → exit 0.

5. [TEST-005] Les tests de sécurité (destructive, protected files, path escape) doivent être présents.
   - Why: défense en profondeur — ces tests valident que asef/tools.py bloque les actions interdites.
   - Blocks: suppression des tests test_tools_reject_*.
   - Evidence: ces 4 tests toujours présents et verts.

## Required Inputs

- `tests/test_orchestrator.py` — tests existants
- `pyproject.toml` — config pytest/ruff

## Required Outputs

- Output de `pytest -q tests/` avec exit code 0
- Nouveaux tests si nouveau code ajouté

## Validation Checklist

- [ ] `pytest -q tests/` → exit 0
- [ ] Aucun test skipped sans raison documentée
- [ ] Aucun appel API Anthropic sans mock
- [ ] Tests de sécurité présents (destructive, protected, path escape, secret)
- [ ] Nouveau code a des tests correspondants

## Rejection Criteria

- `pytest -q` → exit non-zéro → BLOCKED_BY_TEST_FAILURE
- Test skipped sans raison → BLOCKED
- Appel API Anthropic sans mock → BLOCKED_BY_SECURITY

## Related Directives

- `directives/06_BACKEND.md` — code Python
- `directives/12_QA.md` — validation QA
- `gates/testing.gate.md` — gate G4

## Evidence Required

- `pytest -q tests/ 2>&1` — output complet + exit code
- `pytest --tb=short tests/ 2>&1` si échec — traceback complet
