---
applyTo: "**"
---

# Bootstrap ASEF — Obligatoire en début de session

> Ce fichier est chargé automatiquement dans tout contexte de fichier ASEF.  
> Il impose le bootstrap documentaire avant toute action.

## Protocole de démarrage (L0 → L4)

Avant de répondre à TOUTE demande, exécuter dans l'ordre :

| Niveau | Fichier | Ce qu'on y cherche |
|--------|---------|-------------------|
| L0 | `AGENTS.md` | Constitution — permissions du rôle actif |
| L1 | `MEMORY.md` | Phase actuelle, sprint, décisions stabilisées |
| L2 | `SCOPE.md` | La tâche demandée est-elle IN scope ? |
| L3 | `DECISIONS.md` | Décisions structurantes à ne pas violer |
| L4 | `docs/ARCHITECTURE.md` | Si la tâche touche l'architecture technique |

## Règle de blocage

Si la tâche est **OUT OF SCOPE** selon `SCOPE.md` :
1. Ne pas exécuter
2. Signaler clairement : "Cette tâche est hors périmètre ASEF (SCOPE.md §X)"
3. Proposer la redirection ou l'escalade appropriée

## Ce que le bootstrap révèle

- **MEMORY.md** dit dans quelle phase est le projet (Sprint 1 = CI/CD, pas runtime)
- **SCOPE.md** dit ce qui est hors périmètre (runtime LLM, MCP, Grafana, Ollama)
- **DECISIONS.md** dit quelles décisions sont actives (format ADR, ne pas revisiter sans raison)

## Failure mode à éviter

> Répondre sans avoir lu ces fichiers = proposer des actions hors scope ou en contradiction avec les décisions actives.  
> Ce fichier existe précisément parce que ce failure mode s'est produit.

## Rôle actif : `orchestrator` (par défaut)

- Pas d'implémentation directe de code sans délégation explicite via subagent
- Lire, analyser, planifier, écrire `DECISIONS.md` / `MEMORY.md` / `SESSION_LOG.md` = autorisé
- Modifier du code source = déléguer à `developer`
