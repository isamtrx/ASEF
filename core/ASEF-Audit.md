# ASEF-Audit — Journalisation, conformité, auditabilité

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core, ASEF-Evidence

---

## 1. Principe

**Toute instance ASEF doit être auditable par un tiers sans accès au code source.**

L'auditeur utilise les seuls fichiers de gouvernance pour répondre
aux 14 questions fondamentales d'ASEF.

---

## 2. Les 14 questions fondamentales d'un audit ASEF

| # | Question | Fichier source |
|---|---|---|
| Q-01 | Quel est le périmètre exact de ce framework ? | SCOPE.md |
| Q-02 | Quels agents opèrent dans ce framework ? | registry/agents.registry.json |
| Q-03 | Quels quality gates sont définis et lesquels sont bloquants ? | docs/quality/QUALITY_GATES.md |
| Q-04 | Les gates ont-ils été franchis pour le dernier cycle ? | docs/evidence/ |
| Q-05 | Quelles preuves existent pour le dernier livrable ? | docs/evidence/[dernier]/INDEX.md |
| Q-06 | Quelles décisions structurantes ont été prises ? | DECISIONS.md |
| Q-07 | Quelles validations humaines ont été obtenues ? | DECISIONS.md (section HITL) |
| Q-08 | Quels risques ont été identifiés et comment sont-ils gérés ? | RISKS.md |
| Q-09 | Quelle est l'état actuel du framework ? | MEMORY.md |
| Q-10 | Quels incidents se sont produits et quelles leçons ont été tirées ? | LESSONS_LEARNED.md |
| Q-11 | Les agents respectent-ils leurs permissions ? | SESSION_LOG.md + AGENTS.md |
| Q-12 | La documentation est-elle à jour ? | CHANGELOG.md + SESSION_LOG.md |
| Q-13 | Les changements architecturaux sont-ils tracés ? | docs/adr/ |
| Q-14 | Le framework s'améliore-t-il dans le temps ? | LESSONS_LEARNED.md + CHANGELOG.md |

---

## 3. Types d'audit ASEF

### AUDIT-CONTINU
**Fréquence** : À chaque cycle d'exécution.
**Responsable** : AuditAgent (automatique).
**Périmètre** : Gates G0-G9 du cycle courant, traçabilité SESSION_LOG.md.
**Sortie** : Résultats de gates dans evidence package.

### AUDIT-LIVRAISON
**Fréquence** : À chaque livrable.
**Responsable** : AuditAgent + validation humaine.
**Périmètre** : Q-01 à Q-08.
**Sortie** : Rapport de livraison dans docs/evidence/[slug]/reports/audit.md.

### AUDIT-FRAMEWORK
**Fréquence** : Trimestriel ou sur demande.
**Responsable** : AuditAgent + humain externe à l'équipe.
**Périmètre** : Q-01 à Q-14.
**Sortie** : Rapport complet avec recommandations.

### AUDIT-INSTANCE
**Fréquence** : À la création d'une nouvelle instance.
**Responsable** : AuditAgent.
**Périmètre** : Vérification de l'héritage ASEF-Core, conformité MANIFEST.md.
**Sortie** : Rapport de conformité initiale.

### AUDIT-EXTERNE
**Fréquence** : Annuel ou sur demande réglementaire.
**Responsable** : Tiers externe + AuditAgent.
**Périmètre** : Q-01 à Q-14 + sécurité + conformité légale.
**Sortie** : Rapport d'audit externe certifié.

---

## 4. Format du rapport d'audit de livraison

```markdown
# Rapport d'audit — [Nom du livrable]
Date : YYYY-MM-DD
Auditeur : AuditAgent v[X.Y.Z]
Validation humaine : [Oui / Non]

## Conformité MANIFEST.md

| Garantie | Statut | Evidence |
|---|---|---|
| G-01 Périmètre explicite | ✓ CONFORME | SCOPE.md présent |
| G-02 Agents identifiés | ✓ CONFORME | registry/ complet |
| G-03 Gates bloquants | ✓ CONFORME | Gates G0-G9 tous verts |
| G-04 Evidence obligatoire | ✓ CONFORME | INDEX.md complet |
| ... | ... | ... |

## Résultats des gates

| Gate | Statut | Preuves |
|---|---|---|
| G0 | PASS | gates/G0-intake.md |
| G1 | PASS | gates/G1-scope.md |
| ... | ... | ... |

## Écarts détectés

| Écart | Sévérité | Recommandation |
|---|---|---|
| [Description] | LOW / MEDIUM / HIGH / CRITICAL | [Action recommandée] |

## Conclusion

**Statut global** : CONFORME | PARTIELLEMENT CONFORME | NON CONFORME
**Bloquant pour livraison** : Oui | Non
**Recommandations** : [Liste]
```

---

## 5. Règles AuditAgent

1. **Lecture seule obligatoire.** AuditAgent ne modifie jamais les fichiers qu'il audite.
2. **Questions fondamentales en premier.** Toujours évaluer Q-01 à Q-07 minimum.
3. **Aucun écart silencieux.** Tout écart est documenté, même les mineur.
4. **Séparation stricte.** L'agent qui exécute ne peut pas s'auditer lui-même.
5. **Preuves avant conclusion.** Une conclusion sans preuve = violation MANIFEST G-08.

---

## 6. Checklist d'audit avant livraison

```
□ Q-01 : SCOPE.md présent et à jour
□ Q-02 : Registre agents complet
□ Q-03 : Gates définis et bloquants
□ Q-04 : Tous les gates du cycle franchis
□ Q-05 : Evidence package complet avec INDEX.md
□ Q-06 : Décisions structurantes tracées dans DECISIONS.md
□ Q-07 : Validations HITL documentées
□ Q-08 : Registre risques à jour
□ SESSION_LOG.md continu depuis le début du cycle
□ Aucun secret dans les fichiers de gouvernance
□ AuditAgent ≠ agent ayant produit le livrable
```
