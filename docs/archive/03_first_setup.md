# First Setup — Mémoires en transit (Prototype 01)

**Date :** 7 juillet 2026  
**Objectif :** Pure Data + ambisonie `iem_ambi` sur 4 sorties M-Audio.

---

## 0. Clarification IRCAM vs IEM

Tu as mentionné **l'IRCAM** (Institut de Recherche et Coordination Acoustique/Musique). C'est l'institut qui a développé **Spat** (Max/MSP) et des outils comme **VBAP**.

Pour ce projet en **Pure Data**, on utilise la bibliothèque **IEM** (Graz) :

| Outil | Écosystème | Rôle |
|-------|------------|------|
| Spat / VBAP | IRCAM / Max | Référence historique, pas dans ce repo |
| **`iem_ambi`** | IEM Graz | Encode/decode ambisonique dans Pd ✅ |
| **`pd-acre-amb`** | IEM (abstractions) | Couche au-dessus de `iem_ambi` — phase 2 |

Les deux approches (IRCAM et IEM) visent la même chose : **spatialiser le son dans l'espace**. `iem_ambi` est l'équivalent open-source utilisable sur Mac, Linux et Raspberry Pi.

---

## 1. MET_ROOT — convention des chemins

**MET_ROOT** = la racine du dépôt `memoires-en-transit/` (le dossier qui contient `pd/`, `SONS_PROTOTYPE/`, `scripts/`, etc.).

Tous les chemins du projet sont **relatifs à MET_ROOT** :

| Chemin relatif | Rôle |
|----------------|------|
| `pd/prototype_01_4hp_ambi.pd` | Patch principal |
| `SONS_PROTOTYPE/wav/` | Fichiers audio pour Pd |
| `pd/externals/iem_ambi-master/` | Bibliothèque ambisonie |
| `scripts/launch_prototype_01.sh` | Lancement |

Dans les patches Pd, les `open` utilisent par ex. `SONS_PROTOTYPE/wav/mon_fichier.wav` — Pd les résout via **MET_ROOT ajouté au Path**.

Le script `launch_prototype_01.sh` calcule MET_ROOT automatiquement (`scripts/../`) et l'ajoute au Path Pd. Aucun chemin absolu type `/Users/...` n'est nécessaire.

---

## 2. État actuel du dépôt (déjà fait)

- [x] `iem_ambi` extrait et **compilé** → `pd/externals/iem_ambi-master/iem_ambi.pd_darwin`
- [x] `iemmatrix` cloné et **compilé** → `pd/externals/iemmatrix/iemmatrix.pd_darwin`
- [x] MP3 convertis en WAV mono 48 kHz → `SONS_PROTOTYPE/wav/`
- [x] Patch prototype → `pd/prototype_01_4hp_ambi.pd`
- [x] Script de lancement → `scripts/launch_prototype_01.sh`

---

## 3. Installer / vérifier Pure Data

Tu as **Pd 0.56-2** dans `/Applications/Pd-0.56-2.app`.

