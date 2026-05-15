# GOVERNANCE.md — ASEF

> Source de vérité de la gouvernance organisationnelle.  
> 1 responsabilité : définir qui décide quoi, comment, avec quel niveau d'autorité.  
> Dépend de : AGENTS.md, SCOPE.md  
> Ne doit jamais contenir : procédures techniques, règles de code.

---

## Instances de décision

| Instance | Membres | Scope de décision | Fréquence | Mode |
|---------|---------|------------------|-----------|------|
| CTO / Sponsor | CTO | Releases critiques, budget, décisions existentielles | Sur événement | Manuel |
| Tech Lead | Tech Lead | Architecture, scope, exceptions sécurité, Gate 7 | Continu | Manuel |
| Product Owner | PO | Scope produit, priorisation backlog, DoD | Par sprint | Manuel |
| Agent Architect | Agent IA | Décisions techniques dans le périmètre du sprint | Continu | Auto + validation |
| Agent Security | Agent IA | Remontée vulnérabilités, recommandations sécurité | Continu | Auto |
| Équipe | Tous | Rétrospective, leçons apprises, évolutions processus | Mensuel | Collectif |

---

## Niveaux d'autorité

### Niveau 1 — Agent seul (autonomie complète)

L'agent peut agir sans validation humaine préalable si :
- Le changement est IN scope (SCOPE.md)
- Aucun gate bloquant n'est rouge
- Aucune décision structurante n'est requise (pas d'ADR nécessaire)
- Le changement ne touche pas : secrets, accès, AGENTS.md, SCOPE.md

**Exemples :** Écrire du code, créer des tests, mettre à jour la doc, corriger un bug mineur.

### Niveau 2 — Validation Tech Lead

Obligatoire si :
- Décision architecturale (→ ADR requis)
- Modification AGENTS.md ou SCOPE.md
- Exception quality gate (→ EXCEPTIONS.md)
- Nouvelle dépendance externe significative
- Changement d'authentification ou d'autorisation

### Niveau 3 — Validation CTO / Sponsor

Obligatoire si :
- Release en production (Gate 7)
- Modification du modèle économique ou du périmètre stratégique
- Incident de sécurité de niveau CRITICAL
- Décision irréversible à impact élevé

---

## RACI — Activités principales

| Activité | CTO | Tech Lead | PO | Agent |
|---------|-----|-----------|-----|-------|
| Définir le scope | I | A/R | R | — |
| Écrire le code | I | A | I | R |
| Valider l'architecture | I | R/A | — | C |
| Prioriser le backlog | A | I | R | — |
| Valider Gate 7 | R/A | C | I | — |
| Gérer les exceptions | A | R | I | C |
| Définir les agents | I | A/R | — | C |
| Approuver un ADR | A | R | I | C |
| Répondre à un incident | R | A | I | C |
| Revue mensuelle gouvernance | I | R/A | I | C |

_R = Responsable (fait) · A = Accountable (répond) · C = Consulté · I = Informé_

---

## Délégations

| Situation | Délégation |
|----------|-----------|
| CTO indisponible | Tech Lead prend Gate 7 et décisions Niveau 3 urgentes |
| Tech Lead indisponible | Blocage livraison — escalader vers CTO |
| PO indisponible | Tech Lead prend les décisions de scope d'urgence |

---

## Pouvoirs des agents IA

Les agents IA dans ASEF ont les pouvoirs suivants, définis dans AGENTS.md :
- Lire tous les fichiers du repo
- Écrire du code, des tests, de la documentation
- Exécuter des commandes de build et test
- Proposer des décisions (ADR) sans les valider
- Remonter des risques et blocages

Les agents IA ne peuvent PAS :
- Merger vers main sans approbation humaine
- Modifier AGENTS.md, SCOPE.md, EXCEPTIONS.md sans validation
- Prendre des décisions Niveau 2 ou 3 de façon autonome
- Ignorer un gate bloquant

---

## Processus de revue de gouvernance

La gouvernance est révisée mensuellement (voir AUDIT.md).  
Toute évolution de ce fichier requiert un ADR dans `docs/adr/`.
