# Docs — Mémoires en transit / Micro-opacités

Installation 8 HP · Loumana · son : Simon Mahungu · Pd : Alassane Traoré
Expos : 11 sept. 2026 CWB Paris · nov. 2026 Bozar / MBA Bruxelles

Loumana travaille **à l'oreille** : un prompt, une modification. Ce n'est pas un sprint.

---

## Carte

| | |
|--|--|
| [`etatactuel.md`](./etatactuel.md) | Ce qui sonne **maintenant**. Point d'entrée |
| [`log.md`](./log.md) | **Pourquoi** ça a changé. Journal, tête du fichier = le plus récent |
| [`Zones/`](./Zones/) | **Comment chaque zone sonne** — timbre, effets, mouvement. Indépendant des samples |
| [`Matiere/`](./Matiere/) | Pipeline des samples, vocabulaire d'attributs, classeur de classification |
| [`Backlog/`](./Backlog/) | [`Q&A.md`](./Backlog/Q&A.md) = à trancher · [`TO DO.md`](./Backlog/TO%20DO.md) = clair |
| [`Sources/`](./Sources/) | Documents reçus, tels quels. **Pas** des specs applicables |
| [`archive/`](./archive/) | Historique. L'IA ne le lit que sur demande |
| [`../scripts/README.md`](../scripts/README.md) | `proto07/` courant · `proto06/` figé · `archive/` |

Pas de numéro dans les noms de fichiers. Les numéros qui restent sont dans `archive/`, où ils datent de l'historique.

---

## Protocole IA

**Lire dans cet ordre :** ce fichier → [`etatactuel.md`](./etatactuel.md) → la zone concernée dans [`Zones/`](./Zones/) → [`log.md`](./log.md).

### Après chaque prompt qui change le patch ou les sons

1. Faire la modification. Si elle touche `proto07_lib`, régénérer.
2. **Ajouter une strophe en tête de [`log.md`](./log.md)** : date, prompt, pourquoi, changement. Ne jamais réécrire les strophes plus anciennes.
3. **Corriger [`etatactuel.md`](./etatactuel.md)** si le son, un pool ou le câblage a changé.
4. **Corriger le fichier de zone concerné** dans [`Zones/`](./Zones/) si une valeur citée a bougé. Sinon le gel ne vaut rien.

### Ce qu'il ne faut pas faire

- Piocher dans [`Backlog/TO DO.md`](./Backlog/TO%20DO.md) de sa propre initiative. Seulement si Loumana le demande.
- **Coder ce qui dépend d'une question encore ouverte** dans [`Backlog/Q&A.md`](./Backlog/Q&A.md). Demander, ne pas deviner.
- Traiter un document de [`Sources/`](./Sources/) comme une spec applicable. Un document reçu se **trie** d'abord : ce qui est clair va dans `TO DO.md`, ce qui est ambigu ou contradictoire va dans `Q&A.md`.
- Recoder « comme le 16 août » contre le prompt en cours.

---

## Colonne vs oreille

| Ça tient | Ça bouge au prompt |
|----------|--------------------|
| 8 HP · Proto 07 · Proto 06 figé | Les FX, les densités |
| `SONS_V3/` seul dossier audio · masters dans `WIP/` | Quels dossiers sont lus |
| FSM Cortex → Hippo → Recon | LPF, saturation, delay |
| Micro et piézo jamais vers `dac~` | La carte des HP en Cortex (voir [Q1](./Backlog/Q&A.md#q1)) |

---

## Commandes

| | |
|--|--|
| Lancer sur Mac | `bash scripts/launch_prototype_07_8hp.sh` |
| Lancer / boot sur Pi | [`../deploy/debian/README.md`](../deploy/debian/README.md) |
| Régénérer le patch | `python3 scripts/gen_prototype_07_8hp.py` |
| Découper la matière | `python3 scripts/slice_opacite_v3.py` → `SONS_V3/` |
| Régénérer le classeur | `python3 scripts/gen_catalogue_xlsx.py` |

Pas d'édition à la main des `.pd` du Proto 07 : ils sont générés. Console Pd attendue : zéro erreur, zéro avertissement.

**Interdits :** toucher à `SONS_V3/WIP/` (les masters de Simon, seule matière irremplaçable) · toucher aux patches 06 ou à `presets06.py` · router `adc~` vers les HP · mettre des `,` ou `;` bruts dans un `#X text`.

**Le projet n'est pas sous git.** Donc : on déplace, on ne supprime pas — sauf demande explicite de Loumana. Voir [`Backlog/TO DO.md`](./Backlog/TO%20DO.md) §0.
