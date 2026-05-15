# DEPLOYMENT.md — ASEF

> Source de vérité des procédures de déploiement.  
> 1 responsabilité : définir les environnements, les étapes de build et les procédures de rollback.  
> Dépend de : CI_CD.md, RELEASE_MANAGEMENT.md  
> Ne doit jamais contenir : configuration des secrets (→ SECRETS.md), pipelines CI (→ CI_CD.md).

---

## Environnements

| Environnement | Usage | Déclenchement | Accès |
|-------------|-------|-------------|------|
| local | Développement quotidien | Manuel | Developer |
| staging | Validation pré-prod | Merge sur main (CI auto) | Developer, QA |
| production | Système de production | Tag + Gate 7 validé | Tech Lead + DevOps |

---

## Prérequis avant déploiement

### Pour staging

- [ ] Tous les jobs CI verts sur le commit cible
- [ ] G3 (code) + G4 (tests) + G5 (sécurité) validés
- [ ] Pas de vulnérabilité CRITICAL ou HIGH non résolue

### Pour production

- [ ] Version taguée sur main (`vX.Y.Z`)
- [ ] Release notes écrites (RELEASE_NOTES.md)
- [ ] G0 à G6 validés
- [ ] Gate 7 : validation Tech Lead explicite (commentaire GitHub ou ticket)
- [ ] Communication préalable si impact utilisateurs

---

## Build

```bash
# Build de production
npm ci                          # Dépendances clean
npm run build                   # Build optimisé

# Vérification de l'artifact
ls -lh dist/                    # Vérifier la présence des fichiers
npm run build:check             # Vérification intégrité (si script présent)
```

Variables d'environnement à définir pour le build de production :

```bash
NODE_ENV=production
APP_VERSION=$(git describe --tags --exact-match)
BUILD_SHA=$(git rev-parse HEAD)
```

---

## Déploiement

### Déploiement staging (automatique via CI)

Le CI déclenche le déploiement staging après un merge sur main.  
Le pipeline staging (release.yml) exécute :
1. Validation complète (lint + tests + audit)
2. Build de l'artifact
3. Déploiement sur l'environnement staging
4. Smoke tests automatiques

### Déploiement production (semi-automatique)

```bash
# 1. Vérifier que le tag est correct
git describe --tags --exact-match HEAD

# 2. Créer la release GitHub (déclenche release.yml)
# Via GitHub UI ou gh CLI :
gh release create v1.2.0 --notes-file RELEASE_NOTES.md

# 3. Valider Gate 7 (humain)
# Le Tech Lead approuve la release sur GitHub

# 4. Le pipeline finalise le déploiement production
```

---

## Rollback

### Rollback rapide (< 15 min après déploiement)

```bash
# Identifier la version précédente
git log --oneline --tags | head -5

# Redéployer la version précédente
gh release create vX.Y.Z-rollback --target [SHA version précédente]
```

### Rollback complet

1. Identifier la cause du problème (logs, alertes)
2. Décision de rollback par Tech Lead
3. Déployer la version N-1 via le pipeline release
4. Vérifier la santé du système après rollback
5. Ouvrir un postmortem (POSTMORTEMS.md)
6. Ne pas re-déployer sans corriger la cause racine

---

## Checklist post-déploiement

Après chaque déploiement production :

- [ ] Smoke tests passés (endpoints santé, fonctionnalités critiques)
- [ ] Alertes de monitoring normales (aucune alarme)
- [ ] Logs sans erreurs critiques (5 premières minutes)
- [ ] Métriques SLO stables (SLO.md)
- [ ] Communication envoyée si changement visible pour les utilisateurs
- [ ] SESSION_LOG.md mis à jour avec le numéro de version déployée

---

## Variables d'environnement par environnement

| Variable | local | staging | production |
|---------|-------|---------|-----------|
| NODE_ENV | development | staging | production |
| LOG_LEVEL | debug | info | warn |
| DATABASE_URL | localhost:5432 | Via secret CI | Via secret CI |
| API_BASE_URL | http://localhost:3000 | https://staging.api.asef.dev | https://api.asef.dev |

Les secrets ne sont jamais hardcodés — voir SECRETS.md pour la gestion des credentials.
