# ASEF-Workflow — Chaînes opérationnelles

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core

---

## 1. Définitions

**Workflow** : Séquence ordonnée d'étapes produisant un livrable.
**Étape** : Unité de travail assignée à un agent avec entrées, sorties, critères de validation.
**Gate** : Point de contrôle bloquant entre deux étapes.
**Dépendance** : Étape B ne peut démarrer que si étape A est terminée.

---

## 2. Statuts d'une étape

| Statut | Description |
|---|---|
| `NOT_STARTED` | Étape non démarrée (dépendances non satisfaites) |
| `IN_PROGRESS` | Étape en cours d'exécution |
| `BLOCKED` | Étape bloquée (gate FAIL ou HITL en attente) |
| `PENDING_HUMAN` | Étape en attente de validation humaine |
| `DONE` | Étape terminée avec preuves |
| `SKIPPED` | Étape sautée (justification obligatoire dans SESSION_LOG.md) |
| `FAILED` | Étape échouée (escalade obligatoire) |

**Règle** : Une étape `SKIPPED` sans justification = violation MANIFEST G-03.
**Règle** : Une étape `FAILED` sans escalade = violation MANIFEST G-03.

---

## 3. Workflow standard WF-INTAKE

Applicable à toute nouvelle tâche ou demande entrant dans le système.

```
Step 1 — Réception de la demande
  Responsable : CoreOrchestratorAgent
  Entrée : Demande brute
  Sortie : Fiche tâche structurée
  Gate : G0 (intake recevable ?)

Step 2 — Analyse du scope
  Responsable : ScopeAnalystAgent
  Entrée : Fiche tâche + SCOPE.md
  Sortie : Rapport scope IN/OUT/AMBIGU
  Gate : G1 (périmètre validé ?)

Step 3 — Analyse des risques
  Responsable : RiskAgent
  Entrée : Fiche tâche + contexte
  Sortie : Registre risques initial
  Gate : G2 (risques gérés ?)

Step 4 — Conception du workflow
  Responsable : WorkflowDesignerAgent
  Entrée : Fiche tâche validée + agents disponibles
  Sortie : Plan d'exécution séquencé
  Gate : G3 (workflow complet ?)

Step 5 — Définition des livrables et preuves
  Responsable : GatekeeperAgent + EvidenceAgent
  Entrée : Plan d'exécution
  Sortie : Liste livrables + dossier evidence pré-créé
  Gate : G4 + G5
```

---

## 4. Workflow standard WF-EXECUTION

Applicable à l'exécution d'une tâche validée en WF-INTAKE.

```
Step 6 — Exécution
  Responsable : Agents spécialisés + EvidenceAgent
  Entrée : Plan WF-INTAKE validé
  Sortie : Livrables + preuves collectées en temps réel
  Gate : G6 (exécution conforme ?)

Step 7 — Collecte evidence package
  Responsable : EvidenceAgent + AuditAgent
  Entrée : Sorties de toutes les étapes
  Sortie : Evidence package complet (INDEX.md + preuves)
  Gate : G7 (evidence package valide ?)

Step 8 — Décision
  Responsable : DecisionAgent + HumanApprovalAgent
  Entrée : Evidence package + analyse risques finaux
  Sortie : GO | NO-GO | CONDITIONAL GO | BLOCKED
  Gate : G8 (décision tracée ?)

Step 9 — Mémoire et archivage
  Responsable : MemoryAgent
  Entrée : SESSION_LOG.md complet, décisions, apprentissages
  Sortie : MEMORY.md mis à jour, LESSONS_LEARNED.md, archive
  Gate : G9 (mémoire consolidée ?)
```

---

## 5. Règles de composition de workflow

1. **Tout workflow doit avoir un gate entre chaque phase majeure.**
2. **Chaque étape a exactement un responsable principal.**
3. **Les HITL sont planifiés dans le workflow, pas découverts en cours.**
4. **Un workflow peut avoir des branches** (si condition X alors step A sinon step B).
5. **Les étapes parallèles sont possibles si sans dépendances croisées.**
6. **Tout saut d'étape nécessite une justification dans SESSION_LOG.md.**

---

## 6. Format d'une étape de workflow

```markdown
## Step [N] — [Nom de l'étape]

**Statut** : NOT_STARTED | IN_PROGRESS | BLOCKED | PENDING_HUMAN | DONE | SKIPPED | FAILED
**Responsable** : [Agent ou équipe]
**Dépendances** : Step [X], Step [Y]
**Entrées** : [Fichiers ou outputs requis]
**Sorties attendues** : [Fichiers ou résultats produits]
**Gate** : [G0-G9 ou "Aucun"]
**HITL** : [Oui / Non — trigger si Oui]
**Durée estimée** : [Optionnel]
**Notes** : [Contexte ou contraintes spécifiques]
```
