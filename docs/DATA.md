# DATA.md — ASEF

> Source de vérité de la gestion des données.  
> 1 responsabilité : types de données, stockage, rétention, indexation et ce qui est envoyé aux LLMs.  
> Dépend de : ARCHITECTURE.md, SECURITY.md  
> Ne doit jamais contenir : gestion des secrets (→ SECRETS.md), modèles IA (→ MODEL_POLICY.md).

---

## Inventaire des données

### Données de code source

| Type | Description | Sensibilité | Stockage |
|------|-------------|------------|---------|
| Code source | Fichiers .ts, .py, .go, etc. | Interne | Git repo |
| Tests | Fichiers de test | Interne | Git repo |
| Configuration | .env.example, config sans secrets | Interne | Git repo |
| Artifacts build | dist/, reports/ | Interne | CI artifacts |

### Données de gouvernance

| Type | Description | Sensibilité | Stockage |
|------|-------------|------------|---------|
| ADR | Décisions architecturales | Interne | Git repo |
| Session logs | Journal des sessions | Interne | Git repo |
| Evidence package | Preuves de qualité (CI logs, rapports) | Interne | CI artifacts |
| Audit logs agent | Piste d'audit actions IA | Confidentiel | Log store immuable |

### Données opérationnelles

| Type | Description | Sensibilité | Stockage |
|------|-------------|------------|---------|
| Logs applicatifs | Événements système | Interne | Log store |
| Métriques | Performance, SLOs | Interne | Metrics store |
| Traces | Distributed traces | Interne | Trace store |

---

## Données interdites dans le repo

Les données suivantes ne doivent **jamais** être dans le repo Git :

- Secrets, tokens, clés API, mots de passe
- Données personnelles (PII) : nom, email, adresse, numéro de sécu
- Données de santé
- Données financières identifiantes
- Bases de données de production (dumps)
- Credentials d'accès

→ Voir SECRETS.md pour la gestion des credentials.

---

## Ce qui est envoyé aux LLMs

Conformément à MODEL_POLICY.md, les données envoyées aux modèles IA externes sont limitées à :

| Données autorisées | Données interdites |
|-------------------|--------------------|
| Code source non sensible | Clés API, tokens |
| Texte de documentation | Données personnelles (PII) |
| Requêtes de génération de code | Données de production réelles |
| Résultats de tests | Configurations de sécurité internes |
| Messages d'erreur (sans stack privée) | Schémas de base de données de prod |

**Règle agent :** Avant d'envoyer un contexte à un LLM, vérifier qu'aucune donnée interdite n'est incluse dans le prompt.

---

## Rétention des données

| Type | Durée de rétention | Suppression |
|------|-------------------|------------|
| Logs applicatifs | 90 jours | Automatique |
| Audit logs agent | 1 an | Manuel avec justification |
| Evidence CI | 90 jours (artifacts) | Automatique GitHub |
| Evidence release | 1 an | Archivage |
| Session logs Git | Permanente | Non (historique Git) |
| Métriques | 13 mois | Automatique |

---

## Indexation et recherche

Les données de gouvernance (fichiers Markdown) sont indexées par Git.  
Recherche dans le repo : `git grep`, `grep_search`, `semantic_search`.

Pour les logs et métriques opérationnels : indexation dans le log store avec rétention définie ci-dessus.

---

## Conformité RGPD

ASEF v0.1.0 est un framework sans traitement de données personnelles en production.

Si un projet dérivé traite des données personnelles, il doit :
1. Ajouter une DPIA (Data Protection Impact Assessment)
2. Documenter les bases légales dans ce fichier
3. Ajouter les mécanismes de droit à l'effacement
4. Notifier le DPO si applicable
