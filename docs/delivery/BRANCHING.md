# BRANCHING.md — ASEF

> Source de vérité de la stratégie de branches Git.  
> 1 responsabilité : définir le modèle de branches, les règles de merge et les protections.  
> Dépend de : ENGINEERING_HANDBOOK.md  
> Ne doit jamais contenir : règles de déploiement (→ DEPLOYMENT.md), pipelines CI (→ CI_CD.md).

---

## Modèle de branches

ASEF utilise un modèle **trunk-based development simplifié** pour les projets MVP, avec la possibilité d'évoluer vers GitFlow pour les projets enterprise.

```
main                    ← branche de production (protégée)
  └── feat/TICKET-xxx   ← feature branches (courte durée)
  └── fix/TICKET-xxx    ← bug fix branches
  └── hotfix/TICKET-xxx ← corrections urgentes
  └── chore/titre       ← tâches techniques
  └── docs/titre        ← documentation seule
  └── release/v1.x.x    ← (Enterprise) branche de release
```

---

## Règles des branches

### main

- **Protégée** — pas de push direct, pas de force push
- Toujours déployable en production
- Chaque commit doit passer G3 + G4 + G5 en CI
- Merge uniquement via PR approuvée
- Historique linéaire maintenu (squash or rebase merge)

### Branches de feature / fix

- Durée maximale : 3 jours (au-delà → risque de divergence, diviser en sous-tâches)
- Naming : `feat/TICKET-123-titre-court` ou `fix/TICKET-123-titre-court`
- Créée depuis main, rebased sur main avant PR
- Supprimée après merge

### Branches de hotfix

- Créée depuis main (version en production)
- Correctif minimal — pas d'autres changements
- Merge vers main + tag de patch version
- Naming : `hotfix/TICKET-123-description-urgente`

### Branches de release (Enterprise)

- Créée depuis main au moment du gel de code (feature freeze)
- Seuls les bugfixes critiques y sont mergés
- Naming : `release/v1.2.0`
- Tag de version sur le commit de release

---

## Protection de la branche main

Configuration GitHub à appliquer :

```yaml
protection:
  required_status_checks:
    strict: true
    contexts:
      - lint
      - test
      - sast
      - dependency-audit
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  restrictions:
    push: []  # Personne ne peut pusher directement
  enforce_admins: true
  allow_force_pushes: false
  allow_deletions: false
```

---

## Workflow quotidien recommandé

```bash
# Créer une branche depuis main à jour
git checkout main
git pull origin main
git checkout -b feat/TICKET-123-ma-feature

# Travailler et committer régulièrement
git add -p
git commit -m "feat(scope): description courte"

# Rebaser avant d'ouvrir une PR
git fetch origin
git rebase origin/main

# Vérifier avant push
npm run lint && npm test

# Ouvrir la PR
git push origin feat/TICKET-123-ma-feature
# Puis ouvrir la PR sur GitHub
```

---

## Résolution des conflits

- Les conflits sont résolus par l'auteur de la branche, pas le reviewer
- En cas de conflit complexe, impliquer le Tech Lead
- Pas de merge commit sur main — utiliser rebase ou squash

---

## Tags de version

Format : `vMAJOR.MINOR.PATCH` (semver)

```bash
# Taguer une release
git tag -a v1.2.0 -m "Release v1.2.0 — voir CHANGELOG.md"
git push origin v1.2.0
```

Les tags sont créés sur le commit de release après Gate 7 validé.
