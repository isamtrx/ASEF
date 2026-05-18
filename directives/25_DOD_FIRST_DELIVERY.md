# DIRECTIVE — dod_first_delivery

## Purpose

Définir ce que "terminé" veut dire AVANT d'exécuter, pas après.  
Sans cette directive, un livrable reflète l'interprétation de l'agent, pas l'intent de l'humain.  
Pourquoi elle existe : L-019, validé 2026-04-18. Désalignement systématique sur les demandes "fais X complet".  
Quand elle s'applique : toute demande de livrable (code, doc, analyse, plan, implémentation).  
Quelle mauvaise action elle empêche : livraison qui répond à la mauvaise question.

## Scope

Couvre : tout livrable demandé dans ASEF.  
Ne couvre pas : questions factuelles sans livrable associé.

## Pipeline obligatoire

```
1. Recevoir la demande
2. Formuler un DoD ≤ 8 lignes
3. Présenter le DoD à l'humain
4. Attendre validation (5 secondes suffisent si évident)
5. Exécuter bout en bout
6. Revenir avec preuve binaire (logs, screenshots, build)
```

## Format DoD

```
DoD — [Titre de la tâche]
□ [Critère 1 — vérifiable, binaire]
□ [Critère 2 — vérifiable, binaire]
□ [Critère 3 — vérifiable, binaire]
...
(≤ 8 lignes)
```

## Ce qu'un bon critère DoD fait

- **Vérifiable** : peut être coché oui/non sans ambiguïté
- **Binaire** : passé ou raté, pas "à peu près"
- **Lié à l'intent** : répond à ce que l'humain voulait, pas à ce que j'ai produit

## Ce qu'un mauvais critère DoD fait

- "Le code est propre" → non vérifiable
- "L'utilisateur est content" → non mesurable avant livraison
- "Ça marche" → trop vague

## Interdit

- Commencer à coder/écrire avant que le DoD soit validé
- Déclarer "terminé" sans avoir vérifié chaque critère
- Reformuler le DoD après coup pour qu'il corresponde à ce qui a été livré

## Mandatory Rules

- [DOD-001] DoD formulé et validé avant toute exécution
- [DOD-002] Chaque critère est vérifié à la fin, pas supposé satisfait
- [DOD-003] Preuve fournie pour chaque critère (log, screenshot, fichier)
