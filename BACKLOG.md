# BACKLOG.md — ASEF

> Backlog des tâches et fonctionnalités planifiées.  
> 1 responsabilité : liste priorisée des items à développer.  
> Dépend de : ROADMAP.md, PRODUCT.md  
> Ne doit jamais contenir : sprint en cours (→ CURRENT_SPRINT.md), décisions (→ DECISIONS.md).

---

## Légende

| Priorité | Description |
|---------|-------------|
| P0 | Bloquant — doit être résolu avant toute autre chose |
| P1 | Critique — sprint prochain |
| P2 | Important — dans les 2 sprints |
| P3 | Souhaitable — backlog long terme |

| Complexité | Estimation |
|---------|-------------|
| XS | < 2h |
| S | 2h — 1j |
| M | 1j — 3j |
| L | 3j — 1 semaine |
| XL | > 1 semaine |

---

## Backlog Phase 1 — Activation (v0.2.x)

| ID | Titre | Priorité | Complexité | UC lié | Critère d'acceptation |
|----|-------|---------|-----------|--------|----------------------|
| B-001 | Créer le projet exemple d'application ASEF | P1 | M | UC-001 | Projet avec ASEF appliqué, CI qui passe |
| B-002 | Configurer GitHub Actions CI réel | P1 | M | UC-002 | Pipeline lint+test+sast vert sur main |
| B-003 | Configurer Semgrep en CI | P1 | S | UC-002 | Rapport SAST généré, findings visibles |
| B-004 | Configurer Gitleaks en CI | P1 | S | — | Scan secret actif sur chaque PR |
| B-005 | Créer npm scripts de base (validate, clean) | P1 | XS | UC-001 | `npm run validate` passe |
| B-006 | Configurer branch protection sur main | P1 | XS | — | Push direct rejeté |
| B-007 | Écrire le premier ADR réel | P2 | S | — | ADR-0004 dans DECISIONS.md |
| B-008 | Configurer les instructions VS Code Copilot | P2 | S | UC-001 | instructions.md actif, testé |

---

## Backlog Phase 2 — Evals (v0.3.x)

| ID | Titre | Priorité | Complexité | UC lié | Critère d'acceptation |
|----|-------|---------|-----------|--------|----------------------|
| B-101 | Créer le runner d'evals Python | P1 | L | UC-102 | `python scripts/run_evals.py` fonctionnel |
| B-102 | Implémenter EVAL-001 (génération code) | P1 | M | UC-102 | Score affiché en CI |
| B-103 | Implémenter EVAL-002 (revue sécurité) | P2 | M | UC-102 | Score affiché en CI |
| B-104 | Créer l'audit log agent JSON | P1 | M | UC-003 | Entrées JSON dans logs avec tous les champs |
| B-105 | Dashboard observabilité simple | P2 | L | UC-101 | SLOs visibles dans interface web |
| B-106 | Métriques agentiques (Prometheus) | P2 | L | — | `agent_actions_total` exposé |

---

## Backlog Phase 3 — Enterprise (v1.0.x)

| ID | Titre | Priorité | Complexité | UC lié | Critère d'acceptation |
|----|-------|---------|-----------|--------|----------------------|
| B-201 | Rapport de conformité exportable PDF | P2 | XL | UC-103 | PDF généré avec evidence package |
| B-202 | SLO avec budget d'erreur et alertes | P2 | L | — | Alertes actives selon SLO.md |
| B-203 | RBAC granulaire par agent | P3 | XL | — | Permissions configurables par agent |

---

## Items refusés

| ID | Titre | Raison |
|----|-------|--------|
| BR-001 | Développer un LLM propriétaire | Hors périmètre SCOPE.md |
| BR-002 | Interface SaaS multi-tenant | Hors périmètre phase MVP |

---

## Règles du backlog

- Tout item a un critère d'acceptation mesurable
- Les items P0 sont traités en dehors du sprint normal
- Un item non touché depuis 90 jours est archivé ou supprimé
- Les items dépendants sont liés explicitement (voir `Dépend de :` colonne si complexe)
