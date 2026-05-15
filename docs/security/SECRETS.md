# SECRETS.md — ASEF

> Source de vérité sur la gestion des secrets et des credentials.  
> 1 responsabilité : définir où stocker les secrets, comment les faire tourner et quoi faire en cas de fuite.  
> Dépend de : SECURITY.md  
> Ne doit jamais contenir : secrets réels (JAMAIS dans Git).

---

## Principe absolu

**Aucun secret ne doit jamais apparaître dans le code source, les fichiers de config versionnés, les logs, les prompts IA ou les messages de commit.**

---

## Définition d'un secret

Un secret est toute information dont la divulgation permet un accès non autorisé :
- Clés API (OpenAI, Anthropic, AWS, GitHub, etc.)
- Tokens d'authentification (JWT secrets, OAuth secrets)
- Mots de passe (bases de données, services)
- Certificats et clés privées
- Variables d'environnement sensibles

---

## Stockage autorisé

| Contexte | Stockage autorisé |
|---------|------------------|
| Développement local | Fichier `.env` non versionné (listé dans .gitignore) |
| CI/CD | GitHub Actions Secrets (chiffrés, jamais dans les logs) |
| Production | Secret Manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) |
| Documentation | Placeholder uniquement : `[YOUR_API_KEY]` |

---

## Stockage interdit

```
INTERDIT — Fichier versionné dans Git (.env, config.json, appsettings.json...)
INTERDIT — Hardcodé dans le code source
INTERDIT — Dans les logs applicatifs
INTERDIT — Dans le contexte d'un agent IA (prompt, mémoire)
INTERDIT — Dans les messages de commit ou les descriptions de PR
INTERDIT — Dans les fichiers de documentation markdown
INTERDIT — En clair dans les variables CI affichées dans les logs
```

---

## Détection automatique

Le secret scan est exécuté à chaque commit via git hooks et CI :

```bash
# git-secrets (local)
git secrets --install
git secrets --register-aws
git secrets --scan

# trufflehog (CI)
trufflehog git file://. --json > reports/secrets.json

# gitleaks (CI)
gitleaks detect --source . --report-format json --report-path reports/gitleaks.json
```

Un finding = Gate 5 rouge. Blocage immédiat.

---

## Règle .gitignore obligatoire

Le fichier `.gitignore` doit toujours inclure :

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
secrets/
.secrets
```

---

## Rotation des secrets

| Type de secret | Fréquence de rotation | Priorité si compromis |
|---------------|----------------------|----------------------|
| Clés API LLM | 6 mois | < 1h |
| Tokens CI/CD | 3 mois | < 30min |
| Credentials DB | 6 mois | < 1h |
| JWT secrets | 1 an | < 4h |

---

## Procédure en cas de secret commité

1. **Immédiatement** : révoquer le secret dans le service concerné (ne pas attendre)
2. **Immédiatement** : ouvrir un incident dans `docs/security/INCIDENT_RESPONSE.md`
3. **Immédiatement** : notifier le Tech Lead et le CTO
4. Dans les 24h : nettoyer l'historique Git (git filter-repo) avec validation TL
5. Dans les 24h : générer un nouveau secret et le déployer
6. Documenter la procédure dans `POSTMORTEMS.md`

**Attention :** Supprimer le commit ne suffit pas si le secret a été exposé même 1 minute. Il faut toujours révoquer d'abord.

---

## Agents IA et secrets

- Un agent ne doit JAMAIS lire un fichier `.env` ou tout fichier contenant des credentials
- Si l'agent détecte un secret dans son contexte, il doit alerter et arrêter l'exécution
- Les secrets ne doivent pas être transmis comme paramètres de prompt
