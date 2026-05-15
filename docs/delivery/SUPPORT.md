# SUPPORT.md — ASEF

> Source de vérité du modèle de support.  
> 1 responsabilité : définir les canaux, les SLAs de support et les procédures d'escalade.  
> Dépend de : INCIDENT_RESPONSE.md, SLO.md  
> Ne doit jamais contenir : procédures d'incident (→ INCIDENT_RESPONSE.md).

---

## Canaux de support

| Canal | Usage | Délai de réponse cible |
|-------|-------|----------------------|
| GitHub Issues | Bugs, questions techniques, demandes de feature | 2 jours ouvrés |
| GitHub Discussions | Questions générales, aide, retours | 3 jours ouvrés |
| Email équipe | Sécurité, données sensibles | 24h |
| Escalade directe | Incidents P1/P2 | Voir INCIDENT_RESPONSE.md |

---

## Niveaux de ticket

### P1 — Critique

**Critères :** Système inutilisable, perte de données, vulnérabilité CRITICAL exploitable

**SLA :**
- Accusé de réception : 30 minutes
- Premier diagnostic : 1 heure
- Résolution ou contournement : 4 heures
- Communication : Toutes les heures

**Processus :** Directement via INCIDENT_RESPONSE.md §P1

---

### P2 — Majeur

**Critères :** Fonctionnalité principale dégradée, pas de contournement simple

**SLA :**
- Accusé de réception : 2 heures
- Premier diagnostic : 4 heures
- Résolution : 24 heures

---

### P3 — Mineur

**Critères :** Fonctionnalité secondaire impactée, contournement disponible

**SLA :**
- Accusé de réception : 1 jour ouvré
- Résolution : Prochain sprint (1-2 semaines)

---

### P4 — Question / Demande

**Critères :** Question technique, demande de documentation, suggestion

**SLA :**
- Accusé de réception : 2 jours ouvrés
- Réponse ou planification : Backlog (BACKLOG.md)

---

## Format de ticket (GitHub Issue)

```markdown
## Description
[Description précise du problème ou de la demande]

## Environnement
- Version ASEF : vX.Y.Z
- OS : [Windows / macOS / Linux]
- Node.js : [version]
- Navigateur (si applicable) : [navigateur + version]

## Comportement attendu
[Ce qui devrait se passer]

## Comportement observé
[Ce qui se passe réellement]

## Étapes pour reproduire
1. [Étape 1]
2. [Étape 2]
3. ...

## Logs / captures
[Attacher les logs, screenshots, traces d'erreur]

## Priorité suggérée
[ ] P1 - Critique
[ ] P2 - Majeur
[x] P3 - Mineur
[ ] P4 - Question
```

---

## Escalade

| Situation | Escalade vers |
|---------|--------------|
| Bug non résolu en P2 depuis > 24h | Tech Lead |
| Question de sécurité | Security Lead (email privé) |
| Litige sur priorité | Product Owner |
| Comportement inattendu d'un agent IA | Tech Lead + SESSION_LOG.md |

---

## FAQ

**Q : Comment savoir quelle version est déployée ?**  
R : Endpoint `/version` ou en consultant le dernier tag Git sur main.

**Q : Mon build local échoue mais CI passe. Que faire ?**  
R : Vérifier `.env.local` vs `.env.example`, faire `npm ci` (pas `npm install`).

**Q : Un agent IA a fait quelque chose d'inattendu. Quoi signaler ?**  
R : Ouvrir un P2 avec les logs de la session agent (`SESSION_LOG.md`) et l'entrée dans l'audit log (OBSERVABILITY.md). Ne pas supprimer les traces.

**Q : Comment proposer une nouvelle feature ?**  
R : Ouvrir un P4 GitHub Discussion → si acceptée, elle atterrit dans BACKLOG.md → planifiée en sprint.
