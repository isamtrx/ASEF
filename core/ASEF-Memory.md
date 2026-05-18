# ASEF-Memory — Modèle de mémoire systémique

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core

---

## 1. Principe

La mémoire ASEF est systémique. Elle ne repart jamais de zéro.
Chaque cycle d'exécution enrichit la mémoire du framework.

**Règle fondamentale** :
- `MEMORY.md` = état courant stabilisé (réécrit quand nouvelles preuves)
- `SESSION_LOG.md` = historique append-only (jamais édité, jamais effacé)
- `DECISIONS.md` = décisions structurantes tracées avec contexte

Ces trois fichiers ont des rôles distincts. Les confondre est une violation.

---

## 2. Fichiers de mémoire ASEF

### MEMORY.md
**Rôle** : État courant du projet / framework.
**Format** : Sections thématiques, mise à jour à la fin de chaque session.
**Règles** :
- Ne contient PAS d'historique.
- Ne contient PAS de to-do-list (→ BACKLOG.md).
- Ne contient PAS de changelog (→ CHANGELOG.md).
- Reflète la vérité actuelle, pas ce qui était vrai hier.

```markdown
## État courant
[Ce qui est vrai maintenant, pas ce qui était vrai avant]

## Décisions stabilisées
[Décisions actives qui conditionnent le travail]

## Risques actifs
[Risques identifiés non résolus]

## Prochaine session
[Contexte minimal pour reprendre sans relire tout]
```

---

### SESSION_LOG.md
**Rôle** : Journal chronologique de toutes les sessions.
**Format** : Entries append-only, plus récente en premier.
**Règles** :
- Jamais édité rétroactivement.
- Jamais effacé.
- Chaque entrée contient : date, objectif, actions clés, fichiers modifiés, statut.

```markdown
## [YYYY-MM-DD] — [Résumé en 1 ligne]

**Objectif** : [Tâche initiale]
**Statut** : TERMINÉ | PARTIEL | BLOQUÉ
**Actions clés** :
- [Action 1]
- [Action 2]
**Fichiers modifiés** : [liste]
**Gates franchis** : [G0, G1, G2...]
**Escalades humaines** : [si applicable]
**Apprentissages** : [si applicables]
```

---

### DECISIONS.md
**Rôle** : Registre des décisions structurantes.
**Format** : ADR minimal par décision.
**Règles** :
- Toute décision GO/NO-GO/CONDITIONAL sur un sujet critique.
- Toute décision architecturale.
- Toute exception à un gate.
- Jamais une décision sans contexte, options, justification.

```markdown
## [YYYY-MM-DD] — [Titre décision]

**Type** : GO | NO-GO | CONDITIONAL GO | ADR | EXCEPTION
**Contexte** : [Pourquoi cette décision est nécessaire]
**Options évaluées** :
1. [Option A] — Avantages / Inconvénients
2. [Option B] — Avantages / Inconvénients
**Décision** : [Ce qui a été choisi]
**Raison** : [Pourquoi cette option]
**Conséquences** : [Impacts positifs et négatifs]
**Validation humaine** : [Qui a validé, quand — ou "N/A si agent autonome"]
**Réversibilité** : Réversible | Irréversible
```

---

### LESSONS_LEARNED.md
**Rôle** : Capitalisation des erreurs et incidents.
**Format** : Entrées append-only, classées par date.
**Règles** :
- Ne pas documenter les succès banals.
- Documenter les incidents, erreurs, patterns surprenants.
- Chaque leçon produit une règle applicable.

```markdown
## [YYYY-MM-DD] — [Titre incident / erreur]

**Erreur** : [Ce qui s'est passé]
**Cause** : [Pourquoi]
**Impact** : [Ce que ça a coûté]
**Règle nouvelle** : [Ce qu'on fait différemment maintenant]
**Fichier mis à jour** : [Où la règle a été ajoutée]
```

---

## 3. Règles MemoryAgent

1. **Lire avant d'agir.** Bootstrap toujours : AGENTS.md → MEMORY.md → SCOPE.md → DECISIONS.md.
2. **Écrire après chaque cycle.** Fin de session = mise à jour obligatoire.
3. **État actuel ≠ historique.** MEMORY.md ne contient jamais le passé.
4. **Preuves avant écriture.** Un fait dans MEMORY.md doit être vérifiable.
5. **Compounding systématique.** Chaque session enrichit la mémoire. Pas de reset.

---

## 4. Mémoire distribuée (multi-agent)

Dans un système multi-agent, chaque agent a accès en lecture à la mémoire partagée.
Seul MemoryAgent (ou CoreOrchestratorAgent) peut écrire MEMORY.md.
Chaque agent trace ses actions dans SESSION_LOG.md (append-only, pas de conflit).

```
Agent A ──→ SESSION_LOG.md (append)
Agent B ──→ SESSION_LOG.md (append)
Agent C ──→ SESSION_LOG.md (append)
MemoryAgent ──→ MEMORY.md (write, fin de session)
            ──→ LESSONS_LEARNED.md (write, si incident)
```

---

## 5. Checklist mémoire de fin de cycle

```
□ SESSION_LOG.md mise à jour (entrée datée)
□ MEMORY.md reflète l'état stabilisé actuel
□ DECISIONS.md mis à jour si décision structurante
□ LESSONS_LEARNED.md mis à jour si incident
□ CHANGELOG.md mis à jour si livrable
□ Aucune information sensible dans la mémoire
```
