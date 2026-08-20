# Matière — pipeline des samples

**20 août 2026.** Vérité matière : ce fichier. Ce qui sonne : [`../etatactuel.md`](../etatactuel.md). Attributs et tags : [`Attributs.md`](./Attributs.md).

---

## Deux métiers

| | Simon (Ableton) | Loumana (ici) |
|--|-----------------|---------------|
| Livrable | **4 pistes longues** (~48 min en V6), les samples séparés par des silences techniques | **un wav par sample** dans `SONS_V3/` |
| Pistes | Cortex · Cortex ambiances · Hippocampe · Reconstruction | pas de piste Boucle |
| Suite | export | script de découpe → 3 sous-dossiers par strate → classification |

**`SONS_V3/` est le seul dossier audio du projet** depuis le 20 août. `SONS/`, `SONS_V2/`, `SONS_FINAL/` et `SONS_PROTOTYPE/` ont été supprimés (3 Go). Conséquence assumée : les patches Proto 06 sont muets.

```text
SONS_V3/
  WIP/Opacité V6/   ← les 4 masters de Simon. IRREMPLAÇABLE. Ne jamais toucher.
  AMBIANCE/         ← pool partagé (toutes zones)
  CORTEX/ HIPPOCAMPE/ RECONSTRUCTION/   ← paroles : FRAGMENTS + LONG_MOYEN
```

Tout sous `SONS_V3/` sauf `WIP/` est **dérivé** et peut être régénéré. `WIP/` ne peut pas.

---

## Pipeline

```text
SONS_V3/WIP/Opacité V6/  — 4 masters (silences entre les samples)
        │
        ▼
  slice_opacite_v3.py  ──►  registre_ids.csv  (ID stables, incrémental)
        │
        ▼
  SONS_V3/<ETAT>/{FRAGMENTS,LONG_MOYEN}/*.wav
  SONS_V3/AMBIANCE/*.wav                    ← pool partagé
        │
        ▼
  gen_prototype_07_8hp.py  →  pd/lib/playlists07/slot_*.txt
        │
        ▼
  moteur 07 : tirage au hasard dans le dossier    ← aujourd'hui
  moteur 08 : sélection par attributs             ← plus tard, Attributs.md
```

```bash
python3 scripts/slice_opacite_v3.py --dry-run   # voir sans écrire
python3 scripts/slice_opacite_v3.py             # découpe incrémentale
python3 scripts/gen_prototype_07_8hp.py         # patch + playlists
python3 scripts/gen_catalogue_xlsx.py           # classeur (conserve les colonnes remplies)
```

Attention, le mot « ambiance » dans un nom de fichier master ne détermine pas le rôle d'ambiance dans le moteur.

---

## Arborescence

```text
SONS_V3/
  AMBIANCE/                    ← nappes partagées (69 wav en V6)
  CORTEX/          FRAGMENTS/  LONG_MOYEN/
  HIPPOCAMPE/      FRAGMENTS/  LONG_MOYEN/
  RECONSTRUCTION/  FRAGMENTS/  LONG_MOYEN/
```

| Master | Destination | Règle de découpe |
|--------|-------------|------------------|
| `… Cortex ambiance.wav` | `SONS_V3/AMBIANCE/` | atomes ≥ 2 s |
| `… Cortex.wav` | `CORTEX/FRAGMENTS` si < 13 s, `CORTEX/LONG_MOYEN` si ≥ 13 s | |
| `… Hippocampe.wav` | idem dans `HIPPOCAMPE/` | collage des trous ≤ 1,8 s |
| `… Reconstruction.wav` | idem dans `RECONSTRUCTION/` | pas de collage |

Nommage produit : `C###_v3_cortex.wav`, `A##_v3_cortex_ambiance.wav` (pool `AMBIANCE/`), `H###_v3_hippocampe.wav`, `R###_v3_reconstruction.wav`.

---

## ID stables — découpe incrémentale

