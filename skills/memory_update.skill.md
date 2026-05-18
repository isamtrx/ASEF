# skill: memory_update

**id**: memory_update
**version**: 1.0.0
**agents**: orchestrator, docs
**tools_required**: read_file, write_file

## Purpose

Mettre à jour les fichiers de mémoire structurée après une tâche.

## When to Use

- Fin de chaque tâche (obligatoire si outcome = success)
- Après résolution d'un incident
- Quand une décision structurante est prise

## Fichiers à mettre à jour

| Condition | Fichier | Action |
|---|---|---|
| Toujours | `memory/task_history.jsonl` | Append entrée JSON |
| Toujours | `SESSION_LOG.md` | Append section |
| Nouvelle décision | `memory/decisions.jsonl` | Append entrée JSON |
| Leçon apprise | `memory/lessons.jsonl` | Append entrée JSON |
| Risque identifié | `memory/risks.jsonl` | Append entrée JSON |
| Fin de session | `MEMORY.md` (racine) | Mise à jour par orchestrator |

## Format SESSION_LOG.md

```markdown
## <YYYY-MM-DD HH:MM> — <résumé bref>

- Objectif : <description tâche>
- Actions : <liste des actions clés>
- Fichiers modifiés : <liste>
- Outcome : success | blocked | escalated | rejected
- Gates : G3=<pass/fail>, G4=<pass/fail>, G5=<pass/fail>
```

## Format task_history.jsonl

```json
{"task_id": "T-<8hex>", "task_type": "<string>", "created_at": "<ISO8601>", "archived_at": "<ISO8601>", "outcome": "<success|blocked|escalated|rejected>", "agents_used": ["<role>"], "gates_passed": ["<gate>"], "gates_failed": ["<gate>"], "iterations": 0, "files_touched": ["<path>"], "escalations": 0}
```

## Rules

1. Toujours `read_file(memory/task_history.jsonl)` avant d'écrire pour vérifier le format
2. Append-only — ne jamais modifier ou supprimer une entrée existante
3. Ne jamais écrire dans MEMORY.md (racine) sauf orchestrateur en fin de session
4. Ne jamais écrire de secret ou de credential dans la mémoire

## Edge Cases

- `task_history.jsonl` vide → commencer par une ligne valide
- SESSION_LOG.md très long → ajouter à la fin, ne pas tronquer
