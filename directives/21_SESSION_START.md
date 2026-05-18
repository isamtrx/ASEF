# DIRECTIVE — session_start

## Purpose

Forcer le bootstrap documentaire avant toute réponse.  
Sans cette directive, l'agent répond sans contexte → propose des actions hors scope ou en contradiction avec les décisions actives.  
Pourquoi elle existe : failure mode observé 2026-05-18 — réponse avant lecture MEMORY.md/SCOPE.md/DECISIONS.md.  
Quand elle s'applique : début de chaque session, avant le premier mot de réponse.  
Quelle mauvaise action elle empêche : action hors scope, violation de décision active, contexte stale non détecté.

## Scope

Couvre : toute session agentique dans ASEF.  
Ne couvre pas : actions mid-session (voir CORE_REFLEXES).

## Steps obligatoires (dans l'ordre)

### STEP 1 — Lire HEARTBEAT.md
- Vérifier la date de dernière mise à jour
- Si > 7 jours → warning contexte potentiellement stale
- Si statut = 🔴 → lire POSTMORTEMS.md avant de continuer

### STEP 2 — Lire BRIEF.md
- Identifier la session précédente et ce qui reste à faire
- Si BRIEF.md absent → première session, continuer

### STEP 3 — Lire MEMORY.md
- Identifier la phase active (Sprint X)
- Identifier les décisions stabilisées
- Identifier la prochaine action prioritaire

### STEP 4 — Lire SCOPE.md
- Identifier le périmètre IN SCOPE / OUT OF SCOPE
- Comparer avec la demande reçue
- Si OUT OF SCOPE → escalader immédiatement (ne pas exécuter)

### STEP 5 — Lire DECISIONS.md
- Vérifier les décisions actives
- La demande contredit-elle une décision ? → signaler avant d'agir

### STEP 6 (conditionnel) — Lire docs/ARCHITECTURE.md
- Uniquement si la tâche touche l'architecture technique

## Validation bootstrap

```
□ HEARTBEAT.md lu — contexte récent confirmé
□ BRIEF.md lu — état session précédente connu
□ MEMORY.md lu — phase et contexte actifs connus
□ SCOPE.md lu — tâche confirmée IN scope
□ DECISIONS.md lu — aucune décision active violée
□ Rôle actif confirmé (orchestrator par défaut)
```

## Failure mode à rapporter

Si le bootstrap n'a pas été fait en début de session :
1. Le reconnaître explicitement ("bootstrap non effectué")
2. L'effectuer immédiatement
3. Vérifier si les réponses déjà données sont cohérentes avec le contexte lu

## Mandatory Rules

- [SESSION-START-001] Aucune réponse substantielle avant bootstrap complet
- [SESSION-START-002] Le bootstrap se fait via read_file sur les fichiers listés, pas de mémoire supposée
- [SESSION-START-003] En cas de fichier manquant → signaler, ne pas supposer son contenu
