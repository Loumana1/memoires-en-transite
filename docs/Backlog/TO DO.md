# TO DO — ce qui est clair

**20 août 2026.** Ce qui suit ne demande **aucune décision artistique** : soit c'est un bug, soit c'est une demande sur laquelle le document de Simon et l'implémentation sont d'accord.

Ce qui demande une décision est dans `[Q&A.md](./Q&A.md)`. **Une tâche marquée « bloquée par Qn » ne se code pas avant que Qn soit répondue.**

Ce fichier n'est pas un sprint. L'IA n'y pioche que si Loumana le demande.

---

## 0. À faire avant tout le reste

- [ ] **Mettre le projet sous git.** Il n'y a aucun contrôle de version aujourd'hui. On est en train de réorganiser la doc, de préparer une refonte du Cortex et un travail de classification de plusieurs heures — sans filet. C'est exactement le « limiter les dégâts à chaque nouvelle implémentation » demandé. Un `git init` + un premier commit coûte deux minutes et rend toute la suite réversible. Ajouter `SONS*/` au `.gitignore` (trop lourd) mais versionner `pd/`, `scripts/`, `docs/`, `deploy/`.
- [ ] **Vérifier que la sauvegarde des masters existe vraiment.** `SONS_V3/WIP/Opacité V6/` (2,6 Go, 4 fichiers) est désormais la **seule matière irremplaçable** du projet : tout le reste de `SONS_V3/` se reconstruit à partir de là. Annoncé comme sauvegardé ailleurs le 20 août — le confirmer physiquement.

**Fait le 20 août.** Suppression de `SONS/`, `SONS_V2/`, `SONS_FINAL/` et `SONS_PROTOTYPE/` — 3 Go libérés, `SONS_V3/` est le seul dossier audio. Conséquences assumées : les patches **Proto 06 sont muets** (ils lisaient `SONS/`), et `scripts/proto06/slice_sons_final.py` et `build_cortex_beds.py` ne peuvent plus tourner (ils lisaient `SONS_FINAL/`).

