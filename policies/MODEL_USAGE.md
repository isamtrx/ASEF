# Policy : MODEL_USAGE

**ID** : POL-MODEL-001
**Source** : ADR-0002 (docs/adr/ADR-0002-selection-modeles-par-role.md)
**Statut** : Actif
**Version** : 1.0.0

## Description

Définit quel modèle LLM chaque rôle agent doit utiliser.
Implémenté dans `asef/config.py` et `asef/provider.py`.

## Mapping modèle par rôle

| Rôle | Modèle | Justification |
|---|---|---|
| `architect` | `claude-opus-4-7` | Décisions structurantes irréversibles — qualité maximale requise |
| `orchestrator` | `claude-sonnet-4-6` | Coordination et routage — équilibre coût/qualité |
| `developer` | `claude-sonnet-4-6` | Génération de code — équilibre éprouvé |
| `qa` | `claude-sonnet-4-6` | Analyse, validation — même tier que developer |
| `security` | `claude-sonnet-4-6` | Audit de sécurité — précision requise sans aller en opus |
| `docs` | `claude-haiku-4-5-20251001` | Mises à jour documentaires directes — économies justifiées |

## Surcharge par variable d'environnement

Chaque modèle peut être surchargé :

```bash
ASEF_MODEL_ARCHITECT=claude-opus-4-7
ASEF_MODEL_ORCHESTRATOR=claude-sonnet-4-6
ASEF_MODEL_DEVELOPER=claude-sonnet-4-6
ASEF_MODEL_QA=claude-sonnet-4-6
ASEF_MODEL_SECURITY=claude-sonnet-4-6
ASEF_MODEL_DOCS=claude-haiku-4-5-20251001
```

## Règles

- **POL-MODEL-001** : Aucun agent ne peut appeler un modèle d'un tier supérieur à celui assigné
  sans validation humaine (prévention de dérive de coût).
- **POL-MODEL-002** : Le provider par défaut est Anthropic. GitHub Models est un fallback
  configurable via `ASEF_PROVIDER=github`.
- **POL-MODEL-003** : Aucune clé API ne peut apparaître dans les logs ou fichiers.
  Utiliser exclusivement les variables d'environnement.
- **POL-MODEL-004** : En environnement de test, utiliser le mock provider de `asef/provider.py`
  pour éviter les appels LLM réels.
