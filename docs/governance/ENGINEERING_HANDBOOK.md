# ENGINEERING_HANDBOOK.md — ASEF

> Conventions quotidiennes de l'équipe d'ingénierie.  
> 1 responsabilité : fournir les règles pratiques de travail journalier.  
> Dépend de : STANDARDS.md (principes), BRANCHING.md (Git flow)  
> Ne doit jamais contenir : standards fondamentaux (→ STANDARDS.md), politiques sécurité (→ docs/security/).

---

## Conventions de nommage

### Fichiers et répertoires
```
kebab-case        → fichiers et dossiers
PascalCase        → composants React/Vue, classes
camelCase         → fonctions, variables, méthodes
UPPER_SNAKE_CASE  → constantes, variables d'environnement
```

### Git
```
feat/TICKET-XXX-titre-court      → nouvelle feature
fix/TICKET-XXX-titre-court       → correction de bug
chore/titre-court                → tâche technique sans feature
docs/titre-court                 → documentation seule
hotfix/TICKET-XXX-titre-court    → correction urgente en prod
```

### Commits
Format : `type(scope): description courte en français`

Types valides :
- `feat` — nouvelle fonctionnalité
- `fix` — correction de bug
- `docs` — documentation uniquement
- `test` — ajout ou modification de tests
- `refactor` — refactoring sans changement fonctionnel
- `chore` — tâche de maintenance (deps, config)
- `ci` — changement pipeline CI/CD
- `security` — changement lié à la sécurité

Exemples :
```
feat(api): ajouter endpoint POST /users
fix(auth): corriger expiration du token JWT
docs(agents): mettre à jour AGENTS.md permissions
security(deps): mettre à jour express@4.19.2
```

---

## Définition de prêt (DoR) — item

Un item est prêt à être engagé si :
- [ ] Critères d'acceptation rédigés et compréhensibles
- [ ] Dépendances identifiées et disponibles
- [ ] Effort estimé (≤ 3 jours idéalement)
- [ ] IN scope confirmé (SCOPE.md)
- [ ] DoD ≤ 8 lignes rédigé

---

## Définition de terminé (DoD) — item

Un item est terminé quand :
- [ ] Code écrit et lint propre (G3 vert)
- [ ] Tests unitaires verts, coverage ≥ 80% (G4 vert)
- [ ] Tests E2E verts si applicable (G4 vert)
- [ ] SAST et audit propres (G5 vert)
- [ ] PR ouverte avec description complète
- [ ] CHANGELOG.md mis à jour
- [ ] Revue humaine approuvée

---

## Structure d'une Pull Request

**Titre :** `type(scope): description courte`

**Corps obligatoire :**
```markdown
## Changements
[Ce qui a été modifié et pourquoi]

## DoD
- [ ] critère 1
- [ ] critère 2

## Preuves
- Lien rapport tests
- Lien rapport SAST
- Screenshot si UI

## Risques identifiés
[Aucun / Description si applicable]
```

**Labels obligatoires :** `feat` | `fix` | `docs` | `security` | `chore`  
**Reviewers :** Tech Lead toujours, domaine-expert si applicable

---

## Revue de code — règles

### Pour le revieweur
- Lire la PR description avant le code
- Commentaires constructifs et actionnables
- Un commentaire bloquant = justification obligatoire
- Approuver seulement si Gates G3-G5 sont verts en CI
- Ne jamais approuver avec des secrets dans le code

### Pour l'auteur
- Répondre à chaque commentaire avant de demander une re-revue
- Ne pas merger sans approbation
- Si désaccord avec un commentaire : escalader (pas d'impasse silencieuse)

---

## Patterns encouragés

- **Early return** — réduire l'imbrication logique
- **Immutabilité par défaut** — const, readonly, frozen
- **Composition plutôt qu'héritage** — pour les comportements partagés
- **Injection de dépendances** — pour la testabilité
- **Fail fast** — valider les inputs le plus tôt possible

---

## Patterns interdits

- `console.log` en production (utiliser le logger structuré)
- `TODO` sans numéro de ticket dans le code livré
- Fetch direct depuis le frontend vers une API externe (passer par le BFF)
- `eval()` ou équivalent (injection risk)
- Credentials hardcodés (voir SECRETS.md)
- `git push --force` sur une branche partagée

---

## Environnement local

**Setup :**
```bash
git clone https://github.com/[org]/asef
cp .env.example .env
npm install          # ou pip install -r requirements.txt
npm run dev          # ou équivalent
```

**Vérification avant commit :**
```bash
npm run lint
npm run test
npm run build
```

**Commandes fréquentes :** voir `docs/delivery/RUNBOOK.md`
