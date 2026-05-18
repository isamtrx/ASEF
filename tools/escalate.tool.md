# tool: escalate

**id**: escalate
**level**: EXECUTE_SAFE
**implementation**: asef/tools.py

## Description

Déclencher une escalade humaine. Arrête le pipeline et documente le problème.

## Input

```json
{
  "tool": "escalate",
  "reason": "<string — raison explicite>",
  "recommendation": "<string — action recommandée pour l'humain>",
  "evidence": "<string — preuve: output d'outil, chemin fichier, phrase suspecte>",
  "urgency": "CRITIQUE|OBLIGATOIRE|RECOMMANDÉE"
}
```

## Output

```json
{
  "escalation_id": "ESC-<8hex>",
  "timestamp": "<ISO8601>",
  "logged_to": "SESSION_LOG.md",
  "pipeline_status": "HALTED"
}
```

## Effets

1. Pipeline arrêté immédiatement
2. Entrée écrite dans SESSION_LOG.md :
   ```
   ## ESCALADE ESC-<id> — <timestamp>
   - Urgence : <urgency>
   - Raison : <reason>
   - Evidence : <evidence>
   - Recommandation : <recommendation>
   ```
3. Si urgency = CRITIQUE → entrée additionnelle dans LESSONS_LEARNED.md

## Rules

- Tout agent peut appeler escalate
- Ne jamais bloquer l'outil escalate (pas de filtre sur cet outil)
- Après escalade, NE PAS reprendre sans réponse humaine explicite
- Ne pas simuler une réponse humaine
