# CONTEXT_LOADING — Séquence de chargement du contexte

> Protocole de bootstrap et de chargement adaptatif du contexte agent.
> Version 1.0 · 2026-05-18

---

## 1. Séquence de bootstrap obligatoire

Tout agent doit lire ces fichiers **avant** toute action, dans cet ordre :

```
1. AGENTS.md                          → Constitution et permissions
2. MEMORY.md                          → Contexte actuel
3. SCOPE.md                           → Périmètre (tâche IN scope ?)
4. DECISIONS.md                       → Décisions structurantes actives
5. [Directive domaine applicable]
   → .github/instructions/frontend.instructions.md
   → .github/instructions/backend.instructions.md
   → .github/instructions/qa.instructions.md
   → .github/instructions/security.instructions.md
   → .github/instructions/docs.instructions.md
   → .github/instructions/ai.instructions.md
6. docs/ARCHITECTURE.md               → Si modification technique
7. docs/quality/QUALITY_GATES.md      → Avant toute livraison
```

**Règle absolue** : Un agent qui modifie sans avoir bootstrappé correctement
doit stopper et relire. La vitesse ne justifie pas le saut du bootstrap.

---

## 2. Mode contexte minimal

Applicable pour les tâches `bugfix` rapides ou les corrections de syntaxe.

```
Obligatoire :
  □ AGENTS.md
  □ MEMORY.md
  □ SCOPE.md (section IN/OUT uniquement)

Optionnel selon la tâche :
  □ Fichier directement modifié
  □ Tests liés
```

---

## 3. Mode contexte étendu

Applicable pour les tâches `feature`, `architecture`, `governance`, `release`.

```
Obligatoire :
  □ AGENTS.md
  □ MEMORY.md
  □ SCOPE.md
  □ DECISIONS.md
  □ Directive domaine applicable
  □ docs/ARCHITECTURE.md
  □ docs/quality/QUALITY_GATES.md

Recommandé selon la tâche :
  □ core/ASEF-Core.md (si modification d'un agent ou d'un gate)
  □ core/ASEF-Evidence.md (si livraison)
  □ core/ASEF-HITL.md (si trigger HITL potentiel)
  □ registry/agents.registry.json (si nouveau rôle agent)
  □ docs/adr/ (si décision architecturale)
```

---

## 4. Règles de chargement par type de tâche

### bugfix
```
always-loaded + [fichier bugué] + [tests liés]
```

### feature
```
always-loaded + directive domaine + ARCHITECTURE.md + [fichiers impactés]
```

### audit / security
```
always-loaded + QUALITY_GATES.md + core/ASEF-Evidence.md + core/ASEF-Audit.md
+ [fichiers audités]
```

### governance
```
always-loaded + QUALITY_GATES.md + core/ASEF-Core.md + MANIFEST.md
+ docs/adr/ (si modification ADR)
```

### release
```
always-loaded + QUALITY_GATES.md + core/ASEF-Evidence.md + core/ASEF-HITL.md
+ CHANGELOG.md + docs/evidence/[dernier]/INDEX.md
```

---

## 5. Signaux d'échec du bootstrap

Ces situations indiquent un bootstrap incomplet :

- Agent qui modifie SCOPE.md sans avoir lu AGENTS.md (interdiction).
- Agent qui produit un livrable sans connaître les gates.
- Agent qui pose une question sur le périmètre alors qu'il aurait dû lire SCOPE.md.
- Agent qui ignore une décision active dans DECISIONS.md.

Si l'un de ces signaux est détecté : arrêter, relire le bootstrap, reprendre.
