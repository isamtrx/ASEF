# SDLC.md — ASEF

> Source de vérité du cycle de développement logiciel.  
> 1 responsabilité : décrire le cycle de vie complet d'un artefact, de l'intake au retrait.  
> Dépend de : OPERATING_MODEL.md, QUALITY_GATES.md  
> Ne doit jamais contenir : conventions de code (ENGINEERING_HANDBOOK.md), pipelines CI (CI_CD.md).

---

## Phases du SDLC ASEF

### Phase 1 — Intake et définition

**Entrée :** Idée, bug report, demande utilisateur, dette technique  
**Sortie :** DoD validé, item BACKLOG.md mis à jour

Activités :
- Formulation de la demande par le PO ou l'équipe
- Vérification scope (SCOPE.md)
- Rédaction DoD ≤ 8 lignes
- Estimation et priorisation dans BACKLOG.md
- Si décision structurante : ouverture d'un ADR

---

### Phase 2 — Planification sprint

**Entrée :** Backlog priorisé  
**Sortie :** CURRENT_SPRINT.md mis à jour, tâches engagées

Activités :
- Sélection des items pour le sprint selon capacité
- Validation de la définition de prêt (DoR) pour chaque item
- Mise à jour CURRENT_SPRINT.md

**Définition de prêt (DoR) :**
- Critères d'acceptation clairs
- Dépendances identifiées
- Effort estimé raisonnable pour le sprint
- IN scope confirmé

---

### Phase 3 — Développement

**Entrée :** Item prêt (DoR validé)  
**Sortie :** Code, tests, documentation

Activités :
- Création de branche (BRANCHING.md)
- Implémentation (STANDARDS.md, ENGINEERING_HANDBOOK.md)
- Tests unitaires et d'intégration
- Lint et type-check
- Mise à jour documentation si nécessaire

**Définition de terminé (DoD) :**
- Tous les critères du DoD item satisfaits
- Gates G2 à G5 verts
- PR ouverte et description complète

---

### Phase 4 — Revue et validation

**Entrée :** PR ouverte, CI vert  
**Sortie :** PR mergée ou refusée

Activités :
- Revue de code humaine (Gate 7 si release)
- Validation des preuves (EVIDENCE.md)
- Correction des commentaires de revue
- Approbation et merge

---

### Phase 5 — Release

**Entrée :** main avec les fonctionnalités prêtes  
**Sortie :** Version taguée déployée

Activités :
- Gel du code (feature freeze)
- Tests de release complets
- Gate 7 — validation humaine
- Tag Git avec numéro de version (semver)
- CHANGELOG.md section versionnée
- Déploiement (DEPLOYMENT.md)
- Vérification post-déploiement

---

### Phase 6 — Exploitation et maintenance

**Entrée :** Version en production  
**Sortie :** Version stable, métriques, incidents traités

Activités :
- Monitoring (OBSERVABILITY.md)
- Gestion des incidents (INCIDENT_RESPONSE.md)
- Hotfixes si nécessaire
- Collecte des retours utilisateurs

---

### Phase 7 — Retrait (EOL)

**Entrée :** Décision de retrait (ADR requis)  
**Sortie :** Version retirée, users migrés

Activités :
- Communication aux utilisateurs (SUPPORT.md)
- Plan de migration
- Archivage du repo
- Mise à jour PRODUCT.md et ROADMAP.md

---

## Jalons clés et critères de passage

| Jalon | Critère | Responsable |
|-------|---------|-------------|
| Sprint Start | DoR validé pour tous les items engagés | PO + TL |
| Merge vers main | G0-G5 verts, revue approuvée | CI + TL |
| Release candidate | G0-G6 verts, evidence package complet | CI |
| Production release | Gate 7 validé | CTO/TL |
| EOL | ADR validé, plan migration approuvé | CTO |

---

## Rythme recommandé MVP

| Cadence | Fréquence |
|---------|-----------|
| Sprint | 2 semaines |
| Release | 1/sprint minimum |
| Rétrospective | Fin de sprint |
| Audit gouvernance | Mensuel |
| Audit sécurité | Trimestriel |
