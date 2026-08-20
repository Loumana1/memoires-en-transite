# Prototype 07 — Synthèse, écarts, backlog

> **18 août 2026 — intention historique (16 août).** Pas une spec. Vérité runtime : [`../etatactuel.md`](../etatactuel.md) · pourquoi : [`../log.md`](../log.md). Les statuts UC ci-dessous sont **périmés**.

**Projet :** Mémoires en transit / Micro-opacités  
**Date :** 16 août 2026  
**Statut :** moteur **Proto 07 8HP généré** (16 août 2026, soir) — à écouter FORCE puis AUTO  
**Cible machine :** 8 HP (parcours artiste). 4 HP / 6 HP restent le legacy Proto 06.

**Sources :** intention Micro-opacités (4 zones) · tableaux d’écoute artiste · Proto 06 8HP (`presets06.py`, `docs/12`, `docs/13`) · masters `Opacité fin V2/`

**Documents liés :**
- [`etatactuel.md`](../etatactuel.md) · [`log.md`](../log.md)
- [`archive/15_prototype_07_qa_createur.md`](../archive/15_prototype_07_qa_createur.md) — Q&A 16 août (intention)
- [`archive/07_roadmap_prototypes_finale.md`](../archive/07_roadmap_prototypes_finale.md)

---

## 0. Ce que Proto 07 est (et n’est plus)

La roadmap de juillet plaçait le **07 = interaction piezo**. Ce n’est plus le centre.

**Proto 07 = conceptualisation des quatre zones comme manières de traiter une même matière**, plus de précision sur les cycles et les comportements de couches, plus intégration des nouveaux masters.

| | Proto 06 (aujourd’hui) | Proto 07 (cible) |
|--|------------------------|------------------|
| Nature des zones | 4 **états FSM temporisés** qui jouent chacun **son dossier** | 4 **modes de traitement** d’une matière qui **circule** |
| Cycle 1 (8HP) | CORTEX 28 s → HIPPO 9 s → RECON 16 s | **AUTO :** Cortex **40 s** → Hippo **50 s** → Recon **2 min** (plages 20–60 / 30–90 / 1–4 min) ; Boucle en latence |
| Boucle | 4ᵉ état FORCE / debug, durée fixe | **Pas un état qui s’installe** : buffer de persistance / réactivation |
| Matière | `SONS_FINAL` ~72 s × 3 | `Opacité fin V2` ~26 min × 4 (dont **Cortex ambiance**) |
| Public | hors moteur | **biais** densité / transition / retour — sans causalité évidente |

Le piezo n’est pas abandonné : il devient un **modulateur** des règles 07 (voir UC-P*), pas un prototype séparé.

---

## 1. Ce qui est déjà implémenté (Proto 06 8HP)

À garder comme **socle** — on ne recommence pas le moteur.

### Moteur

- FSM 4 états, AUTO ⊥ FORCE, reset 7 min, session au `AUDIO_ON`
- Cycle 1 8HP déjà dans le **sens artiste** : CORTEX → HIPPO → RECON (Boucle hors AUTO)
- Jusqu’à **10 couches**, mapping fixe par ancre, decode octogone 8 HP
- Chaîne FX par couche : `fx_distort_06` → `fx_filter_06` → `fx_fluid`
- 3 variantes / état, CONTRASTE HAUT/BAS, INSTALL_MODE, presets V0
- Générateurs Python : `presets06.py` → `gen_prototype_06_8hp.py`

### CORTEX (8HP)

- Densité **10** (HP1–8 + 2ᵉ fragment sur HP1 et HP5)
- **Pas** de sample principal partagé ; pools exclusifs `SONS/CORTEX/B1..B8`
- Sat forte + ECHO **modéré** + HPF 400–600 / LPF sombre
- Fragments assemblés (lits 13–30 s) depuis l’ancien master 72 s

### HIPPOCAMPE (8HP)

- Densité **4** (< CORTEX) — bon sens de gradient
- `mode 4` circulation locale 3–4 baffles + sweep solo 1→8 **parfois**
- `play_reps=3` (même sample 3 fois avant swap)
- FX encore trop présents vs cible (filtre / delay / reverb)

### RECONSTRUCTION (8HP)

