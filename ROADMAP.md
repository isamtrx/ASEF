# ROADMAP.md — ASEF

> Source de vérité de la feuille de route.  
> 1 responsabilité : phases, jalons et livraisons planifiées.  
> Dépend de : PROJECT.md, PRODUCT.md, BACKLOG.md  
> Ne doit jamais contenir : backlog détaillé (→ BACKLOG.md), décisions structurantes (→ DECISIONS.md).

---

## Phase actuelle : MVP Foundation

**Objectif :** Poser une architecture documentaire complète, opérationnelle et gouvernée qui peut être adoptée par une équipe.

**Status :** En cours — v0.1.0

---

## Phase 0 — Bootstrap documentaire (v0.1.0)

**Objectif :** 55 fichiers de gouvernance opérationnels, aucun placeholder.

| Livrable | Status |
|---------|--------|
| Architecture documentaire 9 couches | ✓ Complète |
| AGENTS.md constitution multi-agents | ✓ |
| Quality Gates G0-G7 | ✓ |
| Sécurité complète (8 fichiers) | ✓ |
| Gouvernance IA (6 fichiers) | ✓ |
| Delivery pipeline (9 fichiers) | ✓ |
| Instructions domaine (6 fichiers) | ✓ |

**Jalons :**
- [x] 2026-05-15 : Session de création initiale — 18 fichiers
- [x] 2026-05-15 : Session de complétion — 55 fichiers cible

---

## Phase 1 — Activation (v0.2.0)

**Objectif :** ASEF utilisé sur un premier projet réel. Validation des gates en CI réel.  
**Cible :** Q3 2026 (jalon : premier pipeline CI vert sur projet exemple)

| Livrable | Status |
|---------|--------|
| Projet exemple avec ASEF appliqué | À faire |
| Pipeline GitHub Actions opérationnel | À faire |
| Premier rapport de coverage réel | À faire |
| Premier rapport SAST réel (Semgrep) | À faire |
| Dashboard observabilité basique | À faire |

**Dépendances :**
- Projet cible identifié
- Tokens CI/secrets configurés

---

## Phase 2 — Evals et Observabilité (v0.3.0)

**Objectif :** Les prompts sont testés automatiquement. Les métriques agent sont visibles.  
**Cible :** Q4 2026 (jalon : premier rapport eval en CI, métriques OTel visibles)

| Livrable | Status |
|---------|--------|
| Runner d'evals automatisé | À faire |
| Rapport evals en CI | À faire |
| Audit log agent en JSON | À faire |
| Dashboard agent activity | À faire |
| HITL workflow formalisé | À faire |

---

## Phase 3 — Enterprise Ready (v1.0.0)

**Objectif :** ASEF applicable dans un contexte enterprise avec conformité, RBAC et rapports.  
**Cible :** Q2 2027 (jalon : premier audit de conformité externe réussi)

| Livrable | Status |
|---------|--------|
| Rapport de conformité exportable | À faire |
| SLOs avec budget d'erreur actif | À faire |
| RBAC granulaire par agent | À faire |
| Intégration LDAP/SSO (optionnel) | À faire |
| Documentation multi-équipe | À faire |

---

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Adoption faible par les devs | Moyen | Élevé | Onboarding simple, gain mesurable |
| Drift entre la gouvernance et la pratique | Élevé | Élevé | AUDIT.md mensuel |
| Modèles IA changent d'API | Moyen | Moyen | Abstraction MODEL_POLICY.md |
| Faux positifs SAST excessifs | Élevé | Moyen | Tuning rules Semgrep |

---

## Hors roadmap (décidé)

Ces éléments ne sont pas dans la roadmap ASEF — ils peuvent être dans des projets dérivés :

- Développement d'un LLM propriétaire
- Plateforme SaaS ASEF multi-tenant
- Plugin IDE custom ASEF
- Certification officielle ASEF

_Source : SCOPE.md §Hors périmètre_
