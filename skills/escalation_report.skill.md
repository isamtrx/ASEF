# skill: escalation_report

**id**: escalation_report
**version**: 1.0.0
**agents**: orchestrator
**tools_required**: read_file, replace_string_in_file

## Purpose
Produire un rapport d'escalade structuré pour présentation humaine.

## Trigger
Condition d'éscalade détectée (voir `directives/28_STOP_LIST.md` et `directives/31_ESCALATION_PROTOCOL.md`).

## Input
Raison de l'escalade. Contexte de la tâche en cours. Options disponibles.

## Steps
1. Identifier précisément la condition déclenchante (quelle règle, quel gate, quelle contrainte)
2. Documenter dans SESSION_LOG.md : "ESCALADE — [raison] — [date]"
3. Construire le rapport (voir Format)
4. Présenter à l'humain
5. Attendre autorisation explicite
6. Documenter la réponse humaine dans SESSION_LOG.md

## Format rapport
```
🚨 ESCALADE REQUISE — [raison en 1 ligne]

Contexte : [ce qui se passe, étape en cours]
Condition déclenchante : [règle/gate/contrainte avec référence fichier]
Options disponibles :
  A. [option] — avantages / inconvénients
  B. [option] — avantages / inconvénients
  C. [option si applicable]
Recommandation : [option préférée + raison courte]
Action en attente : [ce que je ne peux pas faire sans autorisation]
```

## Output
Rapport présenté. Réponse humaine obtenue et documentée.

## Evidence required
SESSION_LOG.md contient l'entrée d'escalade ET la décision humaine.
