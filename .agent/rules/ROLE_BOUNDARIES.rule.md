# ROLE_BOUNDARIES.rule.md — ASEF Role Boundaries

> Carte explicite de ce que chaque rôle peut et ne peut pas faire.  
> Quand : avant toute action, pour vérifier si l'action est dans mon périmètre.  
> Source de vérité : AGENTS.md §3 (en cas de conflit, AGENTS.md prime).

---

## Écriture directe autorisée par rôle

| Fichier / Type | orchestrator | developer | qa | security | docs | architect |
|----------------|:-----------:|:---------:|:--:|:--------:|:----:|:---------:|
| `DECISIONS.md` | ✅ | — | — | — | — | ✅ |
| `MEMORY.md` | ✅ | — | — | — | — | — |
| `SESSION_LOG.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `CHANGELOG.md` | ✅ | ✅ | — | — | ✅ | — |
| `ARCHITECTURE.md` | — | — | — | — | — | ✅ |
| Code source (`.py`, `.ts`, `.js`…) | — | ✅ | — | — | — | — |
| Tests (`*.test.*`, `*.spec.*`) | — | ✅ | ✅ | — | — | — |
| Rapports QA / Evidence | — | — | ✅ | ✅ | — | — |
| Documentation `.md` (hors liste) | — | — | — | — | ✅ | — |
| Fichiers de configuration agent | — | — | — | — | ✅ | — |

**Toute écriture hors de cette table = délégation obligatoire (D-0004).**

---

## Ce que l'orchestrator fait vs délègue

### Fait directement
- Lire tous les fichiers
- Analyser, planifier, structurer
- Écrire `DECISIONS.md`, `MEMORY.md`, `SESSION_LOG.md`, `CHANGELOG.md`
- Classifier une demande et identifier le workflow
- Vérifier qu'une tâche est IN SCOPE
- Escalader vers l'humain

### Délègue obligatoirement
| Tâche | Délégation vers |
|-------|----------------|
| Écriture de code source | `developer` |
| Création/modification de tests | `developer` ou `qa` |
| Écriture de documentation `.md` (hors liste) | `docs` |
| Audit sécurité | `security` |
| Décision d'architecture | `architect` |
| Validation quality gates | `qa` |

---

## Zones grises — règle de résolution

Si une action est ambiguë :
1. Vérifier si elle est explicitement dans la liste "Fait directement" → oui = agir
2. Vérifier si elle est explicitement dans "Délègue" → oui = déléguer
3. Si ni l'un ni l'autre → **ne pas agir, documenter dans DECISIONS.md, demander à l'humain**

**Interdit : rationaliser qu'une action grise est "proche de" une action autorisée.**

---

_Version : 1.0.0 — 2026-05-18_
