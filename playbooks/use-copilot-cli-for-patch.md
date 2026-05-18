# Playbook : Appliquer un patch avec GitHub Copilot CLI

> Applicable aux opérations de patch précis sur du code ou de la configuration.
> Version 1.0 · 2026-05-18

---

## Quand utiliser ce playbook

- Patch de sécurité sur une dépendance.
- Correction ciblée d'un bug identifié (Gate G3 FAIL).
- Modification d'une configuration sans refactoring.
- Mise à jour d'un fichier de configuration suite à un DECISIONS.md.

---

## Principes directeurs (Karpathy — règle chirurgicale)

```
1. Lire le fichier ENTIER avant de modifier une seule ligne
2. Toucher UNIQUEMENT ce qui est demandé
3. Chaque ligne modifiée doit tracer vers le gate ou la décision source
4. Ne pas refactorer pendant le patch
5. Ne pas ajouter de fonctionnalités pendant le patch
```

---

## Step 1 — Cadrage du patch

Avant tout :

```markdown
**Fichier cible** : [chemin exact]
**Ligne(s) concernée(s)** : [numéros de lignes]
**Raison** : [Gate X FAIL — raison / CVE / DECISIONS.md référence]
**Périmètre exact** : [Ce qui change, ce qui ne change pas]
**Test de validation** : [Comment vérifier que le patch est correct]
```

---

## Step 2 — Lecture du fichier

```bash
# Lire le fichier avant tout patch
cat [fichier] | head -100   # aperçu
# ou via outils IDE
```

Vérifier :
- Le contexte des lignes à modifier (lignes avant/après).
- Les dépendances (qui importe ce fichier, qui appelle cette fonction).
- Le style de code existant (indentation, nommage, patterns).

---

## Step 3 — Appliquer le patch

Via Copilot CLI ou outil éditeur :

**Règle** : passer un contexte suffisant (≥ 3 lignes avant et après la modification).

```bash
# Exemple avec git apply (patch fichier)
git diff > /tmp/patch.diff
# Vérifier le diff avant d'appliquer
cat /tmp/patch.diff
git apply /tmp/patch.diff
```

Pour les patches inline via Copilot :
- Fournir le contexte : "Modifier uniquement la ligne X de [fichier] : [ancien code] → [nouveau code]"
- Ne jamais demander "améliore ce fichier" pendant un patch ciblé.

---

## Step 4 — Valider le patch

```bash
# Test de non-régression
[commande test appropriée]

# Vérifier que seul ce qui devait changer a changé
git diff [fichier]
```

Checklist :
```
□ Seules les lignes prévues ont changé
□ Tests passent (si applicable)
□ Linting/type checking passe
□ Aucun secret introduit
□ Gate source maintenant PASS
```

---

## Step 5 — Documenter

1. Ajouter dans CHANGELOG.md :
```markdown
### Fixed
- [YYYY-MM-DD] [fichier] : [description du patch] (Gate G[X] FAIL → PASS)
```

2. Mettre à jour DECISIONS.md si le patch répond à une décision :
```markdown
**Appliqué le** : YYYY-MM-DD — [fichier] ligne [X] modifié
```

3. Ajouter dans SESSION_LOG.md.

---

## Pièges à éviter

| Piège | Conséquence | Règle |
|---|---|---|
| Patch sans lire le fichier | Contexte manquant, casse le code adjacent | Toujours lire avant |
| Patch sur fichier de gouvernance sans validation | Violation AGENTS.md §7 | HITL obligatoire |
| Patch qui refactore "en passant" | Scope creep, non traçable | 1 patch = 1 raison |
| Patch déclaré sans test d'exécution | Gate G4 invalide | Exécuter les tests réellement |
