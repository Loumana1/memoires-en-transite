# État actuel — Mémoires en transit / Micro-opacités

**Snapshot :** 23 août 2026 · Proto **08** 8 HP  
**IA :** [`README.md`](./README.md) (protocole) → **ce fichier** → [`Zones/`](./Zones/) → [`log.md`](./log.md).

Ce fichier dit **ce qui sonne**. [`Zones/`](./Zones/) dit **pourquoi ça sonne comme ça** et ce qui reste à figer. Détail Cortex spatialisation + effets : [`Zones/Cortex.md`](./Zones/Cortex.md) §10.

Installation **8 baffles physiques** · Loumana · son : Simon Mahungu · Pd : Alassane Traoré  
Expos : 11 sept. 2026 CWB Paris · nov. 2026 Bozar / MBA Bruxelles

> **8 HP ≠ 12 voix.** 8 = nombre de haut-parleurs (carte Simon : 6 parole + 2 ambiance). 12 = couches de parole simultanées en Cortex (6 baffles × 2 fragments).

Le **fonctionnement général** ci-dessous tient pour le **Proto 08**. Les réglages d'oreille non figés = dernier prompt + [`log.md`](./log.md).

---

## Lancer

| | |
|--|--|
| Patch | `pd/prototype_08_fsm_8hp.pd` (généré, pas à la main) |
| Lancer Mac | `bash scripts/proto08/launch_prototype_08_8hp.sh` |
| Lancer Raspberry Pi / Debian | `bash deploy/debian/launch.sh` (test) · au boot : `sudo bash deploy/debian/install-service.sh` |
| Régénérer | `python3 scripts/gen_prototype_08_8hp.py` |
| Matière | `SONS_V3/` — **seul dossier audio** · masters dans `SONS_V3/WIP/Opacité V6/` |
| Proto 07 | figé, écoutable pour comparer · Proto 06 **hors service** |

AUDIO_ON off/on pour reset. FORCE 0/1/2/3 = Cortex / Hippo / Recon / Boucle (si AUTO off). Reset session **7 min**. Mac Pd 0.56.2 · Pi Pd 0.55.2. Détail déploiement : [`deploy/debian/README.md`](../deploy/debian/README.md).

Sources : `scripts/proto08/proto08_lib/`. DSP partagé 06 : `fx_router_06`, `spatial_router_06`. Décodeur 08 : `decode_8hp_08.pd` (matrice depuis `layout08.py`).

---

## Comment ça marche

```text
AUDIO_ON → dsp → 200 ms → session → FSM
couche → player_state_08 → gain → gate ~3 ms → fx_router_06
  Cortex : 6 paires → HP1-6 direct (pas ambisonics) · 2 nappes → HP5 texture, HP7 musicale
  Hippo/Recon : spatial_router → decode_8hp_08 → trim → MASTER → dac (canaux depuis layout)
```

Cycle AUTO : Cortex **40 s** → Hippo **50 s** → Recon **120 s**, puis libre 40–90 s.  
**14 lecteurs** : L1–L12 fragments Cortex · L15–L16 nappes Cortex · L13 nappe Hippo/Recon · inject Boucle one-shot.  
Listes `pd/lib/playlists08/`. Entropie session : `seed_source_08.pd` → `s6_seed`.

---

## Zones (oreille, 23 août)

**Cortex** — **12 voix** sur **6 baffles** + **2 nappes globales**.  
HP1–6 : 6 paires (2 samples / baffle), rotation, gestes `EMERGER`/`RECOUVRIR`, voyage phi 180° (15 s), échange avant/arrière (4×/passage, 7 s), gestes spectraux (`cortex_motion_08`).  
HP5 = texture · HP7 = musicale (pool mélodique A45–A69, gain ~+3 dB vs fragments). Nappe Reconstruction (état 2) : couche 13, slot 41.  
FX fragments : LPF balayé 12 osc. (500–2000 Hz) + HPF + sat + delay court. Override LPF pendant gestes spectraux. **Pas** de réverb « pièce voisine » encore.

**Hippo** — **loin du gel** (§9 [`Zones/Hippocampe.md`](./Zones/Hippocampe.md)). Proto 08 : 4 voyageurs (pas encore 5 voies) · `hippo_motion_08` / `hippo_assoc_08` / duck = **scaffold** · assoc mock sans classeur · spat `decode_8hp_08`. Nappe = repli pool partagé `AMBIANCE/` (pas master Hippo dédié [Q2]).

**Recon** — fragments + nappe (état 2). Quasi dry sur paroles.

**Boucle** — one-shot 8–90 s à 15 % des transitions. Pas de buffer.

Spatialisation détaillée : [`Zones/Cortex.md`](./Zones/Cortex.md) §10 · [`log.md`](./log.md) (22 août).

---

## Matière `SONS_V3/`

Pipeline : [`Matiere/Pipeline.md`](./Matiere/Pipeline.md). Découpe : `python3 scripts/slice_opacite_v3.py` (incrémentale, ID stables).  
Contrôle : `python3 scripts/verifier_sons.py`.

Pools Cortex ambiance (22 août) : segments A45–A69 ≥ 25 s, pool mélodique partagé ; 8 favoris Cortex (A53, A54, A59, A64–A68) en slots dédiés.

---

## UI utile

AUDIO_ON · MASTER 1,2 · FSM_AUTO · FORCE · CONTRASTE_HAUT · INPUT_ON (jamais vers HP) · RMS_SIM · SAMPLES_EN_COURS.  
Debug Cortex : `; s6_spec_recipe RIPPLE` · `; s6_amb_gain 0` (nappes, dB relatif) · `; s6_trim{n}` (égalisation par baffle).

---

## Interdits (inchangés)

Pas d'édition Proto 06. Pas de `,` / `;` bruts dans `#X text`. Piezo/micro jamais vers `dac~`.

**`SONS_V3/WIP/` = les masters de Simon.** Jamais de suppression, jamais de déplacement, jamais de découpe qui écrit dedans.
