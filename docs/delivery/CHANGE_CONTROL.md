# CHANGE_CONTROL.md — ASEF

> Source de vérité du contrôle des changements.  
> 1 responsabilité : classifier les changements, définir leur niveau de risque et leur traceabilité.  
> Dépend de : GOVERNANCE.md, QUALITY_GATES.md  
> Ne doit jamais contenir : procédures de déploiement (→ DEPLOYMENT.md), gestion des releases (→ RELEASE_MANAGEMENT.md).

---

## Classification des changements

### Standard (faible risque)

Changements routiniers, prévisibles, sans impact architectural.

**Exemples :** bugfix, mise à jour dépendances mineure, ajout de tests, amélioration docs

**Processus :**
1. Branch depuis main
2. PR + 1 reviewer
3. CI vert
4. Merge

**Délai :** Même jour

---

### Normal (risque modéré)

Changements planifiés avec impact sur le comportement ou l'architecture.

**Exemples :** nouvelle feature, changement d'API, refactoring avec impact cross-module

**Processus :**
1. DoD défini avant implémentation
2. Branch depuis main
3. PR + 1 reviewer minimum + revue Tech Lead si architectural
4. CI vert (G0-G5)
5. Documentation mise à jour (G6)
6. Merge

**Délai :** 1 à 5 jours selon complexité

---

### Urgent (risque élevé, délai contraint)

Changement non planifié nécessaire pour résoudre un incident ou une vulnérabilité critique.

**Exemples :** hotfix P1/P2, patch vulnérabilité CRITICAL

**Processus accéléré :**
1. Notification Tech Lead immédiate
2. Branch `hotfix/` depuis main
3. Correctif minimal (pas d'autres changements)
4. Review rapide (1 reviewer, focusé)
5. CI ciblé (tests liés au correctif obligatoires)
6. Gate 7 simplifié : validation orale + traçabilité a posteriori
7. Postmortem dans les 48h

**Délai :** < 4h en P1, < 24h en P2

---

## Analyse d'impact

Avant tout changement Normal ou Urgent, documenter :

| Aspect | Question | Réponse |
|--------|---------|---------|
| Fonctionnel | Quels comportements changent ? | |
| API | Quelle surface d'API est modifiée ? | |
| Données | Quel schéma de données est impacté ? | |
| Sécurité | Y a-t-il un impact sur la surface d'attaque ? | |
| Tests | Quels tests existants peuvent être impactés ? | |
| Agents | Quels agents IA voient leur comportement changer ? | |

**Format recommandé :** inclure dans la description de PR.

---

## Traçabilité obligatoire

Chaque changement doit être traçable dans :

| Artefact | Standard | Normal | Urgent |
|---------|---------|--------|--------|
| Ticket / issue GitHub | Recommandé | Obligatoire | Obligatoire |
| PR avec description | Obligatoire | Obligatoire | Obligatoire |
| CHANGELOG.md | Si livrable | Obligatoire | Obligatoire |
| SESSION_LOG.md | Non | Si décision structurante | Obligatoire |
| POSTMORTEMS.md | Non | Non | Obligatoire |

---

## Registre des changements urgents

| Date | ID | Description | Initiateur | Résolu en | Postmortem |
|-----|-----|-------------|-----------|-----------|-----------|
| — | — | _(aucun à date)_ | — | — | — |

---

## Changements hors périmètre (refus automatique)

Les changements suivants sont refusés sans validation humaine explicite :

- Modification de AGENTS.md, SCOPE.md ou DECISIONS.md par un agent IA
- Désactivation d'un gate de qualité (sans EXCEPTIONS.md)
- Ajout d'une dépendance avec licence non autorisée (OPEN_SOURCE_POLICY.md)
- Tout accès aux secrets CI/CD depuis le code source
