# EVIDENCE.md — ASEF

> Source de vérité des preuves acceptées.  
> 1 responsabilité : définir ce qu'est une preuve valide pour chaque type de changement.  
> Dépend de : QUALITY_GATES.md, QA.md  
> Ne doit jamais contenir : procédures de test, règles de sécurité.

---

## Principe

Une preuve est valide si et seulement si elle est :
1. **Vérifiable** — un auditeur externe peut la reproduire
2. **Horodatée** — liée à un commit, une PR ou un pipeline CI
3. **Complète** — couvre le périmètre du changement
4. **Non altérable** — archivée en CI ou signée

---

## Types de preuves

### Logs de tests

| Type | Format accepté | Outil | Conservation |
|------|---------------|-------|-------------|
| Tests unitaires | JUnit XML, rapport HTML | Jest, pytest | Artifact CI, 90 jours |
| Tests intégration | JUnit XML | Jest + Supertest | Artifact CI, 90 jours |
| Tests E2E | Rapport HTML Playwright + traces | Playwright | Artifact CI, 30 jours |
| Coverage | HTML + JSON (lcov) | Istanbul, coverage.py | Artifact CI, 90 jours |

### Rapports sécurité

| Type | Format accepté | Outil | Conservation |
|------|---------------|-------|-------------|
| SAST | JSON (Semgrep, CodeQL) | Semgrep | Artifact CI, 1 an |
| Dependency audit | JSON (npm audit, pip-audit) | npm, pip-audit | Artifact CI, 1 an |
| Secret scan | Log texte (propre = 0 finding) | git-secrets, trufflehog | Artifact CI, 1 an |
| Container scan | JSON (Trivy) | Trivy | Artifact CI, 1 an |

### Rapports qualité

| Type | Format accepté | Outil | Conservation |
|------|---------------|-------|-------------|
| Lint | Log texte (0 erreur) | ESLint, flake8 | Artifact CI, 30 jours |
| Accessibilité | JSON (axe-core) + rapport HTML | axe, pa11y | Artifact CI, 90 jours |
| Performance | JSON Lighthouse | Lighthouse CI | Artifact CI, 30 jours |
| Evals agents | Score JSON + détails | Script interne | Artifact CI, 1 an |

### Captures et artefacts visuels

| Type | Format accepté | Quand requis |
|------|---------------|-------------|
| Screenshot UI | PNG, ≥ 1280px wide | Changement visuel significatif |
| Capture navigateur E2E | PNG (Playwright auto) | Échec E2E, validation Gate 7 |
| Vidéo E2E | WebM (Playwright) | Optionnel, parcours complexes |

### Traçabilité documentaire

| Élément | Preuve acceptée |
|---------|----------------|
| Changement livrable | Diff CHANGELOG.md (section Unreleased) |
| Décision structurante | ADR dans docs/adr/ avec date et statut |
| Exception quality gate | Entrée EXCEPTIONS.md validée et signée |
| Session de travail | Entrée SESSION_LOG.md |
| Release | Tag Git versionné + CHANGELOG section versionnée |

---

## Preuves minimales par type de changement

| Type | Preuves obligatoires |
|------|---------------------|
| Bug fix | Tests unitaires vert + test de régression + CHANGELOG |
| Feature frontend | Tests unitaires + E2E + accessibilité + screenshot + CHANGELOG |
| Feature backend | Tests unitaires + intégration + SAST + audit dépendances + CHANGELOG |
| Changement API | Tests intégration + doc API mise à jour + CHANGELOG |
| Changement dépendance | Dependency audit + validation SUPPLY_CHAIN + CHANGELOG |
| Changement sécurité | SAST + audit + revue humaine + CHANGELOG |
| Changement prompt/agent | Score evals + SAST output IA + PROMPT_GOVERNANCE mis à jour |
| Documentation seule | Diff markdown + vérification liens |
| Release | Toutes les preuves du contenu de la release + Gate 7 sign-off |

---

## Règles de conservation

- Preuves CI : conservées comme artifacts dans GitHub Actions (durée selon type ci-dessus)
- Evidence package release : archivé dans un répertoire immuable ou taggé dans Git
- Rapports sécurité : 1 an minimum (conformité)
- Rapports evals IA : 1 an minimum (audit gouvernance IA)

---

## Ce qui N'est PAS une preuve valide

- "Ça marche sur ma machine" sans log reproductible
- Un screenshot sans horodatage ni commit associé
- Un test marqué `.skip` ou désactivé
- Un log tronqué ou partiel
- Une déclaration verbale non documentée
