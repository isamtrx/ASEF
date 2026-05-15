# QUALITY_GATES.md — ASEF

> Source de vérité des portes de validation obligatoires.  
> 1 responsabilité : définir les critères bloquants de chaque gate.  
> Dépend de : docs/quality/QA.md  
> Ne doit jamais contenir : règles de style, procédures de release détaillées.

---

## Principe

Un gate bloquant = livraison impossible tant que le critère n'est pas satisfait.  
Il n'existe pas de "contournement silencieux". Toute exception doit être tracée dans `docs/quality/EXCEPTIONS.md`.

---

## Gate 0 — Intake recevable

**Objectif :** S'assurer que la demande est compréhensible, délimitable et in-scope avant tout travail.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Une demande a été soumise | Demande acceptée ET un DoD ≤ 8 lignes est défini |

**Contrôles obligatoires :**
- [ ] La demande est formulée clairement (pas ambiguë)
- [ ] La demande est IN scope (vérifier `SCOPE.md`)
- [ ] Un DoD avec critères mesurables est défini

**Bloquants :**
- Demande hors scope → refuser ou ouvrir une évolution de scope (ADR requis)
- Demande ambiguë sans possibilité de clarification → bloquer et escalader

**Responsable :** Humain (Product Owner / Tech Lead)  
**Mode :** Manuel  
**Preuves :** DoD écrit et validé

---

## Gate 1 — Scope validé

**Objectif :** Confirmer que l'implémentation prévue ne dépasse pas le scope défini.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| DoD défini (Gate 0 vert) | Plan d'implémentation approuvé, pas de dérive |

**Contrôles obligatoires :**
- [ ] Chaque point du DoD map vers un élément IN scope de `SCOPE.md`
- [ ] Aucune dépendance hors scope identifiée
- [ ] Si décision structurante : ADR rédigé dans `docs/adr/`

**Bloquants :**
- Le plan implique des changements hors scope non validés
- Une décision structurante est prise sans ADR

**Responsable :** Agent architect + validation humaine si structurant  
**Mode :** Mixte  
**Preuves :** Vérification SCOPE.md documentée, ADR si applicable

---

## Gate 2 — Architecture validée

**Objectif :** S'assurer que la solution technique respecte l'architecture définie.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Scope validé (Gate 1 vert) | Approche technique conforme à ARCHITECTURE.md |

**Contrôles obligatoires :**
- [ ] Approche cohérente avec `docs/ARCHITECTURE.md`
- [ ] Pas de nouvelle dépendance majeure sans validation
- [ ] Interfaces respectent les contrats définis dans `docs/API.md`
- [ ] Si nouvelle intégration : `docs/INTEGRATIONS.md` mis à jour

**Bloquants :**
- Violation de contrainte architecturale documentée
- Nouvelle dépendance externe sans validation SUPPLY_CHAIN

**Responsable :** Agent architect  
**Mode :** Auto (lint archi) + Manuel si structurant  
**Preuves :** Revue architecture documentée

---

## Gate 3 — Code conforme aux standards

**Objectif :** Vérifier que le code généré respecte les standards définis.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Architecture validée (Gate 2 vert) | Code propre, style conforme, pas de patterns interdits |

**Contrôles obligatoires :**
- [ ] Lint passe sans erreur (`npm run lint` ou équivalent)
- [ ] Types corrects — zéro `any` non justifié (TypeScript)
- [ ] Pas de patterns interdits (voir `docs/governance/ENGINEERING_HANDBOOK.md`)
- [ ] Pas de code mort (fonctions non utilisées, imports inutiles)
- [ ] Pas de TODO ou FIXME non tracés dans le code livré

**Bloquants :**
- Erreur de lint
- Pattern interdit détecté

**Responsable :** Agent developer + linter CI  
**Mode :** Automatique  
**Preuves :** Log lint propre

---

## Gate 4 — Tests passés

**Objectif :** Prouver que le code fonctionne et ne régresse pas.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Code conforme (Gate 3 vert) | Tous les tests passent, couverture suffisante |

