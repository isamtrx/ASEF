# ASEF-Gates — Quality gates universels G0-G9

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core, ASEF-Evidence

---

## Principe

Un gate est un **point de contrôle bloquant**.
Si un gate est FAIL ou BLOCKED, le pipeline s'arrête. Toujours.
La seule exception est une validation humaine documentée dans DECISIONS.md.

---

## G0 — Intake

**Question** : La demande est-elle recevable ?

| Critère | Vérification |
|---|---|
| Demande compréhensible | Oui — ambiguïtés résolues ou escaladées |
| Demandeur identifié | Oui — source connue |
| Domaine couvert par SCOPE.md | Oui — IN scope |
| Priorité assignée | Oui — CRITICAL / HIGH / MEDIUM / LOW |

**Responsable** : GatekeeperAgent + CoreOrchestratorAgent
**Sortie** : PASS → créer la tâche / FAIL → retour au demandeur / BLOCKED → escalade humaine

---

## G1 — Scope

**Question** : Le périmètre est-il clairement défini ?

| Critère | Vérification |
|---|---|
| Frontières IN/OUT explicites | Oui |
| Aucune zone d'ombre non documentée | Oui |
| SCOPE.md consulté | Oui |
| DoD ≤ 8 lignes produit | Oui |

**Responsable** : ScopeAnalystAgent
**Sortie** : PASS → continuer / FAIL → repréciser le périmètre / BLOCKED → modification SCOPE.md nécessaire (humain)

---

## G2 — Risques

**Question** : Les risques ont-ils été identifiés et traités ?

| Critère | Vérification |
|---|---|
| Risques identifiés (≥ 1 si CRITICAL/HIGH) | Oui |
| Chaque risque scoré (Probabilité × Impact) | Oui |
| Mitigation documentée pour risques ≥ 6 | Oui |
| Risques résiduels ≥ 6 escaladés si non mitigés | Oui |

**Responsable** : RiskAgent
**Sortie** : PASS → continuer / FAIL → compléter le registre / BLOCKED → risque non mitigé critique

---

## G3 — Workflow

**Question** : La chaîne opérationnelle est-elle complète ?

| Critère | Vérification |
|---|---|
| Toutes les étapes identifiées | Oui |
| Responsable pour chaque étape | Oui |
| Dépendances documentées | Oui |
| Points de validation humaine (HITL) identifiés | Oui |

**Responsable** : WorkflowDesignerAgent
**Sortie** : PASS → continuer / FAIL → compléter le workflow

---

## G4 — Livrables définis

**Question** : Sait-on ce qui doit être produit ?

| Critère | Vérification |
|---|---|
| Liste des livrables explicite | Oui |
| Format de chaque livrable défini | Oui |
| Destinataires identifiés | Oui |
| Critères d'acceptation définis | Oui |

**Responsable** : GatekeeperAgent
**Sortie** : PASS → continuer / FAIL → préciser les livrables

---

## G5 — Preuves définies

**Question** : Sait-on quelles preuves seront nécessaires ?

| Critère | Vérification |
|---|---|
| Types de preuves requis définis | Oui |
| Sources des preuves identifiées | Oui |
| Dossier evidence pré-créé | Oui |
| Anti-hallucination activé | Oui |

**Responsable** : EvidenceAgent
**Sortie** : PASS → continuer / FAIL → définir les preuves avant d'exécuter

---

## G6 — Exécution conforme

**Question** : L'exécution a-t-elle été réalisée conformément au workflow ?

| Critère | Vérification |
|---|---|
| Toutes les étapes du workflow exécutées | Oui |
| Aucune étape sautée sans justification | Oui |
| Preuves collectées en temps réel | Oui |
| Anomalies documentées dans SESSION_LOG.md | Oui |

**Responsable** : CoreOrchestratorAgent + EvidenceAgent
**Sortie** : PASS → continuer / FAIL → reprendre les étapes manquantes / BLOCKED → escalade

---

## G7 — Evidence package

**Question** : Le package de preuves est-il complet et valide ?

| Critère | Vérification |
|---|---|
| INDEX.md présent dans docs/evidence/YYYY-MM-DD_slug/ | Oui |
| Toutes les preuves définies en G5 collectées | Oui |
| Aucune preuve inventée ou approximée | Oui |
| AuditAgent a validé la cohérence | Oui |
| Archivage effectué | Oui |

**Responsable** : EvidenceAgent + AuditAgent
**Sortie** : PASS → continuer / FAIL → compléter le package / BLOCKED → preuve non disponible (escalade)

---

## G8 — Décision

**Question** : La décision finale est-elle prise et tracée ?

| Critère | Vérification |
|---|---|
| Type de décision identifié (GO / NO-GO / CONDITIONAL / BLOCKED) | Oui |
| Fiche de décision dans DECISIONS.md | Oui |
| Validation humaine si trigger HITL actif | Oui |
| Conséquences documentées | Oui |

**Responsable** : DecisionAgent + HumanApprovalAgent
**Sortie** : GO → livrer / NO-GO → annuler / CONDITIONAL GO → conditions définies / BLOCKED → escalade

---

## G9 — Mémoire

**Question** : Les apprentissages ont-ils été consolidés ?

| Critère | Vérification |
|---|---|
| SESSION_LOG.md mis à jour | Oui |
| MEMORY.md reflète l'état stabilisé | Oui |
| LESSONS_LEARNED.md complété si incident | Oui |
| CHANGELOG.md mis à jour si livrable | Oui |
| DECISIONS.md mis à jour si décision structurante | Oui |

**Responsable** : MemoryAgent
**Sortie** : PASS → cycle terminé / FAIL → compléter la mémoire avant archivage

---

## Matrice de sévérité des gates

| Gate | Bloquant | Déclencheur HITL | Urgence |
|---|---|---|---|
| G0 | Oui | Toujours si FAIL ou hors scope | Immédiate |
| G1 | Oui | Si modification SCOPE.md nécessaire | Haute |
| G2 | Oui | Si risque résiduel CRITICAL non mitigé | Haute |
| G3 | Non | Non | Normale |
| G4 | Non | Non | Normale |
| G5 | Non | Non | Normale |
| G6 | Oui | Si anomalie critique détectée | Haute |
| G7 | Oui | Si preuve non disponible | Haute |
| G8 | Oui | Toujours si trigger HITL actif | Immédiate |
| G9 | Non | Non | Normale |
