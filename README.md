# ASEF — Agentic Software Engineering Framework

> Framework de production logicielle augmentée par agents IA.  
> Gouvernable. Auditable. Industrialisable.

## Statut

| Version | Statut | Phase |
|---------|--------|-------|
| **0.2.0** | **Actif** | **ASEF 2.0 — governance layer (core, context, missions, playbooks)** |
| 0.1.2 | Livré | Runtime — agents, skills, tools, schemas, policies, registry |
| 0.1.1 | Livré | Security documentation |
| 0.1.0 | Livré | Bootstrap documentaire complet |

## Ce qu'est ASEF

ASEF est un framework d'engineering gouvernable qui permet à une organisation de cadrer, générer, tester, sécuriser, auditer et livrer du logiciel avec des agents IA — tout en conservant un contrôle humain, documentaire, technique et organisationnel.

**ASEF n'est pas** un outil de vibe coding, un wrapper LLM, un générateur de code magique, ni un ensemble de prompts.

**Le pipeline central :**
```
Demande → Cadrage → Génération → Contrôle → Tests → Sécurité → Preuves → Validation → Livraison → Audit → Amélioration
```

## Démarrage rapide

```bash
# Installer le runtime Python
pip install -e .

# Lancer une tâche (dry-run)
asef run "Décris ta tâche ici" --dry-run

# Lancer une tâche (réelle, nécessite LLM_PROVIDER + LLM_API_KEY dans .env)
asef run "Décris ta tâche ici"

# Exécuter les tests
pytest tests/ -x -q
```

**Bootstrap documentaire :**
```bash
# 1. Lire la constitution agents
cat AGENTS.md

# 2. Vérifier le périmètre
cat SCOPE.md

# 3. Séquence bootstrap 7 étapes
cat context/CONTEXT_LOADING.md
```

## Structure du dépôt

```
ASEF/
├── AGENTS.md                    # Constitution générale multi-agent
├── MANIFEST.md                  # 12 garanties publiques ASEF (G-01 à G-12) [v0.2]
├── VISION.md                    # Vision ASEF 2.0 — architecture 3 couches [v0.2]
├── CLAUDE.md                    # Adaptateur Claude Code
├── PROJECT.md                   # Mission, vision, principes fondateurs
├── SCOPE.md                     # Périmètre strict — IN / OUT
├── MEMORY.md                    # Mémoire active courante
├── DECISIONS.md                 # Registre décisions structurantes
├── CHANGELOG.md                 # Historique versions
├── SESSION_LOG.md               # Journal des sessions
├── asef/                        # Package Python runtime [v0.1.2]
│   ├── __init__.py
│   ├── cli.py                   # Entrypoint CLI — `asef run`
│   ├── config.py                # Config.from_env()
│   ├── orchestrator.py          # Pipeline G0→G7
│   ├── agents.py                # Agents & rôles
│   ├── gates.py                 # Quality gates
│   ├── memory.py                # Persistance mémoire
│   ├── provider.py              # Abstraction LLM (OpenAI, Anthropic…)
│   └── tools.py                 # ToolExecutor + is_destructive()
├── tests/                       # 5 tests pytest (exit 0) [v0.1.2]
├── pyproject.toml               # Config projet + dépendances
├── .env.example                 # Template variables d'environnement
├── core/                        # 10 frameworks primitifs universels [v0.2]
│   ├── ASEF-Core.md             # 10 agents universels, pipeline G0-G9
│   ├── ASEF-Gates.md            # Gates G0-G9 avec checklists
│   ├── ASEF-Memory.md           # Modèle mémoire systémique
│   ├── ASEF-Evidence.md         # Taxonomie de preuves (7 types)
│   ├── ASEF-Risk.md             # 9 catégories de risque, scoring P×I
│   ├── ASEF-HITL.md             # 13 triggers Human-in-the-Loop
│   ├── ASEF-Workflow.md         # Statuts, WF-INTAKE, WF-EXECUTION
│   ├── ASEF-Decision.md         # 6 types de décision, format ADR
│   ├── ASEF-AgentGov.md         # Cycle de vie agents, contrats, permissions
│   └── ASEF-Audit.md            # 14 questions fondamentales, 5 types d'audit
├── context/                     # Gestion du contexte agent [v0.2]
│   ├── CONTEXT_BUDGET.md        # Budgets tokens par type de tâche
│   ├── CONTEXT_LOADING.md       # Séquence bootstrap 7 étapes
│   └── CONTEXT_PRIORITY.md     # Priorité 10 niveaux, résolution conflits
├── missions/                    # Cycle de vie des missions [v0.2]
│   ├── active/                  # Missions en cours
│   ├── completed/               # Missions terminées (DoD + preuves)
│   ├── blocked/                 # Missions bloquées (gate FAIL ou HITL)
│   └── archived/                # Missions annulées / obsolètes
├── playbooks/                   # Playbooks opérationnels [v0.2]
│   ├── create-new-framework.md
│   ├── improve-framework.md
│   ├── specialize-framework.md
│   ├── produce-evidence-package.md
│   ├── run-go-no-go.md
│   ├── run-maturity-assessment.md
│   └── use-copilot-cli-for-patch.md
├── evaluations/                 # Grilles d'évaluation [v0.2]
│   └── MISSION_SCORECARD.md     # 20 points — ACCEPTED/PARTIAL/REJECTED
├── domains/                     # Frameworks domaine (héritent de core/) [v0.2]
│   └── software/
│       └── ASEF-QA/             # Framework QA — 4 agents, 2 workflows
├── .github/
│   ├── copilot-instructions.md  # Adaptateur GitHub Copilot
│   └── instructions/            # Instructions par domaine
└── docs/
    ├── ARCHITECTURE.md
    ├── governance/
    ├── quality/                 # QA et quality gates
    ├── security/
    ├── ai/                      # Gouvernance IA
    ├── delivery/
    └── adr/                     # Architecture Decision Records
```

## Documents clés par objectif

| Objectif | Document |
|----------|----------|
| Installer le runtime | [pyproject.toml](pyproject.toml) + `.env.example` |
| Comprendre le framework | [PROJECT.md](PROJECT.md) |
| Vision ASEF 2.0 | [VISION.md](VISION.md) |
| 12 garanties publiques | [MANIFEST.md](MANIFEST.md) |
| Configurer un agent | [AGENTS.md](AGENTS.md) |
| Connaître le périmètre | [SCOPE.md](SCOPE.md) |
| Lancer une tâche | [docs/governance/OPERATING_MODEL.md](docs/governance/OPERATING_MODEL.md) |
| Valider un livrable | [docs/quality/QUALITY_GATES.md](docs/quality/QUALITY_GATES.md) |
| Produire des preuves | [playbooks/produce-evidence-package.md](playbooks/produce-evidence-package.md) |
| Auditer la sécurité | [docs/security/SECURITY.md](docs/security/SECURITY.md) |
| Gouverner l'IA | [docs/ai/AI_GOVERNANCE.md](docs/ai/AI_GOVERNANCE.md) |
| Évaluer la maturité | [playbooks/run-maturity-assessment.md](playbooks/run-maturity-assessment.md) |
| Tracer une décision | [DECISIONS.md](DECISIONS.md) |

## Priorités de lecture pour un nouvel agent

1. `AGENTS.md` — constitution et permissions
2. `MANIFEST.md` — 12 garanties non négociables
3. `MEMORY.md` — contexte actuel
4. `SCOPE.md` — ce qui est IN/OUT
5. `DECISIONS.md` — décisions structurantes actives
6. `core/ASEF-Core.md` — primitifs universels
7. Instructions domaine dans `.github/instructions/`
