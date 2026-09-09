# TO DO — ce qui est clair

**Mis à jour : 9 sep. 2026.**  
Ligne active = **Proto 08** (expo). **Proto 07** = référence figée (comparaison A/B).  
Ce qui demande une décision artistique est dans [`Q&A.md`](./Q&A.md). Ce fichier n'est pas un sprint.

---

## 0. Infrastructure (toutes versions)

- [x] ~~Git + `.gitignore`~~ — 20 août.
- [ ] **Vérifier la sauvegarde des masters** — `SONS_V3/WIP/Opacité V6/` (2,6 Go). Seule matière irremplaçable.
- [ ] **Détecter un Pd gelé** — timer systemd externe (Pd n'envoie pas `sd_notify`).
- [ ] **Service expo** — `Restart=always` + `StartLimitIntervalSec=0` (ne jamais abandonner au boot).

---

## 1. Proto 07 — legacy (maintenance)

Figé comme le 06. **Ne pas** y porter le chantier 08 (plans, gestes, sélecteur).

### Fait (9 sep. 2026)

- [x] Regénérer après pool `SONS_V3/AMBIANCE/` — `python3 scripts/gen_prototype_07_8hp.py` · 104 ambiances → 5 baffles.
- [x] **`normaliser_niveaux.py`** — 757 fragments mesurés · `niveau_db` / `gain_db` dans `registre_ids.csv`.
- [x] **`verifier_sons.py`** — 4484 refs playlists 07 · aucune erreur bloquante.
- [x] **Boucle inject L10** — valeurs centralisées dans `presets07.BOUCLE_INJECT` (distinct des presets état 3 FSM).
- [x] **`presets07.py`** — docstring et commentaires corrigés.
- [x] **`hippo_motion_07`** — `sens` réécrit sur la couche active (comme `mode` / `step`).

### Reste optionnel (07 seulement)

- [ ] Figer bornes LPF / rotation / nappes **à l'oreille sur le 07** — basse priorité ; le gel oreille vit en 08.
- [ ] Seuil 30 s nappes + refonte `cortex_amb_pulse_07` — **reporté** (07 obsolète pour nappes).

**Regen 07 :** `python3 scripts/gen_prototype_07_8hp.py` puis `python3 scripts/verifier_sons.py`.

---

## 2. Proto 08 — chantier actif (expo)

Objectif : son stable + matière batch 4 intégrée **avant** le sélecteur attributs.

### Cortex

- [x] ~~12 voix / 6 paires · 2 nappes · gestes temporels · gestes spectraux · spatialisation~~ — gelé oreille 26 août.
- [x] ~~Pools nappes disjoints · gains · bleed · HPF voix 400 Hz~~ — figé.
- [ ] **Plans de présence** — 2 chaînes FX complètes par plan · spec [`spec_cortex_plans_presence_08.md`](./spec_cortex_plans_presence_08.md) · prompt [`prompt_cortex_plans_presence_08.md`](./prompt_cortex_plans_presence_08.md).
- [ ] **Figer à l'oreille** — bornes LPF 12 osc. · rotation 6 paires · niveaux nappes (§9 `Cortex.md`).
- [ ] **Batch 4 en nappes** — ajouter les A70+ utiles à `FAVORIS_CORTEX` / `FAVORIS_TEXTURE_CORTEX` (`ambiance_catalog.py`) + regen 08.
- [ ] **Regen patch 08** après matière — `python3 scripts/gen_prototype_08_8hp.py`.

### Hippocampe

Voir [`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) §10 · prompt [`prompt_hippo_oreille_v1_08.md`](./prompt_hippo_oreille_v1_08.md).

- [x] ~~Recettes spatiales · biais fluide · HP7 trim −3 dB~~ — 23 août.
- [ ] **Anti-doublon Pd** — `hippo_play_08` par couche dans `gen_patch08` · **ne pas** toucher `player_state_08` (piège §10).
- [ ] **`FAVORIS_HIPPO`** — liste à définir · wiring prêt dans `ambiance_catalog.py`.
- [ ] **Calibrer `ROT_*`** à l'oreille · duck ambiance (`hippo_duck_08`) · doc §5 à jour.
- [ ] **`gen_assoc_hippo.py`** — brancher le vrai classeur (events mock tant que feuille vide).

### Reconstruction

Spec Simon 21 août · [Q29–Q36](./Q&A.md#j-reconstruction--spec-simon-reçue-le-21-août).

- [ ] **Réécrire [`Reconstruction.md`](../Zones/Reconstruction.md)** — moteur compositionnel ([Q29](./Q&A.md#q29)=A).
- [ ] **`gen_formes_recon.py`** — recettes · garde-fous R12/R13 · proto sur matière actuelle.
- [ ] **Supprimer `recon_pulse_*`** · bibliothèque spatiale §14 · chaîne FX mutabilité 1–3.
- [ ] **Batch 4 Recon** — re-découper si master Simon OK · regen catalogue.

### Boucle · lecteur · niveaux

- [ ] **Câbler `gain_db` au lecteur** — troisième mot playlists · `player_state_08` (calcul fait, pas entendu).
- [ ] **31 fragments plafonnés +12 dB** — écouter · écarter ou traiter cas par cas.
- [ ] **Boucle 08** — aligner preset état 3 vs inject si le 08 reprend le pattern 07.

### Piézo · présence

- [ ] **`presence_08`** — fondu nappes 0,5–2 s · retirer `s6_cortex_hold` · lier `INTERRUPTIBLE` ([Q14](./Q&A.md#q14), [Q27](./Q&A.md#q27)).

---

## 3. Matière · pipeline

- [ ] **Batch 4 Recon** — master silencieux corrigé chez Simon ? → `slice_batch4.py --only reconstruction` · `gen_catalogue_batch4.py`.
- [ ] **Remplir classeur** — collègue : `catalogue_batch4.xlsx` · V6 : `catalogue_fragments.xlsx` · axes immédiats : `famille_son`, `usage_prefere`, `type_ambiance`.
- [ ] **Seuil 30 s nappes** — `AMBI_MIN_SEG` dans `slice_opacite_v3.py` ([Q3](./Q&A.md#q3)=B) · 52 courts déjà sur disque restent orphelins.
- [ ] **Intro Cortex −27 dB** — question à Simon (250 premières secondes du master).
- [ ] **Master ambiance Hippo dédié** — [Q2](./Q&A.md#q2) · matière différente du Cortex.
- [ ] **Belgique / Congo** — [Q4](./Q&A.md#q4) · bloqué remplissage `contexte`.

---

## 4. V8 — sélecteur attributs (après classeur)

Spec : [`../Matiere/Attributs.md`](../Matiere/Attributs.md) §6. **Ne pas coder avant remplissage partiel du tableau.**

- [ ] Colonnes Recon §26.1 dans `gen_catalogue_xlsx.py` ([Q32](./Q&A.md#q32)).
- [ ] **Audit `gen_paires.py`** (mode rapport) — mesurer si C1/C2 tiennent ([Q4](./Q&A.md#q4)).
- [ ] **`gen_paires.py`** + **`gen_ambiance_cortex.py`** — bloqué par classeur.
- [ ] **Lecteur Pd chemin forcé** — extension `player_state_08` (sans casser anti-doublon Hippo).
- [ ] `s6_tag_hook` — laisser tel quel jusqu'au sélecteur.

---

## 5. Salle · calibrage

- [ ] **Plan salle** — 2 baffles ambiance non adjacents (CWB · Bozar).
- [ ] **Piézo matériel** — combien, où (Loumana / salle).
- [ ] **Calibrage FORCE/AUTO** — 8 HP · contraste Cortex flou / Hippo suivable / Recon composition.

---

## 6. Plus tard — envies, pas des tâches V1

- Buffer Boucle réel (`writesf~`) — écarté [Q35](./Q&A.md#q35)=A.
- Fragment voyageur inter-zones · graphe mot/timbre · segmentation live Pd · phaser/granulaire.
- Réverb « pièce voisine » Cortex ([Q18](./Q&A.md#q18)) — delay V1 suffit pour l'instant.
- 5 voies Hippocampe Simon (H45) — rejeté V1 · FSM = 4 voyageurs.
- Sous-zone Hippocampe–Ambiance · `REVENIR` — rejetés.

---

## Archive — bugs résolus

<details>
<summary>20 août – 9 sep. 2026</summary>

- [x] README racine périmé · `scripts/README.md` slice v2 · `slice_opacite_v3` chemin WIP + `rmtree` · rsync Pi WIP · import `pdbuild` proto06 · `.gitignore`.
- [x] ID stables · découpe incrémentale · colonnes classeur §5 · git init.
- [x] Détection Scarlett · `verifier_sons.py` · normalisation spec [Q9](./Q&A.md#q9).
- [x] Proto 08 créé · 12 voices · 2 nappes · gestes · spatialisation.
- [x] Proto 07 regen AMBIANCE · registre gains · Boucle L10 · hippo sens · presets07 doc.

</details>
