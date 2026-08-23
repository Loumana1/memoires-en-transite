# Prompt IA — Finir les plans de présence Cortex (Proto 08)

Copier-coller ce prompt dans une session Agent. Spec : [`spec_cortex_plans_presence_08.md`](./spec_cortex_plans_presence_08.md).  
Contexte zone : [`../Zones/Cortex.md`](../Zones/Cortex.md) §5 bis · §9 · §10 A.

---

## Mission

Finaliser les **plans de présence** `PREMIER_PLAN` / `ARRIERE_PLAN` sur les 12 voix Cortex du Proto 08.

Ce n'est **pas** « ajouter 12 nouveaux fx_router » : ils existent déjà (un par couche). Il faut **aligner**, **dé-doubler le gain**, **clarifier les LFO**, et **permettre un forçage manuel** pour l'écoute.

**Ne pas** implémenter de vraie réverb (delay V1 seulement). **Ne pas** toucher au sélecteur C1…C11 / tableau.

---

## Contexte repo (lire avant de coder)

| Fichier | Rôle |
|---------|------|
| `scripts/proto08/proto08_lib/presets08.py` | `PLAN_PREMIER`, `PLAN_ARRIERE`, `GAIN_*`, `CORTEX_LPF_*`, `_cortex_twelve_parole()`, `bank_msg_body` |
| `scripts/proto08/proto08_lib/gen_patch08.py` | `*~` gain lecteur × plan (à corriger) · `fx_router_06 {n}` · entrée `cortex_pair_08` |
| `scripts/proto08/proto08_lib/gen_libs08.py` | `gen_cortex_ctrl_08` (LPF + swap plages) · `gen_cortex_pair_08` (gains plan + swap) · `gen_fsm_presets_08` |
| `pd/lib/fx_router_06.pd` | lit `s6_l$1_wet`, `_del`, `_fb`, `_hpf`, `_lpf`, `_sat`, … |
| `docs/Zones/Cortex.md` §5 bis | **valeurs cibles** Q10 |

Régénération : `python3 scripts/gen_prototype_08_8hp.py`  
Patch : `pd/prototype_08_fsm_8hp.pd`

---

## Architecture à respecter

```text
L1..L12 : player_state_08 → *~ CORTEX_LAYER_GAIN seulement
        → (gate EMERGER si présent)
        → fx_router_06 {n}     ← preset plan (wet/hpf/sat/delay…)
        → cortex_pair_08       ← gain plan + swap + somme paire + AM + spat
```

- Couches **impaire d'index 0-based pair** (L1, L3, …) = `PREMIER_PLAN` par défaut.
- Couches **L2, L4, …** = `ARRIERE_PLAN` par défaut.
- Paire `pr` = couches `2*pr+1` et `2*pr+2`.

Ne **pas** déplacer les FX dans `cortex_pair_08`.

---

## Travail demandé (ordre)

### Étape 1 — Corriger le double gain

Dans `gen_patch08.py`, pour `i < 12` :

- Aujourd'hui : `lg = CORTEX_LAYER_GAIN * (GAIN_PREMIER ou GAIN_ARRIERE)`.
- Cible : `lg = CORTEX_LAYER_GAIN` uniquement.

Les `GAIN_PREMIER_PLAN` / `GAIN_ARRIERE_PLAN` restent appliqués **uniquement** dans `cortex_pair_08` (déjà via `swfa` / `swba`).

Vérifier à swap=0 : niveau perçu ≈ gain couche × gain plan **une fois**.

### Étape 2 — Aligner `PLAN_*` sur §5 bis

Dans `presets08.py`, faire coller `PLAN_PREMIER` / `PLAN_ARRIERE` (et donc `_cortex_twelve_parole`) à :

| | Premier | Arrière |
|--|---------|---------|
| wet | 0,06 | 0,12 |
| delay (ms) | 120 | 200 |
| fb | 0,04 | 0,08 |
| hpf | 300 | 20 ou 30 (pas de HPF musical) |
| lpf initial | centre de plage OK (écrasé par balayage) | idem |
| sat | ~0,48 / ~0,52, désaccord léger par couche OK | |

