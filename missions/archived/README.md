# missions/archived — Missions archivées

Ce répertoire contient les missions **annulées, obsolètes ou remplacées**.

## Quand archiver une mission

- La mission a été annulée par décision humaine.
- La mission a été remplacée par une autre mission.
- Le périmètre a changé et la mission n'est plus applicable.
- La mission était un doublon identifié a posteriori.

## Format d'une mission archivée

Ajouter en tête du fichier de mission :

```markdown
---
**Archivée le** : YYYY-MM-DD
**Raison d'archivage** : ANNULÉE | REMPLACÉE | OBSOLÈTE | DOUBLON
**Décision de référence** : [Référence dans DECISIONS.md — date + titre]
**Remplacée par** : [Slug de la mission remplaçante — si applicable]
**Contexte** : [1-2 lignes expliquant pourquoi]
---
```

## Règles
- Les missions archivées sont en lecture seule.
- Jamais supprimer une mission archivée (traçabilité).
- L'archivage nécessite une justification documentée.
- Toute archive de mission CRITICAL nécessite une validation humaine.
