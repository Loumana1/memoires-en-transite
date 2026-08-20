# Créer un patch Pd fonctionnel — Mémoires en transit

**Date :** 8 juillet 2026  
**Contexte :** session de débogage du prototype 02 (Volt 2), puis passage au prototype 01 (4 HP ambisonie).  
**Prérequis :** [`03_first_setup.md`](./03_first_setup.md) (Pd installé, libs compilées, WAV convertis).

---

## 1. Ce qui s’est passé (prototype 02)

Le prototype 02 (`pd/prototype_02_2out.pd`) devait valider la chaîne la plus simple : **lecteur WAV → dac~ 1–2 → UAD Volt 2**. Pd et l’interface audio fonctionnaient (Test Audio OK, patch d’aide `readsf~-help.pd` OK), mais **aucun son** ne sortait du prototype pendant plusieurs heures.

### Chronologie des blocages

| Symptôme | Cause réelle | Correction |
|----------|--------------|------------|
| `-lib iemmatrix: can't load library` | Dans **Preferences → Startup**, les entrées étaient `-lib iemmatrix` alors que Pd **ajoute déjà** le flag `-lib`. Pd cherchait un fichier nommé `-lib iemmatrix.pd_darwin`. | Startup : **`iemmatrix`** et **`iem_ambi`** seulement (sans `-lib`). |
| Silence, aucune erreur | `[readsf~]` recevait `open` mais jamais **`start`**. Sans `start`, le buffer se remplit mais la lecture ne démarre pas. | Chaîne `open` → `delay 150` → `start` → `readsf~`. |
| `delay: no method for 'open'` | La **sortie** des messages `open …` était branchée sur `[delay]`, qui n’accepte qu’un bang. | Déclencher le delay depuis `[select]` (bang), pas depuis le message `open`. |
| Toujours silence après les fixes ci-dessus | Chemins audio : `[readsf~]` est dans l’abstraction `pd/lib/player_folder.pd`. Le `declare -path ..` du patch parent **ne suffit pas** toujours pour résoudre `SONS_PROTOTYPE/wav/…` depuis une abstraction. | Ajouter `#X declare -path ../..;` **dans l’abstraction** (`pd/lib/` → MET_ROOT). |
| Erreurs `prvu~`, `rvu~`, `rbpq2~`… | Patch **`Ambisonic_2d_example.pd`** (démo IEM) ouvert en parallèle — ces objets viennent de **iemlib**, pas du prototype MET. | Fermer l’exemple IEM ou installer iemlib via Deken. |

### Validation finale

- Console au démarrage : `iemmatrix` + `iem_ambi (1.21.1) library loaded!`
- Patch d’aide officiel :  
  `/Applications/Pd-0.56-2.app/Contents/Resources/doc/5.reference/readsf~-help.pd` → **son OK**
- Prototype 02 rechargé → **son OK** sur Volt 2

**Leçon principale :** un patch MET peut être « correct » en apparence et rester muet. Il faut valider **dans l’ordre** : libs → audio système → patch d’aide Pd → patch MET.

---

## 2. Convention MET_ROOT (rappel)

**MET_ROOT** = racine du dépôt `memoires-en-transit/` (dossier contenant `pd/`, `SONS_PROTOTYPE/`, `scripts/`, `docs/`).

| Emplacement | Chemin relatif vers MET_ROOT |
|-------------|------------------------------|
| Patch principal `pd/prototype_*.pd` | `..` (un niveau au-dessus) |
| Abstraction `pd/lib/*.pd` | `../..` (deux niveaux au-dessus) |
| Fichiers audio | `SONS_PROTOTYPE/wav/nom.wav` (depuis MET_ROOT) |

Les chemins dans les messages `open` sont **toujours relatifs à MET_ROOT**, pas au fichier `.pd` qui les contient — **à condition** que MET_ROOT soit dans le path du canvas qui exécute `[readsf~]`.

---

## 3. Anatomie d’un patch MET qui fonctionne

### A. Patch principal (`pd/prototype_XX.pd`)

En tête du canvas, une ligne `declare` :

```pd
#X declare -path .. -path . -path lib -path externals/iem_ambi-master -path externals/iemmatrix;
```

