# Spec — Hippocampe oreille V1 (Proto 08)

**23 août 2026.** Priorités Loumana · détail zone [`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) §10.  
Prompt IA : [`prompt_hippo_oreille_v1_08.md`](./prompt_hippo_oreille_v1_08.md).

## Objectif

Rendre l'Hippocampe **écoutable** : plus de doublons monstrueux, du mouvement **fluide** perceptible, recettes spatiales calibrables, nappes dédiées (liste Loumana), trim HP7.

**Hors scope :** 5 voies FSM · classeur tags complet · sous-zone Hippocampe–Ambiance · figer FIGÉ sans oreille Loumana.

## Quatre livrables

| # | Sujet | Done quand |
|---|--------|------------|
| 1 | Anti-doublon wav simultané L1–L4 | Python : séquence sans doublon. Pd : **pas** dans `player_state_08` — abstraction par couche ou nodup patch (TODO) |
| 2 | Fluide perceptible + defaults spatiaux | Recettes 0/4 avec `rot` nettement plus rapide ; part fluide ↑ ; debug force recette intact |
| 3 | Trim HP7 | Constante `layout08` + doc `; s6_trim7` (valeur provisoire −3 dB, Loumana ajuste) |
| 4 | Nappes Hippo dédiées | `FAVORIS_HIPPO` (ou liste) dans `ambiance_catalog` — **placeholder** si liste vide ; Loumana remplit ensuite |

## Diagnostic (ne pas rediscuter)

- `rot` 0,03–0,07 Hz → tour en 14–33 s → inaudible comme mouvement.
- 3/5 recettes = sauts purs ; mode 4 = hops voisins ≠ pan fluide.
- `events.txt` : séquence Python sans doublon + slot/index — **Pd ignore l'index** tant que le wiring n'est pas refait hors lecteur.
- HP7 : `trim_db=0` partout ; boost ressenti = salle ou decode — trim live d'abord.

## Piège Pd — `player_state_08` (23 août 2026)

**Ne jamais** câbler anti-doublon (chemin, index, spigots) **dans** `gen_player_state_08` :

- Abstraction **partagée** 14× · ~28 branches slot en parallèle.
- Une sortie `[i idx]` ou `symbol` vers toutes les branches = **lecteur mort** (silence, UI vide, **sans** erreur console).
- Tentatives invalides : `s6_hippo_path*`, `s6_hippo_idx*` + arg2, `list index`, `text add`, `t b s`.

**Voie correcte (future)** : `hippo_play_08` ou routeur dans `gen_patch08` — **1 instance / couche** L1–L4, entre `r_h*` et `p*`.

Détail : [`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) §10 « Piège ».

## Non-régression

- `; s6_hippo_motion 0..4` continue de forcer une recette.
- Cortex / Recon / nappes Cortex inchangés.
- Regen `python3 scripts/gen_prototype_08_8hp.py` + Pd headless sans erreur.
- Doc §10 + TO DO + log mis à jour.