- Densité **2**, ECHO très bas / dry, sat off — **déjà le plus proche** de la cible
- Pas encore de distinction **principal continu** vs **interruptions 1–5 s**
- Durée d’état **16 s** — trop courte pour un fil 1–4 min

### BOUCLE (8HP)

- Existe comme état FORCE (densité 4, ECHO fort)
- **N’est pas** un buffer de fragments avec délai / proba / dégradation / réinjection

### Audio actuel dans `SONS/`

| Dossier | Ordre de grandeur | Problème pour le 07 |
|---------|-------------------|---------------------|
| CORTEX B1–B8 | ~50 lits assemblés | issus de l’**ancien** master 72 s |
| HIPPO COURT/MOYEN | 4 + 2 fichiers, 0,8–4,6 s | trop peu, trop courts vs 5–10 s |
| RECON COURT/MOYEN | 4 + 2 fichiers, 0,8–8,6 s | pas de principal long |
| BOUCLE | ancien stock proto | hors matière V2 |
| `Opacité fin V2/` | **4 × 26 min 42 s**, 48 kHz stéréo 16-bit | **pas encore découpé ni branché** |

---

## 2. Ce qui doit être implémenté (cible artiste)

Les zones ne sont **pas** quatre banques fermées. Un fragment peut apparaître, être retenu, associé, transformé, disparaître, revenir ailleurs.

```text
CORTEX ──► HIPPOCAMPE ──► RECONSTRUCTION ──► BOUCLE ──► CORTEX
   │              │                │              │
   └──────── raccourcis, latence, disparition ────┘
```

### 2.1 Cortex — accumulation / transparence

| Paramètre | Cible 07 |
|-----------|----------|
| Durée d’état | **20–60 s** (défaut AUTO **40 s** — Q07-02) |
| Fragments | **13–30 s** chacun ; **aucun** sample principal |
| Spatial | **Les 8 baffles** actifs (Q07-03). Plus de mouvement que le croquis 2+2+2. Superposition possible **dans** un même baffle. |
| Ambiance | **1 HP dédié**, fixe pendant le tour, index peut changer au tour suivant (Q07-04). **XOR** (Q07-20) : mode **ambiance** (dry, highs un peu coupés) **ou** mode **next-room** (highs presque tous coupés + reverb). Jamais les deux. Fichiers **2–3 min** (Q07-06). |
| Densité fragments | min 3 / max 6 **plus** la couche ambiance (les 7 HP restants portent les fragments / le mouvement) |
| FX (fragments) | **moins de delay**, **plus de filtre** ; LPF **400–600 Hz** (Q07-10). Next-room **uniquement** sur le lit d’ambiance, pas sur un autre fragment. |
| Public | pas de mouvement → **reste Cortex** ; piezo / énergie → favorise le changement |
| Sortie | sélectionne de **petits** fragments (mot, syllabe, souffle, texture) vers Hippo / Recon / Boucle |

Le flou vient du **traitement** (filtre / recouvrement), pas d’une matière déjà illisible.

### 2.2 Hippocampe — association

| Paramètre | Cible 07 |
|-----------|----------|
| Durée d’état | **30–90 s** |
| Fragments | **5–10 s** |
| Densité | **moins** que Cortex, **plusieurs** sons (pas un seul voyageur) — Q07-08 |
| Spatial | **circulaire** 1→2→…→8→7→…→1 (pas zigzag) ; plusieurs fragments sur le cercle |
| FX | moins filtre / delay / reverb que Cortex — on **suit** et on **reconnaît** |
| Logique | un son en **déclenche** un autre (pas toujours le même) ; appel–réponse entre enceintes |
| Public | peut renforcer, interrompre ou dévier une association, **sans** choisir le fichier |

V1 réaliste : **tirage au hasard** (Q07-12). Tags **souhaités** dès qu’un système de classification existe (Q07-16) — crochet prévu, pas bloquant.

### 2.3 Reconstruction — recomposer sans figer

| Paramètre | Cible 07 |
|-----------|----------|
| Durée d’état | **1–4 min** |
| Couche 1 | voix / archive **continue**, 30 s à plusieurs minutes |
| Couche 2 | interruptions **1–5 s** |
| FX | quasi dry ; lisibilité **volontaire** |
| Spatial | un **tout petit peu** mobile, comme le 06 actuel (Q07-09) |
| Logique | versions d’une même mémoire (phrase → mots → syllabe) ; résultats **réinjectables** |

