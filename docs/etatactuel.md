# État actuel — Mémoires en transit / Micro-opacités

**Snapshot :** 18 août 2026 · liens mis à jour le 20 août  
**IA :** [`README.md`](./README.md) (protocole) → **ce fichier** → [`Zones/`](./Zones/) → [`log.md`](./log.md).

Ce fichier dit **ce qui sonne**. [`Zones/`](./Zones/) dit **pourquoi ça sonne comme ça** et ce qui reste à figer. À trancher : [`Backlog/Q&A.md`](./Backlog/Q&A.md).

Installation 8 HP · Loumana · son : Simon Mahungu · Pd : Alassane Traoré  
Expos : 11 sept. 2026 CWB Paris · nov. 2026 Bozar / MBA Bruxelles

Le **fonctionnement général** ci-dessous tient. Les **FX / densités / pools** = oreille ; la source c’est le **dernier prompt** + [`log.md`](./log.md), pas le Q&A du 16 août.

---

## Lancer

| | |
|--|--|
| Patch | `pd/prototype_07_fsm_8hp.pd` (généré, pas à la main) |
| Lancer Mac | `bash scripts/launch_prototype_07_8hp.sh` |
| Lancer Raspberry Pi / Debian | `bash deploy/debian/launch.sh` (test) · au boot : `sudo bash deploy/debian/install-service.sh` |
| Régénérer | `python3 scripts/gen_prototype_07_8hp.py` |
| Matière | `SONS_V3/` — **seul dossier audio** · masters dans `SONS_V3/WIP/Opacité V6/` |
| Proto 06 | **hors service** depuis le 20 août : `SONS/` supprimé, les patches 06 sont muets |

AUDIO_ON off/on pour reset. FORCE 0/1/2/3 = Cortex / Hippo / Recon / Boucle (si AUTO off). Reset session **7 min**. Mac Pd 0.56.2 · Pi Pd 0.55.2. Sur le Pi, `launch.sh` ouvre la Scarlett (pas le HDMI). Expo : service systemd `memoires-en-transit` — **garder le mot de passe SSH**, pas besoin de se connecter au boot. Détail : [`deploy/debian/README.md`](../deploy/debian/README.md).

Sources : `scripts/proto07/proto07_lib/`. DSP partagé 06 : `fx_router_06`, `spatial_router_06`, `decode_8hp_06`.

---

## Comment ça marche

```text
AUDIO_ON → dsp → 200 ms → session → FSM
couche → player_state_07 → gain → gate ~3 ms → fx_router_06
  Cortex : 3 paires → HP1-3 · 5 nappes différentes → HP4-8
  Hippo/Recon : spatial_router → decode → MASTER → dac 1..8
```

Cycle AUTO : Cortex **40 s** → Hippo **50 s** → Recon **120 s**, puis libre 40–90 s.  
9 couches : L1–L6 fragments (3 paires HP1–3 en Cortex) · L9 nappe Hippo · 5 lecteurs nappe Cortex HP4–8 · inject Boucle one-shot.  
Lecteur : listes `pd/lib/playlists07/` (plus un `open` par wav — sinon Pd ne s’ouvre pas).  
Spat/filtre tout de suite. En Cortex **pas de send** delay/reverb vers d’autres baffles.  
Tirage hasard, évite le dernier fichier **de cette couche**. FORCE même zone = nouveau tirage.

---

## Zones (oreille, 18 août)

Détail, statut de gel et paramètres exacts : [`Zones/`](./Zones/) — un fichier par zone.

**Cortex** — **6 couches** fragments + **5 nappes**.  
Carte 8 HP : **HP1–3** = 3 paires (2 samples / baffle), rotation ou saut, LFO. **HP4–8** = 5 ambiances **différentes** en même temps — **uniquement** `CORTEX/AMBIANCE` (**27**), +2 dB, dry. Pas de baffle send.  
Fragments : **C0xx court** (`FRAGMENTS`, 48) + **C0xx moyen** (`LONG_MOYEN`, 42) + A déplacés (42). Pulse **10 s**.  
FX fragments : LPF **1500 Hz** qui **bouge 500–2000 Hz** (chaque couche à son rythme) + HPF ~450–630 + sat **~0,55–0,65** + peu de delay/reverb (wet ~0,10).

**Hippo** — 4 voyageurs. `FRAGMENTS` + `LONG_MOYEN` (pas d’ambiance Hippo encore : L9 **replie** sur nappe Cortex). Modes spat 4/2, steps 0,8–2,2 s. Nappe **voyage**, LPF lit 5 kHz. FX secs.

**Recon** — L1 `LONG_MOYEN` (**1**) · L2 `FRAGMENTS` (**287**). Quasi dry. L9 off.

**Boucle** — pas un paysage AUTO. 15 % à une transition → one-shot 8–90 s. Pas un buffer.

---

## Matière `SONS_V3/`

Pipeline : [`Matiere/Pipeline.md`](./Matiere/Pipeline.md). Attributs et tags : [`Matiere/Attributs.md`](./Matiere/Attributs.md).  
Découpe : `python3 scripts/slice_opacite_v3.py` — **incrémentale, ID stables** depuis le 20 août. Elle ne vide jamais `SONS_V3/`, ne renumérote pas, et ne touche jamais `WIP/`. Registre : `Matiere/registre_ids.csv`. Inventaire généré : `Matiere/inventaire_SONS_V3.md`. Classeur oreille : [`Matiere/catalogue_fragments.xlsx`](./Matiere/catalogue_fragments.xlsx) (pas lu par le patch).

Le rangement manuel gagne : un wav déplacé à la main (les 42 `A0xx` passés en `FRAGMENTS`) n'est jamais remis en place tout seul. `--reclasser` pour forcer, `--reset --yes` pour tout refaire (perd les ID).

Contrôle : `python3 scripts/verifier_sons.py` — 526 wav lus en une seconde, plus les 3481 références des playlists. Au 20 août : **aucune erreur**. Quinze fragments sont signalés « très bas » (pic −35 à −42 dBFS) sur une étendue totale de 42 dB ; à écouter, ce n'est pas un défaut de fichier mais un écart de niveau qui rend la densité perçue variable selon le tirage.

Chaque strate : `FRAGMENTS` · `AMBIANCE` · `LONG_MOYEN`.

| Pool | N | Moteur |
|------|---|--------|
| Cortex FRAGMENTS (C court + A déplacés) | 48+42 | L1–L6 avec moyens |
| Cortex LONG_MOYEN (C moyen) | 42 | L1–L6 (C0xx ≥13 s) |
| Cortex AMBIANCE | 27 | 5 nappes HP4–8 (exclusif) |
| Hippo FRAGMENTS / LONG_MOYEN / AMBIANCE | 69 / 10 / **0** | voyageurs ; L9 = nappe Cortex |
| Recon FRAGMENTS / LONG_MOYEN / AMBIANCE | 287 / 1 / **0** | L2 + L1 |

---

## UI utile

AUDIO_ON · MASTER 1,2 · FSM_AUTO · FORCE · CONTRASTE_HAUT · INPUT_ON (jamais vers HP) · RMS_SIM · SAMPLES_EN_COURS (noms réels).

---

## Interdits (inchangés)

Pas d’édition Proto 06. Pas de `,` / `;` bruts dans `#X text`. Piezo/micro jamais vers `dac~`.

**`SONS_V3/WIP/` = les masters de Simon.** Jamais de suppression, jamais de déplacement, jamais de découpe qui écrit dedans. C'est la seule matière irremplaçable du projet.
