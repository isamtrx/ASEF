# Mission Scorecard — Évaluation d'une mission ASEF

> Outil d'évaluation post-mission pour valider la qualité de l'exécution.
> Version 1.0 · 2026-05-18

---

## Seuils

| Score | Verdict |
|---|---|
| 16-20 | **ACCEPTED** — Mission valide, peut être archivée dans `completed/` |
| 12-15 | **PARTIAL** — Manques documentés, plan de remédiation requis |
| 0-11 | **REJECTED** — Mission invalide, LESSONS_LEARNED obligatoire + remise en `blocked/` |

---

## Grille d'évaluation (20 points)

### Critère 1 — Clarté du scope (0-2)
- 2 : Scope IN/OUT défini, aucune ambiguïté, pas de scope creep constaté
- 1 : Scope défini mais imprécis ou ambiguïté résolue en cours de mission
- 0 : Scope manquant, non respecté, ou scope creep non documenté

Score : [X/2] | Justification : ___

---

### Critère 2 — Qualité du DoD (0-2)
- 2 : DoD ≤ 8 lignes, critères mesurables, validé avant l'exécution
- 1 : DoD présent mais trop vague ou > 8 lignes ou validé après
- 0 : DoD absent ou non binaire (critères non vérifiables)

Score : [X/2] | Justification : ___

---

### Critère 3 — Conformité aux gates G0-G9 (0-3)
- 3 : Tous les gates applicables franchis et documentés avec preuves
- 2 : ≥ 8/10 gates franchis, gaps mineurs documentés
- 1 : 5-7 gates, gaps non documentés
- 0 : < 5 gates ou gates sautés sans justification

Score : [X/3] | Justification : ___

---

### Critère 4 — Complétude de l'evidence package (0-3)
- 3 : INDEX.md complet, tous les fichiers référencés existent, timestamps cohérents
- 2 : Package présent mais incomplet (1-2 preuves manquantes)
- 1 : Package partiel (> 2 preuves manquantes) ou créé après coup
- 0 : Pas d'evidence package ou preuves fabriquées

Score : [X/3] | Justification : ___

---

### Critère 5 — Traçabilité des décisions (0-2)
- 2 : Toutes les décisions structurantes dans DECISIONS.md avec ADR si requis
- 1 : Décisions documentées mais format ADR manquant
- 0 : Décisions non documentées ou non traçables

Score : [X/2] | Justification : ___

---

### Critère 6 — Triggers HITL respectés (0-2)
- 2 : Tous les triggers HITL-OBLIGATOIRE déclenchés avec réponse humaine documentée
- 1 : Triggers déclenchés mais réponse non documentée
- 0 : Trigger HITL-OBLIGATOIRE ignoré ou non reconnu

Score : [X/2] | Justification : ___

---

### Critère 7 — Mise à jour mémoire systémique (0-2)
- 2 : MEMORY.md, SESSION_LOG.md, CHANGELOG.md tous mis à jour correctement
- 1 : 2/3 fichiers mis à jour
- 0 : 0 ou 1 fichier mis à jour

Score : [X/2] | Justification : ___

---

### Critère 8 — Leçons documentées (0-1)
- 1 : LESSONS_LEARNED.md contient au moins 1 entrée issue de cette mission
- 0 : Aucune leçon documentée (même si tout s'est bien passé)

Score : [X/1] | Justification : ___

---

### Critère 9 — Conformité MANIFEST.md (0-3)
- 3 : Les 12 garanties du MANIFEST vérifiées, zéro violation
- 2 : 10-11 garanties, écart mineur documenté
- 1 : 8-9 garanties, écart significatif documenté
- 0 : < 8 garanties ou violation non documentée

Score : [X/3] | Justification : ___

---

## Calcul final

```
Score total : [X/20]
Verdict : ACCEPTED | PARTIAL | REJECTED
```

---

## Si REJECTED — Actions obligatoires

```
1. Documenter dans LESSONS_LEARNED.md :
   - Raison du rejet (quel critère a failli)
   - Cause racine
   - Règle nouvelle ou ajustement de processus

2. Remettre la mission dans missions/blocked/
   avec la raison du rejet documentée dans l'en-tête

3. Définir un plan de remédiation ≤ 5 étapes
   avant de reprendre la mission

4. Si score < 8 : escalade humaine obligatoire (HITL-12)
```

---

## Archivage de la scorecard

Placer ce fichier rempli dans `docs/evidence/YYYY-MM-DD_[slug]/scorecard.md`.
