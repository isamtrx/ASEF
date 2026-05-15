# CI_CD.md — ASEF

> Source de vérité des pipelines CI/CD.  
> 1 responsabilité : définir les jobs, les déclencheurs et les règles de blocage.  
> Dépend de : BRANCHING.md, QUALITY_GATES.md  
> Ne doit jamais contenir : procédures de déploiement (→ DEPLOYMENT.md).

---

## Pipelines définis

### Pipeline PR — `ci.yml`

**Déclencheur :** Toute PR ouverte ou mise à jour vers main  
**Résultat attendu :** Tous les jobs verts pour que le merge soit autorisé

```yaml
name: CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    name: Lint & Type Check (G3)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[SHA]
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  test:
    name: Tests (G4)
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@[SHA]
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@[SHA]
        with:
          name: coverage
          path: coverage/

  security:
    name: Sécurité (G5)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[SHA]
      - run: npm ci
      - run: npm audit --audit-level=high
      - name: SAST Semgrep
        uses: semgrep/semgrep-action@[SHA]
        with:
          config: auto
      - name: Secret Scan
        uses: gitleaks/gitleaks-action@[SHA]
```

---

### Pipeline Release — `release.yml`

**Déclencheur :** Push d'un tag `v*.*.*` sur main  
**Résultat attendu :** Release créée avec evidence package

```yaml
name: Release

on:
  push:
    tags: ['v*.*.*']

permissions:
  contents: write
  packages: write

jobs:
  validate:
    name: Validation complète G0-G6
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[SHA]
      - run: npm ci && npm run lint && npm test && npm audit --audit-level=high

  build:
    name: Build artifact
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[SHA]
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@[SHA]
        with:
          name: build
          path: dist/

  release:
    name: Créer la release GitHub
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[SHA]
      - uses: softprops/action-gh-release@[SHA]
        with:
          generate_release_notes: false
          body_path: RELEASE_NOTES.md
```

---

## Jobs obligatoires (bloquants)

| Job | Gate | Bloquant merge | Bloquant release |
|-----|------|---------------|-----------------|
| lint | G3 | ✓ | ✓ |
| typecheck | G3 | ✓ | ✓ |
| test | G4 | ✓ | ✓ |
| coverage | G4 | ✓ (< 80%) | ✓ |
| security-audit | G5 | ✓ | ✓ |
| sast | G5 | ✓ | ✓ |
| secret-scan | G5 | ✓ | ✓ |

---

## Artifacts CI

Chaque pipeline conserve les artifacts suivants :

| Artifact | Durée de conservation | Quand |
|---------|----------------------|-------|
| coverage/ | 30 jours | Chaque CI |
| reports/sast.json | 1 an | Chaque CI |
| reports/audit.json | 1 an | Chaque CI |
| dist/ | 90 jours | Release uniquement |
| reports/evals/ | 1 an | Si changement prompt |

---

## Environnements CI

| Environnement | Déclencheur | Secrets disponibles |
|-------------|------------|-------------------|
| test | Chaque PR | Aucun (tests seulement) |
| staging | Merge sur main | Credentials staging |
| production | Tag de release + Gate 7 | Credentials production |

---

## Règles de sécurité des pipelines

- Secrets injectés uniquement dans les jobs qui en ont besoin (pas de secrets globaux)
- Pinning par SHA sur toutes les actions tierces
- Pas d'`actions: write` en dehors des jobs de release
- Les outputs de build sont signés avec une clé attestée (GitHub artifact attestations)
- Les logs CI ne doivent jamais afficher de secrets (vérifier `::add-mask::`)
