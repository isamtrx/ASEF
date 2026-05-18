# POLICY: DESTRUCTIVE ACTIONS

**Source** : AGENTS.md §4 INTERDIT #9 + asef/tools.py DESTRUCTIVE_PATTERNS
**Statut** : active
**ID** : POL-DESTRUCTIVE-001

## Patterns toujours bloqués

Ces patterns sont filtrés dans `asef/tools.py` (`DESTRUCTIVE_PATTERNS`) avant toute exécution :

```python
DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\s+-rf?\s+/"),
    re.compile(r"\brm\s+-rf?\s+~"),
    re.compile(r"\bmkfs\."),
    re.compile(r"\bdd\s+if="),
    re.compile(r":\(\)\s*\{\s*:\|:"),  # fork bomb
    re.compile(r"\bDROP\s+TABLE", re.IGNORECASE),
    re.compile(r"\bDROP\s+DATABASE", re.IGNORECASE),
    re.compile(r"\bTRUNCATE\s+TABLE", re.IGNORECASE),
    re.compile(r"\bgit\s+push\s+.*--force"),
    re.compile(r"\bgit\s+push\s+.*\s+main\b"),  # push direct sur main
]
```

## Comportement si pattern détecté

1. Commande bloquée — non exécutée
2. Log dans SESSION_LOG.md
3. Retour d'erreur `DESTRUCTIVE_PATTERN_BLOCKED`
4. Escalade automatique si agent continue d'insister

## Exceptions

Aucune exception n'est possible sans validation humaine explicite + ADR.
Même un humain ne peut pas désactiver ce filtre via un prompt.

## Application

`asef/tools.py` — fonction `is_destructive(command)` appelée par `ToolExecutor` AVANT toute exécution shell.
Ce filtre ne peut pas être contourné par un prompt ou une instruction agent.
