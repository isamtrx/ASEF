# skill: repo_audit

**id**: repo_audit
**version**: 1.0.0
**agents**: orchestrator, qa
**tools_required**: read_file, list_directory, run_command

## Purpose

Effectuer un audit complet du repo : structure, fichiers manquants, cohérence
des registres, état des gates.

## When to Use

- task_type = `audit`
- Bootstrap initial (vérifier que AGENTS.md, SCOPE.md, MEMORY.md sont présents)
- Avant une release (vérifier cohérence globale)

## Steps

1. Lister la structure du repo (`list_directory` récursif)
2. Vérifier la présence des fichiers obligatoires :
   - `AGENTS.md`, `SCOPE.md`, `MEMORY.md`, `DECISIONS.md`
   - `directives/00_MASTER.md`
   - `registry/agents.registry.json`, `registry/skills.registry.json`
3. Vérifier la cohérence des registres :
   - Chaque agent dans `registry/agents.registry.json` a un fichier `agents/*.agent.md`
   - Chaque skill dans `registry/skills.registry.json` a un fichier `skills/*.skill.md`
4. Vérifier les gates :
   - `ruff check .` → noter le résultat
   - `pytest -q tests/` → noter le résultat (optionnel si pas de changement)
5. Produire un rapport dans `artifacts/audits/<YYYY-MM-DD>_audit.md`

## Output Format

```markdown
# Audit Report — <YYYY-MM-DD>

## Files
- [x] AGENTS.md présent
- [x] SCOPE.md présent
- ...

## Registry
- [x] Tous agents ont un fichier .agent.md
- ...

## Gates
- G3: <passed|failed>
- G4: <passed|failed|skipped>

## Missing
- <liste des fichiers manquants>

## Recommendation
<ready_to_proceed|needs_fix>
```

## Edge Cases

- Si MEMORY.md absent → escalade (fichier critique)
- Si AGENTS.md absent → escalade CRITIQUE (constitution absente)
- Si registres absents → noter comme gap, ne pas bloquer

## Errors

- `list_directory` échoue → escalade
- Fichiers protégés non lisibles → noter, ne pas forcer l'accès
