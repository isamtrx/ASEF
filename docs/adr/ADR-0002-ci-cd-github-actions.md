# ADR-0002 — GitHub Actions comme toolchain CI/CD

Date : 2026-05-15  
Statut : Validé  
Auteur : Platform Engineering

---

## Contexte

ASEF définit un pipeline de livraison avec 8 quality gates (G0–G7) qui doivent être exécutés automatiquement sur chaque changement. Un outil de CI/CD doit être choisi pour héberger ces pipelines.

Les contraintes sont :
- Dépôt hébergé sur GitHub
- Pipeline docs-first : lint Markdown, secret scan, SAST (Semgrep), et à terme tests et builds
- Équipe petite, peu de budget infra
- Intégration native avec GitHub Secrets et GitHub Environments (gates G5, G7)

---

## Options considérées

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **GitHub Actions** | Natif GitHub, marketplace riche, gratuit pour repos publics, secrets intégrés | Vendor lock-in GitHub |
| GitLab CI | Puissant, self-hosted possible | Requiert migration vers GitLab |
| Jenkins | Très flexible, self-hosted | Infra à maintenir, overhead |
| CircleCI | Rapide, bon DX | Coût, 3rd party |

---

## Décision

**GitHub Actions** est retenu comme toolchain CI/CD principale d'ASEF.

---

## Raison

- Le dépôt est sur GitHub : pas de friction réseau ou d'authentification supplémentaire
- GitHub Secrets permet de gérer les tokens CI sans les exposer (Gate G5)
- GitHub Environments permet d'implémenter le Gate G7 (validation humaine avant déploiement)
- Le marketplace Actions contient des actions officielles pour Semgrep, `git-secrets`, `npm audit`
- Coût nul pour les projets open-source

---

## Conséquences

**Positives :**
- Pipelines définis en YAML dans `.github/workflows/`
- Intégration native des status checks sur les PRs
- Secrets gérés sans configuration externe

**Négatives :**
- Dépendance à la plateforme GitHub
- En cas de migration vers GitLab/Bitbucket, les workflows sont à réécrire

---

## Réversibilité

Réversible — les workflows GitHub Actions peuvent être récrits pour d'autres plateformes (syntaxe différente, logique identique).

---

## Fichiers concernés

- `docs/delivery/CI_CD.md` — définition du pipeline
- `docs/quality/QUALITY_GATES.md` — gates à implémenter
- `docs/security/SECURITY.md` — contrôles de sécurité CI
