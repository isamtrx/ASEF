# POSTMORTEMS.md — ASEF

> Registre des postmortems d'incidents.  
> 1 responsabilité : documenter chaque incident significatif avec sa chronologie et ses actions correctives.  
> Dépend de : INCIDENT_RESPONSE.md  
> Ne doit jamais contenir : leçons générales (→ LESSONS_LEARNED.md), procédures d'incident (→ INCIDENT_RESPONSE.md).

---

## Format d'un postmortem

```markdown
## PM-XXX — [Titre de l'incident]

| Champ | Valeur |
|-------|--------|
| Date incident | YYYY-MM-DD |
| Date postmortem | YYYY-MM-DD |
| Durée | HH:MM |
| Sévérité | P1 / P2 / P3 |
| Systèmes impactés | [liste] |
| Utilisateurs impactés | [nombre ou description] |
| Auteur du postmortem | [Nom] |
| Statut | Ouvert / Actions en cours / Clôturé |

### Résumé exécutif
[2-3 phrases maximum]

### Timeline
| Heure | Événement |
|-------|---------|
| HH:MM | [Événement] |

### Cause racine
[Description précise de la cause racine — pas de symptôme]

### Facteurs contributifs
- [Facteur 1]
- [Facteur 2]

### Ce qui a bien fonctionné
- [Point positif]

### Ce qui a mal fonctionné
- [Point négatif]

### Actions correctives

| ID | Action | Responsable | Délai | Status |
|----|--------|------------|-------|--------|
| PM-XXX-A01 | [Action] | [Nom] | YYYY-MM-DD | À faire |

### Leçon produite
[Référence LL-XXX dans LESSONS_LEARNED.md]
```

---

## Registre des postmortems

| ID | Date | Sévérité | Résumé | Status |
|----|------|---------|--------|--------|
| — | — | — | _(aucun incident à date — ASEF v0.1.0)_ | — |

---

## Règles de postmortem ASEF

### Obligatoire pour

- Tout incident P1 ou P2
- Tout incident impliquant un comportement inattendu d'un agent IA
- Tout incident ayant causé une perte ou corruption de données
- Tout déploiement raté nécessitant un rollback

### Délai

- P1 : postmortem dans les 24h
- P2 : postmortem dans les 48h
- P3 : postmortem dans la semaine si impact visible

### Principes

- **Blameless** : l'objectif est de comprendre les systèmes, pas de blâmer les personnes
- **Cause racine vs symptômes** : continuer à demander "pourquoi" jusqu'à la cause structurelle
- **Actions concrètes** : chaque postmortem produit ≥ 1 action corrective avec un responsable et une date

### Anti-patterns à éviter

- "Erreur humaine" comme cause racine — toujours aller plus loin
- Actions vagues ("améliorer la surveillance") sans responsable ni date
- Postmortem non publié à l'équipe
- Leçon non ajoutée dans LESSONS_LEARNED.md
