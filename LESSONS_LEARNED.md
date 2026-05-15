# LESSONS_LEARNED.md — ASEF

> Registre des leçons apprises.  
> 1 responsabilité : capitaliser les erreurs et les succès pour améliorer le framework.  
> Dépend de : SESSION_LOG.md, POSTMORTEMS.md  
> Ne doit jamais contenir : décisions structurantes (→ DECISIONS.md), postmortems complets (→ POSTMORTEMS.md).

---

## Format

```markdown
## LL-XXX — [Titre court]

| Champ | Valeur |
|-------|--------|
| Date | YYYY-MM-DD |
| Source | Session / Incident / Audit / Retour équipe |
| Contexte | Bref résumé de la situation |
| Erreur observée | Ce qui s'est passé |
| Cause racine | Pourquoi c'est arrivé |
| Correction appliquée | Ce qui a été fait |
| Règle produite | Nouvelle règle ou directive |
| Impact | Ce que ça évite à l'avenir |
| Fichier modifié | Fichier de gouvernance mis à jour |
```

---

## LL-001 — 1-fichier-1-responsabilité comme règle de conception

| Champ | Valeur |
|-------|--------|
| Date | 2026-05-15 |
| Source | Session de conception ASEF |
| Contexte | Architecture documentaire initiale pour ASEF |
| Erreur observée | Tendance à fusionner governance et opérations dans un seul fichier |
| Cause racine | Pas de règle explicite → chaque fichier grossit par accumulation |
| Correction appliquée | ADR-0002 — 1 fichier = 1 responsabilité, avec table de correspondance objectif/fichier |
| Règle produite | Chaque fichier a un en-tête "1 responsabilité :" et "Ne doit jamais contenir :" |
| Impact | Maintien de la cohérence sur 55 fichiers, pas de duplication détectée |
| Fichier modifié | DECISIONS.md (ADR-0002), tous les en-têtes de fichiers |

---

## LL-002 — Les agents ne doivent pas modifier les fichiers de gouvernance

| Champ | Valeur |
|-------|--------|
| Date | 2026-05-15 |
| Source | Conception AGENTS.md |
| Contexte | Définition des permissions agent |
| Erreur observée | Risque de boucle : un agent modifie ses propres règles |
| Cause racine | Pas de protection explicite des fichiers de gouvernance |
| Correction appliquée | Liste des fichiers protégés dans AGENTS.md + TOOL_REGISTRY.md |
| Règle produite | AGENTS.md, SCOPE.md, DECISIONS.md = lecture seule pour les agents |
| Impact | Gouvernance stable, évite la dérive auto-référentielle |
| Fichier modifié | AGENTS.md §Permissions, TOOL_REGISTRY.md §Outils interdits |

---

## LL-003 — Gate 7 obligatoire pour les releases MAJOR/MINOR

| Champ | Valeur |
|-------|--------|
| Date | 2026-05-15 |
| Source | Conception QUALITY_GATES.md |
| Contexte | Définition des gates de qualité |
| Erreur observée | Dans d'autres projets, des releases significatives sont déployées sans validation humaine explicite |
| Cause racine | CI automatique donne une fausse impression de validation suffisante |
| Correction appliquée | Gate G7 formalisé : validation humaine obligatoire pour vMAJOR.MINOR.0 |
| Règle produite | RELEASE_MANAGEMENT.md §Gate 7, QUALITY_GATES.md §G7 |
| Impact | Toute release significative a une signature humaine traçable |
| Fichier modifié | QUALITY_GATES.md, RELEASE_MANAGEMENT.md |

---

## LL-004 — Les prompts sont des artefacts logiciels

| Champ | Valeur |
|-------|--------|
| Date | 2026-05-15 |
| Source | Conception PROMPT_GOVERNANCE.md |
| Contexte | Gouvernance de la génération de code par IA |
| Erreur observée | Prompts improvisés → comportement agent non reproductible |
| Cause racine | Pas de standard de versionnement des prompts |
| Correction appliquée | PROMPT_GOVERNANCE.md avec semver + template + registre |
| Règle produite | Un prompt = un ID + une version + un jeu d'evals associé |
| Impact | Régressions de prompt détectées automatiquement en CI |
| Fichier modifié | PROMPT_GOVERNANCE.md, EVALS.md |

---

## Règles d'ajout

1. Une leçon est ajoutée après chaque incident, postmortem ou session révélant un pattern nouveau
2. Les leçons ne sont jamais supprimées — seulement marquées `deprecated` si invalidées
3. Chaque leçon produit une règle concrète dans au moins un fichier de gouvernance
4. Le registre est relu en début de chaque session pour éviter de répéter les erreurs
