# Changelog — ASEF

> Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
> Versioning : [Semantic Versioning](https://semver.org/lang/fr/)  
> 1 responsabilité : historique des versions livrées.  
> Ne pas y mettre : sessions, backlog, décisions architecturales.

---

## [Unreleased]

### Added
- `MANIFEST.md` — Contrat public des 12 garanties ASEF (G-01 à G-12)
- `VISION.md` — Vision ASEF 2.0 : meta-framework universel, architecture 3 couches
- `core/` — 11 fichiers primitifs universels transverses à tout framework ASEF :
  - `ASEF-Core.md` (10 agents universels, pipeline G0-G9, règles d'extension)
  - `ASEF-Gates.md` (gates G0-G9 avec checklists et matrice de maturité)
  - `ASEF-Memory.md` (modèle mémoire systémique à 4 fichiers)
  - `ASEF-Evidence.md` (taxonomie de preuves, 7 types, format evidence package)
  - `ASEF-Risk.md` (9 catégories, scoring P×I 1-9, registre)
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
- `evaluations/mission_scorecard.md` — Grille 20 points, seuils ACCEPTED/PARTIAL/REJECTED
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
