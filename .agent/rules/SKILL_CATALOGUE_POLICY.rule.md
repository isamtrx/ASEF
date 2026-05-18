# SKILL_CATALOGUE_POLICY.rule.md — ASEF

> Politique de gestion du catalogue de skills.  
> Sans cette politique, les skills s'accumulent sans structure → introuvables → inutilisés.

---

## Structure obligatoire

```
skills/
├── SKILLS.md              → index central (toujours à jour)
├── *.skill.md             → skills actifs
└── archived/              → skills dépréciés (ne pas supprimer, archiver)
```

---

## Format d'un skill

Chaque fichier `*.skill.md` doit contenir :

```markdown
# [NOM_DU_SKILL] — ASEF Skill

## Purpose
[1 phrase : ce que ce skill fait]

## Trigger
[Quand l'invoquer — signal ou condition]

## Input
[Ce qu'il reçoit]

## Steps
[Étapes numérotées]

## Output
[Ce qu'il produit]

## Evidence required
[Preuve que le skill a été exécuté correctement]
```

---

## Règles d'ajout

1. Avant d'ajouter un skill → vérifier dans `SKILLS.md` qu'il n'existe pas déjà
2. Nom en `snake_case` : `code_review.skill.md`, `security_review.skill.md`
3. Ajouter une ligne dans `SKILLS.md` immédiatement après création
4. Un skill = une responsabilité. Pas de skills "fourre-tout"

---

## Règles de dépréciation

1. Ne jamais supprimer un skill — archiver dans `skills/archived/`
2. Mettre le statut `Déprécié` dans `SKILLS.md`
3. Indiquer le skill de remplacement si applicable

---

## Règles d'utilisation

1. Avant d'improviser une procédure → vérifier si un skill couvre le cas
2. Après avoir improvisé avec succès → créer un skill pour la prochaine fois
3. L'orchestrator peut lire les skills. L'exécution appartient à l'agent désigné.

---

## SKILLS.md — format de ligne d'index

```markdown
| Nom | Fichier | Statut | Rôle owner | Déclencheur |
|-----|---------|--------|-----------|------------|
| code_review | code_review.skill.md | Actif | reviewer | PR soumise |
```

---

_Version : 1.0.0 — 2026-05-18_
