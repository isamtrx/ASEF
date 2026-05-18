# POLICY: AUTONOMY LEVELS

**Source** : AGENTS.md §3 + §10
**Statut** : active
**ID** : POL-AUTONOMY-001

## Niveaux d'autonomie

| Niveau | Description | Exemples |
|---|---|---|
| `AUTONOMOUS` | Agent décide et exécute seul | Correction de lint, mise à jour CHANGELOG |
| `SUPERVISED` | Agent exécute mais doit produire une preuve | Tests, sécurité — gates exécutés + rapport |
| `GATED` | Agent exécute, gate bloquant, humain si rouge | G3/G4/G5 rouges → escalade |
| `HUMAN_REQUIRED` | Agent prépare, humain décide | Release, décision structurante, SCOPE.md |
| `FORBIDDEN` | Agent ne peut pas exécuter | Actions destructives, fichiers protégés |

## Mapping task_type → autonomie minimale

| task_type | Autonomie | Justification |
|---|---|---|
| `bugfix` | SUPERVISED | Gates requis mais pas d'approbation |
| `feature` | SUPERVISED | idem + ADR si structurant |
| `review` | AUTONOMOUS | Lecture seule |
| `audit` | SUPERVISED | Rapport requis |
| `release` | HUMAN_REQUIRED | Gate G7 toujours humain |
| `security` | GATED | Escalade si finding critique |
| `documentation` | AUTONOMOUS | Écriture docs non-protégées |
| `governance` | HUMAN_REQUIRED | ADR + validation humaine |

## Configuration

Voir `config/autonomy.config.json` pour ajustements par environnement.
