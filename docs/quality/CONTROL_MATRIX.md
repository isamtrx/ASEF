# CONTROL_MATRIX.md — ASEF

> Source de vérité des contrôles auditables.  
> 1 responsabilité : relier chaque règle à un contrôle vérifiable, une preuve et un responsable.  
> Dépend de : QUALITY_GATES.md, SECURITY.md  
> Ne doit jamais contenir : procédures opérationnelles détaillées.

---

## Matrice de contrôle

| ID | Contrôle | Risque couvert | Fichier de référence | Preuve attendue | Fréquence | Responsable | Auto/Manuel | Statut |
|----|---------|--------------|---------------------|----------------|-----------|-------------|------------|--------|
| C-01 | Secret scan sur chaque commit | Fuite de credentials | SECRETS.md | Rapport git-secrets propre | Chaque commit | CI | Auto | ⚠️ Documenté (pipeline CI non déployé) |
| C-02 | SAST sur chaque PR | Injection, vulnérabilités code | APPSEC.md | Rapport Semgrep 0 HIGH/CRIT | Chaque PR | CI | Auto | ⚠️ Documenté (pipeline CI non déployé) |
| C-03 | Dependency audit | Dépendances vulnérables | SUPPLY_CHAIN.md | Rapport npm audit propre | Chaque PR | CI | Auto | ⚠️ Documenté (pipeline CI non déployé) |
| C-04 | Tests unitaires + coverage | Régression, non-qualité | QA.md | Rapport JUnit + coverage ≥ 80% | Chaque PR | CI | Auto | ⚠️ Documenté (pipeline CI non déployé) |
| C-05 | Tests E2E sur main | Régression parcours critiques | QA.md | Rapport Playwright | Chaque merge main | CI | Auto | ⏳ À configurer |
| C-06 | Lint et type-check | Non-conformité standards | STANDARDS.md | Log lint propre | Chaque PR | CI | Auto | ⚠️ Documenté (pipeline CI non déployé) |
| C-07 | Revue humaine PR | Décision non maîtrisée | ENGINEERING_HANDBOOK.md | Approbation PR | Chaque PR | Tech Lead | Manuel | ✓ Actif |
| C-08 | Validation Gate 7 avant release | Release non autorisée | QUALITY_GATES.md | Sign-off humain tracé | Chaque release | CTO/TL | Manuel | ✓ Actif |
| C-09 | ADR avant décision structurante | Décision non tracée | DECISIONS.md | ADR dans docs/adr/ | Sur événement | Architect | Manuel | ✓ Actif |
| C-10 | CHANGELOG.md à jour | Historique incomplet | CHANGELOG.md | Diff présent dans PR | Chaque livrable | Agent docs | Auto+Manuel | ✓ Actif |
| C-11 | Audit accès trimestriel | Accès non révoqués | ACCESS_CONTROL.md | Rapport revue accès | Trimestriel | Sécurité | Manuel | ⏳ À planifier |
| C-12 | Revue AGENTS.md | Dérive permissions agents | AGENTS.md | Compte rendu revue | Mensuel | Tech Lead | Manuel | ⏳ À planifier |
| C-13 | Scan prompt injection | Manipulation agent | PROMPT_GOVERNANCE.md | Log détection | Chaque session agent | Agent security | Auto | ⏳ À configurer |
| C-14 | Eval agents sur jeu de test | Dégradation qualité IA | EVALS.md | Score eval ≥ seuil | Chaque changement prompt | Agent QA | Auto | ⏳ À configurer |
| C-15 | Accessibilité WCAG | Non-conformité légale | STANDARDS.md | Rapport axe-core | Chaque PR UI | CI | Auto | ⏳ À configurer |
| C-16 | Revue exceptions EXCEPTIONS.md | Exception permanente non gérée | EXCEPTIONS.md | Liste exceptions expirées traitées | Mensuel | Tech Lead | Manuel | ⏳ À planifier |
| C-17 | Container image scan | Image vulnérable en prod | SUPPLY_CHAIN.md | Rapport Trivy propre | Chaque build image | CI | Auto | ⏳ Si applicable |
| C-18 | Rotation secrets | Secret compromis ancienneté | SECRETS.md | Log rotation | Semestriel | Platform Eng | Manuel | ⏳ À planifier |

---

## Légende statut

| Statut | Signification |
|--------|--------------|
| ✓ Actif | Contrôle en place et opérationnel |
| ⚠️ Documenté (pipeline CI non déployé) | Défini et prêt à déployer — pipeline CI non encore activé |
| ⏳ À configurer | Défini, pas encore implémenté |
| ⏳ À planifier | Planifié, pas encore schedulé |
| ⏳ Si applicable | Dépend du contexte (stack, infra) |
| ✗ Désactivé | Désactivé avec justification dans EXCEPTIONS.md |

---

## Contrôles bloquants (ne peuvent pas être ignorés)

- C-01 (secrets), C-02 (SAST), C-03 (audit), C-04 (tests), C-08 (Gate 7) sont bloquants en CI
- Tout résultat rouge bloque le merge
- Exception uniquement via EXCEPTIONS.md validé par humain

> **Note :** C-01, C-02, C-03, C-04, C-06 sont en statut ⚠️ (documentés, pipeline non déployé) jusqu'à la mise en place du CI GitHub Actions (Sprint 1). Exécution manuelle requise en attendant — voir EXCEPTIONS.md.
