# CONTEXT_BUDGET — Gestion du budget de contexte

> Politique de gestion de la fenêtre de contexte par type de tâche.
> Version 1.0 · 2026-05-18

---

## 1. Budgets par type de tâche

| Type de tâche | Budget contexte max | Justification |
|---|---|---|
| `bugfix` | ≤ 30% du contexte | Portée chirurgicale, peu de fichiers nécessaires |
| `feature` | ≤ 50% du contexte | Portée moyenne, quelques modules concernés |
| `audit` | ≤ 70% du contexte | Vue large nécessaire |
| `security` | ≤ 70% du contexte | Analyse transversale |
| `governance` | ≤ 90% du contexte | Lecture quasi-complète des fichiers de gouvernance |
| `release` | ≤ 90% du contexte | Validation complète du pipeline |
| `architecture` | ≤ 70% du contexte | Focus sur docs/ et core/ |

---

## 2. Fichiers toujours chargés (Always-loaded)

Ces fichiers sont chargés en priorité absolue, peu importe la tâche :

```
AGENTS.md             — Constitution et permissions
MEMORY.md             — État courant du projet
SCOPE.md              — Périmètre IN/OUT
DECISIONS.md          — Décisions actives
```

Taille totale estimée de ces fichiers : < 5% du contexte standard.
Ces fichiers ne peuvent pas être omis même si le budget est dépassé.

---

## 3. Règles de chargement adaptatif

### Si budget restant > 50% après always-loaded :
→ Charger le contexte étendu (voir CONTEXT_LOADING.md).

### Si budget restant 20-50% après always-loaded :
→ Charger uniquement les fichiers domaine pertinents à la tâche.
→ Sauter les READMEs et les fichiers de convention.

### Si budget restant < 20% après always-loaded :
→ Charger uniquement QUALITY_GATES.md et les fichiers directement modifiés.
→ Signaler le budget contraint dans SESSION_LOG.md.

---

## 4. Règles de priorisation des fichiers

En cas de contrainte budgétaire, prioriser dans cet ordre :

1. Fichiers always-loaded (AGENTS.md, MEMORY.md, SCOPE.md, DECISIONS.md)
2. Fichier(s) directement concerné(s) par la tâche
3. Tests liés aux fichiers modifiés
4. QUALITY_GATES.md
5. Directives domaine applicables
6. Documentation architecture (docs/ARCHITECTURE.md)
7. Autres fichiers de gouvernance
8. READMEs et conventions (chargement optionnel)

---

## 5. Anti-patterns de gestion de contexte

| Anti-pattern | Impact | Alternative |
|---|---|---|
| Charger tous les fichiers par défaut | Tokens gaspillés, contexte dilué | Chargement sélectif par type de tâche |
| Sauter AGENTS.md pour gagner de la place | Violation constitution | AGENTS.md est toujours chargé |
| Charger docs/evidence/ complet en cours de tâche | Contexte saturé par les preuves passées | Charger uniquement l'INDEX.md du dernier package |
| Ignorer MEMORY.md pour aller plus vite | Perte de continuité | MEMORY.md toujours chargé — est court par conception |

---

## 6. Signaux d'alerte budget contexte

Signaler dans SESSION_LOG.md si :
- Budget contexte > 80% utilisé avant la phase G6 (exécution).
- Plus de 20 fichiers chargés sur une tâche `bugfix` ou `feature`.
- Impossible de charger QUALITY_GATES.md dans le budget restant.

Dans ces cas : documenter, reprioriser, ou fragmenter la tâche.
