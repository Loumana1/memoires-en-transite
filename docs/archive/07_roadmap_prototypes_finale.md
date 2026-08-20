# Roadmap — Prototypes 05 à 08 et version finale

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Statut :** document de référence pour l’organisation du projet jusqu’à l’installation finale.  
**Expositions :** 11 sept. 2026 — Centre Wallonie-Bruxelles, Paris (24 h) · nov. 2026 — Bozar / MBA, Bruxelles (5 jours)

> **Mise à jour 16 août 2026 :** le **Proto 07** n’est plus « piezo d’abord ». C’est la conceptualisation des **quatre modes de traitement** (Cortex / Hippo / Recon / Boucle-buffer), le recalibrage des cycles et couches, et l’intégration de `Opacité fin V2/` (~26 min × 4). Le piezo redevient un **modulateur** (vague 8). Voir [`etatactuel.md`](../etatactuel.md) et [`log.md`](../log.md). Intention 16 août : [`backlog/14_prototype_07_synthese_backlog.md`](../backlog/14_prototype_07_synthese_backlog.md), [`15_prototype_07_qa_createur.md`](./15_prototype_07_qa_createur.md). Le Proto **06 8HP** est figé ; l’écoute courante est le **07**.

---

## 1. Vue d’ensemble

> **Mise à jour 9 juil. 2026 (L.1) :** le **proto 05 est figé** (état actuel). L’implémentation complète FSM/FX/multi-bus = **proto 06** (4 HP + 6 HP). L’ancien proto 06 (piezo) → **proto 07**, etc.

```text
PROTO 01 ──► spatial 4 HP (base ambisonie)
PROTO 02 ──► lecteur minimal (debug I/O)
PROTO 03 ──► ABANDONNÉ
PROTO 04 ──► SPAT + FLUID + 4 HP  ✅ RÉALISÉ
PROTO 05 ──► FSM squelette + SONS/   ✅ FIGÉ (ne pas étendre)
     │
     ▼
PROTO 06 ──► FSM complète + multi-bus + FX + presets  ← EN COURS (Q&A)
             ├── prototype_06_fsm_4hp.pd  (test 4 HP)
             └── prototype_06_fsm_6hp.pd  (test 6 HP, sorties 1-2-4-5-6)
PROTO 07 ──► Interaction (piezo + micro) → modifie FSM   (ex-proto 06)
PROTO 08 ──► Banque FX modulaire (comportements figés)   (ex-proto 07)
PROTO 09 ──► 12 HP + calibration salle                    (ex-proto 08)
FINAL    ──► Pi 5 headless + mémoire vivante + déploiement
```

Chaque prototype **ajoute une couche**, ne refait pas les précédentes, et suit la discipline du proto 04 :

- patch test isolé par abstraction ;
- test console `scripts/test_patch_console.sh` ;
- générateur Python pour les `#X connect` si le patch dépasse ~50 objets ;
- **pas de passage à l’étape suivante** tant que la console n’est pas propre et le comportement audible.

---

## 2. Calendrier indicatif (juil. → sept. 2026)

| Période | Prototype | Jalons |
|---------|-----------|--------|
| **9–20 juil.** | **06 — FSM complète** | Q&A implémentée, 4 HP (auj.) + 6 HP (samedi), presets intensité |
| **11–25 juil.** | **07 — Interaction** | Piezo (réception ~11–12 juil.), analyse RMS, FSM perturbée |
| **20 juil. – 10 août** | **08 — FX bank** | Saturation, filtre, LFO, phaser (ordre J8) |
| **10–25 août** | **09 — 12 HP** | Interface multi-sorties, calibration |
| **25 août – 10 sept.** | **FINAL** | Raspberry Pi, mémoire vivante, contenu archives, tests stress, Paris in situ |
| **Nov. 2026** | **Redéploiement** | Bozar — plug & play, recalibration légère |

Ce calendrier est **serré** (2 mois avant Paris). Priorité absolue : **proto 06** (4 HP) puis 6 HP samedi ; proto 07 dès réception du piezo.

---

## 3. Prototype 05 — FSM squelette (FIGÉ)

→ **[`06_prototype_05_plan.md`](./06_prototype_05_plan.md)** — brief d’origine.

| | |
|--|--|
| **Statut** | **Figé** — `prototype_05_fsm.pd` tel quel ; pas d’extension |
| **Objectif atteint** | Preuve FSM + 3 lecteurs + presets basiques |
| **Suite** | Toute évolution → **proto 06** |

---

## 4. Prototype 06 — FSM complète (EN COURS)

