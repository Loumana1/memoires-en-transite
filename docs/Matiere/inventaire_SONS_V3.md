# Inventaire — SONS_V3 (découpe Opacité V6)

**Généré le :** 2026-08-20
**Source :** `SONS_V3/WIP/Opacité V6/`
**Sortie :** `SONS_V3/<ÉTAT>/{FRAGMENTS,AMBIANCE,LONG_MOYEN}/`
**Script :** `scripts/slice_opacite_v3.py`

Downmix **mono 48 kHz**. Table brute : [`inventaire_SONS_V3.csv`](./inventaire_SONS_V3.csv) · registre des ID : [`registre_ids.csv`](./registre_ids.csv).

## Compteurs

| État | Dossier | N |
|------|---------|---|
| CORTEX | FRAGMENTS | 90 |
| CORTEX | AMBIANCE | 27 |
| CORTEX | LONG_MOYEN | 42 |
| HIPPOCAMPE | FRAGMENTS | 69 |
| HIPPOCAMPE | AMBIANCE | 0 |
| HIPPOCAMPE | LONG_MOYEN | 10 |
| RECONSTRUCTION | FRAGMENTS | 287 |
| RECONSTRUCTION | AMBIANCE | 0 |
| RECONSTRUCTION | LONG_MOYEN | 1 |

**Total fichiers :** 526

## Dernière exécution

| | N |
|--|--|
| ID réutilisés | 526 |
| nouveaux ID | 0 |
| inchangés sur le disque | 484 |
| rangés à la main, respectés | 42 |
| déplacés (`--reclasser`) | 0 |
| ré-exportés (fichier manquant) | 0 |
| entrées sans segment (conservées) | 0 |

## Règles

| Master | Destination |
|--------|-------------|
| Cortex ambiance | `CORTEX/AMBIANCE` (atomes ≥ 2 s) |
| Cortex / Hippo / Recon | `FRAGMENTS` si < 13 s · `LONG_MOYEN` si ≥ 13 s |
| Hippo | collage trou ≤ 1,8 s, max 12 s |

## ID stables

La découpe est **incrémentale** : elle ne vide jamais `SONS_V3/` et ne renumérote jamais. Un segment déjà connu garde son nom, apparié via (master, état, rôle, début ± 0.3 s). Un nouveau segment reçoit le numéro suivant. Le travail de classification à l'oreille est conservé.

Les masters sont dans `SONS_V3/WIP/` et ne sont jamais touchés.

Moteur 07 : relancer `python3 scripts/gen_prototype_07_8hp.py` après chaque découpe.
Pipeline : [`Pipeline.md`](./Pipeline.md) · attributs : [`Attributs.md`](./Attributs.md).

⚠ Fichier **généré**, écrasé à chaque découpe.

