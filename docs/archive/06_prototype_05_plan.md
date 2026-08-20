# Prototype 05 — Machine à états mémorielle (FSM)

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Statut :** document de **planification uniquement** — ne pas coder avant d’avoir lu ce fichier en entier et la roadmap [`07_roadmap_prototypes_finale.md`](./07_roadmap_prototypes_finale.md).  
**Prérequis :** [`05_prototype_04_plan.md`](./05_prototype_04_plan.md) (proto 04 **réalisé et validé** à l’oreille), [`04_creer_un_patch_pd.md`](./04_creer_un_patch_pd.md)

---

## 0. Décisions actées (réponses du 9 juil. 2026)

| Question | Décision |
|----------|----------|
| Priorité proto 05 | **FSM uniquement** — pas de montée à 12 HP dans ce prototype |
| Variantes HP | **4 HP** (référence) + variante **6 HP** optionnelle pour tester **2–3 couches simultanées** |
| Lecteurs simultanés | **Oui** — 2 à 3 fragments en parallèle selon l’état (surtout RECONSTRUCTION / HIPPOCAMPE) |
| Transitions | **Cycle 1 séquentiel** (~50 s) + cycles 2+ libres (fin CORTEX) + **reset 7 min** ; timing lié **contenu + queue FX** |
| Contenu audio | Les 10 pistes `SONS_PROTOTYPE/` = **placeholders** ; seuls **3–4 extraits réels** disponibles → **découpage** en segments LONG/MOYEN/COURT pour alimenter `SONS/` |
| Micros / piezo | **Hors scope proto 05** → proto 06 (piezo attendu ~11–12 juil.) |
| Cible expo Paris (11 sept. 2026) | **Installation complète 12 HP** — le proto 05 est une étape intermédiaire, pas la version finale |
| **Ordre AUTO** | **Cycle 1 :** BOUCLE → HIPPO → RECON → **CORTEX** (~50 s). **Cycles 2+ :** ordre libre, **fin CORTEX**. **Reset 7 min** → cycle 1. |
| **Durée visite** | **1 min** = succès ; **2–3 min** = idéal ; typique passionné **5–7 min** |
| **Dominance AUTO** | **CORTEX** = le plus de temps cumulé (clarté, effets atténués) |
| **Silence transitions** | **Aucun** (≤ 100 ms si coupure technique) |
| **FSM_AUTO load** | **On** dès ouverture patch ; off = manuel ; re-on à tout moment |
| **AUTO ↔ FORCE** | **Exclusifs** — FORCE inopérant si AUTO actif ; AUTO **off** → timer **arrêté/reset** (Q26) |
| **CONTRASTE défaut** | **HAUT** au load (Q24) |
| **variante_id** | Affiché en UI — **obligatoire** (Q25) |
| **FORCE re-clic** | **SPAT + FX** seulement — pas de nouveau fichier (Q27) |
| **Transition matériau** | **Même fichier** en général ; switch **rare** |
| **Fondu inter-état** | **Off** par défaut ; option **700 ms** si variante l’active |
| **Variantes / état** | **3** par état ; re-clic **50/50** ; toggle **`CONTRASTE`** haut/bas (Q24) |
| **Transitions timing** | Liées au **contenu** + **queue sortie** (delay/FLUID) |
| **Interaction** | Option **INPUT_ON** + triggers (proto 05 léger, larsen à gérer) |
| **Médiation** | **Panneau** + compréhensible ; couche **poétique**, pas trop abstrait |
| **Contenu SONS/** (Q6) | Pondération voix / radio **en attente** — selon quantité disponible |

---

## 1. Objectif du prototype 05

Créer **`pd/prototype_05_fsm.pd`** (+ script `scripts/launch_prototype_05.sh`) qui ajoute le **cerveau comportemental** au moteur spatial/effets du proto 04.

Le système ne se contente plus de jouer un fichier aléatoire : il **habite un état mémoriel** (Cortex, Hippocampe, Reconstruction, Boucle) qui détermine :

- **quoi** lire (dossiers + durées) ;
- **combien** de couches sonores actives (1 à 3) ;
- **comment** spatialiser et traiter (presets SPAT + FLUID hérités du proto 04) ;
- **quand** changer d’état (horloge + matrice de probabilités, ou forçage manuel).

### 1.1 Ce que le proto 05 apporte

| Couche | Proto 04 | Proto 05 |
|--------|----------|----------|
| Spatialisation | SPAT 0/1/2 manuel | **Presets par état** (ex. Cortex → saut rapide) |
| Effets | FLUID toggle global | **Presets wet/delay/fb/lfo par état** |
| Lecture | 1 lecteur aléatoire | **2–3 lecteurs** par état + durée |
| Décision | Aucune | **FSM** 4 états + transitions |
| Contrôle | UI Transport/SPAT/FLUID | **+ panneau ÉTAT** (auto/manuel) |

### 1.2 Ce que le proto 05 ne fait **pas**

- Pas de micros, piezo, RMS (→ proto 06)
- Pas de banque FX étendue (distorsion, bitcrusher…) (→ proto 07)
- Pas de 12 HP ni calibration salle (→ proto 08)
- Pas de Raspberry Pi headless (→ version finale)
- Pas de mémoire vivante `writesf~` (→ version finale)
- Pas du contenu définitif Quai Branly / BnF (préparation contenu en parallèle, hors code)

---

## 2. Les quatre états mémoriels

Aligné sur `Document_Technique_Definitif.md` et `02_prototype_01_decisions_et_plan.md`.

| État | Sens artistique | Position cycle | Lecteurs | FX / spatial (résumé) |
|------|-----------------|--------------|----------|------------------------|
| **BOUCLE** | Répétition, obsession — **entrée** | 1 | 1 | Saut lent ; delay variable |
| **HIPPOCAMPE** | Association, **dialogue en mouvement** | 2 | 2–3 | Fond + superpositions (F.0.1) ; bus indép. (Q49 B) |
| **RECONSTRUCTION** | Mémoire recomposée, plus claire | 3 | **1–2** | Phi **lent** indép. (G2–3) ; delay **décalé** dynamique (G4) ; moins filtré, plus saturé |
| **CORTEX** | Parole, idées claires (parfois floues) — **fin** | 4 (final) | 1–2 | Superposition brève ; filtre+LFO, pas de delay |

Les valeurs numériques exactes seront des **presets** dans `pd/lib/fsm_presets.pd` (ou table de messages), réglables sans recâbler l’audio.

---

## 3. Arborescence audio `SONS/`

### 3.1 Structure cible

```text
SONS/
├── CORTEX/
│   ├── LONG/    (> 60 s)
│   ├── MOYEN/   (15–60 s)
│   └── COURT/   (< 15 s)
├── HIPPOCAMPE/
│   ├── LONG/
│   ├── MOYEN/
│   └── COURT/
├── RECONSTRUCTION/
│   ├── LONG/
│   ├── MOYEN/
│   └── COURT/
├── BOUCLE/
│   ├── LONG/
│   ├── MOYEN/
│   └── COURT/
└── MEMOIRE_VIVANTE/    ← dossier vide en proto 05 (réservé version finale)
```

### 3.2 Stratégie contenu (extraits réels vs placeholders)

**Constat :** `SONS_PROTOTYPE/wav/` contient surtout des **exemples de travail**, pas la narration coloniale finale. Seuls **3–4 extraits réels** sont disponibles aujourd’hui.

**Décision proto 05 :**

1. **Découper** les 3–4 extraits réels en segments nommés `etat_duree_NNN.wav` (script `scripts/slice_extracts.sh` à créer).
2. **Répartir** manuellement les segments dans `SONS/<ETAT>/<DUREE>/` selon une grille artistique (session dédiée avec Loumana — voir § 3.3).
3. **Compléter** les dossiers vides avec des segments dérivés des placeholders `SONS_PROTOTYPE/` (clairement marqués `PLACEHOLDER_` dans le nom de fichier) pour que la FSM ait assez de matière en dev.
4. **Ne pas bloquer** le codage de la FSM sur le contenu définitif — la logique de scan de dossiers doit fonctionner avec n’importe quel WAV valide.

### 3.3 Session à planifier (hors code)

Avant ou en parallèle du proto 05, une session de **classification des extraits réels** :

- Quel extrait → quel état dominant ?
- Quelles plages temporelles → LONG / MOYEN / COURT ?
- Y a-t-il des zones « multi-états » à dupliquer dans plusieurs dossiers ?

**Livrable :** `docs/08_grille_contenu_sons.md` (à créer lors de la session).

---

## 4. Architecture technique

### 4.1 Vue d’ensemble

```text
┌─────────────────────────────────────────────────────────────────┐
│  UI : TRANSPORT | ÉTAT (FSM) | SPAT (debug) | FLUID (debug)   │
└─────────────────────────────────────────────────────────────────┘
         │                    │                      │
         ▼                    ▼                      ▼
   [player × N]         [fsm_memory]          [fsm_presets]
   N = 1..3                  │                      │
         │                    │ état + transition     │ SPAT/FLUID params
         │                    ▼                      │
         └────────────► [couche spatiale proto 04] ◄─┘
                              │
                    decode_4hp ou decode_6hp
                              │
                         dac~ 1..4 ou 1..6
```

### 4.2 Principe directeur (hérité du proto 04)

> **Réutiliser le moteur spatial du proto 04. Ajouter la FSM en amont. Une couche testable à la fois.**

- **Ne pas** recopier-coller le patch monolithique proto 04.
- **Extraire** la chaîne SPAT+FLUID+dac en abstraction `pd/lib/spatial_chain_4hp.pd` (refactor depuis proto 04) — ou appeler le générateur proto 04 comme sous-patch.
- **Générer** `prototype_05_fsm.pd` via `scripts/gen_prototype_05.py` (même discipline d’indices que proto 04).

### 4.3 FSM — comportement

**États :** entiers 0–3 ou symboles `CORTEX` / `HIPPOCAMPE` / `RECONSTRUCTION` / `BOUCLE`.

**Mode AUTO :**

- À l’entrée dans un état : timer aléatoire dans `[durée_min, durée_max]` de l’état.
- À expiration : tirage du prochain état selon **matrice de transition** 4×4 (lignes = état courant, colonnes = prochain état, somme = 1.0).
- Matrice par défaut (à affiner artistiquement) :

```text
              → CORTEX  HIPPO  RECON  BOUCLE
depuis CORTEX     0.10   0.50   0.30   0.10
depuis HIPPO      0.20   0.15   0.45   0.20
depuis RECON      0.25   0.35   0.10   0.30
depuis BOUCLE     0.40   0.20   0.20   0.20
```

**Mode MANUEL :**

- Toggle `FSM_AUTO` (1 = auto, 0 = manuel).
- En manuel : timer suspendu ; boutons ou `hradio` **FORCE_ÉTAT** pour passer à l’état voulu (répétitions, présentations).
- Transition manuelle déclenche quand même l’application des presets (SPAT/FLUID/lecteurs).

**Sorties FSM (messages) :**

- `état_courant` (symbol ou int)
- `bang transition` (front montant à chaque changement)
- `preset_id` → `fsm_presets`
- `n_lecteurs` (1, 2 ou 3)
- `dossier_cible` (chemin relatif MET_ROOT)

### 4.4 Multi-lecteurs (2–3 couches)

**Abstraction `pd/lib/player_state.pd` :**

- Entrées : `bang` (nouveau fichier), `dossier` (symbol), `durée` (LONG/MOYEN/COURT ou chemin complet).
- Sortie : `outlet~` mono.
- Pattern validé : `open` → `delay 150` → `start` → `readsf~` (comme `player_folder.pd`).
- Scan : `folder` ou liste fixe de messages `open` selon sous-dossier.

**Mixage avant spatialisation :**

| Variante | Stratégie multi-couche |
|----------|------------------------|
| **4 HP** | Somme mono des N lecteurs → **1** chaîne spatiale proto 04 (couches fusionnées dans le champ) |
| **6 HP** | **2–3 chaînes spatiales** indépendantes (1 lecteur → 1 encode → bus ambi séparé OU assignation HP dédiés) — voir § 5 |

En 4 HP, 2–3 fragments = **texture superposée** spatialisée ensemble.  
En 6 HP, 2–3 fragments = **sources distinctes** sur des HP différents (test de séparation spatiale).

### 4.5 Presets SPAT / FLUID

Abstraction `pd/lib/fsm_presets.pd` :

- Entrée : état (0–3).
- Sorties (messages) : `SPAT`, `rot_speed`, `SENS`, `jump_ms`, `jump_xfade`, `fluid_wet`, `fluid_delay`, `fluid_fb`, `fluid_lfo`, `fluid_on`.

Les messages alimentent les contrôles du moteur proto 04 (pas de recâblage audio à chaque transition — uniquement des floats/toggles).

---

## 5. Variantes 4 HP et 6 HP

### 5.1 Variante A — 4 HP (référence, obligatoire)

- `decode_4hp` + `dac~ 1 2 3 4` (déjà validé proto 04).
- Multi-couche : somme des lecteurs → 1× `fx_fluid` → 1× chaîne SPAT.
- **Critère :** FSM audible 10+ min, transitions claires, console propre.

### 5.2 Variante B — 6 HP (optionnelle, si matériel dispo)

- Nouvelle abstraction `pd/lib/decode_6hp.pd` : matrice `mtx_*~` 6×3, angles à confirmer (hexagone ou rectangle + 2 HP latéraux).
- Patch `pd/prototype_05_fsm_6hp.pd` OU flag dans le générateur.
- **2 lecteurs** → 2 encode_2d avec phi décalés (ex. 0° et 180°) → somme bus WXY → decode_6hp.
- **3 lecteurs** → 3 phi (0°, 120°, 240°) ou 2 chaînes + 1 saut HP dédié.

**Question matérielle à trancher avant variante B :** disposition physique des 6 HP et mapping `dac~ 1..6`.

---

## 6. Interface utilisateur

Canvas cible : **~1100 × 800 px** (proto 04 + panneau ÉTAT).

```text
┌──────── TRANSPORT ────────┐  ┌──────── ÉTAT (FSM) ────────────────┐
│  AUDIO_ON  PLAY           │  │  [ ] FSM_AUTO    État: CORTEX      │
│                           │  │  ( ) Cortex ( ) Hippocampe         │
└───────────────────────────┘  │  ( ) Reconstr. ( ) Boucle          │
                               │  timer: 1:23  [FORCE transition]   │
┌──────── SPAT (debug) ───────┐  └────────────────────────────────────┘
│  (lecture seule ou override)│
└───────────────────────────┘
┌──────── FLUID (debug) ──────┐
│  (lecture seule ou override)│
└───────────────────────────┘

[ chaîne audio — bas / droite ]
```

En mode AUTO, les sliders SPAT/FLUID peuvent être **pilotés par la FSM** (affichage des valeurs preset). Option debug : toggle `OVERRIDE_UI` pour reprendre la main (proto 04).

Couleurs `cnv` : reprendre proto 04 + panneau ÉTAT `#f8f0e8` (beige chaud).

---

## 7. Fichiers à créer / réutiliser

| Fichier | Action |
|---------|--------|
| `pd/prototype_05_fsm.pd` | **Créer** (générateur) |
| `pd/prototype_05_fsm_6hp.pd` | **Créer** (optionnel) |
| `scripts/gen_prototype_05.py` | **Créer** |
| `scripts/launch_prototype_05.sh` | **Créer** |
| `scripts/slice_extracts.sh` | **Créer** — découpe ffmpeg des 3–4 extraits |
| `pd/lib/fsm_memory.pd` | **Créer** — FSM + timer + matrice |
| `pd/lib/fsm_presets.pd` | **Créer** — table presets par état |
| `pd/lib/player_state.pd` | **Créer** — lecteur 1 dossier/durée |
| `pd/lib/spatial_chain_4hp.pd` | **Créer** — refactor chaîne proto 04 |
| `pd/lib/decode_6hp.pd` | **Créer** (optionnel) |
| `SONS/` | **Créer** arborescence + remplissage initial |
| `pd/lib/player_folder.pd` | **Conserver** (référence, pas supprimer) |
| `pd/prototype_04_effects.pd` | **Ne pas modifier** (référence stable) |

---

## 8. Étapes de réalisation (ordre strict)

Ne pas passer à l’étape N+1 tant que l’étape N n’est pas audible **et** console propre.

### Étape 0 — Préparation contenu minimal

1. Créer l’arborescence `SONS/`.
2. Découper au moins **1 extrait réel** en 3 segments (LONG/MOYEN/COURT) pour **1 état** (test).
3. Copier quelques placeholders dans les autres dossiers (dev seulement).

### Étape 1 — `player_state.pd` isolé

1. Patch test `pd/_test_player_state.pd` : bang → lecteur → dac~.
2. Valider scan d’un sous-dossier `SONS/CORTEX/COURT/`.

### Étape 2 — `fsm_memory.pd` isolé

1. Patch test `pd/_test_fsm.pd` : FSM seule, `print` des transitions, mode AUTO + MANUEL.
2. Pas d’audio — validation logique uniquement.

### Étape 3 — `fsm_presets.pd` isolé

1. Patch test : état 0→3 → vérifier les messages SPAT/FLUID sortants.

### Étape 4 — Squelette proto 05 = proto 04 + FSM passive

1. Chaîne audio proto 04 inchangée.
2. FSM tourne et affiche l’état, **sans** encore piloter l’audio.
3. Console propre.

### Étape 5 — FSM pilote presets + 1 lecteur

1. `player_state` remplace `player_folder`.
2. FSM choisit dossier selon état.
3. Presets SPAT/FLUID appliqués à chaque transition.

### Étape 6 — Multi-lecteurs (2 puis 3)

1. 2 lecteurs en HIPPOCAMPE, somme mono, 4 HP.
2. 3 lecteurs en RECONSTRUCTION.
3. Vérifier : pas de clipping (gain `*~ 0.5` ou `0.33` par couche).

### Étape 7 — Mode manuel + UI complète

1. Toggle FSM_AUTO, boutons FORCE_ÉTAT.
2. Panneaux `cnv` finaux.

### Étape 8 — Variante 6 HP (si matériel)

1. `decode_6hp.pd` + test tonal par HP.
2. 2 couches sur 6 HP.

### Étape 9 — Script, doc, checklist

1. `launch_prototype_05.sh`.
2. Mise à jour `04_creer_un_patch_pd.md` §13.
3. Session classification contenu → `08_grille_contenu_sons.md`.

---

## 9. Règles bloquantes (héritées proto 04)

1. **Interdit** : `outlet~` → inlet non-signal.
2. **Interdit** : deux chemins SPAT actifs (gates `*~` 0/1 conservés).
3. **`spigot`** : contrôle uniquement (phi, messages FSM).
4. **Test console** après chaque étape : `./scripts/test_patch_console.sh pd/prototype_05_fsm.pd`
5. **Générateur** pour les `#X connect` — pas d’édition manuelle des indices.
6. **DSP** : toggle AUDIO_ON, pas de `; pd dsp 1` loadbang sur patch lourd.

---

## 10. Checklist finale proto 05

| Test | Attendu |
|------|---------|
| FSM AUTO 10 min | Au moins 3 changements d’état audibles |
| FSM MANUEL | FORCE_ÉTAT change timbre + spatial immédiatement |
| CORTEX | Saut rapide, 1–2 couches |
| HIPPOCAMPE | Rotation + 2–3 couches |
| RECONSTRUCTION | FLUID élevé + superposition |
| BOUCLE | 1 HP dominant, répétition |
| Console Pd | Aucune error / failed / ignored |
| 4 HP | Son sur les 4 sorties |
| 6 HP (si fait) | 2 sources séparables spatialement |

---

## 11. Livrables attendus

- [ ] `pd/prototype_05_fsm.pd`
- [ ] `scripts/gen_prototype_05.py` + `launch_prototype_05.sh`
- [ ] `pd/lib/fsm_memory.pd`, `fsm_presets.pd`, `player_state.pd`
- [ ] `SONS/` peuplé (extraits réels découpés + placeholders dev)
- [ ] `scripts/slice_extracts.sh`
- [ ] Patches test `_test_player_state.pd`, `_test_fsm.pd`
- [ ] (Optionnel) `prototype_05_fsm_6hp.pd`, `decode_6hp.pd`
- [ ] Console propre au chargement

---

## 12. Résumé en une phrase

**Prototype 05 = proto 04 spatial validé + machine à états 4 mémories + 2–3 lecteurs parallèles + presets comportementaux + mode auto/manuel — sur 4 HP (6 HP en variante), avec contenu réel découpé dans `SONS/`, sans micros ni 12 HP.**

---

## 13. Clarification SPAT (9 juil. 2026)

### 13.1 Rotation ambisonique (mode existant)

Le mode **rotation** actuel (SPAT=1) utilise `phi` continu -> `encode_2d` -> `decode_4hp`.

- Ce mode produit un **mouvement fantôme continu** (pondérations sur plusieurs HP).
- Il **ne** correspond pas à une rotation discrète "HP1 puis HP2 puis HP3 puis HP4".
- Donc la perception peut être mobile sans qu'un seul HP soit dominant a 100 %.

### 13.2 Nouveau mode ajoute

Ajout d'un mode **SPAT=3** "sequence HP" pour lecture plus lisible en diffusion :

- cycle deterministe **HP1 -> HP2 -> HP3 -> HP4 -> HP1**
- vitesse = `jump_ms`
- fondu = `jump_xfade`
- implementation via `pd/lib/spatial_stepseq.pd`

### 13.3 Intention artistique

Les deux modes sont complementaires :

- **SPAT=1** : mouvement spatial continu (ambi, plus organique)
- **SPAT=3** : mouvement discret pedagogique/installation (baffle par baffle)

Ne pas supprimer SPAT=1 ; conserver les deux pour essais artistiques et mediation publique.

### 13.4 Modes autorisés par état FSM (I1 — acté)

| État | Base | Flash superposition |
|------|------|---------------------|
| **BOUCLE** | saut · séquence · rotation — **pas dry** | — |
| **RECON** | dry · saut · séquence · rotation | — |
| **HIPPO** | dry · rotation | saut · séquence · rotation |
| **CORTEX** | dry · rotation | saut · séquence · rotation |

→ Détail et cohérences F.0 / G2 / H4 : [`09_qa_prototype_05.md`](./09_qa_prototype_05.md) §I.1.

### 13.5 Continu vs baffle par baffle (I7 — acté)

| Perception | Mode | Rôle |
|------------|------|------|
| **Continu** (défaut) | **SPAT=1** | Rotation ambi — mouvement organique, fantôme |
| **Baffle par baffle** (option) | **SPAT=3** | Séquence HP — lecture discrète, installation |

Les deux coexistent ; le continu reste le **défaut** ; la séquence reste une **option** souhaitée (arrivées F.0.1, flash I.1, variantes).

---

## 14. Retours utilisateur — session proto 05 (9 juil. 2026)

Session de test réelle (M-Audio M-Track Eight, 4 baffles sur sorties 1–4, `dac~ 1 2 3 4`).

### 14.1 Ce qui fonctionne bien

| Élément | Retour |
|---------|--------|
| **FORCE_ETAT** | Changement audible immédiat à chaque clic ; effets et spatial globalement fonctionnels |
| **SPAT 0 (manuel)** | Comportement clair, rien à signaler |
| **États 2 et 3** (RECONSTRUCTION, BOUCLE) | Timbre + spatial jugés convaincants avec le traitement actuel |
| **SPAT 3 (séquence HP)** | Amélioration nette vs rotation ambisonique pour un balayage 1→2→3→4 |

### 14.2 Points à corriger (priorité artistique)

| Sujet | Constat utilisateur | Priorité |
|-------|---------------------|----------|
| **FSM_AUTO** | Le rythme de changement d’état ne correspond pas au ressenti voulu ; au démarrage, on ne sait pas si AUTO est actif | Haute — voir §16 |
| **Presets SPAT « identiques »** | En FORCE, le *mode* SPAT change, mais l’impression est que les réglages SPAT restent « les mêmes » d’un état à l’autre | Haute — voir §15 |
| **Rotation (SPAT 1)** | Trop lent ou trop rapide ; pas de zone confortable sur 4 HP | Haute — précision `rot_speed` au centième (§15.3) |
| **FLUID FX** | Perçu comme un delay simple, souvent trop présent ; états 0 et 1 moins réussis que 2 et 3 | Haute — renommer + recalibrer (§17) |
| **Rythme général** | Trop de rythme partout (sauts trop rapides, tempo mécanique) ; besoin de **respiration** et d’**intervalles variables** | Haute — voir §16.4–16.5 |

### 14.3 Matériel validé

- Carte : **M-Audio M-Track Eight**
- Câblage recommandé : **4 sorties mono distinctes** (1, 2, 3, 4) — pas `Primary Output` pour la quadriphonie
- Branchement testé fonctionnel sur 1–2 + Primary ; migration vers 1–2–3–4 validée comme meilleure pratique

---

## 15. Principe : presets dynamiques (pas valeurs fixes figées)

### 15.1 Problème actuel

À chaque transition FSM, le patch envoie une **ligne de preset** (messages vers SPAT, FLUID, lecteurs). En théorie ces valeurs **diffèrent par état** (voir tableau §15.2). En pratique :

- l’utilisateur perçoit parfois un **manque de différenciation** entre états 0/1 et 2/3 ;
- certains paramètres globaux (ex. `rot_speed` initial à 0.05 au loadbang) peuvent donner l’impression de « valeurs par défaut fixes » si les presets ne recouvrent pas tous les champs visibles ;
- le delay/feedback trop fort **masque** les différences spatiales sur CORTEX et HIPPOCAMPE.

### 15.2 Décision produit (actée)

Les « valeurs par défaut » ne sont **pas** une seule valeur fixe pour toute l’installation. Ce sont des **profils par état** :

- chaque état possède une **rangée de référence** (preset de base) ;
- à chaque entrée dans l’état, le moteur applique **toute la rangée** (SPAT + FX + nombre de lecteurs + durées) ;
- évolution prévue (proto 05b / 07) : **variation contrôlée** dans une plage autour de la rangée (ex. `wet ∈ [0.15, 0.25]` pour CORTEX, pas toujours `0.20` exact).

**Complément acté (9 juil. 2026, session FORCE) :** un état n’est pas **une** configuration figée, mais une **famille de configurations possibles** (voir §15.6–15.7).

### 15.3 Tableau des presets actuels (code `gen_prototype_05.py`)

Valeurs envoyées à chaque transition FORCE / AUTO :

| Paramètre | CORTEX (0) | HIPPOCAMPE (1) | RECONSTRUCTION (2) | BOUCLE (3) |
|-----------|------------|----------------|---------------------|------------|
| **SPAT mode** | 2 = saut | 1 = rotation | 0 = manuel | 2 = saut |
| **rot_speed** | — | **0.03** | — | — |
| **phi (manuel)** | — | — | **120** | — |
| **jump_ms** | **400** | — | — | **2000** |
| **jump_xfade** | **15** | — | — | **0** |
| **FX wet** | **0.20** | **0.50** | **0.75** | **0.85** |
| **FX delay (ms)** | **200** | **400** | **600** | **800** |
| **FX feedback** | **0.20** | **0.35** | **0.55** | **0.70** |
| **FX LFO** | **0.10** | **0.20** | **0.08** | **0.50** |
| **FX on** | 1 | 1 | 1 | 1 |
| **Lecteurs (n)** | 2 | 3 | 3 | 1 |
| **Durées dur** | 0,1,0 | 0,1,2 | 1,1,2 | 0,0,0 |
| **Timer auto (ms)** | 45 000 | 90 000 | 180 000 | 60 000 |

→ **Plafond delay projet (H3) :** BOUCLE `wet=0,85` `delay=800` `fb=0,70` `lfo=0,50` — **jamais dépasser** ; autres états dans plages inférieures (§M).

**Problème constaté (FORCE_ETAT) :** à chaque clic, la **même** rangée est rejouée (ex. BOUCLE → toujours SPAT=2 + FLUID on + mêmes floats). Le spatial change de mode mais **FLUID reste activé partout**, y compris CORTEX — ce qui ne correspond pas à l’intention.

**Lecture artistique :**

- CORTEX / HIPPO : delay actif dès l’entrée → peut noyer le spatial (saut / rotation).
- RECONSTRUCTION / BOUCLE : presets plus cohérents avec l’intention (superposition, feedback long).

### 15.4 Ajustements presets demandés (cible immédiate)

| Paramètre | Avant (typique) | Cible proposée |
|-----------|-----------------|----------------|
| **CORTEX — FLUID/DELAY** | `fl_on = 1`, wet 0.20 | **`fl_on = 0`** — pas de delay sur CORTEX |
| **CORTEX — FX principal** | delay + LFO sur temps | **filtre + LFO** (mouvement spectral, pas écho) — proto 07 |
| **FX wet global** | 0.20 – 0.85 | Baisser d’environ **−0.15 à −0.25** sur états 1–3 quand delay actif |
| **FX feedback global** | 0.20 – 0.70 | Plafond **≤ 0,70** (J3) ; RECON bas par défaut (G5) |
| **rot_speed pas** | floatatom **0.1** | floatatom **0.01** pour réglage fin sur 4 HP |
| **Renommage UI** | `FLUID_FX` | **`ECHO`** (J1) |
| **FORCE re-clic** | preset unique identique | **variantes** dans une famille par état (§15.6) |

### 15.5 Champs SPAT à couvrir à chaque transition

Pour éviter l’effet « tout pareil », chaque preset d’état doit explicitement pousser :

- `SPAT` (mode 0/1/2/3)
- `rot_speed`, `SENS` si mode rotation
- `phi` si mode manuel
- `jump_ms`, `jump_xfade` si saut ou séquence
- et **réinitialiser** les champs non utilisés (ex. passer en rotation → vider l’effet saut résiduel)
- et **désactiver explicitement** les FX non utilisés (ex. CORTEX → `delay_on=0`, `filter_on=1`)

### 15.6 Variantes par état — non-linéarité à la répétition (acté)

#### Problème

En **FORCE_ETAT**, chaque état se comporte comme un **interrupteur fixe** :

```text
Clic BOUCLE → toujours SPAT=2 + FLUID on + jump 2000 + wet 0.85 …
Re-clic BOUCLE → exactement la même chose
```

L’utilisateur veut **plus de complexité et de non-linéarité** : le clic sur un état doit ouvrir une **famille** de comportements possibles, pas une seule ligne.

#### Principe (acté)

| Niveau | Règle |
|--------|-------|
| **Identité de l’état** | CORTEX reste CORTEX, BOUCLE reste BOUCLE — même archétype narratif |
| **Instanciation** | À chaque entrée (FORCE ou AUTO), tirage d’une **variante** dans un pool défini pour cet état |
| **Paramètres** | Chaque variante utilise des **plages** (min/max), pas des scalaires fixes |
| **Re-clic même état** | **50/50** même variante vs autre parmi **3 variantes** par état |
| **FX** | Modules autorisés par état ; écart piloté par toggle **`CONTRASTE`** (Q24) |
| **Matériau audio** | AUTO : conserver le fichier (switch rare, Q18). **FORCE** : **SPAT/FX seuls** — pas de nouveau fichier (Q27) |

#### Modèle conceptuel

```text
FORCE_ETAT = BOUCLE
       │
       ▼
  pick_variant(BOUCLE)   ← **3 variantes** par état (v0, v1, v2)
       │
       ├── variante 0 : …
       ├── variante 1 : … (peut être la plus « extrême », même mentalité)
       └── variante 2 : …
       │
       ▼
  random_in_ranges(variante) → SPAT + FX  (+ même fichier audio sauf switch rare)
```

**Re-clic même état :** tirage **50/50** — rejouer la variante courante **ou** en choisir une autre dans le pool de 3.

#### Pools par état — **3 variantes** chacun (acté Q23)

Chaque pool existe en deux **échelles** selon `CONTRASTE` (Q24) :

| `CONTRASTE` | Effet sur les 3 variantes |
|-------------|----------------------------|
| **HAUT** | Wet/fb/spat plus extrêmes ; FX « voyants » ; séparation strates très nette |
| **BAS** | Mêmes 3 variantes logiques, paramètres **resserrés** ; différences audibles mais discrètes |

| État | v0 / v1 / v2 | Delay | Notes |
|------|--------------|-------|-------|
| **CORTEX (0)** | filtre+LFO × 3 profils | **off** | HAUT : filtres plus tranchés ; BAS : mouvements plus doux |
| **HIPPOCAMPE (1)** | spat + FX distincts | on, **dynamique** (↓ si superposition) | Phaser **ou** filtre+LFO : **50/50** (F5) ; HPF/LPF si dense — F4 |
| **RECONSTRUCTION (2)** | 3 profils delay/phi | on, **décalé** par couche | Phi lent ±180° aller-retour (G2–3) ; FX atténuables — G4 |
| **BOUCLE (3)** | saut **ou** séquence **50/50** (H4) ; saturation **dynamique** (H5) | on, **plafond** (H3) | Fort ~70–80 % ; phases **clarté** sans delay |

→ Une variante peut rester la plus « extrême » **dans l’échelle** choisie ; même mentalité d’état.

#### Ce qu’on ne veut pas

- un état qui active un effet complètement hors-sujet (ex. phaser agressif en BOUCLE profonde) ;
- une nouvelle configuration **totalement différente** à chaque fois sans cohérence narrative ;
- FLUID/DELAY **forcé on** sur CORTEX.

#### Impact technique (prévu)

| Composant | Rôle |
|-----------|------|
| `scripts/gen_fsm_presets.py` (nouveau) ou extension `gen_prototype_05.py` | Tables `VARIANTS[state][i]` avec plages |
| `pd/lib/fsm_presets.pd` | Tirage variante + plages + `variante_id` → UI |
| FORCE re-clic | Variante **50/50** ; applique **SPAT/FX** sans `open` nouveau fichier |
| UI | `variante_id` (floatatom 0–2) + `CONTRASTE` (défaut **1**) |
| Mode switch | AUTO off → **stop + reset** timer FSM ; pas de tick parallèle (Q26) |

### 15.7 CORTEX — traitement FX et superposition (acté)

| Module | CORTEX |
|--------|--------|
| **DELAY / FLUID** | **Désactivé** (`on = 0`) |
| **Filtre + LFO** | **Activé**, **très léger** — perturbation timbrale minimale |
| **Phaser** | Optionnel (variante) |
| **Saturation** | Légère possible (variante) |
| **SPAT** | Saut ou séquence, intervalles variables (§16.5) |

**Intention :** CORTEX = parole, idées claires (parfois floues) — **phase finale** ; fond stable + **impulsions** furtives (pensées / influx électriques).

#### Modèle audio CORTEX — couches et durées (Q29–32)

| Élément | Comportement |
|---------|--------------|
| **Défaut** | **Superposition brève** active (pas une variante optionnelle) |
| **Couche principale** | 1 lecteur — peut tenir **~50 s** sur le **même** fichier (cible debug ; plafond souple) |
| **Couche interférence** | 1 lecteur — fragments **parole** (mots / courte phrase) |
| **Spatial défaut** | Principal + interférence sur **mêmes baffles** |
| **FX défaut** | **Même** filtre+LFO (**identique**, même phase) sur toutes les couches superposées |
| **Intensité FX** | **Très légère** ; si plus forte → compte comme **interférence de pensée** (trouble la clarté) |
| **Sans superposition** | **Possible** — principal seul, pas de `p_intr` ; clarté maximale |
| **Durée overlap** | **~2 s** par événement (défaut) ; plancher ~**800 ms** trop court ; blocs **10–20 s** possibles |
| **Budget sur ~50 s** | Jusqu’à **~15 s cumulées** d’interférences — continues, parsemées, ou **aucune** |
| **Variante rare** | 2e interférence sur **autre baffle** (même FX) |
| **Variante très rare** | **3 couches** — baffles **distincts**, même FX (à confirmer) |
| **Variante FX** | Phase LFO **décalée** entre couches (loin du défaut) |

#### Perturbations de clarté (Q33–34)

Deux familles d’**interférences** sur la parole claire :

1. **Samples superposés** — pensées furtives (§ ci-dessus).
2. **Filtre + LFO** — même rôle perturbateur si intensité monte ; **défaut = très léger**.

**Clarté maximale :** 1 couche, pas d’overlap sample, filtre+LFO au minimum.

**Contenu (Q35) :** pas de média privilégié ; surtout **voix** — affinage quand `SONS/` complet.

```text
p_main ═══════════════════════════════════════►  clarté (~50 s possible)
p_intr    ▄▄ 2s    ▄▄ 2s      ▄▄▄▄▄ 10s        pensées furtives (≤ ~15 s total)
          └─ même HP + même filtre/LFO (défaut, phase identique)
```

Paramètres filtre+LFO CORTEX (J4 — acté) :

| Paramètre | Plage | Notes |
|-----------|-------|-------|
| **HPF** | 20 – 1 200 Hz | Coupe-bas |
| **LPF** | 1 200 – 20 000 Hz | Coupe-haut |
| **Résonance** | **~1 %** max | Très peu |
| LFO rate | à calibrer §M | Défaut très léger |
| mix filtre | à calibrer §M | **bas** (~0.2–0.35) |

### 15.8 Multi-couches — spatial et FX par lecteur (acté 9 juil. 2026)

#### Problème actuel (architecture)

```text
player_1 ─┐
player_2 ─┼─► mix~ ─► 1× fx_fluid ─► 1× SPAT ─► 4 HP
player_3 ─┘
```

Toutes les couches sont **superposées en permanence**, sur la **même** image spatiale, avec les **mêmes** effets — ce qui convient mal à HIPPOCAMPE et RECONSTRUCTION.

#### Principe par état (acté)

| État | Comportement multi-couches par défaut |
|------|--------------------------------------|
| **CORTEX** | **Principal long** (~50 s possible) + **interférences brèves** parsemées (défaut : **même baffle**, **même FX**) | Voir §15.7 |
| **HIPPOCAMPE** | **Fond + superpositions** (F.0.1) : arrivée → séquence HP ; 2e ajout → ambi ; fond indépendant |
| **RECONSTRUCTION** | Idem HIPPO pour **spatial** (Q46) ; **moins de couches** simultanées ; timbre **moins filtré**, **plus saturé** |
| **BOUCLE** | **1 lecteur** par défaut (Q47) ; superposition **prob.** (F4) ; palette spatiale riche ; queue FX |

#### Règles spatiales multi-couches (HIPPO / RECON)

| Règle | Détail |
|-------|--------|
| **2 sons** | **Toujours séparés**, baffles **opposés** (Q36) — **jamais** superposés |
| **3–4 sons** | **Alternance dynamique** : distincts **ou** superposés (Q37) — **non-linéaire** |
| **Plafond** | **4** samples simultanés max ; overlap 4 voix ~**5 s** max |
| **3 sons** | Souvent 3 HP distincts possible, mais **pas** le seul mode — superposition permise |
| **Distance (concept)** | **Degré de distance** entre couches — proto 05 = opposition max ; **12 HP** = séparation suffisante, pas toujours diamétrale |
| **Rotation** | 2 couches : tirage **sens** (±) et **vitesse** (±) — Q38 ; défaut probabiliste : **opposés + même vitesse** |
| **Croisement** | **Émergent** (rotation `phi`) — occasionnel ; ping-pong preset + ~25–30 % — Q43–45 |
| **Effets** | **Delay** seul levier FX à différencier (on/off/atténuer) ; autres FX **identiques** possibles — Q41 ; types variés possibles mais non obligatoires — Q40 |

#### Assignation 2 couches — algorithme proto 05 (Q36)

```text
hp_a = random(1, 4)
hp_b = opposite(hp_a)   // 1↔3, 2↔4
couche_1 → hp_a (ou hp_b, tirage 50/50 qui prend quel son)
couche_2 → l'autre
```

Implémentation prévue : `pd/lib/spatial_assign.pd` ou table dans `fsm_presets`.

#### Trois à quatre couches — dynamisme (Q37)

| Principe | Détail |
|----------|--------|
| **2 couches** | Séparation **obligatoire** (opposés) |
| **3–4 couches** | Mouvement **non linéaire** : LFO, filtre, **rotation ambi**, delay ; phases **séparées** et **superposées** |
| **4 simultanés** | Rare, **~5 s** max — malaise bref puis dispersion |
| **Linéarité** | **À éviter** — pas de pattern fixe apparition / déplacement |

États concernés : surtout **HIPPOCAMPE** et **RECONSTRUCTION** (pas CORTEX — règles propres §15.7).

**RECONSTRUCTION vs HIPPOCAMPE (Q46) :** règles spatiales **identiques** ; RECON se distingue par **densité** (moins d’infos simultanées) et **timbre** (filtre ↓ ; vivacité — saturation **superposés** seulement, J6).

**RECONSTRUCTION — phi & delay (G2–G4) :** `phi` **lent indépendant** par couche (aller-retour ±180°, pas cercle plein) ; delay **décalé** et **retiré** à chaque réactivation ; FX **atténuables / relançables**.

**RECONSTRUCTION — wet / fb (G5) :** **bas par défaut** (< HIPPO/BOUCLE) ; pics **brefs** si montée ; plages §M.

#### Gradient clarté narrative (Q46)

| État | Densité | Timbre (cible) |
|------|---------|----------------|
| **BOUCLE** | **Max** (impression dense, flou OK) | Filtré / delay — réf. proto 05 actuel |
| **HIPPOCAMPE** | 2–3 couches | Filtré, associations |
| **RECONSTRUCTION** | **Moins** de couches simultanées | **Moins filtré**, **plus saturé** (vivacité) |
| **CORTEX** | Overlaps furtifs | Clarté parole |

#### BOUCLE — une couche stricte + queue FX (Q47)

| | |
|---|---|
| **Simultané** | **1 lecteur actif** — jamais 2 couches BOUCLE en parallèle |
| **Transition** | Saut strict couche → couche (réf. proto 05 actuel) |
| **Queue FX** | Delay / reverb de la couche **précédente** continue après mute — lien inter-états (complète Q16) |

#### Layout spatial — AUTO vs debug (Q48)

| Contexte | Comportement |
|----------|--------------|
| **FSM_AUTO = 1** | Dynamisme presets + tirages (Q37) — **pas** de mode forcé |
| **FSM_AUTO = 0** | Toggle debug `SPAT_LAYOUT` : AUTO \| SÉPARATION \| SUPERPOSITION \| **UNISON** |
| **Stabilité** | `SPAT_LAYOUT` **ignoré** si AUTO on — ⊥ FSM_AUTO (comme FORCE) |

#### Rotation 2 couches (Q38)

| | |
|---|---|
| **Options** | Sens identique / opposé × vitesse identique / différente — **4 combinaisons** |
| **Favori (prob. modérée)** | Sens **opposés**, vitesse **identique** |
| **Règle** | Favori **plus probable** mais **pas dominant** — diversité préservée (≥ ~65 % autres cas) |
| **Vitesses** | Identiques ou différentes selon tirage ; plages numériques **[PLAGE]** (Q39) |
| **Ping-pong** | Variante : `rot_pingpong` + prob. ~25–30 % ; flip `SENS` au croisement — Q43–44 |

#### Croisement baffle (Q43–45)

| | |
|---|---|
| **Fréquence** | **Occasionnel** — acceptable, pas cible |
| **Origine** | **Émergent** — rotation `phi`, sens opposés ; **pas** saut programmé ni tirage HP aléatoire (Q44) |
| **Ping-pong** | Preset `rot_pingpong` + prob. ~**25–30 %** ; flip `SENS` au seuil croisement |
| **Durée overlap** | **Pas** de plafond forcé — passage naturel, typ. **< 1–2 s** (Q45) |

#### Effets par couche (Q40)

| | |
|---|---|
| **Préféré** | **Types différents** par couche (delay / saturation / filtre…) |
| **Aussi permis** | **Même** effet, réglages proches ou identiques |
| **Interdit** | **3 delays** simultanés très différents (oppressant, petite pièce) |
| **Max delays** | **2** max, réglages **proches** seulement |
| **Dynamique** | Alternance entre configurations différentes et unifiées |

#### Paramètres obligatoires par couche (Q41)

| Paramètre | Différenciation |
|-----------|-----------------|
| **Spatial** (nature : baffle, sens, mode) | **Toujours** — comportement actuel validé |
| **Delay** | **Seul FX** à moduler entre couches : **on / off / atténuer** |
| **Autres FX** (filtre, saturation, LFO…) | **Pas** d’obligation à différer — peuvent être **identiques** |
| **Delay permanent** | **Non** — pas sur **toutes** les couches en continu |
| **Rôle du delay** | **Nuage** autour de l’info ; couper = moins d’information, changement plus net |

#### CORTEX — superposition brève (résumé)

- Fond **clair** + influx **furtifs** (souvent **parole** : au moins un mot).
- **Défaut :** 1 principal + 1 interférence, **mêmes baffles**, **même FX**.
- Overlap **~2 s** ; budget **~15 s / ~50 s** ; variantes multi-baffles (rare / très rare) — §15.7.

#### Architecture cible (à implémenter — Q49 Option B)

```text
player_1 ─► FX_1 ─► encode_2d (phi₁) ──┐
player_2 ─► FX_2 ─► encode_2d (phi₂) ──┼─► somme W,X,Y ─► decode_4hp ─► 4 HP
player_3 ─► FX_3 ─► encode_2d (phi₃) ──┘

Mode saut (BOUCLE etc.) : spatial_jump par couche → bus HP ──┐
                                                              ├─► somme → dac~
Rotation (HIPPO/RECON)   : encode → ambi → decode ────────────┘
```

| Composant | Changement |
|-----------|------------|
| `prototype_05_fsm.pd` | Ne plus mixer avant FX ; **3 bus FX** + **3 encode** → **1 decode** |
| `spatial_jump` | Bus HP **hybride** (hors ambi) si saut par couche — somme avant `dac~` |
| `fsm_presets` | Par état : mode `separate` vs `brief_overlap` (CORTEX) |
| Assignation HP | **2 couches :** `random(1–4)` + **opposé** (1↔3, 2↔4) ; concept **degré de distance** pour 12 HP |
| Rotation opposée | `rot_speed` × `SENS` inversé par couche |

#### 4e HP, densité 3 couches, UNISON (Q50)

| | |
|---|---|
| **4e baffle** | Peut recevoir **remainder** / reverb — **bref** |
| **3 couches actives** | **Delay ↓↓↓** ; dernier arrivé part tôt ; patterns **P1–P7** (F.0.2) |
| **UNISON** | Par moments : même sample + mêmes FX sur tous les HP |

**Questions ouvertes :** voir `09_qa_prototype_05.md` §F–§M.

---

## 16. FSM — comportement cible (acté 9 juil. 2026)

### 16.0 Problème au démarrage (constat)

Quand on ouvre le patch et active **AUDIO_ON** :

| Élément | Comportement actuel (code) | Problème |
|---------|---------------------------|----------|
| **FSM_AUTO** | Toggle initialisé à **0** (off) | L’utilisateur ne sait pas si l’installation est « vivante » ou figée |
| **État FSM** | `fsm_memory` loadbang → état **0 (CORTEX)** | Ne correspond pas à l’intention narrative |
| **SPAT** | loadbang patch → mode **0 (manuel)** | Pas de preset d’état tant qu’aucune transition FSM |
| **Lecture** | Pas de `go` automatique au load | Silence jusqu’à FORCE ou activation manuelle d’AUTO |

### 16.1 Comportement au démarrage — cible (acté)

**Décision :** l’installation doit être **dynamique d’office**.

```text
Ouverture patch + AUDIO_ON
       │
       ▼
  FSM_AUTO = 1  (toggle ON par défaut)
       │
       ▼
  État initial = BOUCLE (3)   ← « partie la plus profonde » du cerveau
       │
       ├──► applique preset complet BOUCLE (SPAT + FX + lecteurs)
       └──► démarre timer FSM + lecture audio
```

| Règle | Détail |
|-------|--------|
| **AUTO par défaut** | `FSM_AUTO` doit être **activé** au load (toggle à 1) |
| **Premier état** | **BOUCLE (3)** — répétition, strate profonde, obsession mémorielle |
| **Feedback UI** | `etat_courant` + toggle AUTO doivent refléter immédiatement l’état réel |
| **FORCE_ETAT** | Reste disponible pour tests ; coupe temporairement la logique auto si besoin (comportement à préciser en implémentation) |

**Narration :** on entre par la **BOUCLE** (profondeur), on remonte via **HIPPOCAMPE** et **RECONSTRUCTION**, on **atterrit sur CORTEX** (clarté — phase finale de la circulation).

### 16.2 Mode FORCE (manuel) — exclusif avec AUTO

```text
FSM_AUTO = 1  ──►  FORCE_ETAT **ignoré**
       │
FSM_AUTO = 0  ──►  timer AUTO **arrêté + reset** (Q26)
       │
       ▼
  FORCE_ETAT / re-clic
       │
       ▼
  pick_variant [50/50] → **SPAT + FX** (+ variante_id UI)
       │
       └──► **pas** de bang `open` / pas de nouveau fichier (Q27)
```

| Règle | Détail |
|-------|--------|
| **Exclusivité** | AUTO on → FORCE sans effet (Q21) |
| **Timer AUTO** | Couper AUTO pour FORCE → timer **stop + reset** — **aucun** processus parallèle (Q26) |
| **Réactiver AUTO** | Repart de zéro (cycle 1 ou état documenté) — pas reprise du timer suspendu |
| **3 variantes** | Pool de 3 ; re-clic **50/50** (Q22–23) |
| **CONTRASTE** | Toggle HAUT/BAS ; **défaut HAUT** (Q24) |
| **variante_id** | **Affiché** dans UI (Q25) |
| **Matériau** | FORCE = **altération** spat/FX sur le **même** audio en cours ; choix des fichiers / couches = logique **séparée** (distribution « aléatoire » des lecteurs, Q27) |

### 16.2b Transitions inter-états — fondu et matériau (Q18–20)

| Paramètre | Défaut | Variante possible |
|-----------|--------|-------------------|
| **Fichier audio** | **Continuer** le même segment | **Switch** rare (flag dans preset variante) |
| **Fondu global** | **Coupure** (≤ 100 ms, Q7) | **Fondu 700 ms** si variante l’active |
| **Relance lecteurs** | **Non** — ne pas `open` à chaque transition sauf switch rare |

Implémentation : champ `xfade_ms` par transition (0 = défaut, 700 = fondu) dans `fsm_presets`.

### 16.3 Mode AUTO — parcours narratif et temporalité (acté 9 juil. 2026)

#### Contexte visite

| Indicateur | Cible |
|------------|-------|
| Petite pièce | Visite naturellement **courte** |
| **1 min** d’écoute | Déjà un **succès** |
| **2–3 min** | Durée **idéale** |
| **5–7 min** | Visiteur **passionné** (plafond réaliste) |
| **15 min** | Exceptionnel — quasi maximum |
| **3 min** cumulées | Chaque strate vécue **≥ 2 fois** (objectif initial) |
| **7 min** cumulées | **Reset forcé** → nouveau **cycle 1** (BOUCLE en tête) |

#### Règle d’or : atterrissage sur la clarté

Chaque cycle AUTO (sauf le départ initial) doit **se terminer sur CORTEX** — strate la plus **claire**, la moins dérangeante. Sur une session 5–7 min, **CORTEX** doit dominer le **temps cumulé** (variantes atténuées / quasi directes privilégiées).

#### Cycle 1 — obligatoire, ~50 s, BOUCLE en premier

**Ordre acté :** montée profondeur → clarté ; **CORTEX uniquement en fin de cycle**.

```text
   BOUCLE (3)  ──14s──►  HIPPO (1)  ──7s──►  RECON (2)  ──16s──►  CORTEX (0)  ──13s──►  [fin cycle 1]
   profondeur              associations        recomposition         clarté (final)
```

| Transition | De | Vers | Durée cible | Plage (ms) |
|------------|-----|------|-------------|------------|
| T0 | — | BOUCLE | **14 s** | 12 000 – 16 000 |
| T1 | BOUCLE | HIPPO | **7 s** | 5 000 – 9 000 |
| T2 | HIPPO | RECON | **16 s** | 14 000 – 18 000 |
| T3 | RECON | CORTEX | **13 s** | 10 000 – 16 000 |
| | | **Total** | **~50 s** | 41 000 – 59 000 |

→ Temps **le plus long** sur **RECON** (recomposition) puis **CORTEX final** (clarté / parole). HIPPO = passage rapide.

#### Cycles 2+ — ~2 min, ordre libre, fin CORTEX

| Règle | Détail |
|-------|--------|
| **Durée cible** | **~120 s** (plus abstrait, plus respirant) |
| **Ordre intermédiaire** | **Libre** — HIPPO, RECON, BOUCLE, CORTEX dans un ordre variable |
| **Contrainte** | **Fin obligatoire sur CORTEX** (clarté) |
| **BOUCLE en tête** | **Non** requis (sauf reset 7 min) |
| **Variantes** | Pools §15.6 — plus de diversité spat/FX |

Exemple cycle 2 :

```text
HIPPO ──► RECON ──► BOUCLE ──► CORTEX   (~2 min, atterrissage clarté)
```

#### Reset à 7 minutes

Chronomètre session AUTO : à **420 s**, **forcer** un nouveau **cycle 1** complet :

```text
BOUCLE → HIPPO → RECON → CORTEX
```

→ Retour à la strate profonde puis remontée complète.

#### Transitions liées au contenu et à la sortie (Q16)

Le timer **seul** ne déclenche pas la transition. Conditions de passage :

1. **Fin de fichier** / fin de segment joué (ou fenêtre de silence détectée dans le fichier) ;
2. **Queue audio de sortie** : attendre la **fin de la répétition delay/FLUID/reverb** — et **laisser la queue résonner** lors du changement de couche/état même si le FX est coupé sur la destination (Q47) ;
3. **Plafond max** de la plage (ex. ne pas dépasser 18 s en RECON cycle 1) ;
4. `timer_min` atteint + conditions contenu (§16.3) ;
5. **Silence de transition** : **aucun** — coupure max **100 ms** ;
6. **Fondu inter-état** : **0 ms** par défaut ; **700 ms** si la variante de transition l’active (Q19–20) ;
7. **Matériau** : **ne pas relancer** `open` sauf switch rare (Q18).
6. **Fondu inter-état** : **0 ms** par défaut ; **700 ms** si la variante de transition le prévoit (Q19–20).

```text
timer_min atteint ──┐
fin fichier ────────┼──► AND/OR logique ──► transition si conditions OK
queue FX vide ──────┘
```

#### FSM_AUTO — toggles (Q9–Q10)

| Événement | Comportement |
|-----------|--------------|
| **loadbang** | `FSM_AUTO = 1`, démarre cycle 1 |
| **AUTO → off** | Reste sur **état courant** ; **FORCE_ETAT** actif |
| **AUTO → on** (re-clic) | FSM **reprend** (pas réservé au boot) |

#### Silence (Q7)

**Pas** de silence programmé entre états. Si gap technique : **≤ 100 ms**.

#### Interaction micro (Q8 — proto 05 léger)

- Toggle **`INPUT_ON`** (optionnel) ;
- **1 entrée audio** → détection seuil → **triggers** (changement variante, bump FSM, etc.) ;
- **Risque larsen** : micro dynamique + 4 HP en quadri — à tester avec garde-fous (seuil, mute sortie pendant capture courte).

#### Comportement actuel à remplacer (`fsm_memory.pd`)

| Actuel | Cible |
|--------|-------|
| `DELAY` fixe + `random 4` | Cycle 1 séquentiel + cycles 2+ libres (fin CORTEX) + reset 7 min |
| Timer seul | **Contenu + queue FX** + bornes min/max |

| État | DELAY actuel (ms) | Problème |
|------|-------------------|----------|
| BOUCLE | 60 000 | 4× trop long pour cycle 1 |
| HIPPO | 90 000 | Idem |
| CORTEX | 45 000 | Idem |
| RECON | 180 000 | Idem |

#### Médiation (Q2)

- **Panneau** en salle : entrée narrative (mémoire, strates, écoute).
- Son : **poétique mais lisible** — cycle 1 = démonstration complète en ~50 s.

### 16.4 Principe général : moins de rythme, plus de respiration

Problème transversal signalé sur **tous** les effets temporels :

- sauts spatiaux trop rapides (ex. `jump_ms = 400` en CORTEX, `2000` en BOUCLE mais métronome fixe) ;
- rotation, delay, transitions FSM : sensation de **tempo constant** plutôt que de **présence variable**.

**Décision produit :** remplacer les temporisations **fixes** par des **plages de durées** rééchantillonnées à chaque événement (saut HP, fin de timer FSM, etc.).

Ce n’est pas du « hasard pur » pour le plaisir : c’est une **variabilité contrôlée dans des bornes** définies par état — parfois court, parfois long, sans que l’auditeur puisse prédire le prochain intervalle exact.

### 16.5 Sauts spatiaux (SPAT 2 et 3) — intervalles variables

#### Comportement actuel (technique)

`spatial_jump.pd` et `spatial_stepseq.pd` utilisent un **`metro` à intervalle fixe** (`jump_ms` unique). Chaque saut arrive donc au même rythme — d’où l’impression de métronome, surtout en BOUCLE au démarrage (mode saut, `jump_ms = 2000`).

#### Comportement cible (acté)

À chaque saut vers un nouveau HP :

1. le sample **reste audible** sur le baffle courant pendant une durée **variable** ;
2. à la fin de cette durée → saut (éventuellement avec fondu `jump_xfade`) ;
3. la **prochaine** durée est tirée dans une **plage** propre à l’état FSM.

**Exemple narratif (BOUCLE / saut) — donné par Loumana :**

| Séjour sur un HP | Durée avant saut |
|------------------|------------------|
| HP1 (1er sample) | ~**2 s** |
| HP2 | ~**10 s** |
| HP3 | ~**3 s** |
| HP suivant | … dans la plage |

→ Pas une valeur unique : une **succession de durées différentes**, toutes dans une enveloppe min–max.

#### Modèle de paramètres (à implémenter)

Remplacer le couple fixe `jump_ms` par **deux bornes par état** :

| Paramètre | Rôle |
|-----------|------|
| `jump_min_ms` | Durée minimale de séjour sur un HP |
| `jump_max_ms` | Durée maximale de séjour sur un HP |

À chaque saut : `prochain_intervalle = échantillon dans [jump_min_ms, jump_max_ms]`.

**Note :** « échantillon dans une plage » peut être :

- tirage uniforme `random(min, max)` ;
- ou distribution biaisée (ex. plus de séjours longs en BOUCLE, plus de courts en CORTEX) ;
- ou petite table de durées prédéfinies mélangées.

→ Ce n’est **pas** obligatoirement de l’aléatoire pur : c’est une **plage de possibilités** validée artistiquement par état.

#### Plages proposées (première cible — à affiner en écoute)

| État | SPAT saut | `jump_min_ms` | `jump_max_ms` | Intention |
|------|-----------|---------------|---------------|-----------|
| **BOUCLE (3)** | 2 ou 3 | **2000** | **12000** | Obsession lente ; séjours longs possibles (ex. 10 s) |
| **CORTEX (0)** | 2 | **1500** | **6000** | Plus nerveux que BOUCLE, mais plus de 400 ms fixe |
| **HIPPOCAMPE (1)** | 1 ou 3 | rotation lente **ou** séquence `[3000, 10000]` | Association, respiration |
| **RECONSTRUCTION (2)** | 0 ou 1 | phi / rotation très lente | Immersion, peu de sauts |

**Valeurs actuelles à abandonner comme défaut unique :** CORTEX `400 ms`, BOUCLE `2000 ms` fixe.

#### Impact code

| Fichier | Changement |
|---------|------------|
| `pd/lib/spatial_jump.pd` | `metro` réinitialisé après chaque saut avec nouvelle durée ∈ `[min, max]` |
| `pd/lib/spatial_stepseq.pd` | Tables **patterns P1–P7** (trajectoires non linéaires + repos oscillant) ; intervalles variables |
| `scripts/gen_prototype_05.py` | presets par état : `jump_min`, `jump_max` au lieu d’un seul `jump_ms` |
| UI SPAT | afficher min/max (debug) ou masquer en installation |

### 16.6 Cartographie narrative des 4 états (référence artistique)

| État | Archétype | Spatial cible | FX cible | Couches | Rythme cycle 1 |
|------|-----------|---------------|----------|---------|----------------|
| **BOUCLE** | Obsession, strate profonde (**entrée**) | Saut lent, intervalles variables | Delay variable | 1 | ~14 s |
| **HIPPOCAMPE** | Dialogue de fragments | Interlocuteurs opposés ; **mouvement relatif** (F1) | FX par couche | 2–3 | ~7 s |
| **RECONSTRUCTION** | Mémoire recomposée | Phi lent, aller-retour ±180° | Delay décalé dynamique | 1–2 | ~16 s |
| **CORTEX** | Parole, clarté (**phase finale**) | Superposition brève, mêmes baffles | Pas de delay — filtre+LFO | 1–2 | ~13 s |

### 16.7 Synthèse implémentation — **proto 06** (checklist)

> Proto **05 figé** (N.8). Tous les items ci-dessous → `prototype_06_fsm_4hp.pd` / `_6hp.pd`.

- [ ] Créer `scripts/gen_prototype_06.py` + `launch_prototype_06.sh` (base 05, routage neuf)
- [ ] **Mapping HP fixe** par slot lecteur (N.1) : couche1→HP1, couche2→HP3, couche3→HP4
- [ ] `SENS` par couche **variable** par variante (N.2)
- [ ] SPAT mixte saut+rotation même variante (N.3)
- [ ] CORTEX : **délai** avant 1ère superposition (N.6)
- [ ] `FSM_AUTO` toggle initial = **1**
- [ ] `fsm_memory` état initial = **3 (BOUCLE)** + bang preset au load
- [ ] Relier démarrage à **AUDIO_ON** ou loadbang (déclencher lecture + timer auto)
- [ ] **Patterns spatiaux** P1–P7 dans `spatial_stepseq` + poids `fsm_presets` (F.0.2)
- [ ] Durées FSM : cycle 1 séquentiel + cycles 2+ (fin CORTEX) + **reset 7 min** + **sync contenu/queue FX**
- [ ] **`variante_id`** + **`CONTRASTE`** (défaut HAUT) dans UI FSM (Q24–25)
- [ ] AUTO off → **stop/reset** timer ; FORCE sans `open` fichier (Q26–27)
- [ ] **CORTEX** : `delay_on=0`, module **filtre+LFO** (proto 07)
- [ ] **FORCE re-clic** : re-tirage variante même si état inchangé
- [ ] **Multi-bus** : 3× FX + 3× encode → **1× decode_4hp** ; jump HP hybride (Q49 Option B)
- [ ] **`SPAT_LAYOUT`** debug : AUTO \| SÉPARATION \| SUPERPOSITION \| **UNISON** — actif si `FSM_AUTO = 0` (Q48–50)
- [ ] **UNISON** + règles densité 3 couches (delay ↓, mute précoce) dans `fsm_presets` (Q50)
- [ ] Recalibrer presets BOUCLE / HIPPO (wet/fb) — §15.4
- [ ] **BOUCLE** : SPAT saut/séquence **50/50** (H4) ; macro **clarté → sat/phase → delay** (H5)
- [ ] **Modes SPAT par état** (I1) : pools `spat_mode` + `spat_mode_flash` HIPPO/CORTEX

---

## 17. Roadmap effets — au-delà du delay (proto 05 → 07)

### 17.1 Renommage

| Ancien | Nouveau (UI) | Notes |
|--------|--------------|-------|
| `FLUID_FX` | **ECHO** | Reflète le comportement réel (`fx_fluid` = delay + feedback + LFO sur le temps) — J1 |

### 17.2 Banque FX cible (nouvelle rangée, proto 07 ou 05b)

| Module | Rôle artistique | Paramètres envisagés |
|--------|-----------------|----------------------|
| **Phaser** | Mouvement spectral, « souvenir qui ondule » | rate, depth, feedback, mix |
| **Filtre + LFO** | Respiration timbrale, masque/franchissement | cutoff, résonance, vitesse LFO, forme (sin/tri) |
| **Saturation douce** | Corps, présence, fatigue mémorielle | drive, **soft clip**, atténuation **highs**, **gain de compensation** |

Chaîne saturation (J7 — acté) :

```text
in~ → drive / sat_wet → softclip~ → *~ gain_comp → out~
                         gain_comp = 1 / (1 + sat_amount × 1.5)
                         sat_amount = f(drive, dry/wet entrée)
```

→ Atténuation highs optionnelle en complément — pas de valeur fixe en dB (compensation **dynamique**).

### 17.3 Routage par état FSM (vision)

Chaque état active un **preset FX complet** via une **variante** du pool (§15.6), pas une ligne unique :

| État | Delay/Echo | Phaser | Filtre LFO | Saturation |
|------|------------|--------|------------|------------|
| **CORTEX** | **off** | off / subtil (var.) | **on** (principal) | **off** principal ; possible superposé (J6) |
| **HIPPOCAMPE** | dynamique (F4) | **50/50** vs filtre+LFO (F5) | **50/50** vs phaser (F5) | **modérée** principal ; superposés oui (J6) |
| **RECONSTRUCTION** | dynamique, **décalé** (G4) ; **wet/fb bas** (G5) | modéré | moins qu’HIPPO | **off** principal ; superposés oui (J6) |
| **BOUCLE** | variable (**plafond** H3) | off / dynam. (H5) | **plus filtré** (flou dense) | **prédominante** principal (H5, J6) ; superposés oui |

### 17.4 Ordre de prototypage FX (J8 — acté)

| Étape | Module | Proto |
|-------|--------|-------|
| **1** | **Saturation** (+ compensation ×1,5, J7) | 07 |
| **2** | **Filtre** HPF/LPF (J4) | 07 |
| **3** | **LFO** (filtre + ECHO existant, J5) | 07 |
| **4** | **Phaser** (F5) | 07 |

**Proto 05** (parallèle, inchangé) :

1. Recalibrer presets ECHO (wet/fb bas) + `rot_speed` 0.01
2. Documenter + ajuster rythme FSM AUTO
3. Intégration presets par état dans la FSM — **proto 07 → FINAL**

Patches test suggérés (dans l’ordre J8) : `_test_saturation.pd` → `_test_filter.pd` → `_test_lfo.pd` → `_test_phaser.pd`

---

## 18. Prochaine étape documentaire / technique

- [x] Loumana précise démarrage AUTO + BOUCLE + sauts variables (§16)
- [x] Variantes par état + CORTEX sans delay + filtre LFO (§15.6–15.7)
- [x] Multi-couches : séparation HIPPO/RECON vs superposition brève CORTEX (§15.8)
- [x] Liste Q&A ouverte → [`09_qa_prototype_05.md`](./09_qa_prototype_05.md)
- [x] Créer `docs/08_grille_contenu_sons.md`
- [ ] Implémenter §16.7 (AUTO on, état 3, sauts min/max, variantes)
- [ ] `gen_fsm_presets.py` + `fsm_presets.pd` (pools par état)
- [ ] CORTEX : couper delay immédiatement dans `gen_prototype_05.py` (quick win)
- [ ] Mettre à jour les presets selon §15.4
- [ ] Renommer FLUID → **ECHO** dans l’UI (J1)
- [ ] Plages variables pour timers FSM auto
- [ ] Patches test (ordre J8) : `_test_saturation.pd` → `_test_filter.pd` → `_test_lfo.pd` → `_test_phaser.pd`