V1 : deux pools (PRINCIPAL / COURT) + tirage d’interruptions.  
Dossiers `DEGRE_*` prévus pour la pré-coupe artiste (Q07-17) — contenu **pas encore livré**.  
V2 : tags / « sons qui font semblant de s’entendre » quand la classification existera.

### 2.4 Boucle — persistance, pas un 4ᵉ « paysage »

Ce n’est **pas** une durée d’état. Le système **pioche** dans un buffer selon une **probabilité de bascule**, pas selon un timer « rester 14 s en Boucle ».

Chaque fragment stocké : durée de conservation, délai min/max, proba de retour, nb de retours, version (originale / reconstruite / dégradée), enceinte, gain, filtrage, destination (Cortex / Recon / Boucle).

À chaque retour : autre baffle, autre délai, plus court / plus sourd / partiel, ou **intact** après une longue absence.

---

## 3. Écarts majeurs (lire avant de coder)

| Sujet | Proto 06 8HP | Cible 07 | Gravité |
|-------|--------------|----------|---------|
| Durées d’état | 28 / 9 / 16 s (~53 s le cycle) | AUTO 40 / 50 / 120 s (plages 20–60 / 30–90 / 60–240) | **Cassante** — acté Q07-01/02 |
| HIPPO spatial | zigzag local + sweep 1→8 parfois | ping-pong circulaire **1↔8** | Contraste d’écoute |
| CORTEX mapping | 10 couches / 8 HP | **8 HP tous utilisés** + 1 HP ambiance dry (index par tour) ; plus de mouvement | Acté Q07-03/04 |
| CORTEX FX | delay encore présent | LPF 400–600 **sur fragments** ; lit ambiance = dry **ou** next-room (XOR) | Calibrage |
| RECON forme | 2 couches génériques, 16 s | principal long + interrupts, 1–4 min | Architecture player |
| BOUCLE | état FORCE temporisé | buffer latent + proba de réinjection | **Nouveau module** |
| Matière | master 72 s | V2 26 min + piste ambiance | Pipeline audio |
| Circulation fragments | dossiers étanches | un fragment **voyage** | Mémoire partagée — V1 légère |
| Associations Hippo | tirage de dossier | A déclenche B | Nouveau |
| Piezo | hors 06 | « pas de mouvement = Cortex » | Couplage léger |

**Contradiction historique (déjà tranchée en 8HP, à ne pas recréer) :**  
l’ancien Q&A 05 disait CORTEX = clarté finale. Chez l’artiste, CORTEX = **opaque**. Le 07 suit l’artiste.

---

## 4. Pipeline audio — `Opacité fin V2` → `SONS/`

### 4.1 Inventaire (16 août 2026)

Dossier : `Opacité fin V2/` (à ne pas confondre avec `SONS_FINAL/`, master court d’août).

| Fichier | Durée | Rôle probable |
|---------|-------|----------------|
| `opacité fin V2  Cortex.wav` | 26 min 42 s | fragments Cortex (silences longs 2–22 s déjà présents) |
| `opacité fin V2  Cortex ambiance.wav` | 26 min 42 s | **lit continu** → découpe en **2–3 min** ; 1 HP dédié dry (pas forcément 4) |
| `opacité fin V2  Hippocampe.wav` | 26 min 42 s | fragments plus denses, gaps courts |
| `opacité fin V2  Reconstruction.wav` | 26 min 42 s | mix principal + bribes ; à classer à la découpe |

Format : PCM 16-bit, **48 kHz stéréo**. Les scripts actuels exportent en **mono**.

Sondage Cortex (3 premières minutes) : les prises utiles ont l’air d’être déjà dans la plage **13–30 s**, séparées par de longs silences. **Ne pas** recoller des atomes comme `build_cortex_beds.py` le faisait sur le master 72 s.

### 4.2 Travail à faire (avant / pendant le moteur)

