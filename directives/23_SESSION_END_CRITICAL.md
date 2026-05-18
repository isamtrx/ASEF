# DIRECTIVE — session_end_critical

## Purpose

Gestion de session interrompue brutalement (crash, timeout, coupure réseau).  
Sans cette directive, le travail en cours est abandonné silencieusement sans signal de reprise.  
Quand elle s'applique : session coupée sans avoir pu exécuter session_end.md normalement.  
Quelle mauvaise action elle empêche : perte silencieuse de travail en cours, absence de point de reprise.

## Détection d'interruption

Une session est considérée interrompue si :
- BRIEF.md date > HEARTBEAT.md date (session ouverte sans fermeture propre)
- SESSION_LOG.md dernière entrée ne correspond pas à MEMORY.md état actuel
- Une tâche est marquée `in-progress` dans le plan sans entrée de clôture

## Protocole de reprise (à lire en début de session suivante)

### STEP 1 — Détecter l'interruption
- Comparer date BRIEF.md vs HEARTBEAT.md
- Si BRIEF.md plus récent → session précédente n'a pas été fermée proprement

### STEP 2 — Reconstituer l'état
1. Lire BRIEF.md (dernière session connue)
2. Lire SESSION_LOG.md (dernière entrée)
3. Lire les fichiers listés comme "modifiés" dans BRIEF.md
4. Identifier ce qui était en cours

### STEP 3 — Évaluer la complétude
- Les fichiers en cours sont-ils dans un état cohérent ?
- Y a-t-il des fichiers partiellement écrits ?
- Les gates ont-ils été vérifiés avant l'interruption ?

### STEP 4 — Décision de reprise
| État trouvé | Action |
|-------------|--------|
| Fichiers cohérents, tâche > 80% | Continuer depuis l'état trouvé |
| Fichiers partiels ou incohérents | Revenir au dernier état stable (SESSION_LOG.md) |
| État indéterminable | Escalader à l'humain avant toute action |

### STEP 5 — Documenter la reprise
- Ajouter une entrée SESSION_LOG.md : "Reprise après interruption — [date] — état reconstruit depuis [fichier]"
- Mettre à jour HEARTBEAT.md

## Mandatory Rules

- [SESSION-CRIT-001] Ne jamais supposer qu'une interruption = travail terminé
- [SESSION-CRIT-002] En cas de doute sur l'état → escalader plutôt que supposer
- [SESSION-CRIT-003] La reprise doit être documentée dans SESSION_LOG.md