**Résolu le 20 août** ([Q21](../Backlog/Q&A.md#q21) = option A). Avant, la découpe vidait `SONS_V3/` et renumérotait tout : les ID bougeaient à chaque passage, et le travail de classification à l'oreille aurait été perdu à la première nouvelle livraison de Simon.

Maintenant :

| Règle | Détail |
|-------|--------|
| Jamais de suppression | `SONS_V3/` n'est plus vidé. `WIP/` n'est jamais touché |
| Jamais de renumérotation | un numéro attribué ne sera jamais réattribué à un autre segment |
| Appariement | par (master, état, rôle, temps de début **± 0,3 s**) — un segment survit à un petit changement de détection de silence |
| Nouveau segment | reçoit le numéro suivant, à la fin de la série |
| Rangement manuel respecté | un wav déplacé à la main n'est pas remis en place. `--reclasser` pour forcer |
| Orphelins | une entrée du registre sans segment correspondant est **signalée**, jamais supprimée |

Le registre est [`registre_ids.csv`](./registre_ids.csv) : une ligne par wav, avec son master d'origine et ses temps. C'est lui qui rend les ID stables ; ne pas l'éditer à la main.

Deux colonnes ne sont **pas** écrites par la découpe : `niveau_db` et `gain_db` viennent de `scripts/normaliser_niveaux.py` (sonie mesurée, et gain de normalisation calculé pour l'atteindre). Elles sont malgré tout déclarées dans `REG_FIELDS`, sans quoi la découpe suivante les effacerait sans bruit. Aucun wav n'étant modifié, la mesure porte toujours sur le fichier d'origine : les deux scripts peuvent être relancés dans n'importe quel ordre.

Amorcé depuis l'inventaire du 18 août par `scripts/proto07/amorcer_registre_ids.py` (migration unique). Vérification : `slice_opacite_v3.py --dry-run` doit annoncer **0 nouveau, 526 réutilisés**.

Échappatoire : `--reset --yes` refait tout à zéro et **perd les ID**. À n'utiliser que si la classification est vide.

## Problème connu restant

**La règle des 2 s pour les ambiances contredit la spec.** Simon demande des ambiances de 30 s à 7 min. La découpe produit des atomes à partir de 2 s, re-déclenchés toutes les 14 s. Voir [Q3](../Backlog/Q&A.md#q3).

---

## État des pools

| Pool | Fichiers | Lu par |
|------|----------|--------|
| `CORTEX/FRAGMENTS` | 48 | Cortex L1–L6 (Proto 07) |
| `CORTEX/LONG_MOYEN` | 42 | Cortex L1–L6 |
| `SONS_V3/AMBIANCE/` | 69, **partagé** | nappes Cortex (Proto 07) · futur Hippo/Recon via classeur |
| `HIPPOCAMPE/FRAGMENTS` | 69 | voyageurs |
| `HIPPOCAMPE/LONG_MOYEN` | 10 | voyageurs |
| `RECONSTRUCTION/FRAGMENTS` | 287 | Recon L2, interruptions |
| `RECONSTRUCTION/LONG_MOYEN` | **1** | Recon L1, le fil — **insuffisant** |

Les deux déséquilibres marqués en gras sont des manques de matière, pas des réglages. Voir [`../Backlog/TO DO.md`](../Backlog/TO%20DO.md) §4.

---

## Ce que le moteur lit aujourd'hui

| Zone | Dossiers | Couche |
|------|----------|--------|
| Cortex L1–L6 | `CORTEX/FRAGMENTS` + `CORTEX/LONG_MOYEN` | 3 paires sur HP1–3 |
| Cortex nappes | `SONS_V3/AMBIANCE/` | 5 nappes HP4–8 (Proto 07) |
| Hippo voyageurs | `HIPPOCAMPE/FRAGMENTS` + `LONG_MOYEN` | 4 couches |
| Hippo nappe | `SONS_V3/AMBIANCE/` (filtre classeur à venir) | L9 |
| Recon fil | `RECONSTRUCTION/LONG_MOYEN`, repli `FRAGMENTS` | L1 |
| Recon interruptions | `RECONSTRUCTION/FRAGMENTS` | L2 |
| Boucle | tout `HIPPOCAMPE` + `RECONSTRUCTION/FRAGMENTS` | couche 10 |

Le tirage est au **hasard** dans le dossier, en évitant seulement le dernier fichier joué sur cette couche. Aucun attribut n'est lu.

Les durées d'état de la FSM (40 / 50 / 120 s) ne viennent pas des dossiers : elles sont dans `presets07.py`.

---

## Classification

Classeur : [`catalogue_fragments.xlsx`](./catalogue_fragments.xlsx) — **4 feuilles** : Cortex / Hippocampe / Reconstruction (paroles) + **Ambiances** (pool `SONS_V3/AMBIANCE/`). Schéma [`Attributs.md`](./Attributs.md) §5.

**On peut commencer à remplir** : les ID sont stables et `gen_catalogue_xlsx.py` conserve les cellules déjà remplies quand on le relance (clé = ID). Une nouvelle livraison de Simon ajoutera des lignes vides sans toucher aux vôtres.

---

## Écarts assumés avec le guide Ableton de Simon

Pure Data ne découpe pas en direct. `TRACE` n'est pas une piste. Les durées d'états sont décidées à l'oreille, pas dans le guide. Les 4 pistes sont les masters reçus, pas les 4 zones du moteur — il n'y a pas de master Boucle.
