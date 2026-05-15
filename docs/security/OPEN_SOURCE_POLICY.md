# OPEN_SOURCE_POLICY.md — ASEF

> Politique d'utilisation des composants open source.  
> 1 responsabilité : définir les licences autorisées, le processus d'approbation et les restrictions.  
> Dépend de : SUPPLY_CHAIN.md  
> Ne doit jamais contenir : audit de vulnérabilités (→ SUPPLY_CHAIN.md).

---

## Licences autorisées

Les dépendances avec les licences suivantes sont **approuvées par défaut** :

| Licence | Type | Usage autorisé |
|---------|------|---------------|
| MIT | Permissive | Tout usage, y compris commercial |
| Apache 2.0 | Permissive | Tout usage, attribution requise |
| BSD 2-Clause | Permissive | Tout usage |
| BSD 3-Clause | Permissive | Tout usage, non-endorsement |
| ISC | Permissive | Tout usage |
| CC0 1.0 | Domaine public | Tout usage |
| Unlicense | Domaine public | Tout usage |

---

## Licences nécessitant une revue

Les dépendances avec les licences suivantes **nécessitent une approbation Tech Lead** avant ajout :

| Licence | Contrainte | Conditions d'approbation |
|---------|-----------|------------------------|
| LGPL v2.1 | Copyleft faible | Utilisation en bibliothèque dynamique seulement |
| LGPL v3 | Copyleft faible | Utilisation en bibliothèque dynamique seulement |
| Mozilla Public License 2.0 | Copyleft par fichier | Fichiers MPL non modifiés |
| EUPL | Copyleft européen | Analyse juridique requise |

---

## Licences interdites

Les dépendances avec les licences suivantes sont **interdites** sans exception légale :

| Licence | Raison |
|---------|--------|
| GPL v2 | Copyleft fort — contamination du code propriétaire |
| GPL v3 | Copyleft fort — contamination du code propriétaire |
| AGPL v3 | Copyleft réseau — applicable aux SaaS |
| SSPL | Copyleft commercial très étendu |
| CC BY-NC | Non commercial — interdit usage commercial |
| Propriétaire sans licence | Aucun droit d'utilisation |

---

## Processus d'ajout d'une dépendance open source

1. Identifier la licence avec l'outil de détection automatique
2. Vérifier la conformité avec ce fichier
3. Si licence "revue requise" → ouvrir un ticket + validation Tech Lead avant merge
4. Si licence interdite → chercher une alternative ou escalader vers CTO
5. Documenter l'approbation dans le ticket associé

```bash
# Vérification de licence automatique
npx license-checker --summary
pip-licenses --format=markdown
```

---

## Détection automatique dans le CI

Le pipeline CI vérifie les licences à chaque PR :

```bash
npx license-checker --onlyAllow "MIT;ISC;Apache-2.0;BSD-2-Clause;BSD-3-Clause;CC0-1.0" \
  --excludePrivatePackages --json > reports/licenses.json
```

Un finding de licence interdite = Gate 5 rouge.

---

## Contributions open source depuis ASEF

Avant de contribuer du code ASEF à un projet open source externe :
- Validation Tech Lead obligatoire
- Vérifier qu'aucun code confidentiel n'est inclus
- La contribution ne doit pas révéler d'information sur l'architecture interne

---

## Registre des exceptions

Toute dépendance avec une licence "revue requise" approuvée est listée ici :

| Package | Licence | Approuvé par | Date | Justification |
|---------|---------|-------------|------|--------------|
| _(aucune exception active)_ | | | | |
