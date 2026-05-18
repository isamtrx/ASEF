# CONTRACT: ORCHESTRATION PLAN

**Schema** : `schemas/orchestration_plan.schema.json`
**Version** : 1.0.0
**ID** : CONTRACT-ORCH-PLAN-001

## Description

Plan produit par `execution/route_task.py` avant l'exécution.
Validé par l'orchestrateur en Gate G1 avant de commencer.

## Champs obligatoires

| Champ | Type | Contrainte |
|---|---|---|
| `task_id` | string | Pattern `T-[0-9a-f]{8}` |
| `task_type` | enum | 8 valeurs possibles |
| `planned_agents` | array | Minimum 1 agent, valeurs dans l'enum des rôles |
| `planned_gates` | array | Minimum 1 gate, pattern `G[0-7]` |
| `approval_required` | boolean | Toujours `true` pour release et governance |

## Invariants

1. `G0` et `G1` toujours présents dans `planned_gates`
2. Si `task_type == "release"` → `approval_required == true` et `G7` dans les gates
3. Si `task_type == "governance"` → `approval_required == true` et `G2` dans les gates
4. `planned_agents` inclut toujours `orchestrator`
5. Tous les agents listés doivent être dans `registry/agents.registry.json`

## Exemple valide

```json
{
  "task_id": "T-a1b2c3d4",
  "task_type": "bugfix",
  "planned_agents": ["orchestrator", "developer", "qa", "security", "docs"],
  "planned_skills": ["code_review", "test_generation", "security_review"],
  "planned_tools": ["read_file", "write_file", "run_command", "escalate"],
  "planned_gates": ["G0", "G1", "G3", "G4", "G5", "G6"],
  "approval_required": false,
  "estimated_steps": 7,
  "risks": ["regression risk if tests incomplete"]
}
```

## Validation

`python execution/validate_schemas.py` → valide le schema
`python execution/route_task.py --dry-run "..."` → teste la production de plan
