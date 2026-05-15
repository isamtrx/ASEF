# CURRENT_SPRINT.md — ASEF

> État du sprint en cours.  
> 1 responsabilité : objectif, tâches et critères de fin du sprint actuel.  
> Dépend de : BACKLOG.md  
> Ne doit jamais contenir : backlog long terme (→ BACKLOG.md), historique des sprints (→ SESSION_LOG.md).

---

## Sprint 0 — Bootstrap documentaire

**Période :** 2026-05-15  
**Objectif :** Produire l'architecture documentaire complète d'ASEF (55 fichiers opérationnels).

---

## Tâches engagées

| ID | Tâche | Status | Commentaire |
|----|-------|--------|------------|
| S0-001 | Créer les 8 fichiers racine | ✓ Fait | README, PROJECT, SCOPE, AGENTS, MEMORY, DECISIONS, CHANGELOG, SESSION_LOG |
| S0-002 | Créer CLAUDE.md et copilot-instructions.md | ✓ Fait | Bootstrap 7 étapes, règles, interdictions |
| S0-003 | Créer les 6 instructions domaine | ✓ Fait | frontend, backend, qa, security, docs, ai |
| S0-004 | Créer docs/ARCHITECTURE.md | ✓ Fait | Modules, flux, contraintes |
| S0-005 | Créer Layer 4 — Qualité (6 fichiers) | ✓ Fait | QA, QUALITY_GATES, CONTROL_MATRIX, EVIDENCE, EXCEPTIONS, AUDIT |
| S0-006 | Créer Layer 5 — Gouvernance (6 fichiers) | ✓ Fait | GOVERNANCE, OPERATING_MODEL, SDLC, STANDARDS, ENGINEERING_HANDBOOK, SERVICE_CATALOG |
| S0-007 | Créer Layer 6 — Sécurité (8 fichiers) | ✓ Fait | SECURITY, APPSEC, THREAT_MODEL, SUPPLY_CHAIN, OPEN_SOURCE_POLICY, SECRETS, ACCESS_CONTROL, INCIDENT_RESPONSE |
| S0-008 | Créer Layer 7 — Gouvernance IA (6 fichiers) | ✓ Fait | AI_GOVERNANCE, MODEL_POLICY, PROMPT_GOVERNANCE, EVALS, AGENT_REGISTRY, TOOL_REGISTRY |
| S0-009 | Créer Layer 8 — Delivery (9 fichiers) | ✓ Fait | BRANCHING, CI_CD, DEPLOYMENT, RELEASE_MANAGEMENT, CHANGE_CONTROL, RUNBOOK, OBSERVABILITY, SLO, SUPPORT |
| S0-010 | Créer Layer 9 — Mémoire/Histoire | ✓ Fait | PRODUCT, ROADMAP, BACKLOG, CURRENT_SPRINT, LESSONS_LEARNED, POSTMORTEMS |
| S0-011 | Créer docs secondaires | ✓ Fait | DATA, API, INTEGRATIONS, REPOSITORY_STRATEGY, ADR-template |
| S0-012 | Valider et finaliser MEMORY.md | ✓ Fait | Mise à jour état final + corrections audit multi-agents |

---

## Tâches refusées (hors sprint 0)

- Implémentation réelle des scripts CI (→ Sprint 1)
- Configuration GitHub Actions réelle (→ Sprint 1)
- Projet exemple (→ Sprint 1)

---

## Critères de fin du sprint

- [x] 64 fichiers créés (55 gouvernance + 9 support)
- [x] Aucun fichier dépasse 400 lignes
- [x] CHANGELOG.md mis à jour
- [x] MEMORY.md mis à jour
- [x] SESSION_LOG.md entrée ajoutée

**Sprint 0 : FERMÉ — 2026-05-15**

---

## Risques du sprint

| Risque | Mitigation |
|--------|-----------|
| Duplication de contenu entre fichiers | Principe 1-fichier-1-responsabilité appliqué + vérification finale |
| Dépassement des 400 lignes | Contrôle par lecture avant finalisation |
