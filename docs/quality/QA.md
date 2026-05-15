# QA.md — ASEF

> Source de vérité de la stratégie qualité.  
> 1 responsabilité : définir comment prouver qu'un changement fonctionne.  
> Dépend de : docs/ARCHITECTURE.md  
> Ne doit jamais contenir : policy sécurité, règles agents, procédures de release.

---

## Principe

Un changement sans preuves n'est pas livré. Les preuves sont définies ici, pas décidées au cas par cas.

---

## Types de tests par couche

### Tests unitaires

**Scope :** Fonctions, classes, composants isolés  
**Outil :** Jest / Vitest (JS/TS) · pytest (Python) · Go test (Go)  
**Seuil de couverture minimum :** 80% des lignes sur le périmètre modifié  
**Bloquant :** Oui (Gate 4)

```bash
# JavaScript/TypeScript
npm run test -- --coverage --passWithNoTests

# Python
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Go
go test ./... -cover
```

---

### Tests d'intégration

**Scope :** Flux inter-modules, API endpoints, intégrations DB  
**Outil :** Jest + Supertest · pytest + httpx · Testcontainers  
**Bloquant :** Oui (Gate 4)

```bash
npm run test:integration
pytest tests/integration/
```

---

### Tests E2E (End-to-End)

**Scope :** Parcours utilisateur complets dans un navigateur réel  
**Outil :** Playwright  
**Déclencheur :** Obligatoire si changement frontend avec flux utilisateur  
**Bloquant :** Oui si E2E existant tourne (Gate 4)

```bash
npx playwright test
npx playwright test --reporter=html
```

---

### Tests accessibilité

**Scope :** Tous les composants UI et pages  
**Outil :** axe-core (via jest-axe) · pa11y · Lighthouse CI  
**Standard :** WCAG 2.1 niveau AA minimum  
**Bloquant :** Oui sur violations CRITICAL (Gate 4)

```bash
npm run test:a11y
npx pa11y http://localhost:3000
```

---

### Tests performance

**Scope :** Pages critiques du parcours utilisateur principal  
**Outil :** Lighthouse CI  
**Seuils :**
- Performance score ≥ 80
- Core Web Vitals LCP < 2.5s, FID < 100ms, CLS < 0.1
**Bloquant :** Non (Gate 4) — alerte seulement, sauf régression > 20%

```bash
npx lhci autorun --config=.lighthouserc.json
```

---

### Tests sécurité (SAST + dependency)

**Scope :** Tout le code source + dépendances  
**Outil :** Semgrep · npm audit · pip-audit · Trivy  
**Bloquant :** Oui (Gate 5 — voir docs/quality/QUALITY_GATES.md)

```bash
semgrep --config=auto . --json > reports/sast.json
npm audit --audit-level=high
```

---

### Tests agents IA

**Scope :** Prompts, outputs IA, comportement agents  
**Outil :** Jeu de test défini dans docs/ai/EVALS.md  
**Bloquant :** Oui si score eval < seuil (Gate 4 étendu)

```bash
python scripts/run_evals.py --suite all
```

---

## Critères de passage (Gate 4)

| Test | Critère PASS | Critère FAIL |
|------|-------------|-------------|
| Unitaires | 0 rouge, coverage ≥ 80% | ≥ 1 rouge OU coverage < 80% |
| Intégration | 0 rouge | ≥ 1 rouge |
| E2E | 0 rouge (si existant) | ≥ 1 rouge |
| Accessibilité | 0 violation CRITICAL | ≥ 1 violation CRITICAL |
| Performance | Pas de régression > 20% | Régression > 20% sur métrique core |
| Agents | Score ≥ seuil EVALS.md | Score < seuil |

---

## Critères de refus (Gate 4 bloque la livraison)

- Un test unitaire ou d'intégration est rouge
- La couverture du code modifié est < 80%
- Un test E2E critique est rouge
- Une violation WCAG CRITICAL est introduite
- Un test est désactivé (`.skip`, `xtest`) sans justification et ticket associé

---

## Evidence package requis par type de changement

| Type de changement | Preuves minimales |
|-------------------|------------------|
| Bug fix | Logs tests unitaires + test de régression |
| Nouvelle feature | Logs tests unitaires + intégration + E2E si UI |
| Changement API | Logs tests intégration + doc API mise à jour |
| Changement sécurité | Rapport SAST + audit dépendances |
| Changement IA/prompt | Score evals + rapport sécurité output |
| Release | Toutes les preuves ci-dessus consolidées |

---

## Nommage des rapports

Les rapports sont stockés dans `reports/` (gitignored) pendant le développement, archivés dans CI comme artifacts.

```
reports/
├── test-results.xml          # JUnit format
├── coverage/                 # HTML coverage report
├── sast.json                 # SAST results
├── audit.json                # Dependency audit
├── lighthouse/               # Lighthouse reports
└── evals/                    # Agent eval results
```
