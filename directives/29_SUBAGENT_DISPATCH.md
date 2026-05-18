# DIRECTIVE — subagent_dispatch

## Purpose

Définir comment dispatcher les tâches vers les subagents.  
Sans cette directive, le dispatch est 1:1 (1 tâche → 1 agent) → aucune perspective adverse → simulation mono-angle.  
Pourquoi elle existe : 3 corrections sur le même point en session 2026-04-16 — dispatch solo répété.  
Quand elle s'applique : toute délégation de tâche vers un subagent.  
Quelle mauvaise action elle empêche : dispatch solo qui ne croise aucune perspective.

## Scope

Couvre : toute invocation de subagent dans ASEF.  
Ne couvre pas : outils de lecture pure (grep_search, read_file, etc.).

## Principe fondamental

> **1 problème → 1 équipe composite → 1 synthèse**  
> Pas : 1 problème → 1 agent → 1 réponse

La friction entre perspectives fait émerger ce qu'aucun angle isolé ne voit.

## Types de dispatch

### Dispatch simple (1 agent, 1 tâche claire)
Acceptable pour :
- Tâches procédurales avec output défini (ex: "générer le fichier X selon ce template")
- Tâches de lecture/exploration (ex: subagent `Explore`)
- Tâches avec un seul domaine d'expertise requis

### Dispatch composite (équipe dans 1 brief)
Obligatoire pour :
- Audits (qualité, sécurité, architecture)
- Décisions avec trade-offs
- Tout problème où > 1 perspective est pertinente

**Format brief équipe composite :**
```
Équipe : [persona1 (angle1)] + [persona2 (angle2)] + [persona3 (angle3)]
Objectif de croisement : [ce qu'on cherche à faire émerger par la friction]
Livrable attendu : [format précis]
```

## Règles de dispatch

1. Avant de dispatcher → identifier combien de perspectives sont pertinentes
2. Si > 1 perspective → brief composite, pas dispatch séquentiel solo
3. Le brief doit contenir : contexte complet, output attendu, critères de qualité
4. L'orchestrator récolte, structure, synthétise — les subagents pensent et font
5. Ne pas enchaîner > 3 subagents sans gate de validation intermédiaire

## Mandatory Rules

- [DISPATCH-001] Audit → équipe composite obligatoire (min 2 perspectives)
- [DISPATCH-002] Brief complet → contexte + output + critères, jamais une phrase vague
- [DISPATCH-003] L'orchestrator ne délègue pas sa responsabilité de synthèse
