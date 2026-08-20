# Proto 06 — Calibrage à l'oreille (séparé du figé)

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Statut :** document vivant — valeurs modifiables sans toucher à l'architecture.  
**Référence figée :** `docs/10_proto_06_handoff_technique.md` §3 et §12 (ne pas rediscuter).

---

## 1. Où modifier les valeurs

Toutes les valeurs calibrables vivent dans **`scripts/proto06/proto06_lib/presets06.py`** :

| Bloc | Contenu | Q&A source |
|------|---------|------------|
| `CYCLE1` | états + durées du cycle 1 (~50 s) | Q3, §M |
| `FREE_DUR_BASE` / `FREE_DUR_RAND` | durées cycles 2+ (15–35 s par état) | Q12–15 |
| `FREE_CORTEX_EVERY` | retour CORTEX toutes les N transitions libres | Q3 |
| `RESET_MS` | reset session (420 000 ms = 7 min) | Q3 |
| `PRESETS` | 3 variantes × 4 états : mode SPAT, rot, sens, step, xfade, wet, delay, fb, lfo, on, ovl | Q22–23, H3, G5, F4 |
| `CONTRASTE_BAS` | facteur wet/fb/lfo en CONTRASTE bas (0.65) | Q24 |
| `ANCHORS_4HP` / `ANCHORS_6HP` | ancres fixes couche→HP (**figé N1** — ne pas permuter les slots, seuls les azimuts sont ajustables en salle) | N1 |
| `DECODE_6HP_AZ` | azimuts decode 6HP (rectangle + paire médiane) | §3.6 |

Après modification : relancer `python3 scripts/gen_prototype_06_4hp.py` (et `_6hp`),
puis `bash scripts/test_patch_console.sh pd/prototype_06_fsm_4hp.pd` (**console propre obligatoire, L6**).

## 2. Plafonds à ne jamais dépasser (figés)

- ECHO BOUCLE : wet **0.85**, delay **800 ms**, fb **0.70**, lfo **0.50** (H3).
- Feedback global hors CORTEX : **0.70** max (J3).
- CORTEX : ECHO **off** sur la couche principale (H3).
- Gain master : `*~ 0.65` (L3) — codé en dur dans `gen_patch06.py`, ne pas toucher.

## 3. À valider à l'oreille (session salle)

- [ ] Durées cycle 1 (12–16 / 5–9 / 14–18 / 10–16 s) — tableau §M.
- [ ] `ovl` CORTEX par variante (actuel : 3000 / 5000 / 8000 ms — plage §M 2–8 s).
- [ ] wet/fb par état (BOUCLE fort, HIPPO moyen, RECON bas ~0.15–0.35).
- [ ] `step` saut/séquence par variante (BOUCLE lent 3–10 s vs burst 300–400 ms — burst pas encore implémenté, voir §4).
- [ ] `rot` (vitesse rotation) par couche et ratio A/B.
- [ ] Azimuts 6HP en salle réelle (rectangle + paire médiane grand côté).
- [ ] Séparation spatiale audible 6HP (test 8.2 du handoff).

## 4. Hors périmètre V0 (implémentations futures, ne pas bloquer le gel)

- Patterns catalogués P1–P7 + repos oscillant (F.0.2) — actuel : séquence linéaire + saut aléatoire "jamais le même".
- Ping-pong au croisement (~25–30 % — E.7).
- Burst rapide BOUCLE 300–400 ms sur fenêtre 3–4 s (H2).
- Saturation / filtre HPF-LPF / phaser (proto 07 — J8 : sat → filtre → LFO → phaser).
- Tirage 1er HP aléatoire + opposé pour la séparation dynamique (Q36) — actuel : ancres fixes N1.
- `SPAT_LAYOUT` debug (AUTO/SÉPARATION/SUPERPOSITION/UNISON — Q48) et facteur UNISON (Q50).
- Queue delay/reverb inter-états (E.9) — actuel : le delay de `fx_fluid` résonne naturellement tant que la couche reste active.
- Superpositions **répétées** dans un même état (budget ~15 s / 50 s CORTEX, arrivées multiples HIPPO) — actuel : couches 2/3 one-shot, une superposition par entrée d'état.
- Graine aléatoire : les objets `random` de Pd sont déterministes au boot (même séquence de variantes à chaque lancement) — à randomiser si gênant en installation.

## 5. Rappels d'exploitation

- Lancement : `bash scripts/launch_prototype_06_4hp.sh` / `_6hp.sh`.
- Presets V0 (canvas principal) : `mode_presentation`, `mode_edition_complete`, `mode_automatique` (défaut au boot), `mode_danse`.
- INSTALL_MODE ON masque les fenêtres `moteur_06_*` et `debug_06_*` ; OFF les ouvre.
- FORCE_ETAT n'agit que si FSM_AUTO = 0 (Q21) ; re-clic = nouvelle variante SPAT/FX, même fichier (Q27).
- Proto 05 (`pd/prototype_05_fsm.pd`) : **figé**, sert uniquement de référence et de smoke test.

## 6. Continuité audio (Q7 — aucun blanc) — 10 juil. 2026

`player_state_06` diffère du lecteur 05 sur trois points :

| Changement | Raison |
|------------|--------|
| Fin de fichier → **relance automatique** (nouveau tirage dans le même slot état×durée) sur la **couche 1 (fond)** uniquement (`player_state_06 1`) | Q7 : aucun silence — un segment COURT dans un état long ne laisse plus de blanc |
| Couches 2/3 en **one-shot** (`player_state_06 0`) | Superpositions ponctuelles, pas d'interférence continue (budget Q29–30) |
| `del 150` → `del 80` avant `start` ; slot en entrée **froide** | Coupure ≤ 100 ms (Q7) ; le fichier ne change qu'au changement d'état réel (Q18/Q27) |

