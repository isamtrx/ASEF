---
applyTo: "**/*.md"
---

# Instructions Documentation — ASEF

> S'applique à : tous les fichiers Markdown du dépôt  
> Lire d'abord : AGENTS.md → SCOPE.md → Règles de non-redondance (section 10 du framework)

## Principe absolu

**1 fichier = 1 responsabilité = 1 source de vérité.**  
Avant de créer un fichier, vérifier qu'aucun fichier existant ne couvre déjà cette responsabilité.

## Avant de modifier un fichier de documentation

1. Identifier sa responsabilité unique (voir matrice dans README.md)
2. Vérifier que le contenu appartient bien à ce fichier
3. Identifier les fichiers à mettre à jour par cascade (ex: CHANGELOG.md après tout livrable)

## Règles de contenu

- **Pas de duplication.** Référencer par lien, pas par copie-colle.
- **Pas de documentation décorative.** Chaque paragraphe doit servir un des 10 objectifs ASEF.
- **Pas de contenu marketing.** Opérationnel, direct, exigeant.
- **Seuil de taille.** Un fichier > 400 lignes doit être divisé ou justifié.
- **Présent actif.** Écrire "doit contenir", "ne doit pas contenir" — pas "pourrait", "peut".

## Structure obligatoire pour les fichiers ASEF

```markdown
# [NOM DU FICHIER] — ASEF

> Ligne de responsabilité unique.  
> Dépend de : [fichiers lus avant]  
> Ne doit jamais contenir : [liste explicite]

---

[Contenu]
```

## Règles CHANGELOG.md

- Format : Keep a Changelog
- Sections : Added | Changed | Fixed | Removed | Security | Deprecated
- **Ne jamais modifier une version déjà publiée**
- Chaque entrée doit référencer un commit ou une PR si disponible

## Règles DECISIONS.md

- Format ADR minimal obligatoire (voir template dans `docs/adr/ADR-0001-template.md`)
- Écrire la décision **avant** de l'implémenter
- Statut : Proposé → Validé → Obsolète | Remplacé

## Règles MEMORY.md

- État **actuel** uniquement — pas d'historique
- Seuil : 200 lignes maximum
- Purge mensuelle obligatoire (déplacer l'obsolète vers CHANGELOG ou supprimer)

## Contrôles avant livraison

```
□ Aucun contenu dupliqué avec un autre fichier
□ Aucun lien cassé
□ Toutes les références croisées sont valides
□ CHANGELOG.md mis à jour si changement livrable
□ SESSION_LOG.md entrée ajoutée
```

## Erreurs communes à éviter

- Copier-coller une section de AGENTS.md dans CLAUDE.md (→ référencer)
- Ajouter des règles agents dans README.md
- Transformer MEMORY.md en changelog
- Créer un fichier "NOTES.md" fourre-tout
- Mettre du contenu d'architecture dans PROJECT.md
