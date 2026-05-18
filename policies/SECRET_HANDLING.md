# POLICY: SECRET HANDLING

**Source** : AGENTS.md §4 INTERDIT #1 + §7 Règle 5
**Statut** : active
**ID** : POL-SECRET-001

## Règles

1. **Aucun secret dans aucun fichier du workspace** — clé API, token, mot de passe, credential
2. **Aucun secret dans les tests** — utiliser des variables d'environnement ou des mocks
3. **Aucun secret dans les artifacts** — rapports, logs, evidence packages
4. **Aucun secret dans la mémoire** — MEMORY.md, JSONL, SESSION_LOG.md
5. **Variables d'environnement uniquement** — `os.environ.get("API_KEY")`
6. **Rotation immédiate si exposé** — escalade CRITIQUE + notification humaine

## Patterns de détection (Gate G5)

```python
SECRET_PATTERNS = [
    r'api[_-]?key\s*=\s*[\'\"]\w{20,}',
    r'(?:password|passwd|pwd)\s*=\s*[\'\"][^\s\'\"]{8,}',
    r'(?:secret|token)\s*=\s*[\'\"]\w{20,}',
    r'sk-[a-zA-Z0-9]{48}',    # OpenAI
    r'ghp_[a-zA-Z0-9]{36}',   # GitHub PAT
    r'AKIA[A-Z0-9]{16}',       # AWS Access Key
    r'anthropic[_-]api[_-]key',
]
```

## Procédure si secret détecté

1. Ne pas committer
2. Escalade CRITIQUE immédiate avec `escalate(urgency="CRITIQUE")`
3. Identifier l'origine (qui a ajouté, quand)
4. Révoquer/rotation du secret exposé
5. Écrire dans LESSONS_LEARNED.md

## Application

Gate G5 — `asef/gates.py` — secret scan gitleaks + fallback regex.
