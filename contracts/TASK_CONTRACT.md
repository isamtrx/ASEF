# CONTRACT: TASK INPUT

**Schema** : `schemas/task.schema.json`
**Version** : 1.0.0
**ID** : CONTRACT-TASK-001

## Description

Contrat d'entrée pour toute tâche soumise à l'orchestrateur ASEF.

## Champs obligatoires

| Champ | Type | Contrainte |
|---|---|---|
| `task_id` | string | Pattern `T-[0-9a-f]{8}` — généré par `route_task.py` |
| `description` | string | ≥ 5 mots minimum (Gate G0) |

## Champs optionnels

| Champ | Type | Défaut |
|---|---|---|
| `task_type` | enum | Classifié automatiquement si absent |
| `priority` | enum | `medium` si absent |
| `created_at` | ISO 8601 | Injecté par `route_task.py` |
| `requester` | string | Identifiant humain ou agent déclencheur |

## Exemple valide

```json
{
  "task_id": "T-a1b2c3d4",
  "description": "Fix authentication bug in asef/gates.py",
  "task_type": "bugfix",
  "priority": "high",
  "created_at": "2026-05-17T10:00:00Z",
  "requester": "human"
}
```

## Erreurs de rejet

| Erreur | Gate | Action |
|---|---|---|
| `task_id` malformé | G0 | Rejeter, régénérer |
| `description` < 5 mots | G0 | Rejeter, demander précision |
| `task_type` hors enum | G1 | Reclassifier automatiquement |
| Tâche hors SCOPE.md | G1 | Escalade |
