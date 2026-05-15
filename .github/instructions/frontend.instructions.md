---
applyTo: "**/*.{tsx,jsx,ts,js,css,scss,html}"
---

# Instructions Frontend — ASEF

> S'applique à : tout fichier frontend (composants, styles, pages, hooks, utils UI)  
> Lire d'abord : AGENTS.md → SCOPE.md → docs/ARCHITECTURE.md

## Avant de modifier

1. Identifier le composant dans `docs/ARCHITECTURE.md` (section Frontend)
2. Vérifier les patterns autorisés dans `docs/governance/ENGINEERING_HANDBOOK.md`
3. Vérifier les standards UI dans `docs/governance/STANDARDS.md`

## Règles de code frontend

- **Composants** : fonctionnels uniquement, pas de classes React
- **État** : state local via useState/useReducer, global via le store défini en architecture
- **Props** : typées explicitement — jamais `any`
- **Effets** : documenter les dépendances de useEffect, cleanup obligatoire si subscription
- **Accessibilité** : attributs `aria-*` sur éléments interactifs, contraste WCAG AA minimum
- **Performance** : éviter les re-renders inutiles, mémoïser avec parcimonie et justification

## Patterns autorisés

- Composition de composants (pas d'héritage)
- Custom hooks pour la logique réutilisable
- CSS Modules ou Tailwind (selon choix défini dans ARCHITECTURE.md)
- Lazy loading des routes

## Patterns interdits

- `any` sur les props ou les données API
- Logique métier dans les composants de présentation
- Appels API directs dans les composants (passer par des hooks ou services)
- Styles inline non justifiés
- Mutation directe du state

## Contrôles obligatoires avant livraison

```bash
# Tests unitaires composants
npm run test -- --coverage

# Lint
npm run lint

# Vérification types
npm run type-check

# Tests accessibilité (si configuré)
npm run test:a11y
```

## Preuves attendues

- Log de `npm run test` avec coverage ≥ seuil défini dans QA.md
- Log de `npm run lint` sans erreur
- Capture navigateur si changement visuel

## Erreurs communes à éviter

- Oublier le cleanup des subscriptions (memory leaks)
- Ne pas gérer les états d'erreur dans les fetch hooks
- Hardcoder des URLs API (utiliser les variables d'environnement)
- Committer des fichiers `.env` ou des clés API
