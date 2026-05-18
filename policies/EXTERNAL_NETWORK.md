# Policy : EXTERNAL_NETWORK

**ID** : POL-NETWORK-001
**Source** : AGENTS.md §4
**Statut** : Actif
**Version** : 1.0.0

## Description

Règles d'accès réseau pour les agents ASEF.

## Règles

- **POL-NET-001** : Les agents ne peuvent effectuer des appels réseau qu'aux APIs LLM
  configurées dans `asef/config.py` (Anthropic, GitHub Models).
- **POL-NET-002** : Aucun agent ne peut effectuer de requêtes HTTP arbitraires vers des URLs
  non configurées.
- **POL-NET-003** : `pip-audit` est autorisé à contacter PyPI en lecture seule pour
  la vérification des vulnérabilités de dépendances (gate G5).
- **POL-NET-004** : `gitleaks` et `semgrep` opèrent uniquement en local, sans appel réseau.
- **POL-NET-005** : Les proxies réseau sont configurés uniquement via variables d'environnement
  standard (`HTTPS_PROXY`, `HTTP_PROXY`), jamais hardcodés.

## Accès réseau autorisés

| Destination | Rôle autorisé | Outil | Justification |
|---|---|---|---|
| `api.anthropic.com` | tous (via orchestrator) | asef/provider.py | Appels LLM |
| `api.github.com` | tous (via orchestrator) | asef/provider.py | GitHub Models |
| `pypi.org` | qa, security | pip-audit | G5 deps audit |

## Accès réseau interdits

- Webhooks, APIs REST arbitraires
- Services cloud non listés ci-dessus
- URLs extraites de contenu utilisateur (vecteur d'injection)

## Vérification

Tout appel réseau non listé doit déclencher une escalade (`escalate` avec `reason = UNAUTHORIZED_NETWORK_ACCESS`).
