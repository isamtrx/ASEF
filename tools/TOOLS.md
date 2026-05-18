# TOOLS — Index

## Purpose

Catalogue des outils autorisés dans ASEF Runtime.
Chaque outil a un niveau d'accès, une description et des contraintes d'usage.

Implémentation réelle : `asef/tools.py` — `class ToolExecutor`.

## Catalogue

| Tool | Niveau | Fichier | Description |
|---|---|---|---|
| `read_file` | READ_ONLY | `tools/read_file.tool.md` | Lecture de fichiers |
| `list_directory` | READ_ONLY | `tools/list_directory.tool.md` | Liste de répertoires |
| `write_file` | WRITE_WORKSPACE | `tools/write_file.tool.md` | Écriture dans le workspace |
| `run_command` | EXECUTE_SAFE | `tools/run_command.tool.md` | Commandes shell filtrées |
| `escalate` | EXECUTE_SAFE | `tools/escalate.tool.md` | Escalade humaine |

## Niveaux d'accès

| Niveau | Description |
|---|---|
| `READ_ONLY` | Lecture uniquement, aucun effet de bord |
| `WRITE_WORKSPACE` | Écriture dans le workspace, filtrée par PROTECTED_FILES |
| `EXECUTE_SAFE` | Exécution filtrée (patterns destructifs bloqués) |
| `EXECUTE_UNRESTRICTED` | INTERDIT — jamais autorisé à un agent |

## Règles globales

1. Chaque agent ne peut utiliser que les outils listés dans son contrat agent.md
2. Tout outil EXECUTE_SAFE passe par le filtre de `asef/tools.py`
3. Patterns destructifs filtrés : `rm -rf`, `DROP TABLE`, `git push --force`, `dd if=`
4. PROTECTED_FILES : AGENTS.md, SCOPE.md, PROJECT.md, docs/security/SECURITY.md
5. Validation : `python execution/validate_tools.py`
