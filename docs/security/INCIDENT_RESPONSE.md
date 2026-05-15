# INCIDENT_RESPONSE.md — ASEF

> Source de vérité du processus de réponse aux incidents de sécurité.  
> 1 responsabilité : définir comment détecter, contenir, escalader et apprendre d'un incident.  
> Dépend de : SECURITY.md  
> Ne doit jamais contenir : résultats d'incidents (→ POSTMORTEMS.md).

---

## Niveaux d'incident

| Niveau | Description | Exemples |
|--------|-------------|---------|
| P1 — CRITICAL | Impact immédiat en production, données compromises | Secret exposé, accès non autorisé, service down |
| P2 — HIGH | Risque élevé, pas encore en production | Vulnérabilité exploitable détectée, anomalie agent |
| P3 — MEDIUM | Risque limité, contenu, pas d'impact utilisateur | Dépendance vulnérable sans exploit connu |
| P4 — LOW | Observation, bonnes pratiques | Finding SAST low severity |

---

## Contacts d'escalade

| Rôle | Responabilité | Délai de réponse |
|------|--------------|-----------------|
| Tech Lead | Coordination incident, décisions techniques | < 30min (P1/P2) |
| CTO | Décisions critiques, communication externe | < 1h (P1) |
| Équipe sécurité | Analyse technique, containment | < 30min (P1/P2) |

---

## Procédure P1 — CRITICAL

### Phase 1 : Détection et alerte (0-30min)

```
1. Détecter l'incident (alerte auto, signalement humain, detection agent)
2. Ouvrir immédiatement un ticket P1 (GitHub Issue ou équivalent)
3. Alerter Tech Lead et CTO par le canal d'urgence défini
4. Ne pas discuter de l'incident sur des canaux publics non chiffrés
```

### Phase 2 : Containment (0-4h)

```
5. Si secret exposé → révoquer immédiatement dans le service concerné
6. Si accès compromis → révoquer les tokens/sessions suspects
7. Si code malveillant → bloquer les livraisons, isoler la branche
8. Documenter chaque action avec horodatage dans le ticket P1
```

### Phase 3 : Éradication (4-24h)

```
9. Identifier la cause racine
10. Supprimer l'artefact compromis (secret de l'historique Git, code vulnérable)
11. Vérifier qu'aucune trace de la compromission ne subsiste
12. Remplacer les credentials compromis par des nouveaux
```

### Phase 4 : Rétablissement (24-72h)

```
13. Redéployer avec des credentials valides
14. Vérifier le bon fonctionnement complet
15. Informer les parties prenantes du rétablissement
```

### Phase 5 : Postmortem (< 1 semaine)

```
16. Écrire un postmortem dans POSTMORTEMS.md
17. Identifier les leçons apprises (LESSONS_LEARNED.md)
18. Implémenter les corrections structurelles
19. Clôturer le ticket P1
```

---

## Procédure P2 — HIGH

1. Ouvrir un ticket P2 dans les 2 heures
2. Alerter Tech Lead
3. Évaluer si une livraison en cours doit être bloquée
4. Corriger dans les 72h ou documenter une exception (EXCEPTIONS.md)

---

## Indicateurs d'alerte à surveiller

- Push direct sur main (CI devrait le bloquer, mais surveiller)
- Secret scan avec finding (Gate 5 rouge)
- Comportement agent anormal (exécution hors périmètre)
- Accès à des endpoints non autorisés par un agent
- Erreurs d'authentification en masse (brute force)
- SAST finding CRITICAL en PR

---

## Communication pendant un incident

- Canal interne sécurisé uniquement (ex : Slack privé chiffré)
- Pas de détail de l'incident sur des issues publiques GitHub tant que non résolu
- Notification utilisateurs uniquement si leurs données sont impactées (RGPD)
- Communication externe via CTO uniquement

---

## Postmortem obligatoire pour P1/P2

Chaque incident P1 ou P2 résolu génère une entrée dans `POSTMORTEMS.md` avec :
- Impact (qui, quoi, durée)
- Timeline détaillée
- Cause racine
- Ce qui a fonctionné dans la réponse
- Ce qui n'a pas fonctionné
- Actions correctives avec responsable et délai