| Flag | Rôle |
|------|------|
| `-path ..` | MET_ROOT |
| `-path .` | dossier `pd/` (patch + abstractions) |
| `-path lib` | abstractions `pd/lib/` |
| `-path externals/…` | patches d’aide IEM si besoin |

> **Ne pas** mettre `-lib iemmatrix` dans `declare` si les libs sont déjà dans **Startup** — évite les doublons. Les libs au démarrage suffisent pour les objets `ambi_*`, `mtx_*~`, etc.

**Audio :**

- Toggle ou loadbang → `; pd dsp 1`
- Sorties : `dac~ 1 2` (Volt 2) ou `dac~ 1 2 3 4` (prototype 01)

### B. Abstraction (`pd/lib/nom.pd`)

**Règle obligatoire** si l’abstraction lit des fichiers ou charge d’autres abstractions par chemin MET :

```pd
#X declare -path ../..;
```

Sans cela, `[readsf~]`, `[soundfiler]`, etc. cherchent les WAV **depuis `pd/lib/`** et échouent **sans message visible** (souvent filtré par la console Pd).

### C. Lecteur audio `[readsf~]` — pattern validé

Référence officielle : `readsf~-help.pd` (Pd 0.56).

```
[inlet / bang]
    |
 [t b] → [random] → [select …]
    |                      |
    |                      ├→ [open SONS_PROTOTYPE/wav/fichier.wav( → [readsf~]
    |                      └→ [delay 150] → [start(              → [readsf~]
    |
 [readsf~] → [*~ 0.9] → [outlet~]
    |
 (fin de fichier) bang → [t b]  … boucle aléatoire
```

Points clés :

1. **`open`** puis **`start`** (attendre ~100–150 ms)
2. WAV **PCM**, mono ou stéréo, **48 kHz** (aligné avec Media → Audio Settings)
3. Espaces dans les noms : `open SONS_PROTOTYPE/wav/mon\ fichier.wav`
4. Tester d’abord **un seul fichier** avant un sélecteur aléatoire

### D. Preferences Pd (une fois)

**Startup → Libraries** (Pd 0.56) :

```text
iemmatrix
iem_ambi
```

**Pas** `-lib iemmatrix` — Pd ajoute `-lib` automatiquement.

**Path** (complément au `declare` des patches) :

```text
/Users/…/memoires-en-transit
/Users/…/memoires-en-transit/pd
/Users/…/memoires-en-transit/pd/externals
```

(Copie des `.pd_darwin` dans `~/Documents/Pd/externals/` possible — voir session Solution C dans [`03_first_setup.md`](./03_first_setup.md).)

**macOS :** lancer via `open -a Pd patch.pd` — **ne pas** passer `-path` au launcher Tcl de l’app (erreur `unknown option: -path`).

---

## 4. Procédure : créer un nouveau patch MET

### Étape 1 — Valider l’environnement

1. Pd démarre sans `can't load library`
2. **Media → Test Audio** → bip audible
3. Ouvrir `readsf~-help.pd` → son audible

Si l’étape 3 échoue, ne pas avancer sur un patch custom.

### Étape 2 — Squelette minimal (test I/O)

Copier la structure de `prototype_02_2out.pd` :

- `declare -path ..` etc.
- `dac~` + abstraction lecteur ou `readsf~` inline
- DSP ON au loadbang

Objectif : **entendre un WAV** avant d’ajouter ambisonie, FSM, etc.

### Étape 3 — Ajouter une abstraction

1. Créer `pd/lib/mon_module.pd`
2. Ajouter **`#X declare -path ../..;`** en ligne 2
3. Dans le patch principal : `[lib/mon_module]`
4. **Fermer et rouvrir** le patch principal après chaque modification d’abstraction (Pd met en cache)

### Étape 4 — Spatialisation (prototype 01)

Chaîne MET actuelle :

```text
[player_folder] → [encode_2d] → [decode_4hp] → 4 × [*~ 0.65] → [dac~ 1 2 3 4]
                      ↑ phi (azimut)
```

Fichiers :

