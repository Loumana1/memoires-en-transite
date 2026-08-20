# Journal de découpe — Opacité V6 (SONS_V3)

**Date :** 18 août 2026
**Source :** `Opacité V6/`
**Sortie :** `SONS_V3/` (`SONS/` et `SONS_V2/` intacts)
**Script :** `scripts/slice_opacite_v3.py`

Downmix **mono 48 kHz**. Table brute : [`19_proto_07_journal_decoupe_v3.csv`](./19_proto_07_journal_decoupe_v3.csv).

Sous-dossiers **identiques** par strate : `FRAGMENTS` · `AMBIANCE` · `LONG_MOYEN`.

## Compteurs

| État | Dossier | N |
|------|---------|---|
| CORTEX | FRAGMENTS | 48 |
| CORTEX | AMBIANCE | 69 |
| CORTEX | LONG_MOYEN | 42 |
| HIPPOCAMPE | FRAGMENTS | 69 |
| HIPPOCAMPE | AMBIANCE | 0 |
| HIPPOCAMPE | LONG_MOYEN | 10 |
| RECONSTRUCTION | FRAGMENTS | 287 |
| RECONSTRUCTION | AMBIANCE | 0 |
| RECONSTRUCTION | LONG_MOYEN | 1 |

**Total fichiers :** 526

## Règles

| Master | Destination |
|--------|-------------|
| Cortex ambiance | `CORTEX/AMBIANCE` (atomes ≥ 2 s) |
| Cortex / Hippo / Recon | `FRAGMENTS` si < 13 s · `LONG_MOYEN` si ≥ 13 s |
| Hippo | collage trou ≤ 1,8 s, max 12 s (comme V2) |

Moteur 07 : relancer `python3 scripts/gen_prototype_07_8hp.py` après chaque découpe.
Pipeline : [`source_samples.md`](./source_samples.md).

