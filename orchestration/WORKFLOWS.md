# ORCHESTRATION — WORKFLOWS

## Purpose

Workflows nommés avec séquences d'agents, skills, tools et gates.
Référencés par `registry/workflows.registry.json` et `execution/route_task.py`.

---

## BUGFIX_WORKFLOW

**Déclencheur** : task_type = `bugfix`

**Séquence** :
1. ORCHESTRATOR : classify + scope check (G0, G1)
2. DEVELOPER : lire code, corriger bug, écrire/mettre à jour tests
3. QA : `ruff check .` (G3) + `pytest -q` (G4)
4. SECURITY : gitleaks + pip-audit (G5)
5. DOCS : CHANGELOG.md + SESSION_LOG.md (G6)

**Agents mobilisés** : orchestrator, developer, qa, security, docs
**Skills** : code_review, test_generation
**Gates** : G0, G1, G3, G4, G5, G6
**Approval** : non
**Output** : DEVELOPER.output_contract + QA.output_contract + fichiers modifiés

---

## FEATURE_IMPLEMENTATION_WORKFLOW

**Déclencheur** : task_type = `feature`

**Séquence** :
1. ORCHESTRATOR : classify + scope check (G0, G1)
2. ARCHITECT : analyse structurelle, ADR si décision structurante (G2)
3. DEVELOPER : implémenter feature + tests
4. QA : G3 + G4
5. SECURITY : G5
6. DOCS : G6

**Agents mobilisés** : orchestrator, architect, developer, qa, security, docs
**Skills** : code_review, test_generation, documentation_update
**Gates** : G0, G1, G2, G3, G4, G5, G6
**Approval** : non (sauf si structurant → G7 humain pour ADR)
**Output** : ADR si structurant + code + tests + CHANGELOG.md

---

## AUDIT_WORKFLOW

**Déclencheur** : task_type = `audit`

**Séquence** :
1. ORCHESTRATOR : classify + scope check
2. QA : lint + tests (G3, G4)
3. SECURITY : full G5 (gitleaks + semgrep + pip-audit)
4. DOCS : rapport d'audit dans artifacts/audits/

**Agents mobilisés** : orchestrator, qa, security, docs
**Skills** : repo_audit, security_review
**Gates** : G0, G1, G3, G4, G5
**Approval** : non
**Output** : rapport audit dans artifacts/audits/

---

## SECURITY_REVIEW_WORKFLOW

**Déclencheur** : task_type = `security`

**Séquence** :
1. ORCHESTRATOR : classify + scope check
2. SECURITY : gitleaks + semgrep + pip-audit (G5)
3. DOCS : rapport dans artifacts/security/

**Agents mobilisés** : orchestrator, security, docs
**Skills** : security_review
**Gates** : G0, G1, G5
**Approval** : non (escalade si finding critique)
**Output** : rapport sécurité formaté

---

## RELEASE_WORKFLOW

**Déclencheur** : task_type = `release`

**Séquence** :
1. ORCHESTRATOR : classify + scope check
2. QA : full G3 + G4
3. SECURITY : full G5
4. DOCS : G6 — evidence package complet
5. HUMAIN : Gate G7 (approbation obligatoire)

**Agents mobilisés** : orchestrator, qa, security, docs
**Skills** : repo_audit, security_review, documentation_update
**Gates** : G0, G1, G3, G4, G5, G6, G7
**Approval** : OUI — Gate G7 toujours humain
**Output** : evidence package + CHANGELOG.md version bump + tag git

---

## GOVERNANCE_WORKFLOW

**Déclencheur** : task_type = `governance`

**Séquence** :
1. ORCHESTRATOR : classify + scope check
2. ARCHITECT : analyser la décision, produire ADR
3. HUMAIN : valider l'ADR
4. DOCS : mettre à jour DECISIONS.md

**Agents mobilisés** : orchestrator, architect, docs
**Skills** : repo_audit
**Gates** : G0, G1, G2
**Approval** : OUI — décision structurante toujours humaine
**Output** : ADR dans docs/adr/ + entrée DECISIONS.md

---

## DIRECTIVE_UPDATE_WORKFLOW

**Déclencheur** : modification d'un fichier dans `directives/`

**Séquence** :
1. ORCHESTRATOR : classify
2. ARCHITECT : vérifier cohérence avec AGENTS.md
3. Exécuter `python execution/validate_directives.py`
4. HUMAIN : si directive modifie des permissions ou le scope

**Agents mobilisés** : orchestrator, architect
**Skills** : repo_audit
**Gates** : G0, G1
**Approval** : si modification de permissions/scope
**Output** : `validate_directives.py` → exit 0

---

## AGENT_CREATION_WORKFLOW

**Déclencheur** : création d'un nouveau fichier dans `agents/`

**Séquence** :
1. ORCHESTRATOR : classify
2. Vérifier format agents/ROLE.agent.md (sections obligatoires)
3. Ajouter entrée dans `registry/agents.registry.json`
4. Exécuter `python execution/validate_agents.py`
5. Exécuter `python execution/validate_registry.py`

**Agents mobilisés** : orchestrator
**Skills** : repo_audit
**Gates** : G0, G1
**Approval** : non
**Output** : `validate_agents.py` → exit 0 + `validate_registry.py` → exit 0

---

## Validation

Script : `python execution/validate_orchestration.py`
Vérifie que chaque workflow référence des agents, skills, tools et gates existants.
