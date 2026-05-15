# GitHub Copilot Instructions — ASEF

> Adaptateur GitHub Copilot pour ASEF.  
> Source de vérité agents : [AGENTS.md](../AGENTS.md)  
> En cas de conflit, AGENTS.md prime.

## Bootstrap obligatoire

```
1. AGENTS.md          → constitution et permissions
2. MEMORY.md          → contexte actuel
3. SCOPE.md           → périmètre (tâche IN scope ?)
4. DECISIONS.md       → décisions actives
```

## Fichiers sources de vérité

| Sujet | Fichier |
|-------|---------|
| Constitution agents | `AGENTS.md` |
| Périmètre | `SCOPE.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| Quality gates | `docs/quality/QUALITY_GATES.md` |
| Sécurité | `docs/security/SECURITY.md` |
| Gouvernance IA | `docs/ai/AI_GOVERNANCE.md` |

## Règles avant modification

- Modifications chirurgicales : toucher uniquement ce qui est demandé
- Ne pas refactorer hors demande explicite
- Ne pas ajouter de features hors DoD
- Respecter les patterns de `docs/governance/ENGINEERING_HANDBOOK.md`
- Décision structurante → `DECISIONS.md` avant d'implémenter

## Règles de test

- Tests définis dans `docs/quality/QA.md`
- Ne jamais déclarer un test passé sans l'exécuter
- Gate G4 (tests) et G5 (sécurité) sont toujours bloquants

## Règles de documentation

- `CHANGELOG.md` : mettre à jour pour tout changement livrable
- `SESSION_LOG.md` : entrée en fin de session
- Ne jamais dupliquer du contenu existant dans d'autres fichiers

## Interdictions critiques

```
INTERDIT — Secret, token ou clé dans le dépôt
INTERDIT — Contournement d'un quality gate bloquant
INTERDIT — Push direct sur main ou branche protégée
INTERDIT — Test déclaré passé sans exécution réelle
INTERDIT — Refactoring non demandé explicitement
INTERDIT — Créer des missions KERN depuis ce repo
INTERDIT — Déployer sans confirmation humaine explicite
```

## Critères de complétion

```
□ DoD satisfait ligne par ligne
□ Tests passés — logs fournis
□ CHANGELOG.md mis à jour
□ SESSION_LOG.md entrée ajoutée
□ Aucun secret committé
□ Gate G7 : validation humaine si release critique
```

## Fin de tâche

```
kern_write_lesson("...", "ASEF")
kern_log_project_action("...", "ASEF", "DONE")
```
