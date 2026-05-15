# ASEF — Agentic Software Engineering Framework

> Framework de production logicielle augmentée par agents IA.  
> Gouvernable. Auditable. Industrialisable.

## Statut

| Version | Statut | Phase |
|---------|--------|-------|
| 0.1.0 | Sprint 0 Fermé — Sprint 1 en préparation | Bootstrap documentaire complet |

## Ce qu'est ASEF

ASEF est un framework d'engineering gouvernable qui permet à une organisation de cadrer, générer, tester, sécuriser, auditer et livrer du logiciel avec des agents IA — tout en conservant un contrôle humain, documentaire, technique et organisationnel.

**ASEF n'est pas** un outil de vibe coding, un wrapper LLM, un générateur de code magique, ni un ensemble de prompts.

**Le pipeline central :**
```
Demande → Cadrage → Génération → Contrôle → Tests → Sécurité → Preuves → Validation → Livraison → Audit → Amélioration
```

## Démarrage rapide

```bash
# 1. Lire la constitution agents
cat AGENTS.md

# 2. Vérifier le périmètre
cat SCOPE.md

# 3. Lancer une tâche via le modèle opérationnel
cat docs/governance/OPERATING_MODEL.md
```

## Structure du dépôt

```
ASEF/
├── AGENTS.md                    # Constitution générale multi-agent [MVP]
├── CLAUDE.md                    # Adaptateur Claude Code [MVP]
├── PROJECT.md                   # Mission, vision, principes fondateurs [MVP]
├── SCOPE.md                     # Périmètre strict — IN / OUT [MVP]
├── MEMORY.md                    # Mémoire active courante [MVP]
├── DECISIONS.md                 # Registre décisions structurantes [MVP]
├── CHANGELOG.md                 # Historique versions [MVP]
├── SESSION_LOG.md               # Journal des sessions [MVP]
├── .github/
│   ├── copilot-instructions.md  # Adaptateur GitHub Copilot [MVP]
│   └── instructions/            # Instructions par domaine [MVP]
└── docs/
    ├── ARCHITECTURE.md          # Architecture technique [MVP]
    ├── governance/              # Gouvernance entreprise [ENT]
    ├── quality/                 # QA et quality gates [MVP]
    ├── security/                # Sécurité et supply chain [MVP]
    ├── ai/                      # Gouvernance IA [MVP]
    ├── delivery/                # Delivery et exploitation [ENT]
    └── adr/                     # Architecture Decision Records [MVP]
```

## Documents clés par objectif

| Objectif | Document |
|----------|----------|
| Comprendre le framework | [PROJECT.md](PROJECT.md) |
| Configurer un agent | [AGENTS.md](AGENTS.md) |
| Connaître le périmètre | [SCOPE.md](SCOPE.md) |
| Lancer une tâche | [docs/governance/OPERATING_MODEL.md](docs/governance/OPERATING_MODEL.md) |
| Valider un livrable | [docs/quality/QUALITY_GATES.md](docs/quality/QUALITY_GATES.md) |
| Auditer la sécurité | [docs/security/SECURITY.md](docs/security/SECURITY.md) |
| Gouverner l'IA | [docs/ai/AI_GOVERNANCE.md](docs/ai/AI_GOVERNANCE.md) |
| Tracer une décision | [DECISIONS.md](DECISIONS.md) |

## Priorités de lecture pour un nouvel agent

1. `AGENTS.md` — constitution et permissions
2. `MEMORY.md` — contexte actuel
3. `SCOPE.md` — ce qui est IN/OUT
4. `DECISIONS.md` — décisions structurantes actives
5. Instructions domaine dans `.github/instructions/`
