# DIRECTIVE-17 — DOCUMENTATION

## Purpose

Règles de mise à jour de la documentation du projet.

> Standards complets : `.github/instructions/docs.instructions.md`

Pourquoi elle existe : la documentation désynchronisée du code crée des dettes
et des erreurs d'interprétation pour les agents futurs.
Quand elle est utilisée : toute tâche qui modifie le comportement du système.
Quelle décision elle encadre : quels fichiers docs mettre à jour et comment.
Quelle mauvaise action elle empêche : code livré sans CHANGELOG.md, ADR sans docs.

## Scope

Couvre : CHANGELOG.md, SESSION_LOG.md, LESSONS_LEARNED.md, docs/, README.md.
Ne couvre pas : la documentation domaine dans domains/ (gérée par les frameworks).

## Mandatory Rules

1. [DOC-001] CHANGELOG.md mis à jour pour tout changement livrable.
   - Why: traçabilité des versions.
   - Blocks: livraison sans entrée Unreleased dans CHANGELOG.md.
   - Evidence: diff de CHANGELOG.md avec nouvelle entrée.

2. [DOC-002] SESSION_LOG.md mis à jour en fin de session.
   - Why: AGENTS.md §8 impose la traçabilité des sessions.
   - Blocks: clôture de session sans log.
   - Evidence: entrée dans SESSION_LOG.md avec date, objectif, outcome.

3. [DOC-003] LESSONS_LEARNED.md mis à jour après bug ou escalade.
   - Why: éviter de répéter les erreurs.
   - Blocks: clôture de session escaladée sans leçon.
   - Evidence: entrée dans LESSONS_LEARNED.md avec Erreur → Cause → Règle.

4. [DOC-004] Un ADR doit être créé pour toute décision structurante.
   - Why: les décisions non documentées créent des précédents invisibles.
   - Blocks: décision structurante sans ADR dans docs/adr/.
   - Evidence: fichier docs/adr/ADR-XXXX-slug.md.

## Required Inputs

- `.github/instructions/docs.instructions.md` — standards de documentation

## Required Outputs

- CHANGELOG.md mis à jour (si changement livrable)
- SESSION_LOG.md mis à jour (toujours)
- ADR si décision structurante

## Validation Checklist

- [ ] CHANGELOG.md a une section Unreleased non vide si changement livrable
- [ ] SESSION_LOG.md a une entrée avec timestamp du jour
- [ ] LESSONS_LEARNED.md mis à jour si incident ou escalade
- [ ] Tout ADR référencé dans DECISIONS.md

## Rejection Criteria

- Livraison sans CHANGELOG.md mis à jour → BLOCKED
- Session terminée sans SESSION_LOG.md → BLOCKED

## Related Directives

- `directives/20_GOVERNANCE.md` — ADR et décisions
- `directives/00_MASTER.md` — séquence de bootstrap

## Evidence Required

- diff de CHANGELOG.md
- entrée dans SESSION_LOG.md (timestamp + outcome)
