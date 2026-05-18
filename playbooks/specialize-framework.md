# Playbook : Spécialiser un framework ASEF (Domain Layer)

> Applicable quand ASEF-Core doit être étendu pour un domaine métier vertical.
> Version 1.0 · 2026-05-18

---

## Principe d'héritage

```
ASEF-Core (universal primitives)
    └── ASEF-Domain (vertical specialization)
            └── ASEF-Instance (project-specific)
```

Un framework Domain **hérite** des primitives Core sans les réimplémenter.
Il **spécialise** les agents, gates et workflows pour son domaine.

---

## Step 1 — Déclarer l'héritage

Dans le fichier `domains/[domaine]/ASEF-[NOM]/PURPOSE.md` :

```markdown
## Héritage ASEF-Core

Ce framework hérite des primitives universelles suivantes :

| Primitif Core | Hérité ? | Spécialisations |
|---|---|---|
| ASEF-Core (orchestration) | ✓ | Ajoute [Agent1], [Agent2] |
| ASEF-Gates (G0-G9) | ✓ | G3 spécialisé : [critère domaine] |
| ASEF-Evidence | ✓ | Ajoute type ARTIFACT spécifique |
| ASEF-Memory | ✓ | Mémoire domaine dans memory/[domaine]/ |
| ASEF-Risk | ✓ | Ajoute catégorie R-[DOMAINE] |
| ASEF-HITL | ✓ | Ajoute HITL-14 : [trigger domaine] |
| ASEF-Workflow | ✓ | Ajoute workflow WF-[DOMAINE] |
| ASEF-Decision | ✓ | Aucune divergence |
| ASEF-AgentGov | ✓ | Gouverne les agents domaine |
| ASEF-Audit | ✓ | Ajoute Q-15 : [question domaine] |

## Divergences
[Si divergence : ADR requis — Référence ADR-XXXX]
[Si aucune divergence : "Pas de divergence avec ASEF-Core"]
```

---

## Step 2 — Spécialiser les gates

Copier le template G0-G9 de `core/ASEF-Gates.md` et ajouter les critères domaine-spécifiques.

**Règle** : les critères Core ne peuvent pas être retirés. On peut seulement en ajouter.

Créer `domains/[domaine]/ASEF-[NOM]/GATES.md` :
```markdown
# Gates — ASEF-[NOM]

[Hérite de ASEF-Gates.md G0-G9]

## Critères domaine additionnels

### G3 — Contrôle standard (hérité)
**Ajout domaine** :
| Critère | Statut | Note |
|---|---|---|
| [Critère domaine 1] | ✓/✗ | |
```

---

## Step 3 — Ajouter des agents domaine

Pour chaque agent domaine spécialisé :

1. Créer `agents/domains/[domaine]/[NOM]-AGENT.md`.
2. Utiliser le format de contrat de `core/ASEF-AgentGov.md`.
3. Déclarer explicitement l'agent Core parent (si applicable).
4. Ajouter dans `registry/agents.registry.json`.

```json
{
  "id": "ASEF-[DOMAINE]-[NOM]-AGENT",
  "parent": "CoreOrchestratorAgent",
  "domaine": "[domaine]",
  "version": "0.1.0",
  "statut": "ACTIVÉ"
}
```

---

## Step 4 — Publier le framework

```
□ PURPOSE.md avec héritage déclaré
□ SCOPE.md avec IN/OUT précis
□ README.md avec quickstart ≤ 5 étapes
□ GATES.md avec critères domaine
□ Agents déclarés dans registry
□ Divergences documentées dans ADR (si applicable)
□ Framework ajouté dans ROADMAP.md
□ CHANGELOG.md mis à jour
```

---

## Erreurs courantes à éviter

| Erreur | Conséquence | Correction |
|---|---|---|
| Réimplémenter une primitive Core | Désynchronisation lors d'updates Core | Hériter, ne pas copier |
| Diverger sans ADR | Incohérence non tracée | ADR obligatoire avant toute divergence |
| Créer un agent sans contrat | Comportement imprévisible | Contrat complet requis |
| Oublier d'ajouter dans registry | Agent non découvrable | Toujours mettre à jour registry |
