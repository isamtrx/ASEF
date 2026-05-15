# DECISIONS.md — ASEF

> Registre des décisions structurantes.  
> 1 responsabilité : tracer le **pourquoi** des décisions, pas le **comment**.  
> Format ADR minimal obligatoire. Voir `docs/adr/ADR-0001-template.md`.

---

## Index des décisions

> **Note de navigation :** Deux espaces de nommage coexistent :
> - **Décisions fondatrices** (ci-dessous, sections D-0001/D-0002/D-0003) : principes architecturaux définis en session d'initialisation, inline dans ce fichier.
> - **ADRs techniques** (docs/adr/) : décisions techniques formelles créées en session de corrections, dans des fichiers séparés.

### Décisions fondatrices (inline)

| ID | Titre | Statut | Date |
|----|-------|--------|------|
| [D-0001](#adr-0001) | Structure documentaire ASEF MVP | Validé | 2026-05-15 |
| [D-0002](#adr-0002) | Principe 1 fichier = 1 responsabilité | Validé | 2026-05-15 |
| [D-0003](#adr-0003) | AGENTS.md comme constitution outil-agnostique | Validé | 2026-05-15 |

### ADRs techniques (docs/adr/)

| ID | Titre | Statut | Date | Fichier |
|----|-------|--------|------|---------|
| ADR-0002 | GitHub Actions comme toolchain CI/CD | Validé | 2026-05-15 | [docs/adr/ADR-0002-ci-cd-github-actions.md](docs/adr/ADR-0002-ci-cd-github-actions.md) |
| ADR-0003 | Gestion des secrets — GitHub Secrets + env vars | Validé | 2026-05-15 | [docs/adr/ADR-0003-secrets-management.md](docs/adr/ADR-0003-secrets-management.md) |
| ADR-0004 | Orchestration multi-agents — protocole handoff | Validé | 2026-05-15 | [docs/adr/ADR-0004-agent-orchestration.md](docs/adr/ADR-0004-agent-orchestration.md) |
| ADR-0005 | Stratégie de branches Git | Validé | 2026-05-15 | [docs/adr/ADR-0005-branching-strategy.md](docs/adr/ADR-0005-branching-strategy.md) |
| ADR-0006 | Modèle de distribution ASEF | Validé | 2026-05-15 | [docs/adr/ADR-0006-distribution-model.md](docs/adr/ADR-0006-distribution-model.md) |

---

## ADR-0001

**Titre :** Structure documentaire ASEF MVP — 22 fichiers core  
**Date :** 2026-05-15  
**Statut :** Validé  

**Contexte :**  
ASEF démarrait sans structure documentaire. Risque de créer des fichiers ad-hoc sans frontières claires, générant de la duplication et de la dette documentaire.

**Options considérées :**
1. Documentation flat (tout dans README.md) — rejeté : non scalable, non auditable
2. Documentation par outil (CLAUDE.md = tout pour Claude) — rejeté : duplication garantie
3. Documentation par responsabilité (1 fichier = 1 objectif) — **retenu**

**Décision :**  
Adopter une architecture documentaire en 9 couches (Produit → Agentique → Architecture → Gouvernance → Qualité → Sécurité → IA → Delivery → Mémoire) avec 22 fichiers MVP et 55 fichiers au total.

**Raison :**  
La séparation par responsabilité garantit qu'un changement dans un domaine n'affecte qu'un fichier, rendant l'audit possible et la maintenance prévisible.

**Conséquences :**
- (+) Audit trail clair par domaine
- (+) Pas de duplication structurelle
- (-) Overhead initial de création des fichiers
- (-) Nécessite discipline de maintenance

**Réversibilité :** Réversible (migration possible vers structure différente avec effort moyen)

---

## ADR-0002

**Titre :** Principe fondateur — 1 fichier = 1 responsabilité = 1 source de vérité  
**Date :** 2026-05-15  
**Statut :** Validé  

**Contexte :**  
Sans règle explicite de non-duplication, les frameworks documentaires dérivent vers des fichiers fourre-tout qui se contredisent.

**Décision :**  
Tout fichier ASEF doit servir exactement un des 10 objectifs : Décider · Cadrer · Construire · Tester · Sécuriser · Auditer · Livrer · Exploiter · Tracer · Améliorer. Si un fichier ne sert aucun de ces objectifs, il est fusionné ou supprimé.

**Raison :**  
La lisibilité, la maintenabilité et l'auditabilité d'un framework documentaire dépendent directement de la clarté des frontières de responsabilité.

**Conséquences :**
- (+) Zéro duplication structurelle
- (+) Un auditeur sait exactement où chercher
- (-) Règle à faire respecter activement (signal de dérive dans SCOPE.md)

**Réversibilité :** Irréversible (c'est un principe fondateur)

---

## ADR-0003

**Titre :** AGENTS.md comme constitution outil-agnostique — prime sur les adaptateurs  
**Date :** 2026-05-15  
**Statut :** Validé  

**Contexte :**  
CLAUDE.md et copilot-instructions.md risquaient de devenir des doublons avec des règles contradictoires selon l'outil utilisé.

**Options considérées :**
1. Un fichier par outil avec toutes les règles — rejeté : duplication et divergence garanties
2. Un fichier constitutionnel outil-agnostique + adaptateurs légers — **retenu**
3. Pas de fichier constitutionnel, règles dans chaque adaptateur — rejeté : incohérence

**Décision :**  
`AGENTS.md` est la constitution générale. `CLAUDE.md` et `copilot-instructions.md` sont des adaptateurs qui référencent `AGENTS.md` sans le dupliquer. En cas de conflit, `AGENTS.md` prime.

**Raison :**  
Garantit la cohérence des règles quel que soit l'outil agent utilisé. Facilite l'ajout de nouveaux outils (Cursor, Aider, Gemini CLI) sans réécrire les règles.

**Conséquences :**
- (+) Cohérence totale entre outils
- (+) Évolutivité vers nouveaux agents
- (-) Deux niveaux de lecture requis au bootstrap

**Réversibilité :** Réversible

---

## Template pour nouvelle décision

```markdown
## ADR-XXXX

**Titre :** [Titre court et précis]  
**Date :** YYYY-MM-DD  
**Statut :** Proposé | Validé | Obsolète | Remplacé par ADR-XXXX  

**Contexte :**  
[Pourquoi cette décision est nécessaire. Quel problème elle résout.]

**Options considérées :**
1. Option A — [résumé + raison rejet/sélection]
2. Option B — [résumé + raison rejet/sélection]

**Décision :**  
[Ce qui a été choisi, en une phrase claire.]

**Raison :**  
[Pourquoi cette option plutôt que les autres.]

**Conséquences :**
- (+) [Impact positif]
- (-) [Impact négatif ou contrainte]

**Réversibilité :** Réversible / Irréversible
```
