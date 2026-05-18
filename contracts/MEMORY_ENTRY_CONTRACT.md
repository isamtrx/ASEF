# CONTRACT: MEMORY ENTRY

**Schema** : `schemas/memory_entry.schema.json`
**Version** : 1.0.0
**ID** : CONTRACT-MEMORY-001

## Description

Contrat pour toute entrée écrite dans les fichiers JSONL de mémoire.
Écrit via `execution/append_memory.py` uniquement.

## Champs obligatoires

| Champ | Type | Contrainte |
|---|---|---|
| `id` | string | Identifiant unique dans le fichier JSONL |
| `date` | string | Format ISO 8601 `YYYY-MM-DD` |
| `type` | enum | `decision` \| `lesson` \| `risk` \| `task` \| `agent_run` \| `tool_call` |

## Exemples par type

### `task_history.jsonl`
```json
{
  "id": "T-a1b2c3d4",
  "date": "2026-05-17",
  "type": "task",
  "task_type": "bugfix",
  "description": "Fix authentication bug",
  "status": "completed",
  "gates_passed": ["G0", "G1", "G3", "G4", "G5", "G6"],
  "agents_used": ["orchestrator", "developer", "qa", "docs"],
  "duration_minutes": 12
}
```

### `lessons.jsonl`
```json
{
  "id": "LESSON-003",
  "date": "2026-05-17",
  "type": "lesson",
  "error": "Agent self-certified a failed test",
  "cause": "exit_code not checked from real command",
  "rule": "Always read exit_code from subprocess, never infer",
  "source_task": "T-a1b2c3d4"
}
```

### `risks.jsonl`
```json
{
  "id": "RISK-003",
  "date": "2026-05-17",
  "type": "risk",
  "description": "jsonschema not installed — schema meta-validation skipped",
  "severity": "medium",
  "mitigation": "pip install jsonschema",
  "status": "open"
}
```

## Règle absolue

`append_memory.py` est la SEULE façon d'écrire dans ces fichiers.
Écriture directe = violation du contrat.
