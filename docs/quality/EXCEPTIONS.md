# EXCEPTIONS.md — ASEF

> Registre des écarts aux quality gates acceptés.  
> 1 responsabilité : tracer les dérogations, leur justification et leur expiration.  
> Dépend de : QUALITY_GATES.md  
> Principe : une exception non documentée = une violation. Pas d'exception silencieuse.

---

## Format d'une exception

```markdown
## EXC-XXXX — [Titre court]

| Champ | Valeur |
|-------|--------|
| Gate contourné | G[N] — [Nom] |
| Demandeur | [Nom / Rôle] |
| Valideur | [Nom / Rôle — doit être humain] |
| Date d'émission | YYYY-MM-DD |
| Date d'expiration | YYYY-MM-DD |
| Statut | Actif / Expiré / Clôturé |

**Motif :**
[Pourquoi ce gate ne peut pas être satisfait maintenant]

**Risque accepté :**
[Description précise du risque assumé]

**Plan de retour à la norme :**
[Actions et date cible pour supprimer l'exception]

**Référence :**
[PR / ticket / commit associé]
```

---

## Registre des exceptions actives

_(Aucune exception active — initialisation MVP)_

---

## Registre des exceptions clôturées

_(Aucune exception clôturée — initialisation MVP)_

---

## Règles d'émission d'une exception

1. Une exception ne peut être émise que par un **humain** (Tech Lead ou CTO) — jamais par un agent seul.
2. Chaque exception a une **date d'expiration obligatoire** (maximum 30 jours, renouvelable une fois avec justification).
3. Une exception expirée = le gate redevient bloquant immédiatement.
4. Une même exception ne peut pas être renouvelée plus de deux fois — à ce stade, ouvrir un ADR.
5. Les exceptions sur G5 (sécurité) ont une durée maximale de 7 jours.
6. Aucune exception permanente n'est acceptée.

---

## Revue mensuelle des exceptions

Le Tech Lead révise ce fichier chaque mois :
- Clôturer les exceptions dont le plan de retour est complété
- Escalader les exceptions sur le point d'expirer sans plan viable
- Identifier les exceptions répétées (signal d'une dette structurelle → ADR)
