# PRODUCT.md — ASEF

> Source de vérité produit.  
> 1 responsabilité : personas, cas d'usage, journeys et critères d'acceptation.  
> Dépend de : PROJECT.md, SCOPE.md  
> Ne doit jamais contenir : architecture technique (→ ARCHITECTURE.md), backlog (→ BACKLOG.md).

---

## Personas

### P1 — Tech Lead / Engineering Manager

**Contexte :** Responsable de la qualité et de la gouvernance sur une équipe qui utilise l'IA pour coder.

**Douleurs :**
- Impossible de savoir ce que les agents IA ont fait sans logs
- Pas de règles claires → chaque dev configure les agents différemment
- Les erreurs de l'IA sont découvertes tard, en review ou en production

**Attentes d'ASEF :**
- Un cadre commun, configurable, applicable par toute l'équipe
- Des gates automatiques qui ne se contournent pas
- Une piste d'audit lisible des actions agent

---

### P2 — Developer senior

**Contexte :** Développeur expérimenté qui utilise l'IA comme copilote, pas comme oracle.

**Douleurs :**
- Les suggestions IA sont parfois hors périmètre ou non cohérentes avec l'archi
- Pas de retour sur la qualité des prompts qu'il utilise
- Les revues de code IA ne suivent pas les standards maison

**Attentes d'ASEF :**
- Des instructions claires pour ses outils (Copilot, Claude)
- Des gates qui valident son code sans lui imposer de surcharge manuelle
- Un système de documentation automatisable

---

### P3 — Auditeur / RSSI

**Contexte :** Responsable de la conformité, de la traçabilité et de la sécurité des systèmes.

**Douleurs :**
- Impossible de répondre à "quel LLM a généré ce code ?" ou "qui a validé ?"
- Pas de traçabilité des décisions prises par l'IA vs l'humain
- Les modèles IA utilisés ne sont pas documentés (data privacy ?)

**Attentes d'ASEF :**
- Une piste d'audit complète et immuable
- Une documentation des modèles et de ce qu'ils reçoivent
- Des gates de sécurité automatiques visibles dans les rapports

---

## Jobs-to-be-done (JTBD)

| Persona | JTBD | Valeur mesurable |
|---------|------|----------------|
| Tech Lead | Établir des règles communes pour l'équipe | Réduction des inconsistances inter-devs (baseline : nombre de commentaires "hors standards" en PR, mesuré sur 4 sprints) |
| Developer | Coder plus vite avec l'IA sans sacrifier la qualité | Moins de cycles de review (baseline : nombre moyen de rounds de review par PR avant merge) |
| Auditeur | Prouver la traçabilité des décisions IA | Audit réussi sans effort manuel (baseline : temps de préparation d'un rapport d'audit, estimé > 4h sans ASEF) |

---

## Cas d'usage par MVP

### MVP (v0.1.0)

| ID | Cas d'usage | Persona | Accepté si |
|----|-------------|---------|-----------|
| UC-001 | Configurer Copilot avec les règles ASEF | Developer | instructions.md appliqué, lint passe |
| UC-002 | Exécuter un pipeline CI complet | Developer | G0-G5 verts, artifacts produits |
| UC-003 | Tracer une action agent en audit log | Tech Lead | Entrée JSON lisible en < 2h |
| UC-004 | Déclencher une exception de gate | Tech Lead | EXCEPTIONS.md mis à jour, justification tracée |
| UC-005 | Produire un rapport de release | Auditeur | Evidence package complet (EVIDENCE.md) |

### V1 (cible)

| ID | Cas d'usage | Persona | Accepté si |
|----|-------------|---------|-----------|
| UC-101 | Dashboard observabilité en temps réel | Tech Lead | SLOs visibles, alertes actives |
| UC-102 | Evals automatiques sur changement de prompt | Developer | Score visible en CI, merge bloqué si régression |
| UC-103 | Rapport de conformité exportable | Auditeur | PDF générable avec signatures numériques |

---

## Critères d'acceptation globaux MVP

- [ ] Zéro secret committé dans le repo depuis la création
- [ ] Toutes les actions agent sont loggées avec `agent_id` et `prompt_version`
- [ ] CI passe (G0-G5) sur chaque PR
- [ ] Chaque fichier de gouvernance ≤ 400 lignes
- [ ] Aucun fichier est un placeholder — tout le contenu est opérationnel
