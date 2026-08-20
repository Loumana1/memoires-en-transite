# Prototype 01 — Décisions confirmées & plan de réalisation

**Projet :** Mémoires en transit  
**Date :** 7 juillet 2026  
**Objectif du jour :** premier patch Pure Data fonctionnel — 4 baffles, ambisonie, fichiers audio de test.

---

## 1. Ce qui est confirmé (suite à relecture du dépôt)

### Concept (inchangé)
- Installation sonore immersive sur mémoire coloniale, archives et field recordings.
- Le médium n'est pas le fichier audio seul, mais **leur circulation algorithmique et spatiale**.
- 4 dynamiques mémorielles cible : **Cortex / Hippocampe / Reconstruction / Boucle**.
- Interaction future : présence du public comme **interférence involontaire** (micros + RMS/transitoires).

### Expositions (inchangé)
| Date | Lieu | Durée |
|------|------|-------|
| 11 sept. 2026 | Centre Wallonie-Bruxelles, Paris | 24 h |
| Nov. 2026 | Bozar / MBA, Bruxelles | 5 jours continus |

### Cible finale (installation — pas le prototype d'aujourd'hui)
| Élément | Choix confirmé |
|---------|----------------|
| Logiciel | **Pure Data** (Pd) |
| Machine | **Raspberry Pi 5** (headless en expo) |
| Sorties audio | **12 baffles** via interface USB class-compliant (ex. Focusrite 18i20 + ADAT) |
| Spatialisation | **Ambisonie** via **`iem_ambi`** (IEM Graz) |
| Algorithme | Machine à états probabiliste + lecteurs `readsf~` sur arborescence `SONS/` |
| Mémoire vivante | Enregistrement automatique vers `MEMOIRE_VIVANTE/` (phase ultérieure) |

### Arborescence audio cible (finale)
```text
SONS/
├── CORTEX/       (LONG/ MOYEN/ COURT/)
├── HIPPOCAMPE/   (LONG/ MOYEN/ COURT/)
├── RECONSTRUCTION/ (LONG/ MOYEN/ COURT/)
├── BOUCLE/       (LONG/ MOYEN/ COURT/)
└── MEMOIRE_VIVANTE/
```

### Ressources déjà dans le dépôt
| Fichier | Rôle |
|---------|------|
| `ressources :outils /iem_ambi-master.zip` | Bibliothèque externe Pd — encode/decode/rotate ambisonique (base technique) |
| `ressources :outils /pd-acre-amb-master.zip` | Abstractions de plus haut niveau (ACRE amb), **construites sur `iem_ambi`** — utile plus tard, pas indispensable pour le proto 01 |
| `docs/01_premiere_recherche.md` | Archive de la première exploration (Pd vs SuperCollider, Raspberry Pi, routing) |
| `Document_de_travail_evolutif.md` | Document collaboratif concept + technique (Simon / Alassane) |
| `Document_Technique_Definitif.md` | Cahier des charges technique d'avril 2026 |

### Clarification importante : IEM, pas « LIRCAP »
Les zips présents correspondent à l'écosystème **IEM** (Institut d'Électroacoustique de Graz) :
- **`iem_ambi`** : objets natifs compilés (`ambi_encode`, `ambi_decode3`, `ambi_rot`, etc.)
- **`pd-acre-amb`** : couches d'abstraction Pd pure (pas d'externals supplémentaires) pour prototyper plus vite

Si tu pensais à **IRCAM** (Spat, VBAP), ce n'est pas ce qui est dans le dépôt — mais `iem_ambi` couvre le même besoin (spatialisation 3D/2D open-source).

### Clarification IRCAM vs IEM

Tu vises l'écosystème **IRCAM** (Spat, VBAP) conceptuellement. Dans Pure Data, l'équivalent open-source est **`iem_ambi`** (IEM Graz) — c'est ce qui est installé. Voir [`03_first_setup.md`](./03_first_setup.md) pour le guide complet.

### Décision actée pour le prototype 01 (aujourd'hui)
| Élément | Proto 01 | Installation finale |
|---------|----------|---------------------|
| Machine | **Mac de dev** (ton ordi) | Raspberry Pi 5 |
| Baffles | **4** (carré ou rectangle) | 12 |
| Audio | **Fichiers de test** (hors narratif colonial) | Archives Quai Branly, BnF, terrain |
| Spatialisation | **`iem_ambi`** ordre 1, 2D | `iem_ambi` ordre supérieur + calibration salle |
| FSM / micros / mémoire vivante | **Hors scope** | Oui |
| `pd-acre-amb` | Optionnel (phase 2) | Peut simplifier le patch 12 HP |

---

## 2. Plan de réalisation — Prototype 01 (quelques heures)

### Phase A — Environnement (≈ 30–45 min)

