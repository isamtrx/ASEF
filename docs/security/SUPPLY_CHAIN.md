# SUPPLY_CHAIN.md — ASEF

> Source de vérité de la sécurité de la chaîne d'approvisionnement logicielle.  
> 1 responsabilité : définir les règles pour ajouter, auditer et contrôler les dépendances.  
> Dépend de : SECURITY.md, OPEN_SOURCE_POLICY.md  
> Ne doit jamais contenir : politique de licences (→ OPEN_SOURCE_POLICY.md).

---

## Principe

Toute dépendance externe est une surface d'attaque potentielle. Elle doit être choisie délibérément, auditée régulièrement et validée avant intégration.

---

## Ajout d'une nouvelle dépendance

**Processus obligatoire :**

1. Vérifier qu'une dépendance existante ne couvre pas déjà le besoin
2. Vérifier la licence (→ OPEN_SOURCE_POLICY.md)
3. Vérifier l'activité du mainteneur (dernier commit < 1 an)
4. Vérifier l'historique de vulnérabilités CVE
5. Lancer un audit initial

```bash
# npm
npm install [package] && npm audit

# pip
pip install [package] && pip-audit

# Go
go get [module] && govulncheck ./...
```

6. Ouvrir un ticket tracé dans le backlog

**Dépendance non auditée = dépendance non autorisée.**

---

## Audit continu des dépendances

**Fréquence :** Chaque PR (CI automatique)  
**Outil :** npm audit · pip-audit · Trivy (containers) · govulncheck (Go)  
**Seuil bloquant :** 0 vulnérabilité HIGH ou CRITICAL

```bash
# npm
npm audit --audit-level=high --json > reports/audit.json

# pip
pip-audit --output=json > reports/audit.json

# Container
trivy image [image:tag] --severity HIGH,CRITICAL --format json > reports/trivy.json
```

---

## Règles de gestion des vulnérabilités

| Sévérité | Action | Délai |
|----------|--------|-------|
| CRITICAL | Mise à jour ou suppression immédiate | 24h |
| HIGH | Mise à jour dans le sprint en cours | 72h |
| MEDIUM | Planifier mise à jour | 2 semaines |
| LOW | Backlog | 1 mois |

**Dépendance sans fix disponible :**
- Ouvrir une exception dans EXCEPTIONS.md (maximum 7 jours)
- Documenter le risque accepté
- Surveiller la publication d'un fix

---

## SBOM — Software Bill of Materials

Le SBOM documente toutes les dépendances directes et transitives du projet.

```bash
# Générer un SBOM (format SPDX)
npm run sbom          # si configuré
cyclonedx-py poetry --output-format json > sbom.json   # Python
```

Le SBOM est archivé à chaque release dans les artifacts CI.

---

## Règles pour les images Docker

- Utiliser uniquement des images officielles ou vérifiées (Docker Hub Verified Publisher)
- Images basées sur Alpine ou Distroless en priorité (surface minimale)
- Scanner l'image avec Trivy avant le push
- Ne jamais utiliser le tag `:latest` en production — toujours pinning par digest SHA256

```dockerfile
# Correct
FROM node:20.12.0-alpine3.19@sha256:[digest]

# Interdit
FROM node:latest
```

---

## Règles pour les GitHub Actions

- Utiliser des actions maintenues par GitHub (`actions/`) ou des actions auditées
- Pinning par commit SHA sur les actions tierces (pas de tag flottant)
- Pas de `run: curl | bash` dans les workflows

```yaml
# Correct
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

# Interdit
- uses: actions/checkout@v4
```

---

## Provenance des artifacts

Chaque artifact de release ASEF doit avoir :
- Un commit Git identifiable (SHA)
- Un pipeline CI traçable (lien GitHub Actions run)
- Un SBOM associé (archivé en artifact CI)
