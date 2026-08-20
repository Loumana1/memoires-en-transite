# Zones — comment ça sonne

Un fichier par zone. Chacun décrit **comment la zone sonne**, pas quels samples y passent.

| Zone | Fichier | Statut |
|------|---------|--------|
| Cortex | [`Cortex.md`](./Cortex.md) | en cours de gel — priorité 1 |
| Hippocampe | [`Hippocampe.md`](./Hippocampe.md) | en cours de gel — priorité 2 |
| Reconstruction | [`Reconstruction.md`](./Reconstruction.md) | pas encore travaillée |
| Boucle | [`Boucle.md`](./Boucle.md) | pas encore travaillée |

---

## La règle de séparation

C'est le point central de cette réorganisation. Deux choses sont mélangées dans les documents reçus jusqu'ici, et il faut les séparer :

**Le timbre d'une zone** — filtre, saturation, réverbération, gain, mouvement dans les 8 HP, rythme de déclenchement. Ça ne dépend pas du contenu du sample. Un fragment de parole quelconque envoyé dans le Cortex doit sonner « Cortex ». C'est ce que décrivent ces fichiers, et c'est ce qu'on veut **figer maintenant**.

**Le choix du sample** — quel fragment, associé à quel autre, avec quel niveau de présence, selon quels attributs. Ça dépend entièrement du tableau de classification, qui n'existe pas encore. C'est décrit dans [`../Matiere/Attributs.md`](../Matiere/Attributs.md) et ça viendra **après**.

Conséquence pratique : on doit pouvoir remplacer tout le contenu de `SONS_V3/` par d'autres wav et la zone doit sonner pareil. Si ce n'est pas le cas, un paramètre de zone dépend en cachette du contenu, et c'est un bug.

---

## Les trois statuts d'un paramètre

Chaque paramètre dans ces fichiers porte un statut :

| Statut | Sens | Qui peut le changer |
|--------|------|---------------------|
| **FIGÉ** | Validé à l'oreille. C'est le son de la zone. | Loumana, par un prompt explicite, avec une strophe dans [`../log.md`](../log.md) |
| **OREILLE** | Valeur actuelle plausible, pas encore validée. | Se règle librement pendant les séances d'écoute |
| **OUVERT** | Pas de valeur décidée, ou contredit la spec Simon. | Renvoie vers une question dans [`../Backlog/Q&A.md`](../Backlog/Q&A.md) |

Rien n'est encore **FIGÉ** au 20 août 2026. C'est justement le travail à faire : passer les paramètres de OREILLE à FIGÉ, zone par zone, en commençant par le Cortex.

---

## Où vivent réellement les valeurs

Les chiffres cités ici sont **recopiés** de `scripts/proto07/proto07_lib/presets07.py` et des abstractions `pd/lib/*_07.pd`. Le code fait foi. Si une valeur bouge dans le code, ces fichiers doivent être corrigés dans le même prompt — sinon le gel ne vaut rien.

Les `.pd` de Proto 07 sont **générés** : on modifie `presets07.py` puis `python3 scripts/gen_prototype_07_8hp.py`. Jamais le `.pd` à la main.
