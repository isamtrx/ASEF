# OBSERVABILITY.md — ASEF

> Source de vérité de l'observabilité du système.  
> 1 responsabilité : définir les logs, métriques, traces, alertes et la piste d'audit des agents.  
> Dépend de : ARCHITECTURE.md, SLO.md  
> Ne doit jamais contenir : seuils SLO (→ SLO.md), procédures d'incident (→ INCIDENT_RESPONSE.md).

---

## Principe

Tout comportement observable — technique ou agentique — doit être traçable. L'observabilité est non-négociable pour un système d'ingénierie assisté par IA.

---

## Logs structurés

### Format obligatoire (JSON)

```json
{
  "timestamp": "2026-05-15T14:23:01.123Z",
  "level": "INFO | WARN | ERROR | DEBUG",
  "service": "nom-du-service",
  "trace_id": "uuid-v4",
  "span_id": "uuid-v4",
  "event": "description.courte.de.l.evenement",
  "data": { "clés": "valeurs contextuelles" },
  "duration_ms": 42
}
```

### Niveaux de log

| Niveau | Usage |
|--------|-------|
| DEBUG | Développement uniquement — jamais en production |
| INFO | Événements normaux (requête reçue, action agent, step CI) |
| WARN | Situation anormale mais récupérée (retry réussi, dégradation) |
| ERROR | Erreur impactant une requête ou action (sans crash) |
| FATAL | Crash ou erreur système non récupérée |

### Règles

- Jamais de données personnelles dans les logs (PII)
- Jamais de secrets dans les logs
- Chaque requête HTTP a un `trace_id` propagé de bout en bout
- Les logs d'actions agent incluent `agent_id`, `prompt_id`, `input_hash` (pas l'input brut)

---

## Métriques techniques

| Métrique | Type | Description |
|---------|------|-------------|
| `http_requests_total` | Counter | Nombre total de requêtes par endpoint + status |
| `http_request_duration_ms` | Histogram | Latence p50, p95, p99 |
| `http_error_rate` | Gauge | Taux d'erreurs 4xx + 5xx |
| `db_query_duration_ms` | Histogram | Durée des requêtes base de données |
| `build_duration_seconds` | Gauge | Durée du build CI |
| `test_pass_rate` | Gauge | Taux de réussite des tests |

---

## Métriques agentiques (piste d'audit IA)

| Métrique | Type | Description |
|---------|------|-------------|
| `agent_actions_total` | Counter | Actions par agent + type + résultat |
| `agent_action_duration_ms` | Histogram | Durée des actions agent |
| `agent_hitl_required_total` | Counter | Nombre de fois où HITL a été déclenché |
| `agent_hitl_overridden_total` | Counter | Nombre de fois où un humain a annulé une décision agent |
| `prompt_eval_score` | Gauge | Score des evals par prompt + version |
| `agent_error_rate` | Gauge | Taux d'erreurs par agent |

---

## Traces distribuées

Format : OpenTelemetry (OTLP)

Chaque action agent crée un span avec :
- `agent.id` : identifiant de l'agent
- `agent.prompt_id` : version du prompt utilisé
- `agent.action.type` : lecture / écriture / exécution / décision
- `agent.action.target` : fichier ou service ciblé
- `agent.hitl` : `true | false` (validation humaine requise ?)

---

## Alertes

| Alerte | Condition | Sévérité | Action |
|--------|---------|---------|--------|
| Error rate élevé | > 5% sur 5 min | WARNING | Vérifier logs |
| Error rate critique | > 15% sur 5 min | CRITICAL | Incident P2 |
| Latence dégradée | p95 > 2s sur 10 min | WARNING | Investigation |
| Build cassé | CI rouge > 30 min | WARNING | Assign + fix |
| Secret détecté | Scan positif | CRITICAL | Incident P1 |
| Agent HITL bloqué | > 2h sans validation | WARNING | Notifier Tech Lead |
| Eval régresse | Score < seuil - 5% | WARNING | Bloquer merge |

---

## Dashboards

| Dashboard | Contenu | Audience |
|---------|---------|---------|
| Operations | Santé globale, SLO, error rates, latence | Tous |
| CI/CD | Build success rate, durée, déploiements | Developer, DevOps |
| Security | SAST findings, vulnérabilités, secret scans | Security |
| Agent Activity | Actions par agent, HITL rate, eval scores | Tech Lead, Product |

---

## Piste d'audit des actions agent

Toute action d'un agent est journalisée dans un audit log immuable :

```json
{
  "timestamp": "2026-05-15T14:23:01.123Z",
  "session_id": "uuid-v4",
  "agent_id": "AGENT-001",
  "prompt_id": "PROMPT-001",
  "prompt_version": "1.0.0",
  "action_type": "write_file",
  "target": "src/feature/auth.ts",
  "triggered_by": "user | ci | schedule",
  "hitl_required": false,
  "hitl_validated_by": null,
  "outcome": "success | failure | refused"
}
```

L'audit log est append-only, conservé 1 an, non modifiable par les agents.
