# SERVICE_CATALOG.md — ASEF

> Catalogue des services proposés par ASEF.  
> 1 responsabilité : décrire chaque service avec ses contrats, préconditions, contrôles et limites.  
> Dépend de : OPERATING_MODEL.md, QUALITY_GATES.md  
> Ne doit jamais contenir : implémentation technique, code source.

---

## Principe

Un service ASEF est un ensemble de capacités offertes par le framework, invocables par des agents ou des humains, avec des contrats clairs.

---

## S-01 — Génération de code gouvernée

**Description :** Génération de code source par un agent IA avec gates de qualité automatiques.

| Champ | Valeur |
|-------|--------|
| Input | DoD rédigé + contexte technique (ARCHITECTURE.md, STANDARDS.md) |
| Output | Fichiers de code + tests unitaires + rapport lint |
| Préconditions | G0 et G1 verts · Contexte architecture chargé |
| Contrôles | G3 (lint) + G4 (tests) + G5 (SAST) automatiques |
| Preuves | Rapport lint propre + rapport tests JUnit + rapport SAST |
| Limite | Pas de génération hors scope · Pas de décision structurante sans ADR |

---

## S-02 — Validation qualité (QA pipeline)

**Description :** Exécution complète du pipeline de tests et génération de l'evidence package.

| Champ | Valeur |
|-------|--------|
| Input | Codebase sur une branche + configuration CI |
| Output | Evidence package complet (tests, coverage, SAST, audit) |
| Préconditions | Code buildable · Tests configurés |
| Contrôles | G3 + G4 + G5 complets |
| Preuves | Artifacts CI : JUnit XML, coverage HTML, SAST JSON, audit JSON |
| Limite | Ne valide pas la sémantique fonctionnelle, seulement les critères formels |

---

## S-03 — Revue sécurité

**Description :** Analyse de sécurité du code et des dépendances.

| Champ | Valeur |
|-------|--------|
| Input | Code source + manifestes de dépendances |
| Output | Rapport SAST JSON + rapport audit + recommandations |
| Préconditions | Code dans le repo · Outils SAST configurés (Semgrep) |
| Contrôles | SAST + dependency audit + secret scan |
| Preuves | Rapport SAST (0 HIGH/CRIT) + audit propre + secret scan propre |
| Limite | Ne remplace pas un pentest · Auth/authz requiert revue humaine |

---

## S-04 — Génération et mise à jour de documentation

**Description :** Création et mise à jour de la documentation technique et gouvernance.

| Champ | Valeur |
|-------|--------|
| Input | Changement à documenter + fichiers sources de vérité |
| Output | Fichiers markdown mis à jour (CHANGELOG, SESSION_LOG, ADR, etc.) |
| Préconditions | Changement identifié · Sources de vérité lues |
| Contrôles | G6 (documentation) · Vérification liens |
| Preuves | Diff fichiers markdown + vérification liens propre |
| Limite | Ne crée pas de contenu dupliqué · Respecte la règle 1-fichier-1-responsabilité |

---

## S-05 — Évaluation des agents IA

**Description :** Test et validation des prompts et du comportement des agents IA.

| Champ | Valeur |
|-------|--------|
| Input | Prompts versionnés + jeu de test (docs/ai/EVALS.md) |
| Output | Score d'évaluation JSON + rapport détaillé |
| Préconditions | Jeu de test défini · Prompts versionnés dans PROMPT_GOVERNANCE.md |
| Contrôles | Score ≥ seuil défini dans EVALS.md |
| Preuves | Rapport evals JSON archivé |
| Limite | Évalue les critères définis, pas la créativité ou la pertinence subjective |

---

## S-06 — Gestion des exceptions

**Description :** Traitement formel des écarts aux quality gates.

| Champ | Valeur |
|-------|--------|
| Input | Gate bloquant + justification humaine |
| Output | Exception tracée dans EXCEPTIONS.md avec date d'expiration |
| Préconditions | Validation humaine explicite (Tech Lead minimum) |
| Contrôles | Format ADR exception respecté · Date expiration ≤ 30j |
| Preuves | Entrée EXCEPTIONS.md signée + ticket associé |
| Limite | Pas d'exception permanente · Pas d'exception sur G5 > 7j |

---

## S-07 — Release management

**Description :** Préparation et validation d'une release production.

| Champ | Valeur |
|-------|--------|
| Input | main stable + evidence package G0-G6 complet |
| Output | Tag Git versionné + CHANGELOG versionnée + release déployée |
| Préconditions | G0-G6 tous verts · Evidence package complet |
| Contrôles | Gate 7 (validation humaine) |
| Preuves | Approbation PR + sign-off humain tracé + tag Git |
| Limite | Humain obligatoire · Rollback plan requis |

---

## Catalogue — Index

| ID | Service | Qui peut l'invoquer | Gate requis |
|----|---------|--------------------|----|
| S-01 | Génération de code | Agent developer | G0, G1 |
| S-02 | Validation qualité | Agent QA, CI | G3, G4, G5 |
| S-03 | Revue sécurité | Agent security, CI | G5 |
| S-04 | Documentation | Agent docs | G6 |
| S-05 | Évaluation agents | Agent QA | G4 étendu |
| S-06 | Gestion exceptions | Humain + Agent | Toujours |
| S-07 | Release management | Humain | G7 |
