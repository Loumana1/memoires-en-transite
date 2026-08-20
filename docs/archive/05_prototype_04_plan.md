# Prototype 04 — Plan de réalisation (brief pour l’IA suivante)

**Projet :** Mémoires en transit  
**Date :** 8 juillet 2026  
**Statut :** document de **planification uniquement** — ne pas coder avant d’avoir lu ce fichier en entier.  
**Prérequis :** [`03_first_setup.md`](./03_first_setup.md), [`04_creer_un_patch_pd.md`](./04_creer_un_patch_pd.md)

---

## 0. Contexte et décision

Le **prototype 03** (`pd/prototype_03_effects.pd`) est **abandonné dans l’état actuel**. Il ne doit **pas** servir de base de copier-coller. Les abstractions créées pour le proto 03 (`channel_strip.pd`, etc.) sont **suspectes** tant qu’elles n’ont pas été validées isolément.

Le **prototype 01** (`pd/prototype_01_4hp_ambi.pd`) **fonctionne** (son + spatialisation phi sur Volt 2 avec `decode_2hp`). C’est la **référence obligatoire** pour :

- la structure `declare` ;
- la chaîne audio de base ;
- le routage des modes via **`hradio` + `==` + `spigot`** ;
- l’initialisation (`loadbang`, phi, PLAY).

Les patches **exemples officiels / IEM** restent la référence pour les primitives bas niveau :

- `readsf~-help.pd` (Pd 0.56) — lecture WAV ;
- abstractions MET déjà validées : `player_folder.pd`, `encode_2d.pd`, `decode_4hp.pd`, `decode_2hp.pd`.

---

## 1. Objectif du prototype 04

Créer **`pd/prototype_04_effects.pd`** (+ script `scripts/launch_prototype_04.sh`) avec **les mêmes fonctionnalités visées** que le proto 03, mais avec une **architecture différente** : partir du proto 01, ajouter les effets **par couches testables**, sans routage parallèle fragile ni patch monolithique mal câblé.

### 1.1 Modes spatiaux (`hradio SPAT` — un seul actif)

| Mode | Comportement | Contrôles |
|------|--------------|-----------|
| **0 MANUEL** | Ambisonie 4 HP (`decode_4hp`) | Slider **phi** |
| **1 ROTATION** | Source qui tourne (encode + decode) | **rot_speed**, **SENS** (horaire / antihoraire) |
| **2 SAUT** | Mono sur **1 HP** à la fois, HP suivant aléatoire | **jump_ms**, **jump_xfade** (0 = coupure sèche) |

### 1.2 FX FLUID (toggle indépendant)

Combinable avec **n’importe quel** mode SPAT.

| Paramètre | Rôle |
|-----------|------|
| **fluid_wet** | Mix sec / effet |
| **fluid_delay** | Délai de base (ms) |
| **fluid_fb** | Feedback boucle |
| **fluid_lfo** | Modulation lente du délai |

### 1.3 Matériel de test actuel

- **Mac** + **UAD Volt 2** (2 sorties physiques).
- Pour entendre les 4 HP en dev : soit interface 4 sorties, soit accepter que seuls **`dac~ 1–2`** soient audibles (comme proto 01 en `decode_2hp`).
- **Recommandation dev Volt 2 :** commencer en **`decode_2hp` + `dac~ 1 2`**, basculer en **`decode_4hp` + `dac~ 1 2 3 4`** une fois la chaîne stable.

---

## 2. Pourquoi le prototype 03 a échoué (leçons obligatoires)

### 2.1 Échecs de routage / connexions

