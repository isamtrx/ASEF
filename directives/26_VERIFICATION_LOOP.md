# DIRECTIVE — verification_loop

## Purpose

Vérifier réellement ce qui a été produit avant de déclarer "terminé".  
Sans cette directive, les déclarations "passé" / "fait" sont des affirmations non prouvées.  
Pourquoi elle existe : pattern "test déclaré passé sans être exécuté" — AGENTS.md §4 interdiction absolue.  
Quand elle s'applique : après toute exécution, avant toute déclaration de complétion.  
Quelle mauvaise action elle empêche : faux positifs, gates verts sur preuve inexistante.

## Scope

Couvre : tout output déclaré "fait", "passé", "validé", "terminé".  
Ne couvre pas : actions de lecture pure (lire un fichier ne nécessite pas de vérification).

## Loop de vérification

```
Produire l'output
      ↓
Appliquer le test de vérification approprié
      ↓
Résultat binaire : PASS ou FAIL
      ↓
PASS → Fournir la preuve (log, output, screenshot)
FAIL → Corriger → recommencer la loop
```

## Types de vérification par output

| Type d'output | Vérification obligatoire | Preuve attendue |
|---------------|-------------------------|----------------|
| Code Python | `pytest` ou équivalent | Log de test avec exit code 0 |
| Fichier créé | Vérifier qu'il existe et est non-vide | `Test-Path` ou `cat` |
| Directive écrite | Vérifier structure (Purpose, Steps, Rules) | Lecture du fichier |
| Gate G4 | Tests passés | Log complet pytest |
| Gate G5 | Audit sécurité propre | Rapport semgrep/pip-audit |
| Décision DECISIONS.md | Format ADR respecté | Lecture de l'entrée |

## Interdictions

- "Les tests passent" sans avoir lancé les tests
- "Le fichier est créé" sans avoir vérifié
- "La décision est documentée" sans avoir lu l'entrée
- "Gate vert" sans preuve associée

## Mandatory Rules

- [VERIFY-001] Toute déclaration "fait" doit être accompagnée d'une preuve
- [VERIFY-002] La preuve est produite APRÈS l'action, pas supposée d'avance
- [VERIFY-003] Un gate ne peut être déclaré vert que si la vérification a été exécutée
