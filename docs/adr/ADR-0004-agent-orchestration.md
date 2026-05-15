# ADR-0004 — Orchestration des agents : kern natif + GitHub Copilot

Date : 2026-05-15  
Statut : Validé  
Auteur : Platform Engineering

---

## Contexte

ASEF coordonne plusieurs agents IA (Developer, Security, QA, Architect, Docs — voir `docs/ai/AGENT_REGISTRY.md`). Un mécanisme d'orchestration est nécessaire pour :
- Séquencer les agents selon le workflow ASEF (STEP 0–7 dans AGENTS.md §5)
- Passer le contexte d'un agent au suivant (handoff)
- Maintenir la traçabilité des actions

Les options d'orchestration vont du framework LLM dédié à l'orchestration native dans l'IDE.

---

## Options considérées

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **kern (natif) + Copilot** | Déjà intégré dans la stack, pas d'infra, HITL naturel | Moins de parallélisme, pas de multi-agent simultané |
| LangGraph | Graphe d'agents, parallélisme | Infra Python, complexité, dépendance externe |
| CrewAI | Simple, rôles pré-définis | Framework tiers, moins de contrôle |
| AutoGen (Microsoft) | Conversation multi-agents | Verbeux, moins de contrôle sur les permissions |

---

## Décision

**Orchestration native** via kern (MCP) + GitHub Copilot dans VS Code. Pas de framework d'orchestration tiers à ce stade.

---

## Raison

- La stack kern + Copilot est déjà opérationnelle dans l'environnement ASEF
- L'orchestration est documentaire d'abord : le workflow AGENTS.md §5 (STEP 0–7) est l'orchestrateur logique
- L'humain joue naturellement le rôle d'orchestrateur pour les gates HITL (G7)
- Les frameworks LLM (LangGraph, CrewAI) ajoutent de la complexité et des dépendances sans gain mesurable à ce stade
- Cette décision est révisable dès la Phase 2 (evals + observabilité) quand le besoin de parallélisme sera prouvé

---

## Protocole d'orchestration retenu

1. L'humain (ou AGENT-000 Orchestrateur) décide l'ordre des agents
2. Chaque agent reçoit un contexte minimal suffisant (pas le repo entier)
3. Les outputs d'un agent sont validés avant d'être passés au suivant
4. La traçabilité est maintenue dans SESSION_LOG.md

Voir le protocole de handoff détaillé dans `docs/ai/AI_GOVERNANCE.md §Protocole de handoff`.

---

## Conséquences

**Positives :**
- Pas de dépendance framework tiers
- Contrôle total sur les permissions (AGENTS.md §3)
- HITL naturel à chaque étape

**Négatives :**
- Pas de parallélisme automatique entre agents
- Scalabilité limitée si le nombre d'agents augmente significativement

---

## Conditions de révision

Cette ADR est révisée si :
- Le besoin de >5 agents simultanés est démontré
- Un framework tiers offre une intégration native avec AGENTS.md et les quality gates
- La Phase 2 (evals) révèle un goulot d'étranglement d'orchestration

---

## Fichiers concernés

- `docs/ai/AGENT_REGISTRY.md` — liste des agents
- `docs/ai/AI_GOVERNANCE.md` — protocole de handoff
- `AGENTS.md §5` — workflow standard ASEF
