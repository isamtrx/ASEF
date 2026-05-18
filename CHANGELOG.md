# Changelog — ASEF

> Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
> Versioning : [Semantic Versioning](https://semver.org/lang/fr/)  
> 1 responsabilité : historique des versions livrées.  
> Ne pas y mettre : sessions, backlog, décisions architecturales.

---

## [Unreleased]

### Added
- `HEARTBEAT.md` — Fichier de santé projet (détection contexte périmé > 7j)
- `BRIEF.md` — Capsule de fin de session (lue au début de la session suivante)
- `orchestration/WORKFLOW_TRIGGER_INDEX.md` — Routing O(1) task_type → workflow → agents
- `.agent/rules/IDENTITY.rule.md` — Identité agent stable anti-dérive
- `.agent/rules/SOUL.rule.md` — 8 principes de décision en cas de règles absentes
- `.agent/rules/ROLE_BOUNDARIES.rule.md` — Matrice permissions écriture par rôle (référence D-0004)
- `.agent/rules/CORE_REFLEXES.rule.md` — 8 réflexes automatiques (REFLEX-001 à 008)
- `.agent/rules/CONFLICT_RESOLUTION.rule.md` — Résolution conflit rôle/règle (hiérarchie 5 niveaux)
- `.agent/rules/SKILL_CATALOGUE_POLICY.rule.md` — Gouvernance ajout/deprecation des skills
- `directives/21_SESSION_START.md` — Bootstrap de session (STEPS 1-6)
- `directives/22_SESSION_END.md` — Fermeture de session (checklist STEPS 1-6)
- `directives/23_SESSION_END_CRITICAL.md` — Récupération après session interrompue
- `directives/24_MISSION_FIRST.md` — Mission obligatoire avant tout livrable > 3 fichiers / 100 lignes
- `directives/25_DOD_FIRST_DELIVERY.md` — DoD ≤ 8 lignes avant exécution
- `directives/26_VERIFICATION_LOOP.md` — Preuves obligatoires pour chaque déclaration "done"
- `directives/27_WEB_RESEARCH_POLICY.md` — Hiérarchie outils web (browser > search > fetch_webpage)
- `directives/28_STOP_LIST.md` — 8 conditions d'arrêt immédiat
- `directives/29_SUBAGENT_DISPATCH.md` — Dispatch composite (équipe) vs dispatch solo
- `directives/30_CONTEXT_BUDGET.md` — Gestion budget tokens fenêtre de contexte
- `directives/31_ESCALATION_PROTOCOL.md` — Format et protocole escalade humaine
- `skills/bootstrap_check.skill.md` — Vérification bootstrap complet
- `skills/session_close.skill.md` — Fermeture propre de session
- `skills/scope_check.skill.md` — Vérification IN/OUT SCOPE
- `skills/dod_formulation.skill.md` — Formulation DoD avant livrable
- `skills/escalation_report.skill.md` — Rapport structuré d'escalade
- `agents/REVIEWER.agent.md` — Agent revue et approbation de changements
- `agents/ADR_WRITER.agent.md` — Agent rédaction ADR conformes ASEF
- `agents/CHANGELOG_MANAGER.agent.md` — Agent maintenance CHANGELOG

### Changed
- `.github/copilot-instructions.md` — Bloc ⚡ BOOTSTRAP ajouté en première section
- `.github/instructions/session_start.instructions.md` — Créé (applyTo: "**")
- `DECISIONS.md` — D-0004 ajouté (contrainte écriture orchestrator)
- `skills/SKILLS.md` — 5 nouveaux skills indexés (11 total)


  - `ASEF-HITL.md` (13 triggers HITL, format notification, comportement pipeline)
  - `ASEF-Workflow.md` (statuts, WF-INTAKE, WF-EXECUTION)
  - `ASEF-Decision.md` (6 types, format ADR et EXCEPTION, DecisionAgent)
  - `ASEF-AgentGov.md` (cycle de vie, contrat agent, matrice permissions)
  - `ASEF-Audit.md` (14 questions fondamentales, 5 types d'audit)
  - `README.md` (index des 10 frameworks + règle d'héritage)
- `context/` — Gestion du contexte agent :
  - `CONTEXT_BUDGET.md` (budgets tokens par type de tâche)
  - `CONTEXT_LOADING.md` (séquence bootstrap 7 étapes)
  - `CONTEXT_PRIORITY.md` (ordre de priorité 10 niveaux, résolution conflits)
- `missions/` — Structure cycle de vie des missions :
  - `missions/active/README.md` (format, convention, règles)
  - `missions/completed/README.md` (format archivage avec evidence)
  - `missions/blocked/README.md` (format blocage avec gate + HITL)
  - `missions/archived/README.md` (format annulation avec justification)
- `playbooks/` — 7 playbooks opérationnels :
  - `create-new-framework.md` (5 phases, cadrage → validation)
  - `produce-evidence-package.md` (6 étapes, anti-hallucination)
  - `run-go-no-go.md` (5 étapes, HITL, DECISIONS.md)
  - `run-maturity-assessment.md` (5 niveaux, scoring 55 points)
  - `improve-framework.md` (gap analysis, ADR, validation)
  - `specialize-framework.md` (héritage ASEF-Core, domain layer)
  - `use-copilot-cli-for-patch.md` (règles chirurgicales, validation)
- `evaluations/MISSION_SCORECARD.md` — Grille 20 points, seuils ACCEPTED/PARTIAL/REJECTED
- `domains/software/ASEF-QA/README.md` — Framework QA avec 4 agents et 2 workflows

---

## [0.1.0] — 2026-05-15

### Added
- Architecture documentaire ASEF complète — 55 fichiers opérationnels sur 9 couches
- **Layer 1 — Racine** : README, PROJECT, SCOPE, AGENTS, MEMORY, DECISIONS, CHANGELOG, SESSION_LOG
- **Layer 2 — Instructions agent** : CLAUDE.md, copilot-instructions.md, 6 fichiers domaine (frontend/backend/qa/security/docs/ai)
- **Layer 3 — Architecture** : docs/ARCHITECTURE.md
- **Layer 4 — Qualité** : QA, QUALITY_GATES (G0-G7), CONTROL_MATRIX, EVIDENCE, EXCEPTIONS, AUDIT
- **Layer 5 — Gouvernance** : GOVERNANCE, OPERATING_MODEL, SDLC, STANDARDS, ENGINEERING_HANDBOOK, SERVICE_CATALOG
- **Layer 6 — Sécurité** : SECURITY, APPSEC, THREAT_MODEL, SUPPLY_CHAIN, OPEN_SOURCE_POLICY, SECRETS, ACCESS_CONTROL, INCIDENT_RESPONSE
- **Layer 7 — Gouvernance IA** : AI_GOVERNANCE, MODEL_POLICY, PROMPT_GOVERNANCE, EVALS, AGENT_REGISTRY, TOOL_REGISTRY
- **Layer 8 — Delivery** : BRANCHING, CI_CD, DEPLOYMENT, RELEASE_MANAGEMENT, CHANGE_CONTROL, RUNBOOK, OBSERVABILITY, SLO, SUPPORT
- **Layer 9 — Mémoire** : PRODUCT, ROADMAP, BACKLOG, CURRENT_SPRINT, LESSONS_LEARNED, POSTMORTEMS
- **Docs secondaires** : DATA, API, INTEGRATIONS, REPOSITORY_STRATEGY, docs/adr/ADR-0001-template.md

### Changed
- `CLAUDE.md` mis à jour depuis scaffold vers adaptateur ASEF (7 étapes bootstrap)
- `MEMORY.md` mis à jour pour refléter l'état final MVP

---

## [0.0.1] — 2026-05-15

### Added
- Initialisation du workspace ASEF
- `CLAUDE.md` scaffold initial (via KERN scaffold_project.ps1)