| Fichier | Rôle |
|---------|------|
| `pd/lib/player_folder.pd` | Lecture aléatoire WAV |
| `pd/lib/encode_2d.pd` | `ambi_encode` + `mtx_*~` |
| `pd/lib/decode_4hp.pd` | Matrice fixe 4 HP (5°, 95°, 185°, 275°) |

### Étape 5 — Script de lancement

```bash
./scripts/launch_prototype_01.sh   # 4 sorties ambisonie
./scripts/launch_prototype_02.sh   # 2 sorties direct (Volt 2)
```

Sur macOS, le script ouvre l’app Pd ; le `declare` du patch configure les paths.

---

## 5. Tester le prototype 01

### Matériel

Le prototype 01 utilise **`dac~ 1 2 3 4`**. Sur le **Volt 2** (2 sorties physiques), seules les sorties 1–2 recevront du signal ; les canaux 3–4 existent dans Pd mais n’ont pas de sortie hardware.

Options :

| Option | Usage |
|--------|--------|
| Interface **4 sorties** (ex. M-Audio) | Test spatial réaliste |
| Volt 2 | Entendre un sous-ensemble (HP 1–2) — suffisant pour valider encode/decode + son |
| Casque sur sortie 1 | Vérifier que le timbre **change** avec l’azimut (MODE 0 + slider phi) |

### Procédure

1. Fermer tous les autres patches Pd (surtout `Ambisonic_2d_example.pd`)
2. `./scripts/launch_prototype_01.sh`
3. Vérifier console : libs iem chargées, **pas** d’objets rouges (`ambi_encode`, `mtx_*~`)
4. **AUDIO_ON** activé (loadbang ou toggle)
5. **PLAY_ALEATOIRE** — un WAV démarre
6. **MODE 0** : bouger **phi** (0–360°) — la balance entre les 4 sorties doit évoluer
7. **MODE 1** : orbite automatique (phasor~)
8. **MODE 2** : azimut aléatoire toutes les 3 s

### Si pas de son

Appliquer la même checklist que prototype 02 :

- [ ] `player_folder.pd` contient `declare -path ../..` + `open` / `start`
- [ ] Patch **rechargé** après modif d’abstraction
- [ ] DSP ON
- [ ] Sample rate 48000
- [ ] Console : filtrer moins de lignes (Preferences → log level)

### Phi ne change rien (panning)

Deux causes fréquentes :

1. **Encode** : la chaîne IEM doit être `phi → ambi_encode → mtx → mtx_*~` (pas `col` direct vers `mtx_*~` seul). Voir `pd/lib/encode_2d.pd`.
2. **Decode + 2 sorties** : avec `decode_4hp` et `dac~ 1 2`, une grande part du signal part vers les HP 3–4 (inaudibles sur Volt 2). Le prototype 01 utilise **`decode_2hp`** (L=270°, R=90°) pour tester la spatialisation en stéréo. Pour 4 baffles physiques, repasser à `decode_4hp` + `dac~ 1 2 3 4`.

Repères phi en mode 2 HP : **0° ≈ gauche**, **90° ≈ droite**, **180° ≈ centre/arrière**, **270° ≈ gauche fort**.

Si les objets `ambi_*` / `mtx_*~` sont rouges → libs Startup (section 3.D).

Si `matrix_inverse nonsingular` → problème de matrice decode (matrice **fixe** dans `decode_4hp.pd` / `decode_2hp.pd` pour l’éviter).

---

## 6. Pièges connus (anti-sèche)

| Message / symptôme | Diagnostic |
|--------------------|------------|
| `can't load library` | Startup : nom seul (`iemmatrix`), binaire dans Path |
| Silence, zero erreur | `readsf~` sans `start`, ou mauvais path dans abstraction |
| `delay: no method for 'open'` | `open` branché sur `[delay]` au lieu d’un bang |
| `couldn't create prvu~` | Patch IEM / iemlib — pas un patch MET |
| `connection failed` | Indices `#X connect` incorrects après édition manuelle |
| `matrix~: no method for 'symbol'` | Message matrice envoyé au mauvais inlet |
| Interface vide au lancement | `-path` passé au mauvais binaire macOS |
| Modif abstraction ignorée | Fermer / rouvrir le patch parent |

---

## 7. Ordre de debug recommandé