| | |
|--|--|
| **Objectif** | Implémenter le Q&A `09_qa_prototype_05.md` : multi-bus, variantes, ECHO, presets, SPAT par état |
| **4 HP** | `prototype_06_fsm_4hp.pd` — `dac~ 1 2 3 4` — test **aujourd’hui** |
| **6 HP** | `prototype_06_fsm_6hp.pd` — `dac~ 1 2 4 5 6` — test **samedi** |
| **Gain master** | `*~ 0.65` — validé (L3) |
| **Console** | Zéro error, zéro warning (L6) |
| **Presets** | Banque intensité / présentation (L5) |
| **Mapping HP** | **Fixe** par slot (N.1) ; `SENS` variable par variante (N.2) |
| **CORTEX** | Délai avant 1ère superposition (N.6) |

---

## 5. Prototype 07 — Interaction & captation (ex-proto 06)

### 5.1 Objectif

Le public (ou l’artiste en studio) **perturbe** la FSM sans interface visible en exposition. La présence acoustique modifie les probabilités de transition et l’intensité des états.

### 5.2 Entrées audio

| Source | Priorité | Notes |
|--------|----------|-------|
| **Piezo** (contact / structure) | **Principale** | Attendu ~11–12 juil. 2026 ; faible risque de larsen |
| **Micro studio** (omni/cardioïde) | Secondaire / debug | **Risque larsen** en studio → entrée avec high-pass, seuil, **pas de monitoring direct** vers les HP ; gain très bas |
| **Simulateur** (slider `rms_sim`) | Dev sans micro | Pour coder avant réception piezo |

### 5.3 Traitement signal

Abstraction `pd/lib/analyze_presence.pd` :

- `adc~` ou entrée interface (canal dédié) ;
- envelope follower → RMS lissé ;
- détection transitoires (seuil + cooldown) ;
- sorties : `rms` (0–1), `bang_transient`, `presence` (0/1 hysteresis).

**Anti-larsen studio :**

- HPF 80–120 Hz sur entrée micro ;
- pas de routage `adc~` → `dac~` direct ;
- gate : analyse seulement, pas de réinjection du micro dans le mix HP ;
- niveau d’entrée Pd : -20 dB ou moins en test studio.

### 5.4 Couplage FSM

| Signal | Effet sur FSM |
|--------|----------------|
| RMS bas (silence) | Favorise BOUCLE / HIPPOCAMPE (introspection) |
| RMS moyen | État courant prolongé |
| RMS haut / transitoire | Favorise CORTEX / RECONSTRUCTION (afflux) |
| Transitoire fort | Bang → transition forcée ou reset timer |

Matrice de transition **modulée** : `proba_effective = proba_base × facteur_presence`.

### 5.5 Mode studio vs mode expo

- Toggle `INPUT_MODE` : OFF (proto 06 pur) / PIEZO / MICRO / SIM.
- En expo : piezo seul, pas de micro studio.

### 5.6 Livrables proto 07

- `pd/prototype_07_interaction.pd` (= proto 06 + couche analyse)
- `pd/lib/analyze_presence.pd`
- `pd/_test_piezo.pd` — piezo → RMS → print (sans HP)
- `pd/_test_analyze_presence.pd` — seuils réglables
- Doc : réglages anti-larsen, branchement piezo (préampli ? interface entrée ?)

### 5.7 Piezo — préparation dès réception (11–12 juil.)

Checklist jour J :

1. Brancher piezo sur entrée interface (laquelle ?) — noter le canal dans la doc.
2. Lancer `_test_piezo.pd` : taper/frapper près du capteur → voir RMS monter.
3. Régler seuil `presence` sans déclencher sur bruit de fond.
4. Intégrer dans proto 07 seulement après test isolé propre.

---

## 6. Prototype 08 — Banque FX modulaire (ex-proto 07)

### 6.1 Objectif

Enrichir l’identité sonore de chaque état avec des **modules d’effets à comportement figé** — plus spécifiques que le seul `fx_fluid` du proto 04. Chaque module = 1 abstraction testée isolément, puis intégrée via **sends** (pas de générate aléatoire d’effets).

### 6.2 Philosophie « module figé »

Comme `spatial_jump.pd` a été réécrit en proto 04 : chaque FX a un **contrat d’entrées/sorties** stable, un patch `_test_*.pd`, et une validation console avant intégration.

```text
[Lecteur] ──► [dry bus] ──► spatial ──► dac~
                  │
                  ├── send A ──► [fx_distort]  ──┐
                  ├── send B ──► [fx_granular] ──┼──► retour mix
                  └── send C ──► [fx_fluid]    ──┘
```

Les **niveaux de send** et **quels modules actifs** dépendent de l’état FSM (table dans `fsm_presets` étendue).

### 6.3 Modules prévus (liste de travail)

