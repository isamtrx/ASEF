# TOOL_REGISTRY.md — ASEF

> Catalogue de tous les outils disponibles pour les agents.  
> 1 responsabilité : définir quels outils un agent peut utiliser, avec quel niveau de risque.  
> Dépend de : AGENT_REGISTRY.md, AI_GOVERNANCE.md  
> Ne doit jamais contenir : définitions des agents (→ AGENT_REGISTRY.md).

---

## Classification des outils

| Niveau de risque | Description | Validation humaine |
|-----------------|-------------|-------------------|
| FAIBLE | Lecture seule, pas d'effet de bord | Non requise |
| MOYEN | Écriture réversible, impact limité | Non requise (traçabilité obligatoire) |
| ÉLEVÉ | Écriture irréversible, accès système, réseau externe | Recommandée |
| CRITIQUE | Déploiement, suppression, accès secrets | Toujours obligatoire |

---

## Outils de lecture (Niveau FAIBLE)

| Outil | Description | Agents autorisés |
|-------|-------------|-----------------|
| `read_file` | Lit le contenu d'un fichier | Tous |
| `list_dir` | Liste le contenu d'un répertoire | Tous |
| `grep_search` | Recherche textuelle dans les fichiers | Tous |
| `file_search` | Recherche de fichiers par pattern | Tous |
| `semantic_search` | Recherche sémantique dans le codebase | Tous |
| `get_errors` | Récupère les erreurs de compilation/lint | Developer, QA |
| `vscode_listCodeUsages` | Trouve les usages d'un symbole | Developer, Architect |

---

## Outils d'écriture (Niveau MOYEN)

| Outil | Description | Agents autorisés | Restriction |
|-------|-------------|-----------------|------------|
| `create_file` | Crée un nouveau fichier | Developer, Docs | Hors AGENTS.md, SCOPE.md |
| `replace_string_in_file` | Modifie une portion de fichier | Developer, Docs | Hors AGENTS.md |
| `multi_replace_string_in_file` | Modifications multiples | Developer | Hors fichiers de gouvernance |
| `manage_todo_list` | Gère la liste de tâches | Tous | — |
| `memory` | Lit/écrit les fichiers mémoire | Tous | — |

---

## Outils d'exécution (Niveau MOYEN à ÉLEVÉ)

| Outil | Description | Agents autorisés | Risque | Validation |
|-------|-------------|-----------------|--------|-----------|
| `run_in_terminal` | Exécute une commande shell | Developer, QA | MOYEN | Traçabilité obligatoire |
| `get_terminal_output` | Récupère l'output d'un terminal | Developer, QA | FAIBLE | — |

---

## Outils navigateur (Niveau MOYEN)

| Outil | Description | Agents autorisés |
|-------|-------------|-----------------|
| `mcp_microsoft_pla_browser_navigate` | Navigation web | QA (tests E2E) |
| `mcp_microsoft_pla_browser_take_screenshot` | Screenshot navigateur | QA |
| `mcp_microsoft_pla_browser_click` | Clic dans navigateur | QA |
| `mcp_io_github_chr_take_screenshot` | Screenshot Chrome | QA |

---

## Outils interdits aux agents (Niveau CRITIQUE)

Ces outils requièrent **toujours** une validation humaine explicite avant usage :

| Outil | Raison |
|-------|--------|
| Merge sur main | Décision de livraison — humain uniquement |
| Modification des secrets CI | Accès critique — humain uniquement |
| `rm -rf` / suppression massive | Irréversible — humain uniquement |
| Déploiement production | Gate 7 — humain obligatoire |
| Modification de AGENTS.md | Gouvernance — humain obligatoire |

---

## Appels API externes

Tout appel vers une API externe par un agent doit être :
1. Listé dans ce registre (outil ou endpoint)
2. Documenté avec le type de données envoyées
3. Conforme à MODEL_POLICY.md si données envoyées à un LLM

| Service externe | Usage | Données envoyées | Autorisé |
|----------------|-------|-----------------|---------|
| Anthropic API | Génération code / texte | Code source non sensible | ✓ |
| OpenAI API | Alternative Anthropic | Code source non sensible | ✓ |
| GitHub API | Gestion PR/issues | Metadata repo | ✓ |
| npm Registry | Installation packages | Noms de packages | ✓ |
| PyPI | Installation packages | Noms de packages | ✓ |
| Services non listés | — | — | ✗ Interdit sans validation |
