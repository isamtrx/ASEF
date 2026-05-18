# CONTRACT: AGENT OUTPUT

**Schema** : `schemas/agent_output.schema.json`
**Version** : 1.0.0
**ID** : CONTRACT-AGENT-OUT-001

## Description

Tout agent ASEF doit produire une sortie conforme à ce contrat.
L'orchestrateur vérifie ce contrat avant de transmettre à la gate suivante.

## Champs obligatoires

| Champ | Type | Contrainte |
|---|---|---|
| `role` | enum | `orchestrator` \| `architect` \| `developer` \| `qa` \| `security` \| `docs` |
| `task_id` | string | Doit correspondre à la tâche en cours |
| `status` | enum | `success` \| `failed` \| `escalated` |
| `summary` | string | Description courte de ce qui a été fait |

## Champs conditionnels

| Champ | Quand requis |
|---|---|
| `escalation` | Si `status == "escalated"` — objet avec `reason`, `recommendation`, `urgency` |
| `gate_g3` | Si rôle `qa` — objet avec `exit_code` (int), `output` (string) |
| `gate_g4` | Si rôle `qa` — objet avec `exit_code` (int), `output` (string) |
| `secret_scan` | Si rôle `security` — objet avec `exit_code`, `tool`, `findings` |
| `sast` | Si rôle `security` — objet avec `exit_code`, `tool`, `findings` |
| `deps_audit` | Si rôle `security` — objet avec `exit_code`, `tool`, `findings` |
| `test_exit_code` | Si rôle `developer` — int (0 = tests ok, non-0 = tests rouges) |
| `lint_exit_code` | Si rôle `developer` — int (0 = lint ok, non-0 = lint rouge) |

## Champs optionnels

| Champ | Type | Description |
|---|---|---|
| `iterations` | int | Nombre d'itérations LLM utilisées |
| `tokens_in` | int | Tokens d'entrée consommés |
| `tokens_out` | int | Tokens de sortie produits |
| `files_modified` | array | Chemins des fichiers modifiés |
| `artifacts` | array | Chemins des artifacts produits |

## Exemple valide (QA)

```json
{
  "role": "qa",
  "task_id": "T-a1b2c3d4",
  "status": "success",
  "summary": "G3 et G4 verts — 12 tests passés, 0 rouges, lint OK",
  "gate_g3": {
    "exit_code": 0,
    "output": "All checks passed."
  },
  "gate_g4": {
    "exit_code": 0,
    "output": "12 passed in 0.42s"
  }
}
```

## Règle absolue

Un agent ne peut PAS auto-certifier un gate rouge comme vert.
`exit_code` doit être le code de retour réel de la commande exécutée.
