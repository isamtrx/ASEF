# ADR-0006 — Modèle de distribution : framework template open-source

Date : 2026-05-15  
Statut : Validé  
Auteur : Platform Engineering

---

## Contexte

ASEF doit clarifier son modèle de distribution et d'usage. Deux directions sont possibles :

1. **Framework template** — un dépôt GitHub que les équipes copient/forkent pour leurs projets
2. **Framework opérationnel** — une plateforme SaaS ou un outil CLI déployé par une organisation centrale

Cette clarification est nécessaire car plusieurs décisions techniques (adresses des fichiers, références `[org]/[repo]`, absence de code exécutable) dépendent du modèle retenu.

---

## Options considérées

| Option | Description | Avantages | Inconvénients |
|--------|-------------|-----------|---------------|
| **Template GitHub (fork)** | Les équipes forkent ASEF et adaptent | Simple, zéro infra, auto-suffisant | Divergence entre forks |
| Template GitHub (Use this template) | Repo GitHub "template" officiel | Propre, pas de lien avec l'upstream | Pas de mises à jour automatiques |
| CLI outil | `npx asef init` qui génère les fichiers | DX moderne | Complexité de maintenance CLI |
| SaaS ASEF | Plateforme hébergée | Monétisable | Hors scope défini dans SCOPE.md |

---

## Décision

**Framework template open-source** — dépôt GitHub marqué comme "Template repository" que les équipes utilisent pour créer leur propre dépôt de gouvernance. Distribué sous licence permissive.

---

## Raison

- Cohérent avec `SCOPE.md §Hors périmètre` : pas de SaaS, pas de plugin IDE custom
- Zéro infrastructure à maintenir pour la distribution
- Les équipes adaptent les fichiers à leur contexte sans dépendance à un service central
- Un CLI ou une plateforme peut être ajouté en Phase 3 sans invalider cette décision

---

## Implications

1. Le dépôt ASEF est marqué "Template repository" sur GitHub
2. Toutes les références `[org]/[repo]` dans les fichiers sont des placeholders à remplacer par l'équipe adoptante
3. `QUICKSTART.md` guide l'onboarding
4. Les mises à jour ASEF sont documentées dans `CHANGELOG.md` — les équipes ayant forké décident elles-mêmes d'incorporer les mises à jour
5. Pas de version "runtime" — tout est documentation et configuration

---

## Conséquences

**Positives :**
- Adoption sans friction (pas de compte, pas d'installation)
- Les équipes ont le contrôle total de leur instance

**Négatives :**
- Pas de mécanisme de mise à jour automatique pour les adoptants
- Pas de métriques d'adoption centralisées

---

## Réversibilité

Réversible — un CLI ou une plateforme peut être ajouté ultérieurement sans invalider les fichiers de gouvernance existants.

---

## Fichiers concernés

- `SCOPE.md` — périmètre (SaaS hors scope confirmé)
- `README.md` — instructions d'adoption
- `QUICKSTART.md` — guide de démarrage
- `ROADMAP.md` — phases d'évolution
