# Micro-opacités — Plan de mise en œuvre sonore par zone

**Document de travail** — traduction numérique de l’installation artistique  
**Date :** 12 août 2026 (v2 — alignement 8HP + FX + SONS_FINAL)  
**Rôle :** référence **artiste** (cible) · état du **Proto 06 8HP** · checklist d’écoute  
**Lancement :** `bash scripts/launch_prototype_06_8hp.sh`

> **Suite Proto 07 :** [`../etatactuel.md`](../etatactuel.md) · [`../log.md`](../log.md). Ce fichier 13 reste le mémo d’écoute du **06**.

---

## Comment utiliser ce document

| Colonne | Signification |
|---------|----------------|
| **Règle artiste (cible)** | Ce que l’artiste attend pour le résultat final |
| **Proto 06 8HP (actuel)** | Ce que le code 8HP fait aujourd’hui |
| **Écart** | ✅ aligné · ✏️ à valider / calibrer · ❌ encore à faire |

Cochez la checklist en salle après écoute.

**Circulation artistique (cycle 1 — 8HP) :**  
**CORTEX (profond / opaque) → HIPPOCAMPE (tri / mouvement) → RECONSTRUCTION (clarté accessible)**  
Durées typiques : ~14 s / ~9 s / ~16 s (~39 s le cycle).

> **4HP / 6HP** : ancien cycle legacy (BOUCLE→HIPPO→RECON→CORTEX clarté).  
> Seul le **8HP** suit le parcours artiste ci-dessus.

---

## Ce qui est en place dans le code 8HP

| Élément | Avant (legacy) | Maintenant (8HP artiste) |
|---------|----------------|--------------------------|
| Cycle 1 | BOUCLE→HIPPO→RECON→CORTEX | **CORTEX→HIPPO→RECON** |
| Densité CORTEX | 2 | **10** (8 HP + 2 doublons) |
| Densité HIPPO | 6 | **3** |
| Densité RECON | 3 | **2** |
| ECHO CORTEX | off | **modéré** (moins delay, plus filtre) |
| ECHO HIPPO | moyen-fort | **plus court** (~0,2–0,35) |
| ECHO RECON | bas | **très bas / dry** (≤ ~0,12) |
| Distorsion / filtre | absents | **chaîne sat → filtre → echo** |
| BOUCLE | entrée du cycle | **hors cycle 1** (FORCE OK) |
| Contenu audio | anciens extraits proto | **SONS_FINAL** découpés → `SONS/` |
| CORTEX samples | pool partagé + couche1 « principal » | **10 fragments exclusifs** (`B1..B8`, HP1–8 + 2e HP1/HP5) — **aucun sample principal** |

**Chaîne FX par couche :** `fx_distort_06` → `fx_filter_06` → `fx_fluid`  
**Fichiers pivots :** `presets06.py` · `gen_libs06.py` · `pd/lib/fsm_*_06_8hp.pd` · `pd/prototype_06_fsm_8hp.pd`

---

## Contenu audio (SONS_FINAL → SONS)

Masters dans `SONS_FINAL/` (CORTEX / HIPO / RECONS), découpés par silences via :

`python3 scripts/proto06/slice_sons_final.py` puis `python3 scripts/gen_prototype_06_8hp.py`

| État | Fragments | Notes 8HP |
|------|-----------|-----------|
| CORTEX | **10** dans `B1..B8` (1/HP + 2e sur HP1/HP5) | pas de sample principal ; copie aussi en MOYEN (legacy) |
| HIPPOCAMPE | COURT + MOYEN (`final_*`) | densité 4 + motion |
| RECONSTRUCTION | COURT + MOYEN (`final_*`) | densité 2 |

Fichiers CORTEX 8HP : `SONS/CORTEX/B{n}/final_cortex_b{n}_f{1|2}_aNN.wav`.  
BOUCLE conserve l’ancien stock (hors parcours AUTO artiste).

Rebuild lits : `python3 scripts/proto06/build_cortex_beds.py` puis `python3 scripts/gen_prototype_06_8hp.py`

---

## Zone 1 — CORTEX (zone profonde)

**Fonction artistique :** mémoire à l’état brut, non filtrée, saturée d’informations parasites. On perçoit sans distinguer clairement — opacité (Glissant) : droit à ne pas être totalement compris.

| Paramètre | Règle artiste (cible) | Proto 06 8HP (actuel) | Écart |
|-----------|----------------------|------------------------|-------|
| Nombre de samples simultanés | jusqu’à **6** (3–4 « réels » + interférences) | **10** (8 HP + 2 doublons) | ✅ densifié |
| Fragments par baffle | 2 fragments **différents** / baffle ; **pas** de sample principal partagé | pools `B1..B8` ; **4 alts / couche** ; HPF **400–600** | ✅ |
| Effets actifs | distorsion, delay long, filtre | **sat forte** + **ECHO modéré** + **HPF/LPF sombre** (+ flfo) | ✅ |
| Clarté perçue | floue, proches/éloignés indistincts | densités + delay + filtre pour masquer | ✏️ à valider |
| Spatialisation | certains omniprésents, d’autres 1 baffle | **8 baffles** HP1–8 dry/ancré (+ 2e sur HP1/HP5) | ✅ |
| Compréhension verbale | **non déchiffrable** | contenu FINAL + FX — **à écouter** | ✏️ |
| Variabilité | à trancher | 1 fichier fixe / couche (exclusif) ; random Pd au boot ailleurs | ✏️ |