```text
1. Libs IEM au démarrage
2. Media → Test Audio
3. readsf~-help.pd (Pd officiel)
4. prototype_02_2out.pd (MET, 2 sorties)
5. prototype_01_4hp_ambi.pd (MET, spatialisation)
6. Ambisonic_2d_example.pd (+ iemlib si vu-mètres IEM)
```

Ne pas sauter les étapes : chaque niveau isole une couche (audio OS → readsf~ → chemins MET → ambisonie).

---

## 8. Fichiers modifiés lors de la session (8 juil. 2026)

| Fichier | Modification |
|---------|--------------|
| `pd/lib/player_folder.pd` | `declare -path ../..` ; chaîne `open` → delay → `start` ; routage bang vers delay |
| `~/Library/Preferences/org.puredata.pd.plist` | `loadlib1` / `loadlib2` corrigés (`iemmatrix`, `iem_ambi`) |

---

## 10. Prototype 03 — effets spatiaux + fluid (8 juil. 2026) — **ABANDONNÉ**

**Patch :** `pd/prototype_03_effects.pd` — laissé tel quel, **ne pas utiliser comme base**.

Le proto 03 a échoué (connexions `#X connect`, routage parallèle ambi/jump, UI illisible). Voir le plan de reprise :

→ **[`05_prototype_04_plan.md`](./05_prototype_04_plan.md)** — brief complet pour l’IA suivante.

### Spec fonctionnelle conservée (à implémenter en proto 04)

| Mode | Comportement | Contrôles |
|------|--------------|-----------|
| **0 MANUEL** | Ambisonie 4 HP (`decode_4hp`) | Slider **phi** |
| **1 ROTATION** | Source qui tourne (encode + decode) | **rot_speed**, **SENS** (horaire / antihoraire) |
| **2 SAUT** | Mono sur **1 HP** à la fois, HP suivant aléatoire | **jump_ms**, **jump_xfade** (0 = coupure sèche) |

### FX FLUID (toggle indépendant)

Peut se combiner avec n’importe quel mode SPAT.

| Paramètre | Rôle |
|-----------|------|
| **fluid_wet** | Mix sec / effet |
| **fluid_delay** | Délai de base (ms) |
| **fluid_fb** | Feedback boucle |
| **fluid_lfo** | Modulation lente du délai (fluidité) |

### Abstractions du proto 03 (réutiliser avec prudence)

| Fichier | Statut |
|---------|--------|
| `lib/spatial_rotate.pd` | Contrôles OK — reprendre |
| `lib/spatial_jump.pd` | Tester isolément avant intégration |
| `lib/fx_fluid.pd` | Tester isolément avant intégration |
| `lib/channel_strip.pd` | **Ne pas réutiliser** (routage gates fragile) |

### Test proto 03 (historique)

1. Fermer les autres patches Pd
2. `./scripts/launch_prototype_03.sh`
3. Non concluant — voir [`05_prototype_04_plan.md`](./05_prototype_04_plan.md)

---

## 11. Prototype 04 — effets spatiaux + fluid (8 juil. 2026) — **RÉALISÉ**

**Patch :** `pd/prototype_04_effects.pd` — construit selon **[`05_prototype_04_plan.md`](./05_prototype_04_plan.md)** (base proto 01, pas de copier-coller du proto 03).

### Lancement et test

```bash
./scripts/launch_prototype_04.sh                              # GUI Pd
./scripts/test_patch_console.sh pd/prototype_04_effects.pd    # test console (critère: OK)
```

`scripts/test_patch_console.sh` lance `pd -nogui` avec les libs IEM, charge le patch + `pd/_autoquit.pd` (quitte après 3 s) et filtre `error|failed|ignored|signal outlet connected to nonsignal inlet`. Sortie attendue : `OK — console propre`.

### Architecture retenue

