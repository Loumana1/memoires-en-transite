# Journal de découpe — Opacité fin V2 (Proto 07)

**Date :** 17 août 2026 — ambiance remplacée par Opacité fin V3 (WIP)
**Source :** `WIP/`
**Sortie :** `SONS_V2/` (l’ancien `SONS/` n’est pas touché)
**Script :** `scripts/slice_opacite_v2.py`

Downmix **mono 48 kHz**. Table brute : [`16_proto_07_journal_decoupe.csv`](./16_proto_07_journal_decoupe.csv).

## Compteurs

| État | Dossier | N |
|------|---------|---|
| AMBIANCE | OK | 68 |
| CORTEX | ECART | 33 |
| CORTEX | FRAGMENTS | 14 |
| HIPPOCAMPE | ECART | 21 |
| HIPPOCAMPE | OK | 7 |
| HIPPOCAMPE | SOUPLE | 6 |
| RECONSTRUCTION | COURT | 85 |
| RECONSTRUCTION | MOYEN | 3 |

**Total fichiers :** 237

## Plages visées vs hors plage

| Pool | Cible | Accepté ici |
|------|-------|-------------|
| Cortex FRAGMENTS | 13–30 s | strict |
| Cortex ECART | — | hors 13–30 s à la découpe ; **moteur 17 août : tout lu** |
| Ambiance | silences ≥1 s (comme Cortex) | atomes ≥ 2 s |
| Hippo OK | 5–10 s | après collage des atomes (trou ≤ 1,8 s) |
| Hippo SOUPLE | — | 4,5–12 s |
| Recon COURT | 0,2–5 s (MICRO/TRACE) | atomes isolés, **sans collage** |
| Recon MOYEN / PRINCIPAL | 5–30 s / ≥ 30 s | **une région continue** (silence technique = coupe) |

## Minimums UC-A04

- Cortex fragments 13–30 s : **14** OK
- Hippo 4,5–12 s (OK+SOUPLE) : **13** OK
- Recon PRINCIPAL : **0** INSUFFISANT (besoin ≥ 2)
- Recon COURT : **85** OK
- Ambiance lits : **68**

## Suite

Le collage Recon (trou ≤ 8 s) a été retiré : un silence technique sépare deux fichiers. Il n’y a **pas** de PRINCIPAL ≥ 30 s continu dans le master actuel — à préparer dans Ableton (piste RECONSTRUCTION, une phrase / texture d’une traite, silences seulement *entre* les clips).

Moteur 07 : relancer `python3 scripts/gen_prototype_07_8hp.py` après chaque découpe.  
Ce que le patch **lit** : [`etatactuel.md`](./etatactuel.md) (Cortex = FRAGMENTS + ECART). Pourquoi : [`log.md`](./log.md).
