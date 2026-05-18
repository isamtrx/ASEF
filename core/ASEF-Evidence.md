# ASEF-Evidence — Preuves, traçabilité et evidence packages

> Framework transverse · Version 1.0 · 2026-05-18
> Dépendance : ASEF-Core

---

## 1. Principe

**Rien n'est terminé sans preuve.**

Une preuve est un artifact vérifiable produit lors de l'exécution.
Elle ne peut pas être créée après coup. Elle ne peut pas être approximée.
EvidenceAgent est responsable de leur collecte, structuration et archivage.

---

## 2. Taxonomie des preuves

| Type | Description | Exemples |
|---|---|---|
| `LOG` | Journal d'exécution brut | Logs CI/CD, output terminal, traces d'exécution |
| `REPORT` | Rapport structuré produit par un outil ou agent | Rapport SAST, rapport test, rapport audit |
| `CAPTURE` | Capture d'état visuel ou d'interface | Screenshot, capture navigateur, PDF |
| `ATTESTATION` | Déclaration formelle signée ou horodatée | Validation humaine, approbation, sign-off |
| `METRIC` | Valeur mesurée quantifiable | Coverage %, score sécurité, latence P95 |
| `DIFF` | Trace de modification | Git diff, comparaison avant/après |
| `ARTIFACT` | Fichier produit livrable | Binary, package, rapport final |

---

## 3. Structure d'un evidence package

Chaque livrable produit un evidence package dans :
```
docs/evidence/YYYY-MM-DD_[slug]/
├── INDEX.md          ← Catalogue des preuves (OBLIGATOIRE)
├── gates/            ← Résultats de chaque gate
│   ├── G0-intake.md
│   ├── G1-scope.md
│   └── ...
├── logs/             ← Logs bruts (LOG)
├── reports/          ← Rapports structurés (REPORT)
├── captures/         ← Screenshots et captures (CAPTURE)
├── metrics/          ← Données mesurées (METRIC)
└── artifacts/        ← Fichiers livrables (ARTIFACT)
```

---

## 4. INDEX.md — Format obligatoire

```markdown
# Evidence Package — [Nom du livrable]
Date : YYYY-MM-DD
Tâche : [Description 1 ligne]
Statut : COMPLET | PARTIEL (raison)

## Gates

| Gate | Statut | Preuve |
|---|---|---|
| G0 | PASS | gates/G0-intake.md |
| G1 | PASS | gates/G1-scope.md |
| G2 | PASS | gates/G2-risks.md |
| ... | ... | ... |

## Preuves collectées

| Fichier | Type | Description |
|---|---|---|
| logs/ci-run-12345.txt | LOG | Output CI pipeline |
| reports/sast-report.json | REPORT | Rapport SAST semgrep |
| captures/browser-test.png | CAPTURE | Screenshot test E2E |
| metrics/coverage.txt | METRIC | Coverage 87.3% |

## Anomalies et écarts
[Liste des déviations du workflow, ou "Aucune"]

## Validation humaine
[Nom, date, décision — ou "N/A"]
```

---

## 5. Règles EvidenceAgent

1. **Créer le dossier evidence AVANT l'exécution.** G5 vérifie que le dossier existe.
2. **Collecter en temps réel.** Jamais rétroactivement.
3. **Jamais inventer une preuve.** Une preuve manquante = BLOCKED, pas une approximation.
4. **Horodater toutes les preuves.** Un log sans timestamp est incomplet.
5. **INDEX.md est obligatoire.** Sans INDEX.md, le package est invalide.
6. **AuditAgent valide avant G7.** Pas de livraison sans validation externe du package.

---

## 6. Anti-patterns interdits

| Anti-pattern | Conséquence |
|---|---|
| Créer une preuve après l'action | Violation MANIFEST G-08 — invalide |
| Décrire une preuve sans la fichier | Violation G7 |
| Screenshot sans timestamp ni contexte | Preuve incomplète |
| Log tronqué sans mention de troncature | Preuve potentiellement trompeuse |
| Valider G7 sans INDEX.md | Violation MANIFEST G-03 |
| "Tests passés" sans log de test | Violation MANIFEST G-08 — faute grave |

---

## 7. Checklist EvidenceAgent avant G7

```
□ Dossier docs/evidence/YYYY-MM-DD_slug/ créé
□ INDEX.md présent et complet
□ Tous les gates documentés dans gates/
□ Tous les logs collectés dans logs/
□ Toutes les captures archivées dans captures/
□ Toutes les métriques dans metrics/
□ Tous les artifacts dans artifacts/
□ AuditAgent a validé la cohérence
□ Aucune preuve inventée ou approximée
□ Validation humaine documentée si HITL actif
```
