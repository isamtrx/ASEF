# SLO.md — ASEF

> Source de vérité des objectifs de niveau de service.  
> 1 responsabilité : définir les SLOs, les seuils d'alerte et les budgets d'erreur.  
> Dépend de : OBSERVABILITY.md  
> Ne doit jamais contenir : alertes détaillées (→ OBSERVABILITY.md), procédures d'incident (→ INCIDENT_RESPONSE.md).

---

## Principe

Un SLO (Service Level Objective) est un contrat interne mesurant la fiabilité perçue par les utilisateurs. Il est distinct du SLA (contrat client) mais en est la base technique.

---

## SLOs par service

### Service Principal (API / Application)

| SLO | Objectif | Fenêtre | Alerte |
|-----|---------|---------|--------|
| Disponibilité | ≥ 99,5% | 30 jours glissants | < 99,0% |
| Latence p95 | ≤ 800ms | 1 heure | > 1 200ms |
| Latence p99 | ≤ 2 000ms | 1 heure | > 3 000ms |
| Taux d'erreur | ≤ 1% | 5 minutes | > 5% |

### Pipeline CI/CD

| SLO | Objectif | Fenêtre | Alerte |
|-----|---------|---------|--------|
| Build success rate | ≥ 95% | 7 jours | < 90% |
| Durée du build | ≤ 5 min | Chaque run | > 10 min |
| Time to deploy (staging) | ≤ 15 min | Chaque merge | > 30 min |

### Qualité des agents IA

| SLO | Objectif | Fenêtre | Alerte |
|-----|---------|---------|--------|
| Eval score moyen | ≥ seuil par eval | Chaque release | Régresse > 5% |
| Taux de refus adversarial | 100% | Chaque release | < 100% |
| HITL response time | ≤ 4h en jours ouvrés | Chaque demande | > 8h |

---

## Budgets d'erreur

Le budget d'erreur = (100% - SLO objectif) × temps de la fenêtre.

**Exemple pour disponibilité 99,5% sur 30 jours :**
- Budget = 0,5% × 30 jours × 24h × 60min = **216 minutes** de downtime autorisé

### Règles de consommation du budget

| Budget consommé | Action |
|----------------|--------|
| < 50% | Normal — releases courantes autorisées |
| 50% à 80% | Ralentir les releases risquées, prioriser stabilité |
| > 80% | Freeze des features — corriger la stabilité |
| 100% (épuisé) | Incident déclaré, release bloquée, postmortem obligatoire |

---

## Mesure

Les SLOs sont calculés à partir des métriques définies dans OBSERVABILITY.md.

| Méthode de mesure | Source |
|------------------|--------|
| Disponibilité | `1 - (requests_5xx / total_requests)` sur fenêtre |
| Latence | Histogramme `http_request_duration_ms` percentile |
| Error rate | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(...))` |
| Build success | `build_success / (build_success + build_failure)` |

---

## Révision des SLOs

- **Revue mensuelle** : comparer les SLOs aux valeurs mesurées
- **Révision semestrielle** : ajuster les objectifs selon la maturité du système
- **Post-incident** : vérifier si le SLO doit être renforcé après un incident
- Tout changement de SLO est une décision structurante (ADR dans DECISIONS.md)

---

## SLO Phase MVP (v0.x.x)

Pendant la phase MVP, les SLOs sont assouplis :

| SLO | MVP | Target v1.0 |
|-----|-----|------------|
| Disponibilité | ≥ 99,0% | ≥ 99,5% |
| Latence p95 | ≤ 1 500ms | ≤ 800ms |
| Taux d'erreur | ≤ 2% | ≤ 1% |

Cette distinction est supprimée lors du passage à v1.0.0.
