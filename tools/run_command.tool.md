# tool: run_command

**id**: run_command
**level**: EXECUTE_SAFE
**implementation**: asef/tools.py

## Description

Exécuter une commande shell filtrée. Les patterns destructifs sont bloqués
avant l'exécution par `asef/tools.py`.

## Input

```json
{"tool": "run_command", "command": "<string>", "cwd": "<string optional>", "timeout": "<integer optional, default 60>"}
```

## Output

```json
{"exit_code": "<integer>", "stdout": "<string>", "stderr": "<string>", "command": "<string>"}
```

## Commandes autorisées (whitelist par agent)

| Agent | Commandes autorisées |
|---|---|
| developer | ruff, pytest, pip install |
| qa | ruff, pytest |
| security | gitleaks, semgrep, pip-audit |
| orchestrator | python execution/*.py, ruff, pytest |

## Patterns bloqués (asef/tools.py — DESTRUCTIVE_PATTERNS)

```
rm -rf
DROP TABLE
git push --force
git push -f
dd if=
mkfs
format c:
del /f /s /q
```

Si pattern détecté → commande bloquée, erreur retournée, escalade loggée.

## Erreur si pattern destructif

```json
{"exit_code": -1, "error": "DESTRUCTIVE_PATTERN_BLOCKED", "command": "<string>"}
```

## Timeout

Défaut : 60 secondes. Maximum autorisé : 300 secondes (configurable dans `config/tools.config.json`).
Si timeout → exit_code = -2, stdout/stderr capturés jusqu'au timeout.

## Validation

`python execution/validate_tools.py` → vérifie que les patterns bloqués sont actifs
