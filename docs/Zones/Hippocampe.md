# Zone Hippocampe — comportement sonore

**Priorité 2 pour le gel.** Aucun paramètre n'est encore FIGÉ.
Statuts : voir [`README.md`](./README.md). Questions ouvertes : [`../Backlog/Q&A.md`](../Backlog/Q&A.md).

**Simon n'a pas encore livré de spec pour cette zone.** Le document reçu ne couvre que le Cortex et Cortex-Ambiance. Tout ce qui suit vient donc de l'implémentation et des séances d'écoute. C'est un avantage : il n'y a pas de contradiction à résoudre, on peut figer plus vite. → [Q19](../Backlog/Q&A.md#q19).

---

## 1. Intention

Le contraire du Cortex. Là où le Cortex est une masse floue et immobile, l'Hippocampe est **net et mobile**. Peu de couches, peu d'effets, et un mouvement qu'on peut suivre de l'oreille : des « voyageurs » qui se déplacent de baffle en baffle.

C'est la zone du souvenir qui circule, qui se cherche un endroit. On doit pouvoir suivre un fragment individuel des yeux, pour ainsi dire.

---

## 2. Invariants — vrais quel que soit le sample

1. Les effets sont **secs**. Presque pas de wet, pas de saturation notable. Le contraste avec le Cortex vient d'abord de là.
2. Le LPF est **haut** (9 kHz) : la matière garde ses aigus, ses transitoires, sa netteté.
3. Le mouvement est un **saut**, pas un panoramique. Les fondus de 35 ms font entendre un déplacement discret d'un baffle à l'autre.
4. Chaque voyageur a sa propre vitesse, et cette vitesse **change** en cours de route.
5. Il y a moins de couches simultanées qu'en Cortex. La zone doit rester lisible.
6. Contrairement au Cortex, l'Hippocampe **passe par le décodage ambisonique** : c'est là que les 8 HP servent comme un espace, pas comme 8 sources.

---

## 3. Couches

`FSM_N_8HP[1] = (4, …)` — 4 voyageurs, plus la nappe L9.

| Couche | Rôle | Matière lue aujourd'hui |
|--------|------|-------------------------|
| L1 | voyageur | `HIPPOCAMPE/FRAGMENTS` (court) |
| L2 | voyageur | `HIPPOCAMPE/LONG_MOYEN` |
| L3 | voyageur, déclenché en différé | `HIPPOCAMPE/LONG_MOYEN` |
| L4 | voyageur, déclenché en différé | `HIPPOCAMPE/LONG_MOYEN` |
| L9 | nappe qui voyage | `HIPPOCAMPE/AMBIANCE` si non vide, **sinon repli sur `CORTEX/AMBIANCE`** |

`HIPPOCAMPE/AMBIANCE` est **vide** : il n'y a pas de 5ᵉ master d'ambiance de la part de Simon. La nappe de l'Hippocampe est donc aujourd'hui une nappe de Cortex qu'on fait bouger et qu'on filtre différemment.

