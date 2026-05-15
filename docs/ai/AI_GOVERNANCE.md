# AI_GOVERNANCE.md — ASEF

> Source de vérité de la gouvernance de l'IA dans le framework ASEF.  
> 1 responsabilité : définir les cas d'usage autorisés, les obligations HITL et la traçabilité.  
> Dépend de : AGENTS.md, SECURITY.md (§ IA)  
> Ne doit jamais contenir : politique modèles (→ MODEL_POLICY.md), prompts (→ PROMPT_GOVERNANCE.md).

---

## Positionnement

ASEF utilise l'IA générative comme amplificateur de capacité, pas comme décideur autonome. L'IA augmente la productivité de l'ingénieur ; elle ne se substitue pas au jugement humain pour les décisions structurantes.

---

## Cas d'usage autorisés

| Usage | Autorisé | HITL requis | Preuve |
|-------|---------|------------|--------|
| Génération de code | ✓ | Non (mais Gate G3-G5 bloquants) | Rapport CI |
| Génération de tests | ✓ | Non | Rapport CI |
| Mise à jour de documentation | ✓ | Non (vérification post) | Diff markdown |
| Revue de code (aide) | ✓ | Oui (décision humaine) | Approbation PR humaine |
| Refactoring | ✓ | Oui si structurant | ADR si applicable |
| Analyse de sécurité (aide) | ✓ | Oui (décision humaine) | Rapport validé humain |
| Déploiement en production | ✗ | — | Interdit sans Gate 7 |
| Modification de AGENTS.md | ✗ | — | Interdit sans humain |
| Décision d'architecture | Partiel | Obligatoire | ADR validé humain |
| Communication externe | ✗ | — | Toujours via humain |

---

## Human-In-The-Loop (HITL)

### Quand le HITL est obligatoire

1. **Décisions structurantes** : changement de scope, d'architecture, de sécurité → validation Tech Lead
2. **Release production** : Gate 7 — signature humaine explicite
3. **Exceptions quality gates** : EXCEPTIONS.md validé par humain
4. **Incident de sécurité** : toute décision de containment validée par humain
5. **Modification des règles de gouvernance** : AGENTS.md, SCOPE.md, EXCEPTIONS.md

### Ce que le HITL signifie concrètement

- L'humain lit et comprend la décision avant d'approuver
- L'humain peut refuser ou modifier la proposition de l'agent
- L'approbation est tracée (commentaire PR, entrée SESSION_LOG)
- "L'humain a cliqué Approve sans lire" n'est pas un HITL valide

---

## Traçabilité des outputs IA

Tout output IA qui devient un artefact livrable doit être traçable :

| Artefact | Traçabilité requise |
|---------|-------------------|
| Code généré | Commit SHA + pipeline CI + rapport SAST |
| Documentation générée | Commit SHA + diff visible |
| Décision proposée par agent | ADR avec date + responsable humain |
| Prompt modifié | Version dans PROMPT_GOVERNANCE.md |
| Eval score | Rapport archivé avec date et version du prompt |

---

## Données interdites dans le contexte IA

Les éléments suivants ne doivent **jamais** être inclus dans un prompt ou contexte agent :

- Credentials, secrets, tokens (voir SECRETS.md)
- Données personnelles identifiables (RGPD)
- Données contractuelles confidentielles
- Données client non anonymisées

---

## Responsabilité

- L'agent IA propose et exécute dans les limites définies
- L'humain répond des outputs IA qu'il approuve et livre
- "L'IA l'a fait" n'est pas une défense — la responsabilité est celle de l'humain qui a validé

---

## Protocole de handoff inter-agents

Un handoff est le transfert de contexte entre deux agents successifs dans le workflow ASEF (STEP 0-7 de `AGENTS.md §5`).

### Structure d'un handoff

Avant de passer la main à l'agent suivant, l'agent courant doit fournir :

```markdown
## Handoff — [AGENT-XXX] → [AGENT-YYY]

**Tâche accomplie :** [Description en 1-2 lignes]
**DoD partiel :** [Cases cochées du DoD initial]
**Fichiers modifiés :** [Liste des fichiers touchés]
**Contexte critique :** [Ce que l'agent suivant doit absolument savoir]
**Points d'attention :** [Risques identifiés, décisions en suspens]
**Gate validé :** [G0/G1/... — vert ou bloquant]
```

### Règles de handoff

1. **Pas de handoff implicite** — le contexte est toujours explicitement fourni
2. **L'agent recevant valide** — il confirme avoir reçu et compris le contexte avant d'agir
3. **Pas de handoff si gate bloquant** — si le gate de l'étape précédente est rouge, escalader vers l'humain avant de continuer
4. **Traçabilité** — chaque handoff est loggé dans SESSION_LOG.md

### Séquence type

```
AGENT-000 (Orchestrateur humain)
  → AGENT-001 (Developer) : génère code
  → AGENT-002 (Security) : audite le code produit [handoff avec fichiers + contexte]
  → AGENT-003 (Docs) : documente les changements [handoff avec diff + décisions]
  → AGENT-004 (QA) : valide les tests [handoff avec fichiers + rapport sécurité]
  → AGENT-000 : consolide, Gate G6-G7, livre
```

---

## Gouvernance des modèles et fournisseurs

Voir `docs/ai/MODEL_POLICY.md` pour :
- Les modèles autorisés
- Les données pouvant être envoyées à chaque fournisseur
- La politique cloud vs local

---

## Révision de cette politique

Cette politique est révisée :
- À chaque changement majeur des capacités des outils IA utilisés
- À chaque incident lié à un agent IA
- Semestriellement en révision planifiée

Toute évolution génère un ADR dans `docs/adr/`.
