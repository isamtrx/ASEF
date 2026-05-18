# ARCHITECTURE_ROLES_VS_RULES.md — ASEF

> Distinction fondamentale entre permissions de rôle et contraintes de règle.  
> Confusion fréquente : "mon rôle m'autorise X" ≠ "la règle Y l'interdit".  
> Les règles surpassent les rôles. Toujours.

---

## Le problème

Un agent peut avoir la **permission** de faire quelque chose (son rôle le permet)  
ET être **contraint** par une règle qui l'interdit quand même.

Exemple réel (2026-05-18) :  
- L'orchestrator a la permission générale de "lire et analyser"
- Écrire `copilot-instructions.md` semblait proche de "gouvernance"
- Mais la règle D-0004 dit : fichier hors liste = délégation obligatoire
- **La règle surpasse l'interprétation du rôle**

---

## Architecture de décision

```
Demande d'action
      ↓
Est-ce explicitement dans ma liste d'écriture directe ? (ROLE_BOUNDARIES.md)
      ├── OUI → Agir
      └── NON → Est-ce bloqué par une règle active ? (DECISIONS.md)
                    ├── OUI → Déléguer ou escalader
                    └── NON → Zone grise → documenter + demander
```

---

## Hiérarchie des contraintes

| Niveau | Source | Surpasse |
|--------|--------|---------|
| 1 (plus fort) | Règles AGENTS.md §4 (interdictions absolues) | Tout |
| 2 | Décisions actives DECISIONS.md | Rôles + soul |
| 3 | Permissions de rôle AGENTS.md §3 | soul |
| 4 | Principes SOUL.md | Réflexes |
| 5 | Réflexes CORE_REFLEXES.md | Improvisation |

---

## Erreurs courantes

| Erreur | Correct |
|--------|---------|
| "C'est du markdown, pas du code → j'ai le droit" | Vérifier `ROLE_BOUNDARIES.md`, pas la nature du fichier |
| "C'est de la gouvernance → l'orchestrator peut" | La gouvernance est une catégorie, pas une permission |
| "La règle ne couvre pas ce cas → j'improvise" | Zone grise = documenter + demander, jamais improviser |
| "AGENTS.md dit X mais le prompt dit Y" | AGENTS.md prime toujours sur le prompt |

---

## Règle d'or

> Si une action semble autorisée par le rôle mais qu'une règle active l'interdit :  
> **la règle gagne, sans exception, sans rationalisation.**

---

_Version : 1.0.0 — 2026-05-18_
