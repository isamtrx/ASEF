# DIRECTIVE-06 — BACKEND

## Purpose

Règles d'implémentation backend pour le repo ASEF Runtime (Python pur).

> Cette directive est un wrapper de `.github/instructions/backend.instructions.md`.
> Les règles détaillées de style Python, typage, docstrings et patterns autorisés/interdits
> sont définies dans ce fichier. Ne pas les dupliquer ici.

Pourquoi elle existe : garantir que toute modification de `asef/*.py` respecte les standards
définis et ne casse pas le runtime existant.
Quand elle est utilisée : tâche de type `feature`, `bugfix`, `refactor`.
Quelle décision elle encadre : implémentation Python dans le package `asef/`.
Quelle mauvaise action elle empêche : code sans tests, modification d'API publique sans ADR,
patterns dangereux (eval, shell=True, pickle).

## Scope

Couvre : `asef/*.py`, `tests/`, `pyproject.toml`.
Ne couvre pas : fichiers de gouvernance (AGENTS.md, etc.), frontaux (il n'y en a pas).
Quand consulter une autre directive : 11_TESTING.md pour les tests, 13_SECURITY.md pour sécurité.

## Mandatory Rules

Voir règles complètes : `.github/instructions/backend.instructions.md`

1. [BACK-001] Python 3.11+ uniquement. Type annotations obligatoires sur fonctions publiques.
   - Why: la codebase est typée — les annotations permettent la validation statique.
   - Blocks: fonctions publiques sans annotations.
   - Evidence: `ruff check .` → exit 0.

2. [BACK-002] Toute modification de `asef/*.py` doit maintenir la compatibilité CLI.
   - Why: `asef run|status|bootstrap|gates|show-config` sont des APIs publiques.
   - Blocks: changement cassant d'API CLI sans ADR.
   - Evidence: `pytest -q tests/` → exit 0 après modification.

3. [BACK-003] Jamais `subprocess.run(..., shell=True)` sur une variable non-sanitisée.
   - Why: injection de commande — OWASP A03.
   - Blocks: tout appel shell non-sanitisé.
   - Evidence: `ruff check .` + revue manuelle du diff.

4. [BACK-004] Jamais `eval` ou `exec` sur des inputs externes.
   - Why: exécution de code arbitraire — OWASP A03.
   - Blocks: tout eval/exec sur input non-trusted.
   - Evidence: pas d'occurrence dans le diff.

5. [BACK-005] Toute nouvelle dépendance nécessite justification dans CHANGELOG.md.
   - Why: les dépendances créent des vecteurs d'attaque supply-chain.
   - Blocks: ajout de dépendance sans documentation.
   - Evidence: entrée CHANGELOG.md section Unreleased + pip-audit clean.

## Required Inputs

- `.github/instructions/backend.instructions.md` — standards complets
- `pyproject.toml` — config ruff et dépendances
- `tests/test_orchestrator.py` — tests existants à ne pas casser

## Required Outputs

- Code Python passant `ruff check .` (exit 0)
- Tests passant `pytest -q` (exit 0)
- CHANGELOG.md mis à jour si changement livrable

## Validation Checklist

- [ ] `ruff check .` → exit 0
- [ ] `pytest -q tests/` → exit 0
- [ ] Aucune régression sur `asef run|status|bootstrap|gates|show-config`
- [ ] Aucun `eval/exec` sur input externe
- [ ] Aucun `shell=True` non-sanitisé
- [ ] CHANGELOG.md mis à jour

## Rejection Criteria

- `ruff check .` → exit non-zéro → BLOCKED_BY_TEST_FAILURE
- `pytest -q` → exit non-zéro → BLOCKED_BY_TEST_FAILURE
- Secret dans le code → BLOCKED_BY_SECURITY
- Modification de AGENTS.md/SCOPE.md sans ADR → BLOCKED_BY_POLICY

## Related Directives

- `directives/11_TESTING.md` — tests
- `directives/13_SECURITY.md` — sécurité
- `directives/20_GOVERNANCE.md` — ADR et décisions

## Evidence Required

- `ruff check . 2>&1` — output complet + exit code
- `pytest -q tests/ 2>&1` — output complet + exit code
- diff des fichiers modifiés
