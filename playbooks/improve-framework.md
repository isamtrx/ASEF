# Playbook : Améliorer un framework existant

> Applicable quand un framework ASEF existant nécessite une évolution.
> Version 1.0 · 2026-05-18

---

## Quand utiliser ce playbook

- Un POSTMORTEM ou LESSONS_LEARNED a révélé un gap.
- Un gate fail systématique suggère un problème de définition.
- Un nouveau besoin est hors scope du framework existant.
- Une décision ADR a invalidé une partie du framework.

---

## Phase 1 — Audit de l'état actuel

1. Lire le framework entier (README.md, PURPOSE.md, SCOPE.md, agents, gates).
2. Comparer avec les 12 garanties du MANIFEST.md.
3. Identifier les lacunes :

```markdown
## Gap Analysis

| Garantie MANIFEST | Couvert ? | Preuve / Lacune |
|---|---|---|
| G-01 Scope explicite | Oui | PURPOSE.md §2 |
| G-02 Agents identifiés | Partiel | Agent X non déclaré |
| G-03 Gates bloquants | Non | Gates 4+ manquent de critères |
| ... | ... | ... |
```

4. Documenter les 3 gaps les plus critiques.

---

## Phase 2 — Décision structurante ou amélioration mineure

| Si | Alors |
|---|---|
| La modification change l'architecture ou les permissions | ADR obligatoire dans `docs/adr/` avant toute modification |
| La modification ajoute ou retire un gate bloquant | HITL recommandé |
| La modification change un contrat agent | HITL si l'agent est en production |
| Amélioration cosmétique (exemples, typos, clarifications) | Pas d'ADR, modification directe |

---

## Phase 3 — Implémentation

**Règle chirurgicale** : toucher uniquement ce qui est demandé.

1. Si ADR requis : écrire l'ADR et attendre validation avant de coder.
2. Modifier uniquement les fichiers concernés.
3. Respecter le style et les patterns existants.
4. Mettre à jour les références (si un gate change de numéro, mettre à jour tous les fichiers qui y font référence).

---

## Phase 4 — Validation de la modification

```
□ La modification résout le gap identifié en Phase 1
□ Aucune régression sur les garanties MANIFEST.md non touchées
□ ADR créé si décision structurante (avec statut VALIDÉ)
□ CHANGELOG.md mis à jour (section Unreleased)
□ DECISIONS.md mis à jour si applicable
□ Numéro de version incrémenté dans README.md du framework
```

---

## Phase 5 — Post-amélioration

1. Documenter la leçon dans LESSONS_LEARNED.md :

```markdown
## [YYYY-MM-DD] — [Nom du framework] amélioration

**Gap identifié** : [Description]
**Cause racine** : [Pourquoi le gap existait]
**Modification** : [Ce qui a été changé]
**Validation** : [Comment on sait que ça marche]
```

2. Relancer un maturity assessment (`run-maturity-assessment.md`) pour vérifier que le score a progressé.
3. Mettre à jour SESSION_LOG.md.
