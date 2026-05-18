# DIRECTIVE-20 — GOVERNANCE

## Purpose

Règles de gouvernance du projet : ADR, décisions structurantes, fichiers protégés,
permissions et escalade humaine.

Pourquoi elle existe : garantir que les décisions structurantes sont documentées
avant d'être implémentées, et que les fichiers critiques ne sont pas modifiés
sans validation humaine.
Quand elle est utilisée : toute tâche qui touche l'architecture, la sécurité,
le scope, ou une décision structurante.
Quelle décision elle encadre : ce qui nécessite un ADR et ce qui bloque sans approbation humaine.
Quelle mauvaise action elle empêche : modification silencieuse de fichiers protégés,
décision structurante sans traçabilité.

## Scope

Couvre : AGENTS.md, SCOPE.md, PROJECT.md, DECISIONS.md, docs/adr/, docs/security/.
Ne couvre pas : le code applicatif (voir directive backend).

## Mandatory Rules

1. [GOV-001] Les fichiers protégés ne peuvent être modifiés sans ADR + validation humaine.
   - Why: AGENTS.md, SCOPE.md, PROJECT.md, SECURITY.md définissent le périmètre et les permissions.
   - Blocks: modification de ces fichiers sans ADR validé.
   - Evidence: ADR dans docs/adr/ référencé dans DECISIONS.md.
   - Fichiers protégés : AGENTS.md, SCOPE.md, PROJECT.md, docs/security/SECURITY.md.

2. [GOV-002] Toute décision structurante nécessite un ADR avant implémentation.
   - Why: les décisions non documentées créent des précédents invisibles.
   - Blocks: implémentation avant ADR pour décisions structurantes.
   - Evidence: fichier docs/adr/ADR-XXXX-slug.md avec statut Validé.

3. [GOV-003] La Gate G7 (release) est toujours humaine.
   - Why: aucun agent ne peut approuver une release.
   - Blocks: release automatique sans validation humaine.
   - Evidence: confirmation humaine explicite documentée.

4. [GOV-004] Toute modification du scope nécessite un ADR + validation humaine.
   - Why: SCOPE.md est la source de vérité sur le périmètre.
   - Blocks: modification de SCOPE.md sans ADR.
   - Evidence: ADR avec section Réversibilité.

5. [GOV-005] Les agents ne peuvent pas émettre d'exception à un quality gate.
   - Why: les exceptions sont toujours humaines.
   - Blocks: contournement automatique d'un gate bloquant.
   - Evidence: escalade documentée si gate rouge.

## Required Inputs

- `DECISIONS.md` — registre des décisions
- `docs/adr/` — ADR existants
- `AGENTS.md` §3 — matrice de permissions

## Required Outputs

- ADR si décision structurante
- Entrée dans DECISIONS.md pour tout ADR
- Confirmation humaine si Gate G7

## Validation Checklist

- [ ] Aucun fichier protégé modifié sans ADR
- [ ] Tout ADR dans DECISIONS.md
- [ ] Gate G7 : confirmation humaine documentée
- [ ] DECISIONS.md cohérent avec docs/adr/

## Rejection Criteria

- Modification de AGENTS.md sans ADR → BLOCKED_BY_POLICY
- Modification de SCOPE.md sans ADR → BLOCKED_BY_POLICY
- Release sans Gate G7 humain → BLOCKED_BY_APPROVAL_REQUIRED

## Related Directives

- `directives/00_MASTER.md` — master routing
- `policies/HUMAN_APPROVAL.md` — approbations humaines
- `policies/PERMISSIONS.md` — matrice de permissions

## Evidence Required

- Fichier ADR créé (docs/adr/ADR-XXXX-slug.md)
- Entrée dans DECISIONS.md
- Confirmation humaine si applicable