1. Étendre `slice_sons_final.py` (ou script `slice_opacite_v2.py`) : source = `Opacité fin V2/`, 4 masters.
2. Découpe par silences **par zone**, avec seuils différents (Cortex silences longs ; Hippo plus serré).
3. Classification :
   - Cortex → fragments 13–30 s → pools sur **les 8 baffles** (pas seulement B1–B3)
   - Ambiance → tranches **2–3 min** (`SONS/CORTEX/AMBIANCE/`), plafond **180 s**
   - Hippo → viser 5–10 s ; trop court / trop long = dossier `ECART/` à écouter
   - Recon → `PRINCIPAL/` (≥ 30 s) et `COURT/` (1–5 s) ; 5–30 s → `MOYEN/`
4. Remplir `SONS/` **sans écraser** l’ancien stock tant que le 07 n’est pas validé à l’oreille (`SONS_V2/` ou suffixe `v2_`).
5. Rebuild 8HP uniquement quand les pools minimaux existent (voir UC-A04).

---

## 5. Backlog de use cases (à respecter)

Règle : un UC est **écoutable** ou **vérifiable en patch**.  
Priorité : **P0** = Proto 07 n’existe pas sans ça · **P1** = comportement de zone · **P2** = circulation mémoire · **P3** = plus tard.

### A — Matière

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-A01** | Les 4 masters V2 sont découpés ; fragments nommés, mono 48 kHz, classés | P0 | **fait** (`SONS_V2/`, 159 fichiers) |
| **UC-A02** | Piste **Cortex ambiance** découpée en lits **2–3 min**, distincte des fragments | P0 | **fait** (10 × 160 s) |
| **UC-A03** | Ancien `SONS/` conservé / basculable (A/B d’écoute) | P0 | **fait** (`SONS/` intact) |
| **UC-A04** | Minimums : Cortex ≥ 6 ; Hippo ≥ 8 (5–10 s) ; Recon ≥ 2 principaux + ≥ 8 courts | P0 | **fait** (14 / 13 / 4+49) — journal doc 16 |
| **UC-A05** | Journal de découpe (durée, écarts vs plages) pour correction oreille | P1 | **fait** [`16_proto_07_journal_decoupe.md`](../16_proto_07_journal_decoupe.md) |

### C — Cortex

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-C01** | Aucun sample « principal » unique | P0 | partiel (06 OK, à garder) |
| **UC-C02** | **Les 8 baffles** portent du Cortex ; plus de mouvement que le croquis 2+2+2 | P0 | à recabler (aujourd’hui 1/HP × 8 + 2 doublons, peu de mouvement) |
| **UC-C03** | 1 couche ambiance, 1 HP dédié (pas forcément 4), **fixe pendant le tour** ; **XOR** dry / next-room (~1/2) | P0 | absent |
| **UC-C04** | 3 à 6 fragments actifs (+ ambiance) ; densité variable dans l’état | P0 | 10 couches fixes aujourd’hui |
| **UC-C05** | Durée d’état 20–60 s (tirage dans la plage) | P0 | 28 s fixe |
| **UC-C06** | Chaque fragment 13–30 s | P0 | lits 06 trop liés à l’ancien master |
| **UC-C07** | Plus de filtre que de delay ; LPF ~400–600 Hz | P0 | partiel (HPF 400–600 + LPF 2–3 kHz — **pas** le LPF 400–600 demandé) |
| **UC-C08** | Mode next-room : highs presque off + reverb **sur le lit d’ambiance seulement** | P0 | SPACE hors V0 — à ajouter pour cette couche |
| **UC-C09** | Superposition **dans** un même baffle (2 couches HP1, etc.) | P0 | partiel (seulement HP1 et HP5) |
| **UC-C10** | Parole **non déchiffrable** (flou de traitement, pas matière morte) | P0 | à valider oreille V2 |
| **UC-C11** | Variabilité **contenue** (rester flou Cortex, ne pas sonner Recon) | P1 | à calibrer |
| **UC-C12** | Sans énergie / mouvement détecté → **rester** Cortex | P1 | absent (timer seul) |

