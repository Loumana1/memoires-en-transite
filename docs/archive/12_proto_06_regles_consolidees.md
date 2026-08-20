# Proto 06 — Règles consolidées (mémo)

**Projet :** Mémoires en transit  
**Date :** 12 août 2026  
**Statut :** synthèse des règles actées et implémentées pour le Proto 06.  
**Sources :** `archive/09_qa_prototype_05.md`, `10_proto_06_handoff_technique.md`, `11_proto_06_calibrage.md`, `archive/08_grille_contenu_sons.md`, `scripts/proto06/proto06_lib/presets06.py`.

Ce document ne remplace pas le Q&A ni le handoff : c’est un **mémo de lecture rapide** pour se rappeler ce qui est en vigueur.

---

## 1. Narration / FSM

- **4 états :** CORTEX (0) · HIPPOCAMPE (1) · RECONSTRUCTION (2) · BOUCLE (3)
- **Cycle 1 — 4HP / 6HP (legacy Q3) :** BOUCLE → HIPPO → RECON → CORTEX(clarté) (~50 s)
- **Cycle 1 — 8HP (artiste, docs/13) :** **CORTEX (opaque) → HIPPO → RECON** (~39 s)
  - CORTEX **~14 s** — densité / delay fort / non lisible
  - HIPPO **~9 s** — mouvement, moins de couches
  - RECON **~16 s** — fil clair + fragments
  - BOUCLE **hors cycle 1** (FORCE / debug uniquement)
- **Cycles 2+ :** ordre libre, **~15–35 s** par état, retour CORTEX **1 transition sur 5** (`FREE_CORTEX_EVERY = 5`) — en 8HP = retour zone opaque
- **État suivant toujours différent** (pas de doublon immédiat)
- **Reset session = 7 min** (420 000 ms) → reforce le cycle 1
- Session démarre au **AUDIO_ON** (pas au loadbang du patch)
- **Aucun silence** entre états ; coupure ≤ **100 ms**
- **AUTO ⊥ FORCE** : FORCE ignoré si AUTO = 1

---

## 2. Couches

### 4HP / 6HP (max 3) — legacy

| État | Nb couches | Rôle |
|------|------------|------|
| **BOUCLE** | **1** | Strict, pas d’interférence par défaut |
| **CORTEX** | **2** | Fond + 1 interférence **après délai** (`ovl` 3 / 5 / 8 s) |
| **RECON** | **2** | Superposition limitée |
| **HIPPO** | **3** | Fond + **2** arrivées courtes |

### 8HP — gradient artiste (max 6)

CORTEX = zone **profonde / opaque** ; RECON = zone **haute / claire**.

| État | Zone | Nb couches | ECHO (cible) |
|------|------|------------|--------------|
| **CORTEX** | profonde (opaque) | **6** | **fort** (plafond projet) |
| **HIPPO** | intermédiaire | **3** | court / moyen |
| **RECON** | haute (lisible) | **2** | bas / quasi off |
| **BOUCLE** | hors parcours AUTO | **4** | fort (FORCE) |

- Couche 1 = **MOYEN** (15–90 s), boucle en fin de fichier
- Couches 2+ = **COURT** (&lt; 15 s), **one-shot**
- Segments découpés ≤ **90 s** (K5)
- Jamais le même fichier deux fois de suite dans un slot
- Ancres 8HP (6) : HP1 / HP3 / HP5 / HP7 / HP2 / HP6 sur l’octogone

---

## 3. Spatial

- **Mapping fixe (N1)** — pas de rotation des ancres à chaque transition :
  - **4HP :** couche1→HP1, couche2→HP3, couche3→HP4
  - **6HP :** mêmes slots, géométrie rectangle + 2 milieux du grand côté
  - **8HP :** 6 ancres — HP1 / HP3 / HP5 / HP7 / HP2 / HP6 (octogone)
- **SPAT mixte** autorisé (une couche saute, une autre tourne)
- Modes : dry ancré · rotation · saut · séquence
- **BOUCLE :** saut/séquence **50/50** (pas dry)
- **HIPPO / CORTEX :** dry + rotation (flash = saut/seq/rot)
- Sens de rotation **configurable par variante**

---

## 4. FX (ECHO = delay `fx_fluid`)

### 4HP / 6HP (legacy)

> CORTEX **sans ECHO** ; BOUCLE / HIPPO / RECON en ont à des degrés différents.

- **Plafond ECHO BOUCLE :** wet **0.85** / delay **800 ms** / fb **0.70** / lfo **0.50**
- **CORTEX : ECHO off** sur la couche principale (clarté legacy)

### 8HP (artiste)

| État | ECHO | Sat | Filtre |
|------|------|-----|--------|
| **CORTEX** | **fort** (wet ~0.7–0.85) | **forte** (sat ~0.35–0.60) | HPF ↑ / LPF sombre + flfo |
| **HIPPO** | court / moyen | légère (~0.15–0.25) | plus ouvert |
| **RECON** | bas / quasi off | **off** / min | ouvert (lpf ~16–20 kHz) |
| **BOUCLE** | fort (FORCE) | moyenne | moyen |

Chaîne par couche : **`fx_distort_06` → `fx_filter_06` → `fx_fluid`** (ordre J8).  
Compensation sat : `gain = 1/(1+sat×1.5)` (J7).  
Gain master figé : `*~ 0.65`. Phaser / réverb SPACE → hors V0.

---

## 5. Variantes / UI / exploitation

- **3 variantes** par état
- Toggle **CONTRASTE** HAUT (défaut) / BAS (×0.65 sur wet/fb/lfo)
- Re-clic FORCE = change **SPAT/FX**, **pas** le fichier
- Presets V0 : `mode_presentation` · `mode_edition_complete` · `mode_automatique` · `mode_danse`
- **INSTALL_MODE** ON = masque moteur/debug
- Console Pd : **zéro error, zéro warning**
- Proto **05 figé** — tout le travail vit dans le 06
- Lancement : `bash scripts/launch_prototype_06_4hp.sh` / `_6hp.sh` / `_8hp.sh`
- Calibrage vivant : `docs/11_proto_06_calibrage.md` + `scripts/proto06/proto06_lib/presets06.py`

---

## 6. Contenu audio

- Dossiers `SONS/{ÉTAT}/{COURT|MOYEN|LONG}/`
- Audit RMS : exclut segments vides ou trous ≥ **5 s**
- Pool MOYEN limité aujourd’hui → répétitions possibles sur longue session (contenu, pas le moteur)

---

## 7. Hors V0 (décidé mais pas encore codé)

- Burst BOUCLE 300–400 ms sur fenêtre 3–4 s
- Patterns trajectoires catalogués P1–P7 + repos oscillant
- Ping-pong au croisement (~25–30 %)
- Superpositions **répétées** dans un même état (budget ~15 s / 50 s CORTEX)
- Queue delay/reverb inter-états
- Phaser
- Saturation / filtre sur **4HP/6HP** (déjà en place sur **8HP**)

---

## 8. Variantes hardware Proto 06

| Variante | Sorties carte | Notes |
|----------|---------------|--------|
| **4HP** | 1–2–3–4 | Référence fonctionnelle |
| **6HP** | 1–2–4–5–6 | Rectangle + paire médiane |
| **8HP** | 1–2–3–4–5–6–7–8 | Octogone + VISU + **jusqu’à 6 couches** (profondeur) |