| Module | Fichier | Rôle artistique | États prioritaires |
|--------|---------|-----------------|-------------------|
| FLUID (existant) | `fx_fluid.pd` | Délai modulé, mémoire liquide | HIPPOCAMPE, RECONSTRUCTION |
| DISTORT | `fx_distort.pd` | Saturation, bitcrush léger | CORTEX |
| FILTER | `fx_filter.pd` | LPF/HPF modulés, « lointain » | BOUCLE, RECONSTRUCTION |
| GRAIN | `fx_grain.pd` | Micro-boucles, stutter | CORTEX, HIPPOCAMPE |
| RING | `fx_ring.pd` | Ring mod, métallique | RECONSTRUCTION |
| SPACE | `fx_space.pd` | Réverb très courte (HP feed) | Tous (send faible) |

**Ordre d’implémentation (J8) :** saturation → filtre → LFO → phaser.

### 6.4 Règles d’intégration

1. Un module à la fois : `_test_fx_xxx.pd` → console propre → intégration.
2. Bypass total (`enable=0`) = signal sec bit-identique au dry.
3. Pas plus de **3 sends actifs** simultanés (charge CPU / lisibilité).
4. Gain staging : sends à -6 dB par défaut, somme des retours ≤ 0 dB.

### 6.5 Livrables proto 08

- `pd/prototype_08_fxbank.pd`
- `pd/lib/fx_*.pd` (nouveaux modules)
- `pd/lib/fx_router.pd` — sends/returns par état FSM
- Patches test un par module
- Extension `fsm_presets.pd` : colonnes `send_distort`, `send_filter`, etc.

---

## 7. Prototype 09 — 12 haut-parleurs & calibration (ex-proto 08)

### 7.1 Objectif

Passer de 4–6 HP de dev à **12 baffles** (cible installation Paris + Bruxelles). Calibration géométrique et test de stress longue durée.

### 7.2 Choix technique spatialisation 12 HP

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **A — `decode_12hp` custom** (matrice fixe `mtx_*~`) | Cohérent avec proto 01–05, contrôle total | Matrice à calculer selon géométrie salle |
| **B — `iem_ambi` ordre supérieur** | Plus précis 3D | Plus lourd, calibration complexe |
| **C — VBAP** (`vbap` / pd-iem) | Bon pour orbites localisées | Moins « masse ambisonique » |
| **D — `pd-acre-amb`** | Abstractions haut niveau | Dépendance supplémentaire |

**Décision recommandée :** commencer par **A** (même pattern que `decode_4hp.pd`), angles `real_ls` mesurés in situ. VBAP en fallback si la salle impose une géométrie irrégulière.

### 7.3 Matériel cible

- Interface USB class-compliant 12+ sorties (Focusrite 18i20 + ADAT ou équivalent budget 500–1000 €).
- 12 baffles actifs (fournis / loués par la salle).
- Carte son déjà en test 4 sorties → identifier le modèle 12 sorties avant proto 09.

### 7.4 Multi-couche sur 12 HP

- Jusqu’à **4–6 sources simultanées** (état RECONSTRUCTION) avec phi / HP distincts.
- Limite CPU : profiler sur Mac avant migration Pi.

### 7.5 Calibration

1. Test tonal : 1 kHz sur chaque `dac~` channel → vérifier HP physique.
2. Documenter mapping `dac~ N` → position salle → `docs/09_calibration_salle.md`.
3. Ajuster matrice decode ou angles VBAP.
4. Test 1 h continu sans crash Pd.

### 7.6 Livrables proto 09

- `pd/lib/decode_12hp.pd`
- `pd/prototype_09_12hp.pd` (= proto 08 + decode 12)
- `docs/09_calibration_salle_CWB.md` (Paris) — version Bruxelles en nov.
- Script test tonal `pd/_test_hp_tonal.pd`

---

## 7. Version finale — Installation « Mémoires en transit »

### 7.1 Objectif

Patch **autonome**, déployable en 24 h (Paris) puis 5 jours (Bruxelles), sans ordinateur personnel, résistant aux coupures de courant.

### 7.2 Composants (tous les prototypes réunis)

| Couche | Source |
|--------|--------|
| FSM 4 états + presets | Proto 05 |
| Interaction piezo | Proto 06 |
| Banque FX + sends | Proto 07 |
| 12 HP spatialisé | Proto 08 |
| Mémoire vivante | **Nouveau** (final uniquement) |
| Raspberry Pi 5 headless | **Nouveau** |
| Contenu `SONS/` définitif | Production parallèle (archives, terrain) |

### 7.3 Mémoire vivante (scope final)

- `writesf~` périodique (ex. toutes les 60–120 s si `presence` ou aléatoire lent).
- Capture : mix sortie système + optionnel piezo (pas micro salle en expo).
- Découpe automatique en segments COURT → `SONS/MEMOIRE_VIVANTE/COURT/`.
- Réinjection : FSM peut piocher dans `MEMOIRE_VIVANTE` avec probabilité faible (état HIPPOCAMPE / BOUCLE).

