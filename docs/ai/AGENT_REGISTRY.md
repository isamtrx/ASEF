# AGENT_REGISTRY.md — ASEF

> Catalogue de tous les agents IA actifs dans ASEF.  
> 1 responsabilité : documenter chaque agent avec ses entrées, sorties, permissions et limites.  
> Dépend de : AGENTS.md, AI_GOVERNANCE.md, TOOL_REGISTRY.md  
> Ne doit jamais contenir : définitions des outils (→ TOOL_REGISTRY.md), prompts (→ PROMPT_GOVERNANCE.md).

---

## Format d'un agent

```markdown
## [ID] — [Nom]

| Champ | Valeur |
|-------|--------|
| Rôle | [Description courte] |
| Modèle | [Modèle utilisé] |
| Prompt | [Référence PROMPT_GOVERNANCE.md] |
| Input | [Ce qu'il reçoit] |
| Output | [Ce qu'il produit] |
| Permissions | [Actions autorisées] |
| Outils | [Outils TOOL_REGISTRY.md autorisés] |
| Limites | [Ce qu'il ne peut pas faire] |
| HITL requis | [Oui/Non + quand] |
```

---

## AGENT-000 — Orchestrateur

| Champ | Valeur |
|-------|--------|
| Rôle | Coordination du workflow ASEF entre agents, séquencement des STEP 0-7 |
| Modèle | Claude Sonnet 4.x / GitHub Copilot (selon environnement) |
| Prompt | — (rôle humain assisté par LLM, pas d'agent autonome) |
| Input | DoD + contexte projet + AGENTS.md |
| Output | Plan d'exécution séquencé, délégation aux agents spécialisés, rapport de session |
| Permissions | Lecture totale · Délégation aux rôles developer, qa, security, docs · Écriture SESSION_LOG.md, MEMORY.md |
| Outils | Tous les outils de lecture + invocation d'agents |
| Limites | Ne code pas directement · Ne valide pas les gates lui-même · Toute décision structurante → HITL |
| HITL requis | Oui — l'orchestrateur humain reste le responsable final de chaque gate |

**Note :** L'orchestrateur est principalement un rôle humain (Tech Lead) assisté par un LLM. Il n'est pas un agent autonome. Son rôle est de maintenir la cohérence du workflow ASEF, d'activer les bons agents au bon moment, et d'assurer les transitions (handoffs) entre étapes.

Voir le protocole de handoff dans `docs/ai/AI_GOVERNANCE.md §Protocole de handoff`.

---

## AGENT-001 — Developer

| Champ | Valeur |
|-------|--------|
| Rôle | Génération et modification de code source |
| Modèle | Claude Sonnet 4.x |
| Prompt | PROMPT-001 |
| Input | DoD validé + contexte ARCHITECTURE.md + standards |
| Output | Fichiers de code + tests unitaires |
| Permissions | Lire tout le repo, écrire du code, créer/modifier fichiers non-gouvernance |
| Outils | read_file, write_file, grep_search, run_tests |
| Limites | Ne peut pas modifier AGENTS.md, SCOPE.md, merger sur main |
| HITL requis | Non pour le code courant · Oui pour architecture ou sécurité |

---

## AGENT-002 — Security Reviewer

| Champ | Valeur |
|-------|--------|
| Rôle | Analyse de sécurité du code et des dépendances |
| Modèle | Claude Sonnet 4.x |
| Prompt | PROMPT-002 |
| Input | Code source + manifestes de dépendances |
| Output | Rapport SAST + liste de recommandations |
| Permissions | Lecture seule sur le code source |
| Outils | read_file, grep_search, run_sast, run_audit |
| Limites | Ne peut pas modifier de fichiers · Ne décide pas des exceptions |
| HITL requis | Oui — ses recommandations doivent être validées par humain avant action |

---

## AGENT-003 — Documentation Writer

| Champ | Valeur |
|-------|--------|
| Rôle | Création et mise à jour de documentation |
| Modèle | Claude Sonnet 4.x |
| Prompt | PROMPT-003 |
| Input | Changements à documenter + fichiers de gouvernance existants |
| Output | Fichiers Markdown mis à jour (CHANGELOG, SESSION_LOG, ADR) |
| Permissions | Lire et écrire les fichiers markdown |
| Outils | read_file, write_file, grep_search |
| Limites | Ne peut pas modifier AGENTS.md · Ne peut pas prendre de décision structurante |
| HITL requis | Non pour la doc courante · Oui pour ADR et DECISIONS.md |

---

## AGENT-004 — QA Tester

| Champ | Valeur |
|-------|--------|
| Rôle | Exécution des tests et génération du rapport d'evidence |
| Modèle | Claude Sonnet 4.x |
| Prompt | — (pipeline CI principalement) |
| Input | Codebase + configuration de tests |
| Output | Rapport tests JUnit + rapport coverage + rapport evals |
| Permissions | Lecture code, exécution tests |
| Outils | read_file, run_tests, run_evals |
| Limites | Ne peut pas modifier le code de production |
| HITL requis | Non — les résultats sont des faits, la décision d'accepter reste humaine |

---

## AGENT-005 — Architect

| Champ | Valeur |
|-------|--------|
| Rôle | Propositions d'architecture et rédaction d'ADR |
| Modèle | Claude Sonnet 4.x |
| Prompt | — |
| Input | Contexte projet + ARCHITECTURE.md + contraintes |
| Output | Proposition technique + ADR rédigé (non signé) |
| Permissions | Lecture tout le repo |
| Outils | read_file, grep_search, semantic_search |
| Limites | Ne décide pas seul — propose uniquement · ADR doit être validé par humain |
| HITL requis | Toujours — aucune décision architecturale sans validation Tech Lead |

---

## AGENT-006 — Reviewer

| Champ | Valeur |
|-------|--------|
| Rôle | Validation des changements avant merge — approve ou refuse avec justification |
| Modèle | Claude Sonnet 4.x |
| Prompt | — (à définir — voir BACKLOG Sprint 1) |
| Input | Diff de code ou documentation + DoD + quality gates |
| Output | Verdict (Approved / Request Changes) + liste des non-conformités |
| Permissions | Lecture totale du repo · Approbation ou refus de PR (droit de blocage) |
| Outils | read_file, grep_search, get_errors, run_tests |
| Limites | Ne modifie pas de fichiers · Ne fait pas les corrections lui-même · Pas d'auto-approbation |
| HITL requis | Toujours — son verdict est une recommandation ; le merge reste une décision humaine |

**Note :** Rôle défini dans AGENTS.md §1. Ce registre étend la définition avec les champs opérationnels. Tant que le prompt n'est pas rédigé et évalué, ce rôle est exercé manuellement par le Tech Lead.

---

## Agents désactivés / archivés

_(Aucun pour l'instant — registre initialisé à la création d'ASEF v0.1.0)_

---

## Ajout d'un nouvel agent

Processus avant de déployer un nouvel agent :
1. Définir le prompt dans PROMPT_GOVERNANCE.md
2. Créer le jeu de test dans EVALS.md
3. Passer les evals (score ≥ seuil)
4. Ajouter l'entrée dans ce registre
5. Valider les permissions avec Tech Lead
6. ADR si l'agent a des permissions nouvelles ou étendues
