# skill: scope_check

**id**: scope_check
**version**: 1.0.0
**agents**: orchestrator, developer, qa
**tools_required**: read_file

## Purpose
Vérifier qu'une tâche donnée est IN SCOPE avant d'agir.

## Trigger
Toute demande impliquant une modification, création ou action substantielle.

## Input
Description de la tâche demandée. Accès lecture à SCOPE.md.

## Steps
1. Lire SCOPE.md — section IN SCOPE et OUT OF SCOPE
2. Décomposer la tâche en actions élémentaires
3. Pour chaque action : est-elle couverte par IN SCOPE ? Contredite par OUT OF SCOPE ?
4. Vérifier également DECISIONS.md pour des contraintes de périmètre spécifiques
5. Produire le verdict (voir Output)

## Output
```
Scope check — [titre de la tâche]
IN SCOPE : [liste des parties validées]
OUT OF SCOPE : [liste des parties invalides avec référence SCOPE.md §X]
Verdict : ✅ TOUT IN SCOPE / ⚠️ PARTIEL / ❌ HORS SCOPE
Action recommandée : [exécuter / exécuter partiellement / escalader]
```

## Evidence required
Citer explicitement la section SCOPE.md qui valide ou invalide chaque partie.
