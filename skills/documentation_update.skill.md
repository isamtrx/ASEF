# skill: documentation_update

**id**: documentation_update
**version**: 1.0.0
**agents**: docs
**tools_required**: read_file, write_file

## Purpose

Mettre à jour CHANGELOG.md, SESSION_LOG.md, README.md et produire l'evidence package (G6).

## When to Use

- Après tout changement livrable (bugfix, feature, release)
- Gate G6 (avant release)

## Steps

### 1. CHANGELOG.md

1. Lire CHANGELOG.md entier
2. Identifier la section `## [Unreleased]`
3. Ajouter sous la section appropriée (Added/Changed/Fixed/Security/Deprecated/Removed) :
   ```markdown
   ### <Category>
   - <Description de la modification> (#<task_id>)
   ```
4. Format Keep a Changelog (https://keepachangelog.com)

### 2. SESSION_LOG.md

Suivre le format de `skills/memory_update.skill.md`.

### 3. Evidence Package (G6)

Vérifier et collecter :
- [ ] G3 rapport : `ruff check .` exit 0
- [ ] G4 rapport : `pytest -q tests/` exit 0
- [ ] G5 rapport : `artifacts/security/<date>_<id>_security.md`
- [ ] CHANGELOG.md mis à jour
- [ ] SESSION_LOG.md mis à jour
- [ ] Aucun secret dans les fichiers modifiés

Produire : `artifacts/reports/<YYYY-MM-DD>_<task_id>_evidence.md`

```markdown
# Evidence Package — <date> — <task_id>

## Gates
- G3 (lint): PASS — exit 0
- G4 (tests): PASS — <n> tests, 0 failures
- G5 (security): PASS — 0 leaks, 0 CVE high+

## Documents
- CHANGELOG.md: mis à jour le <date>
- SESSION_LOG.md: mis à jour le <date>

## Files Modified
<liste>

## Verdict
<ready_for_g7|incomplete>
```

## Rules

1. Ne jamais déclarer G6 complet sans tous les éléments checklist
2. Ne jamais modifier AGENTS.md ou SCOPE.md dans ce skill
3. CHANGELOG.md doit avoir une section Unreleased avant d'ajouter des entrées
4. Evidence package est READ_ONLY après création

## Edge Cases

- CHANGELOG.md sans section Unreleased → créer la section
- G5 rapport absent → G6 INCOMPLET, escalader
