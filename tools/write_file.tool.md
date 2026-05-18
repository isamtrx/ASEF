# tool: write_file

**id**: write_file
**level**: WRITE_WORKSPACE
**implementation**: asef/tools.py

## Description

Écrire ou modifier un fichier dans le workspace.
Filtré par PROTECTED_FILES et règles de path.

## Input

```json
{"tool": "write_file", "path": "<chemin relatif>", "content": "<string>", "mode": "write|append"}
```

## Output

```json
{"success": true, "path": "<string>", "bytes_written": "<integer>"}
```

## Contraintes

- Ne peut pas écrire dans PROTECTED_FILES (AGENTS.md, SCOPE.md, PROJECT.md, docs/security/SECURITY.md)
- Ne peut pas écrire hors du workspace
- Content scanné pour patterns secrets avant écriture
- Chaque agent a un sous-ensemble de paths autorisés (défini dans son contrat)

## PROTECTED_FILES

Définis dans `asef/tools.py` — constante `PROTECTED_FILES` :
```python
PROTECTED_FILES = {
    "AGENTS.md", "SCOPE.md", "PROJECT.md", "docs/security/SECURITY.md"
}
```

## Erreur si path protégé

```json
{"success": false, "error": "PROTECTED_FILE", "path": "<string>"}
```

## Validation

Tentative d'écriture sur PROTECTED_FILES → erreur + log + escalade
