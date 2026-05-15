# SCOPE.md — ASEF

> Source de vérité du **périmètre**.  
> 1 responsabilité : empêcher la dérive.  
> Ce fichier est un contrat, pas une suggestion.

---

## Périmètre actuel : Phase MVP

### IN SCOPE

**Documentation et gouvernance**
- Définition et maintien de l'arborescence documentaire ASEF
- Création et mise à jour des fichiers de gouvernance agents
- Gestion des décisions architecturales (ADR)
- Traçabilité des sessions et changements

**Orchestration agentique**
- Instructions pour agents Claude Code, GitHub Copilot
- Instructions spécialisées par domaine (frontend, backend, QA, sécurité, docs, IA)
- Définition des permissions, interdictions et workflows agents
- Quality gates et preuves de livraison

**Qualité et sécurité**
- Définition des quality gates (G0-G7)
- Stratégie QA et commandes de test
- Doctrine sécurité, supply chain, gestion des secrets
- Gouvernance IA : modèles autorisés, prompts, évaluations

**Stack supportée**
- VS Code + GitHub Copilot
- Claude Code (Claude Sonnet)
- GitHub + GitHub Actions CI/CD
- Markdown governance (fichiers .md)
- Scripts Bash/PowerShell de validation

### OUT OF SCOPE

**Ce qu'ASEF ne fait pas :**
- Exécution de code ou de tests (délégué aux outils CI/CD)
- Génération de code applicatif métier (délégué aux agents)
- Gestion des infrastructures cloud (délégué à la plateforme)
- Orchestration runtime LLM (pas d'API propre, pas de serveur)
- Formation des développeurs (délégué à l'ENGINEERING_HANDBOOK.md)
- Gestion des tickets/issues (délégué à GitHub Issues)
- Déploiement en production (délégué aux procédures DEPLOYMENT.md)

**Stack hors périmètre MVP :**
- Agents locaux (Ollama, LM Studio) — reporté à V2
- Intégrations Jira, Confluence, Slack — reporté à Entreprise
- Dashboards d'observabilité (Grafana, Datadog) — reporté à Régulé
- Runtime MCP personnalisé — reporté à V2

### Fonctionnalités refusées

| Fonctionnalité | Motif du refus |
|----------------|---------------|
| Auto-merge sans human sign-off | Risque sécurité, contredit le principe HITL |
| Agent avec accès prod direct | Excessive agency non acceptable |
| Prompts sans versioning | Contredit PROMPT_GOVERNANCE.md |
| Fichiers > 400 lignes sans justification | Signal de dérive responsabilité |
| Documentation auto-générée non validée | Hallucination sans preuve |

### Fonctionnalités reportées

| Fonctionnalité | Phase cible |
|----------------|------------|
| Agent Registry avec API | V2 |
| Eval framework automatisé | Entreprise |
| SBOM automatique | Régulé |
| SLO monitoring temps réel | Régulé |
| Multi-repo orchestration | V2 |

## Non-négociables

Ces éléments ne peuvent pas être négociés, retirés ou contournés :

1. **AGENTS.md doit exister avant toute tâche agentique.**
2. **Toute décision structurante doit être tracée dans DECISIONS.md avant implémentation.**
3. **Aucun secret ne peut être committé dans le dépôt.**
4. **Les quality gates G4 (tests) et G5 (sécurité) sont toujours bloquants.**
5. **MEMORY.md ne doit jamais être un fourre-tout — purge mensuelle obligatoire.**

## Signaux de dérive

Si l'un de ces signaux apparaît, stopper et arbitrer :

- Un fichier assume plus d'une responsabilité
- Du contenu est copié-collé entre deux fichiers
- Un agent exécute une action sans permission déclarée dans `AGENTS.md`
- Un changement est livré sans evidence package
- `README.md` contient des règles agents ou de l'architecture détaillée
- `MEMORY.md` dépasse 200 lignes
- Un quality gate est contourné sans exception tracée dans `EXCEPTIONS.md`

## Règles d'arbitrage

| Situation | Règle |
|-----------|-------|
| Demande hors scope | Refuser ou ouvrir une évolution de scope (ADR requis) |
| Fonctionnalité ambiguë | Défaut = OUT SCOPE jusqu'à arbitrage explicite |
| Conflit entre deux fichiers | Le fichier de plus haute priorité (PROJECT > SCOPE > ARCHITECTURE) prime |
| Feature demandée par utilisateur | Passer par BACKLOG.md → CURRENT_SPRINT.md → Gate 0 |

## Historique des évolutions de scope

| Date | Évolution | Décision |
|------|-----------|---------|
| 2026-05-15 | Scope initial MVP défini | ADR-0001 |
