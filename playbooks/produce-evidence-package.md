# Playbook : Produire un evidence package

> Applicable à toute livraison nécessitant des preuves formelles.
> Version 1.0 · 2026-05-18

---

## Quand utiliser ce playbook

- Avant toute livraison en production (Gate G8).
- Avant toute validation humaine formelle.
- À la fin de chaque cycle de tâche CRITICAL ou HIGH.
- Quand le MANIFEST G-04 est applicable (toujours).

---

## Step 1 — Créer la structure du dossier

**AVANT** de commencer l'exécution (Gate G5) :

```bash
# Créer le dossier evidence avec le bon slug
mkdir docs/evidence/YYYY-MM-DD_[slug]
mkdir docs/evidence/YYYY-MM-DD_[slug]/gates
mkdir docs/evidence/YYYY-MM-DD_[slug]/logs
mkdir docs/evidence/YYYY-MM-DD_[slug]/reports
mkdir docs/evidence/YYYY-MM-DD_[slug]/captures
mkdir docs/evidence/YYYY-MM-DD_[slug]/metrics
mkdir docs/evidence/YYYY-MM-DD_[slug]/artifacts
```

Créer `INDEX.md` vide avec le header :
```markdown
# Evidence Package — [Nom du livrable]
Date : YYYY-MM-DD
Tâche : [Description 1 ligne]
Statut : EN COURS
```

---

## Step 2 — Documenter chaque gate pendant l'exécution

Pour chaque gate G0-G9 franchi, créer `gates/G[X]-[nom].md` :

```markdown
# Gate G[X] — [Nom]
Date : YYYY-MM-DD HH:MM
Statut : PASS | FAIL | BLOCKED | NOT_APPLICABLE

## Critères évalués

| Critère | Statut | Note |
|---|---|---|
| [Critère 1] | ✓ | [Observation] |
| [Critère 2] | ✓ | [Observation] |

## Preuves rattachées
- [logs/fichier.txt]
- [reports/rapport.md]

## Décision
[PASS — continuer / FAIL — raison / BLOCKED — raison et actions]
```

---

## Step 3 — Collecter les preuves en temps réel

**Règle absolue** : Chaque preuve est collectée au moment de l'action, jamais après.

| Type de preuve | Où la mettre | Nommage |
|---|---|---|
| Output terminal | `logs/` | `YYYYMMDD-[action].txt` |
| Rapport outil | `reports/` | `[outil]-report.md` ou `.json` |
| Screenshot | `captures/` | `YYYYMMDD-[context].png` |
| Métrique | `metrics/` | `[metric-name].txt` |
| Livrable final | `artifacts/` | `[slug]-[version].[ext]` |

---

## Step 4 — Compléter INDEX.md

À la fin de l'exécution :

```markdown
# Evidence Package — [Nom du livrable]
Date : YYYY-MM-DD
Tâche : [Description]
Statut : COMPLET

## Gates

| Gate | Statut | Preuve |
|---|---|---|
| G0 | PASS | gates/G0-intake.md |
| G1 | PASS | gates/G1-scope.md |
| ... | ... | ... |

## Preuves collectées

| Fichier | Type | Description |
|---|---|---|
| logs/ci-run.txt | LOG | Output pipeline CI |
| ... | ... | ... |

## Anomalies et écarts
[Liste ou "Aucune"]

## Validation humaine
[Nom, date, décision — ou "N/A"]
```

---

## Step 5 — Vérification anti-hallucination

Avant de finaliser le package :

```
□ Chaque proof fichier référencé dans INDEX.md existe réellement dans le dossier
□ Aucun fichier dans INDEX.md créé après coup (timestamp antérieur à l'action)
□ Les métriques correspondent aux logs (coverage ≠ logs coverage = cohérents)
□ Les captures correspondent aux tests décrits
□ Aucun résumé approximatif sans fichier source
```

---

## Step 6 — Revue AuditAgent et archivage

1. AuditAgent vérifie les 14 questions (voir ASEF-Audit.md).
2. Si tout est conforme : statut `COMPLET`.
3. Archiver le dossier evidence (ne pas modifier après archivage).
4. Référencer le package dans la mission correspondante.

---

## Checklist finale

```
□ Dossier docs/evidence/YYYY-MM-DD_slug/ créé AVANT l'exécution
□ INDEX.md présent et complet
□ Tous les gates documentés dans gates/
□ Toutes les preuves collectées en temps réel
□ Vérification anti-hallucination effectuée
□ AuditAgent a validé
□ Validation humaine documentée si HITL actif
□ CHANGELOG.md mis à jour
```
