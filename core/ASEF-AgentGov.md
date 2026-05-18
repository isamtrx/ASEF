# ASEF-AgentGov — Gouvernance des agents

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core

---

## 1. Principe

Un agent sans définition formelle ne peut pas opérer dans ASEF.
Tout agent déclaré doit avoir : identifiant unique, rôle, permissions, interdictions, preuves de succès.

---

## 2. Cycle de vie d'un agent ASEF

```
DÉCLARÉ ──→ ACTIVÉ ──→ EN ACTIVITÉ ──→ SUSPENDU ──→ RETRAITÉ
               ↑                              |
               └──────────────────────────────┘
                    (réactivation possible)
```

| Statut | Description | Condition de transition |
|---|---|---|
| `DÉCLARÉ` | Agent défini dans le registre, non actif | Définition complète validée |
| `ACTIVÉ` | Agent actif dans une instance | Assigné à une tâche |
| `EN ACTIVITÉ` | Agent en train d'exécuter | En cours d'exécution |
| `SUSPENDU` | Agent temporairement inactif | Violation détectée, ou pause volontaire |
| `RETRAITÉ` | Agent hors service définitivement | Remplacé ou obsolète |

---

## 3. Contrat d'agent — Format obligatoire

```markdown
# Agent : [identifiant]

**Rôle** : [Description 1 ligne]
**Statut** : DÉCLARÉ | ACTIVÉ | EN ACTIVITÉ | SUSPENDU | RETRAITÉ
**Version** : [X.Y.Z]

## Mission
[Ce que cet agent fait, son périmètre exact]

## Permissions
- Lire : [liste des fichiers / répertoires]
- Écrire : [liste des fichiers / répertoires]
- Exécuter : [liste des actions autorisées]

## Interdictions absolues
- [Ce que cet agent ne peut JAMAIS faire]

## Entrées
[Ce que l'agent reçoit pour fonctionner]

## Sorties
[Ce que l'agent produit]

## Critères de succès
[Comment savoir que l'agent a bien fait son travail]

## Escalade
[Quand et comment cet agent escalade à un humain]

## Anti-patterns connus
[Comportements incorrects déjà observés, avec corrections]
```

---

## 4. Matrice des permissions par rôle ASEF

| Action | architect | developer | qa | security | docs | orchestrator |
|---|---|---|---|---|---|---|
| Lire tous les fichiers | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Modifier le code source | — | ✓ | — | — | — | — |
| Créer des tests | — | ✓ | ✓ | — | — | — |
| Modifier DECISIONS.md | ✓ | — | — | — | — | ✓ |
| Modifier ARCHITECTURE.md | ✓ | — | — | — | — | — |
| Modifier CHANGELOG.md | — | ✓ | — | — | ✓ | ✓ |
| Modifier MEMORY.md | — | — | — | — | — | ✓ |
| Modifier SESSION_LOG.md | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Valider un quality gate | — | — | ✓ | ✓ | — | — |
| Approuver une release | — | — | — | — | — | — |
| Émettre une exception | — | — | — | — | — | — |

**Règle** : Les deux dernières lignes sont toujours réservées aux humains.

---

## 5. Registre d'agents

Chaque framework maintient son registre d'agents dans `registry/agents.registry.json`.

```json
{
  "agents": [
    {
      "id": "core-orchestrator",
      "role": "Coordination et orchestration",
      "status": "ACTIVÉ",
      "version": "1.0.0",
      "definition_file": "core/ASEF-Core.md",
      "permissions": ["READ_ALL", "WRITE_SESSION_LOG", "WRITE_DECISIONS"],
      "interdictions": ["WRITE_AGENTS_MD", "WRITE_SCOPE_MD", "DEPLOY"]
    }
  ]
}
```

---

## 6. Violations et sanctions

| Violation | Détectée par | Conséquence |
|---|---|---|
| Agent sans définition formelle | AuditAgent | Suspension immédiate |
| Agent hors permissions | AuditAgent | Suspension + escalade HITL-12 |
| Agent qui invente une preuve | AuditAgent | Suspension + LESSONS_LEARNED |
| Agent qui contourne un gate | AuditAgent | Suspension + ADR exception |
| Agent qui décide à la place d'un humain | HumanApprovalAgent | Rollback + HITL-01 |

---

## 7. Checklist de déclaration d'un nouvel agent

```
□ Identifiant unique défini
□ Rôle décrit en 1 ligne
□ Mission complète rédigée
□ Permissions listées (lire / écrire / exécuter)
□ Interdictions absolues listées
□ Entrées et sorties définies
□ Critères de succès définis
□ Conditions d'escalade définies
□ Fichier de définition créé (agents/*.agent.md ou core/ASEF-Core.md)
□ Registre mis à jour (registry/agents.registry.json)
```
