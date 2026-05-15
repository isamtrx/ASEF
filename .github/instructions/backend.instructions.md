---
applyTo: "**/*.{py,ts,js,go,java,cs,rs}"
---

# Instructions Backend — ASEF

> S'applique à : API, services, workers, scripts, fonctions backend  
> Lire d'abord : AGENTS.md → docs/ARCHITECTURE.md → docs/API.md → docs/security/SECURITY.md

## Avant de modifier

1. Vérifier le contrat API dans `docs/API.md` (ne pas casser un contrat existant)
2. Identifier les dépendances dans `docs/ARCHITECTURE.md`
3. Vérifier les données sensibles dans `docs/DATA.md`

## Règles de code backend

- **Validation** : valider tous les inputs à la frontière du système (jamais faire confiance à l'entrée externe)
- **Erreurs** : ne jamais exposer les stack traces en production, logger avec contexte
- **Auth** : vérifier l'authentification et l'autorisation avant toute opération
- **Secrets** : utiliser les variables d'environnement, jamais de secrets en clair dans le code
- **Idempotence** : les endpoints POST critiques doivent être idempotents (avec un idempotency key)
- **Pagination** : obligatoire sur tout endpoint retournant des listes

## Standards API (voir docs/API.md)

- HTTP status codes sémantiques (200/201/400/401/403/404/409/422/500)
- Format erreur standardisé : `{ "error": { "code": "", "message": "", "details": {} } }`
- Versioning via URL path : `/api/v1/`
- Authentification via Bearer token (JWT) ou API key selon le contexte

## Patterns autorisés

- Repository pattern pour l'accès aux données
- Service layer pour la logique métier
- Dependency injection (pas de singletons globaux mutables)
- Circuit breaker sur les appels services externes

## Patterns interdits

- SQL brut sans paramétrage (risque injection SQL)
- Secrets ou credentials dans le code source
- Logs contenant des données PII ou des tokens
- Endpoints sans validation d'input
- Retry infini sans backoff exponentiel

## Contrôles obligatoires avant livraison

```bash
# Tests unitaires + intégration
npm run test (ou pytest, go test, etc.)

# SAST
npm run sast (ou équivalent configuré)

# Dependency audit
npm audit --audit-level=high

# Lint
npm run lint
```

## Preuves attendues

- Log de tests avec couverture ≥ seuil QA.md
- Rapport `npm audit` sans vulnérabilité HIGH ou CRITICAL
- Log SAST propre

## Erreurs communes à éviter

- N+1 queries (utiliser eager loading ou batch queries)
- Ne pas fermer les connexions DB dans les error paths
- Oublier de valider les types de données reçus de sources externes
- Utiliser des dates sans timezone dans les comparaisons
- Logger des mots de passe ou tokens même en mode debug
