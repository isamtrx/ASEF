# missions/blocked — Missions bloquées

Ce répertoire contient les missions **bloquées sur un gate FAIL ou en attente HITL**.

## Quand déplacer une mission ici

- Un gate G0-G9 est FAIL sans résolution dans le cycle courant.
- Un trigger HITL-OBLIGATOIRE est actif et l'humain n'a pas encore répondu.
- Une dépendance externe non résolue empêche toute progression.
- Un risque CRITICAL (score 9) non mitigé bloque l'exécution.

## Format d'un fichier de mission bloquée

Ajouter en tête du fichier de mission :

```markdown
---
**Bloquée le** : YYYY-MM-DD
**Raison du blocage** : [Gate X FAIL — raison précise]
**Gate bloquant** : G[X]
**HITL actif** : [HITL-XX / Non]
**Actions nécessaires pour débloquer** :
1. [Action 1]
2. [Action 2]
**Responsable du déblocage** : [Agent ou humain]
**Deadline de révision** : YYYY-MM-DD
---
```

## Règles
- Revoir les missions bloquées en début de chaque session.
- Déplacer vers `active/` dès que le blocage est levé.
- Déplacer vers `archived/` si la mission est abandonnée (avec justification).
- Une mission bloquée > 30 jours sans action = escalade humaine obligatoire.
