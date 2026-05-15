# ARCHITECTURE.md — ASEF

> Source de vérité de la structure technique.  
> 1 responsabilité : décrire ce que le système EST, pas pourquoi il existe (→ PROJECT.md).  
> Dépend de : SCOPE.md, DECISIONS.md  
> Ne doit jamais contenir : règles agents, politiques de sécurité, procédures QA.

---

## Vue système

```
┌─────────────────────────────────────────────────────────────────┐
│                    ASEF — Vue système                            │
│                                                                  │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐  │
│  │   Humains   │────▶│  Demande /  │────▶│   Agents IA     │  │
│  │ (Dev/TL/PO) │     │   Cadrage   │     │ (Claude/Copilot)│  │
│  └─────────────┘     └─────────────┘     └────────┬────────┘  │
│                                                    │            │
│  ┌─────────────────────────────────────────────────▼──────────┐ │
│  │               COUCHE DE GOUVERNANCE ASEF                    │ │
│  │  AGENTS.md · SCOPE.md · QUALITY_GATES.md · SECURITY.md    │ │
│  └─────────────────────────────────────────────────┬──────────┘ │
│                                                    │            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────▼──────────┐ │
│  │ Génération   │  │   Tests &    │  │   Sécurité &          │ │
│  │    Code      │  │    QA        │  │   Supply Chain        │ │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬──────────┘ │
│         │                 │                        │            │
│  ┌──────▼─────────────────▼────────────────────────▼──────────┐ │
│  │                 PIPELINE CI/CD                               │ │
│  │        GitHub Actions · Preuves · Artifacts                 │ │
│  └─────────────────────────────────────────────────┬──────────┘ │
│                                                    │            │
│  ┌─────────────────────────────────────────────────▼──────────┐ │
│  │               VALIDATION & LIVRAISON                        │ │
│  │        Gate 7 (humain) · Release · Audit trail             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Modules principaux

### Module 1 — Gouvernance documentaire

**Responsabilité :** Définir les règles, périmètres, décisions et mémoire du framework.

**Fichiers :**
- `AGENTS.md` — constitution agents (source de vérité unique)
- `SCOPE.md` — périmètre (contrat anti-dérive)
- `MEMORY.md` — état actuel du projet
- `DECISIONS.md` — registre ADR

**Contraintes :**
- AGENTS.md ne dépend d'aucun autre fichier (racine de la hiérarchie)
- Toute modification de AGENTS.md ou SCOPE.md nécessite une validation humaine

---

### Module 2 — Instructions agentiques

**Responsabilité :** Configurer le comportement des agents par outil et par domaine.

**Fichiers :**
- `CLAUDE.md` — adaptateur Claude Code
- `.github/copilot-instructions.md` — adaptateur GitHub Copilot
- `.github/instructions/*.instructions.md` — 6 domaines spécialisés

**Contraintes :**
- Les adaptateurs ne dupliquent pas AGENTS.md — ils le référencent
- Chaque fichier d'instructions a un `applyTo` défini

---

### Module 3 — Pipeline de génération et contrôle

**Responsabilité :** Orchestrer la génération de code, les tests et les contrôles.

**Flux :**
```
Demande → [architect] → DoD → [developer] → Code → [qa] → Tests → [security] → Audit → Preuves
```

**Agents concernés :**
- `architect` : cadrage, décisions structurantes
- `developer` : implémentation
- `qa` : tests, coverage, evidence
- `security` : SAST, dependency audit, secret scan

**Sorties :**
- Code source (dans le repo)
- Rapport de tests (CI artifact)
- Evidence package (logs + captures)
- Entrée CHANGELOG.md

---

### Module 4 — Quality Gates

**Responsabilité :** Bloquer la livraison si les critères ne sont pas satisfaits.

**Référence :** `docs/quality/QUALITY_GATES.md`

**Gates (G0-G7) :**
| Gate | Déclencheur | Bloquant |
|------|-------------|---------|
| G0 | Toute demande | Oui |
| G1 | Avant cadrage | Oui |
| G2 | Avant dev | Oui si structurant |
| G3 | Avant tests | Oui |
| G4 | Avant sécu | Oui |
| G5 | Avant docs | Oui |
| G6 | Avant release | Oui |
| G7 | Release | Oui (humain) |

---

### Module 5 — Sécurité et Supply Chain

**Responsabilité :** Garantir l'intégrité du code, des dépendances et des processus.

**Fichiers :**
- `docs/security/SECURITY.md` — doctrine
- `docs/security/SUPPLY_CHAIN.md` — dépendances, SBOM
- `docs/security/SECRETS.md` — gestion secrets
- `docs/security/THREAT_MODEL.md` — modèle de menace IA

---

### Module 6 — Gouvernance IA

**Responsabilité :** Encadrer l'usage des modèles IA et des agents.

**Fichiers :**
- `docs/ai/AI_GOVERNANCE.md` — cas autorisés/interdits
- `docs/ai/MODEL_POLICY.md` — modèles validés
- `docs/ai/PROMPT_GOVERNANCE.md` — versioning prompts, anti-injection
- `docs/ai/EVALS.md` — benchmarks et métriques

---

### Module 7 — Delivery et Exploitation

**Responsabilité :** Piloter la livraison, les releases et l'observabilité.

**Fichiers :**
- `docs/delivery/CI_CD.md` — pipelines
- `docs/delivery/BRANCHING.md` — stratégie Git
- `docs/delivery/DEPLOYMENT.md` — procédure déploiement
- `docs/delivery/OBSERVABILITY.md` — logs, métriques agents

---

## Flux de données

### Données en transit entre agents

```
Humain → Demande texte → Agent [architect]
Agent [architect] → DoD + spec → Agent [developer]
Agent [developer] → Code diff + logs → Agent [qa]
Agent [qa] → Rapport tests → Agent [security]
Agent [security] → Rapport sécurité → Agent [orchestrator]
Agent [orchestrator] → Evidence package → Humain (Gate 7)
```

### Données envoyées aux modèles LLM

- Code source du projet : **autorisé** (voir MODEL_POLICY.md)
- Données utilisateurs : **interdit sans validation** (voir AI_GOVERNANCE.md)
- Secrets, credentials : **interdit absolument**

---

## Contraintes techniques

| Contrainte | Raison | Référence |
|------------|--------|-----------|
| Markdown comme source de vérité | Lisible par humains et agents, versionnable Git | PROJECT.md |
| Pas de runtime ASEF propre | ASEF gouverne, les outils exécutent | SCOPE.md |
| CI/CD via GitHub Actions | Stack définie, intégration native Copilot | PROJECT.md |
| Agents sans accès prod direct | Excessive agency non acceptable | SECURITY.md |

---

## Dette technique actuelle

| Dette | Impact | Plan |
|-------|--------|------|
| Scripts de validation non créés | Checklist manuelle | V1 |
| Eval framework non automatisé | Évaluations manuelles | Entreprise |
| SBOM non généré automatiquement | Supply chain partielle | Régulé |
| Agent Registry non implémenté | Catalogue manuel | V2 |
