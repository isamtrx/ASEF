# ACCESS_CONTROL.md — ASEF

> Source de vérité du contrôle d'accès.  
> 1 responsabilité : définir qui a accès à quoi, selon quel niveau de privilège.  
> Dépend de : SECURITY.md, AGENTS.md  
> Ne doit jamais contenir : secrets réels, credentials.

---

## Principe du moindre privilège

Chaque acteur (humain ou agent) dispose uniquement des accès strictement nécessaires à son rôle. Tout accès supplémentaire doit être demandé, justifié, temporaire et traçable.

---

## Rôles et accès GitHub

| Rôle | Niveau GitHub | Qui | Accès |
|------|-------------|-----|-------|
| Admin | Owner | CTO | Paramètres repo, branches protégées, secrets CI |
| Mainteneur | Maintainer | Tech Lead | Merge sur main, gestion labels, reviews obligatoires |
| Développeur | Write | Équipe | Push sur branches feature, ouverture PR |
| Observateur | Read | Auditeur externe | Lecture seule |
| Agent CI | Permissions scope | GitHub Actions | Lecture code, écriture artifacts, secrets CI déclarés |

---

## Règles branches protégées

La branche `main` doit avoir les protections suivantes :
- Pas de push direct (force push interdit)
- Revue obligatoire par au moins 1 maintainer (Tech Lead)
- CI devant passer avant merge (G3, G4, G5 au minimum)
- Pas de merge si la branche est outdated

---

## Accès CI/CD (GitHub Actions)

| Permission | Justification | Accordé |
|-----------|--------------|---------|
| `contents: read` | Lire le code source | Oui |
| `contents: write` | Créer des releases, tags | Seulement lors de la release |
| `id-token: write` | OIDC pour AWS/Azure | Si déploiement cloud |
| `pull-requests: write` | Poster des commentaires de revue | Limité aux jobs de revue |
| `packages: write` | Publier des packages | Limité aux jobs de release |

**Règle :** Les permissions GitHub Actions sont déclarées au niveau du job, pas du workflow global. Utiliser `permissions: {}` par défaut + overrides par job.

---

## Accès aux secrets CI/CD

| Secret | Accessible par | Jamais accessible par |
|--------|--------------|----------------------|
| Clés API LLM | Job de génération code | Tous les autres jobs |
| Credentials cloud | Job de déploiement | Tous les autres jobs |
| Token GitHub | Job de release | Tous les autres jobs |

---

## Permissions des agents IA

Les permissions des agents sont définies dans `AGENTS.md`. Résumé :

| Action | Agent seul | Validation TL | Interdit agents |
|--------|-----------|--------------|----------------|
| Lire le code | ✓ | — | — |
| Écrire du code | ✓ | — | — |
| Modifier AGENTS.md | — | ✓ | — |
| Merger sur main | — | — | ✗ Toujours |
| Lire .env | — | — | ✗ Toujours |
| Appeler API externe non listée | — | — | ✗ Toujours |
| Committer un secret | — | — | ✗ Toujours |

---

## Revue trimestrielle des accès

Chaque trimestre, le Tech Lead vérifie :
- Les membres ayant accès Write ou plus → vérifier qu'ils sont toujours actifs
- Les tokens de service → vérifier qu'ils sont toujours nécessaires et expirés si possible
- Les secrets CI/CD → vérifier la liste, supprimer les inutilisés
- Les GitHub Apps et intégrations tierces → vérifier les permissions accordées

Résultat tracé dans `SESSION_LOG.md` et dans les métriques de AUDIT.md.

---

## Offboarding

À chaque départ d'un membre de l'équipe :
- Révoquer l'accès GitHub dans les 24h
- Faire tourner les secrets partagés qu'il connaissait
- Révoquer les tokens personnels d'accès
- Documenter l'action dans SESSION_LOG.md
