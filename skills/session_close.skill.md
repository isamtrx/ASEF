# skill: session_close

**id**: session_close
**version**: 1.0.0
**agents**: orchestrator
**tools_required**: read_file, replace_string_in_file

## Purpose
Fermer proprement une session en persistant tout le contexte nécessaire à la reprise.

## Trigger
Signal de fin de session (demande humaine ou tâche terminée).

## Input
Liste des fichiers modifiés pendant la session. Décisions prises. Tâches complétées et en cours.

## Steps
1. Rédiger l'entrée BRIEF.md :
   - Section : date, objectif, fait, décisions prises, prochaine session (point de reprise précis), risques actifs, fichiers modifiés
2. Ajouter une ligne dans SESSION_LOG.md :
   - Format : `| Date | Objectif | Actions résumées | Fichiers modifiés | Gates validés | Statut |`
3. Si contexte a changé → mettre à jour MEMORY.md :
   - Phase active, décisions stabilisées, prochaine action prioritaire
4. Si livrable produit → ajouter dans CHANGELOG.md section `## [Unreleased]`
5. Mettre à jour HEARTBEAT.md :
   - Date, statut général, prochaine action prioritaire
6. Vérifier DECISIONS.md : toutes les décisions de session sont documentées ?

## Output
Confirmation que les 6 fichiers ont été mis à jour avec les données de session.

## Evidence required
Lire chaque fichier après mise à jour pour confirmer que le contenu est correct et non-vide.
