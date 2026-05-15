---
applyTo: "**/*.{test,spec}.{ts,tsx,js,jsx,py}"
---

# Instructions QA — ASEF

> S'applique à : tests unitaires, tests d'intégration, tests E2E, fixtures, mocks  
> Lire d'abord : AGENTS.md → docs/quality/QA.md → docs/quality/QUALITY_GATES.md

## Avant d'écrire un test

1. Identifier le gate concerné dans `docs/quality/QUALITY_GATES.md`
2. Vérifier les commandes de test dans `docs/quality/QA.md`
3. Vérifier si un test similaire existe (ne pas dupliquer)

## Règles de test

- **Un test = une assertion principale.** Un test qui teste 7 choses simultanément est illisible.
- **Tests déterministes.** Pas de `Math.random()`, pas de `Date.now()` non mocké.
- **Tests isolés.** Chaque test doit pouvoir tourner seul sans dépendre d'un autre.
- **Mocks explicites.** Documenter pourquoi quelque chose est mocké.
- **Arrange-Act-Assert.** Structure systématique.
- **Naming.** `test("should [comportement] when [condition]")` — pas de `test("test1")`.

## Types de tests et couverture minimale (voir QA.md pour seuils)

| Type | Scope | Outil suggéré |
|------|-------|--------------|
| Unitaires | Fonctions, composants isolés | Jest, pytest, Vitest |
| Intégration | Flux inter-modules | Jest + supertest, pytest |
| E2E | Parcours utilisateur complets | Playwright |
| Accessibilité | UI — WCAG AA | axe-core, pa11y |
| Performance | Core Web Vitals | Lighthouse CI |
| Sécurité | SAST, dependency audit | Semgrep, npm audit |

## Patterns autorisés

- Factory functions pour les fixtures (pas de données hardcodées globales)
- Mocks au niveau module pour les dépendances externes
- Snapshot tests uniquement pour les composants stables

## Patterns interdits

- Tests qui modifient la base de données de production
- `expect.anything()` sur des champs critiques (typer précisément)
- `setTimeout` dans les tests (utiliser `jest.useFakeTimers`)
- Désactiver un test avec `xtest` ou `.skip` sans commentaire de raison et ticket
- Assertions sur des strings localisées sans mock du système i18n

## Preuves attendues (evidence package Gate 4)

```
□ Log complet de l'exécution des tests (aucun rouge)
□ Rapport de couverture (coverage ≥ seuil défini dans QA.md)
□ Rapport Lighthouse si changement UI (performance + accessibilité)
□ Aucun test skippé sans justification
```

## Commandes de référence

```bash
# Run tous les tests avec couverture
npm run test:coverage

# Run tests E2E
npm run test:e2e

# Run audit accessibilité
npm run test:a11y

# Run Lighthouse CI
npx lhci autorun
```

## Erreurs communes à éviter

- Tester l'implémentation plutôt que le comportement
- Mocks qui ne reflètent plus l'API réelle (stale mocks)
- Tests qui passent par chance (race conditions)
- Oublier de tester les cas d'erreur et les edge cases
- Coverage 100% artificiel avec des tests sans assertions utiles