`CORTEX_LPF_AVANT = (800, 2000)` et `CORTEX_LPF_ARRIERE = (500, 1000)` : **déjà bons**, ne pas casser.

Les presets FSM (`PRESETS_8HP[0]`) doivent republier ces valeurs via `bank_msg_body` à l'entrée Cortex (déjà le cas si `_cortex_twelve_parole` est à jour).

### Étape 3 — LFO « osc #7 » pour le premier plan

Dans `gen_cortex_ctrl_08`, les couches premier (i pair) ne doivent **pas** utiliser la même suite `0.063 + i*0.019` que les arrières.

- Arrière (i impair) : garder 6 vitesses non harmoniques (indices 0–5 de la masse).
- Premier (i pair) : fréquence(s) dédiée(s) type **0,041 Hz** (ou autre hors rapports simples avec les 6 arrières) — une seule valeur partagée ou 6 très proches, peu importe tant que ce n'est pas la même grille que l'arrière.

Documenter la constante dans `presets08.py` (ex. `CORTEX_LFO_PREMIER_HZ`).

### Étape 4 — Forçage manuel pour l'écoute

Ajouter un mécanisme simple (messages Pd), documenté dans le patch / log :

**Minimum viable :**

```text
; s6_cx_force_plan <layer 1..12> <0|1>
```

- `0` = forcer PREMIER (gain + push FX PLAN_PREMIER + plage LPF avant)
- `1` = forcer ARRIERE

Implémentation suggérée dans `cortex_ctrl_08` (ou petit `cortex_plan_08.pd` généré) :

1. `r s6_cx_force_plan` → `route` / unpack layer + plan.
2. Envoyer `s6_l{n}_*` selon `amb_fx_msg`-like helper `plan_fx_msg(n, PLAN_*)`.
3. Positionner le gain plan : soit en écrivant un bus lu par `cortex_pair`, soit en réutilisant `s6_cx_swap{pr}` à 0 ou 1 **sans** lancer le geste spatial (attention mutex spectraux).

**Mieux si simple :** bus `s6_cx_plan_gain{n}` lu par `cortex_pair` à la place des constantes fixes quand un forçage est actif ; sinon comportement actuel.

Ne pas casser le swap automatique 4×/passage : le forçage est pour debug FORCE ; en AUTO, les plans nominaux (pair/impair) restent la règle V1 ([Q9] : le moteur attribue — ici attribution fixe alternée jusqu'au sélecteur tags).

### Étape 5 — Doc + log

1. [`docs/Zones/Cortex.md`](../Zones/Cortex.md) §6 : retirer « somme à poids égal / problème connu » ; pointer §10.
2. §10 A : plans → **FAIT** (ou PARTIEL si forçage minimal seulement).
3. [`docs/Backlog/TO DO.md`](./TO%20DO.md) §1 : cocher « plans de présence » + « deux gains / deux chaînes ».
4. Strophe append-only [`docs/log.md`](../log.md).
5. Si `etatactuel.md` mentionne encore plans incomplets : une ligne.

---

## Interdits

- Modifier Proto 06 / `fx_router_06.pd` (sauf lecture).
- Ajouter freeverb, granulaire, ou 2ᵉ delay custom.
- Brancher `gen_paires` / lire le xlsx.
- Casser `cortex_motion_08`, mutex `s6_cx_swp*`, seed, nappes.
- Éditer à la main les `.pd` générés — uniquement via `gen_libs08` / `gen_patch08` + regen.

---

## Tests de validation

1. Regen sans erreur + Pd headless : aucune « couldn't create ».
2. FORCE Cortex, une paire :  
   `; s6_cx_force_plan 1 0` puis `1 1` — différence claire (corps HPF, queue delay, ouverture).
3. Passage AUTO : swap avant/arrière toujours audible ; spectraux `; s6_spec_recipe RIPPLE` toujours OK.
4. Mesure mentale du gain : pas deux fois −2 dB sur l'arrière.

---

## Livrable attendu

- Diff code générateurs + presets.
- Patch régénéré.
- Spec respectée ; cases TO DO cochées.
- Réponse courte : ce qui a été fait, comment forcer un plan, quoi écouter.
