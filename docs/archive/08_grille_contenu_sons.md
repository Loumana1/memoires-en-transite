# Grille contenu — SONS/ et états FSM

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Statut :** document vivant — aligné sur les extraits réels dans `SONS_PROTOTYPE/wav/`

---

## 1. Sources actuelles

| Fichier source | Usage principal |
|----------------|-----------------|
| `keren 5 bon.wav` | Voix intime — BOUCLE, HIPPOCAMPE, CORTEX |
| `Voix pour la danse fin.wav` | Corps / voix — RECONSTRUCTION, HIPPOCAMPE, BOUCLE — **+ 3 parties** (`parts/voix_danse_part{1,2,3}.wav`) |
| `radio campus rencontre.wav` | Dialogue / archive — **+ 10 parties** (`parts/radio_campus_part{01..10}.wav`) |
| `Martin Luther King.wav` | Discours — CORTEX, HIPPOCAMPE, RECONSTRUCTION, BOUCLE |
| `cheick anta diop.wav` | Archive / discours — **+ 3 parties** (`parts/cheick_diop_part{1,2,3}.wav`) |

Découpe : `scripts/slice_extracts.sh` → `SONS/<ETAT>/<DUREE>/*.wav`  
Tiers sources longues : `scripts/split_long_sources_thirds.sh` → `SONS_PROTOTYPE/wav/parts/`

**Matériel :** insuffisant pour Paris (K1) — seul stock disponible ; compléter avant installation.

---

## 2. Les quatre états — intention narrative

| État | Ce qu’on entend | Spatial (cible) | FX (cible) | Variantes |
|------|-----------------|-----------------|------------|-----------|
| **0 — CORTEX** | Clarté + pensées furtives (phase finale) | Dry / rotation ; flash = saut·seq·rot (I1) | Filtre HPF/LPF (J4) ; ECHO off ; sat superposés | **3** |
| **1 — HIPPOCAMPE** | Fond + **superpositions** | Dry / rotation ; flash = saut·seq·rot (I1) | ECHO dynamique (F4) ; sat modérée (J6) | **3** |
| **2 — RECONSTRUCTION** | Recomposition, **plus claire** | Dry + saut + seq + rotation (I1) | ECHO décalé (G4/G5) ; sat **superposés** seulement (J6) | **3** |
| **3 — BOUCLE** | Obsession ; **clarté** possible (H5) | Saut·seq·rotation — pas dry (I1, H4) | ECHO max (H3) ; sat **prédominante** (J6, H5) | **3** |

---

## 3. Durées de segments

| Dossier | Durée typique | Rôle |
|---------|---------------|------|
| `COURT/` | &lt; 15 s | Accents, transitions, nervosité |
| `MOYEN/` | 15 – 90 s | Développement d’une scène mémorielle |
| `LONG/` | *(réservé)* | Plafond global **90 s** (K5) — pas de segment &gt; 1 min 30 |

**Plafond K5 :** tout segment découpé ≤ **1 min 30** (90 s).

---

## 4. Lien avec la FSM

- **Démarrage :** cycle 1 **BOUCLE → HIPPO → RECON → CORTEX** (~50 s) ; CORTEX = **phase finale** ; cycles 2+ libres, **fin CORTEX** ; reset **7 min**.
- **CORTEX** domine le temps cumulé sur session 5–7 min.
- Les presets SPAT/FX sont des **familles de variantes** par état ; re-clic FORCE peut changer l’instanciation (§15.6).

---

## 5. À compléter

- [ ] Valider la répartition fine de chaque extrait (session classification) — **CORTEX : pas de média privilégié pour l’instant ; surtout voix** (Q35)
- [x] Découpe sources longues (K1) : voix + cheick ×3, radio ×10
- [ ] Minimum segments par case État×Durée (K3)
- [ ] Re-découper `SONS/` si plafond 90 s (K5) invalide des segments actuels
- [ ] Contenu définitif archives (hors scope proto 05)