1. **Installer Pure Data**
   - macOS : [https://puredata.info/downloads](https://puredata.info/downloads) — version **0.54** ou dernière stable.
   - Au premier lancement : *Pd → Preferences → Audio* → choisir ta carte son (interface ou sortie intégrée).

2. **Extraire et installer `iem_ambi`**
   ```bash
   cd "ressources :outils "
   unzip -o iem_ambi-master.zip -d ../pd/externals/
   ```
   - Compiler sur Mac (nécessite Xcode Command Line Tools) :
     ```bash
     cd pd/externals/iem_ambi-master
     make
     ```
   - Ajouter dans Pd : *File → Preferences → Path… → New…* → pointer vers `pd/externals/iem_ambi-master`
   - *File → Preferences → Startup… → New…* → `-lib iem_ambi`

3. **Vérifier l'installation**
   - Ouvrir `iem_ambi-master/Ambisonic_2d_example.pd` — doit produire du son sur les sorties.

### Phase B — Audio de test (≈ 15 min)

4. **Placer les fichiers prototype** dans `SONS_PROTOTYPE/` (à la racine du repo).
   - Format recommandé : **WAV**, 44.1 ou 48 kHz, mono ou stéréo.
   - Nommage libre pour l'instant ; le proto lira un dossier fixe.

### Phase C — Patch spatial 4 baffles (≈ 1h30–2h)

5. **Architecture du patch `pd/prototype_01_4hp_ambi.pd`**

```text
[Lecteur readsf~] ──► [ambi_encode 2D ordre 1] ──► bus ambisonique (3 canaux : W, X, Y)
                                                          │
                    [source azimuth / élévation / distance] (sliders ou automation)
                                                          │
                    [ambi_decode3 2D ordre 1 → 4 sorties] ──► [dac~ 1 2 3 4]
```

6. **Géométrie des 4 baffles (carré, vue du dessus)**
   ```text
        HP1 (0°)
    HP4         HP2
   (270°)       (90°)
        HP3 (180°)
   ```
   - Positions en degrés azimut : `0, 90, 180, 270` (à confirmer selon ton câblage réel).

7. **Fonctions minimales du proto**
   - Lecture d'au moins 1 fichier audio (idéalement sélection aléatoire dans un dossier).
   - Contrôle manuel de la position de la source (2 sliders : azimuth + éventuellement distance).
   - Option : rotation automatique lente (`ambi_rot`) pour tester le mouvement.
   - 4 sorties distinctes vers `dac~`.

8. **Test d'écoute**
   - Casque d'abord (stéréo décodée) si pas encore 4 HP branchés.
   - Puis 4 sorties réelles via interface audio.

### Phase D — Validation (≈ 15 min)

9. **Critères de succès du proto 01**
   - [ ] Pd démarre sans erreur `iem_ambi`
   - [ ] Un fichier WAV joue
   - [ ] Le son se déplace perceptiblement dans l'espace (manuel ou auto)
   - [ ] 4 canaux de sortie actifs et identifiables (test tonal par HP)

---

## 3. Ce qui est volontairement reporté (proto 02+)

- Machine à états (Cortex / Hippocampe / …)
- Scan dynamique de dossiers `SONS/CORTEX/…`
- Micros + analyse RMS
- Mémoire vivante (`writesf~`)
- Migration Raspberry Pi
- 12 baffles + calibration acoustique de salle
- Intégration `pd-acre-amb`

---

## 4. Contradictions résolues dans les anciens documents

| Document | Ancienne position | Position actuelle |
|----------|-------------------|-------------------|
| `Document_de_travail_evolutif.md` §7 | Simon propose d'abandonner l'ambisonie pour un routing dynamique | **Ambisonie `iem_ambi` retenue** (confirmé par toi + `Document_Technique_Definitif`) |
| `docs/01_premiere_recherche.md` | Routing matriciel simple recommandé | Archive — remplacé par ambisonie pour la spatialisation organique |
| `Document_de_travail_evolutif.md` §12 | Mention de patch **Max/MSP** | **Pure Data** remplace Max pour la portabilité Linux/Pi |

---

## 5. Structure de projet proposée (à créer au fur et à mesure)

```text
memoires-en-transit/
├── docs/
│   ├── 01_premiere_recherche.md      ← archive
│   └── 02_prototype_01_decisions_et_plan.md  ← ce fichier
├── pd/
│   ├── externals/iem_ambi-master/    ← après extraction + compilation
│   └── prototype_01_4hp_ambi.pd      ← patch du jour
├── SONS_PROTOTYPE/                   ← tes WAV de test
└── SONS/                             ← arborescence finale (plus tard)
```

---

## 6. Questions à clarifier AVANT de coder

> **Réponses du 7 juillet 2026 :**

| Question | Réponse |
|----------|---------|
| Fichiers audio de test | Copiés dans `SONS_PROTOTYPE/` à la racine du repo |
| Setup audio | Interface USB avec **≥ 4 sorties** |
| Pure Data | **Déjà installé** sur le Mac |
| Comportement spatial proto | **Les trois modes** : manuel, orbite auto, sauts aléatoires — avec sélecteur dans le patch |
| Bibliothèque ambisonique | **`iem_ambi` seul** (pas `pd-acre-amb` pour l'instant) |

### Questions restantes (bloquantes pour le câblage)

1. **Quelle interface audio ?** (modèle exact — pour mapper `dac~ 1 2 3 4` aux bonnes sorties physiques)
2. **Disposition physique des 4 HP** : carré ? rectangle ? dimensions approximatives de la pièce de test ?
3. **Sens de référence** : quel HP est « devant » (0°) dans ta pièce ?
4. **Format des WAV** : sample rate (44.1 / 48 kHz) ? mono ou stéréo ?

Une fois ces 4 points répondus (ou après un premier test à l'aveugle), on peut coder `pd/prototype_01_4hp_ambi.pd`.