**Fait le 20 août.** [Q21](./Q&A.md#q21) répondu — option A. La découpe est **incrémentale** et les ID sont **stables** : voir [`../Matiere/Pipeline.md`](../Matiere/Pipeline.md). La classification à l'oreille peut commencer.

---

## 0 bis. Le chantier ouvert par les réponses du 20 août

Huit questions répondues : [Q1](./Q&A.md#q1) = A, [Q2](./Q&A.md#q2), [Q3](./Q&A.md#q3) = B, [Q4](./Q&A.md#q4), [Q19](./Q&A.md#q19), [Q20](./Q&A.md#q20), [Q21](./Q&A.md#q21) = A, [Q24](./Q&A.md#q24) = A.

**Le Proto 08 est décidé** ([Q24](./Q&A.md#q24) = A). Il existe parce que [Q1](./Q&A.md#q1) = A change la structure du Cortex : **6 baffles de parole × 2 fragments = 12 voix simultanées**, plus **2 baffles d'ambiance fixes**. Le 07 devient figé comme le 06, et reste écoutable pour comparer.

- [ ] **Créer le Proto 08** : `scripts/proto08/`, `proto08_lib/`, `presets08.py`, générateur, launcher. Copie du 07 puis modification, avec `pdbuild` désormais dans [`scripts/shared/`](../../scripts/shared/).
- [ ] **12 couches de parole sur 6 baffles.** `FSM_N_8HP[0]`, les ancrages, le nombre de lecteurs, et `cortex_pair_07` → 6 paires en décalage modulo 6.
- [ ] **Étendre le balayage de LPF à 12 oscillateurs** dans `cortex_ctrl`. Ne pas prolonger mécaniquement la suite 0,070 → 0,170 : vérifier à l'oreille qu'aucune paire d'oscillateurs n'est dans un rapport simple, sinon deux couches respirent ensemble et la masse pulse.
- [ ] **2 nappes au lieu de 5**, sur deux baffles fixes et **non adjacents**, l'un *musical* l'autre *texture*. C'est la partie de la décision qui vide le plus l'espace autour des paroles : à écouter avant de figer quoi que ce soit d'autre.
- [ ] **Les plans de présence deviennent bloquants, pas optionnels.** Douze voix filtrées au même niveau ne produisent pas une superposition mais du bruit. → §1, et [Q10](./Q&A.md#q10) qui passe en tête du Q&A.

Ce qui **n'est pas** dans le Proto 08 au départ : la règle C1 Belgique / Congo. [Q4](./Q&A.md#q4) confirme que l'information n'existe pas encore et viendra du tableau ; le 08 se construit donc avec un tirage au hasard, le sélecteur se branchant ensuite. C'est la séparation voulue depuis le début — le son de la zone d'abord, le choix des samples ensuite.

---



## 1. Geler le son des zones

Objectif : les zones sonnent de façon décidée et stable **avant** que la logique de samples n'arrive. Détail par zone dans `[../Zones/](../Zones/)`.

### Cortex

- [ ] **Ajouter une vraie réverbération « pièce voisine »** sur les couches de parole. Aujourd'hui il n'y a qu'un delay de 180 ms à 6 % de feedback, ce qui ne fabrique pas de pièce. C'est demandé explicitement par Simon (§1.3 et §2.6) et c'est le levier le plus efficace contre l'intelligibilité résiduelle. Réglage à l'oreille, cible à préciser en [Q18](./Q&A.md#q18).
- [ ] **Implémenter les plans de présence dans le Proto 08** — spec [`../Zones/Cortex.md`](../Zones/Cortex.md) §5 bis. **V1 : deux plans** (`PREMIER_PLAN` + `ARRIERE_PLAN`) — 3ᵉ reporté ([Q25](./Q&A.md#q25)).
- [ ] **Deux nappes globales, pas cinq** — [Q25](./Q&A.md#q25) : une musicale + une texture **communes** ; AM lente OK ([Q15](./Q&A.md#q15)) ; texture **fixe**, pas de `SE_DEPLACER` ([Q16](./Q&A.md#q16)) ; **mutex** recouvrement musicale/texture ([Q17](./Q&A.md#q17)).
- [ ] **Implémenter les gestes temporels dans le Proto 08** — spec [`../Zones/Cortex.md`](../Zones/Cortex.md) §8 bis, [Q11](./Q&A.md#q11) tranché. `EMERGER` 6–10 s, `RECOUVRIR` 3–6 s, plafond = niveau du plan assigné, 50/50, décalage aléatoire par paire (pas toutes en même temps), `cortex_pulse_07` **supprimé**. Autres mouvements : extension future.
- [ ] **Deux gains distincts sous chaque paire** + deux chaînes FX (preset de plan par fragment). [Q9](./Q&A.md#q9) tranché : le moteur attribue le plan, pas le classeur.
- [ ] Figer les bornes et la vitesse du balayage de LPF (500–2000 Hz, six LFO de 0,070 à 0,170 Hz dans `cortex_ctrl_07`).
- [ ] Figer la rotation par paires : `metro 2600 ms`, 62 % de probabilité, `xfade` 12 ms.
- [ ] Figer les nappes : gain 0,25, AM de 0,030 à 0,074 Hz.
- [ ] **Séparer les pools d'ambiance musicale et texture.** `CORTEX/AMBIANCE` est un pool unique de 27 fichiers ; Simon distingue deux familles avec des attributs et des comportements différents. Devenu indispensable avec [Q1](./Q&A.md#q1) = A : les deux baffles d'ambiance sont précisément *musical* et *texture*. Se fait par la colonne `type_ambiance` du classeur ([Q20](./Q&A.md#q20)) plutôt que par deux dossiers, pour ne pas casser les ID.
- [ ] **Appliquer le seuil de 30 s aux nappes** ([Q3](./Q&A.md#q3) = B) : `AMBI_MIN_SEG` de 2 s à 30 s dans `slice_opacite_v3.py`. Mesuré faisable — 17 segments de 30 s et plus, dont un de 91 s. Deux effets à traiter en même temps : les 52 segments courts déjà découpés ne disparaîtront pas (découpe incrémentale), et `cortex_amb_pulse_07` qui relance toutes les 14 s n'a plus de sens sur une nappe de 60 s — il faut lire en entier ou enchaîner en fondu.



### Hippocampe

- [ ] Figer le mouvement : bornes de `step` (800–2200 ms), `xfade` 35 ms, répartition 60 / 40 entre mode local et mode saut, horloge de réécriture 2000–4500 ms.
- [ ] Décider si le `sens` est retiré au hasard comme le `mode` et le `step` — aujourd'hui il n'est réglé qu'à l'initialisation.
- [ ] Figer le contraste Cortex / Hippocampe et le vérifier à l'oreille sur une transition : LPF 9 kHz contre 500–2000 Hz, wet 0,06 contre 0,10 plus réverbération.
- [ ] Figer la nappe : LPF 5 kHz, gain 0,35, mode 4, `step` 1500 ms. Le mouvement lent de baffle en baffle est **confirmé** par [Q2](./Q&A.md#q2) — c'est déjà ce que fait le mode 4.
- [ ] **Demander à Simon un master d'ambiance propre à l'Hippocampe.** [Q2](./Q&A.md#q2) exige « une ambiance totalement différente de celle du Cortex ». Le repli actuel sur les nappes du Cortex n'est donc plus une solution acceptable, seulement un provisoire : filtrer autrement la même matière ne change pas de lieu.



### Reconstruction et Boucle

- [ ] Reconstruction : rien à régler utilement avant d'avoir de la matière longue (voir §4).
- [ ] Boucle : aligner les deux jeux de valeurs contradictoires (voir §3).

---



## 2. Préparer le terrain pour les tags

Détail et architecture : `[../Matiere/Attributs.md](../Matiere/Attributs.md)`.

- [ ] **Figer le vocabulaire d'attributs** — les noms exacts et les valeurs permises, une fois pour toutes. C'est fait dans `Attributs.md`, à relire et valider. [Q19](./Q&A.md#q19) précise qu'il s'applique à **tous** les fragments, pas seulement au Cortex : les trois feuilles ont donc les mêmes colonnes.
- [ ] **Ajouter la colonne** `DENSITE_PAROLE` (`FAIBLE` / `MOYENNE` / `FORTE`) au classeur. C8 tranchée ([Q13](./Q&A.md#q13)) : deux `FORTE` → extrémités des plans. Définition à l'oreille encore ouverte.
- [x] ~~**Rendre les ID stables**~~ — fait le 20 août. Registre `docs/Matiere/registre_ids.csv`, appariement par (master, état, rôle, début ± 0,3 s).
- [x] ~~**Découpe incrémentale**~~ — fait le 20 août. `slice_opacite_v3.py` ne vide plus rien, respecte le rangement manuel, signale les orphelins sans les supprimer. `gen_catalogue_xlsx.py` fusionnait déjà le classeur sur l'ID.
- [x] ~~**Aligner les colonnes du classeur sur le §5 d'`Attributs.md`.**~~ — fait le 20 août. `gen_catalogue_xlsx.py` : 16 colonnes (`id`, `type`, `duree_s`, `nature` auto + attributs oreille). Regen : `python3 scripts/gen_catalogue_xlsx.py`. La colonne « traitement souhaité » reste **écartée** ([Q20](./Q&A.md#q20)).
- [ ] Écrire le **sélecteur** — spec algorithme dans `Attributs.md` §6 ([Q5](./Q&A.md#q5), [Q6](./Q&A.md#q6), [Q7](./Q&A.md#q7), [Q8](./Q&A.md#q8)). **`gen_paires.py`** + **`gen_ambiance_cortex.py`** ([Q25](./Q&A.md#q25)). Bloqué par le **remplissage du tableau** ([Q4](./Q&A.md#q4) : C1 différée).
- [ ] **Mesurer si C1 est tenable avant de la coder.** [Q4](./Q&A.md#q4) : « je ne sais pas encore s'il y a assez de fragments ». Avec 6 paires il faut 6 Belgique + 6 Congo disponibles à chaque instant. La réponse retenue en cas de pénurie est « il répète ». À vérifier par l'audit `gen_paires.py` en mode rapport, sur un tableau partiellement rempli, avant d'écrire la moindre règle. **C2 :** symétrie + interdictions dures ([Q8](./Q&A.md#q8)) — spec [`../Matiere/Attributs.md`](../Matiere/Attributs.md) §2 bis.
- [ ] `s6_tag_hook` est écrit par `hippo_assoc_07` et reçu par personne. C'est le point d'accroche prévu. À laisser tel quel jusqu'à ce que le sélecteur existe.

---



## 3. Bugs et incohérences trouvés

Tous constatés le 20 août en relisant le code contre la doc. Aucun ne demande de décision.

- [ ] **Boucle, deux jeux de valeurs.** Le preset de l'état 3 dans `presets07.py` (wet 0,25 · delay 400 ms · fb 0,3 · sat 0,2 · LPF 6000) et le message d'initialisation de la couche 10 dans le patch (wet 0,18 · delay 260 ms · fb 0,22 · sat 0,12 · LPF 5500) ne disent pas la même chose. En pratique c'est la couche 10 qui joue. À aligner ou à documenter.
- [ ] **Commentaire faux dans** `presets07.py`**.** « Hippo: LPF 1000 Hz via ctrl » — `cortex_ctrl_07` envoie **5000**.
- [ ] **Docstring périmée dans** `presets07.py`**.** « 9 couches: 8 fragments (HP1–8) + 1 ambiance » — le Cortex utilise 6 fragments et 5 nappes dédiées. La référence « Q&A 16 août 2026 » pointe vers un document maintenant archivé.
- [x] ~~**README racine périmé** (« Matière : `SONS_V2/` »)~~ — corrigé le 20 août.
- [x] ~~`scripts/README.md` mentionne `slice_opacite_v2`~~ — corrigé le 20 août, le script V2 est passé dans `scripts/archive/`.
- [x] ~~**`slice_opacite_v3.py` cherchait les masters dans `SONS_V2/WIP`**~~, qui n'existait pas : le script était **cassé** depuis le déplacement des masters du 18 août, et personne ne l'avait vu. Corrigé vers `SONS_V3/WIP`. Au passage : combiné à l'ancien `rmtree(SONS_V3)`, le simple fait de corriger ce chemin sans toucher au reste aurait **supprimé les masters de Simon**. Le `rmtree` a disparu.
- [x] ~~Le déploiement Pi rsyncait `SONS_V3/WIP`~~ — 2,6 Go de masters inutiles envoyés sur le réseau à chaque copie. Exclu le 20 août.
- [x] ~~**Le Proto 07 importait `pdbuild` depuis `proto06/`**~~ via un `sys.path.insert`. Le générateur du prototype courant dépendait d'un sous-arbre figé et hors service : supprimer `proto06/` cassait le 07. Déplacé dans [`scripts/shared/`](../../scripts/shared/) le 20 août, avec une réexportation dans `proto06_lib/` pour ne pas dupliquer le code. Les deux prototypes ont été revérifiés.
- [x] ~~**Pas de `.gitignore`**~~ — créé le 20 août : `SONS_V3/`, `__pycache__/`, externals compilés.
- [ ] `sens` **non réécrit** dans `hippo_motion_07` alors que `mode` et `step` le sont. Incohérence à assumer ou à corriger.

---



## 4. Matière — dépend de Simon

- [ ] `RECONSTRUCTION/LONG_MOYEN` **ne contient qu'un seul fichier**, contre 287 dans `FRAGMENTS`. Le fil principal de la zone tire donc toujours le même son sur 120 s d'état. Il faut des fragments longs de Reconstruction dans le master.
- [ ] `HIPPOCAMPE/AMBIANCE` **et** `RECONSTRUCTION/AMBIANCE` **sont vides.** Il n'y a pas de 5ᵉ master d'ambiance. La nappe de l'Hippocampe est aujourd'hui une nappe de Cortex empruntée, filtrée différemment. Soit demander un master, soit assumer l'emprunt définitivement.
- [x] ~~**Vérifier la longueur des plages continues** dans les masters d'ambiance~~ — mesuré le 20 août, condition de [Q3](./Q&A.md#q3) remplie : **17 segments de 30 s et plus**, dont sept autour de 60 s et un de 91 s. Les « 7 minutes » de Simon n'existent pas en revanche, le plafond réel est 91 s. À noter : le tri manuel du 18 août appliquait déjà la règle sans le savoir — les 27 fichiers gardés dans `CORTEX/AMBIANCE` ont une médiane de 41,6 s, les 42 déplacés vers `FRAGMENTS` une médiane de 4,6 s.
- [ ] **Inscrire la règle des 30 s dans la découpe** ([Q3](./Q&A.md#q3) = B). Relever `AMBI_MIN_SEG` de 2 s à 30 s dans `slice_opacite_v3.py`. Attention : la découpe étant devenue incrémentale, les 52 segments courts déjà sur le disque ne disparaîtront pas — ils seront signalés comme orphelins. Il faut décider explicitement de ce qu'on en fait (les laisser en `FRAGMENTS`, ce qui est déjà le cas pour 42 d'entre eux, ou les sortir des pools).
- [ ] **Demander à Simon pourquoi les 250 premières secondes du master Cortex sont 27 dB sous le reste.** Mesuré le 20 août : médiane **−49,0 dBFS** sur l'intro contre **−22,3 dBFS** ensuite, et les douze fragments les plus faibles du projet viennent tous des 208 premières secondes. Le master Reconstruction n'a pas ce défaut (2 fichiers isolés sur 288). C'est la **cause principale** de l'écart de niveaux : en écartant l'intro, l'étendue du Cortex tombe de 47 à 19 dB. Savoir s'il s'agit d'un fondu d'entrée voulu, d'un passage mixé bas, ou d'une erreur d'export — dans le dernier cas un ré-export règle le problème à la source et rend la moitié de la normalisation inutile.
- [ ] **Fragments Belgique / Congo** : savoir si Simon livre deux masters séparés ou si le contexte se renseigne à la main. Bloqué par [Q4](./Q&A.md#q4).

---



## 5. Salle et matériel

- [ ] **Les deux baffles d'ambiance ne doivent pas être côte à côte** (Simon §1.1 et §3.2), pour élargir la perception de l'espace. À reporter sur le plan de salle du CWB et du Bozar.
- [ ] **Piézos : le matériel n'existe pas.** Le cahier des charges prévoit 2 micros d'ambiance, jamais de piézos. Décider combien, où, et sur quoi. Bloqué par [Q14](./Q&A.md#q14).
- [ ] Calibrage en salle : FORCE puis AUTO sur 8 HP, en vérifiant que le Cortex est flou, l'Hippocampe suivable, la Reconstruction lisible.

---

## 6. Robustesse d'exposition

Le risque n'est pas le plantage, c'est **le silence que personne ne remarque**. Trois points issus de l'audit du 20 août, dont deux traités.

- [x] ~~**Détection de la Scarlett sans réessai.**~~ `launch.sh` faisait un seul `timeout 8` puis `exit 1`. Au démarrage du Pi, l'énumération USB peut dépasser 8 s : le service tombait et l'expo était muette. Corrigé le 20 août — quatre tentatives à délais croissants (0, 3, 6, 12 s), `timeout` porté à 15 s, et le device retenu tracé dans `deploy/debian/derniere_carte.log`. En cas d'échec le script distingue maintenant « carte pas branchée » de « Pd ne sait plus l'annoncer » en croisant avec `aplay -l`, et garde la sortie brute pour autopsie.
- [x] ~~**Aucun contrôle d'intégrité de la matière.**~~ Un wav corrompu, vide ou muet ne fait pas planter Pd : ça s'entend comme un trou et ça n'apparaît dans aucun log. Précédent réel : 8 segments morts trouvés au calibrage du 06. `scripts/verifier_sons.py` créé le 20 août — format, durée, fichiers muets, trous internes, et vérification que les 3481 références des playlists existent.
- [ ] **Détecter un Pd gelé.** C'est le seul vrai trou restant : un Pd qui ne plante pas mais ne produit plus rien n'est vu par personne. `WatchdogSec` de systemd ne peut **pas** servir ici, il suppose que le programme envoie des battements de cœur via `sd_notify` — Pd ne le fait pas. Il faut un contrôle externe : un timer systemd qui vérifie que Pd répond encore, ou que la carte consomme toujours des trames.
- [ ] **Ne jamais abandonner au démarrage.** Le service est en `Restart=on-failure` / `RestartSec=4`, donc il réessaie indéfiniment — ce qui est **le bon comportement pour une expo** et qu'il ne faut pas « corriger » en ajoutant un `StartLimitBurst`, sous peine que l'installation reste morte après quelques échecs. À durcir dans l'autre sens : `Restart=always` (couvrir aussi une sortie propre de Pd) et `StartLimitIntervalSec=0` pour le garantir explicitement.
- [x] ~~**Écart de niveau de 42 dB entre fragments.**~~ Mesuré correctement le 20 août : le chiffre de 42 dB était un écart de **pics**, sans signification sur de la parole. En sonie de parole active l'écart réel est de **49 dB**, mais il est **localisé** — voir §4. Décidé : normalisation en sonie, gain calculé par `scripts/normaliser_niveaux.py` et inscrit au registre (`niveau_db`, `gain_db`), **aucun wav modifié**. Cibles −23 dBFS pour les paroles et −45 dBFS pour les ambiances, plafond +12 dB. Gain médian +1,0 dB : la correction se concentre sur les aberrants.
- [ ] **Câbler le gain par fragment dans le lecteur.** Le gain est calculé mais **pas encore appliqué au son** : rien n'a changé à l'écoute. Point d'injection identifié — le `*~ 0.9` en sortie de `readsf~` dans `player_state_07` — via un troisième mot dans les lignes des playlists. À faire dans le Proto 08, la même plomberie servant aux plans de présence ([Q10](./Q&A.md#q10)).
- [ ] **Décider du sort des 31 fragments plafonnés.** Le plafond de +12 dB les empêche d'atteindre la cible, et c'est volontaire : `C002` est à −54,9 dBFS pour un fond à −57,7, soit moins de 3 dB d'écart — du fond de salle, pas une voix discrète, et le remonter de 30 dB ne produirait que du souffle. Mais le plafond bloque aussi de la matière réelle : `C011`, `C013` et `C015` ont 14 à 23 dB de dynamique interne. À écouter un par un, puis écarter des pools ou remonter au cas par cas.
- [x] ~~**Trancher [Q9](./Q&A.md#q9) avant de figer la normalisation.**~~ **Tranché le 20 août** : décision du moteur, pas de colonne `PRESENCE` au classeur. Cohérent avec `gain_db` au registre + plan au moteur.

---



## 6. Plus tard — envies, pas des tâches

Conservé pour mémoire. Rien ici n'est nécessaire pour la V1.

- Boucle comme **buffer** réel : enregistrer ce qui a sonné et le réinjecter, plutôt que retirer dans un pool. C'est la « mémoire fantôme » du cahier des charges d'origine (`writesf~` vers `MEMOIRE_VIVANTE`). Écarté le 18 août.
- Un fragment qui **voyage d'une zone à l'autre** en gardant son identité.
- Table pondérée mot / timbre / souffle / contraste pour « le fragment A déclenche le fragment B ».
- Segmentation des longs wav **en direct** dans Pure Data, au lieu d'une découpe préalable.
- Phaser, granulaire, ring modulation.
- Passage à **12 HP**, prévu dans le cahier des charges d'origine. L'installation est à 8 HP aujourd'hui, et la carte de Simon (6 paroles + 2 ambiances) tient exactement dans 8.
- Fiche éthique par région (contexte, cadre, marque de pouvoir), à remplir au fil de l'eau dans la colonne `notes`.

