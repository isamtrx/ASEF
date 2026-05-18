# missions/active — Missions en cours

Ce répertoire contient les fichiers de mission **actuellement actives**.

Une mission est active si elle est en cours d'exécution ou planifiée pour exécution imminente.

## Convention de nommage
```
YYYY-MM-DD_[slug-mission].md
```
Exemple : `2026-05-18_migration-asef-runtime.md`

## Format d'un fichier de mission

```markdown
# Mission : [Titre]

**Date de création** : YYYY-MM-DD
**Statut** : ACTIVE | PLANIFIÉE
**Priorité** : CRITICAL | HIGH | MEDIUM | LOW

## Objectif
[Ce que la mission doit accomplir — ≤ 3 lignes]

## DoD (Definition of Done)
1. [Critère 1]
2. [Critère 2]
...
≤ 8 lignes max

## Périmètre
**IN** : [Ce qui est dans la mission]
**OUT** : [Ce qui est hors de la mission]

## Plan d'exécution
- [ ] Step 1 — [Description]
- [ ] Step 2 — [Description]
...

## Preuves attendues
- [Type de preuve 1]
- [Type de preuve 2]

## Gates requis
- [ ] G0 — Intake
- [ ] G1 — Scope
...

## Validation humaine requise
[Oui — HITL-XX / Non]

## Dépendances
[Missions ou décisions dont cette mission dépend]
```

## Règles
- Déplacer vers `completed/` dès que le DoD est satisfait et les preuves produites.
- Déplacer vers `blocked/` si un gate bloquant est FAIL sans résolution immédiate.
- Déplacer vers `archived/` si la mission est annulée (avec justification).
- Ne jamais garder une mission terminée dans `active/`.
