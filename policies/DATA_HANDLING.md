# Policy : DATA_HANDLING

**ID** : POL-DATA-001
**Source** : AGENTS.md §4 + RGPD
**Statut** : Actif
**Version** : 1.0.0

## Description

Règles de traitement des données, en particulier les données personnelles (PII)
et les données client.

## Règles

- **POL-DATA-001** : Aucune donnée personnelle (PII) ne peut être envoyée à un modèle LLM
  externe sans validation humaine explicite.
- **POL-DATA-002** : Aucune donnée client réelle ne peut être stockée dans `artifacts/`.
  Les artifacts contiennent uniquement des métadonnées et des résumés anonymisés.
- **POL-DATA-003** : Les logs de session (`SESSION_LOG.md`, `memory/*.jsonl`) ne doivent
  pas contenir d'identifiants personnels, de clés API, ou de mots de passe.
- **POL-DATA-004** : Avant de logger une entrée dans `memory/tool_calls.jsonl`,
  les valeurs de paramètres potentiellement sensibles doivent être masquées
  (ex: `--password ***MASKED***`).
- **POL-DATA-005** : Les fichiers `.env` et leurs équivalents ne sont jamais lus par les agents.
  La configuration est lue via `asef/config.py` depuis les variables d'environnement.

## Types de données PII

Les données suivantes sont considérées PII et soumises à la politique :

- Noms complets
- Adresses email
- Numéros de téléphone
- Adresses physiques
- Identifiants nationaux (SIRET, NIR, etc.)
- Données de localisation précise

## Procédure en cas de détection de PII

1. Stopper le traitement immédiatement.
2. Logger une alerte dans `SESSION_LOG.md` (sans reproduire la donnée).
3. Appeler `escalate` avec `reason = PII_DETECTED`.
4. Ne pas continuer sans validation humaine.
