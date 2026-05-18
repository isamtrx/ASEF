# Playbook : Créer un nouveau framework ASEF

> Applicable quand : un nouveau domaine métier nécessite un framework ASEF vertical.
> Version 1.0 · 2026-05-18

---

## Phase 1 — Cadrage (avant de créer un seul fichier)

Répondre à ces 5 questions. Si une réponse est vague, clarifier avant de continuer.

```
1. Quel problème ce framework résout-il ?
   → Réponse : [1-2 phrases max]

2. Qui sont les utilisateurs / bénéficiaires ?
   → Réponse : [rôles, équipes, contextes]

3. Quels agents spécialisés ce framework nécessite-t-il ?
   → Réponse : [liste des rôles agents, distincts de ASEF-Core]

4. Quels gates G0-G9 sont spécialisés par ce domaine ?
   → Réponse : [liste des gates avec critères domaine spécifiques]

5. Ce framework existe-t-il déjà (dans asef-runtime ou ailleurs) ?
   → Vérification dans domains/ + ROADMAP.md avant de continuer
```

**Vérification d'héritage** :
- Ce framework hérite-t-il d'un framework existant ? → Déclarer dans PURPOSE.md
- Cette fonctionnalité est-elle déjà dans core/ ? → Ne pas la réimplémenter

---

## Phase 2 — Structure minimale

```bash
# Créer la structure dans domains/[slug]/ASEF-[NOM]/
mkdir domains/[domaine]/ASEF-[NOM]
```

Créer les 3 fichiers obligatoires dans cet ordre :

### 1. README.md
```markdown
# ASEF-[NOM] — [Titre du framework]

**Problème résolu** : [1 phrase]
**Domaine** : [Nom du domaine]
**Version** : 0.1.0

## Démarrage rapide
[3 étapes pour utiliser ce framework]

## Liens
- Héritage : [core/ASEF-Core.md]
- Gates : [Lien vers gates spécialisés]
- Agents : [Lien vers définitions agents]
```

### 2. PURPOSE.md
```markdown
# Raison d'être — ASEF-[NOM]

## Problème
[Pourquoi ce framework existe]

## Périmètre
**IN** : [Ce que ce framework couvre]
**OUT** : [Ce que ce framework ne couvre pas]

## Héritage ASEF-Core
Ce framework hérite des frameworks core suivants :
- ASEF-Core (orchestration, primitives)
- ASEF-Evidence (preuves)
- ASEF-Gates (gates G0-G9)
- ASEF-Decision (décisions)
- ASEF-Memory (mémoire)
- ASEF-HITL (validations humaines)

## Divergences avec ASEF-Core
[Liste des écarts — ou "Aucune divergence"]
[Chaque divergence doit avoir un ADR]
```

### 3. SCOPE.md
```markdown
# Périmètre — ASEF-[NOM]

## IN scope
- [Domaine 1]
- [Domaine 2]

## OUT scope
- [Ce qui est exclu explicitement]

## Zones ambiguës
- [Zone X → résolution : [décision]]
```

---

## Phase 3 — Agents

Pour chaque agent spécialisé identifié en Phase 1 :

1. Créer le fichier `agents/[NOM]-AGENT.md` avec le format de contrat (voir ASEF-AgentGov.md).
2. Ajouter l'agent dans `registry/agents.registry.json`.
3. Déclarer les permissions (read / write / execute) précisément.
4. Tester le contrat avec un scénario simple avant de déployer.

---

## Phase 4 — Gates et quality gates

1. Copier la structure G0-G9 de `core/ASEF-Gates.md`.
2. Spécialiser chaque gate avec les critères domaine spécifiques.
3. Créer ou mettre à jour `docs/quality/QUALITY_GATES.md` pour l'instance.
4. Valider que chaque gate a un responsable agent défini.

---

## Phase 5 — Validation du framework

```
□ README.md, PURPOSE.md, SCOPE.md créés
□ Agents définis avec contrats complets
□ Gates G0-G9 spécialisés et documentés
□ Héritage ASEF-Core déclaré dans PURPOSE.md
□ Divergences documentées dans des ADR
□ ROADMAP.md mis à jour (nouveau framework ajouté)
□ CHANGELOG.md mis à jour (section Unreleased)
□ Validation humaine si framework CRITICAL ou productif
```