**Ce que l’artiste doit entendre :**
- Densité presque saturée, sans ancrage clair  
- Sons de partout et de nulle part  
- Aucune phrase / mot clairement reconnaissable  

---

## Zone 2 — HIPPOCAMPE (zone intermédiaire)

**Fonction artistique :** le tri — passage du brut vers une forme organisée ; la mémoire se meut et se structure, sans être fixée.

| Paramètre | Règle artiste (cible) | Proto 06 8HP (actuel) | Écart |
|-----------|----------------------|------------------------|-------|
| Nombre de samples simultanés | **moins** que le CORTEX | **3** (&lt; 10) | ✅ |
| Effets actifs | moins de distorsion ; delay court ; mouvement | sat légère + ECHO court + **mouvement SPAT** | ✅ |
| Clarté perçue | plus définie que CORTEX, encore incomplète | intermédiaire | ✏️ |
| Spatialisation | mouvement autour de l’auditeur | **mode4** circulation 3–4 baffles + **sweep solo 1→8** parfois | ✅ |
| Filtre LF | — | **HPF ~400** sur 2 couches / 3 ; swap sample après **3** lectures | ✅ |
| Compréhension verbale | partielle ? à trancher | fragmentaire (dialogue) | ✏️ |
| Transition depuis CORTEX | seuil / fondu / déclencheur ? | cycle fixe ~14 s → HIPPO ; coupe ≤ 100 ms ; **pas de fondu** | ✏️ |

**Ce que l’artiste doit entendre :**
- Mouvement clair dans l’espace  
- Moins de couches qu’en Zone 1  
- Début d’une direction / d’un sens  

---

## Zone 3 — RECONSTRUCTION (zone haute)

**Fonction artistique :** mémoire (re)devenue accessible ; fil narratif / sonore émergent, perturbé mais audible.

| Paramètre | Règle artiste (cible) | Proto 06 8HP (actuel) | Écart |
|-----------|----------------------|------------------------|-------|
| Nombre de samples simultanés | 1 principal + fragments | **2** | ✅ |
| Effets actifs | plus d’effets intenses | ECHO très bas / dry ; sat off / min | ✅ |
| Clarté perçue | on comprend la majeure partie | dry ancré dominant | ✅ *(à confirmer oreille)* |
| Spatialisation | fixe ou encore mobile ? | dry dominant + variantes mobiles légères | ✏️ |
| Compréhension verbale | lisible (sert la « reconstruction ») | texte accessible visé | ✅ |
| Fragments perturbateurs | d’où ? | pool `SONS/RECONSTRUCTION/COURT/` (final_*) | ✅ |

**Ce que l’artiste doit entendre :**
- Fil sonore/verbal clairement identifiable  
- Interruptions ponctuelles sans casser la compréhension  
- « Clarté retrouvée » vs Zones 1–2  

---

## État BOUCLE (4ᵉ état)

Absent du schéma artiste (3 zones). **Hors cycle 1 AUTO** ; accessible en FORCE / debug.  
Options déjà tranchées côté 8HP : fusion conceptuelle dans CORTEX (comportement delay/sat) + BOUCLE gardé pour tests.

---

## Points encore ouverts

1. **Transitions :** coupe sèche OK, ou fondu / queue delay obligatoire ?  
2. **Variabilité :** seed aléatoire à `AUDIO_ON` (aujourd’hui déterministe au boot) ?  
3. **8 baffles :** zones temporelles (actuel) ou baffles dédiés par zone ?  
4. **Micros piezo/électret :** rôle live — hors Proto 06 actuel  
5. **Phaser / réverb SPACE :** hors V0  
6. **Calibrage oreille :** wet/sat/lpf CORTEX pour opacité verbale réelle avec les nouveaux `final_*`

---

## Checklist d’écoute 8HP

- [ ] **CORTEX** = dense, flou, opaque, delay + sat + filtre, peu/pas de sens verbal  
- [ ] **HIPPOCAMPE** = mouvement net, **moins** de couches que CORTEX  
- [ ] **RECONSTRUCTION** = calme relatif + fil compréhensible  
- [ ] Ordre AUTO : **CORTEX → HIPPO → RECON**  
- [ ] Nouveaux samples `final_*` bien entendus (pas l’ancien stock)  
- [ ] FORCE BOUCLE encore accessible hors parcours  
- [ ] Spatialisation 8 baffles cohérente avec l’intention  

---

## Notes libres (pendant l’écoute)

_(espace à remplir)_
