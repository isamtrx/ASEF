# MANIFEST — Ce qu'ASEF garantit à toute instance

> Ce document est le contrat public d'ASEF.
> Toute instance qui se réclame d'ASEF doit respecter ces garanties.
> Version 2.0 — 2026-05-18

---

## Les 12 garanties ASEF

### G-01 — Périmètre explicite
Toute instance ASEF publie un SCOPE.md définissant ce qui est IN et OUT.
Aucune action hors périmètre n'est autorisée sans ADR validé.

### G-02 — Agents identifiés
Tout agent opérant dans une instance ASEF possède :
- un identifiant unique ;
- un rôle précis ;
- des permissions déclarées ;
- des interdictions absolues ;
- des preuves de succès définies.

Un agent sans définition formelle ne peut pas opérer.

### G-03 — Gates bloquants
Toute instance ASEF implémente au minimum les 10 quality gates universels (G0-G9).
Un gate bloquant non satisfait arrête le pipeline. Sans exception.
La liste des gates passés et bloqués est auditable à tout moment.

### G-04 — Evidence obligatoire
Aucun livrable n'est accepté sans evidence package.
L'evidence package contient au minimum :
- la liste des actions exécutées ;
- les preuves d'exécution (logs, captures, rapports) ;
- les gates franchis avec statuts.

### G-05 — Décision tracée
Toute décision structurante produit un ADR dans docs/adr/.
Toute décision GO/NO-GO est formalisée dans DECISIONS.md.
Aucune décision critique n'est implicite.

### G-06 — Validation humaine souveraine
Les décisions suivantes sont TOUJOURS humaines :
- approbation finale de release ou de livraison ;
- exception à un gate bloquant ;
- modification du périmètre ;
- accès à un environnement de production ;
- décision juridique, réglementaire ou éthique.

### G-07 — Mémoire systémique
Toute instance ASEF met à jour sa mémoire à la fin de chaque cycle.
Les apprentissages, erreurs et décisions sont consolidés.
La mémoire est distinguée de l'historique (MEMORY.md ≠ SESSION_LOG.md).

### G-08 — Anti-hallucination
Tout agent ASEF distingue obligatoirement :
- **FAIT** : observable, vérifiable, daté ;
- **HYPOTHÈSE** : supposition non encore vérifiée ;
- **INFÉRENCE** : déduction logique d'un ensemble de faits ;
- **RECOMMANDATION** : suggestion de l'agent ;
- **DÉCISION** : choix validé par l'humain compétent.

Confondre ces catégories est une violation de la constitution.

### G-09 — Traçabilité complète
Chaque action exécutée dans une instance ASEF est tracée dans SESSION_LOG.md.
La traçabilité est continue, non rétroactive, non falsifiable.

### G-10 — Modularité héritée
Tout framework vertical hérite d'ASEF-Core.
Il ne réimplémente pas les primitives. Il les spécialise.
Toute divergence avec ASEF-Core nécessite un ADR.

### G-11 — Amélioration continue
Toute instance ASEF documente ses erreurs dans LESSONS_LEARNED.md.
Les patterns récurrents sont transformés en règles dans AGENTS.md ou SCOPE.md.
Un framework qui ne s'améliore pas est un framework qui régresse.

### G-12 — Auditabilité externe
Toute instance ASEF peut être auditée par un tiers sans accès au code source.
L'auditeur doit pouvoir répondre aux 14 questions fondamentales d'ASEF
(voir core/ASEF-Audit.md) à partir des seuls fichiers de gouvernance.

---

## Ce que le MANIFEST n'est pas

- Un idéal. C'est un contrat exécutable.
- Une suggestion. C'est une obligation pour toute instance ASEF.
- Un point de départ. C'est le minimum non-négociable.

---

## Violation du MANIFEST

Toute instance qui viole ces garanties doit :
1. Documenter la violation dans SESSION_LOG.md.
2. Ouvrir un ADR d'exception avec justification.
3. Obtenir une validation humaine explicite.
4. Planifier la mise en conformité dans ROADMAP.md.

Une instance en violation persistante non documentée est hors ASEF.