**[Q2](../Backlog/Q&A.md#q2), répondu le 20 août, ferme cette porte.** L'ambiance de l'Hippocampe doit être « une ambiance **totalement différente** de celle qui était dans le Cortex ». L'emprunt n'est donc plus une option acceptable à terme : ce n'est plus un arrangement, c'est un provisoire assumé, et il devient une **dépendance matière envers Simon**. Filtrer autrement une nappe de Cortex ne suffit pas — c'est la même matière, donc la même mémoire, alors que la zone est censée changer de lieu.

Décidé aussi en [Q2](../Backlog/Q&A.md#q2) : le mouvement de cette nappe est **lent, de baffle en baffle** — ce qui est déjà ce que fait le mode 4 (§6). Ce point est donc conforme.

---

## 4. Chaîne de traitement — voyageurs

```text
player_state_07 → *~ 0.22 → gate ~3 ms → fx_router_06 → spatial_router_06 → decode_8hp_06 → HP 1..8
```

Valeurs par défaut (`presets07.py`, fonction `_HP`) :

| Paramètre | Valeur | Statut |
|-----------|--------|--------|
| gain d'entrée | `0.22` | OREILLE |
| saturation | `0.08` | OREILLE |
| HPF | `40 Hz` | OREILLE |
| LPF | `9000 Hz` | OREILLE |
| wet delay | `0.06` | OREILLE |
| temps de delay | `80 ms` | OREILLE |
| feedback | `0.06` | OREILLE |
| `lfo` d'amplitude | `0.03` | OREILLE |
| `flfo` | `0` | FIGÉ de fait |

Pas de balayage de filtre ici : il n'y a pas d'équivalent de `cortex_ctrl_07` pour l'Hippocampe. Le timbre est stable, c'est la position qui bouge. **C'est la décision structurante de la zone** et elle mérite d'être figée telle quelle.

---

## 5. Mouvement — le cœur de la zone

Deux mécanismes se superposent.

### Les modes spatiaux

`spatial_router_06` :

| Mode | Comportement |
|------|--------------|
| 0 | sec, sur le baffle d'ancrage |
| 1 | rotation ambisonique continue |
| **2** | **saut d'un baffle à un autre, au hasard** |
| 3 | séquence ordonnée de baffles |
| **4** | **local, sur 3 ou 4 baffles voisins** |

L'Hippocampe n'utilise que **2** et **4**. Le mode 4 donne un souvenir qui hésite dans une région de la salle ; le mode 2 donne un souvenir qui se téléporte. Alterner les deux entre voyageurs est ce qui rend la zone vivante.

### La réécriture continue

`pd/lib/hippo_motion_07.pd` ne fixe pas les modes une fois pour toutes : il les **réécrit en boucle** pendant tout l'état.

| Élément | Valeur | Statut |
|---------|--------|--------|
| Horloge de réécriture | `metro 3500 ms` au départ, puis **2000 à 4500 ms** au hasard | OREILLE |
| Départ après entrée dans la zone | `delay 80 ms` | OREILLE |
| Réglage initial L1 → L4 | mode 4 / 2 / 4 / 2 · step 1100 / 1600 / 2200 / 1400 ms · sens 0 / 1 / 1 / 0 | OREILLE |
| Réglage initial L9 | mode 4 · step 1500 ms | OREILLE |
| `step` après réécriture | tiré entre **800 et 2200 ms** | OREILLE |
| mode après réécriture | tiré dans {4, 4, 2, 2, 4} — donc **60 % de local**, 40 % de saut | OREILLE |
| Fondu entre baffles (`xfade`) | `35 ms` sur toutes les couches | OREILLE — candidat au gel immédiat |

À chaque tick, un seul voyageur (tiré au hasard parmi les 4) reçoit un nouveau `step` et un nouveau `mode`. Les autres continuent. C'est ce qui évite que les quatre voyageurs changent d'allure en même temps.

Le `sens` (0 ou 1) donne le sens de parcours et n'est réglé qu'à l'initialisation, pas dans la réécriture. Incohérence mineure, à décider : le sens doit-il aussi être retiré au hasard ?

---

## 6. La nappe qui voyage

La nappe L9 se distingue de la nappe du Cortex sur deux points, tous les deux importants :

| | Cortex | Hippocampe |
|--|--------|------------|
| LPF | `18000 Hz` (ouverte) | **`5000 Hz`** (assombrie) |
| Mouvement | fixe sur son baffle | mode 4, `step` 1500 ms — elle circule |
| Gain | `0.25` | `0.35` (`amb_gain`) |

Le changement de LPF est fait par `cortex_ctrl_07` sur transition d'état (`sel 0 1` → `s6_l9_lpf 18000` ou `5000`, après 60 ms). C'est le même wav qui sonne autrement selon la zone — exactement le principe qu'on veut : **la zone impose son timbre, pas le fichier**.

À noter dans `presets07.py` le commentaire « Hippo: LPF 1000 Hz via ctrl » alors que `cortex_ctrl_07` envoie 5000. Le code fait foi : c'est **5000**. Commentaire à corriger. → [TO DO](../Backlog/TO%20DO.md).

---

## 7. Déclenchement et densité

| Élément | Valeur | Source | Statut |
|---------|--------|--------|--------|
| Durée de l'état dans le cycle AUTO | `50 s` | `CYCLE1_8HP` | OREILLE |
| Voyageurs actifs | `4` | `FSM_N_8HP[1]` | OREILLE |
| Cascade de démarrage (`ovl`) | `5 ms` | `presets07.py` | OREILLE |
| Déclenchement différé L3 | `2200 ms` après l'entrée | `hippo_assoc_07` | OREILLE |
| Déclenchement différé L4 | `4100 ms` après l'entrée | `hippo_assoc_07` | OREILLE |
| Répartition des durées | 3 longs (≥ 8 s) + 1 court | `FSM_N_8HP[1]` | provisoire — remplacé par les tags |

Les déclenchements différés de L3 et L4 sont la version minimale de l'envie « un fragment A déclenche un fragment B ». Aujourd'hui c'est un simple retard fixe, sans aucun rapport entre le contenu de A et celui de B. `hippo_assoc_07` écrit dans `s6_tag_hook`, qui n'est reçu par personne : c'est **le point d'accroche prévu pour la logique de tags**. Voir [`../Matiere/Attributs.md`](../Matiere/Attributs.md).

---

## 8. Ce qu'il faut faire pour figer cette zone

Plus court que pour le Cortex, parce qu'il n'y a pas de contradiction de spec à résoudre.

1. **Écouter et figer le mouvement** : les bornes de `step` (800–2200 ms), le `xfade` de 35 ms, la répartition 60 / 40 entre local et saut, et l'horloge de réécriture. C'est ça, le son de la zone.
2. **Décider si le `sens` est retiré au hasard** comme le mode et le step.
3. **Figer le contraste avec le Cortex** : LPF 9 kHz contre 500–2000 Hz, wet 0,06 contre 0,10 plus réverbération. Il faut vérifier à l'oreille que le passage de Cortex à Hippocampe s'entend comme une ouverture.
4. **Figer la nappe** : LPF 5 kHz, gain 0,35, mode 4 / step 1500 ms.
5. ~~**Décider du sort de `HIPPOCAMPE/AMBIANCE`**~~ — tranché le 20 août par [Q2](../Backlog/Q&A.md#q2) : il faut **un master d'ambiance propre à l'Hippocampe**, totalement différent de celui du Cortex. À demander à Simon. Le repli actuel sur les nappes du Cortex reste en place en attendant, mais comme provisoire, pas comme solution.
6. Écrire `FIGÉ` ici et une strophe dans [`../log.md`](../log.md).

Rien dans cette liste ne dépend du tableau de classification. L'Hippocampe peut être figé **avant** que la classification n'arrive, et c'est ce qu'il faut faire.
