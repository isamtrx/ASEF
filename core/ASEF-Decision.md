# ASEF-Decision — Décisions, ADR, Go/No-Go, Exceptions

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core, ASEF-HITL

---

## 1. Principe

**Les agents recommandent. Les humains décident sur les sujets critiques.**

Toute décision structurante est tracée dans DECISIONS.md avec :
- le contexte qui l'a rendue nécessaire ;
- les options évaluées ;
- le choix retenu et sa justification ;
- les conséquences attendues.

Une décision non tracée n'existe pas officiellement.

---

## 2. Les 6 types de décision

| Type | Description | Décideur |
|---|---|---|
| `GO` | Validation — continuer | Agent autonome ou humain |
| `NO-GO` | Blocage — arrêter | Agent autonome ou humain |
| `CONDITIONAL GO` | Validation sous conditions | Agent ou humain, conditions tracées |
| `BLOCKED` | Bloquage pour manque d'information ou conflit | Agent, humain requis pour débloquer |
| `ADR` | Architecture Decision Record — décision structurante | Humain obligatoire |
| `EXCEPTION` | Dérogation à une règle ASEF | Humain obligatoire |

---

## 3. Triggers HITL pour les décisions

| Type | Trigger HITL |
|---|---|
| GO sur livraison en production | HITL-01 OBLIGATOIRE |
| NO-GO sur tâche critique | HITL recommandé (documentation) |
| CONDITIONAL GO avec impact sécurité | HITL-06 ou HITL-05 si applicable |
| ADR sur architecture | HITL-09 RECOMMANDÉ |
| EXCEPTION à un gate | HITL-02 OBLIGATOIRE |
| EXCEPTION à AGENTS.md | Validation humaine OBLIGATOIRE |

---

## 4. Format de décision GO/NO-GO

```markdown
## [YYYY-MM-DD] — [Titre de la décision]

**Type** : GO | NO-GO | CONDITIONAL GO | BLOCKED
**Contexte** : [Situation qui a rendu la décision nécessaire]
**Options évaluées** :
1. [Option A] — Avantages : [...] / Risques : [...]
2. [Option B] — Avantages : [...] / Risques : [...]
**Décision** : [Ce qui a été choisi]
**Raison** : [Pourquoi cette option]
**Conditions** : [Si CONDITIONAL GO — les conditions exactes]
**Conséquences** : [Impacts positifs et négatifs attendus]
**Validation** : [Agent autonome / Humain : [identité] le [date]]
**Réversibilité** : Réversible | Irréversible
```

---

## 5. Format ADR (Architecture Decision Record)

```markdown
# ADR-[XXXX] — [Titre]

**Date** : YYYY-MM-DD
**Statut** : Proposé | Validé | Obsolète | Remplacé par ADR-[XXXX]

## Contexte
[Pourquoi cette décision est nécessaire. Quel problème résout-elle ?]

## Options considérées
### Option 1 — [Titre]
[Description + Avantages + Inconvénients]

### Option 2 — [Titre]
[Description + Avantages + Inconvénients]

## Décision
[Ce qui a été choisi]

## Raison
[Pourquoi cette option — référencer les critères de choix]

## Conséquences positives
[Ce que cette décision améliore]

## Conséquences négatives / Compromis
[Ce que cette décision sacrifie ou complique]

## Réversibilité
Réversible | Irréversible | Partiellement réversible

## Validation humaine
[Qui a validé, quand — ou "N/A si décision purement technique agentique"]
```

---

## 6. Format EXCEPTION

```markdown
## EXCEPTION-[XXXX] — [Titre]

**Date** : YYYY-MM-DD
**Règle dérogée** : [Référence exacte dans AGENTS.md, MANIFEST.md ou quality gate]
**Raison de la dérogation** : [Pourquoi la règle ne peut pas être appliquée ici]
**Risque accepté** : [Ce qu'on accepte de risquer]
**Mesures compensatoires** : [Ce qu'on fait à la place pour mitiger]
**Durée de validité** : [Jusqu'à quelle date ou condition cette exception est valide]
**Validation humaine** : [Obligatoire — identité + date]
**Clôture prévue** : [Comment et quand on revient à la règle normale]
```

---

## 7. Règles DecisionAgent

1. **Jamais décider seul sur un sujet HITL-OBLIGATOIRE.**
2. **Toujours présenter options avant recommandation.** Une recommandation sans options est de la décision déguisée.
3. **Documenter avant d'agir.** La décision est dans DECISIONS.md avant que l'action soit prise.
4. **Tracer les décisions NO-GO aussi.** Un refus est une décision.
5. **Les exceptions sont rares.** Si on crée plus de 2 exceptions par sprint, c'est une règle qui ne convient pas — proposer une révision via ADR.

---

## 8. Checklist DecisionAgent

```
□ Type de décision identifié
□ Contexte documenté
□ Options évaluées (≥ 2)
□ Recommandation formulée
□ Trigger HITL évalué
□ Validation humaine obtenue si HITL-OBLIGATOIRE
□ Décision formalisée dans DECISIONS.md
□ Conséquences documentées
□ Réversibilité précisée
```