### H — Hippocampe

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-H01** | Moins de couches que Cortex | P0 | OK en 06 (4 vs 10) — **recalculer** vs Cortex 8 HP + ambiance |
| **UC-H02** | Fragments 5–10 s | P0 | stock actuel trop court / trop rare |
| **UC-H03** | Durée d’état 30–90 s | P0 | 9 s aujourd’hui |
| **UC-H04** | Spatial **circulaire** 1→2→…→8→7→…→1 ; **plusieurs** sons suivables | P0 | mode4 local + zigzag — **non conforme** |
| **UC-H05** | FX plus secs que Cortex : on reconnaît le son | P0 | encore trop de filtre/delay |
| **UC-H06** | Un fragment **en déclenche** un autre (enceinte différente, pas toujours le même couple) | P1 | absent (tirage dossier) |
| **UC-H07** | Appel–réponse / croisement bref de deux souvenirs | P1 | absent |
| **UC-H08** | Le visiteur ne choisit pas le fichier ; il peut seulement **dévier** | P2 | lié piezo |

### R — Reconstruction

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-R01** | 1 principal continu (30 s – minutes) | P0 | absent (fichiers ≤ 9 s) |
| **UC-R02** | Interruptions 1–5 s qui ne cassent pas la compréhension | P0 | COURT existe, pas câblé comme interrupt |
| **UC-R03** | Durée d’état **1–4 min** | P0 | 16 s |
| **UC-R04** | FX quasi dry ; sat off | P0 | déjà proche |
| **UC-R05** | On comprend la majeure partie du fil | P0 | à valider V2 |
| **UC-R06** | Spatial : **un tout petit peu mobile**, comme le 06 actuel | P0 | déjà proche — **garder / affiner** |
| **UC-R07** | Dossiers prêts pour pré-coupe artiste (phrase / mots) ; classification « s’entendre » plus tard | P2 | pas de fichiers encore |
| **UC-R08** | Résultat réinjectable vers Cortex / Hippo / Boucle | P2 | dossiers étanches |

### B — Boucle

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-B01** | Boucle **hors** cycle comme paysage temporisé | P0 | 8HP AUTO déjà hors cycle 1 — **garder** |
| **UC-B02** | Buffer : un fragment entendu peut être **mis en attente** | P1 | absent |
| **UC-B03** | Délai min/max + proba de réactivation (pas de retour garanti) | P1 | absent |
| **UC-B04** | Réapparition : autre HP, autre gain, éventuellement plus court / plus sourd | P1 | absent |
| **UC-B05** | Parfois retour **intact** après longue absence | P1 | absent |
| **UC-B06** | Parfois coupure avant reconnaissance | P2 | absent |
| **UC-B07** | Réinjection Cortex (nouvelle info) ou Recon | P2 | absent |
| **UC-B08** | Proba de **piocher** la Boucle à une transition (**15 %** v1, Q07-11) | P1 | à coder |

### S — Système / circulation

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-S01** | Cycle 1 : Cortex → Hippo → Recon (durées 07) | P0 | ordre OK, durées non |
| **UC-S02** | Après Recon : soit retour Cortex, soit **piocher Boucle**, soit Hippo (matrice, pas pipeline unique) | P1 | cycles 2+ libres mais sans Boucle-buffer |
| **UC-S03** | État suivant ≠ état courant | P0 | déjà là |
| **UC-S04** | Reset 7 min → reforce Cortex **opaque** (pas clarté) | P0 | déjà l’intention 8HP |
| **UC-S05** | **Queue delay** Cortex→Hippo (pas un fondu volume). **Coupe sèche** Recon→Hippo. Coupes parfois ailleurs. Pas de silence | P0 | coupe sèche partout en 06 ; queue hors V0 |
| **UC-S06** | FORCE toujours dispo hors AUTO pour caler zone par zone | P0 | déjà là |
| **UC-S07** | Console Pd : zéro error / warning | P0 | règle projet |

### P — Présence (logique dès le 07, matériel plus tard)

| ID | Use case | Prio | Statut |
|----|----------|------|--------|
| **UC-P01** | Entrées **piezo** et **micro** + `rms_sim` ; **aucun** monitoring vers les HP | P0 | hors 06 |
| **UC-P05** | Toggle **INPUT_ON** (activer / désactiver) indépendant du matériel | P0 | — |
| **UC-P02** | Énergie basse → prolonger Cortex | P1 | — |
| **UC-P03** | Énergie / transitoire → favoriser sortie Cortex (vers Hippo) | P1 | — |
| **UC-P04** | Même énergie **biais** la proba Boucle, sans 1 geste = 1 fichier | P2 | — |

### Hors vague Proto 07 (noté, pas bloquant)