| Problème | Symptôme | Cause |
|----------|----------|-------|
| Indices `#X connect` invalides | `connection failed`, silence | Édition manuelle / réorganisation d’objets sans recalcul des indices. **Chaque `#X obj` ajouté décale tous les numéros.** |
| Bang mal branché | `dac~: no method for 'bang'` | Message `bang` de auto-play connecté à **`dac~`** au lieu du bouton **PLAY** → lecteur jamais déclenché. |
| Portes audio non initialisées | Silence total malgré DSP ON | `ambi-gate` / `jump-gate` à **0** au démarrage → `*~` multiplie le signal par 0. |
| `s` → `*~` | `send->*~ connection failed` | Un objet **`s`** ne peut pas alimenter l’entrée de contrôle d’un `*~`. Il faut **`r`** (receive) **à côté** de chaque `*~`. |
| Deux chemins audio en parallèle | 14× `audio signal outlet connected to nonsignal inlet` | Ambi **et** jump actifs en même temps sur les mêmes bus, avec abstractions empilées (`channel_strip` × 4 + `fx_fluid` × 4). |
| `loadbang → ; pd dsp 1` sur patch lourd | Erreurs signal au chargement | Activation DSP **trop tôt** (avant que `decode_4hp` ait reçu sa matrice interne). Le toggle **AUDIO_ON** (déjà à 1) suffit ; éviter le double déclenchement loadbang + toggle. |
| Abstraction `channel_strip` | Complexité + sends globaux | Mélange ambi/jump par **`s`/`r`** global : difficile à déboguer, ordre d’initialisation fragile. |

### 2.2 Échecs d’architecture

1. **Tout construire d’un coup** (4 canaux × strip × FX × jump × gates) sans valider une seule sortie d’abord.
2. **Mode SAUT en parallèle** de l’ambisonie au lieu d’un **commutateur exclusif** (comme le proto 01 le fait déjà pour phi).
3. **Réutilisation non testée** de `spatial_jump.pd`, `fx_fluid.pd`, `spatial_rotate.pd` — certaines peuvent être correctes isolément, mais **jamais validées** bout-en-bout dans le dépôt.
4. **Génération automatique** du `.pd` sans rechargement visuel dans Pd → erreurs de câblage restées invisibles jusqu’au runtime.

### 2.3 Échecs d’interface (retour utilisateur)

