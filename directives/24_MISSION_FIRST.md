# DIRECTIVE — mission_first

## Purpose

Toute création de livrable doit être couverte par une mission active avant d'être exécutée.  
Sans cette directive, des fichiers sont créés sans traçabilité → non validables, non rattachables à un objectif.  
Pourquoi elle existe : anti-pattern observé 2026-04-18 — 23 fichiers créés sans mission active.  
Quand elle s'applique : avant toute création > 3 fichiers OU > 100 lignes.  
Quelle mauvaise action elle empêche : travail fantôme, livrables non validables.

## Scope

Couvre : tout workspace, tout type de livrable (code, docs, scripts, configs).  
Ne couvre pas : modifications chirurgicales < 3 fichiers sur mission existante.

## Règle de déclenchement

**Avant de créer > 3 fichiers OU > 100 lignes :**
1. Vérifier qu'une mission active couvre ce travail (`missions/active/`)
2. Si aucune mission active → créer une mission minimale d'abord
3. Si la mission existe → vérifier que le livrable est dans son périmètre

## Format mission minimale

```markdown
# MISSION — [Titre court]
Date : YYYY-MM-DD
Statut : Active
Objectif : [1 phrase]
Périmètre : [liste des fichiers/dossiers concernés]
DoD : [≤ 8 lignes]
Owner : [rôle]
```

## Rationalisations interdites

Ces justifications ne dispensent PAS de mission :
- "C'est juste un side-quest"
- "C'est hors du scope principal"
- "C'est temporaire / expérimental"
- "Je vais le rattacher après"

**Si c'est réel → ça mérite une mission. Sinon → ne pas le faire.**

## Mandatory Rules

- [MISSION-001] Pas de création massive sans mission active couvrant le périmètre
- [MISSION-002] Une mission doit exister AVANT les fichiers, jamais rétroactivement
- [MISSION-003] La mission minimale prend < 5 minutes à écrire — pas une excuse pour s'en passer