### 7.4 Raspberry Pi 5

- Pd `-nogui` au boot (`systemd` ou `crontab @reboot`).
- Même patch que Mac, paths relatifs MET_ROOT.
- Libs `iem_ambi` / `iemmatrix` compilées ARM64.
- Tests : coupure courant → reprise auto ; 24 h continu ; température CPU.

### 7.5 Contenu sonore définitif

Hors scope technique des prototypes — production en parallèle :

- Field recordings, archives Quai Branly, BnF, témoignages.
- Classification dans `SONS/<ETAT>/<DUREE>/` selon `08_grille_contenu_sons.md`.
- Remplacement progressif des placeholders.

### 7.6 Livrables finaux

- `pd/memoires_en_transit.pd` (nom final du patch principal)
- `scripts/launch_installation.sh` (Pi)
- `scripts/deploy_pi.sh`
- `docs/10_guide_exploitation.md` (allumer, calibrer, dépanner)
- `SONS/` complet + `MEMOIRE_VIVANTE/`

---

## 8. Matrice des prototypes

| # | Nom | Cerveau | Spatial | FX | Entrées | HP | Machine |
|---|-----|---------|---------|-----|---------|-----|---------|
| 04 ✅ | effects | — | SPAT×3 | FLUID | — | 4 | Mac |
| **05** | **fsm** | **FSM** | presets | presets | — | 4 (+6) | Mac |
| 06 | interaction | FSM+presence | idem | idem | piezo/micro | 4–6 | Mac |
| 07 | fxbank | idem | idem | **+bank** | idem | 4–6 | Mac |
| 08 | 12hp | idem | **12 HP** | idem | idem | **12** | Mac |
| **FINAL** | installation | idem | 12 HP calibré | bank | piezo | 12 | **Pi 5** |

---

## 9. Arborescence dépôt cible (fin de projet)

```text
memoires-en-transit/
├── docs/
│   ├── 06_prototype_05_plan.md
│   ├── 07_roadmap_prototypes_finale.md    ← ce fichier
│   ├── 08_grille_contenu_sons.md          ← session classification
│   └── 09_calibration_salle_*.md
├── pd/
│   ├── prototype_04_effects.pd            ✅
│   ├── prototype_05_fsm.pd
│   ├── prototype_06_interaction.pd
│   ├── prototype_07_fxbank.pd
│   ├── prototype_08_12hp.pd
│   ├── memoires_en_transit.pd             ← final
│   └── lib/
│       ├── fsm_*.pd, player_state.pd
│       ├── analyze_presence.pd
│       ├── fx_*.pd, fx_router.pd
│       └── decode_4hp/6hp/12hp.pd
├── SONS/                                  ← contenu classé
├── SONS_PROTOTYPE/                        ← dev / archives tests
└── scripts/
    ├── gen_prototype_05.py …
    ├── slice_extracts.sh
    ├── test_patch_console.sh
    └── deploy_pi.sh
```

---

## 10. Principes d’organisation (tous prototypes)

1. **Une couche à la fois** — pas de proto « fourre-tout ».
2. **Test isolé avant intégration** — chaque abstraction a son `_test_*.pd`.
3. **Console propre = critère bloquant** — `test_patch_console.sh`.
4. **Générateur Python** pour les gros patches — éviter le piège du proto 03.
5. **Comportements figés** — paramètres oui, architecture non ; chaque module a un contrat stable.
6. **Contenu et code en parallèle** — la FSM ne attend pas les archives définitives.
7. **Documentation avant code** — lire le plan du proto N en entier avant d’implémenter.

---

## 11. Prochaines actions immédiates

| # | Action | Qui / quand |
|---|--------|-------------|
| 1 | Valider ce document + [`06_prototype_05_plan.md`](./06_prototype_05_plan.md) | Maintenant |
| 2 | Session classification 3–4 extraits réels → `08_grille_contenu_sons.md` | Avant fin proto 05 |
| 3 | Créer arborescence `SONS/` + `slice_extracts.sh` | Début proto 05 |
| 4 | Coder proto 05 étape par étape (§8 du plan 05) | 9–20 juil. |
| 5 | Réception piezo → `_test_piezo.pd` | ~11–12 juil. |
| 6 | Identifier interface 12 sorties (budget / location) | Avant 10 août |

---

## 12. Résumé

**Le projet avance en 4 prototypes structurés après le 04 : le cerveau (05), l’écoute du public (06), la palette sonore (07), l’espace d’exposition (08), puis l’installation autonome (final). Paris en septembre = 12 HP + FSM + interaction piezo + FX — le Pi et la mémoire vivante bouclent le système pour la durée et l’autonomie.**
