# DIRECTIVE — web_research_policy

## Purpose

Définir comment effectuer des recherches web efficacement.  
Sans cette directive, `fetch_webpage` sur des sources larges = dump massif de texte brut → tokens gaspillés, résultats inutilisables.  
Pourquoi elle existe : correction session 2026-04-16 — fetch_webpage sur 10 repos GitHub = output énorme peu exploitable.  
Quand elle s'applique : toute demande impliquant une vérification en ligne ou une recherche de documentation.  
Quelle mauvaise action elle empêche : saturation de contexte, tokens brûlés sur du bruit.

## Scope

Couvre : toute recherche web dans une session ASEF.  
Ne couvre pas : lecture de fichiers locaux.

## Hiérarchie des outils de recherche

### 1. Outils navigateur (privilégiés)
- `mcp_microsoft_pla_browser_navigate` + `mcp_microsoft_pla_browser_snapshot` : navigation ciblée
- `mcp_io_github_chr_navigate_page` + `mcp_io_github_chr_take_screenshot` : capture structurée
- **Quand :** vérification d'URL spécifique, doc officielle, validation UI

### 2. Recherche structurée
- `mcp_microsoftdocs_microsoft_docs_search` : documentation Microsoft/Azure
- `mcp_microsoftdocs_microsoft_code_sample_search` : exemples de code officiels
- **Quand :** questions sur stack Microsoft (.NET, Azure, GitHub Actions)

### 3. `fetch_webpage` (usage restreint)
- **Uniquement pour :** pages simples, APIs JSON, contenu court et ciblé
- **Interdit pour :** catalogues (npm, PyPI, awesome-lists), repos GitHub entiers, pages de documentation longues

## Règles d'utilisation

1. Définir la **question précise** avant de rechercher — pas de recherche exploratoire massive
2. Cibler des URLs spécifiques plutôt que des pages d'index
3. Si le résultat dépasse 10 000 tokens → reformuler la requête plus précisément
4. Documenter la source dans le livrable final

## Mandatory Rules

- [WEB-001] Pas de fetch_webpage sur des sources catalogues ou des repos entiers
- [WEB-002] Préférer les outils navigateur pour toute navigation ciblée
- [WEB-003] Recherche web = question précise définie avant l'appel outil
