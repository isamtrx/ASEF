# Changelog — ASEF

> Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
> Versioning : [Semantic Versioning](https://semver.org/lang/fr/)  
> 1 responsabilité : historique des versions livrées.  
> Ne pas y mettre : sessions, backlog, décisions architecturales.

---

## [Unreleased]

_(Aucun changement en attente de release)_

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