- Classification / tags Hippo (artiste, Q07-16) — crochet prévu
- Fichiers `DEGRE_*` Reconstruction (artiste, Q07-17)
- Phaser, grain, ring
- 12 HP / Pi 5 / mémoire vivante `writesf~`
- 4 HP / 6 HP : **terminé** pour ce proto (Q07-18)

---

## 6. Vagues d’implémentation (ordre)

Ne pas tout coder d’un coup. Chaque vague = écoute FORCE par zone, puis AUTO.

| Vague | Contenu | Use cases | Critère de sortie |
|-------|---------|-----------|-------------------|
| **0** | Q&A créateur 01–20 | — | **fait** (16 août) |
| **1** | Découpe V2 + pools `SONS_V2` + ambiance **2–3 min** + A/B ancien stock | A01–A05 | **fait** (16 août) — voir doc 16 |
| **2** | Durées FSM 07 (40 / 50 / 120 s) + densités 8 HP Cortex / Hippo plusieurs / Recon 2 | C04–C06, H01–H03, R01–R03, S01 | **fait** (moteur) — à valider oreille |
| **3** | Cortex 8 HP + mouvement · lit ambiance XOR dry/next-room · LPF fragments | C02, C03, C07–C09 | **fait** (moteur) |
| **4** | Hippo circulaire 1↔8 · **plusieurs** sons · FX plus secs · fragments 5–10 s | H04, H05 | **fait** (moteur) |
| **5** | Recon = principal + interrupts · mobilité légère comme 06 | R01, R02, R04–R06 | **fait** (moteur) |
| **6** | Boucle-buffer V1 (hasard + 15 %) | B01–B05, B08 | **fait** v1 (inject 8–90 s, pas un paysage) |
| **7** | Hippo A→B hasard ; crochet tags vide | H06, H07 | **fait** v1 (bangs décalés + `s6_tag_hook`) |
| **8** | Présence : logique piezo/micro + **toggle**, simu | C12, P01, P05, P02–P03 | **fait** (`INPUT_ON` / `RMS_SIM`) |

---

## 7. Checklist d’écoute Proto 07

À cocher **en salle 8 HP** après vague 5 (moteur + matière). Vague 6–8 = bonus.

- [ ] CORTEX : dense, flou, **8 baffles** actifs, lit d’ambiance **dry ou next-room** (un seul mode par tour), parole non lisible
- [ ] HIPPO : moins de couches, **plusieurs** sons, mouvement **circulaire** suivable, son reconnaissable
- [ ] RECON : un fil long + interruptions courtes, clarté retrouvée
- [ ] Ordre AUTO Cortex → Hippo → Recon, durées **longues** (plus le cycle 53 s)
- [ ] Matière = fichiers `v2_`, pas l’ancien stock 72 s
- [ ] (vague 6) Un fragment déjà entendu **revient** plus tard, différent ou intact
- [ ] Le visiteur ne « joue » pas de sample précis

---

## 8. Fichiers code probablement touchés (quand on passera au code)

Ne pas modifier le 06 tant que la vague 1 (découpe) n’est pas écoutée. Mapping HP et durées BLOQUANT sont **tranchés**.

| Fichier | Rôle 07 |
|---------|---------|
| `scripts/slice_sons_final.py` / nouveau `slice_opacite_v2.py` | découpe V2 |
| `scripts/build_cortex_beds.py` | **ne plus recoller** si les fragments V2 sont déjà 13–30 s |
| `scripts/proto06_lib/presets06.py` | durées, FSM_N, LPF, mapping couches — ou `presets07.py` |
| `scripts/proto06_lib/gen_libs06.py` | `hippo_motion` circulaire ; player Recon principal+interrupt ; buffer Boucle |
| `pd/lib/hippo_motion_06.pd` | remplacer zigzag par ping-pong 1↔8 |
| `pd/lib/fx_*` | send réverb courte 1 couche Cortex |
| `pd/prototype_06_fsm_8hp.pd` | soit étendre, soit `prototype_07_fsm_8hp.pd` (préférable : 06 figé comme 05) |

**Recommandation actée (Q07-14) :** Proto 06 8HP **figé**. Générer `prototype_07_fsm_8hp.pd` à part, pour A/B en salle. **8 HP seulement** (Q07-18).
