# MEMORY.md — ASEF

> Mémoire active courante du projet.  
> 1 responsabilité : état présent, décisions stabilisées, contexte actif.  
> Ce fichier N'EST PAS : un changelog, un backlog, un journal de session.  
> Purge mensuelle obligatoire. Seuil : 200 lignes maximum.

---

## Contexte actif

| Champ | Valeur |
|-------|--------|
| Phase | Sprint 1 — Opérationnalisation |
| Statut | Framework P0→P4 complet (CI non déployé) |
| Date dernier état | 2026-05-19 |
| Prochaine action prioritaire | Déployer `.github/workflows/ci.yml` + synchroniser `registry/skills.registry.json` |

## Décisions stabilisées

| Décision | Raison | Référence |
|----------|--------|-----------|
| 1 fichier = 1 responsabilité | Principe fondateur anti-dette documentaire | PROJECT.md |
| AGENTS.md = source de vérité agents | Outil-agnostique, prime sur CLAUDE.md et copilot-instructions | AGENTS.md |
| Quality gates bloquants G4+G5 | Sécurité et tests non négociables | QUALITY_GATES.md |
| Human-in-the-loop sur Gate 7 | Release critique = validation humaine obligatoire | AGENTS.md |
| Stack MVP : VS Code + Copilot + Claude Code + GitHub | Définie dans PROJECT.md | PROJECT.md |
| D-0004 : orchestrator write-list = 4 fichiers | Contrainte stricte d'écriture, exception humaine requise | DECISIONS.md |

## Hypothèses actives

- L'organisation utilise GitHub comme plateforme principale
- Les agents disposent d'accès aux fichiers du dépôt en lecture/écriture
- Les pipelines CI/CD sont configurés sur GitHub Actions
- Aucune donnée client sensible ne transite dans le dépôt

## État actuel des fichiers critiques

| Fichier | Statut | Dernière action |
|---------|--------|----------------|
| AGENTS.md | ✓ Opérationnel | Initialisation MVP |
| SCOPE.md | ✓ Opérationnel | Initialisation MVP |
| PROJECT.md | ✓ Opérationnel | Initialisation MVP |
| CLAUDE.md | ✓ Opérationnel | Mis à jour (7 étapes bootstrap) |
| docs/ARCHITECTURE.md | ✓ Opérationnel | Créé en session |
| docs/quality/QUALITY_GATES.md | ✓ Opérationnel | G0-G7 complets |
| docs/security/SECURITY.md | ✓ Opérationnel | Doctrine + obligations |
| docs/ai/AGENT_REGISTRY.md | ✓ Opérationnel | 5 agents documentés |
| docs/delivery/CI_CD.md | ✓ Documenté (pipeline non déployé) | Pipelines CI + release |
| PRODUCT.md | ✓ Opérationnel | 3 personas + JTBD |
| ROADMAP.md | ✓ Opérationnel | 4 phases définies |
| memory/audits/ | ✓ Disponible | Dossier pour les rapports d'audit |
| GLOSSARY.md | ✓ Créé | Termes du framework |
| QUICKSTART.md | ✓ Créé | Onboarding J1 humain |

**Total : fichiers gouvernance core + instructions domaine (.github/) + adaptateur CLAUDE.md + ADRs + prompts.**

## Liens vers logs détaillés

- Décisions : [DECISIONS.md](DECISIONS.md)
- Historique : [CHANGELOG.md](CHANGELOG.md)
- Sessions : [SESSION_LOG.md](SESSION_LOG.md)
- Tâches : [BACKLOG.md](BACKLOG.md)