Validé par `pd/_test_player06_loop.pd` : 45 s de lecture DSP sur fichiers < 15 s, aucun passage sous le seuil d'audibilité.

## 7. Corrections session 10 juil. 2026 (blancs 6HP + couverture baffles)

Quatre causes distinctes de « blancs » / comportement incomplet, toutes corrigées :

| Bug | Effet entendu | Correctif |
|-----|---------------|-----------|
| `decode_6hp_06` : message matrice jamais connecté à `mtx_*~` | **Tout le bus ambisonique muet en 6HP** (modes dry + rotation) — il ne restait que saut/séquence | Connexion ajoutée ; validé par sonde `pd/_test_chain06.pd` (5 canaux actifs) |
| Saut/séquence limités à 4 bus HP | Pas de mouvement sur la paire médiane (canal 6) | `spatial_router_06` paramétré (`$4`=nb HP) : 5 bus en 6HP, séquence circulaire 60→120→240→300→0° |
| **Segments SONS/ silencieux** (mauvaises découpes) : 8 fichiers morts dont `voix_boucle_01` (14 s de silence pur dans BOUCLE/COURT) | Blancs longs aléatoires selon le tirage | `player_state_06` désormais **généré par scan de `SONS/` + audit RMS** (`proto06_lib/sons_audit.py`) : exclut tout segment vide ou à trou ≥ 5 s ; slot vide → repli sur les autres durées du même état |
| FSM démarrait au chargement du patch | Le temps d'allumer AUDIO_ON, le cycle 1 était déjà entamé → on n'entendait jamais BOUCLE→HIPPO→RECON→CORTEX | La session démarre au **AUDIO_ON** (send `s6_session`) : cycle 1 entendu depuis le début ; le reset 7 min court à partir de là |

Fichiers écartés par l'audit (à re-découper depuis les sources — voir `scripts/slice_extracts.sh`) :
`voix_cortex_01`, `voix_recon_04`, `voix_recon_02`, `voix_recon_03`, `voix_boucle_01` (silence total),
`voix_hippo_02` (trou 19 s), `voix_hippo_01` (trou 11 s), `voix_recon_01` (trou 6 s).
Relancer les générateurs après toute re-découpe : le scan est refait à chaque génération.

Validation : moniteur `pd/_test_engine06.pd` sur 90 s (6HP, AUTO) — cycle 1 aux bons timings
(BOUCLE 0 s → HIPPO 14 s → RECON 21.5 s → CORTEX 37.5 s), **aucun silence global**,
premier son ~350 ms après AUDIO_ON, mouvement audible sur les 5 canaux.

## 8. Principal long + interférences courtes, renouvellement (10 juil., après-midi)

Retour Loumana : principal ~20 s + interférences courtes par-dessus ; plus de
changement de samples après le cycle complet. Trois ajustements :

| Ajustement | Où | Détail |
|------------|----|--------|
| **Couche 1 (principal/fond) = slot MOYEN** (15–90 s), couches 2/3 (interférences) = COURT (< 15 s) | `presets06.FSM_N` | Vaut pour les 4 états ; le principal boucle en fin de fichier, les interférences restent one-shot |
| **Cycles libres : état suivant toujours différent** (`cur+1+random(3) mod 4`) | `fsm_memory_06` | Chaque transition libre change d'état → relance lecteurs → nouveaux samples à chaque passage |
| **Tirage sans répétition immédiate** (`prev+1+random(n-1) mod n`) | `player_state_06` | Jamais deux fois le même fichier de suite dans un slot (transitions ET relances fin de fichier) |

Validé au moniteur sur 150 s : cycle 1 exact puis libres `3→1→2→1` sans doublon d'état, zéro silence global.

**Limite contenu (K1) :** en slot MOYEN utilisable il ne reste que CORTEX 3 / HIPPO 4 /
RECON 2 / BOUCLE 2 fichiers — la répétition sur une session longue vient du stock,
pas du moteur. Re-découper les sources (surtout les `voix_*` écartés §7) et relancer
les générateurs élargira automatiquement les pools.

## 9. Variante 8HP + VISU (11 août 2026)

Nouveau patch : `pd/prototype_06_fsm_8hp.pd`

| Élément | Détail |
|---------|--------|
| Sorties | `dac~ 1 2 3 4 5 6 7 8` |
| Géométrie | octogone régulier (azimuts 0 / 45 / … / 315°) — `decode_8hp_06` |
| Ancres N1 | 6 ancres : HP1(0°) / HP3(90°) / HP5(180°) / HP7(270°) / HP2(45°) / HP6(225°) |
| Couches | **gradient profondeur** : CORTEX 2 · RECON 3 · BOUCLE 5 · HIPPO **6** (`FSM_N_8HP`, libs `*_06_8hp`) |
| Lancement | `bash scripts/launch_prototype_06_8hp.sh` (après `python3 scripts/gen_prototype_06_8hp.py`) |
| VISU | panneau **SAMPLES_EN_COURS** (jusqu’à 6 noms) + **HISTORIQUE_CERVEAU** — toujours visible |
| Boot | `mode_edition_complete` par défaut (INSTALL_MODE OFF) pour voir l’UI |

Libs dédiées 8HP : `fsm_memory_06_8hp`, `fsm_presets_06_8hp` (presets jusqu’à 6 couches).  
4HP/6HP restent à max 3 couches (`fsm_memory_06` / `fsm_presets_06`) — pas de régression.
