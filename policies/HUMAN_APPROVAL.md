# POLICY: HUMAN APPROVAL

**Source** : AGENTS.md §3 + §10
**Statut** : active
**ID** : POL-HUMAN-001

## Actions nécessitant validation humaine

| Action | Gate | Urgence |
|---|---|---|
| Release (tout type) | G7 | Obligatoire |
| Merge sur main/production | — | Obligatoire |
| Modification SCOPE.md | — | Obligatoire + ADR |
| Modification AGENTS.md | — | Obligatoire + ADR |
| Émission d'exception à un quality gate | — | Obligatoire |
| Accès environnement production | — | Obligatoire |
| Révocation/rotation d'un secret | — | Obligatoire |
| Réponse à une escalade CRITIQUE | — | Obligatoire |

## Protocole

1. Pipeline pause → état `APPROVAL_PENDING`
2. Présenter le plan d'orchestration JSON à l'humain
3. Attendre réponse explicite ("ok", "approuvé", etc.)
4. Documenter la réponse dans SESSION_LOG.md
5. Reprendre ou arrêter selon la réponse

## Ce qu'un agent ne peut PAS faire

- Simuler une réponse humaine
- Auto-approuver une release
- Contourner Gate G7
- Reprendre après escalade CRITIQUE sans réponse

## Validation

`python execution/validate_policies.py` → vérifie que Gate G7 est toujours dans release workflow
