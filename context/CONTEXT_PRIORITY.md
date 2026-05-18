# CONTEXT_PRIORITY — Ordre de priorité et résolution de conflits

> Règles de priorisation des fichiers de gouvernance en cas de conflit.
> Version 1.0 · 2026-05-18

---

## 1. Ordre de priorité absolu

En cas de conflit entre deux fichiers de gouvernance, la priorité est :

| Priorité | Fichier | Raison |
|---|---|---|
| 1 (plus haute) | `AGENTS.md` | Constitution générale — racine absolue |
| 2 | `MANIFEST.md` | Contrat public — garanties non-négociables |
| 3 | `SCOPE.md` | Périmètre actif — ce qui est IN/OUT |
| 4 | `DECISIONS.md` | Décisions structurantes actives |
| 5 | `core/ASEF-Core.md` | Primitives universelles |
| 6 | `core/ASEF-Gates.md` | Gates universels |
| 7 | `docs/quality/QUALITY_GATES.md` | Gates spécifiques instance |
| 8 | Directives domaine | Instructions spécialisées |
| 9 | `docs/ARCHITECTURE.md` | Architecture courante |
| 10 (plus basse) | Contrats et schemas | Spécifications techniques |

**Règle** : Si AGENTS.md dit X et une directive domaine dit Y (contradictoire),
AGENTS.md prime. Toujours.

---

## 2. Règles de résolution de conflits

### Conflit entre AGENTS.md et tout autre fichier
→ AGENTS.md prime. Le conflit est signalé dans SESSION_LOG.md.
→ Si le conflit est structurel, ouvrir un ADR pour harmoniser.

### Conflit entre SCOPE.md et une demande
→ La demande est hors scope. Escalader à l'humain avec HITL-03.
→ Ne pas modifier SCOPE.md sans ADR et validation humaine.

### Conflit entre DECISIONS.md et une action planifiée
→ La décision dans DECISIONS.md prime.
→ Si la décision est obsolète, ouvrir un ADR pour la réviser.

### Conflit entre une directive domaine et core/ASEF-Core.md
→ core/ASEF-Core.md prime. La directive est un spécialisation, pas une dérogation.
→ Si spécialisation légitime, documenter dans un ADR.

### Conflit entre deux agents sur la même sortie
→ Escalader à CoreOrchestratorAgent.
→ Si non résolu, HITL-11 (conflit non résolu entre agents).

---

## 3. Priorités des directives par type de tâche

### Pour `bugfix` et `feature` (code)
```
AGENTS.md > MANIFEST.md > backend.instructions.md (ou frontend) > QUALITY_GATES.md
```

### Pour `audit` et `security`
```
AGENTS.md > MANIFEST.md > security.instructions.md > ASEF-Audit.md > ASEF-Evidence.md
```

### Pour `governance` et `docs`
```
AGENTS.md > MANIFEST.md > docs.instructions.md > ASEF-Core.md
```

### Pour `ai` et agents
```
AGENTS.md > MANIFEST.md > ai.instructions.md > ASEF-AgentGov.md > ASEF-HITL.md
```

---

## 4. Signaux d'alerte de conflit

Un conflit doit être documenté dans SESSION_LOG.md si :
- Deux fichiers de gouvernance contiennent des instructions contradictoires.
- Une directive de domaine élargit le scope défini dans SCOPE.md.
- Une décision dans DECISIONS.md contredit une règle d'AGENTS.md.
- Un agent reçoit des instructions conflictuelles via deux canaux.

Dans tous ces cas : appliquer l'ordre de priorité de la section 1,
documenter dans SESSION_LOG.md, et proposer une harmonisation.