- ~~v1 = `decode_2hp` + `dac~ 1 2` (Volt 2)~~ → **passé en 4 HP le 8 juil. 2026** (étape 6bis) : `decode_4hp` + `dac~ 1 2 3 4`, une sortie de `spatial_jump` par HP. Nécessite dans Pd : **Media → Audio Settings → output device = carte 4 sorties, output channels = 4**. Pour revenir en Volt 2 : rétablir `decode_2hp`/`dac~ 1 2` dans `gen_prototype_04.py`.
- Commutation SPAT **exclusive** par gates audio `*~` (0/1, rampe `line~` 30 ms) : SPAT 0/1 → chaîne ambi, SPAT 2 → `spatial_jump`. Jamais deux chemins actifs.
- `spigot` réservé au **contrôle** (phi), jamais à l'audio.
- Rotation (SPAT 1) : chaîne **inline** `phasor~ → *~ 360 → snapshot~` (pattern proto 01), vitesse = `rot_speed × sens (±1)`.
- Saut (SPAT 2) : `lib/spatial_jump.pd` **réécrit** (gates `line~` + HP suivant ≠ HP courant), replié en 2 HP : sorties 1+3 → L, 2+4 → R.
- FLUID : `lib/fx_fluid.pd` **réécrit** (`vd~` + feedback clippé 0.95 + LFO ±10 ms), **une** instance sur le bus mono du lecteur, toggle = bypass sec.

### Le fichier est généré

`pd/prototype_04_effects.pd` est produit par **`scripts/gen_prototype_04.py`** (indices `#X connect` calculés par noms symboliques — plus d'indices décalés à la main). Pour modifier le patch : éditer le générateur, relancer :

```bash
python3 scripts/gen_prototype_04.py && ./scripts/test_patch_console.sh pd/prototype_04_effects.pd
```

(Si le patch est modifié dans l'éditeur Pd et sauvegardé, le générateur devient obsolète — le noter ici le cas échéant.)

### Patches de validation isolée

| Fichier | Rôle |
|---------|------|
| `pd/_test_spatial_jump.pd` | player → `spatial_jump` → `dac~ 1 2 3 4` (1 HP à la fois) |
| `pd/_test_fx_fluid.pd` | player → `fx_fluid` → `dac~` (toggle = bypass) |
| `pd/_autoquit.pd` | quitte Pd 3 s après chargement (tests `-nogui`) |

Statut console (8 juil. 2026) : proto 01, proto 04, les deux patches de test → **console propre** (libs IEM chargées, aucune ligne error/failed/ignored).

---

## 13. Suite du projet — prototypes 05 à final

**Roadmap complète :** [`07_roadmap_prototypes_finale.md`](./07_roadmap_prototypes_finale.md)

| Prototype | Objectif | Statut |
|-----------|----------|--------|
| **05 — FSM** | Machine à états 4 mémories, multi-lecteurs, `SONS/` | Plan → [`06_prototype_05_plan.md`](./06_prototype_05_plan.md) (retours terrain §14–18) |
| **06 — Interaction** | Piezo + analyse présence → modifie FSM | Plan dans roadmap §4 |
| **07 — FX bank** | Modules effets figés (distort, filter, grain…) | Plan dans roadmap §5 |
| **08 — 12 HP** | Spatialisation installation + calibration salle | Plan dans roadmap §6 |
| **FINAL** | Raspberry Pi 5, mémoire vivante, déploiement Paris/Bruxelles | Plan dans roadmap §7 |

**Expo Paris (11 sept. 2026) :** installation complète **12 HP** — les prototypes 05–08 sont les étapes intermédiaires sur Mac avant migration Pi.

---

## 14. Liens

- [`03_first_setup.md`](./03_first_setup.md) — installation, compilation, audio
- [`02_prototype_01_decisions_et_plan.md`](./02_prototype_01_decisions_et_plan.md) — architecture ambisonie 4 HP
- [`05_prototype_04_plan.md`](./05_prototype_04_plan.md) — plan proto 04 (brief IA)
- [`06_prototype_05_plan.md`](./06_prototype_05_plan.md) — plan proto 05 (FSM)
- [`07_roadmap_prototypes_finale.md`](./07_roadmap_prototypes_finale.md) — roadmap 05 → final
- [readsf~ (Pd 0.56)](file:///Applications/Pd-0.56-2.app/Contents/Resources/doc/5.reference/readsf~-help.pd)
- [Documentation IEM / declare et abstractions](https://github.com/pure-data/pure-data/issues/234) — chemins dans les abstractions
