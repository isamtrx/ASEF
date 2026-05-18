# tool: read_file

**id**: read_file
**level**: READ_ONLY
**implementation**: asef/tools.py

## Description

Lire le contenu d'un fichier. Aucun effet de bord.

## Input

```json
{"tool": "read_file", "path": "<chemin relatif ou absolu>"}
```

## Output

```json
{"content": "<string>", "path": "<string>", "size_bytes": "<integer>"}
```

## Contraintes

- Lecture seule
- Tous les agents y ont accès
- Ne peut pas lire des fichiers hors du workspace ASEF
- Binaires retournés comme base64 (usage déconseillé)

## Validation

`python execution/validate_tools.py` → vérifie que read_file est dans tools.registry.json
