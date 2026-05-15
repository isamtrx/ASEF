# APPSEC.md — ASEF

> Sécurité applicative — SAST, DAST et pratiques de codage sécurisé.  
> 1 responsabilité : définir les contrôles sécurité au niveau du code et des applications.  
> Dépend de : SECURITY.md  
> Ne doit jamais contenir : gestion secrets (→ SECRETS.md), accès (→ ACCESS_CONTROL.md).

---

## SAST — Analyse statique

**Outil principal :** Semgrep  
**Outil secondaire :** CodeQL (pour les repos GitHub Actions)  
**Déclencheur :** Chaque PR, chaque merge sur main

```bash
# Analyse complète
semgrep --config=auto . --json > reports/sast.json

# Avec règles OWASP
semgrep --config=p/owasp-top-ten . --json >> reports/sast.json

# Avec règles spécifiques IA (prompt injection)
semgrep --config=p/ai-security . --json >> reports/sast.json
```

**Seuils bloquants :**
- 0 finding de sévérité HIGH ou CRITICAL
- 0 finding de type : injection SQL, XSS, deserialization, SSRF, path traversal

**Findings MEDIUM :**
- Non bloquants en CI, mais doivent être traités dans le sprint en cours

---

## DAST — Analyse dynamique

**Outil :** OWASP ZAP (scan passif en staging)  
**Déclencheur :** Avant chaque release (Gate 7)  
**Périmètre :** Endpoints API exposés + pages web

```bash
docker run -v $(pwd)/reports:/zap/wrk/:rw \
  owasp/zap2docker-stable zap-baseline.py \
  -t http://staging-url -r zap-report.html
```

**Seuils bloquants :**
- 0 alert HIGH ou CRITICAL
- 0 injection (SQL, command, LDAP)
- 0 broken auth

---

## Règles de codage sécurisé

### Validation des entrées

- Valider **toutes** les entrées côté serveur (jamais seulement côté client)
- Utiliser des schemas de validation (Zod, Joi, Pydantic, etc.)
- Whitelisting plutôt que blacklisting pour les valeurs autorisées
- Limiter la taille des payloads (max-body-size sur les endpoints)

```typescript
// Correct
const schema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100)
});

// Interdit
function createUser(data: any) { ... }
```

### Prévention des injections

- SQL : uniquement des requêtes paramétrées ou ORM — jamais de concaténation
- Shell : pas d'exécution de commandes shell construites avec des inputs utilisateur
- HTML : encoder tous les outputs dans les templates
- Prompt IA : ne jamais insérer d'input utilisateur directement dans un prompt sans sanitisation

```python
# Correct
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Interdit
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Authentification et sessions

- Tokens JWT : signature HS256 minimum, expiration ≤ 1h pour les access tokens
- Refresh tokens : rotation systématique à chaque usage
- Mots de passe : bcrypt ou argon2 avec coût ≥ 12
- Sessions : invalidation explicite à la déconnexion
- 2FA obligatoire pour les accès admin

### Gestion des erreurs

- Ne jamais exposer les stack traces en production
- Messages d'erreur génériques côté client, détaillés dans les logs serveur
- Logs d'erreurs sans données personnelles ni secrets

### Headers HTTP de sécurité

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

---

## Gestion des vulnérabilités détectées

| Sévérité | Délai de correction | Action |
|----------|--------------------|----|
| CRITICAL | 24h | Blocage livraison + incident INCIDENT_RESPONSE.md |
| HIGH | 72h | Ticket prioritaire + exception EXCEPTIONS.md si > 72h |
| MEDIUM | 2 semaines | Ticket normal |
| LOW | Prochain sprint | Backlog |
