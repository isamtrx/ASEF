# core/ — Frameworks transverses ASEF-Core

Ce répertoire contient les **10 frameworks transverses** qui forment le socle
commun de toute instance ASEF.

Aucun framework vertical (ASEF-Domain) ne doit réimplémenter ce que core/ définit.

## Contenu

| Fichier | Rôle |
|---|---|
| `ASEF-Core.md` | Orchestration, primitives, règles de base |
| `ASEF-AgentGov.md` | Gouvernance des agents, rôles, permissions |
| `ASEF-Evidence.md` | Preuves, captures, rapports, traçabilité |
| `ASEF-Decision.md` | Décisions, ADR, go/no-go, exceptions |
| `ASEF-Memory.md` | Mémoire, historique, apprentissage |
| `ASEF-Workflow.md` | Chaînes opérationnelles, statuts, dépendances |
| `ASEF-Gates.md` | Quality gates universels G0-G9 |
| `ASEF-Risk.md` | Risques, scoring, mitigation |
| `ASEF-Audit.md` | Journalisation, conformité, relecture externe |
| `ASEF-HITL.md` | Human-in-the-loop, validations humaines |

## Règle d'héritage

Un framework vertical hérite de core/ via la déclaration dans son `PURPOSE.md` :

```markdown
## Héritage ASEF-Core
Ce framework hérite des frameworks core suivants :
- ASEF-Core (orchestration, primitives)
- ASEF-Evidence (preuves)
- ASEF-Gates (gates G0-G9)
- ASEF-Decision (décisions)
- ASEF-Memory (mémoire)
- ASEF-HITL (validations humaines)
```

Tout écart avec core/ doit être documenté dans un ADR.
