# DIRECTIVE-00 — MASTER

## Purpose

Point d'entrée unique pour tout agent opérant dans ce repo.
Définit la séquence de bootstrap, la table de routage par task_type
et les règles non-négociables qui s'appliquent à tout agent.

Cette directive est chargée pour **chaque tâche**, sans exception.
Les directives domaine sont chargées **en supplément** selon task_type.

Pourquoi elle existe : sans point d'entrée unique, chaque agent peut
interpréter différemment le périmètre, les permissions et les preuves requises.
Quand elle est utilisée : au bootstrap de chaque session agentique.
Quelle décision elle encadre : la sélection de toutes les autres directives.
Quelle mauvaise action elle empêche : exécution hors-périmètre, routage incorrect.

## Scope

Couvre : toute tâche soumise au runtime ASEF.
Ne couvre pas : les détails domaine (voir directives 05–29).
Quand consulter une autre directive : toujours, en complément de celle-ci.

## Mandatory Rules

1. [MASTER-001] Lire AGENTS.md avant toute action.
   - Why: AGENTS.md est la constitution — toutes les permissions y sont définies.
   - Blocks: action sans constitution lue.
   - Evidence: log de bootstrap mentionnant la lecture de AGENTS.md.

2. [MASTER-002] Classifier la tâche avant de l'exécuter.
   - Why: le routage dépend du type de tâche.
   - Blocks: exécution sans classification explicite.
   - Evidence: champ `task_type` dans le plan d'orchestration.

3. [MASTER-003] Vérifier SCOPE.md (Gate G1) avant toute action.
   - Why: les tâches hors-scope sont rejetées.
   - Blocks: exécution sur tâche hors-scope.
   - Evidence: `in_scope: true` dans le résultat de validation.

4. [MASTER-004] Produire un plan d'orchestration avant d'exécuter.
   - Why: le plan documente les agents, skills, tools et gates impliqués.
   - Blocks: exécution sans plan documenté.
   - Evidence: fichier JSON dans artifacts/reports/ ou stdout JSON.

5. [MASTER-005] Écrire SESSION_LOG.md à la fin de chaque session.
   - Why: traçabilité obligatoire selon AGENTS.md §8.
   - Blocks: clôture de session sans log.
   - Evidence: entrée dans SESSION_LOG.md avec timestamp et outcome.

6. [MASTER-006] Jamais affirmer succès sans preuve.
   - Why: auto-certification interdite.
   - Blocks: rapport final sans evidence package.
   - Evidence: commandes exécutées + exit codes + outputs.

7. [MASTER-007] Escalader si une tâche dépasse le scope ou les permissions.
   - Why: les gates bloquants nécessitent validation humaine.
   - Blocks: contournement silencieux d'un gate rouge.
   - Evidence: entrée dans LESSONS_LEARNED.md si escalade.

## Required Inputs

- `AGENTS.md` — constitution et permissions
- `MEMORY.md` — état courant du projet
- `SCOPE.md` — périmètre IN/OUT
- `DECISIONS.md` — décisions actives
- `registry/agents.registry.json` — agents disponibles
- `registry/directives.registry.json` — directives applicables

## Required Outputs

- Plan d'orchestration (JSON conforme à `schemas/orchestration_plan.schema.json`)
- Entrée dans SESSION_LOG.md
- Entrée dans memory/ si décision ou leçon nouvelle

## Validation Checklist

- [ ] AGENTS.md lu et résumé dans le log
- [ ] task_type classifié (bugfix | feature | review | audit | release | security | documentation)
- [ ] SCOPE.md validé : `in_scope: true`
- [ ] Plan d'orchestration produit avec agents, skills, tools, gates listés
- [ ] Gates G0-G1 passés avant toute exécution
- [ ] SESSION_LOG.md mis à jour en fin de session
- [ ] Aucun secret dans les outputs
- [ ] Aucun fichier protégé modifié sans ADR

## Rejection Criteria

- task_type non classifié → REJECTED
- SCOPE.md indique `in_scope: false` → REJECTED
- Aucun plan d'orchestration produit → BLOCKED
- Gate G0 non passé (description < 5 mots) → REJECTED
- Secret détecté dans output → BLOCKED_BY_SECURITY

## Related Directives

- `directives/09_AGENT_SYSTEM.md` — règles système agent
- `directives/20_GOVERNANCE.md` — gouvernance et décisions
- `orchestration/ROUTING.md` — table de routage complète
- `orchestration/STATE_MACHINE.md` — états de tâche

## Evidence Required

- Log de bootstrap (AGENTS.md lu)
- Plan d'orchestration JSON (chemin vers artifact)
- Résultat Gate G0 + G1
- Entrée SESSION_LOG.md (timestamp + outcome)
