# missions/completed — Missions terminées

Ce répertoire contient les missions dont le **DoD a été satisfait** et les **preuves produites**.

## Convention de nommage
```
YYYY-MM-DD_[slug-mission].md
```

## Archivage d'une mission terminée

Avant de déplacer une mission de `active/` vers `completed/`, ajouter en tête du fichier :

```markdown
---
**Terminée le** : YYYY-MM-DD
**Evidence package** : docs/evidence/YYYY-MM-DD_[slug]/
**Gates franchis** : G0, G1, G2, G3, G4, G5, G6, G7, G8, G9
**Validation humaine** : [Oui — par [identité] / Non]
**Résumé de complétion** : [1-2 lignes]
---
```

## Règles
- Les missions `completed/` sont en lecture seule.
- Jamais supprimer une mission terminée (traçabilité).
- Référencer l'evidence package exact dans la mission.
