# PROJECT.md — ASEF

> Source de vérité du **pourquoi** d'ASEF.  
> 1 responsabilité : Mission · Vision · Principes · Succès.

---

## Mission

Permettre à toute organisation de transformer l'usage des agents IA dans le développement logiciel en un processus maîtrisé, contrôlé, auditable et industrialisable — sans sacrifier la vitesse au profit du contrôle, ni le contrôle au profit de la vitesse.

## Vision

ASEF est le référentiel de facto pour construire une software factory IA gouvernable : applicable par une équipe de 2 développeurs comme par une DSI de 500 personnes.

## Problème résolu

| Problème actuel | Impact |
|----------------|--------|
| Agents IA sans permissions définies | Excessive agency, surface d'attaque non contrôlée |
| Prompts ad-hoc sans versioning | Comportements non reproductibles, non auditables |
| Code généré sans quality gates | Dette technique invisible, bugs en production |
| Documentation sans frontières | Duplication, contradictions, perte de confiance |
| Absence d'audit trail IA | Conformité réglementaire impossible |
| Vibe coding non gouverné | Impossible à maintenir, impossible à auditer |

## Promesse

Un développeur, un tech lead, un CTO et un auditeur de conformité peuvent tous travailler dans ASEF avec un référentiel commun, des preuves vérifiables et une chaîne de responsabilité claire.

## Cibles utilisateurs

| Persona | Besoin principal ASEF |
|---------|----------------------|
| Développeur | Savoir exactement quoi faire et comment le prouver |
| Tech Lead | Cadrer l'usage IA sans bloquer la productivité |
| CTO | Gouvernance IA visible, décisions tracées |
| DSI | Conformité, audit trail, contrôle des accès |
| Security Officer | Threat model, supply chain, incident response |
| QA Lead | Quality gates bloquants, preuves automatisées |
| Product Owner | Scope clair, roadmap pilotable |
| Platform Engineer | Standards, CI/CD, observabilité |

## Différenciation

| Concurrent (approche) | ASEF |
|----------------------|------|
| Vibe coding (génère et espère) | Engineering gouverné avec preuves |
| Wrapper LLM (prompts = produit) | Framework d'engineering complet |
| Outils IDE seuls | Couche gouvernance + delivery + sécurité |
| Documentation théorique | 1 fichier = 1 responsabilité opérationnelle |

## Principes fondateurs

1. **1 fichier = 1 responsabilité = 1 source de vérité.** Pas de duplication. Pas de décoration.
2. **Pas de livraison sans preuves.** Chaque changement doit avoir un trail vérifiable.
3. **Human-in-the-loop non négociable** sur les décisions structurantes et les releases critiques.
4. **Les agents ont des permissions déclarées.** Ce qui n'est pas autorisé est interdit.
5. **Le périmètre est un contrat.** Toute dérive doit être arbitrée explicitement.
6. **La sécurité est un quality gate, pas un audit post-livraison.**
7. **La mémoire se gère.** `MEMORY.md` = état actuel. `CHANGELOG.md` = passé. Jamais les deux mélangés.
8. **Les erreurs deviennent des règles.** `LESSONS_LEARNED.md` est un artefact de production.

## Objectifs mesurables

| Objectif | Seuil MVP | Seuil Entreprise |
|----------|-----------|-----------------|
| Quality gates automatisés | ≥ 5/8 | 8/8 |
| Couverture documentation | 22 fichiers MVP | 55 fichiers complets |
| Temps de bootstrap agent | < 5 min | < 2 min |
| Audit trail complet sur une tâche | Oui | Oui + signature |
| Détection prompt injection | Déclarative | Automatisée |

## Non-objectifs

- ASEF ne génère pas de code à votre place — il gouverne comment ce code est généré et validé.
- ASEF n'est pas un orchestrateur LLM technique (pas de runtime, pas d'API propre).
- ASEF ne remplace pas vos outils CI/CD — il s'y intègre.
- ASEF n'impose pas un LLM spécifique — il encadre leur usage.

## Risques existentiels

| Risque | Mitigation |
|--------|-----------|
| Devenir un système de prompts déguisé | Règle R1-R8 non-redondance + audit documentaire |
| Documentation décorative sans usage | Chaque fichier doit servir un des 10 objectifs ASEF |
| Dérive de scope | `SCOPE.md` est un contrat, pas une suggestion |
| Agent sans contrôle | `AGENTS.md` définit les permissions avant toute tâche |
| Fausse conformité | Evidence package requis, pas de déclaration sans preuve |

## Définition du succès

**MVP :** Un agent peut bootstrapper, exécuter et livrer une tâche complète (de la demande à la preuve) en suivant uniquement ASEF, sans instruction ad-hoc.

**Entreprise :** Un auditeur externe peut reconstituer l'historique complet d'une livraison (qui a demandé, quel agent a fait quoi, quels tests ont passé, quelle validation humaine a eu lieu) depuis les artefacts ASEF seuls.

**Régulé :** ASEF satisfait les exigences d'un audit SOC 2 Type II ou ISO 27001 sur le périmètre du développement assisté par IA.
