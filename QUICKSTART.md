# QUICKSTART.md — ASEF

> Guide de démarrage rapide pour un humain qui veut adopter ASEF sur un projet.  
> Objectif : être opérationnel en moins de 30 minutes.  
> Audience : Tech Lead ou Developer senior qui découvre ASEF.

---

## Ce que vous obtenez en adoptant ASEF

- Un cadre documentaire complet pour gouverner vos agents IA
- Des quality gates clairs (G0–G7) qui bloquent avant la production
- Des règles uniformes pour toute l'équipe (Copilot, Claude, autres)
- Une piste d'audit traçable pour chaque décision IA

---

## Prérequis

- Git installé
- Un dépôt GitHub (ou GitLab) existant
- Accès admin au dépôt pour configurer les secrets CI

---

## Étape 1 — Cloner le framework (5 min)

```bash
# Remplacer [org] par votre organisation GitHub (ou GitLab)
git clone https://github.com/[org]/asef
cd asef
```

> **Note :** Le dépôt ASEF n'est pas encore publié en tant que template public. Copiez ce répertoire dans votre propre dépôt Git, ou utilisez `git init` dans un dossier local pour démarrer.

Parcourez la structure en 2 minutes :

```
AGENTS.md         ← commencez ici — la constitution
SCOPE.md          ← périmètre du projet
MEMORY.md         ← état actuel
DECISIONS.md      ← décisions actives
docs/             ← documentation complète par domaine
```

---

## Étape 2 — Lire les 4 fichiers obligatoires (10 min)

Dans cet ordre :

1. **`AGENTS.md`** — qui peut faire quoi, les interdictions absolues
2. **`MEMORY.md`** — état actuel du framework
3. **`SCOPE.md`** — ce qui est IN scope et ce qui ne l'est pas
4. **`DECISIONS.md`** — les décisions structurantes déjà prises

> Si vous ne lisez pas ces 4 fichiers, vous ne pouvez pas configurer correctement vos agents.

---

## Étape 3 — Configurer vos agents IA (10 min)

### Pour GitHub Copilot (VS Code)

Copiez les fichiers d'instructions dans votre dépôt projet :

```bash
cp -r .github/instructions/ votre-projet/.github/instructions/
cp .github/copilot-instructions.md votre-projet/.github/copilot-instructions.md
```

### Pour Claude Code

Copiez `CLAUDE.md` dans votre dépôt projet. Claude lira ce fichier automatiquement.

### Vérification

Ouvrez une conversation avec votre agent et demandez-lui :
> "Quel est ton rôle dans ce projet et quelles sont tes interdictions absolues ?"

La réponse doit référencer AGENTS.md.

---

## Étape 4 — Configurer le premier quality gate (5 min)

### Gate G5 minimum — secrets

Activez `git-secrets` sur votre dépôt :

```bash
git secrets --install
git secrets --register-aws
```

Ajoutez vos patterns projet :

```bash
git secrets --add 'sk-[a-zA-Z0-9]{32,}'   # tokens OpenAI
git secrets --add 'ghp_[a-zA-Z0-9]{36}'    # tokens GitHub
```

Pour les autres gates (G3-G4 : lint + tests), référez-vous à `docs/quality/QUALITY_GATES.md`.

---

## Étape 5 — Première utilisation (5 min)

### Créer une tâche avec DoD

Avant de demander quoi que ce soit à un agent, définissez un DoD en ≤ 8 lignes :

```markdown
## DoD — [Titre de la tâche]
- [ ] [Critère 1 binaire]
- [ ] [Critère 2 binaire]
- [ ] CHANGELOG.md mis à jour
- [ ] SESSION_LOG.md mis à jour
- [ ] Aucun secret dans les fichiers modifiés
```

### Demander à l'agent

Incluez toujours le DoD dans votre prompt :

```
En respectant AGENTS.md, SCOPE.md et le DoD ci-dessous, implémente [tâche].

DoD :
- [ ] ...
```

---

## Vérifier que tout fonctionne

Après votre première session avec un agent :

```
□ SESSION_LOG.md a une nouvelle entrée
□ CHANGELOG.md a été mis à jour (section Unreleased)
□ Le DoD est entièrement coché
□ Aucun secret n'est apparu dans les fichiers
□ Les fichiers de gouvernance (AGENTS.md, SCOPE.md) n'ont pas été modifiés
```

---

## Prochaines étapes

| Étape | Fichier de référence |
|-------|---------------------|
| Configurer le pipeline CI complet | `docs/delivery/CI_CD.md` |
| Comprendre les quality gates | `docs/quality/QUALITY_GATES.md` |
| Ajouter un nouvel agent | `docs/ai/AGENT_REGISTRY.md` |
| Créer un ADR pour une décision | `docs/adr/ADR-0001-template.md` |
| Configurer les secrets CI | `docs/security/SECRETS.md` |

---

## Problèmes fréquents

**L'agent modifie AGENTS.md ou SCOPE.md**  
→ Rappel explicite : ces fichiers nécessitent une validation humaine. Vérifiez le prompt de l'agent.

**L'agent déclare un test passé sans l'avoir exécuté**  
→ Interdiction absolue dans AGENTS.md §4. Signaler et corriger le prompt.

**Je ne sais pas si une décision est structurante**  
→ Si ça modifie l'architecture, la sécurité ou le scope → c'est structurant → ADR obligatoire.

---

_Pour aller plus loin : `GLOSSARY.md` (termes), `AGENTS.md` (constitution complète), `docs/governance/ENGINEERING_HANDBOOK.md` (pratiques)_
