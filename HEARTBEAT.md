# HEARTBEAT.md — ASEF

> Fichier d'état de santé du projet.  
> Mis à jour en fin de chaque session active.  
> Si la date de dernière mise à jour dépasse 7 jours, le contexte est potentiellement stale.

---

## État actuel

| Champ | Valeur |
|-------|--------|
| Dernière session | 2026-05-19 |
| Phase active | Sprint 1 — Opérationnalisation |
| Statut général | 🟢 P0→P4 complet |
| CI/CD | ❌ Non déployé |
| Tests | ✅ Passés (pytest) |
| Bootstrap | ✅ Mécanisme en place |

---

## Agents actifs

| Agent | Statut | Dernière utilisation |
|-------|--------|---------------------|
| orchestrator | ✅ Actif | 2026-05-18 |
| developer | ⏸ Standby | — |
| qa | ⏸ Standby | — |
| security | ⏸ Standby | — |
| architect | ⏸ Standby | — |
| docs | ⏸ Standby | — |

---

## Blocages actifs

| ID | Description | Depuis | Owner |
|----|-------------|--------|-------|
| — | Aucun blocage actif | — | — |

---

## Prochaine action prioritaire

Déployer `.github/workflows/ci.yml` sur projet cible (voir MEMORY.md).

---

## Règle de lecture

Avant de commencer une session :
1. Lire ce fichier — le contexte est-il récent ?
2. Si `Dernière session` > 7 jours → lire SESSION_LOG.md pour reconstituer le contexte
3. Si `Statut général` = 🔴 → lire POSTMORTEMS.md avant toute action

---

_Mis à jour par : orchestrator — 2026-05-18_
