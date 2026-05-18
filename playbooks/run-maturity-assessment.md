# Playbook : Évaluer la maturité d'un framework

> Applicable à tout audit de maturité d'une instance ou d'un framework ASEF.
> Version 1.0 · 2026-05-18

---

## Niveaux de maturité ASEF

| Niveau | Nom | Description |
|---|---|---|
| 1 | INITIAL | Structure minimale présente, pas d'exécution réelle |
| 2 | DÉFINI | Agents définis, gates déclarés, pas encore opérationnels |
| 3 | OPÉRATIONNEL | Pipeline exécutable de bout en bout, preuves produites |
| 4 | GOUVERNÉ | HITL actif, memory systémique, audits réguliers |
| 5 | OPTIMISÉ | Amélioration continue prouvée, framework stable en production |

---

## Étape 1 — Évaluation des fichiers obligatoires

```
□ AGENTS.md présent et complet (constitution)
□ MANIFEST.md présent (12 garanties)
□ SCOPE.md présent (IN/OUT définis)
□ DECISIONS.md présent (décisions tracées)
□ MEMORY.md présent et à jour
□ SESSION_LOG.md présent et continu
□ LESSONS_LEARNED.md présent
□ CHANGELOG.md présent
□ docs/quality/QUALITY_GATES.md présent
```

Score fichiers : [X/9]
- 7-9 : Niveau 2+
- 4-6 : Niveau 1-2
- < 4 : Niveau 1

---

## Étape 2 — Évaluation des gates

```
□ 10 gates G0-G9 définis dans QUALITY_GATES.md
□ Chaque gate a des critères mesurables
□ Chaque gate a un responsable agent
□ Gates bloquants identifiés (≥ 5)
□ Preuve d'un cycle complet G0-G9 dans docs/evidence/
```

Score gates : [X/5]
- 5 : Niveau 3+
- 3-4 : Niveau 2-3
- < 3 : Niveau 1-2

---

## Étape 3 — Évaluation de la mémoire systémique

```
□ MEMORY.md reflète l'état actuel (pas l'historique)
□ SESSION_LOG.md est continu (pas de gaps > 2 semaines)
□ DECISIONS.md contient des décisions récentes tracées
□ LESSONS_LEARNED.md a au moins 1 entrée récente (dernier mois)
□ MEMORY.md ≠ CHANGELOG.md (pas de confusion mémoire/historique)
```

Score mémoire : [X/5]
- 5 : Niveau 4+
- 3-4 : Niveau 3
- < 3 : Niveau 1-2

---

## Étape 4 — Évaluation HITL

```
□ 13 triggers HITL définis ou hérités de core/ASEF-HITL.md
□ Au moins 1 validation humaine documentée dans DECISIONS.md
□ Aucun déploiement en production sans HITL-01
□ Exceptions documentées dans EXCEPTIONS.md ou DECISIONS.md
```

Score HITL : [X/4]
- 4 : Niveau 4+
- 2-3 : Niveau 3
- < 2 : Niveau 1-2

---

## Calcul du score global

```
Score total = (score fichiers × 2) + (score gates × 3) + (score mémoire × 2) + (score HITL × 3)
Max = 18 + 15 + 10 + 12 = 55

Niveau 5 (OPTIMISÉ)   : score ≥ 50 + preuve d'amélioration continue dans LESSONS_LEARNED
Niveau 4 (GOUVERNÉ)   : score 40-49
Niveau 3 (OPÉRATIONNEL): score 28-39
Niveau 2 (DÉFINI)     : score 15-27
Niveau 1 (INITIAL)    : score < 15
```

---

## Recommandations par niveau

### Passer de 1 à 2
- Compléter les 9 fichiers obligatoires.
- Définir les 10 gates avec critères.
- Déclarer les agents avec contrats.

### Passer de 2 à 3
- Exécuter un cycle complet G0-G9.
- Produire un evidence package.
- Prouver que les gates bloquent réellement.

### Passer de 3 à 4
- Activer les triggers HITL.
- Maintenir MEMORY.md en continu.
- Documenter 5+ décisions dans DECISIONS.md.

### Passer de 4 à 5
- 3+ cycles complets avec evidence packages.
- LESSONS_LEARNED.md avec 5+ leçons appliquées.
- Aucune violation de MANIFEST dans les 3 derniers cycles.
