# Journal moteur — Prototype 07 8HP

> **18 août 2026 :** le journal vivant est [`../log.md`](../log.md). Ce fichier est une **copie figée** (vagues 16 août + notes 17 août). Ne plus y ajouter d’entrées.

**Date :** 16 août 2026 (moteur depuis affiné le 17)  
**Snapshot :** [`etatactuel.md`](./etatactuel.md)  
**Patch :** `pd/prototype_07_fsm_8hp.pd`  
**Lancer :** `scripts/launch_prototype_07_8hp.sh`  
**Régénérer :** `python3 scripts/gen_prototype_07_8hp.py`

Proto 06 **figé** (`prototype_06_fsm_*.pd`, `presets06.py` inchangés).  
Matière : `SONS_V2/` (pas `SONS/`). DSP partagé : `fx_router_06`, `spatial_router_06`, `decode_8hp_06`.

Chargement Pd-0.56.2 `-nogui` : **zéro error / warning**.

## 17 août soir — Cortex flou 06

Loumana : le Cortex 07 (LPF ~500 Hz, sat 0,72) ne sonnait pas. Retour au **son 06 8HP** + 1 HP nappe dry.

- Fragments : HPF 400–600, LPF ~2–3 kHz + flfo ~0,5, sat ~0,5, echo un peu plus que 06, ovl 50–80 ms
- Densité **6–8** (plus 3–6)
- Nappe : inchangée (1 HP, dry)

Régénérer : `python3 scripts/gen_prototype_07_8hp.py`

## 17 août — Cortex delay discret + distorsion

Après le retour flou 06 : distorsion **sat ~0,58**, delay **wet ~0,14** (pas fort), **feedback 5–7 %**. Filtre inchangé.

## 17 août — Cortex ECART dans le pool

Loumana : `SONS_V2/CORTEX/ECART/` n’est pas un rebut. Le lecteur tire dans **FRAGMENTS + ECART** (47 fichiers). Les dossiers restent séparés (journal de découpe).

## Écoute

1. FORCE 0 Cortex → 1 Hippo → 2 Recon (calibrage zone par zone)
2. AUTO : Cortex **40 s** → Hippo **50 s** → Recon **2 min**
3. Présence : `RMS_SIM` ON en Cortex = l’état se prolonge si l’énergie simulée est basse
4. `INPUT_ON` : piezo/micro en logique seulement — **jamais** vers les HP

## Ce qui est dans le moteur

| Vague | Comportement |
|-------|----------------|
| 2 | Cycle AUTO 40 / 50 / 120 s. Cortex densité **3–6** fragments + ambiance. Hippo 4 voyageurs. Recon 2 couches. |
| 3 | 8 baffles fragments (LPF ~550 Hz). Ambiance 1 HP, index tiré à l’entrée d’état. XOR ~50/50 dry / next-room. |
| 4 | Hippo mode 3 ping-pong 1↔8, FX plus secs. |
| 5 | Recon : PRINCIPAL+MOYEN en fond, COURT en interrupts (~4,5 s). |
| 6 | 15 % à une transition : one-shot 8–90 s plus tard, saut de HP. FORCE 3 = Boucle debug. |
| 7 | Hippo : bangs décalés couches 3–4. `s6_tag_hook` vide. Dossiers `DEGRE_*` réservés (vides). |
| 8 | `INPUT_ON` + `RMS_SIM`. Hold Cortex si énergie basse. |

## Fichiers

- `scripts/proto07/proto07_lib/` — presets, audit V2, générateurs
- `pd/lib/*_07*.pd` — FSM, player, Hippo, ambiance, présence, inject
- `scripts/proto07/gen_prototype_07_8hp.py` / `launch_prototype_07_8hp.sh` (raccourcis à `scripts/`)

Les principaux Recon ont des silences internes : le lecteur 07 **n’applique pas** l’audit RMS strict du 06.
