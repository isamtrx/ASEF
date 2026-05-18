# ASEF-Risk — Gestion des risques systémique

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core

---

## 1. Principe

Tout système opérationnel génère des risques. ASEF les traite par défaut.
RiskAgent identifie, score et suit les risques à chaque cycle d'exécution.
Un risque ignoré est une violation de G2.

---

## 2. Les 9 catégories de risques ASEF

| Code | Catégorie | Exemples |
|---|---|---|
| `R-SCOPE` | Scope creep / périmètre flottant | Tâche qui s'étend, périmètre ambigu |
| `R-TECH` | Risque technique | Dette technique, dépendance fragile, absence de tests |
| `R-SEC` | Risque sécurité | CVE non patchée, secret exposé, accès trop larges |
| `R-DATA` | Risque données | PII mal protégée, perte de données, corruption |
| `R-DEPEND` | Dépendance externe | API tierce instable, fournisseur unique, outil non maintenu |
| `R-GOV` | Gouvernance | Décision non tracée, gate sauté, agent hors permissions |
| `R-HUMAN` | Facteur humain | Approbation manquante, désaccord équipe, compétence manquante |
| `R-LEGAL` | Légal / Conformité | RGPD, licence incompatible, contrat ambigu |
| `R-PERF` | Performance / Scalabilité | Latence, charge, SLA non respecté |

---

## 3. Matrice de scoring Probabilité × Impact

**Score = Probabilité (1-3) × Impact (1-3)**

| | Impact 1 (Mineur) | Impact 2 (Modéré) | Impact 3 (Majeur) |
|---|---|---|---|
| **Prob 1 (Faible)** | 1 — WATCH | 2 — WATCH | 3 — MONITOR |
| **Prob 2 (Moyenne)** | 2 — WATCH | 4 — MONITOR | 6 — MITIGATE |
| **Prob 3 (Haute)** | 3 — MONITOR | 6 — MITIGATE | 9 — CRITICAL |

| Score | Niveau | Action requise |
|---|---|---|
| 1-2 | WATCH | Documenter, surveiller |
| 3-4 | MONITOR | Surveiller activement, mitigation optionnelle |
| 6 | MITIGATE | Plan de mitigation obligatoire avant G6 |
| 9 | CRITICAL | Escalade humaine immédiate, pipeline bloqué |

---

## 4. Format du registre de risques

```markdown
## Registre de risques — [Nom du framework / projet]
Mis à jour le : YYYY-MM-DD

| ID | Catégorie | Description | Prob | Impact | Score | Statut | Mitigation |
|---|---|---|---|---|---|---|---|
| R-001 | R-SEC | CVE critique dans dep X | 2 | 3 | 6 | MITIGATE | Patch en cours — deadline YYYY-MM-DD |
| R-002 | R-SCOPE | Périmètre imprécis sur module Y | 1 | 2 | 2 | WATCH | Clarification demandée |
| R-003 | R-HUMAN | Approbation humaine non obtenue | 3 | 3 | 9 | CRITICAL | ESCALADE HUMAINE — en attente |
```

---

## 5. Règles RiskAgent

1. **Identifier ≥ 1 risque pour les tâches CRITICAL et HIGH.** Une tâche sans risque identifié = analyse non faite.
2. **Scorer chaque risque.** Pas de risque sans score.
3. **Plan de mitigation pour score ≥ 6.** Documenté avant G6.
4. **Escalade pour score 9.** Pipeline bloqué jusqu'à validation humaine.
5. **Mettre à jour le registre en fin de session.** Les risques résolus sont marqués CLOSED, pas supprimés.

---

## 6. Risques systémiques ASEF (toujours évaluer)

Ces risques doivent être évalués dans toute instance ASEF :

| Risque | Score par défaut | Mitigation standard |
|---|---|---|
| Gate sauté sans justification | R-GOV score 6 | Revue du pipeline + ADR |
| Décision non tracée | R-GOV score 4 | Ajout dans DECISIONS.md |
| Secret détecté dans un fichier | R-SEC score 9 | Arrêt immédiat, rotation, investigation |
| Preuve inventée | R-GOV score 9 | Arrêt immédiat, escalade humaine |
| Agent hors permissions | R-GOV score 6 | Arrêt, revue des permissions |
| Prompt injection détectée | R-SEC score 9 | Arrêt immédiat, signalement |
