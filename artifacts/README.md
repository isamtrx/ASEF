# artifacts/

Ce répertoire stocke tous les artifacts produits par le pipeline ASEF.

## Structure

| Sous-répertoire | Contenu |
|---|---|
| `reports/` | Rapports finaux de tâches |
| `audits/` | Rapports d'audit repo |
| `diffs/` | Diffs de changements livrés |
| `logs/` | Logs d'exécution bruts |
| `qa/` | Rapports QA (G3, G4) |
| `security/` | Rapports sécurité (G5) |
| `releases/` | Evidence packages de release |

## Rules

- Tous les artifacts sont en lecture seule après production
- Nommage : `<YYYY-MM-DD>_<task_id>_<type>.<ext>`
- Rétention : 90 jours par défaut (configurable dans `config/memory.config.json`)
- Jamais de secret ou donnée sensible dans les artifacts
