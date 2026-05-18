# TOOL: list_directory

**ID** : list_directory
**Access Level** : READ_ONLY
**Version** : 1.0.0
**Implementation** : Native filesystem listing
**Agents** : orchestrator, architect, developer, qa, security, docs (tous)

## Description

Liste le contenu d'un répertoire. Aucun effet de bord. Ne crée, modifie, ni supprime aucun fichier.

## Input Contract

```json
{
  "path": "string — chemin relatif ou absolu du répertoire",
  "recursive": "boolean — lister récursivement (défaut: false)",
  "pattern": "string — glob filter optionnel (ex: '*.md', '*.py')"
}
```

## Output Contract

```json
{
  "path": "string — chemin listé",
  "entries": [
    {
      "name": "string — nom du fichier ou dossier",
      "type": "file | directory",
      "size_bytes": "integer (si fichier)",
      "modified_at": "ISO 8601 (optionnel)"
    }
  ],
  "count": "integer — nombre total d'entrées"
}
```

## Exemple

**Input:**
```json
{"path": "registry/", "pattern": "*.json"}
```

**Output:**
```json
{
  "path": "registry/",
  "entries": [
    {"name": "agents.registry.json", "type": "file", "size_bytes": 1842},
    {"name": "gates.registry.json", "type": "file", "size_bytes": 1203}
  ],
  "count": 2
}
```

## Restrictions

- Ne peut pas lister en dehors du workspace projet
- Chemins traversaux (`../`) bloqués
