# Source — samples (pipeline réel)

**18 août 2026.** Vérité matière : ce fichier. Runtime : [`etatactuel.md`](./etatactuel.md).  
Catalogue à remplir : [`catalogue_samples.csv`](./catalogue_samples.csv).  
Backlog (moteur + tags) : [`backlog/18_catalogue_tags.md`](./backlog/18_catalogue_tags.md).

Guide Ableton de Simon (15 août 2026) : préparation des **4 masters**. Pas le contrat des durées d’états ni du patch.

---

## Deux métiers

| | Simon (Ableton) | Loumana (ici) |
|--|-----------------|---------------|
| Livrable | **4 pistes longues** (~48 min V6), samples séparés par des **silences techniques** | **Un wav par sample** dans `SONS_V3/` |
| Pistes | Cortex · Cortex ambiances · Hippocampe · Reconstruction | Pas de piste Boucle |
| Suite | Export | Script de découpe → **mêmes 3 sous-dossiers dans chaque strate** → catalogue tags |

`SONS/` (proto 06) et `SONS_V2/` (sélection précédente) : **intacts**. Le 07 lit **`SONS_V3/`**.

---

## Pipeline

```text
4 masters V6  (silences entre samples)
        │
        ▼
  slice_opacite_v3.py
        │
        ▼
  SONS_V3/<ETAT>/{FRAGMENTS,AMBIANCE,LONG_MOYEN}/*.wav
        + catalogue_samples.csv
        │
        ▼
  moteur 07 (dossiers)     tags = plus tard
```

```bash
python3 scripts/slice_opacite_v3.py
python3 scripts/gen_prototype_07_8hp.py
```

Masters actuels : `SONS_V2/WIP/Opacité V6/` (préfixe « ambiance » dans le nom de fichier ≠ rôle ambiance).

---

## Arborescence — identique dans chaque strate

```text
SONS_V3/
  CORTEX/          FRAGMENTS/  AMBIANCE/  LONG_MOYEN/
  HIPPOCAMPE/      FRAGMENTS/  AMBIANCE/  LONG_MOYEN/
  RECONSTRUCTION/  FRAGMENTS/  AMBIANCE/  LONG_MOYEN/
```

| Master | Dossier |
|--------|---------|
| `… Cortex ambiance.wav` | `CORTEX/AMBIANCE` (atomes ≥ 2 s) |
| `… Cortex.wav` | `CORTEX/FRAGMENTS` (< 13 s) ou `LONG_MOYEN` (≥ 13 s) |
| `… Hippocampe.wav` | idem dans `HIPPOCAMPE/` (collage trou ≤ 1,8 s) |
| `… Reconstruction.wav` | idem dans `RECONSTRUCTION/` (pas de collage) |

Hippo / Recon n’ont **pas** de 5ᵉ master ambiance pour l’instant → `AMBIANCE/` vides. L9 Hippo **replie** sur `CORTEX/AMBIANCE`. Tu peux y glisser des wav à la main plus tard.

Inventaire machine : [`19_proto_07_journal_decoupe_v3.csv`](./19_proto_07_journal_decoupe_v3.csv).  
Ancien V2 : [`16_proto_07_journal_decoupe.csv`](./16_proto_07_journal_decoupe.csv).

---

## Ce que le moteur lit

| Zone | Dossiers | Couche |
|------|----------|--------|
| Cortex L1–L8 | `FRAGMENTS` + `LONG_MOYEN` | fragments |
| Cortex L9 | `CORTEX/AMBIANCE` | nappe 1 HP |
| Hippo voyageurs | `FRAGMENTS` + `LONG_MOYEN` (≥ 8 s vs plus court) | 4 couches |
| Hippo L9 | `HIPPOCAMPE/AMBIANCE` si non vide, sinon nappe Cortex | nappe qui voyage |
| Recon L1 | `LONG_MOYEN` (repli `FRAGMENTS`) | fil |
| Recon L2 | `FRAGMENTS` | interruptions |
| Recon L9 | off | — |

Les **durées d’états** FSM (40 / 50 / 120 s) ne viennent pas des dossiers.

---

## Catalogue (oreille)

À remplir : [`catalogue_fragments.xlsx`](./catalogue_fragments.xlsx) — 3 feuilles (Cortex, Hippocampe, Reconstruction).  
ID + type (court / long / ambiance) en **vert**, auto. Phrase, attributs, comportements = vous.  
Régénérer les IDs (garde vos colonnes 3–5) : `python3 scripts/gen_catalogue_xlsx.py`.  
Ancien tableau : [`catalogue_samples.csv`](./catalogue_samples.csv). **Pas lu par le patch.**

---

## Écarts vs le guide Ableton

Inchangés : Pd ne découpe pas en live ; TRACE n’est pas une piste ; durées d’états = oreille ; 4 pistes = masters reçus.
