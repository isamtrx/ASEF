# ORCHESTRATION — ROUTING

## Purpose

Table de routage opérationnelle : task_type → directives, agents, skills, tools, gates.
Utilisée par `execution/route_task.py` et `asef/orchestrator.py`.

## Task Types Supportés

| task_type | Description |
|---|---|
| `bugfix` | Correction de bug documenté |
| `feature` | Implémentation de nouvelle fonctionnalité |
| `review` | Revue de code ou d'architecture |
| `audit` | Audit du repo, de la sécurité ou de la qualité |
| `release` | Préparation d'une release |
| `security` | Revue ou correction de sécurité |
| `documentation` | Mise à jour de documentation |
| `governance` | Décision ADR ou modification de gouvernance |

---

## Routing Table

### bugfix

```json
{
  "task_type": "bugfix",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/06_BACKEND.md",
    "directives/11_TESTING.md",
    "directives/13_SECURITY.md"
  ],
  "required_agents": ["orchestrator", "developer", "qa", "security", "docs"],
  "required_skills": ["code_review", "test_generation"],
  "allowed_tools": ["read_file", "list_directory", "write_file", "run_command", "escalate"],
  "required_gates": ["G0", "G1", "G3", "G4", "G5", "G6"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/TASK_CONTRACT.md",
    "contracts/AGENT_OUTPUT_CONTRACT.md"
  ]
}
```

### feature

```json
{
  "task_type": "feature",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/06_BACKEND.md",
    "directives/11_TESTING.md",
    "directives/13_SECURITY.md",
    "directives/17_DOCUMENTATION.md"
  ],
  "required_agents": ["orchestrator", "architect", "developer", "qa", "security", "docs"],
  "required_skills": ["code_review", "test_generation", "documentation_update"],
  "allowed_tools": ["read_file", "list_directory", "write_file", "run_command", "escalate"],
  "required_gates": ["G0", "G1", "G2", "G3", "G4", "G5", "G6"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/TASK_CONTRACT.md",
    "contracts/AGENT_OUTPUT_CONTRACT.md"
  ]
}
```

### review

```json
{
  "task_type": "review",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/06_BACKEND.md",
    "directives/12_QA.md"
  ],
  "required_agents": ["orchestrator", "qa"],
  "required_skills": ["code_review"],
  "allowed_tools": ["read_file", "list_directory", "escalate"],
  "required_gates": ["G0", "G1", "G3", "G4"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/REVIEW_CONTRACT.md"
  ]
}
```

### audit

```json
{
  "task_type": "audit",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/09_AGENT_SYSTEM.md",
    "directives/12_QA.md",
    "directives/13_SECURITY.md"
  ],
  "required_agents": ["orchestrator", "qa", "security"],
  "required_skills": ["repo_audit", "security_review"],
  "allowed_tools": ["read_file", "list_directory", "run_command", "escalate"],
  "required_gates": ["G0", "G1", "G3", "G4", "G5"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/QA_REPORT_CONTRACT.md",
    "contracts/SECURITY_REPORT_CONTRACT.md"
  ]
}
```

### release

```json
{
  "task_type": "release",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/12_QA.md",
    "directives/13_SECURITY.md",
    "directives/17_DOCUMENTATION.md",
    "directives/20_GOVERNANCE.md"
  ],
  "required_agents": ["orchestrator", "qa", "security", "docs"],
  "required_skills": ["repo_audit", "security_review", "documentation_update"],
  "allowed_tools": ["read_file", "list_directory", "run_command", "escalate"],
  "required_gates": ["G0", "G1", "G3", "G4", "G5", "G6", "G7"],
  "approval_required": true,
  "expected_contracts": [
    "contracts/RELEASE_REPORT_CONTRACT.md"
  ]
}
```

### security

```json
{
  "task_type": "security",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/13_SECURITY.md"
  ],
  "required_agents": ["orchestrator", "security"],
  "required_skills": ["security_review"],
  "allowed_tools": ["read_file", "list_directory", "run_command", "escalate"],
  "required_gates": ["G0", "G1", "G5"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/SECURITY_REPORT_CONTRACT.md"
  ]
}
```

### documentation

```json
{
  "task_type": "documentation",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/17_DOCUMENTATION.md"
  ],
  "required_agents": ["orchestrator", "docs"],
  "required_skills": ["documentation_update", "memory_update"],
  "allowed_tools": ["read_file", "list_directory", "write_file", "escalate"],
  "required_gates": ["G0", "G1", "G6"],
  "approval_required": false,
  "expected_contracts": [
    "contracts/MEMORY_ENTRY_CONTRACT.md"
  ]
}
```

### governance

```json
{
  "task_type": "governance",
  "required_directives": [
    "directives/00_MASTER.md",
    "directives/20_GOVERNANCE.md",
    "directives/09_AGENT_SYSTEM.md"
  ],
  "required_agents": ["orchestrator", "architect"],
  "required_skills": ["repo_audit"],
  "allowed_tools": ["read_file", "list_directory", "write_file", "escalate"],
  "required_gates": ["G0", "G1", "G2"],
  "approval_required": true,
  "expected_contracts": [
    "contracts/ORCHESTRATION_PLAN_CONTRACT.md"
  ]
}
```

---

## Classification Rules

Si task_type inconnu, l'orchestrateur applique ces règles dans l'ordre :

1. Contient "fix", "bug", "repair", "correct" → `bugfix`
2. Contient "add", "implement", "feature", "create" → `feature`
3. Contient "review", "check", "inspect", "validate" → `review`
4. Contient "audit", "scan", "assess" → `audit`
5. Contient "release", "version", "publish" → `release`
6. Contient "security", "vuln", "cve", "secret" → `security`
7. Contient "doc", "documentation", "readme", "changelog" → `documentation`
8. Contient "decision", "adr", "governance", "scope" → `governance`
9. Défaut → `feature` (le plus complet)

## Fallback

Si classification échoue → task_type = `feature` (pipeline complet, le plus sûr).

## Validation

Script : `python execution/validate_orchestration.py`
Chaque task_type doit référencer des directives, agents, skills, tools et gates existants.
