# ORCHESTRATION — STATE MACHINE

## Purpose

Définit les états possibles d'une tâche dans le pipeline ASEF et les transitions valides.
Implémenté dans `asef/orchestrator.py` — les états ici sont la spécification formelle.

## États de tâche

```
TASK_CREATED
  ↓
CLASSIFIED        ← task_type déterminé
  ↓
CONTEXT_LOADED    ← AGENTS.md, MEMORY.md, SCOPE.md, DECISIONS.md lus
  ↓
ROUTED            ← directives, agents, skills, tools sélectionnés
  ↓
PLANNED           ← plan d'orchestration JSON produit
  ↓
APPROVAL_PENDING  ← (si approval_required = true)
  ↓
APPROVED_FOR_EXECUTION
  ↓
IN_PROGRESS       ← agents actifs
  ↓
VALIDATING        ← gates G3-G6 en cours
  ↓
NEEDS_FIX         ← gate rouge, agent corrective en cours
  ↓
COMPLETED         ← tous gates passés
  ↓
ARCHIVED          ← SESSION_LOG.md écrit, artifacts stockés
```

## États bloquants

Ces états arrêtent le pipeline et nécessitent une action humaine ou une correction.

| État bloquant | Cause | Action requise |
|---|---|---|
| `BLOCKED_BY_MISSING_DIRECTIVE` | Directive requise introuvable | Créer la directive ou corriger le registry |
| `BLOCKED_BY_POLICY` | Action interdite par une policy | Révision humaine |
| `BLOCKED_BY_SECURITY` | Secret, CVE HIGH ou injection détectée | Escalade humaine immédiate |
| `BLOCKED_BY_ACCESSIBILITY` | N/A (pas de frontend dans ce repo) | — |
| `BLOCKED_BY_TEST_FAILURE` | `pytest` ou `ruff` rouge | Correction code, re-run |
| `BLOCKED_BY_SCHEMA_FAILURE` | Output ne valide pas le schema JSON | Corriger l'output agent |
| `BLOCKED_BY_APPROVAL_REQUIRED` | Gate G7 ou tâche critique | Validation humaine |
| `BLOCKED_BY_AMBIGUOUS_REQUIREMENT` | Description trop vague | Clarification humaine |
| `REJECTED` | G0 ou G1 non passé | Reformuler ou corriger le scope |

## Transitions valides

```
TASK_CREATED       → CLASSIFIED
CLASSIFIED         → CONTEXT_LOADED
CONTEXT_LOADED     → ROUTED
ROUTED             → PLANNED
PLANNED            → APPROVAL_PENDING (si approval_required)
PLANNED            → APPROVED_FOR_EXECUTION (si pas d'approbation requise)
APPROVAL_PENDING   → APPROVED_FOR_EXECUTION (approbation humaine reçue)
APPROVAL_PENDING   → REJECTED (refus humain)
APPROVED_FOR_EXECUTION → IN_PROGRESS
IN_PROGRESS        → VALIDATING
VALIDATING         → COMPLETED (tous gates verts)
VALIDATING         → NEEDS_FIX (gate rouge)
NEEDS_FIX          → IN_PROGRESS (correction en cours)
NEEDS_FIX          → BLOCKED_BY_TEST_FAILURE (après 3 tentatives)
COMPLETED          → ARCHIVED
```

## Transitions interdites

- Sauter CLASSIFIED → IN_PROGRESS (pas de routage = interdit)
- Sauter PLANNED → IN_PROGRESS (pas de plan = interdit)
- COMPLETED → non archivé (SESSION_LOG.md obligatoire)
- REJECTED → IN_PROGRESS (task rejetée ne peut pas démarrer)

## Mapping aux PipelineResult outcomes

| State Terminal | outcome Python |
|---|---|
| ARCHIVED | `success` |
| BLOCKED_BY_* | `blocked` |
| APPROVAL_PENDING → humain refuse | `rejected` |
| ESCALATE appelé | `escalated` |
| REJECTED (G0/G1) | `rejected` |

## Implémentation

La machine d'états est gérée implicitement dans `asef/orchestrator.py`.
Les états bloquants sont retournés comme `PipelineResult.outcome`.

Pour rendre la machine d'états explicite dans le code, voir `runtime/README.md`.
