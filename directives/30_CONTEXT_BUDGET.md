# DIRECTIVE — context_budget

## Purpose

Gérer le budget de contexte (tokens) pour éviter la saturation de fenêtre.  
Sans cette directive, charger trop de fichiers en même temps dégrade les performances et fait perdre les informations en fin de contexte.  
Quand elle s'applique : toute session avec > 5 fichiers chargés ou > 3 subagents invoqués.  
Quelle mauvaise action elle empêche : fenêtre de contexte saturée, informations critiques perdues.

## Scope

Couvre : gestion du contexte dans les sessions ASEF.  
Ne couvre pas : fichiers lus via outils sans les mettre dans le contexte actif.

## Priorités de chargement

### TOUJOURS charger (bootstrap)
1. HEARTBEAT.md — état santé
2. BRIEF.md — contexte session précédente
3. MEMORY.md — phase et décisions
4. SCOPE.md — périmètre
5. DECISIONS.md — contraintes actives

### Charger selon la tâche
- Code source → uniquement les fichiers directement concernés
- Architecture → docs/ARCHITECTURE.md + ADR pertinent
- Sécurité → docs/security/SECURITY.md + THREAT_MODEL.md

### Ne PAS charger systématiquement
- Tous les fichiers du répertoire courant
- Des fichiers "au cas où on en aurait besoin"
- Des docs de référence entières pour une question partielle

## Règles de gestion

1. **Lire en range** — lire 50-100 lignes ciblées plutôt que le fichier entier si possible
2. **Paralléliser les lectures** — lire plusieurs fichiers en parallèle plutôt que séquentiellement
3. **Signal d'alerte** : si > 15 fichiers chargés → évaluer ce qui peut être déchargé
4. **Subagent pour contexte lourd** — si une tâche nécessite > 10 fichiers → déléguer à un subagent dédié

## Indicateurs de saturation

| Signal | Action |
|--------|--------|
| Réponses qui "oublient" des contraintes lues au début | Recharger les contraintes critiques |
| Temps de réponse dégradé | Réduire le contexte chargé |
| Contradictions avec des décisions précédemment lues | Relire DECISIONS.md |

## Mandatory Rules

- [BUDGET-001] Bootstrap files ont priorité absolue dans le contexte
- [BUDGET-002] Ne pas charger un fichier sans raison de tâche explicite
- [BUDGET-003] Contexte > 15 fichiers → audit du contexte avant de continuer
