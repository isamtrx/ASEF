# VISION — Agentic Systemic Execution Framework

> Version 2.0 — Méta-framework agentique multi-domaines
> Date : 2026-05-18
> Statut : Actif

---

## Ce qu'ASEF était

Un runtime Python d'orchestration agentique centré sur le développement logiciel.
Pipeline G0→G7, 5 rôles agents, qualité gates branchés sur ruff / pytest / gitleaks.

Solide. Limité à un seul domaine.

---

## Ce qu'ASEF devient

> **Agentic Systemic Execution Framework**
>
> Un méta-système de frameworks agentiques gouvernables, auditables,
> spécialisés par domaine, fondés sur la preuve.

ASEF n'est plus un outil de développement logiciel.
ASEF est un **socle universel** permettant de transformer n'importe quel métier
en système opérationnel composé d'agents, de workflows, de gates et de preuves.

---

## Principe fondateur

**Tout métier est opérationalisable.**

Chaque domaine — QA, gouvernance IA, data, cybersécurité, product, finance,
santé, éducation — peut être décomposé en :

- agents spécialisés avec des rôles et des limites précises ;
- workflows structurés avec des étapes et des dépendances claires ;
- quality gates bloquants qui empêchent d'avancer sans preuve ;
- evidence packages vérifiables et auditables ;
- décisions tracées avec contexte, alternatives et justification ;
- mémoire consolidée qui capitalise et améliore le système.

ASEF fournit les **primitives universelles** pour construire ces systèmes.

---

## Les quatre problèmes qu'ASEF résout

### 1. Agents sans gouvernance
Les frameworks agentiques actuels ajoutent des agents sans définir leurs limites,
leurs permissions, leurs preuves de succès. Résultat : des agents qui simulent,
qui hallucinent, qui contournent les contrôles.

**ASEF impose** : rôle défini, permissions déclarées, preuves obligatoires,
escalade humaine structurée.

### 2. Livrables sans preuve
Des rapports, des validations, des décisions sont produits sans trace vérifiable.
Impossible d'auditer. Impossible de faire confiance.

**ASEF impose** : evidence package obligatoire. Un livrable sans preuve
rattachée est invalide.

### 3. Simulation de décision
Les LLMs suggèrent, évaluent, recommandent — mais font semblant de décider.
Les décisions critiques restent humaines mais ne sont pas formalisées.

**ASEF impose** : séparation nette entre recommandation agent et décision humaine.
Chaque décision est tracée dans DECISIONS.md avec contexte, options, choix, raison.

### 4. Frameworks documentaires sans exécution
Des processus sur papier que personne ne suit. Des templates jamais utilisés.
Des gates qui ne bloquent rien.

**ASEF impose** : tout framework doit être exécutable. Un gate qui ne bloque pas
n'est pas un gate. Une règle sans enforcement n'est pas une règle.

---

## Architecture cible en trois couches

```
┌─────────────────────────────────────────────────────────────────┐
│  COUCHE 3 — ASEF-Instance                                       │
│  Déclinaison concrète pour un projet, une équipe, un produit    │
│  (ASEF-QA pour App SaaS XYZ / ASEF-AIGov pour Banque ABC)      │
├─────────────────────────────────────────────────────────────────┤
│  COUCHE 2 — ASEF-Domain                                         │
│  Frameworks verticaux par domaine métier                        │
│  (ASEF-QA / ASEF-AIGov / ASEF-DataGov / ASEF-Product / ...)    │
├─────────────────────────────────────────────────────────────────┤
│  COUCHE 1 — ASEF-Core                                           │
│  Primitives universelles : orchestration, gates, evidence,      │
│  memory, decisions, risk, audit, HITL                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ce qu'ASEF n'est PAS

- Un outil de chat multi-agents sans gouvernance.
- Un wrapper LLM avec des prompts habillés en "agents".
- Un système de documentation sans exécution.
- Un framework réservé aux équipes techniques.
- Un projet académique. ASEF doit fonctionner en production.

---

## Principes immuables

1. **Preuve avant déclaration.** Rien n'est terminé sans preuve vérifiable.
2. **Gates bloquants.** Un gate qui ne bloque pas n'existe pas.
3. **Décision humaine souveraine.** Les agents recommandent. Les humains décident
   sur les sujets critiques.
4. **Mémoire systémique.** Chaque cycle enrichit le système. Pas de reset.
5. **Modularité sans duplication.** ASEF-Core fournit les primitives.
   Les domaines les spécialisent. Jamais ils ne les réinventent.
6. **Anti-hallucination par design.** Distinguer fait, hypothèse, inférence,
   recommandation et décision. Toujours. Sans exception.

---

## Indicateurs de succès

| Indicateur | Cible |
|---|---|
| Frameworks verticaux actifs | ≥ 5 d'ici Q3 2026 |
| Instances en production | ≥ 2 d'ici Q4 2026 |
| Couverture documentaire par framework | 100% (15 fichiers requis) |
| Gates bloquants par framework | ≥ 5 |
| Evidence package produit à chaque livraison | 100% |
| Décisions humaines tracées | 100% |

---

## Roadmap synthétique

| Phase | Contenu | Cible |
|---|---|---|
| MVP | ASEF-Core + ASEF-Evidence + ASEF-Gates + ASEF-Decision + ASEF-QA | Q2 2026 |
| V1 | + ASEF-AIGov + ASEF-DataGov + ASEF-Product + ASEF-Delivery | Q3 2026 |
| V2 | + 6 frameworks Priorité 2 (Dev, DevOps, LLMEval, AgentEval, Cyber, Control) | Q4 2026 |
| V3 | + Frameworks Priorité 3 + tooling + IDE integration | Q1 2027 |

Voir `ROADMAP.md` pour le détail.
