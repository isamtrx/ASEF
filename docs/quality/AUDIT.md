# AUDIT.md — ASEF

> Source de vérité du processus d'audit.  
> 1 responsabilité : définir comment vérifier que les contrôles fonctionnent réellement.  
> Dépend de : CONTROL_MATRIX.md, EVIDENCE.md  
> Ne doit jamais contenir : résultats d'audit (SESSION_LOG.md), règles de test (QA.md).

---

## Périmètre de l'audit

L'audit ASEF couvre :
- Les fichiers de gouvernance (AGENTS.md, SCOPE.md, DECISIONS.md, EXCEPTIONS.md)
- Les contrôles CI/CD actifs (CONTROL_MATRIX.md)
- Les preuves de livraison (EVIDENCE.md, artifacts CI)
- Les permissions agents et accès humains
- La conformité des outputs IA (docs/ai/EVALS.md)

L'audit ne couvre pas :
- La qualité fonctionnelle du produit livré (→ QA.md)
- La performance business

---

## Fréquence

| Type d'audit | Fréquence | Déclencheur |
|-------------|-----------|------------|
| Audit léger (contrôles CI) | Continue | Chaque pipeline CI |
| Audit release | À chaque release | Gate 7 |
| Audit mensuel (gouvernance) | Mensuel | Premier lundi du mois |
| Audit sécurité complet | Trimestriel | Calendrier fixe |
| Audit post-incident | Sur événement | Après tout incident P1/P2 |

---

## Méthode — Audit release (Gate 7)

**Checklist minimale avant approbation humaine :**

```
□ G0 à G6 tous verts dans le pipeline CI de la PR de release
□ CHANGELOG.md section versionnée est complète
□ Aucune exception EXCEPTIONS.md expirée en cours
□ Rapport SAST propre (0 HIGH/CRITICAL)
□ Rapport dependency audit propre
□ Secret scan propre
□ Evidence package complet et accessible (artifact CI)
□ DECISIONS.md à jour si décision structurante pendant le sprint
□ AGENTS.md n'a pas été modifié sans ADR associé
```

---

## Méthode — Audit mensuel gouvernance

**Checklist mensuelle :**

```
□ AGENTS.md — vérifier qu'aucune permission n'a été élargie sans ADR
□ EXCEPTIONS.md — réviser les exceptions actives, clôturer les expirées
□ CONTROL_MATRIX.md — vérifier le statut de chaque contrôle
□ SESSION_LOG.md — vérifier que les sessions récentes sont tracées
□ DECISIONS.md — vérifier que toutes les décisions récentes sont tracées
□ Accès GitHub — vérifier que les accès correspondent aux rôles actifs
□ Secrets — vérifier la date de rotation des secrets actifs
```

---

## Méthode — Audit sécurité trimestriel

**Périmètre :**

```
□ Revue complète ACCESS_CONTROL.md vs accès réels
□ Revue THREAT_MODEL.md — nouvelles surfaces d'attaque
□ Audit des secrets : rotation, stockage, accès
□ Test de pénétration léger sur endpoints exposés (si applicable)
□ Revue AGENT_REGISTRY.md — permissions effectives vs définies
□ Test prompt injection sur les agents en production
□ Revue OPEN_SOURCE_POLICY.md — nouvelles dépendances conformes
```

---

## Méthode d'échantillonnage

Pour les audits manuels sur les artifacts CI :
- Sélectionner les 5 dernières releases
- Vérifier que chaque release a un evidence package complet
- Vérifier que le pipeline CI était vert au moment du merge
- Vérifier qu'aucun test n'était skip sans ticket associé

---

## Rapport d'audit

Chaque audit donne lieu à une entrée dans `SESSION_LOG.md` avec :
- Date et type d'audit
- Contrôles vérifiés
- Anomalies détectées
- Actions correctives avec responsable et délai

---

## Remédiation

| Sévérité | Délai | Action |
|----------|-------|--------|
| Critique (violation sécurité) | 24h | Ouverture incident + blocage livraisons |
| Haute (gate non respecté) | 72h | Ticket prioritaire + exception EXCEPTIONS.md si délai > 72h |
| Moyenne (écart processus) | 2 semaines | Ticket normal |
| Faible (observation) | 1 mois | Backlog |

---

## Métriques d'audit cible

| Métrique | Cible MVP |
|---------|----------|
| Pipelines CI avec G4 vert | ≥ 95% |
| Exceptions expirées en cours | 0 |
| Décisions sans ADR | 0 |
| Secrets sans rotation > 6 mois | 0 |
| Sessions sans SESSION_LOG entrée | < 10% |
