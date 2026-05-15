# STANDARDS.md — ASEF

> Standards transversaux applicables à tout le code, les APIs, les tests, les docs et les agents.  
> 1 responsabilité : définir les standards minimum non-négociables.  
> Dépend de : ENGINEERING_HANDBOOK.md (conventions détaillées)  
> Ne doit jamais contenir : conventions de naming, patterns domaine-spécifiques.

---

## Standards de code

### Principes universels
- Un fichier = une responsabilité
- Une fonction = une action (< 40 lignes hors tests)
- Pas de code mort livré (fonctions inutilisées, imports inutilisés)
- Pas de constante magique (utiliser des constantes nommées)
- Pas de duplication logique entre modules distincts

### TypeScript / JavaScript
- Strict mode obligatoire (`"strict": true` dans tsconfig)
- Zéro `any` non justifié (justification en commentaire si inévitable)
- Imports explicites, pas de barrel imports en cascades
- Async/await plutôt que callbacks

### Python
- Type hints obligatoires sur toutes les fonctions publiques
- PEP 8 strict (via ruff ou black)
- Docstring sur les classes et fonctions publiques (Google style)
- Zéro f-string SQL (→ paramètres liés)

### Go
- `gofmt` et `golangci-lint` propres
- Gestion d'erreurs explicite (pas d'`_` sur les erreurs)
- Pas de goroutines sans mécanisme d'arrêt

---

## Standards de tests

- Tests écrits en même temps que le code, pas après
- Nommage : `test_[fonction]_[cas]_[résultat_attendu]`
- Pattern AAA (Arrange / Act / Assert)
- Pas de logique métier dans les tests
- Pas de dépendance entre tests (chaque test est indépendant)
- Mocks limités aux frontières système (réseau, DB, FS)
- Coverage minimum : 80% sur le périmètre modifié

---

## Standards API

- REST : noms de ressources au pluriel, verbes HTTP sémantiques
- Versioning explicite dans l'URL : `/api/v1/`
- Format de réponse uniforme : `{ data, error, meta }`
- Format d'erreur : `{ code, message, details }`
- Codes HTTP sémantiques (400 vs 422 vs 500)
- Pagination sur toutes les listes (limit/offset ou cursor)
- Authentification via header Authorization (Bearer token)
- Pas de données sensibles dans les query params

---

## Standards de sécurité (résumé — détail dans docs/security/)

- Aucun secret dans le code source (→ variables d'environnement)
- Validation de toutes les entrées (côté serveur, pas seulement client)
- Outputs encodés selon le contexte (HTML, SQL, JSON)
- HTTPS obligatoire pour toutes les communications
- Principe du moindre privilège pour tous les accès

---

## Standards UI/Frontend

- Accessibilité WCAG 2.1 AA minimum
- Composants testés avec jest-axe
- Pas de styles inline (CSS modules ou design system)
- Images avec attributs alt systématiques
- Fonctionnement sans JavaScript pour le contenu critique
- Mobile-first (responsive à partir de 375px)

---

## Standards de documentation

- Un fichier = une responsabilité = une source de vérité
- Pas de duplication entre fichiers
- Maximum 400 lignes par fichier (au-delà = signal de dérive)
- Liens internes vérifiés avant livraison
- CHANGELOG.md mis à jour pour tout changement livrable
- Langue : français pour la gouvernance, langue du projet pour le code

---

## Standards de logs

- Format structuré JSON pour les logs en production
- Niveaux : DEBUG / INFO / WARN / ERROR / CRITICAL
- Pas de données personnelles ou secrets dans les logs
- Identifiant de corrélation (trace ID) sur chaque requête
- Rétention définie dans OBSERVABILITY.md

---

## Standards agents IA

- Tout prompt est versionné dans `docs/ai/PROMPT_GOVERNANCE.md`
- Tout output IA touché au code est revu (pas de commit aveugle)
- Aucun secret transmis dans le contexte d'un agent
- Résultat d'un eval IA requis avant merge d'un changement prompt
- Injection de prompt = alerte immédiate, blocage et escalade

---

## Vérification des standards

Les standards sont vérifiables via :
- Lint (G3 — automatique CI)
- Revue de code humaine (Gate 7 / PR review)
- Audit mensuel (AUDIT.md)

Un standard non respecté = commentaire de revue bloquant ou violation de Gate 3.
