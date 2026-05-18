# Contract : SKILL_OUTPUT

**Schéma de référence** : `schemas/skill_output.schema.json`
**Version** : 1.0.0

## Description

Chaque skill produit un output structuré consigné dans `memory/agent_runs.jsonl`.
L'output confirme l'exécution, les artifacts produits, et les preuves fournies.

## Champs obligatoires

| Champ | Type | Description |
|---|---|---|
| `skill_id` | string | ID du skill (ex: `repo_audit`, `code_review`) |
| `agent_role` | enum | Rôle de l'agent qui exécute le skill |
| `task_id` | string | Pattern `T-[0-9a-f]{8}` |
| `status` | enum | `success`, `failed`, `escalated`, `skipped` |

## Champs conditionnels

| Champ | Condition | Description |
|---|---|---|
| `artifacts` | Si `status = success` | Chemins des fichiers produits (array non-vide) |
| `evidence` | Requis pour `security_review` | Objet avec exit codes G5 |
| `output` | Recommandé | Résumé lisible de ce qui a été fait |
| `escalation_id` | Si `status = escalated` | ID de l'escalade |

## Règles

- Un skill avec `status = success` sans `artifacts` n'est valide que si le skill ne produit
  pas de fichiers (ex: `memory_update`).
- Le skill `security_review` DOIT inclure `evidence.secret_scan.exit_code`,
  `evidence.sast.exit_code`, et `evidence.deps_audit.exit_code`.
- Un skill ne peut pas s'auto-certifier `status = success` si les gates associés sont rouges.

## Exemples valides

**repo_audit réussi :**
```json
{
  "skill_id": "repo_audit",
  "agent_role": "qa",
  "task_id": "T-a1b2c3d4",
  "status": "success",
  "output": "Audit complet : 47 fichiers analysés, 3 avertissements",
  "artifacts": ["artifacts/audits/2026-05-17_T-a1b2c3d4_audit.md"]
}
```

**security_review avec evidence :**
```json
{
  "skill_id": "security_review",
  "agent_role": "security",
  "task_id": "T-a1b2c3d4",
  "status": "success",
  "output": "G5 vert : pas de secrets, pas de vulnérabilités critiques",
  "artifacts": ["artifacts/security/2026-05-17_T-a1b2c3d4_g5.md"],
  "evidence": {
    "secret_scan": {"tool": "gitleaks", "exit_code": 0},
    "sast": {"tool": "semgrep", "exit_code": 0},
    "deps_audit": {"tool": "pip-audit", "exit_code": 0}
  }
}
```

**memory_update (pas d'artifact) :**
```json
{
  "skill_id": "memory_update",
  "agent_role": "docs",
  "task_id": "T-a1b2c3d4",
  "status": "success",
  "output": "SESSION_LOG.md mis à jour, memory/lessons.jsonl : 1 entrée ajoutée"
}
```

**Skill échoué :**
```json
{
  "skill_id": "test_generation",
  "agent_role": "developer",
  "task_id": "T-a1b2c3d4",
  "status": "failed",
  "output": "G4 rouge : 3 tests en échec. Skill déclaré failed, pipeline bloqué."
}
```
