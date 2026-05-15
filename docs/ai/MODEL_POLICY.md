# MODEL_POLICY.md — ASEF

> Politique d'utilisation des modèles IA.  
> 1 responsabilité : définir les modèles autorisés, les données pouvant leur être envoyées et les règles de coût.  
> Dépend de : AI_GOVERNANCE.md  
> Ne doit jamais contenir : prompts, evals, règles agents.

---

## Modèles autorisés

### Modèles cloud autorisés

| Modèle | Fournisseur | Cas d'usage | Données autorisées |
|--------|------------|------------|-------------------|
| Claude Sonnet 4.x | Anthropic | Génération code, revue, documentation | Code source non sensible, specs techniques |
| Claude Haiku 3.x | Anthropic | Tâches légères, classification | Code source non sensible |
| GPT-4o | OpenAI | Alternative, génération code | Code source non sensible, specs techniques |
| GitHub Copilot | Microsoft/OpenAI | Auto-complétion IDE | Code source (selon accord GitHub) |
| Gemini 1.5 Pro | Google | Alternative | Code source non sensible |

### Modèles locaux autorisés (optionnel)

| Modèle | Outil | Cas d'usage | Avantage |
|--------|-------|------------|---------|
| Llama 3.x | Ollama | Tâches locales, données sensibles | Aucune donnée envoyée à l'extérieur |
| Mistral | Ollama | Génération légère | Aucune donnée envoyée à l'extérieur |
| Codestral | Ollama | Complétion code | Spécialisé code, local |

---

## Données autorisées par fournisseur

| Données | Anthropic (Claude) | OpenAI (GPT) | GitHub Copilot | Local (Ollama) |
|---------|-------------------|-------------|---------------|----------------|
| Code source non sensible | ✓ | ✓ | ✓ | ✓ |
| Spécifications techniques | ✓ | ✓ | ✓ | ✓ |
| Contenu de documentation | ✓ | ✓ | ✓ | ✓ |
| Données personnelles | ✗ | ✗ | ✗ | ✓ (local) |
| Données contractuelles confidentielles | ✗ | ✗ | ✗ | ✓ (local) |
| Secrets et credentials | ✗ | ✗ | ✗ | ✗ (jamais) |
| Code source classifié | ✗ | ✗ | Vérifier accord | ✓ (local) |

---

## Critères de sélection d'un modèle

| Critère | Guidance |
|---------|---------|
| Données sensibles | → Modèle local uniquement |
| Qualité maximale | → Claude Sonnet ou GPT-4o |
| Coût optimisé | → Claude Haiku ou Mistral local |
| Latence critique | → Modèle local ou Haiku |
| Conformité RGPD stricte | → Modèle local ou accord DPA signé avec fournisseur |

---

## Règles de coût

- Les modèles haute capacité (Sonnet, GPT-4o) sont réservés aux tâches qui le justifient
- Les tâches de classification, résumé simple, validation format → Haiku ou équivalent
- Un budget mensuel approximatif est défini par le CTO et révisé trimestriellement
- Toute dépense anormale (spike > 2x la moyenne) doit être signalée

---

## Ajout d'un nouveau modèle ou fournisseur

Processus obligatoire avant d'utiliser un nouveau fournisseur IA :

1. Revue des CGU et politique de confidentialité du fournisseur
2. Vérification que la politique de rétention des données est acceptable
3. Accord DPA (Data Processing Agreement) si données personnelles
4. Validation Tech Lead
5. Ajout dans ce fichier avec le tableau de données autorisées

---

## Modèles interdits

| Modèle / Fournisseur | Raison |
|----------------------|--------|
| Modèles sans politique de confidentialité publiée | Risque de rétention de données |
| Modèles en beta public non contractuels | Pas de garanties de confidentialité |
| APIs non-officielles / proxies non contractuels | Risque fuite de données |
