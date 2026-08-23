# Spec — Plans de présence Cortex (finir Proto 08)

**23 août 2026.** Complète [`../Zones/Cortex.md`](../Zones/Cortex.md) §5 bis · [Q9](./Q&A.md#q9) · [Q10](./Q&A.md#q10).  
Prompt IA : [`prompt_cortex_plans_presence_08.md`](./prompt_cortex_plans_presence_08.md).

## Intention

Deux profondeurs sous chaque paire de parole : **premier plan** (plus près, filtre plus ouvert) et **arrière-plan** (plus loin, delay plus wet). Sans ça, 12 voix au même traitement = bruit.

**Hors scope :** vraie réverb « pièce voisine » (delay V1 conservé) · sélecteur C1…C11 · `INTERMEDIAIRE`.

## Ce qui existe déjà (ne pas recâbler)

| Élément | Où |
|---------|-----|
| 12× `fx_router_06` (une chaîne **par couche**, avant `cortex_pair_08`) | `gen_patch08.py` |
| Gains nominaux + rampe d'échange avant/arrière | `cortex_pair_08` (`s6_cx_swap{pr}`) |
| Plages LPF distinctes pair/impair + glissement pendant swap | `cortex_ctrl_08` (`CORTEX_LPF_AVANT` / `ARRIERE`) |
| Presets FSM qui poussent wet/hpf/sat… par couche | `presets08._cortex_twelve_parole()` → `fsm_presets_08` |
| Override LPF gestes spectraux | `s6_cx_spec` / `s6_l{n}_spec_val` |

Architecture retenue (déjà en place) :

```text
player → *~ (gain couche) → [EMERGER gate] → fx_router_06 {L}
                                              → cortex_pair_08 (gain plan + somme + AM + spat)
```

**Ne pas** déplacer les `fx_router` *dans* `cortex_pair_08`. Une chaîne par couche **avant** la paire = déjà « deux chaînes sous chaque paire ».

## Écarts à corriger

### 1. Double application du gain de plan

Aujourd'hui le gain plan est appliqué **deux fois** :

- `gen_patch08` : `*~ (CORTEX_LAYER_GAIN × GAIN_PREMIER|ARRIERE)`
- `cortex_pair_08` : `*~` via `swfa` / `swba` (mêmes constantes)

**Règle :** un seul endroit. Garder le gain plan **dans `cortex_pair_08`** (nécessaire pour le swap). Sur le `*~` lecteur : **uniquement** `CORTEX_LAYER_GAIN` (et normalisation registre si présente).

### 2. Alignement des defaults sur §5 bis / Q10

Source de vérité : tableau [`Cortex.md`](../Zones/Cortex.md) §5 bis.

| Champ | `PREMIER_PLAN` | `ARRIERE_PLAN` |
|-------|----------------|----------------|
| Gain linéaire | `1.0` (0 dB) | `0.79` (−2 dB) — déjà `GAIN_*` |
| LPF balayage | **800 → 2000** | **500 → 1000** — déjà `CORTEX_LPF_*` |
| wet / delay / fb | **0,06 / 120 / 0,04** | **0,12 / 200 / 0,08** |
| HPF | **300 Hz** | **aucun** → coder `20` ou `30` (DC only), pas 60 « musical » |
| sat | laisser proches des valeurs actuelles (~0,48 / ~0,52), désaccordés par couche OK | idem |
| LFO LPF | **osc. dédié type #7** (vitesse hors rapports simples avec #0–5) | osc. **#0–5** (indices couche impair / arrière) |

Mettre à jour `PLAN_PREMIER` / `PLAN_ARRIERE` et `_cortex_twelve_parole()` pour coller au tableau wet/delay/fb/hpf. Petites désaccords par couche (hpf ±15, sat) **OK** ; wet/delay/fb restent ceux du tableau.

### 3. Mapping LFO « osc #7 »

Aujourd'hui les 12 osc. LPF sont `0.063 + i×0.019`. Pour les couches **premier** (indices pairs L1, L3, … L11), utiliser **une seule fréquence dédiée** (ex. `0.041` Hz ou autre hors harmoniques des six arrières), partagée ou légèrement désaccordée — l'esprit Q10 : le premier plan ne pulse pas au même rythme que la masse arrière.

### 4. Forçage manuel (debug écoute)

Sans attendre le sélecteur tags :

- Bus ou messages documentés pour forcer le plan d'une couche / d'une paire, ex.  
  `; s6_cx_plan 3 premier` (couche 3)  
  ou bascule paire : `; s6_cx_plan_pair 2 swap` (échange les rôles L5/L6 sans geste swap spatial).
- Doit pousser **gain + preset FX + plage LPF** de façon cohérente (pas seulement le gain).

### 5. Doc

- Mettre à jour [`Cortex.md`](../Zones/Cortex.md) §6 (texte « somme à poids égal » obsolète) et §10 A (plans → FAIT ou PARTIEL selon résultat).
- TO DO §1 : cocher plans + « deux gains / deux chaînes » quand validé à l'oreille.
- Strophe [`log.md`](../log.md).

## Non-régression

- Gestes spectraux + mutex swap inchangés.
- Échange avant/arrière : à swap=1, gains **et** plages LPF restent croisés ; presets wet/hpf suivent le rôle actif si le forçage/swap les pilote.
- Nappes L15/L16 : sèches, pas touchées.
- Pas de freeverb / pas de nouvel objet DSP hors `fx_router_06`.

## Critère « done »

1. Sur une paire isolée (FORCE Cortex, 1 baffle) : différence claire premier vs arrière (HPF, wet delay, ouverture LPF).
2. Swap 7 s : croisement audible sans clic, retour aux plans nominaux.
3. Regen `python3 scripts/gen_prototype_08_8hp.py` + Pd headless sans « couldn't create ».
4. Gain nominal = une seule multiplication plan (pas −4 dB accidentel).
