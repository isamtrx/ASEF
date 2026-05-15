# REPOSITORY_STRATEGY.md — ASEF

> Source de vérité de la stratégie de dépôt.  
> 1 responsabilité : décision mono/multi-repo, structure standard et fichiers obligatoires.  
> Dépend de : ARCHITECTURE.md, ENGINEERING_HANDBOOK.md  
> Ne doit jamais contenir : règles de branches (→ BRANCHING.md), CI/CD (→ CI_CD.md).

---

## Décision : Monorepo pour ASEF v0.x

**Décision :** ASEF utilise un monorepo unique pour le code, la gouvernance et la documentation.

**Justification :**
- Cohérence garantie entre le code et la gouvernance documentaire
- Un seul historique Git, traçabilité complète
- Simplicité pour un projet en phase MVP
- Pas de complexité de synchronisation inter-repos

**Révision :** Envisager multi-repo à partir de v1.x si la taille du monorepo ou l'organisation des équipes le justifie (ADR requis).

---

## Structure standard d'un repo ASEF

```
├── .github/
│   ├── copilot-instructions.md     ← Instructions GitHub Copilot
│   ├── instructions/               ← Instructions domaine (*.instructions.md)
│   ├── workflows/                  ← GitHub Actions
│   └── CODEOWNERS                  ← Propriétaires par zone
│
├── docs/
│   ├── ARCHITECTURE.md             ← Diagramme + modules
│   ├── DATA.md                     ← Gestion données
│   ├── API.md                      ← Standards API
│   ├── INTEGRATIONS.md             ← Intégrations externes
│   ├── REPOSITORY_STRATEGY.md      ← Ce fichier
│   ├── ai/                         ← Gouvernance IA
│   ├── delivery/                   ← CI/CD, déploiement
│   ├── governance/                 ← Gouvernance ingénierie
│   ├── quality/                    ← Gates, contrôles
│   ├── security/                   ← Sécurité
│   └── adr/                        ← ADRs individuels si trop nombreux
│
├── src/                            ← Code source
├── tests/                          ← Tests
├── scripts/                        ← Scripts utilitaires (non-app)
│
├── AGENTS.md                       ← Constitution agents (racine)
├── BACKLOG.md                      ← Backlog
├── CHANGELOG.md                    ← Historique des changements
├── CLAUDE.md                       ← Instructions Claude Code
├── CURRENT_SPRINT.md               ← Sprint actif
├── DECISIONS.md                    ← Registre ADR
├── LESSONS_LEARNED.md              ← Leçons capitalisées
├── MEMORY.md                       ← Mémoire de session
├── POSTMORTEMS.md                  ← Registre postmortems
├── PRODUCT.md                      ← Vision produit
├── PROJECT.md                      ← Mission et principes
├── ROADMAP.md                      ← Feuille de route
├── SCOPE.md                        ← Périmètre et anti-drift
├── SESSION_LOG.md                  ← Journal de sessions
│
├── .env.example                    ← Template variables env (sans secrets)
├── .gitignore                      ← Fichiers ignorés (inclut .env.local)
├── package.json                    ← Dépendances et scripts
└── README.md                       ← Point d'entrée public
```

---

## Fichiers obligatoires (checklist tout projet ASEF)

```
□ README.md              — Point d'entrée, rapide à lire
□ AGENTS.md              — Constitution agents
□ SCOPE.md               — Anti-drift
□ DECISIONS.md           — ADR register
□ CHANGELOG.md           — Keep a Changelog
□ .env.example           — Toutes les variables sans valeurs
□ .gitignore             — Avec .env.local et node_modules
□ .github/copilot-instructions.md
□ .github/workflows/ci.yml
□ CODEOWNERS             — Au moins un owner sur /
```

---

## Fichiers CODEOWNERS

```
# Gouvernance — Tech Lead obligatoire
AGENTS.md @tech-lead
SCOPE.md @tech-lead
DECISIONS.md @tech-lead
docs/security/ @security-lead @tech-lead
docs/ai/AI_GOVERNANCE.md @tech-lead

# Code source — Review par équipe
/src/ @team
/tests/ @team

# CI/CD — DevOps
/.github/workflows/ @devops @tech-lead
```

---

## Création d'un nouveau repo ASEF

1. Utiliser le template GitHub ASEF (si disponible) ou copier la structure ci-dessus
2. Initialiser avec les 10 fichiers obligatoires
3. Configurer branch protection sur main (BRANCHING.md §Protection)
4. Configurer les secrets CI (SECRETS.md §Stockage autorisé)
5. Valider avec `npm run validate` ou équivalent
6. Créer le premier ADR dans DECISIONS.md (ADR-0001 : choix de stack)
