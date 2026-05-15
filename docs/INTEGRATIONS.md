# INTEGRATIONS.md — ASEF

> Source de vérité des intégrations externes.  
> 1 responsabilité : documenter chaque intégration avec ses permissions, ses risques et ses règles.  
> Dépend de : ARCHITECTURE.md, ACCESS_CONTROL.md, MODEL_POLICY.md  
> Ne doit jamais contenir : secrets ou tokens (→ SECRETS.md), modèles IA en détail (→ MODEL_POLICY.md).

---

## GitHub

**Usage :** Hébergement du code, gestion des issues et PR, CI/CD via GitHub Actions.

| Permission | Niveau | Justification |
|-----------|--------|-------------|
| Repository read | Agents (lecture code) | Indexation et analyse |
| Repository write | Developer, CI | Push, merge, tags |
| Actions write | CI uniquement | Déclencher des runs |
| Packages | CI/DevOps | Publication d'artifacts |
| Secrets | Tech Lead uniquement | Gestion des credentials CI |

**Risques :**
- Exposition de secrets si un secret est pushé par erreur (→ Gitleaks en CI)
- Fork malveillant d'actions tierces (→ pinning par SHA)
- Permissions excessives dans les workflows (→ principe de moindre privilège)

---

## GitHub Copilot

**Usage :** Assistance à la rédaction de code dans VS Code.

| Aspect | Configuration ASEF |
|--------|------------------|
| Instructions actives | `.github/copilot-instructions.md` |
| Instructions domaine | `.github/instructions/*.instructions.md` |
| Données envoyées | Code source du workspace courant |
| Données interdites | Secrets, PII — ne jamais inclure dans le code ouvert |

**Règles :**
- Les suggestions Copilot sont soumises aux mêmes gates que le code humain
- Ne pas accepter en aveugle — reviewer le code généré
- Les instructions ASEF orientent les suggestions vers les standards internes

---

## Claude Code (Anthropic)

**Usage :** Agent de développement IA, génération de code, documentation, analyse.

| Aspect | Configuration ASEF |
|--------|------------------|
| Bootstrap | `CLAUDE.md` (7 étapes) |
| Modèle | Claude Sonnet (voir MODEL_POLICY.md) |
| Données envoyées | Code source non sensible, contexte gouvernance |
| Permissions agents | Définies dans AGENT_REGISTRY.md |

**Règles :**
- `CLAUDE.md` est lu en premier à chaque session
- Les actions agent sont loggées (OBSERVABILITY.md)
- Les fichiers de gouvernance sont en lecture seule pour les agents

---

## GitHub Actions (CI/CD)

**Usage :** Pipeline d'intégration et de déploiement continu.

| Workflow | Déclencheur | Jobs |
|---------|------------|------|
| `ci.yml` | PR vers main | lint, test, security |
| `release.yml` | Tag `v*.*.*` | validate, build, release |

**Sécurité :**
- Toutes les actions tierces sont pinnées par SHA (SUPPLY_CHAIN.md)
- Les secrets ne sont pas disponibles dans les PR de forks
- Les permissions sont minimales par job (`contents: read` par défaut)

---

## Fournisseurs LLM (API externes)

Voir MODEL_POLICY.md pour la liste complète.

| Fournisseur | Endpoint | Données envoyées | Régime de données |
|------------|---------|-----------------|-----------------|
| Anthropic | api.anthropic.com | Code source, prompts | Zero Data Retention possible |
| OpenAI | api.openai.com | Code source, prompts | Data opt-out disponible |
| GitHub Copilot | Inclus VS Code | Code workspace | Microsoft DPA |

---

## Ollama (modèles locaux)

**Usage :** Exécution locale de modèles IA sans envoi de données en dehors.

| Aspect | Valeur |
|--------|--------|
| Endpoint | http://localhost:11434 |
| Données | Restent en local |
| Avantage | Sécurité maximale pour données sensibles |
| Limites | Capacités inférieures aux modèles cloud |

Voir MODEL_POLICY.md §Modèles locaux autorisés.

---

## npm / PyPI (registres de paquets)

**Usage :** Installation et gestion des dépendances.

**Règles :**
- Audit systématique avant installation (SUPPLY_CHAIN.md)
- Vérification des licences (OPEN_SOURCE_POLICY.md)
- Pas d'installation de paquet en dehors du CI ou d'une session de développement locale
- Les nouvelles dépendances nécessitent une revue (SUPPLY_CHAIN.md §Ajout d'une dépendance)

---

## Intégrations non autorisées

Toute intégration non listée ci-dessus doit être :
1. Documentée dans ce fichier
2. Évaluée pour les risques (THREAT_MODEL.md)
3. Approuvée par le Tech Lead (GOVERNANCE.md)
4. Conforme à MODEL_POLICY.md si traitement LLM
