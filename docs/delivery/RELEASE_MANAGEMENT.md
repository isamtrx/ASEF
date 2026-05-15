# RELEASE_MANAGEMENT.md — ASEF

> Source de vérité de la gestion des releases.  
> 1 responsabilité : définir le versionnement, les critères de release et le gel de code.  
> Dépend de : BRANCHING.md, QUALITY_GATES.md  
> Ne doit jamais contenir : procédures de déploiement (→ DEPLOYMENT.md).

---

## Versionnement

ASEF suit **Semantic Versioning 2.0.0** (semver).

```
vMAJOR.MINOR.PATCH[-prerelease][+build]

MAJOR : changement incompatible d'API ou de comportement
MINOR : nouvelle fonctionnalité rétrocompatible
PATCH : correction de bug rétrocompatible
```

### Exemples

- `v0.1.0` — MVP initial
- `v0.2.0` — Ajout d'un module (minor)
- `v0.2.1` — Bugfix post-release (patch)
- `v1.0.0` — Première version stable enterprise

### Versions de pré-release

```
v1.0.0-alpha.1   → Alpha interne
v1.0.0-beta.1    → Beta limitée
v1.0.0-rc.1      → Release Candidate
v1.0.0           → Release stable
```

---

## Critères de release

### Critères obligatoires (non-négociables)

- [ ] Gates G0 à G5 verts (automatiques)
- [ ] G6 documentation : CHANGELOG.md à jour + release notes rédigées
- [ ] Aucune vulnérabilité CRITICAL ou HIGH non acceptée explicitement dans EXCEPTIONS.md
- [ ] Tous les tests passent en CI (0 flaky tolérés en release)

### Critères souhaités (non-bloquants pour MVP)

- [ ] Coverage ≥ seuil défini dans QA.md
- [ ] Performance benchmarks dans les seuils SLO.md
- [ ] Revue UX si changement visible utilisateur

### Gate 7 — Validation humaine

Pour toute release `vMAJOR.MINOR.0` (pas les patches) :
- Validation explicite du Tech Lead ou Product Owner
- Forme : commentaire sur la GitHub release, signature dans SESSION_LOG.md, ou ticket dédié
- Sans Gate 7 → le déploiement production est bloqué

---

## Cadence de release

| Type | Cadence recommandée |
|------|-------------------|
| Patch (bugfix) | Sur besoin, pas de cadence fixe |
| Minor (feature) | Toutes les 2 semaines (fin de sprint) |
| Major (breaking) | Sur planification explicite (ROADMAP.md) |
| Hotfix | Sur incident P1/P2 uniquement |

---

## Gel de code (Feature Freeze)

Pour les releases MAJOR ou MINOR planifiées :

- **J-3** : Feature freeze — seuls les bugfixes critiques sont mergés
- **J-1** : Release Candidate — branch `release/vX.Y.0`, tests d'intégration finaux
- **J** : Release — tag + Gate 7 + déploiement production

Pendant le gel de code : les features en cours restent sur leur branche de feature, pas mergées.

---

## Format des release notes

Le fichier `RELEASE_NOTES.md` (racine, temporaire, écrasé à chaque release) contient :

```markdown
## ASEF v1.2.0 — [Date]

### Nouvelles fonctionnalités
- [F-xxx] Description de la feature

### Corrections
- [B-xxx] Description du bug corrigé

### Changements internes
- [D-xxx] Amélioration technique

### Breaking changes (si MAJOR)
- [BREAKING] Description du changement incompatible + guide de migration

### Evidence package
- CI : [lien vers le run CI]
- Tests : 128 passés / 0 échoués
- Coverage : 84%
- SAST : 0 finding CRITICAL/HIGH
```

---

## Traçabilité des releases

Chaque release doit être traçable :
- **Tag Git** : référence le commit exact
- **GitHub Release** : pointe vers RELEASE_NOTES.md
- **CHANGELOG.md** : section datée
- **SESSION_LOG.md** : entrée de session avec version déployée
- **Artifact CI** : conservé 90 jours (voir EVIDENCE.md)

---

## Releases d'urgence (Hotfix)

Processus accéléré pour les P1/P2 (voir INCIDENT_RESPONSE.md) :

1. Branche `hotfix/TICKET-xxx` depuis main
2. Correctif minimal uniquement
3. Tests ciblés (pas suite complète si temps critique)
4. PR → 1 reviewer minimum → merge
5. Tag de patch version
6. Gate 7 simplifié : validation orale + email
7. Postmortem dans les 48h
