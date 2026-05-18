# Policy : TOOL_ACCESS

**ID** : POL-TOOL-ACCESS-001
**Source** : AGENTS.md §3 + tools.registry.json
**Statut** : Actif
**Version** : 1.0.0

## Description

Définit quels outils chaque rôle agent peut utiliser.
Implémenté dans `asef/tools.py#ToolExecutor.check_permission()`.

## Matrice d'accès

| Outil | orchestrator | architect | developer | qa | security | docs |
|---|---|---|---|---|---|---|
| `read_file` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `list_directory` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `write_file` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `run_command` | ✓ | — | ✓ | ✓ | ✓ | — |
| `escalate` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Règles

- **POL-TOOL-001** : Un agent ne peut pas appeler un outil hors de sa whitelist.
- **POL-TOOL-002** : `run_command` est interdit à `architect` et `docs`.
  Ces rôles produisent des fichiers, pas des commandes shell.
- **POL-TOOL-003** : `escalate` est accessible à tous les rôles car tout agent peut
  détecter une situation nécessitant escalade humaine.
- **POL-TOOL-004** : `write_file` est contraint par `PROTECTED_FILES` indépendamment du rôle.
  Voir `policies/DESTRUCTIVE_ACTIONS.md`.
- **POL-TOOL-005** : Les accès sont journalisés dans `memory/tool_calls.jsonl`.

## Restrictions supplémentaires par outil

### run_command — whitelist de commandes par rôle

| Rôle | Commandes autorisées |
|---|---|
| `orchestrator` | ruff, pytest, pip-audit, gitleaks, semgrep, asef |
| `developer` | ruff, pytest, pip install (sans --user sur CI) |
| `qa` | pytest, ruff, coverage |
| `security` | gitleaks, semgrep, pip-audit, bandit |

Toute commande non listée est rejetée par `DESTRUCTIVE_PATTERNS` ou par whitelist absence.