Si besoin de réinstaller : [https://puredata.info/downloads](https://puredata.info/downloads)

---

## 4. Configurer Pure Data (une seule fois)

### A. Chemins (Path)

Depuis la racine du dépôt (`MET_ROOT`), ajoute dans **Pd → Preferences → Path…** :

```text
.                          ← MET_ROOT (racine memoires-en-transit)
pd
pd/externals/iem_ambi-master
pd/externals/iemmatrix
```

Si tu ouvres Pd depuis un autre répertoire, utilise le chemin absolu vers MET_ROOT une seule fois dans les Preferences — ou lance toujours via `scripts/launch_prototype_01.sh` qui configure tout automatiquement.

4. **Save all preferences**

### B. Bibliothèques au démarrage (Startup)

1. **Pd → Preferences → Startup…**
2. Clique **New…** et ajoute **le nom seul** (Pd ajoute `-lib` tout seul) :

```
iem_ambi
iemmatrix
```

   **Ne pas** écrire `-lib iemmatrix` — Pd chercherait un fichier `-lib iemmatrix.pd_darwin` et échouerait. Voir [`04_creer_un_patch_pd.md`](./04_creer_un_patch_pd.md).

3. Redémarre Pd

### C. Audio — UAD Volt 2 (dev actuel)

Interface **2 sorties** : utilise le **prototype 02**, pas le 01 (4 sorties).

1. **Media → Audio Settings…**
2. **Output device :** `Universal Audio Volt 2` (ou nom similaire)
3. **Channels :** **2** (Output 1 + Output 2)
4. **Sample rate :** **48000** (aligné avec les WAV dans `SONS_PROTOTYPE/wav/`)
5. **Delay (msec) :** 50–100 si craquements
6. **Apply** puis **Save settings**
7. **Media → Test Audio and MIDI…** — le bip doit sortir des sorties 1–2 du Volt

> **Mapping :** `dac~ 1 2` = sorties analogiques **1 (L)** et **2 (R)** du Volt 2.  
> Dans **UAD Console** (si ouvert) : vérifie que le monitoring n’est pas muet et que les sorties Main sont actives.

```bash
./scripts/launch_prototype_02.sh
```

Mode **SPATIAL 0 (DIRECT)** : même signal mono sur L et R — idéal pour valider Pd ↔ Volt 2 avant l’ambi.

### Cbis. Audio M-Audio (4 sorties — installation finale)

1. **Media → Audio Settings…**
2. **Output device :** interface **M-Audio**
3. **Channels :** au minimum **4 sorties**
4. **Sample rate :** 48000 (aligné avec les WAV convertis)
5. **Delay (msec) :** commence à 50–100 si tu entends des craquements
6. Clique **Apply** puis **Save settings**

> **Mapping des sorties :** `dac~ 1 2 3 4` dans le patch = sorties 1 à 4 de l'interface.  
> **HP1 (devant) = sortie 1** — à confirmer en branchant un HP à la fois.

---

## 5. Lancer le prototype

### Méthode rapide (recommandée)

Depuis n'importe où :

```bash
cd MET_ROOT   # racine memoires-en-transit
./scripts/launch_prototype_02.sh   # Volt 2 — 2 sorties (recommandé)
# ou
./scripts/launch_prototype_01.sh   # 4 sorties (M-Audio / install)
```

### Méthode manuelle

1. Ouvre `pd/prototype_01_4hp_ambi.pd` dans Pd
2. Vérifie que **AUDIO_ON** est activé (toggle en haut à gauche)
3. Le premier fichier audio démarre automatiquement au load

---

## 6. Utiliser le patch

| Contrôle | Action |
|----------|--------|
| **AUDIO_ON** | Active/désactive le DSP |
| **MODE 0** | Manuel — slider `phi_manuel` (0–360°) |
| **MODE 1** | Orbite — rotation automatique lente |
| **MODE 2** | Aléatoire — sauts de position toutes les ~3 s |
| **PLAY_ALEATOIRE** | Lance un fichier WAV au hasard |
| **phi°** | Affiche l'azimut actuel de la source |

### Chaîne audio

```text
player_folder → encode_2d → decode_4hp → dac~ 1 2 3 4
```

### Géométrie des 4 HP (rectangle, vue du dessus)

```text
         HP1 — 0° (sortie 1, devant)
    HP4              HP2
   270°              90°
         HP3 — 180°
```

Si le son ne va pas dans la bonne direction, inverse ou permute les câbles — c'est normal en prototype.

---

## 7. Tests recommandés

1. **Test sortie** — Mets MODE 0, phi = 0° : le son doit être devant (HP1)
2. **Test rotation** — phi = 90° → droite (HP2), 180° → derrière, 270° → gauche
3. **Test orbite** — MODE 1 : le son tourne tout seul
4. **Test aléatoire** — MODE 2 : sauts de position
5. **Test fichiers** — PLAY_ALEATOIRE plusieurs fois

---

## 8. Fichiers audio

| Dossier | Contenu |
|---------|---------|
| `SONS_PROTOTYPE/*.mp3` | Originaux (référence) |
| `SONS_PROTOTYPE/wav/*.wav` | **Utilisés par Pd** (mono, 48 kHz) |

Pure Data ne lit pas les MP3 nativement. Pour ajouter un nouveau son :

```bash
./scripts/convert_mp3_to_wav.sh
```

Ou manuellement depuis MET_ROOT :

```bash
ffmpeg -i "SONS_PROTOTYPE/mon_son.mp3" -ar 48000 -ac 1 "SONS_PROTOTYPE/wav/mon_son.wav"
```

Puis ajoute dans `pd/lib/player_folder.pd` une ligne :

```text
open SONS_PROTOTYPE/wav/mon_son.wav
```

---

## 9. Dépannage

### `unknown option: -path` au lancement

Sur macOS, utilise `./scripts/launch_prototype_01.sh` (il ouvre le patch via `open -a Pd`). Les chemins et libs sont declares dans le patch (`declare -path ... -lib ...`).

### Fenetre vide ou seulement le titre MET_PROTOTYPE_01

1. Ferme toutes les fenetres Pd ouvertes
2. Relance `./scripts/launch_prototype_01.sh`
3. Verifie le menu **Window** : la fenetre `MET_PROTOTYPE_01` doit etre au premier plan
4. Si des boites rouges `lib/...` ou `ambi_encode` apparaissent : les externals ne sont pas charges — ajoute dans **Pd > Preferences > Path** : `pd/externals/iem_ambi-master` et `pd/externals/iemmatrix`, puis **Startup** : `-lib iem_ambi` et `-lib iemmatrix`

### `iem_ambi: can't create` ou `mtx_*~: no such object`

- Vérifie les chemins Path et Startup (section 3)
- Redémarre Pd complètement
- Lance via `scripts/launch_prototype_01.sh` qui force les bons chemins

### Pas de son

- AUDIO_ON activé ?
- Interface M-Audio sélectionnée dans Audio Settings ?
- Volume système et gain des HP
- Ouvre **Media → Test Audio and MIDI…**

### Son mais pas de spatialisation

- Vérifie que `phi°` change quand tu bouges le slider
- Ouvre `pd/externals/iem_ambi-master/Ambisonic_2d_example.pd` pour valider `iem_ambi` seul

### Recompiler `iem_ambi` (si mise à jour Pd)

```bash
cd pd/externals/iem_ambi-master
make clean && make
```

### Recompiler `iemmatrix`

```bash
cd pd/externals/iemmatrix
make clean && make
```

---

## 10. Structure du projet

```text
memoires-en-transit/
├── docs/
│   ├── 01_premiere_recherche.md
│   ├── 02_prototype_01_decisions_et_plan.md
│   └── 03_first_setup.md          ← ce guide
├── pd/
│   ├── met_config.pd                ← rappel convention MET_ROOT
│   ├── prototype_01_4hp_ambi.pd
│   ├── lib/
│   │   ├── player_folder.pd
│   │   ├── encode_2d.pd
│   │   └── decode_4hp.pd
│   └── externals/
│       ├── iem_ambi-master/         ← compilé
│       └── iemmatrix/               ← compilé
├── SONS_PROTOTYPE/
│   ├── *.mp3
│   └── wav/*.wav
└── scripts/
    └── launch_prototype_01.sh
```

---

## 11. Prochaines étapes

1. Confirmer le mapping physique HP1–HP4 dans ta pièce
2. Passer à 12 HP (même logique, autre matrice `ambi_decode3`)
3. Machine à états (Cortex / Hippocampe / …)
4. Migration Raspberry Pi 5
5. Optionnel : `pd-acre-amb` pour simplifier les patches ambisoniques

---

## 12. À confirmer chez toi

- [ ] Quel **modèle exact** M-Audio ? (Fast Track, Air, autre)
- [ ] HP1 = sortie 1 = devant dans la pièce ?
- [ ] Dimensions approximatives du rectangle de HP ?

Une fois confirmé, on ajuste les angles `real_ls` dans `pd/lib/decode_4hp.pd`.
