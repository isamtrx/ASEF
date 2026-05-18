# skill: code_review

**id**: code_review
**version**: 1.0.0
**agents**: developer, qa
**tools_required**: read_file, list_directory

## Purpose

Effectuer une revue de code chirurgicale sur les fichiers modifiés.
Identifier les problèmes sans modifier le code (rôle lecture seule pour QA).

## When to Use

- Avant de commencer une implémentation (developer : comprendre le contexte)
- Après une implémentation (qa : vérifier la conformité)
- task_type = `review`

## Steps (developer, avant implémentation)

1. Lire le fichier entier avant de modifier quoi que ce soit
2. Identifier les patterns existants (nommage, indentation, structure)
3. Identifier les dépendances (imports, fonctions appelées)
4. Lister les fichiers impactés par la modification prévue
5. Valider que la modification demandée est dans le DoD

## Steps (qa, après implémentation)

1. Lister les fichiers modifiés
2. Pour chaque fichier modifié :
   a. Vérifier que le style correspond au reste du fichier
   b. Vérifier qu'aucune feature non demandée n'a été ajoutée
   c. Vérifier qu'aucun secret n'est présent (patterns: api_key, token, password)
   d. Vérifier que chaque ligne modifiée trace vers la demande
3. Produire un résumé des observations

## Checklist par fichier

```
[ ] Fichier lu entièrement avant toute suggestion
[ ] Nommage conforme au style existant
[ ] Pas de feature ajoutée hors DoD
[ ] Pas de refactoring non demandé
[ ] Pas de secret ou valeur sensible
[ ] Chaque ligne modifiée traceable vers la demande
[ ] Tests écrits pour chaque modification
```

## Edge Cases

- Fichier binaire → passer
- Fichier protégé → lire uniquement, signaler si une modification est proposée
- Import de module externe nouveau → signaler comme décision structurante potentielle

## Output

Résumé textuel des observations. Pas de modification de code dans ce skill.
