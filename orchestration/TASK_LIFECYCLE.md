# ORCHESTRATION — TASK LIFECYCLE

## Purpose

Décrit le cycle de vie complet d'une tâche ASEF, de la création à l'archivage.
Référence les états de `STATE_MACHINE.md` et les workflows de `WORKFLOWS.md`.

## Cycle de vie complet

### Étape 0 — Réception

**Entrée** : description texte de la tâche (≥ 5 mots)
**Gate G0** : Vérifier que la description est recevable
- Description ≥ 5 mots : OUI
- SCOPE.md présent : OUI
- Résultat : `CLASSIFIED` ou `REJECTED`

### Étape 1 — Classification et scope

**Action** : Déterminer le `task_type` (voir ROUTING.md — Classification Rules)
**Gate G1** : Vérifier que la tâche est IN scope (SCOPE.md)
- Si hors scope → `REJECTED` + escalade
- Si in scope → `CONTEXT_LOADED`

### Étape 2 — Chargement du contexte (bootstrap)

**Ordre de lecture obligatoire** :
1. `AGENTS.md` (constitution)
2. `MEMORY.md` (état courant)
3. `SCOPE.md` (périmètre)
4. `DECISIONS.md` (décisions actives)
5. Directives requises selon routing
6. Contrats et schemas requis

**État** : `CONTEXT_LOADED`

### Étape 3 — Routage

**Action** : Sélectionner selon ROUTING.md :
- Directives requises
- Agents requis
- Skills requis
- Tools autorisés
- Gates requis
- Approbation humaine requise ?

**Action** : Vérifier registry intégrité :
- Tous les agents listés existent dans `registry/agents.registry.json`
- Tous les skills listés existent dans `registry/skills.registry.json`

**État** : `ROUTED`

### Étape 4 — Planification

**Action** : Produire le plan d'orchestration JSON :
```json
{
  "task_id": "T-<8hex>",
  "task_type": "<string>",
  "planned_agents": ["<role>"],
  "planned_skills": ["<skill_name>"],
  "planned_tools": ["<tool_name>"],
  "planned_gates": ["G0", "G1", "..."],
  "approval_required": "<boolean>",
  "estimated_steps": "<integer>",
  "risks": ["<string>"]
}
```

**État** : `PLANNED`

### Étape 5 — Approbation (si requise)

Si `approval_required = true` ou task_type ∈ {release, governance} :
- Pipeline pause → `APPROVAL_PENDING`
- Présenter le plan à l'humain
- Attendre réponse explicite
- Réponse OK → `APPROVED_FOR_EXECUTION`
- Refus → `REJECTED`

Si `approval_required = false` :
- Passer directement à `APPROVED_FOR_EXECUTION`

### Étape 6 — Exécution

**État** : `IN_PROGRESS`
**Action** : Lancer les agents dans l'ordre du workflow
- Chaque agent lit ses directives AVANT d'agir
- Chaque agent produit un output conforme à son contrat
- Chaque output est validé contre son schema JSON

**Gestion des erreurs** :
- Output non conforme → `BLOCKED_BY_SCHEMA_FAILURE`
- Agent timeout → log + escalade
- Injection détectée → escalade CRITIQUE immédiate

### Étape 7 — Validation des gates

**État** : `VALIDATING`
**Séquence** :
- G3 (lint) : `ruff check .` → exit 0 requis
- G4 (tests) : `pytest -q tests/` → exit 0 requis
- G5 (sécurité) : gitleaks + pip-audit → aucun finding CRITIQUE
- G6 (docs) : CHANGELOG.md + SESSION_LOG.md + evidence package

**Si gate rouge** :
- État : `NEEDS_FIX`
- DEVELOPER corrige
- Retour à `IN_PROGRESS`
- Max 3 tentatives → `BLOCKED_BY_TEST_FAILURE` + escalade

**Si tous gates verts** :
- État : `COMPLETED`

### Étape 8 — Archivage

**Gate G6 final** :
- CHANGELOG.md mis à jour
- SESSION_LOG.md mis à jour
- Evidence package dans `artifacts/`
- `memory/task_history.jsonl` appended

**État** : `ARCHIVED`
**Outcome** : `success`

## Métriques collectées par tâche

Chaque tâche archivée doit avoir dans `memory/task_history.jsonl` :

```json
{
  "task_id": "T-<8hex>",
  "task_type": "<string>",
  "created_at": "ISO8601",
  "archived_at": "ISO8601",
  "outcome": "<success|blocked|escalated|rejected>",
  "agents_used": ["<role>"],
  "gates_passed": ["<gate>"],
  "gates_failed": ["<gate>"],
  "iterations": "<integer>",
  "files_touched": ["<path>"],
  "escalations": "<integer>"
}
```