**Contrôles obligatoires :**
- [ ] 0 test unitaire rouge
- [ ] 0 test d'intégration rouge
- [ ] 0 test E2E rouge (si applicable)
- [ ] Coverage ≥ 80% sur le périmètre modifié
- [ ] 0 violation WCAG CRITICAL (si changement UI)
- [ ] Score evals ≥ seuil (si changement IA)

**Bloquants :**
- Tout test rouge
- Coverage < 80% sur le périmètre modifié
- Test désactivé sans ticket

**Responsable :** Agent QA + CI  
**Mode :** Automatique  
**Preuves :** Rapport tests JUnit + rapport coverage HTML + rapport evals si IA

---

## Gate 5 — Sécurité validée

**Objectif :** Garantir qu'aucune vulnérabilité n'est introduite.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Tests passés (Gate 4 vert) | Analyse sécurité propre |

**Contrôles obligatoires :**
- [ ] SAST propre (0 finding HIGH ou CRITICAL) — Semgrep ou équivalent
- [ ] Dependency audit propre (0 vulnérabilité HIGH ou CRITICAL)
- [ ] Secret scan propre (0 secret détecté dans les fichiers modifiés)
- [ ] Si code généré par IA : audit du code généré inclus
- [ ] Si nouvelle dépendance : validation `docs/security/SUPPLY_CHAIN.md`
- [ ] Si changement auth/authz : revue humaine obligatoire

**Bloquants :**
- Tout finding SAST HIGH ou CRITICAL
- Toute vulnérabilité dépendance HIGH ou CRITICAL
- Secret détecté dans les fichiers

**Responsable :** Agent security + CI  
**Mode :** Automatique (SAST/audit/scan) + Manuel (auth/authz)  
**Preuves :** Rapport SAST JSON + rapport audit + rapport secret scan

---

## Gate 6 — Documentation à jour

**Objectif :** Garantir que la traçabilité documentaire est complète.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| Sécurité validée (Gate 5 vert) | Documentation et traçabilité complètes |

**Contrôles obligatoires :**
- [ ] `CHANGELOG.md` mis à jour (section Unreleased) pour tout changement livrable
- [ ] `SESSION_LOG.md` entrée ajoutée
- [ ] `DECISIONS.md` mis à jour si décision structurante prise
- [ ] ADR dans `docs/adr/` si décision architecturale
- [ ] Aucun lien cassé dans les fichiers modifiés

**Bloquants :**
- CHANGELOG.md sans entrée pour un changement livrable
- ADR manquant pour une décision structurante

**Responsable :** Agent docs  
**Mode :** Automatique (lint markdown) + Manuel (vérification contenu)  
**Preuves :** Diff CHANGELOG.md + vérification liens

---

## Gate 7 — Release autorisée

**Objectif :** Validation humaine finale avant livraison en production.

| Critère d'entrée | Critère de sortie |
|-----------------|------------------|
| G0 à G6 tous verts | Release approuvée et livrée |

**Contrôles obligatoires :**
- [ ] G0 à G6 tous verts (vérification automatique CI)
- [ ] Evidence package complet et accessible
- [ ] Validation humaine explicite (Tech Lead / CTO selon criticité)
- [ ] `CHANGELOG.md` section release finalisée
- [ ] Plan de rollback défini

**Bloquants :**
- N'importe quel gate G0-G6 non vert
- Evidence package incomplet
- Absence de validation humaine

**Responsable :** Humain (Tech Lead / CTO)  
**Mode :** Manuel  
**Preuves :** Approbation PR + signature release + evidence package archivé

---

## Matrice de criticité

| Type de changement | G0 | G1 | G2 | G3 | G4 | G5 | G6 | G7 |
|-------------------|----|----|----|----|----|----|----|----|
| Fix de bug mineur | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | — |
| Feature | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| Changement archi | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Release production | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Changement sécurité | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Doc uniquement | ✓ | — | — | — | — | — | ✓ | — |
