# Zone Boucle — comportement sonore

**Pas une zone comme les autres.** Décision d'oreille du 18 août : la Boucle n'est **pas un paysage** que le cycle AUTO traverse, et **pas un buffer**. C'est une réinjection courte, rare, qui vient percer les autres zones.

Simon n'a pas livré de spec pour cette zone. → [Q19](../Backlog/Q&A.md#q19).

---

## 1. Intention

Une piqûre. Un fragment déjà entendu qui revient trop mouillé, trop loin, comme un résidu. Ça ne dure pas, ça ne s'installe pas, et ça ne doit pas être fréquent au point de devenir un motif.

C'est la seule zone où la réverbération et le delay sont **assumés comme un effet**, pas comme une distance.

---

## 2. Invariants

1. Rare. Si on l'entend à chaque cycle, c'est raté.
2. Court. Quelques secondes, pas une minute.
3. Nettement plus mouillé que tout le reste.
4. Elle **se superpose** aux autres zones : elle ne les interrompt pas, elle passe par une couche à part (couche 10, hors du compte `n` de la FSM).

---

## 3. Déclenchement

`pd/lib/boucle_inject_07.pd`

| Élément | Valeur | Statut |
|---------|--------|--------|
| Probabilité | **15 %** à chaque transition du cycle libre | OREILLE |
| Retard après décision | tiré entre **8 et 90 s** | OREILLE |
| Durée de l'état | `6000 ms` (`BOUCLE_DUR_MS`) | OREILLE |
| Lecture | one-shot, `player_state_07 0` | OREILLE |
| Pool | slot 9 — tout `HIPPOCAMPE` + `RECONSTRUCTION/FRAGMENTS` | provisoire |
| Gain | `0.16` (`inj_gain`) — plus bas que les autres couches | OREILLE |

Le retard aléatoire de 8 à 90 s est ce qui empêche la Boucle de tomber toujours au même endroit du cycle. À conserver.

---

## 4. Traitement

Deux jeux de valeurs coexistent, et **c'est un bug** : le preset de l'état 3 dans `presets07.py` et le message d'initialisation câblé dans le patch pour la couche 10 ne disent pas la même chose.

| Paramètre | `presets07.py` état 3, L1 | Message couche 10 dans le patch |
|-----------|---------------------------|----------------------------------|
| mode | 2 (saut) | 2 (saut) |
| step | 1800 ms | 1800 ms |
| xfade | 40 ms | 40 ms |
| wet | **0.25** | **0.18** |
| delay | **400 ms** | **260 ms** |
| feedback | **0.3** | **0.22** |
| saturation | **0.2** | **0.12** |
| LPF | **6000 Hz** | **5500 Hz** |
| HPF | (défaut 20) | 40 Hz |

En pratique c'est le message de la couche 10 qui s'applique à l'injection, puisque c'est cette couche qui joue. Le preset de l'état 3 ne sert que si on force `FORCE 3` à la main. Il faut aligner les deux ou documenter clairement lequel gouverne quoi. → [TO DO](../Backlog/TO%20DO.md).

---

## 5. Envie mise de côté

Le backlog du 18 août portait l'idée d'une Boucle **buffer** : enregistrer réellement ce qui a sonné et le réinjecter plus tard, plutôt que retirer un fichier au hasard dans un pool. C'est aussi ce que décrit le cahier des charges d'origine sous le nom de « mémoire fantôme » (`writesf~` vers `MEMOIRE_VIVANTE`).

Décision du 18 août : **non pour l'instant**. Conservé comme envie dans [`../Backlog/TO%20DO.md`](../Backlog/TO%20DO.md), section « plus tard ».

---

## 6. Ce qu'il faut faire pour figer cette zone

1. Aligner les deux jeux de valeurs (bug ci-dessus).
2. Écouter plusieurs cycles complets et juger si 15 % est trop ou pas assez.
3. Figer. C'est la zone la plus rapide à clore : peu de paramètres, pas de spec contradictoire.
