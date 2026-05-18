# Playbook : Exécuter un Go/No-Go

> Applicable à toute décision formelle de continuer ou d'arrêter.
> Version 1.0 · 2026-05-18

---

## Quand utiliser ce playbook

- Gate G8 (décision finale sur un livrable).
- Fin d'un sprint ou d'une phase.
- Avant un déploiement en production.
- Avant une action irréversible.

---

## Step 1 — Identifier le type de décision

Avant toute analyse, identifier :

```
Type : GO | NO-GO | CONDITIONAL GO | BLOCKED
Périmètre : [Ce sur quoi porte la décision]
Irréversibilité : Réversible | Irréversible
Trigger HITL : [HITL-XX si applicable / Non]
```

---

## Step 2 — Évaluer les critères

Pour chaque critère défini dans le gate (ou dans les contrats) :

```markdown
| Critère | Statut | Preuve |
|---|---|---|
| Gates G0-G7 tous PASS | ✓ / ✗ | docs/evidence/[slug]/INDEX.md |
| Evidence package complet | ✓ / ✗ | INDEX.md présent |
| Risques score ≥ 6 mitigés | ✓ / ✗ | RISKS.md |
| DoD satisfait ligne par ligne | ✓ / ✗ | Mission file |
| Tests passés (zéro rouge) | ✓ / ✗ | logs/test-results.txt |
```

---

## Step 3 — Vérifier le trigger HITL

Consulter ASEF-HITL.md section "13 triggers".

Si un trigger HITL-OBLIGATOIRE est actif :
→ Ne pas décider seul.
→ Préparer la notification HITL (format dans ASEF-HITL.md section 3).
→ Envoyer la notification et attendre la réponse humaine.
→ Bloquer le pipeline pendant l'attente.

Si aucun trigger actif :
→ DecisionAgent peut décider en autonomie sur les sujets non critiques.

---

## Step 4 — Documenter la décision

Dans DECISIONS.md :

```markdown
## [YYYY-MM-DD] — [Titre de la décision Go/No-Go]

**Type** : GO | NO-GO | CONDITIONAL GO | BLOCKED
**Contexte** : [Situation]
**Critères évalués** : [Référence au gate ou à l'evidence]
**Décision** : [Ce qui a été choisi]
**Raison** : [Pourquoi]
**Conditions** : [Si CONDITIONAL GO]
**Validation** : [Agent autonome / Humain : [identité] le [date]]
**Réversibilité** : Réversible | Irréversible
```

---

## Step 5 — Actions post-décision

### Si GO
- Continuer le pipeline.
- Mettre à jour SESSION_LOG.md.
- Archiver l'evidence package si c'est la décision finale.

### Si NO-GO
- Arrêter le pipeline.
- Documenter les raisons dans SESSION_LOG.md.
- Déplacer la mission vers `missions/blocked/` ou `missions/archived/`.
- Communiquer les blocages à l'équipe.

### Si CONDITIONAL GO
- Lister les conditions dans DECISIONS.md.
- Assigner les conditions à des responsables.
- Définir une deadline de vérification des conditions.
- Continuer seulement après vérification de chaque condition.

### Si BLOCKED
- Identifier la cause du blocage.
- Escalader si cause externe (HITL si applicable).
- Déplacer la mission vers `missions/blocked/`.

---

## Checklist Go/No-Go

```
□ Type de décision identifié
□ Critères évalués avec preuves
□ Trigger HITL vérifié
□ Si HITL actif : notification envoyée et réponse reçue
□ Décision documentée dans DECISIONS.md
□ Actions post-décision exécutées
□ SESSION_LOG.md mis à jour
```
