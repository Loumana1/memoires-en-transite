# Zone Reconstruction — comportement sonore

**Pas encore travaillée à l'oreille.** Aucun paramètre figé, et c'est normal : cette zone n'a pas encore fait l'objet d'une séance dédiée.

Simon n'a pas livré de spec pour cette zone. → [Q19](../Backlog/Q&A.md#q19).

---

## 1. Intention

La zone **lisible**. Après la masse floue du Cortex et la circulation de l'Hippocampe, la Reconstruction laisse entendre. Presque pas d'effets, un fil principal qu'on suit, et des interruptions courtes qui viennent le contredire.

C'est aussi la zone la plus longue du cycle : **120 s**, contre 40 et 50. Elle a le temps de s'installer.

---

## 2. Invariants — vrais quel que soit le sample

1. Quasi sec. LPF à 18–20 kHz, saturation nulle. C'est la seule zone où la matière est presque telle quelle.
2. Deux couches seulement : un **fil** continu et des **interruptions**.
3. Le fil tourne lentement (rotation ambisonique) ; les interruptions apparaissent ailleurs.
4. Pas de nappe : L9 est éteinte. **Confirmé** le 20 août par [Q2](../Backlog/Q&A.md#q2) — « la reconstruction, je dirais qu'il n'en faut pas ». C'est le seul point du projet où l'implémentation était déjà exactement conforme à la décision : `RECONSTRUCTION/AMBIANCE` est vide et n'a pas à être rempli.

---

## 3. Couches et traitement

`FSM_N_8HP[2] = (2, …)` — 2 couches.

| Couche | Rôle | Matière | Mode spatial |
|--------|------|---------|--------------|
| L1 | le fil | `RECONSTRUCTION/LONG_MOYEN`, repli sur `FRAGMENTS` | 1 — rotation, `rot` 0,012 |
| L2 | interruptions | `RECONSTRUCTION/FRAGMENTS` | 0 ou 3 selon la variante |
| L9 | — | éteinte | — |

Valeurs, variante 1 (`presets07.py`, `_RC0` et `_RC1`) :

| Paramètre | L1 (fil) | L2 (interruptions) | Statut |
|-----------|----------|--------------------|--------|
| saturation | `0` | `0` | OREILLE |
| HPF | `20 Hz` | `25 Hz` | OREILLE |
| LPF | `20000 Hz` | `18000 Hz` | OREILLE |
| wet delay | `0.08` | `0.05` | OREILLE |
| temps de delay | `100 ms` | `80 ms` | OREILLE |
| feedback | `0.1` | `0` | OREILLE |
| `lfo` d'amplitude | `0.04` | `0` | OREILLE |
| vitesse de rotation | `0.012` | — | OREILLE |

Les variantes 2 et 3 changent la rotation (0,010 puis 0,008) et passent L2 en mode 3 (séquence, `step` 2200 ms, `xfade` 80 ms).

| Élément | Valeur | Source | Statut |
|---------|--------|--------|--------|
| Durée de l'état | `120 s` | `CYCLE1_8HP` | OREILLE |
| Interruptions | `s6_recon_bang` toutes les **4,5 s** sur L2 | `recon_pulse_07` | OREILLE |
| Cascade (`ovl`) | `5 ms` | `presets07.py` | OREILLE |

---

## 4. Problème de matière

| Pool | Nombre de fichiers |
|------|--------------------|
| `RECONSTRUCTION/FRAGMENTS` | 287 |
| `RECONSTRUCTION/LONG_MOYEN` | **1** |
| `RECONSTRUCTION/AMBIANCE` | 0 — **normal**, la zone n'en veut pas ([Q2](../Backlog/Q&A.md#q2)) |

Le fil principal tire dans **un seul fichier**. Sur 120 s d'état, c'est le même son qui revient. Ce n'est pas un réglage à faire, c'est de la matière qui manque : il faut des fragments longs de Reconstruction dans le master Ableton. → [TO DO](../Backlog/TO%20DO.md).

Tant que ce déséquilibre existe, il est difficile de juger la zone à l'oreille — donc inutile d'en régler les effets finement.

---

## 5. Ce qu'il faut faire pour figer cette zone

1. **Obtenir de la matière longue** pour le fil. Bloquant.
2. Décider si 120 s est la bonne durée, une fois la matière disponible.
3. Régler le rythme des interruptions (4,5 s aujourd'hui) et leur mode spatial.
4. Vérifier que le contraste avec l'Hippocampe s'entend : l'Hippocampe bouge vite et sec, la Reconstruction tourne lentement et ouvert.
5. Figer, écrire une strophe dans [`../log.md`](../log.md).
