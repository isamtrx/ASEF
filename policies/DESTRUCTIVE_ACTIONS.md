# POLICY: DESTRUCTIVE ACTIONS

**Source** : AGENTS.md §4 INTERDIT #9 + asef/tools.py DESTRUCTIVE_PATTERNS
**Statut** : active
**ID** : POL-DESTRUCTIVE-001

## Patterns toujours bloqués

Ces patterns sont filtrés dans `asef/tools.py` avant toute exécution :

```python
DESTRUCTIVE_PATTERNS = [
    r'\brm\s+-rf\b',
    r'\bDROP\s+TABLE\b',
    r'\bgit\s+push\s+--force\b',
    r'\bgit\s+push\s+-f\b',
    r'\bdd\s+if=\b',
    r'\bmkfs\b',
    r'\bdel\s+/f\s+/s\b',
    r'\bformat\s+[cC]:\b',
    r'\bgit\s+reset\s+--hard\b',
    r'\bgit\s+clean\s+-fd\b',
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

`asef/tools.py` — `class ToolExecutor._check_destructive()` — appliqué AVANT toute exécution.
Ce filtre ne peut pas être contourné par un prompt ou une instruction agent.
