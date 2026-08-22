# Zone Reconstruction — comportement sonore

**Mise à jour 21 août 2026** — [Q29](../Backlog/Q&A.md#q29)=A : moteur **compositionnel** (spec Simon), pas « zone lisible ».

Spec source : [`Specifications_Pure_Data_Reconstruction_Reconstruction_Ambiance.md`](../Sources/Specifications_Pure_Data_Reconstruction_Reconstruction_Ambiance.md). Décisions : [Q&A §J](../Backlog/Q&A.md#j-reconstruction--spec-simon-reçue-le-21-août).

---

## 1. Intention

La Reconstruction **compose** un territoire sonore provisoire : agencement de fragments, sutures, silences, mouvements spatiaux, puis dissolution. Ce n'est plus une zone où l'on « comprend » — la reconnaissabilité varie selon la forme (courbe CLAIR ↔ OPAQUE).

Durée d'état : **120 s** (`CYCLE1_8HP`).

---

## 2. Invariants V1 (Proto 08)

1. **Moteur de formes** — `gen_formes_recon.py` précalcule une recette ; Pd lit `pd/lib/recon_formes/events.txt`. **`recon_pulse_*` supprimé** ([Q31](../Backlog/Q&A.md#q31)).
2. **Deux couches actives** — L1 fil (long) + L2 interruptions (courts). Pas de sous-zone Reconstruction–Ambiance ([Q30](../Backlog/Q&A.md#q30)=A).
3. **Silences ≤ 4 s** ; apparitions **rapides** (pas d'émergences 1–6 s comme Cortex) ([Q34](../Backlog/Q&A.md#q34)).
4. **Mutabilité FX 1–3** selon fragment ; superposition **2 plans** de présence (pas `INTERMEDIAIRE`) ([Q36](../Backlog/Q&A.md#q36), [Q10](../Backlog/Q&A.md#q10)).
5. **Garde-fous R12/R13** — le générateur limite les chaînes de fragments à forte charge sémantique (anti fausse citation).
6. **`REINJECTER` / Boucle** — historique IDs + `recipe.json` ; **pas** de `writesf~` ([Q35](../Backlog/Q&A.md#q35)=A).

---

## 3. Couches et spatial

`FSM_N_8HP[2] = (2, 1, 0, …)` — 2 couches.

| Couche | Rôle | Matière (proto) | Spatial |
|--------|------|-----------------|---------|
| L1 | fil / noyau | `RECONSTRUCTION/LONG_MOYEN` → repli `FRAGMENTS` longs | modes Simon §14 via `recon_recipes.py` |
| L2 | interruptions | `RECONSTRUCTION/FRAGMENTS` | idem |
| L9 | — | éteinte | — |

**Bibliothèque spatiale V1** : `CONVERGENCE`, `CONSTELLATION`, `HALO`, `DISPERSION` — tirées dans la recette, appliquées par `recon_formes_08`.

---

## 4. Matière et classeur

| Pool | État |
|------|------|
| `RECONSTRUCTION/FRAGMENTS` | 287 fichiers — **proto** moteur |
| `RECONSTRUCTION/LONG_MOYEN` | 1 fichier — fil unique en attendant Simon |
| Nouvelle banque Simon | ~jours — cible finale ([Q32](../Backlog/Q&A.md#q32)) |

Feuille **Reconstruction** du classeur : colonnes Simon **§26.1** (distinctes Cortex/Hippo). Colonnes vides OK ; compatibilité hybride quand remplies ([Q33](../Backlog/Q&A.md#q33)).

Regénération :
```bash
python3 scripts/gen_formes_recon.py
python3 scripts/gen_prototype_08_8hp.py
python3 scripts/gen_catalogue_xlsx.py
```

---

## 5. Contraste avec les autres zones

| | Cortex | Hippocampe | Reconstruction |
|---|--------|------------|----------------|
| Logique | masse + plans | association | **composition** |
| Densité | 12 voix | 4 voies | 2 + forme |
| Lisibilité | floue | suivable | **variable** (courbe) |
| Précalcul | playlists | `gen_assoc_hippo.py` | **`gen_formes_recon.py`** |

---

## 6. Ce qu'il reste à figer à l'oreille

1. Nouvelle banque + remplissage feuille §26.1 — **Simon**.
2. Calibrage des 4 modes spatiaux et mutabilité FX 1–3.
3. Lien Reconstruction → Boucle (variation R56 à la relecture).
4. Durée 120 s une fois la matière longue disponible.
