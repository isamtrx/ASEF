# Contract : TOOL_CALL

**Schéma de référence** : `schemas/tool_call.schema.json`
**Version** : 1.0.0

## Description

Un appel d'outil est produit par `asef/tools.py#ToolExecutor` à chaque exécution de tool.
Il doit être consigné dans `memory/tool_calls.jsonl` via `execution/append_memory.py`.

## Champs obligatoires

| Champ | Type | Description |
|---|---|---|
| `tool_id` | enum | `read_file`, `write_file`, `run_command`, `list_directory`, `escalate` |
| `agent_role` | enum | Rôle de l'agent qui appelle |
| `timestamp` | ISO 8601 | Heure d'exécution UTC |

## Champs conditionnels

| Champ | Condition | Description |
|---|---|---|
| `input_path` | Si `read_file` ou `write_file` ou `list_directory` | Chemin accédé |
| `command` | Si `run_command` | Commande exécutée (sans secrets) |
| `exit_code` | Si `run_command` | Code retour de la commande |
| `blocked` | Toujours présent si outil bloqué | `true` |
| `block_reason` | Si `blocked = true` | Pattern ou règle qui a bloqué |
| `escalation_id` | Si `tool_id = escalate` | ID de l'escalade générée |

## Règle d'enregistrement

- Chaque appel DOIT être enregistré, qu'il soit bloqué ou autorisé.
- Les appels bloqués sont les plus importants à consigner.
- Jamais mettre de valeur secrète dans `command`.

## Exemples valides

**run_command autorisé :**
```json
{
  "tool_id": "run_command",
  "agent_role": "developer",
  "timestamp": "2026-05-17T14:00:00Z",
  "command": "pytest -q tests/",
  "exit_code": 0,
  "blocked": false
}
```

**run_command bloqué :**
```json
{
  "tool_id": "run_command",
  "agent_role": "developer",
  "timestamp": "2026-05-17T14:01:00Z",
  "command": "rm -rf .git",
  "blocked": true,
  "block_reason": "DESTRUCTIVE_PATTERN: rm -rf"
}
```

**escalate :**
```json
{
  "tool_id": "escalate",
  "agent_role": "security",
  "timestamp": "2026-05-17T14:05:00Z",
  "blocked": false,
  "escalation_id": "ESC-a1b2c3d4"
}
```
