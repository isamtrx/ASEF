# skill: test_generation

**id**: test_generation
**version**: 1.0.0
**agents**: developer, qa
**tools_required**: read_file, write_file, run_command

## Purpose

Générer des tests pytest conformes au style existant du repo.
Chaque modification de code doit avoir des tests correspondants.

## When to Use

- Après implémentation d'une feature ou correction d'un bug
- Quand les tests existants ne couvrent pas le code modifié
- qa identifie des gaps de couverture

## Règles

1. Les tests sont dans `tests/test_<module>.py`
2. Utiliser pytest fixtures existantes (voir `tests/conftest.py` si présent)
3. Nommer les tests : `test_<comportement_attendu>`
4. Un test par comportement, pas par ligne de code
5. Tester : le chemin nominal, les erreurs attendues, les cas limites
6. Pas de dépendances externes dans les tests (mock si nécessaire)
7. Jamais désactiver un test pour le faire passer

## Steps

1. Lire le code modifié pour comprendre les comportements
2. Lire les tests existants pour comprendre le style
3. Identifier les comportements non couverts
4. Écrire les tests manquants
5. Exécuter `pytest -q tests/test_<module>.py` → vérifier exit 0
6. Si exit ≠ 0 → corriger les tests (pas désactiver)

## Template de test

```python
def test_<comportement>():
    # Arrange
    <setup>
    # Act
    result = <appel>
    # Assert
    assert <condition>
```

## Edge Cases

- Code asynchrone → utiliser `pytest-asyncio` si installé
- Code nécessitant des credentials → mocker, jamais de vrai secret dans les tests
- Test qui échoue toujours → escalade, ne pas désactiver

## Validation

`pytest -q tests/` → exit 0 obligatoire avant de déclarer les tests prêts
