# ADR-0005 — Stratégie de branches : trunk-based + feature branches

Date : 2026-05-15  
Statut : Validé  
Auteur : Platform Engineering

---

## Contexte

ASEF doit définir une stratégie de branches Git claire pour :
- Protéger la branche `main` des modifications directes non validées
- Permettre des contributions parallèles sans conflits excessifs
- Aligner avec le pipeline CI/CD (ADR-0002) et les quality gates (G4, G5)

Le repo est actuellement docs-only (pas de code livrable), mais la stratégie doit tenir pour la Phase 1 (code réel).

---

## Options considérées

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **Trunk-based + feature branches courtes** | Simple, CI rapide, merge fréquents | Discipline requise (branches courtes) |
| GitFlow | Isolation forte des releases | Overhead branches, merge complexes |
| Forking workflow | Sécurité maximale | Overhead pour équipe interne |

---

## Décision

**Trunk-based development** avec feature branches de courte durée (≤ 5 jours) et `main` comme branche protégée.

---

## Règles découlant de cette décision

1. `main` est protégée — push direct interdit (AGENTS.md §4)
2. Toute modification passe par une PR depuis une branche feature
3. Nommage : `feat/`, `fix/`, `docs/`, `chore/` + description courte
4. Une PR = un sujet cohérent — pas de commits fourre-tout
5. Merge uniquement si CI vert (G3-G5) et approbation humaine
6. Les branches feature sont supprimées après merge
7. Tags de release sur `main` : format `v{MAJOR}.{MINOR}.{PATCH}`

---

## Raison

- Trunk-based réduit les risques de long-lived branches (diffs massifs, conflits)
- Cohérent avec le CI continu (ADR-0002) — chaque PR déclenche la suite complète de gates
- Adapté à une petite équipe avec revue humaine systématique (Gate G7)

---

## Conséquences

**Positives :**
- Intégration continue réelle (pas juste "continuous"  en nom)
- Historique Git propre et traçable

**Négatives :**
- Discipline requise sur la taille des branches (risque de PRs trop grosses)

---

## Réversibilité

Réversible — migration vers GitFlow possible sans impact applicatif.

---

## Fichiers concernés

- `docs/delivery/BRANCHING.md` — règles détaillées
- `docs/delivery/CI_CD.md` — triggers CI par branche
- `docs/delivery/RELEASE_MANAGEMENT.md` — processus de release
