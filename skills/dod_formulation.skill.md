# skill: dod_formulation

**id**: dod_formulation
**version**: 1.0.0
**agents**: orchestrator, developer, qa
**tools_required**: read_file

## Purpose
Formuler un DoD (Definition of Done) vérifiable avant d'exécuter un livrable.

## Trigger
Toute demande de livrable (code, doc, analyse, implémentation, plan).

## Input
Description de la demande humaine.

## Steps
1. Identifier l'intent réel derrière la demande (pas l'action littérale)
2. Formuler ≤ 8 critères binaires (passé/raté, sans ambiguïté)
3. Pour chaque critère : identifier comment il sera vérifié
4. Présenter le DoD à l'humain
5. Attendre validation (modification ou go)
6. Ne commencer l'exécution qu'après validation

## Format DoD
```
DoD — [Titre de la tâche]
□ [Critère 1] — vérifié par : [méthode]
□ [Critère 2] — vérifié par : [méthode]
...
(≤ 8 critères)
```

## Critères d'un bon critère DoD
- **Binaire** : peut être coché oui/non
- **Vérifiable** : il existe une méthode de vérification concrète
- **Lié à l'intent** : répond à ce que l'humain voulait

## Output
DoD validé par l'humain, prêt pour exécution.

## Evidence required
DoD présenté ET retour humain obtenu avant toute action de livrable.
