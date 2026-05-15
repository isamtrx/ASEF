# RUNBOOK.md — ASEF

> Source de vérité des procédures opérationnelles courantes.  
> 1 responsabilité : permettre à tout contributeur de démarrer, déboguer et maintenir le projet.  
> Dépend de : ARCHITECTURE.md, DEPLOYMENT.md  
> Ne doit jamais contenir : procédures de release (→ RELEASE_MANAGEMENT.md).

---

## Prérequis locaux

| Outil | Version minimale | Installation |
|-------|----------------|-------------|
| Node.js | 20.x LTS | https://nodejs.org |
| npm | 10.x | Inclus avec Node.js |
| Git | 2.40+ | https://git-scm.com |
| VS Code | 1.89+ | https://code.visualstudio.com |
| GitHub CLI | 2.x | https://cli.github.com |

---

## Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/org/asef.git
cd asef

# 2. Installer les dépendances
npm ci

# 3. Copier et configurer les variables d'environnement
cp .env.example .env.local
# Éditer .env.local avec vos valeurs locales

# 4. Vérifier l'installation
npm run validate  # lint + typecheck + tests
```

---

## Commandes courantes

```bash
# Développement
npm run dev           # Démarrer le serveur de dev
npm run dev:watch     # Dev avec reload automatique

# Qualité
npm run lint          # Vérification lint
npm run lint:fix      # Correction automatique lint
npm run typecheck     # Vérification types TypeScript
npm test              # Tests unitaires
npm run test:watch    # Tests en mode watch
npm run test:e2e      # Tests E2E (nécessite le serveur)
npm run test:coverage # Tests avec rapport de coverage

# Build
npm run build         # Build de production
npm run build:dev     # Build de développement
npm run preview       # Prévisualiser le build

# Sécurité
npm audit             # Audit des dépendances
npm audit --audit-level=high  # Audit strict
```

---

## Débogage

### Activer les logs détaillés

```bash
LOG_LEVEL=debug npm run dev
```

### Inspecter les tests qui échouent

```bash
# Exécuter un test en particulier avec verbose
npm test -- --verbose --testNamePattern="nom du test"

# Exécuter avec le debugger Node.js
node --inspect-brk node_modules/.bin/jest --runInBand
```

### Analyser le build

```bash
npm run build:analyze  # Rapport de bundle (si script présent)
```

---

## Réinitialisation de l'environnement

```bash
# Nettoyer les artifacts de build
npm run clean

# Reinstaller les dépendances depuis zéro
rm -rf node_modules
npm ci

# Réinitialiser la base de données locale (si applicable)
npm run db:reset
```

---

## Erreurs fréquentes et solutions

| Erreur | Cause probable | Solution |
|--------|---------------|---------|
| `MODULE_NOT_FOUND` | Dépendances manquantes | `npm ci` |
| Port déjà utilisé | Autre processus sur le port | `lsof -i :3000` puis `kill -9 [PID]` |
| `Permission denied` | Droits insuffisants | Vérifier propriétaire du fichier |
| Lint échoue après rebase | Conflits résolus avec mauvais style | Relancer `npm run lint:fix` |
| Tests flaky en CI | Race condition ou état global | Investiguer, jamais skipper |
| `ENOTFOUND` API externe | Connexion ou config | Vérifier `.env.local` et network |
| Build trop lent | Cache invalidé | `npm run clean && npm run build` |

---

## Procédures de maintenance

### Mise à jour des dépendances

```bash
# Vérifier les dépendances obsolètes
npm outdated

# Mettre à jour les patches (sûr)
npm update

# Mettre à jour une dépendance spécifique
npm install nom-package@latest

# Vérifier la compatibilité après mise à jour
npm run validate
```

### Rotation des secrets

Voir SECRETS.md pour la procédure complète.

### Vérification d'intégrité du repo

```bash
# Vérifier que tous les hooks pre-commit sont actifs
git config --list | grep hook

# Vérifier la signature des commits récents
git log --show-signature -5
```

---

## Contacts d'urgence

| Rôle | Responsabilité | Escalade |
|------|---------------|---------|
| Tech Lead | Décisions techniques urgentes | INCIDENT_RESPONSE.md |
| DevOps | Infrastructure + déploiement | INCIDENT_RESPONSE.md |
| Security | Incidents sécurité | INCIDENT_RESPONSE.md §Escalade |
