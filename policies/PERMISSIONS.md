# POLICY: PERMISSIONS

**Source** : AGENTS.md §3 (extraite sans modification)
**Statut** : active
**ID** : POL-PERMISSIONS-001

## Matrice de permissions par rôle

| Action | architect | developer | qa | security | docs | orchestrator |
|---|---|---|---|---|---|---|
| Lire tous les fichiers | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Modifier le code source | — | ✓ | — | — | — | — |
| Créer des tests | — | ✓ | ✓ | — | — | — |
| Modifier DECISIONS.md | ✓ | — | — | — | — | ✓ |
| Modifier ARCHITECTURE.md | ✓ | — | — | — | — | — |
| Modifier CHANGELOG.md | — | ✓ | — | — | ✓ | ✓ |
| Modifier MEMORY.md | — | — | — | — | — | ✓ |
| Modifier SESSION_LOG.md | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Valider un quality gate | — | — | ✓ | ✓ | — | — |
| Approuver une release | — | — | — | — | — | — |

## Approbations humaines obligatoires

Ces actions ne peuvent pas être exécutées par un agent seul :

- Approbation finale de release (Gate G7)
- Émission d'une exception à un quality gate
- Modification du périmètre SCOPE.md
- Décision de merge sur branche protégée (main, production)
- Accès à un environnement de production
- Révocation ou rotation d'un secret

## Application

Implémentée techniquement dans `asef/tools.py` — `PROTECTED_FILES` + filtres.
Cette policy est une spécification — pas un mécanisme de confiance.

## Validation

`python execution/validate_policies.py` → vérifie que cette policy est cohérente avec tools.py
