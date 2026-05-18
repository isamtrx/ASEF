# Memory — Project Memory

## Purpose

Ce fichier est un pointeur. La mémoire projet réelle est dans le fichier racine `MEMORY.md`.

**Ne pas dupliquer** `MEMORY.md` ici.

## Pointer

```
d:\asef-runtime\MEMORY.md
```

## Mémoire structurée complémentaire

Ce répertoire contient les mémoires structurées en format JSONL :

| Fichier | Contenu |
|---|---|
| `decisions.jsonl` | Décisions architecturales (sync avec docs/adr/) |
| `lessons.jsonl` | Leçons apprises (sync avec LESSONS_LEARNED.md) |
| `task_history.jsonl` | Historique des tâches exécutées |
| `agent_runs.jsonl` | Historique des runs d'agents |
| `tool_calls.jsonl` | Historique des appels outils |
| `risks.jsonl` | Risques actifs (sync avec risk register) |

## Rules

- Ne pas modifier ces fichiers à la main
- Utiliser `execution/append_memory.py` pour ajouter des entrées
- MEMORY.md (racine) reste le snapshot humain-lisible
- Les fichiers JSONL sont machine-readable et append-only
