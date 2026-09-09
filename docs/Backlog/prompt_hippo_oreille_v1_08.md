# Prompt IA — Hippocampe oreille V1 (Proto 08)

Copier-coller ce prompt dans une session Agent (Claude / Cursor).  
Spec : [`spec_hippo_oreille_v1_08.md`](./spec_hippo_oreille_v1_08.md).  
Contexte : [`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) **§9–§10**.

---

## Mission

Implémenter le **chantier oreille Hippocampe** demandé par Loumana (23 août) :

1. **Anti-doublon** — le même sample ne doit **jamais** jouer en même temps sur deux couches Hippo (L1–L4).
2. **Mouvement fluide perceptible** — les rotations (mode 1 / phi ambisonique) sont trop lentes et trop rares ; on n'entend que des sauts.
3. **Defaults spatiaux** — monter les `rot` / rééquilibrer l'occurrence fluide vs saut, en gardant le calibrage **une recette à la fois** via `; s6_hippo_motion N`.
4. **HP7 trop fort** — trim provisoire −3 dB sur HP7 (ajustable live).
5. **Nappes Hippo** — préparer le même mécanisme que les favoris Cortex (`FAVORIS_HIPPO`). Si la liste n'est pas encore fournie : constante **vide ou TODO claire** + wiring prêt ; **ne pas inventer** une liste de stems.

**Ne pas** : clôturer / marquer FIGÉ · passer à 5 voies FSM · toucher Cortex plans · freeverb · éditer les `.pd` à la main (uniquement générateurs + regen).

---

## Contexte repo (lire avant de coder)

| Fichier | Rôle |
|---------|------|
| `scripts/proto08/proto08_lib/hippo_recipes.py` | 5 recettes Q26 + `INIT_LAYERS` |
| `scripts/proto08/proto08_lib/gen_libs08.py` | `gen_hippo_motion_08`, `gen_hippo_assoc_08`, `gen_player_state_08` |
| `scripts/gen_assoc_hippo.py` | Précalcule `pd/lib/hippo_assoc/events.txt` (sources souvent **perdues** à l'écriture) |
| `pd/lib/spatial_router_06.pd` | Mode 1 = `phasor~` × `rot` → encode_2d (fluide) ; 2/3/4 = sauts |
| `scripts/proto08/proto08_lib/layout08.py` | `Speaker.trim_db` · trim live `s6_trim{n}` |
| `scripts/shared/ambiance_catalog.py` | Modèle `FAVORIS_CORTEX` à répliquer pour Hippo |
| `scripts/proto08/proto08_lib/sons_audit08.py` | Pools Hippo / `usable_ambiance(..., "HIPPOCAMPE")` |
| `docs/Zones/Hippocampe.md` §10 | Priorités Loumana |

Régénération : `python3 scripts/gen_prototype_08_8hp.py`  
(et `python3 scripts/gen_assoc_hippo.py` si events changent)  
Patch : `pd/prototype_08_fsm_8hp.pd`

---

## Étape 1 — Anti-doublon (priorité absolue)

### Problème

- Chaque couche tire au hasard dans **son** slot playlist.
- `gen_assoc_hippo.py` calcule un `source` puis écrit seulement `play {layer} 0` → le chemin est **jeté**.
- Résultat : L1 et L3 peuvent ouvrir le **même wav** → ×2 en volume, très dérangeant.

### Cible

**Invariant :** à tout instant, les chemins (ou stems) joués sur L1–L4 Hippo sont **deux à deux distincts**.

### Implémentation attendue (les deux couches)

**A. Côté générateur d'events (`gen_assoc_hippo.py`)**

- Ne jamais choisir `long_a == long_b` au démarrage (aujourd'hui deux `rng.choice(longs)` indépendants).
- Sur toute la séquence : maintenir un set des sources **actives** par couche ; un nouveau `play` sur une couche doit `_pick_other` hors des sources déjà actives (et hors self).
- Écrire le fichier dans `events.txt`, ex. :
  ```text
  0 play 1 SONS_V3/HIPPOCAMPE/.../H012_....wav
  ```
  ou stem + convention claire documentée.
- Mettre à jour `gen_hippo_assoc_08` pour émettre l'index **avant** le bang — **pas** via `player_state_08` (voir piège ci-dessous).

**B. Côté Pd / player (filet de sécurité)**

Même si l'assoc bange sans chemin (FSM bangs, etc.) :

- Avant d'ouvrir un tirage aléatoire en état Hippo, comparer au nom courant des autres couches (`s6_sample1`…`s6_sample4` existent déjà dans le patch).
- Si collision → **retirer** (re-random jusqu'à unique, plafond d'essais, fallback autre fichier du pool).

**⛔ Piège (23 août — silence total sans erreur console)**

- **Interdit** : logique anti-doublon dans `gen_player_state_08` (receives `s6_hippo_path*` / `s6_hippo_idx*`, arg2 layer, spigots sur branches slot). Le lecteur est instancié 14× ; une sortie vers les ~28 branches slot **tue tout le son**.
- **Interdit** sans test iem : `list index`, `text define` + `add`, `t b s` pour router des symboles.
- **Autorisé** : `gen_assoc_hippo.py` (Python) · tables via fichier + `read -c` · **future** abstraction `hippo_play_08` **par couche** dans `gen_patch08` (entre `r_h{N}` et `p{N}`).

Critère done Pd : en FORCE Hippo 30 s, **aucun** doublon audible / visible dans SAMPLES_EN_COURS — **sans** régression Cortex (son + UI).

---

## Étape 2 — Fluide perceptible + defaults spatiaux

### Problème ressenti

Loumana n'identifie que des **sauts**. Le fluide (mode 1 / pan ambisonique) existe mais :

- `rot` trop bas (0,03–0,07 Hz) ;
- 3 recettes sur 5 = sauts uniquement ;
- mode 4 = hops locaux (xfade 35 ms), **pas** un pan.

### Changements dans `hippo_recipes.py` (defaults de départ — Loumana calibrera ensuite)

Monter nettement les rotations mode 1, par ex. (ordre de grandeur, ajustable) :

| Recette | Avant | Cible indicative |
|---------|-------|------------------|
| 0 Contre-rotation pan | rot 0,04 / 0,07 | **0,18 / 0,32** (ou proche) |
| 4 Fixe + orbite | rot 0,03 | **0,22** |

Documenter les constantes en tête de fichier (`ROT_*`).

### Occurrence fluide

Dans `gen_hippo_motion_08`, le tirage `random 5` est uniforme.  
Changer pour **biais fluide** (ex. poids : recettes 0 et 4 plus fréquentes — 0,0,0,1,2,3,4,4 ou table de poids explicite). Garder `; s6_hippo_motion N` qui force une seule recette (debug calibrage).

### Optionnel si simple

Un commentaire / helper dans la doc §10 : « pour calibrer, forcer 0 puis 4, puis les sauts ».

**Ne pas** allonger massivement tous les `xfade` des sauts en croyant créer du fluide — ça adoucit le hop seulement.

Critère done : en forçant recette 0, on **entend** une masse qui tourne en quelques secondes, pas un faux fixe.

---

## Étape 3 — Trim HP7

Dans `layout08.py`, Speaker HP7 : `trim_db=-3.0` (provisoire).

Vérifier que le patch applique bien `trim_linear` / `s6_trim{n}` (déjà prévu).  
Documenter : `; s6_trim7 -6` pour aller plus loin en salle sans regen.

**Ne pas** toucher aux autres trim sans demande.

---

## Étape 4 — Nappes Hippo dédiées (préparation)

Modèle Cortex : `FAVORIS_CORTEX` dans `ambiance_catalog.py` → slots Cortex.

À faire :

1. Ajouter `FAVORIS_HIPPO = ()`  **tuple vide** + commentaire :
   ```text
   # Loumana fournira la liste (stems Axx). Tant que vide → comportement actuel
   # (usable_ambiance HIPPOCAMPE / repli pool mélodique).
   ```
2. Brancher `usable_ambiance(root, "HIPPOCAMPE")` (ou équivalent slot 41) pour utiliser **uniquement** les favoris quand le tuple est **non vide** (comme Cortex).
3. Doc §10 + TO DO : « coller la liste ici ».

**Interdit :** inventer des stems A53… au feeling.

Quand Loumana enverra la liste dans un prochain prompt : un one-liner remplit `FAVORIS_HIPPO` + regen.

---

## Doc + log (obligatoire)

1. [`docs/Zones/Hippocampe.md`](../Zones/Hippocampe.md) §10 — cocher / préciser ce qui est **codé** vs encore à l'oreille.
2. [`docs/Backlog/TO DO.md`](./TO%20DO.md) §1 Hippo oreille — cocher anti-doublon / rot / trim ; nappes = « wiring prêt, liste à venir ».
3. Strophe append-only [`docs/log.md`](../log.md).
4. Une ligne [`docs/etatactuel.md`](../etatactuel.md) si le comportement Hippo change à l'écoute.

---

## Interdits

- Modifier Proto 06 / `spatial_router_06.pd` sauf **lecture** (les `rot` passent déjà par `s6_l$_rot`).
- Casser Cortex nappes / gestes spectraux / seed.
- Marquer la zone FIGÉ.
- Éditer à la main `pd/lib/hippo_*.pd` ou `prototype_08_fsm_8hp.pd`.

---

## Tests de validation

1. Regen sans erreur + Pd headless : aucune « couldn't create ».
2. FORCE Hippo : SAMPLES_EN_COURS — **pas** deux fois le même basename.
3. `; s6_hippo_motion 0` — rotation **audible** en &lt; ~5–8 s de parcours angulaire ressenti.
4. `; s6_hippo_motion 2` — toujours des sauts (régression OK).
5. `; s6_trim7 -3` / valeur layout — HP7 moins dominant (oreille).
6. Cortex AUTO inchangé au smoke test.

---

## Livrable attendu (réponse courte)

- Diff générateurs + `hippo_recipes` + `layout08` + `ambiance_catalog` (+ assoc).
- Patch régénéré.
- Comment forcer une recette / trim / où coller `FAVORIS_HIPPO`.
- Ce qui reste **uniquement** à l'oreille de Loumana (valeurs rot exactes, liste nappes).
