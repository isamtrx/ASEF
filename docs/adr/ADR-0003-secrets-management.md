# ADR-0003 — Gestion des secrets : GitHub Secrets + interdiction plaintext

Date : 2026-05-15  
Statut : Validé  
Auteur : Platform Engineering

---

## Contexte

ASEF intègre plusieurs outils qui requièrent des credentials : tokens LLM (OpenAI, Anthropic), secrets CI/CD, tokens GitHub. La politique de gestion de ces secrets doit être explicitement définie pour éviter les fuites en dépôt.

L'interdiction absolue dans AGENTS.md §4 stipule déjà : "INTERDIT — Committer un secret, token, mot de passe ou clé API dans le dépôt". Cette ADR formalise comment cette règle est implémentée techniquement.

---

## Options considérées

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **GitHub Secrets + git-secrets scan** | Natif GitHub CI, gratuit, scan automatique au push | Pas de rotation automatique, pas de vault enterprise |
| HashiCorp Vault | Rotation automatique, audit complet | Infra supplémentaire, coût, complexité |
| `.env` commité avec chiffrement | Simple | Non recommandé — risque de déchiffrement |
| Doppler / 1Password Secrets | Bonne DX, rotation | 3rd party, coût |

---

## Décision

**GitHub Secrets** pour les secrets CI + **`git-secrets`** comme gate de détection au push. Aucun secret en plaintext dans le dépôt sous quelque forme que ce soit.

---

## Raison

- Cohérence avec ADR-0002 (GitHub Actions) : les secrets GitHub sont directement injectés comme variables d'environnement dans les workflows
- `git-secrets` peut être exécuté en pre-commit hook et en CI (Gate G5)
- La stack est docs-first à ce stade — pas besoin d'un vault enterprise
- L'ADR sera révisé si un besoin de rotation automatique ou d'audit détaillé émerge

---

## Règles découlant de cette décision

1. Tous les secrets sont dans GitHub Secrets (ou équivalent plateforme CI) — jamais dans le code
2. Le fichier `.env.example` contient des valeurs fictives uniquement
3. `.env` et tout fichier contenant des secrets réels est dans `.gitignore`
4. `git-secrets` est configuré en pre-commit hook ET en CI
5. Toute rotation de secret est documentée dans SESSION_LOG.md (sans révéler la valeur)

---

## Conséquences

**Positives :**
- Gate G5 implémentable sans infra supplémentaire
- Scan automatique au push et en CI

**Négatives :**
- Pas de rotation automatique
- Audit des accès secrets limité à l'interface GitHub

---

## Réversibilité

Réversible — migration vers Vault ou autre solution de secrets management possible sans changer l'architecture applicative.

---

## Fichiers concernés

- `docs/security/SECRETS.md` — politique complète
- `docs/security/SECURITY.md` — contrôles de sécurité
- `docs/delivery/CI_CD.md` — intégration dans le pipeline