- Patch **visuellement « dégueulasse »** : fond gris (`cnv` #404040), contrôles **tassés**, zones qui se chevauchent.
- Impression de **filtre / interface grisée** : labels peu lisibles, pas de regroupement clair SPAT vs FLUID vs Transport.
- Sliders et radios **sans cadre visuel** — l’utilisateur ne voit pas quels paramètres appartiennent à quel mode.

**Consigne UI pour le proto 04 :** espacer, grouper, nommer. Voir section 6.

### 2.4 État des abstractions proto 03 (décision de fiabilité)

- `spatial_rotate.pd`, `spatial_jump.pd`, `fx_fluid.pd` sont considérées **non fiables par défaut** tant qu’un patch test isolé n’a pas validé leur comportement **et** l’absence de warnings console.
- Le proto 04 v1 doit rester fonctionnel même si ces abstractions sont temporairement exclues ou remplacées par une version inline minimale.

---

## 3. Principe directeur du prototype 04

> **Copier le squelette du proto 01. Ajouter une couche. Tester. Commit mental. Répéter.**

**Ne pas** reproduire l’approche proto 03 :

```text
❌ player → encode → decode ──┬── channel_strip ── fx × 4 ── dac
                              └── spatial_jump ──┘   (gates send/receive)
```

**Viser** plutôt :

```text
✅ player ──→ [ sélecteur de mode SPAT ] ──→ sortie spatialisée ──→ [ FX FLUID optionnel ] ──→ gain ──→ dac~
```

Le sélecteur de mode doit être **mutuellement exclusif** (un seul chemin audio actif), sur le modèle **`hradio` → `==` → `spigot`** du proto 01.

---

## 4. Architecture proposée

### 4.1 Vue d’ensemble

```text
┌─────────────────────────────────────────────────────────────────┐
│  UI (Transport + SPAT + FLUID) — patches visuels cnv          │
└─────────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
   [player_folder]              phi / rot / jump (contrôles)
         │
         ▼
   ┌─────────────┐
  │  SPAT_MODE  │  ← hradio 0|1|2 + commutation audio explicite (`*~`)
   └─────────────┘
         │
    ┌────┴────┬──────────────┐
    ▼         ▼              ▼
 MANUEL    ROTATION        SAUT
 encode    encode           spatial_jump
 decode    decode           (4 sorties HP)
 4 ou 2hp   idem             pas d’encode
    │         │              │
    └────┬────┴──────────────┘
         ▼
    [ bus mono ou 4 canaux ]
         ▼
   [ fx_fluid ]  ← toggle FLUID_FX (bypass = pass-through)
         ▼
    [*~ 0.65] × N
         ▼
      [dac~]
```

### 4.2 Trois stratégies possibles pour le mode SAUT (choisir A en priorité)

| Option | Description | Avantages | Inconvénients |
|--------|-------------|-----------|---------------|
| **A — Bypass ambisonie** | SPAT=2 : audio **ne passe pas** par encode/decode ; `[spatial_jump]` route le mono vers 1 HP. | Aligné avec la spec (« jump bypass ambi »). Simple à entendre. | 3 topologies distinctes à câbler. |
| **B — Gates audio explicites** | 4 × `*~` pour ouvrir/fermer les bus decode ou jump (coeff 0/1). | Compatible Pd vanilla, comportement lisible. | Plus de fils ; nécessite discipline stricte sur les inlets de contrôle. |
| **C — Réutiliser channel_strip** | Comme proto 03. | Déjà écrit. | **Déconseillé** — source des bugs. |

**Décision recommandée : option A**, avec **commutation audio explicite en `*~`** (gain 0/1), pilotée par `SPAT`, et validation sonore à chaque étape.

### 4.3 FX FLUID — où le placer

**Phase 1 (validation) :** une seule instance **`fx_fluid`** sur un **bus stéréo** (après `decode_2hp`, avant `dac~ 1 2`).

**Phase 2 (4 HP) :** soit

- **1 FX** sur la somme mono/stéréo intermédiaire (plus simple, suffisant artistiquement au début), soit
- **4 FX** seulement après preuve que 1 FX fonctionne (copier l’abstraction 4 fois — **jamais** avant).

L’abstraction `pd/lib/fx_fluid.pd` existe mais son état actuel est **à revalider** ; la tester seule (patch `_test_fx_fluid.pd`) et ne l’intégrer qu’après vérification console propre.

### 4.4 Fichiers à créer / réutiliser

| Fichier | Action |
|---------|--------|
| `pd/prototype_04_effects.pd` | **Créer** — copie adaptée du proto 01 |
| `scripts/launch_prototype_04.sh` | **Créer** — calquer `launch_prototype_01.sh` |
| `pd/lib/player_folder.pd` | **Réutiliser** tel quel |
| `pd/lib/encode_2d.pd` | **Réutiliser** tel quel |
| `pd/lib/decode_4hp.pd` / `decode_2hp.pd` | **Réutiliser** |
| `pd/lib/spatial_rotate.pd` | **Ne pas prendre comme base v1** ; préférer la rotation inline du proto 01, puis réévaluer l’abstraction |
| `pd/lib/spatial_jump.pd` | **Tester/assainir en patch isolé** avant toute intégration |
| `pd/lib/fx_fluid.pd` | **Tester/assainir en patch isolé** avant toute intégration |
| `pd/lib/channel_strip.pd` | **Ne pas utiliser** dans le proto 04 v1 |

### 4.5 Pattern phi (modes 0 et 1) — copier proto 01

Le proto 01 route déjà correctement l’azimut :

```text
hradio MODE → == 0/1/2 → spigot → s phi-azim → r phi-azim → encode_2d inlet 0
```

Pour le proto 04 :

- Renommer `MODE` → **`SPAT`** (même logique).
- Mode **0** : slider `phi` → spigot → `s phi-azim`.
- Mode **1** : phasor~ × 360 **inline (pattern proto 01)** → spigot → `s phi-azim`.
- Mode **2** : **ne pas** envoyer phi à encode — le spigot phi est fermé ; activer uniquement `spatial_jump`.

Référence lignes proto 01 : objets `== 0/1/2`, `spigot` × 3, `s phi-azim`, `r phi-azim` (voir `prototype_01_4hp_ambi.pd`).

---

## 5. Étapes de réalisation (ordre strict)

L’IA suivante **doit** suivre cet ordre et **ne pas passer à l’étape N+1** tant que l’étape N n’a pas du son audible.

### Étape 0 — Environnement

1. Pd démarre : `iemmatrix` + `iem_ambi` chargés.
2. `readsf~-help.pd` → son OK.
3. `prototype_01_4hp_ambi.pd` → son OK.

### Étape 1 — Squelette proto 04 = proto 01 (base de référence)

1. Dupliquer `prototype_01_4hp_ambi.pd` → `prototype_04_effects.pd`.
2. Renommer canvas `MET_PROTOTYPE_04`.
3. **Garder `decode_2hp` + `dac~ 1 2` en v1** (Volt 2, debug fiable).
4. Vérifier : **PLAY → son → phi bouge** (mode manuel), console sans warning critique.

**Critère de succès :** identique au proto 01.

### Étape 2 — UI de base (avant les nouveaux effets)

Réorganiser l’interface **sans toucher à l’audio** :

1. Créer **3 panneaux `cnv`** (bordure visible, fond clair — voir §6).
2. Déplacer les objets dans ces panneaux (Transport | SPAT | FLUID).
3. Espacer : **minimum 40 px** entre groupes, **120 px** entre colonnes.

Recharger le patch → audio **toujours OK**.

### Étape 3 — Mode ROTATION (SPAT 1)

1. Ajouter la chaîne rotation **inline** du proto 01 (`phasor~` → `*~ 360` → `snapshot~`), sans `spatial_rotate.pd` en v1.
2. Brancher comme proto 01 mode 1 : `== 1` → spigot → phi.
3. Contrôles : `rot_speed`, `SENS` (×1 / ×-1 via `* -2` + `+ 1` — pattern proto 03 validé en **control**, pas en audio).

**Test :** SPAT 1 → source tourne, SPAT 0 → slider reprend la main.

### Étape 4 — Mode SAUT (SPAT 2) — point critique

1. Créer patch test **`pd/_test_spatial_jump.pd`** : player → spatial_jump → dac~ 1 2 3 4 (1 sortie audible à la fois).
2. Valider `jump_ms`, `jump_xfade`, `enable`, **et absence de warnings signal/non-signal**.
3. Intégrer dans proto 04 avec **commutation exclusive** :
   - SPAT 0 ou 1 : player → encode → decode → …
   - SPAT 2 : player → spatial_jump → dac~ (sans encode).
4. Implémenter la commutation audio avec des `*~` (coefficients 0/1), jamais avec des routes ambiguës ni des inlets non-signal.

**Ne pas** mélanger jump et decode sur les mêmes fils sans switch.

### Étape 5 — FX FLUID (toggle)

1. Patch test **`pd/_test_fx_fluid.pd`** : osc~ ou player mono → fx_fluid → dac~.
2. Toggle `FLUID_FX` : bypass = signal sec (wet=0 ou inlet enable).
3. Intégrer **après** le bus spatial, **avant** gain/`dac~`, uniquement si le test isolé est propre.
4. Une instance d’abord ; étendre à 4 canaux seulement si nécessaire.

### Étape 6 — Script + doc

1. `scripts/launch_prototype_04.sh`.
2. Mettre à jour [`04_creer_un_patch_pd.md`](./04_creer_un_patch_pd.md) § prototype 04 (court renvoi vers ce fichier).

### Étape 6bis — Extension 4 HP (optionnelle, après v1 stable)

1. Remplacer `decode_2hp` par `decode_4hp`.
2. Passer de `dac~ 1 2` à `dac~ 1 2 3 4`.
3. Refaire la checklist console complète ; revenir en 2HP immédiatement si un warning réapparaît.

### Étape 7 — Checklist finale

| Test | Attendu |
|------|---------|
| SPAT 0 + phi | Panning ambisonique |
| SPAT 1 | Rotation continue |
| SPAT 2 | 1 HP actif, changement aléatoire |
| FLUID off | Timbré identique au sans-FX |
| FLUID on | Delay modulé audible |
| FLUID + SPAT 2 | Les deux actifs ensemble |
| Console Pd | **Aucune** `connection failed`, **aucune** `signal outlet connected to nonsignal inlet` |
| Volt 2 | Son sur sorties 1–2 minimum |

---

## 6. Interface utilisateur — spec visuelle

### 6.1 Problèmes constatés (proto 03)

- Un seul grand `cnv` gris foncé (#404040) — aspect « filtré / mort ».
- Contrôles SPAT, FLUID et Transport **mélangés** à gauche.
- Sliders `vsl` sans légende de groupe.
- Textes `#X text` noyés dans le patch.

### 6.2 Layout recommandé (proto 04)

Canvas cible : **~1000 × 720 px**.

```text
┌──────────────── TRANSPORT ────────────────┐  x=40, y=40, w=220, h=120
│  [AUDIO_ON]  [PLAY]                     │
│  (note Volt 2 : dac~ 1-2)               │
└─────────────────────────────────────────┘

┌──────────────── SPAT ───────────────────┐  x=40, y=180, w=420, h=320
│  ( ) 0 Manuel  ( ) 1 Rotation  ( ) 2 Saut
│  ── si 0 : [phi slider] [float phi]     │
│  ── si 1 : [rot_speed] [SENS CW/CCW]    │
│  ── si 2 : [jump_ms] [jump_xfade]       │
└─────────────────────────────────────────┘

┌──────────────── FLUID ──────────────────┐  x=500, y=180, w=280, h=220
│  [ ] FLUID_FX                           │
│  wet | delay | fb | lfo  (4 vsl)        │
└─────────────────────────────────────────┘

         [ chaîne audio — bas / droite, hors panneaux UI ]
         player → encode/decode/jump → fx → dac~
```

### 6.3 Couleurs `cnv` (Pd)

Utiliser des fonds **clairs** et des bordures visibles :

| Zone | Couleur fond suggérée | Label `cnv` |
|------|------------------------|-------------|
| Transport | `#f0f0f0` | `TRANSPORT` |
| SPAT | `#e8f4e8` | `SPATIAL` |
| FLUID | `#e8eef8` | `FLUID FX` |

Éviter `#404040` pour les zones de contrôle.

### 6.4 Affichage conditionnel (optionnel v1)

Pd vanilla ne cache pas nativement les sliders. Acceptable en v1 :

- **Tous** les sliders visibles mais **groupés** avec `#X text` (« actif en mode 0 », etc.).
- v2 possible : `spigot` sur les `vsl` (comme phi en proto 01) pour griser inactivement.

---

## 7. Limitations et pièges de routage (anti-sèche proto 04)

### 7.1 Règles de câblage

1. **`#X connect A B C D`** — A et C sont des **indices d’objets** dans l’ordre d’apparition du fichier (0 = premier `#X obj` après `declare`). **Chaque insertion décale tout.**
2. Préférer **câbler dans l’éditeur graphique Pd** puis sauvegarder, plutôt qu’éditer les `#X connect` à la main.
3. **`s` / `r`** : OK pour **phi**, gates, messages — **pas** pour router l’audio. L’audio = fils `~` uniquement.
4. **`receive`** sur l’entrée droite de `*~` : toujours un objet **`r`**, jamais un **`s`** directement.
5. **Mutuelle exclusion SPAT** : un mode = un chemin. Pas deux chemins actifs avec des gates float non initialisées.
6. **Interdit** : relier une sortie audio (`outlet~`) à un inlet non-audio (`inlet` / `float`) ; ce warning Pd est bloquant, même s’il affiche `ignored`.
7. **Commutation audio** : utiliser des `*~` (coeff 0/1) sur les bus ; `spigot` reste réservé au contrôle (phi/messages), pas à l’audio.

### 7.2 DSP et timing

| Action | Recommandation |
|--------|----------------|
| Activer DSP | Toggle **AUDIO_ON** (init à 1) → `; pd dsp $1` |
| Loadbang | phi=90, bang PLAY après **delay 600–800 ms** — **pas** `; pd dsp 1` en parallèle si patch > ~40 objets |
| Matrice decode | `decode_4hp` envoie sa matrice après **delay 200** interne — ne pas paniquer si 100 ms de silence au tout premier boot |

### 7.3 Tests de non-régression

Après **chaque** modification :

```bash
"/Applications/Pd-0.56-2.app/Contents/Resources/bin/pd" -nogui \
  -path ".../memoires-en-transit/pd/externals/iem_ambi-master" \
  -path ".../memoires-en-transit/pd/externals/iemmatrix" \
  -lib iem_ambi -lib iemmatrix \
  ".../memoires-en-transit/pd/prototype_04_effects.pd" 2>&1 | rg -i "error|failed|signal outlet connected to nonsignal inlet|connection failed"
```

Objectif : **sortie vide**. Si une ligne `... (ignored)` apparaît, la traiter comme un bug bloquant et corriger avant l’étape suivante.

### 7.4 Volt 2 vs 4 HP

- `decode_4hp` + `dac~ 1 2 3 4` : énergie sur 4 canaux logiques ; **seuls 1–2** sortent du Volt 2.
- Pour **entendre** la spatialisation à 2 sorties : `decode_2hp` (L=270°, R=90°) comme proto 01.
- Documenter dans le patch : `#X text` en Transport.

---

## 8. Ce qu’il ne faut surtout pas refaire

1. Patch monolithique 70+ objets câblés manuellement en une session.
2. Abstraction `channel_strip` avec `ambi-gate` / `jump-gate` globaux.
3. 4× `fx_fluid` + 4× `channel_strip` avant d’avoir **1** chaîne qui sonne.
4. Auto-générer le `.pd` en Python sans ouvrir Pd entre-temps.
5. Ignorer les erreurs console « signal → nonsignal » (« ignored » ≠ innocent — fils cassés).
6. UI grise sans groupes — l’utilisateur a explicitement demandé **plus d’espace et de clarté**.

---

## 9. Références de code à ouvrir en premier

| Priorité | Fichier | Pourquoi |
|----------|---------|----------|
| 1 | `pd/prototype_01_4hp_ambi.pd` | Chaîne complète qui **sonne** |
| 2 | `pd/prototype_02_2out.pd` | Lecteur minimal |
| 3 | `pd/lib/player_folder.pd` | Pattern open → delay → start |
| 4 | `pd/lib/encode_2d.pd` | Chaîne IEM phi → ambi_encode |
| 5 | `pd/lib/decode_4hp.pd` | Matrice HP fixe |
| 6 | `readsf~-help.pd` | Référence Pd officielle |
| 7 | `pd/prototype_03_effects.pd` | **Anti-exemple** — voir ce qu’il ne faut pas refaire |
| 8 | `docs/04_creer_un_patch_pd.md` | Procédure debug MET |

---

## 10. Livrables attendus de l’IA codeuse

- [ ] `pd/prototype_04_effects.pd`
- [ ] `scripts/launch_prototype_04.sh`
- [ ] (Optionnel) `pd/_test_spatial_jump.pd`, `pd/_test_fx_fluid.pd` — patches de validation intermédiaires
- [ ] Mise à jour minimale de `docs/04_creer_un_patch_pd.md` (lien vers ce plan + statut proto 03 abandonné)
- [ ] **Pas** de modification du proto 03 (laissé tel quel)
- [ ] Console Pd propre au chargement
- [ ] Son audible sur Volt 2 en mode SPAT 0 minimum

---

## 11. Résumé en une phrase

**Prototype 04 = prototype 01 qui fonctionne, plus une UI claire, plus trois modes SPAT commutés proprement (pas en parallèle), plus un FX fluid en bout de chaîne — construit en sept paliers testables, sans reproduire le routage par gates du prototype 03.**
