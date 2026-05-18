# skill: bootstrap_check

**id**: bootstrap_check
**version**: 1.0.0
**agents**: orchestrator, developer, qa
**tools_required**: read_file

## Purpose
Vérifier que le bootstrap de session est complet avant de continuer.

## Trigger
Début de session, ou doute sur la fraîcheur du contexte.

## Input
Accès lecture aux fichiers : HEARTBEAT.md, BRIEF.md, MEMORY.md, SCOPE.md, DECISIONS.md.

## Steps
1. Lire HEARTBEAT.md — date de dernière session > 7 jours ? → warning
2. Lire BRIEF.md — identifier la prochaine action de la session précédente
3. Lire MEMORY.md — identifier la phase active et les décisions stabilisées
4. Lire SCOPE.md — noter les items IN SCOPE et OUT OF SCOPE
5. Lire DECISIONS.md — lister les décisions actives
6. Produire le résumé bootstrap (voir Output)

## Output
```
Bootstrap ASEF — [date]
Phase active : [Sprint X]
Prochaine action : [issue de BRIEF.md]
Décisions actives : [liste D-XXXX]
Scope check : IN ✅ / OUT ❌ [items pertinents]
Risques actifs : [liste issue de HEARTBEAT.md]
```

## Evidence required
Chaque fichier listé dans Steps doit avoir été lu (pas supposé). Le résumé bootstrap doit contenir des données issues de ces lectures.
