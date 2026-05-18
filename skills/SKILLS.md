# SKILLS — Index

## Purpose

Catalogue des skills disponibles dans ASEF Runtime.
Chaque skill est un document déclaratif qui décrit une capacité réutilisable.

## Index des skills

| Skill | Fichier | Agents autorisés | Description |
|---|---|---|---|
| `repo_audit` | `skills/repo_audit.skill.md` | orchestrator, qa | Audit complet du repo |
| `code_review` | `skills/code_review.skill.md` | developer, qa | Revue de code chirurgicale |
| `test_generation` | `skills/test_generation.skill.md` | developer, qa | Génération de tests pytest |
| `security_review` | `skills/security_review.skill.md` | security | G5 complet |
| `memory_update` | `skills/memory_update.skill.md` | orchestrator, docs | Mise à jour mémoire structurée |
| `documentation_update` | `skills/documentation_update.skill.md` | docs | CHANGELOG, SESSION_LOG, README |
| `bootstrap_check` | `skills/bootstrap_check.skill.md` | orchestrator | Vérification bootstrap complet de session |
| `session_close` | `skills/session_close.skill.md` | orchestrator | Fermeture propre de session (BRIEF + LOG + MEMORY) |
| `scope_check` | `skills/scope_check.skill.md` | orchestrator | Vérification périmètre IN/OUT SCOPE |
| `dod_formulation` | `skills/dod_formulation.skill.md` | orchestrator | Formulation et validation DoD avant livrable |
| `escalation_report` | `skills/escalation_report.skill.md` | orchestrator | Rapport structuré d'escalade humaine |

## Règles

1. Un skill est READ_ONLY — il ne contient que des instructions, pas du code exécutable
2. Un agent ne peut utiliser que les skills listés dans son contrat
3. Tout nouveau skill doit être ajouté à `registry/skills.registry.json`
4. Validation : `python execution/validate_skills.py`
