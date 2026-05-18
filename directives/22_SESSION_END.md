# DIRECTIVE — session_end

## Purpose

Persister le contexte de session avant fermeture.  
Sans cette directive, chaque session repart de zéro — les décisions, blocages et état en cours sont perdus.  
Pourquoi elle existe : anti-pattern session_end partielle observé 2026-04-15/17.  
Quand elle s'applique : fin de chaque session, avant de fermer.  
Quelle mauvaise action elle empêche : perte de contexte inter-session, dérive silencieuse.

## Scope

Couvre : toute session agentique normale dans ASEF.  
Ne couvre pas : session interrompue brutalement (voir session_end_critical.md).

## Checklist de fin de session (non-négociable)

### STEP 1 — Mettre à jour BRIEF.md
```
- Session date
- Objectif de session
- Ce qui a été fait (liste)
- Décisions prises
- Prochaine session — reprendre ici (instructions précises)
- Risques actifs
- Fichiers modifiés cette session
```

### STEP 2 — Mettre à jour SESSION_LOG.md
```
Format : | Date | Objectif | Actions | Fichiers modifiés | Gates validés | Statut |
```

### STEP 3 (si contexte change) — Mettre à jour MEMORY.md
- Phase active a changé ? → mettre à jour
- Nouvelle décision stabilisée ? → ajouter
- Nouvelle prochaine action prioritaire ? → mettre à jour

### STEP 4 (si livrable) — Mettre à jour CHANGELOG.md
- Section `## [Unreleased]`
- Format Keep a Changelog

### STEP 5 (si décision structurante) — Vérifier DECISIONS.md
- Toute décision prise en session est-elle documentée ?
- Format ADR minimal respecté ?

### STEP 6 — Mettre à jour HEARTBEAT.md
- Date de dernière session
- Statut général
- Prochaine action prioritaire

## Validation fin de session

```
□ BRIEF.md mis à jour
□ SESSION_LOG.md mis à jour
□ MEMORY.md mis à jour (si nécessaire)
□ CHANGELOG.md mis à jour (si livrable)
□ DECISIONS.md vérifié
□ HEARTBEAT.md mis à jour
□ Aucun secret dans les fichiers modifiés
```

## Mandatory Rules

- [SESSION-END-001] Ne pas fermer sans avoir fait la checklist complète
- [SESSION-END-002] BRIEF.md doit être lisible comme point de reprise par un agent fresh
- [SESSION-END-003] SESSION_LOG.md est append-only — ne jamais modifier les entrées passées
