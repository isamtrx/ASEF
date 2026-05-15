# API.md — ASEF

> Source de vérité des standards d'API.  
> 1 responsabilité : conventions REST, format des erreurs, versionnement et contrats.  
> Dépend de : ARCHITECTURE.md, STANDARDS.md  
> Ne doit jamais contenir : implémentation applicative, configuration réseau.

---

## Conventions REST

### Naming des endpoints

```
GET    /api/v1/resources          → Liste
GET    /api/v1/resources/:id      → Détail
POST   /api/v1/resources          → Création
PUT    /api/v1/resources/:id      → Remplacement complet
PATCH  /api/v1/resources/:id      → Modification partielle
DELETE /api/v1/resources/:id      → Suppression
```

**Règles :**
- Noms en kebab-case, pluriel : `/agent-actions`, pas `/agentAction`
- Pas de verbe dans l'URL : `/api/v1/agents` (pas `/api/v1/getAgents`)
- IDs opaques (UUID v4), jamais d'identifiants séquentiels exposés
- Sous-ressources : `/api/v1/agents/:id/actions`

---

## Versionnement

- Version dans l'URL : `/api/v1/`, `/api/v2/`
- Version MAJOR uniquement dans l'URL (pas de v1.2 dans l'URL)
- Cycle de dépréciation minimum 6 mois avant suppression d'une version
- Header de dépréciation : `Sunset: <date ISO>`

---

## Format des réponses

### Succès

```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2026-05-15T14:23:01.123Z",
    "trace_id": "uuid-v4",
    "version": "1.0.0"
  }
}
```

### Erreur

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "La ressource demandée n'existe pas.",
    "trace_id": "uuid-v4",
    "details": []
  }
}
```

---

## Codes d'erreur standard

| Code HTTP | Code erreur ASEF | Description |
|-----------|----------------|-------------|
| 400 | `INVALID_INPUT` | Corps de requête invalide |
| 400 | `VALIDATION_ERROR` | Erreur de validation avec détails |
| 401 | `UNAUTHORIZED` | Authentification requise ou invalide |
| 403 | `FORBIDDEN` | Authentifié mais non autorisé |
| 404 | `RESOURCE_NOT_FOUND` | Ressource non trouvée |
| 409 | `CONFLICT` | Conflit de ressource (déjà existant) |
| 422 | `UNPROCESSABLE` | Données valides mais logique métier rejetée |
| 429 | `RATE_LIMITED` | Trop de requêtes |
| 500 | `INTERNAL_ERROR` | Erreur serveur non anticipée |
| 503 | `SERVICE_UNAVAILABLE` | Service temporairement indisponible |

---

## Authentification

- **Méthode** : Bearer token (JWT) dans l'en-tête `Authorization`
- **Format** : `Authorization: Bearer <token>`
- Les tokens ont une durée de vie limitée (max 24h)
- Refresh token avec rotation obligatoire
- Pas d'authentification par paramètre URL

---

## Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 143,
    "next": "/api/v1/resources?page=2",
    "prev": null
  }
}
```

---

## En-têtes obligatoires

**Requête :**
- `Content-Type: application/json` pour les requêtes avec corps
- `Authorization: Bearer <token>` pour les endpoints authentifiés
- `X-Request-ID: uuid-v4` (optionnel mais fortement recommandé pour le tracing)

**Réponse :**
- `Content-Type: application/json`
- `X-Trace-Id: uuid-v4` (identifiant de trace propagé)
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`

---

## Documentation des endpoints (format OpenAPI)

Chaque endpoint est documenté dans `docs/openapi.yaml` au format OpenAPI 3.1.  
Le fichier est versionné avec le code source et généré si possible depuis les annotations.
