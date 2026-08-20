# Q&A — ce qui doit être tranché

**20 août 2026.** Questions ouvertes après lecture de `[../Sources/Simon - Cortex et Cortex-Ambiance.md](../Sources/Simon%20-%20Cortex%20et%20Cortex-Ambiance.md)`.

Ce fichier ne contient **que** ce qui est ambigu, incomplet, ou en contradiction avec l'implémentation. Ce qui est clair est dans `[TO DO.md](./TO%20DO.md)`.

**Comment s'en servir :** une réponse écrite sous une question la ferme. Une question fermée reste ici pour la trace, mais ce qui en découle part dans `[TO DO.md](./TO%20DO.md)`, `[../Zones/](../Zones/)` ou `[../Matiere/Attributs.md](../Matiere/Attributs.md)`. L'IA ne code rien qui dépend d'une question encore ouverte : elle demande.

**Ancres — ne pas « corriger ».** Les intitulés sont réduits à `## Qn`, avec le titre en gras dessous. C'est volontaire : les liens `#q1` fonctionnent alors nativement. Les anciennes ancres `<a id="q1"></a>` ont été supprimées par le formateur de l'éditeur en enregistrant, cassant d'un coup les 64 liens internes du projet. Ne pas les remettre.

---

## État

**8 répondues** le 20 août : Q1, Q2, Q3, Q4, Q19, Q20, Q21, Q24.

**2 répondues** le 20 août (après-midi) : Q9, Q10 *(partiel —* `INTERMEDIAIRE` *reporté V1, voir [Q25](#q25))*.

**2 répondues** le 20 août (soir) : Q11, Q25.

**1 répondue** le 20 août (soir, ambiance) : Q23 *(descriptifs seulement — plus bloquante)*.

**1 répondue** le 20 août (soir, sélecteur) : Q8 *(C2 symétrisée + interdictions dures)*.

**7 répondues** le 20 août (session Loumana) : Q5, Q6, Q7, Q13, Q15, Q16, Q17.

**5 ouvertes**, dans cet ordre :


|     | Question                                                                | Bloque quoi                                    |
| --- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| 🔴  | [Q10](#q10) — niveaux exacts de réverb + LFO premier plan               | Presets complets des 12 voix                   |
| 🟠  | [Q18](#q18) — quel niveau d'intelligibilité viser ?                     | Régler le filtre et la réverbération du Cortex |
| 🟡  | [Q12](#q12) — tables C9/C10 (probablement redondantes avec Q11 = 50/50) | Affiner le geste par attributs                 |
| 🟡  | [Q22](#q22)                                                             | Filtre texture `INDETERMINE` (reporté Proto 08) |
| 🟡  | [Q14](#q14)                                                             | Piézo                                          |


**Pourquoi Q10 passait devant.** [Q1](#q1) = 12 voix simultanées ; les plans de présence ([Q9](#q9), [Q10](#q10)) et les gestes temporels ([Q11](#q11)) ne dépendent d'**aucun tag**. [Q11](#q11) tranche : `**EMERGER`/`RECOUVRIR` remplace le pulse** — spec dans `[../Zones/Cortex.md](../Zones/Cortex.md)` §8 bis.

---

# A. Structure des zones

## Q1

**Carte des 8 HP en Cortex**

**Ce que dit Simon.** §1.1 : enceintes **1 à 6** pour le Cortex, chacune diffusant deux fragments superposés (donc **12 fragments de parole simultanés**). Enceinte **7** = ambiance musicale. Enceinte **8** = ambiance texture.

**Ce que fait le patch.** HP1 à HP3 = 3 paires, soit **6 fragments**. HP4 à HP8 = **5 nappes** d'ambiance différentes en même temps, toutes tirées du même pool `CORTEX/AMBIANCE`.

**Pourquoi il faut trancher.** Ce n'est pas un détail de câblage. On passe de 6 à 12 voix de parole simultanées : le CPU double, et surtout la densité perçue change complètement — 12 voix filtrées, c'est du bruit, plus une superposition. Et on passe de 5 nappes à 2, ce qui vide beaucoup l'espace autour des paroles. Les deux versions ont été validées par des personnes différentes : les 5 nappes viennent d'une séance d'écoute du 18 août, les 6 baffles viennent du document de Simon.

**Options.**

- **A** — suivre Simon : 6 baffles de parole × 2 fragments, HP7 musicale, HP8 texture.
- **B** — garder l'existant : 3 paires sur HP1–3, 5 nappes sur HP4–8.
- **C** — intermédiaire : 6 baffles de parole × 2 fragments comme Simon, mais garder plus de deux nappes en les répartissant autrement dans le cycle.
- **D** — 6 baffles de parole mais **pas tous actifs en même temps** : 3 paires actives à un instant donné, qui se déplacent parmi les 6 baffles. Densité de B, occupation spatiale de A.

**Impact.** Réécriture de `cortex_pair_07`, `cortex_amb_07`, `FSM_N_8HP[0]`, les ancrages, et le nombre de lecteurs. C'est le chantier qui justifierait un Proto 08 → [Q24](#q24).

**Réponse :** *A* 

---

## Q2

**« Cortex-Ambiance » : une zone, ou des couches du Cortex ?**

**Ce que dit Simon.** Il en fait une **zone** (§3), avec ses propres attributs, ses propres comportements, sa propre spec. Mais spatialement elle occupe HP7 et HP8 **pendant** que le Cortex occupe HP1–6.

**Ce que fait le patch.** Les zones sont des **états successifs** d'une machine à états : Cortex 40 s, puis Hippocampe 50 s, puis Reconstruction 120 s. Les nappes ne sont pas une zone, ce sont des couches de l'état Cortex, et elles s'arrêtent quand le Cortex s'arrête.

**Pourquoi il faut trancher.** Les deux mots « zone » ne désignent pas la même chose. Chez Simon, c'est un **rôle spatial permanent**. Dans le patch, c'est un **moment dans le temps**. Tant que ce n'est pas clarifié, chaque nouveau document de Simon va produire la même ambiguïté.

**Sous-questions.**

- Pendant l'Hippocampe et la Reconstruction, HP7 et HP8 continuent-ils de diffuser de l'ambiance, ou se taisent-ils ?
- Si oui : est-ce la même ambiance qui continue, ou une ambiance propre à chaque zone ?
- Si l'ambiance est permanente, elle ne fait plus partie du cycle : c'est une **couche de fond** indépendante de la FSM. C'est une modification d'architecture, pas de réglage.

**Réponse :** on va guarder ma definitiond e zone et guarder.1.1.  il ne s'agit pas secifiqument de l'haut parleur 7 ou 8, ca peut etre n'importe quell autre haut parleur qui a l'ambianc HPX et HPX dans cortex (fix),  dans la hippo c'est un peu plus dynamique , ca bouge  de baffle en baffle mais lentement et c'est une ambianc etotalment differente de celle qui etait dans le cortex.  la reconstruction je dirait que il n'en faut pas .

**Complément (20 août, [Q25](#q25)).** Le croisement d'attributs parole/ambiance (ex. Congo au premier plan + milieu « européen ») se fait au **niveau de l'état Cortex entier**, pas par baffle. Deux nappes globales fixes — voir [Q25](#q25).

---

## Q25

**Croisement parole / ambiance : par baffle, ou global ?**

**Ce que dit Simon.** §1.2 : le contraste Belgique/Congo se joue **sur chaque baffle de parole** (règle C1). §3 : les ambiances musicale et texture forment le **milieu sonore** dans lequel les paroles apparaissent — sur **deux enceintes dédiées** (§1.1), pas sur les six baffles de parole.

**L'ambiguïté.** Simon évoque aussi un croisement dramaturgique plus large — par ex. une parole contextualisée au Congo dans un milieu sonore « européen » ou « moderne ». Une lecture possible : une ambiance **par baffle**, avec une couche « intermédiaire » partout. Le Proto 07 a renforcé cette confusion : **5 nappes** sur HP4–8, une ambiance différente par baffle.

**Ce que fait le patch (07).** Chaque baffle HP4–8 porte sa propre nappe, tirée indépendamment. Six compositions parolement différentes **plus** cinq ambiances différentes = trop de contrastes simultanés, pas un lieu cohérent.

**Question.** Le croisement d'attributs entre paroles et ambiances se fait-il :

- **A** — **par baffle** : chaque HP de parole a sa propre ambiance locale en plus de sa paire Belgique/Congo ;
- **B** — **global** : les 6 baffles de parole portent les paires ; **deux nappes communes** (musicale + texture) forment un seul milieu pour tout le Cortex ; le sélecteur choisit **une** ambiance musicale et **une** texture en fonction de l'ensemble des paroles actives, pas par HP.

**Réponse :** **B — global.**

- **Deux baffles d'ambiance fixes** pendant le Cortex ([Q1](#q1), [Q2](#q2)) : une *musicale*, une *texture*. Pas d'ambiance sur les baffles de parole.
- Le croisement dramaturgique (Congo / milieu européen, etc.) se décide **une fois par passage dans le Cortex** : le sélecteur regarde les paroles tirées (ou leurs attributs) et choisit **une paire d'ambiances** pour les deux baffles — pas six micro-milieux.
- `**INTERMEDIAIRE` dans Simon (§2.2.D) = profondeur de parole**, pas une couche d'ambiance par baffle. Pour la V1 : **deux plans de parole seulement** (`PREMIER_PLAN` + `ARRIERE_PLAN`) — le 3ᵉ plan de parole est **reporté**.
- Le Proto 07 (5 nappes / 5 baffles) était une **déviation** ; la cible Proto 08 revient à **2 nappes globales**.

**Conséquences.** `[../Zones/Cortex.md](../Zones/Cortex.md)` §7 bis · `[../Matiere/Attributs.md](../Matiere/Attributs.md)` §6 · sélecteur futur : `gen_paires.py` pour les paires par baffle ; `**gen_ambiance_cortex.py`** (ou équivalent) pour **une** ligne ambiance par état Cortex.

---

## Q3

**Durée des ambiances : 30 s – 7 min, ou atomes de 2 s ?**

**Ce que dit Simon.** §3.3 : « Tous les fragments d'ambiance musicale ou de texture durent entre **30 secondes et 7 minutes**. »

**Ce que fait le patch.** `CORTEX/AMBIANCE` contient **27 atomes découpés à partir de 2 s**, re-déclenchés toutes les 14 s par `cortex_amb_pulse_07`.

**Pourquoi il faut trancher.** C'est une contradiction de matière, pas de réglage. Un atome de 2 s relancé toutes les 14 s ne peut pas produire « le milieu sonore dans lequel les paroles apparaissent » — et ça contredit directement l'interdiction des « découpes rapides » du §3.7. Par ailleurs 7 minutes est plus long que l'état Cortex tout entier (40 s), donc une ambiance ne serait jamais entendue en entier.

**Options.**

- **A** — ne plus découper la piste d'ambiance : un master d'ambiance = un ou quelques longs wav, lus en boucle ou en fondu.
- **B** — garder la découpe mais relever fortement le seuil (30 s minimum), ce qui suppose que les masters contiennent bien des plages continues aussi longues.
- **C** — garder les atomes courts et assumer que la nappe est un tissu de petits éléments, en contradiction avec le document.

**À vérifier avant de répondre :** les masters d'ambiance actuels (`SONS_V2/WIP/Opacité V6/`) contiennent-ils des plages continues de 30 s et plus, ou sont-ils déjà faits de courts éléments séparés par des silences ?

**Impact.** `scripts/proto07/slice_opacite_v3.py` (règle de découpe), les pools, `cortex_amb_pulse_07`.

**Réponse :** *B*

---

# B. Matière et classification

## Q4

**La matière Belgique / Congo existe-t-elle ?**

**Ce que dit Simon.** La règle **C1** est obligatoire : chaque baffle de parole superpose un fragment `CONTEXTE = BELGIQUE` et un fragment `CONTEXTE = CONGO`. Jamais deux du même contexte.

**Ce que fait le patch.** Les fragments du Cortex viennent d'**un seul master** découpé, sans aucune distinction de contexte. Le tirage est au hasard dans un pool unique.

**Pourquoi il faut trancher.** C1 est la règle fondatrice de toute la dramaturgie du Cortex, et elle est **impossible aujourd'hui**. Il faut savoir d'où vient l'information.

**Sous-questions.**

- Simon livre-t-il deux masters séparés (`Cortex Belgique` et `Cortex Congo`), ou bien le contexte se renseigne-t-il à la main dans le tableau, fragment par fragment ?
- Y a-t-il **assez** de fragments de chaque côté ? Avec 3 paires simultanées il faut au moins 3 Belgique + 3 Congo disponibles à chaque instant sans répétition ; avec 6 paires ([Q1](#q1) option A), il en faut 6 + 6.
- Que fait le moteur si un côté est épuisé — il répète, il relâche C1, ou il réduit le nombre de baffles actifs ?

**Réponse :** *Ce n'est pas encore document dans le tableau. le cortex se servira du tableau . je ne sais pas encore si il y a assez fragment. il repete.Pour le moment pas implementé car tableua de classification necessaire* 

---

## Q21

**🔴 Les ID de samples ne sont pas stables**

**Le problème.** `slice_opacite_v3.py` **vide** `SONS_V3/` puis renumérote tout depuis le début. Les noms (`C002_v3_cortex.wav`, `A43_v3_cortex_ambiance.wav`…) dépendent de l'ordre de découpe. Si Simon livre un nouveau master, ou si on change un paramètre de découpe, **tous les ID changent**.

**Pourquoi c'est le blocage numéro un.** Le travail de classification, c'est plusieurs heures d'écoute pour renseigner à la main le contexte, le type de discours, la fonction sociale et la densité de chaque fragment. Si les ID bougent après, **ce travail est perdu** et il est impossible de savoir quelle ligne correspond à quel son.

**Il faut donc résoudre ça avant de commencer à remplir le tableau, pas après.**

**Options.**

- **A** — découpe incrémentale : ne plus vider `SONS_V3/`, n'ajouter que les nouveaux fichiers, ne jamais réattribuer un numéro déjà utilisé. Fusion du tableau sur la clé du nom de fichier, en conservant les colonnes déjà remplies.
- **B** — ID dérivé du contenu (empreinte du signal ou position dans le master), donc stable par construction même en cas de re-découpe complète.
- **C** — geler la découpe : on décide que `SONS_V3/` tel qu'il est aujourd'hui est définitif, on ne relance plus jamais le script, et toute matière nouvelle est ajoutée à la main.

**Recommandation.** A, avec l'option C comme filet immédiat : sauvegarder une copie de `SONS_V3/` avant toute autre manipulation, puisque le projet n'est pas sous git.

**Réponse :** *A. Les samples ici vont rester et la liste va s'aggrangrire.*

---

## Q20

**Structure du tableau de classification**

**Ce que dit Simon.** §5 : deux tables, une pour les fragments du Cortex, une pour les fragments de Cortex-Ambiance. Avec, pour le Cortex, une colonne « Traitement ou comportement autorisé ».

**Ce qui existe.** `Matiere/catalogue_fragments.xlsx`, **3 feuilles** — Cortex, Hippocampe, Reconstruction — avec ID et type pré-remplis automatiquement.

**Questions.**

- Structure finale : 3 feuilles par zone, ou 2 feuilles par nature (paroles / ambiances) ? Les ambiances du Cortex sont aujourd'hui mélangées dans la feuille Cortex, alors que leurs attributs sont complètement différents de ceux des paroles.
- La colonne « traitement autorisé » : est-ce souhaitable ? Elle met le sound design **dans le tableau**, fragment par fragment. Ça va contre le principe qu'on est en train d'établir — la zone impose son timbre, pas le fichier. Proposition : la supprimer, et ne garder que des attributs **descriptifs** du contenu. Le traitement est décidé par la zone, et éventuellement modulé par les attributs.
- Faut-il une colonne libre `notes` pour l'écoute et le contexte éthique ?

**Réponse :** *1 feuilles par zonne avec touts les samples leurs type et attribut, il y a effectivement des "prefenve" ou priorité" de, et peut etre les traitement souhaité je ne sais pas encore* 

---

## Q19

**Périmètre : et les trois autres zones ?**

**Constat.** Le document de Simon ne couvre que le Cortex et Cortex-Ambiance. L'Hippocampe, la Reconstruction et la Boucle n'ont **aucune spec** de sa part.

**Questions.**

- Ces trois zones restent-elles sur l'implémentation actuelle en attendant un document équivalent ? (C'est ce qu'on suppose dans `[../Zones/](../Zones/)`.)
- Le vocabulaire d'attributs (`CONTEXTE`, `TYPE_DISCOURS`, `FONCTION_SOCIALE`, `DENSITE_PAROLE`) s'applique-t-il aussi à leurs fragments, ou seulement à ceux du Cortex ? Le classeur a une feuille par zone, donc la question se pose concrètement au moment de remplir.
- Faut-il demander à Simon un document du même format pour l'Hippocampe avant de continuer, ou figer l'Hippocampe à l'oreille d'abord et lui présenter le résultat ?

**Recommandation.** Figer l'Hippocampe à l'oreille maintenant, sans attendre : c'est la zone la plus propre parce qu'elle n'a pas de contradiction à résoudre.

**Réponse :** *on y va pas a pas, pour le moment seule le cortex a ete donné, il travaille sur l'hippocamp.  oui . oui s'applique a tout les fragments. oui, il tratravaille desssus , ca arrive.*

---

## Q24

**Nouveau prototype, ou modification du Proto 07 ?**

**Le contexte.** Si [Q1](#q1) part vers l'option A ou C, il faut réécrire la carte des HP, les paires, les nappes, et ajouter un sélecteur piloté par le tableau. Ça touche presque tout le moteur du Cortex.

**Options.**

- **A** — Proto 08, nouveau jeu de fichiers. Le 07 devient figé comme le 06 l'est déjà. On peut comparer les deux à l'oreille en relançant l'un ou l'autre. C'est la pratique établie du projet.
- **B** — faire évoluer le 07 en place. Moins de fichiers, mais on perd la possibilité de revenir en arrière — d'autant que le projet n'est pas sous git.

**Recommandation.** A, mais **seulement quand [Q1](#q1) est tranché**. Créer un Proto 08 avant de savoir ce qu'il doit faire ne servirait à rien. Entre-temps, le travail de gel des zones (points 2 de la demande) se fait dans le 07.

**Réponse :** *A.*

---

# C. Règles d'association des fragments

## Q7

**🟠 « À privilégier » : contrainte dure ou préférence ?**

**Ce que dit Simon.** Les tables C2 et C3 donnent les types « **compatibles à privilégier** » pour le second fragment.

**Pourquoi c'est l'ambiguïté la plus dangereuse.** « Privilégier » n'est pas « exiger ». Un algorithme doit savoir quoi faire quand **aucun** candidat compatible n'est disponible — ce qui arrivera forcément, surtout au début quand le tableau sera peu rempli, ou sur les combinaisons rares. Sans réponse, le moteur peut se bloquer, ou bien un développeur choisit à sa place et on découvre le comportement à l'oreille trois semaines plus tard.

**Options en cas d'échec de la recherche.**

- **A** — relâcher : on prend n'importe quel fragment du contexte opposé, C1 reste la seule règle dure.
- **B** — relâcher par étapes : d'abord abandonner C3 (fonction sociale), puis C2 (type de discours), et ne jamais abandonner C1.
- **C** — retirer le premier fragment et retenter l'association.
- **D** — laisser le baffle avec un seul fragment pendant ce tour.

**Recommandation.** B, avec l'ordre de relâchement explicitement écrit. C'est la seule option qui dégrade de façon prévisible et qu'on peut entendre.

**Réponse :** **B — relâcher par étapes.** Ordre fixe en cas d'échec de recherche du 2ᵉ fragment :

1. Appliquer **C2** (`TYPE_DISCOURS`) en priorité — voir [Q5](#q5).
2. Si aucun candidat : **abandonner C3** (`FONCTION_SOCIALE`), garder C2.
3. Si toujours aucun : **abandonner C2**, ne garder que **C1** (Belgique + Congo, contextes opposés).
4. **C1 ne se relâche jamais.**

Tirage final parmi les candidats restants : **au hasard**, non déterministe — voir [Q6](#q6). Spec : [`../Matiere/Attributs.md`](../Matiere/Attributs.md) §6 bis.

---

## Q5

**Priorité entre type de discours et fonction sociale**

C'est le point 1 de la liste de Simon lui-même (§6).

**Le problème.** C2 raisonne sur `TYPE_DISCOURS`, C3 sur `FONCTION_SOCIALE`. Rien ne dit quoi faire quand les deux tables proposent des candidats différents.

**Options.** Priorité au type de discours · priorité à la fonction sociale · poids égal et tirage au hasard entre les deux ensembles · intersection obligatoire (mais voir [Q7](#q7) : l'intersection sera souvent vide).

**Réponse :** **Priorité au `TYPE_DISCOURS` (C2).** En cas de conflit entre les candidats proposés par C2 et C3, C2 l'emporte. C3 ne sert qu'en relâchement ([Q7](#q7)). Si les deux axes pointent vers des ensembles différents, on filtre d'abord par C2, puis on tire au hasard dans le résultat ([Q6](#q6)).

---

## Q6

**La double compatibilité doit-elle augmenter la probabilité ?**

Point 2 de la liste de Simon, et déjà signalé par lui au §2.3 C4.

**La question.** Quand un candidat est compatible **à la fois** sur le type de discours et sur la fonction sociale, faut-il le favoriser, ou les deux axes restent-ils indépendants et de poids égal ?

**Remarque.** Si on favorise, il faut dire de combien. « Deux fois plus probable » et « toujours choisi si disponible » ne donnent pas du tout le même résultat à l'écoute : le second rend la sélection déterministe et donc répétitive.

**Réponse :** **Non déterministe — pas de bonus de probabilité.** Quand un candidat est compatible sur les **deux** axes (C2 et C3), il n'est **pas** favorisé : on tire **uniformément** parmi **tous** les candidats encore valides après filtrage. Pas de « toujours choisi si double compatibilité » — ça éviterait la répétitivité.

---

## Q8

**La table C2 n'est pas symétrique**

**Le constat.** En lisant la table C2 :

- `FAMILIAL` → `ADMINISTRATIF` ou `DESCRIPTIF`
- `MEDIATIQUE` → `DESCRIPTIF` ou `FAMILIAL`

Donc la paire **familial + médiatique** est autorisée si le médiatique est tiré en premier, et interdite si c'est le familial. Le même couple de fragments est valide ou non selon l'ordre de tirage. Or l'ordre logique du §4 impose de tirer d'abord un `BELGIQUE` puis de chercher un `CONGO`.

**Conséquence.** La table se comporte comme **orientée Belgique → Congo**. Si ce n'est pas l'intention, il y a un biais dramaturgique caché : certaines combinaisons ne se produiront jamais dans un sens.

**Options.**

- **A** — assumer l'orientation : on tire toujours le Belgique d'abord, la table se lit dans ce sens.
- **B** — symétriser : une paire est valide si elle est compatible dans **au moins un** des deux sens.
- **C** — Simon reprend la table pour qu'elle soit symétrique par construction.

**Réponse (20 août) :** **B — symétriser**, avec interdictions dures ajoutées.

**La table C2 de Simon est conservée comme référence** (on ne réécrit pas le PDF), mais **l'implémentation ne la lit pas de façon orientée**. Une paire `(A, B)` est compatible sur le type de discours si la table C2 (via C4 pour les tags multiples) valide `**A → B` ou `B → A`**. Ça supprime le biais Belgique-toujours-en-premier : C1 impose toujours un `BELGIQUE` et un `CONGO` sur le baffle, mais **l'ordre de tirage ne change plus** la validité C2.

**Interdictions dures** (prioritaires sur la table — paire **jamais** générée) :


| Interdit                   | Source                                   |
| -------------------------- | ---------------------------------------- |
| `POLITIQUE` ↔ `FAMILIAL`   | Loumana — pas de familial avec politique |
| `POLITIQUE` ↔ `MEDIATIQUE` | Simon — jamais associés                  |


Si l'un porte `POLITIQUE` et l'autre `FAMILIAL` **ou** `MEDIATIQUE` → **refus**, même si la table C2 asymétrique semblait l'autoriser dans un sens.

**Conséquences.** Règle d'implémentation dans `[../Matiere/Attributs.md](../Matiere/Attributs.md)` §2 bis · `gen_paires.py` : symétrie + filtre d'interdiction avant écriture des paires. Le document source de Simon reste intact ; c'est **le moteur** qui corrige l'asymétrie.

# D. Présence et densité

## Q9

`**PRESENCE` : attribut du fichier, ou décision du moteur ?**

**Le doute vient du document lui-même.** §2.2.D dit que la présence « n'est pas nécessairement une caractéristique fixe du fichier : elle peut être attribuée ou modifiée par Pure Data au moment de la lecture ». Mais §5.1 la met comme colonne du tableau, et C7 demande explicitement de **varier** les rôles au fil des occurrences.

**Ce que fait le patch.** Rien. Les deux fragments d'une paire sont sommés à poids égal (`+~` dans `cortex_pair_07`). Il n'y a aucune notion de plan.

**Proposition à valider.** La présence est **toujours** décidée par Pure Data, jamais lue dans le tableau. Le tableau ne sert qu'à **interdire** certains plans, via la densité (règle C8). C'est cohérent avec C7 qui veut de la variation, et avec le principe « la zone impose le timbre ».

**Réponse :** **Décision du moteur.** Pure Data attribue le plan à chaque lecture ; le tableau **ne contient pas** de colonne `PRESENCE`. Le classeur sert seulement à **interdire** certaines combinaisons de plans via `DENSITE_PAROLE` (règle C8, à préciser en [Q13](#q13)). C'est cohérent avec C7 (les rôles doivent varier d'une occurrence à l'autre) et avec le principe « la zone impose le timbre » — la normalisation des niveaux (`[../Matiere/Pipeline.md](../Matiere/Pipeline.md)`) et le plan de présence sont donc tous deux des décisions du moteur, pas des attributs du fichier.

---

## Q10

**🟠 Que sont concrètement les trois plans ?**

Point 5 de la liste de Simon. C'est la question à laquelle il faut répondre pour construire quoi que ce soit.

**Les trois plans sont un objet de sound design, pas seulement un gain.** « Arrière-plan » ne veut pas dire « plus bas de 10 dB », ça veut dire « plus loin ». Donc pour chaque plan : gain, LPF, réverbération, HPF.


|                 | Gain               | LPF (balayage)                                             | Réverbération            | HPF           |
| --------------- | ------------------ | ---------------------------------------------------------- | ------------------------ | ------------- |
| `PREMIER_PLAN`  | normal (référence) | **800 → max** (2000 Hz), **vitesse différente** des autres | **moins** que l'existant | **300 Hz**    |
| `INTERMEDIAIRE` | *à compléter*      | *à compléter*                                              | *à compléter*            | *à compléter* |
| `ARRIERE_PLAN`  | **−2 dB**          | **500 → 1000 Hz**                                          | **oui**                  | **aucun**     |


**Questions.**

- Combien de dB entre chaque plan ?
- Un plan plus lointain est-il **aussi** plus filtré et plus réverbéré, ou seulement plus bas ?
- Les trois plans sont-ils fixes, ou le plan est-il lui-même en mouvement lent (un fragment qui s'éloigne) ?
- Comment ces trois plans se combinent-ils avec le balayage de LPF 500–2000 Hz déjà en place sur toutes les couches ?

**Comment y répondre.** Les construire comme trois presets nommés, forçables à la main dans l'interface, et les écouter sur la même paire de fragments. C'est du travail d'oreille pur, faisable **maintenant**, sans aucun tag.

**Réponse (20 août, partielle).** Deux plans sur trois :

- `**PREMIER_PLAN**` : gain normal ; LPF balayé **800 Hz → max** (plafond = 2000 Hz du Cortex), avec une **vitesse de balayage différente** des autres plans ; **moins** de réverbération qu'aujourd'hui ; HPF **300 Hz**.
- `**ARRIERE_PLAN**` : gain **−2 dB** ; LPF balayé **500 → 1000 Hz** ; **réverbération oui** ; **pas de HPF**.

**Encore ouvert :** niveaux exacts de réverbération, vitesse LFO du premier plan, plans fixes ou mouvants ([Q18](../Backlog/Q&A.md#q18)).

`**INTERMEDIAIRE` — reporté V1 ([Q25](#q25)).** Ce n'est **pas** une ambiance par baffle. Dans Simon (§2.2.D) c'est un 3ᵉ **plan de profondeur pour la parole**. Pour la V1 on n'en implémente que **deux** : `PREMIER_PLAN` + `ARRIERE_PLAN`. Le 3ᵉ plan parole pourra revenir plus tard si les deux ne suffisent pas à l'oreille.

**Conséquences.** Spec détaillée dans `[../Zones/Cortex.md](../Zones/Cortex.md)` §5 bis. À implémenter dans le Proto 08 : chaque fragment d'une paire reçoit son propre preset de plan (deux gains + deux chaînes FX), le moteur choisissant qui est en premier plan et qui en arrière.

---

## Q13

`**DENSITE_PAROLE`, et la règle C8 est peut-être redondante**

**Ce qui manque.** Simon le signale lui-même (point 3) : l'attribut `DENSITE_PAROLE = FAIBLE / MOYENNE / FORTE` n'existe pas encore. Il faut l'ajouter au tableau et le renseigner à l'oreille.

**Le problème de logique.** C8 dit : « Pd ne peut pas placer deux fragments très denses **au même niveau de présence** ». Mais C5 interdit déjà que les deux fragments d'un baffle aient le même niveau de présence, quels qu'ils soient. Donc C8, lu littéralement, n'ajoute **rien**.

**L'intention est probablement autre :** deux fragments très denses doivent être **éloignés** l'un de l'autre dans les plans, pas seulement différents. Ce qui donnerait : si les deux sont `FORTE`, la seule combinaison permise est `PREMIER_PLAN` + `ARRIERE_PLAN`, en excluant `PREMIER_PLAN` + `INTERMEDIAIRE`.

**Question.** Est-ce la bonne lecture ?

**Aussi.** Que veut dire « dense » exactement — un débit de parole rapide, un fragment sans silence, plusieurs voix dans le même fragment ? Il faut une définition utilisable à l'écoute, sinon la colonne sera remplie de façon incohérente.

**Réponse :** **Oui — bonne lecture.** C8 complète C5 : si les **deux** fragments sont `DENSITE_PAROLE = FORTE`, ils doivent être aux **extrémités** des plans — `PREMIER_PLAN` + `ARRIERE_PLAN` uniquement (pas deux plans « proches »). En V1 (deux plans seulement, [Q25](#q25)) c'est automatique ; la règle deviendra contraignante quand un 3ᵉ plan existera. À implémenter dans `gen_paires.py` · [`../Matiere/Attributs.md`](../Matiere/Attributs.md) §2 ter.

**Encore ouvert :** définition opérationnelle de « dense » à l'oreille (débit, silence, multi-voix) — à documenter en remplissant la colonne `densite_parole`.

---

# E. Comportements temporels

## Q11

**🟠** `EMERGER` **/** `RECOUVRIR` **: paramètres, et conflit avec le pulse**

Point 4 de la liste de Simon, plus un conflit d'architecture qu'il ne pouvait pas voir.

**Ce que dit Simon.** §2.5. `EMERGER` : le second fragment apparaît progressivement au-dessus du premier. `RECOUVRIR` : le second monte jusqu'à masquer partiellement ou fortement le premier.

**Ce que fait le patch.** Rien de tel. `cortex_pulse_07` **relance** les six couches toutes les 10 s, avec un échelonnement de 80 à 880 ms.

**Le conflit.** Les deux logiques sont incompatibles. Si on relance toutes les 10 s, aucun fondu progressif n'a le temps de se déployer : on entend des redémarrages, pas une émergence. Il faut choisir l'un ou l'autre.

**Et le budget temps est serré.** L'état Cortex dure 40 s. Un fragment fait de 13 à 30 s. Si `EMERGER` prend 15 s de fondu, il ne se passe qu'une seule émergence par passage dans le Cortex. Est-ce l'intention — un seul geste par visite — ou faut-il des fondus beaucoup plus courts ?

**Paramètres à fixer.**

- durée du fondu d'`EMERGER`
- durée du fondu de `RECOUVRIR` et **niveau maximal** atteint (« partiellement » et « fortement » sont deux choses différentes : jusqu'à quel dB ?)
- durée de coexistence des deux fragments avant que le geste ne commence
- probabilité respective des deux comportements
- ce que devient `cortex_pulse_07`

**Réponse (20 août).**

**Choix d'architecture :** `EMERGER` **/** `RECOUVRIR` **remplace le pulse.** On abandonne `cortex_pulse_07` (re-déclenchement toutes les 10 s). Chaque paire lit ses deux fragments **une fois** par passage ; le geste temporel se joue **à l'intérieur** de la paire, pendant la durée du sample.

**Durées de fondu.**


| Geste       | Durée        | Cible                                                                                                                                                                                                                                                                                        |
| ----------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EMERGER`   | **6 à 10 s** | le 2ᵉ fragment monte progressivement **jusqu'au niveau de son plan de présence**                                                                                                                                                                                                             |
| `RECOUVRIR` | **3 à 6 s**  | idem — le « niveau max » **est** le niveau normal du plan assigné au fragment qui recouvre, pas un boost au-dessus. Pas de « partiellement / fortement » en dB supplémentaires : on monte jusqu'au preset (`PREMIER_PLAN`, etc.), le masquage vient du contraste de plans + du fondu relatif |


**Décalage entre couches.** Toutes les paires ne doivent **pas** émerger ou changer en même temps. Chaque paire (chaque couche) reçoit un **décalage aléatoire** avant le début du geste — même principe que l'échelonnement actuel du pulse (80–880 ms), mais adapté aux fondus de 3–10 s et étendu aux 12 paires.

**Coexistence — pas une durée fixe, trois cas.**

1. **Coexistence permanente** : les deux fragments restent à leur plan respectif pendant toute la durée du sample, sans geste (ou geste nul).
2. **Recouvrement / émergence dès le début** : le geste démarre **à t = 0** du sample (le 2ᵉ monte dès l'ouverture).
3. **Durée liée au sample** : la longueur du fragment conditionne ce qui est possible — un sample court peut n'accueillir qu'un fondu partiel ; un long laisse le geste se jouer en entier puis une coexistence stable.

Le moteur choisit le cas (probablement en fonction de la durée du sample et du geste tiré).

**Probabilité.** **50 / 50** entre `EMERGER` et `RECOUVRIR` (tirage au hasard par paire, à chaque occurrence).

**Autres mouvements.** À ajouter plus tard — hors scope V1 ; noter dans le Proto 08 un point d'extension (`geste` extensible au-delà de EMERGER/RECOUVRIR).

**Conséquences.** Spec détaillée : `[../Zones/Cortex.md](../Zones/Cortex.md)` §8 bis. `cortex_pulse_07` **supprimé** dans le Proto 08. [Q12](#q12) : les tables C9/C10 deviennent probablement **redondantes** pour la V1 (50/50 partout) — à trancher si un jour le geste doit dépendre des attributs.

---

## Q12

**Les tables C9 et C10 ne discriminent rien**

**Le constat.** Dans les deux tables, la colonne « Comportement du deuxième fragment » vaut `EMERGER` **ou** `RECOUVRIR` sur **toutes** les lignes, sans exception.

Autrement dit : quelle que soit la combinaison d'attributs, les deux comportements sont permis. Les tables C9 et C10 n'apportent donc **aucune information exploitable** — elles disent seulement « c'est toujours l'un ou l'autre ».

**Questions.**

- Est-ce voulu ? Si oui, on peut supprimer les deux tables et écrire simplement : le comportement est tiré au hasard entre `EMERGER` et `RECOUVRIR`, avec les probabilités de [Q11](#q11).
- Ou bien certaines lignes devaient-elles imposer **un seul** comportement ? Par exemple : un fragment `CLASSER` ou `NOMMER` qui arrive sur un `RACONTER` **recouvre** (l'administratif écrase le témoignage), alors qu'un `RACONTER` qui arrive sur un `EXPLIQUER` **émerge**. Ce serait dramaturgiquement bien plus fort, et ça donnerait un sens aux tables.

**Note (20 août).** [Q11](#q11) fixe **50/50** pour la V1. Les tables C9/C10 sont donc **redondantes** tant qu'on ne tranche pas la seconde option ci-dessus. Pour le Proto 08 : tirage 50/50, tables ignorées.

**Réponse :** *à remplir — probablement « redondantes pour V1, réviser quand le classeur sera rempli »*

---

# F. Ambiances

## Q15

**La modulation d'amplitude lente casse-t-elle la continuité ?**

**Ce que dit Simon.** §3.7 interdit sur les ambiances : le delay, les découpes rapides, la fragmentation granulaire. « Les ambiances doivent conserver leur continuité. »

**Ce que fait le patch.** `cortex_amb_07` applique à chaque nappe une modulation d'amplitude de 0,030 à 0,074 Hz — soit une période de 13 à 33 s — d'une profondeur de 0,10 autour de 0,78. Aucun delay, aucune réverbération, aucun filtre audible.

**La question.** Est-ce que cette respiration très lente entre dans l'interdiction, ou est-ce acceptable ? À première vue non — ce n'est ni une découpe ni un delay, et c'est bien plus lent que ce que le §3.7 vise. Mais c'est à trancher à l'oreille, avec Simon si possible.

**Et le re-déclenchement toutes les 14 s ?** Celui-là, en revanche, ressemble bien à une découpe rapide — voir [Q3](#q3).

**Réponse :** **Oui — petite modulation de volume lente acceptée.** Conforme au Proto 07 (AM 13–33 s, profondeur ~0,10) : ce n'est ni delay ni découpe. **Idée future (non V1) :** HPF momentané ~350 Hz déclenché par le piézo — effet bref « pièce qui s'ouvre », lié à [Q14](#q14). Spec : [`../Zones/Cortex.md`](../Zones/Cortex.md) §7.

---

## Q16

`**SE_DEPLACER` sur un seul baffle est impossible**

**Ce que dit Simon.** §3.6 : la texture a le comportement `SE_DEPLACER` — « la texture circule dans l'espace sonore ». §3.2 : la texture est sur l'enceinte **8**.

**La contradiction est dans le document.** On ne peut pas circuler dans l'espace en restant sur un seul haut-parleur.

**Options.**

- **A** — la texture a le droit de sortir de HP8 et de circuler sur plusieurs baffles. Techniquement facile : c'est déjà ce que fait la nappe de l'Hippocampe (mode 4). Mais alors elle vient se mélanger aux baffles de parole.
- **B** — la texture reste sur HP8 et `SE_DEPLACER` devient un mouvement **interne** : un panoramique lent entre HP7 et HP8, ou un mouvement dans le contenu même de la texture plutôt que dans l'espace.
- **C** — abandonner `SE_DEPLACER` pour la texture.

**Et le point 7 de la liste de Simon.** Il demande de définir la trajectoire spatiale de `SE_DEPLACER` — ce qui suggère qu'il pense bien à un déplacement réel, donc l'option A.

**Réponse :** **Option fixe — pas de déplacement en Cortex.** La texture reste sur **son baffle fixe** (HPX, [Q2](#q2)). `SE_DEPLACER` de Simon **n'est pas implémenté** dans la zone Cortex — incompatible avec [Q25](#q25) (2 nappes globales fixes). Le mouvement spatial de l'ambiance reste réservé à l'**Hippocampe** ([Q2](#q2)).

---

## Q17

**HP7 et HP8 peuvent-ils recouvrir en même temps ?**

Point 6 de la liste de Simon.

`RECOUVRIR` existe pour l'ambiance musicale **et** pour la texture. Si les deux le font simultanément, les paroles du Cortex disparaissent complètement. Est-ce un moment recherché — un effacement total, une respiration de l'installation — ou faut-il un verrou empêchant les deux recouvrements de se superposer ?

**Réponse :** **Verrou — jamais les deux en `RECOUVRIR` simultanément.** Si l'ambiance musicale est en recouvrement actif, la texture ne peut pas l'être en même temps (et inversement). Évite d'effacer complètement les paroles du Cortex. À implémenter dans le gestionnaire de comportements ambiance du Proto 08 · [`../Zones/Cortex.md`](../Zones/Cortex.md) §7 bis.

---

## Q22

**Une ambiance** `INDETERMINE` **est filtrée comment ?**

**Ce que dit Simon.** §3.4 et §3.5 : « Lorsque `ESPACE = EXTERIEUR`, l'ambiance n'est pas filtrée. »

**Ce qui manque.** L'ambiance musicale n'a que la valeur `EXTERIEUR`, donc elle n'est jamais filtrée — cohérent. Mais la texture peut valoir `EXTERIEUR` **ou** `INDETERMINE`. Par contraste, une texture `INDETERMINE` est donc filtrée — mais le document ne dit ni comment, ni pourquoi, ni avec quelles valeurs.

**Question.** Que veut dire « filtrée » ici, et quel est l'effet visé ? Si c'est pour donner une sensation d'intérieur, c'est un traitement de distance analogue à celui des paroles, et il faut le décrire au même endroit.

**Statut (20 août).** **Plus bloquante pour la V1**, mais **pas obsolète**. [Q25](#q25) réduit la portée : une **seule** texture globale sur un baffle — un traitement `INDETERMINE` vs `EXTERIEUR` à régler **à l'oreille** quand la chaîne ambiance du Proto 08 existera. Simon ne donne pas les valeurs.

**Réponse :** **reportée Proto 08.** Provisoire jusqu'à écoute : `ESPACE = EXTERIEUR` → pas de filtre (sec, §3.7) ; `ESPACE = INDETERMINE` → filtre « intérieur » léger sur le baffle texture (LPF à fixer avec [Q18](#q18), pas les mêmes valeurs que les paroles §5 bis). Détail à figer dans `[../Zones/Cortex.md](../Zones/Cortex.md)` §7 quand les nappes passeront de 5 à 2.

---

## Q23

**Trois attributs d'ambiance ne servent à aucune règle**

**Le constat.** Les tables §3.4 et §3.5 définissent `ACTIVITE`, `CONTINUITE` et `PRESENCE_HUMAINE`. **Aucune règle du document ne les utilise.** Seul `ESPACE` a une conséquence ([Q22](#q22)).

**Questions.**

- Sont-ils descriptifs, pour aider à choisir à la main, ou doivent-ils piloter quelque chose ?
- Intuitions à valider : `CONTINUITE = EVENEMENTIELLE` devrait interdire `RESTER` (une ambiance faite d'événements ne peut pas être stable) ; `ACTIVITE = FORTE` devrait limiter le niveau de `RECOUVRIR` ; `PRESENCE_HUMAINE = IDENTIFIABLE` devrait être rare, parce qu'une voix reconnaissable dans la texture concurrence les paroles du Cortex.
- Si ce sont des attributs purement descriptifs, autant l'écrire dans le tableau pour ne pas les chercher plus tard.

**Réponse :** **Descriptifs pour le classeur** — aider à choisir et documenter à l'oreille. **Aucune règle automatique en V1.** Les intuitions ci-dessus (`EVENEMENTIELLE` ≠ `RESTER`, etc.) sont des **pistes** pour `gen_ambiance_cortex.py` plus tard, pas des contraintes dures. Remplir la colonne si utile à l'écoute lors de la classification ; sinon laisser vide. Ne pas bloquer le Proto 08 ni des heures de classement sur ces trois colonnes.

---

# G. Timbre

## Q18

**🟠 Quel niveau d'intelligibilité viser exactement ?**

**Ce que dit Simon.** §1.3 : l'écoute doit être « floutée et dissipée », comme venant d'une pièce voisine. §2.6 : « Les conversations et les monologues restent encore **trop clairement intelligibles**. »

**Ce que fait le patch.** HPF 450–630 Hz, LPF balayant 500–2000 Hz, saturation 0,55–0,65, et 10 % de wet sur un delay de 180 ms.

**Pourquoi c'est une question et pas une tâche.** « Plus flou » n'est pas une consigne réglable. Il faut une cible qu'on puisse vérifier à l'oreille et défendre en salle. Trois cibles très différentes :

- **A** — on reconnaît les mots mais on perd le sens de la phrase.
- **B** — on reconnaît qu'il y a de la parole, la langue peut-être, mais pas les mots.
- **C** — on ne reconnaît même plus que c'est de la parole : c'est devenu une texture vocale.

Ces trois cibles ne demandent pas les mêmes réglages, et surtout elles n'ont pas les mêmes conséquences éthiques et dramaturgiques. En C, le contenu des témoignages disparaît complètement — ce qui peut être exactement l'intention (« mémoires en transit ») ou exactement ce qu'il faut éviter.

**À noter :** la cible peut varier avec le plan de présence — `PREMIER_PLAN` en A, `ARRIERE_PLAN` en C. C'est probablement la bonne réponse, et ça relie cette question à [Q10](#q10).

**Une piste technique.** Ce qui manque le plus n'est peut-être pas un filtre plus fermé, mais une **vraie réverbération**. Un delay à 180 ms avec 6 % de feedback ne fabrique pas une pièce voisine. Une réverbération courte et sombre détruit l'intelligibilité bien plus efficacement qu'un passe-bas, et sans faire perdre le caractère de la voix. → `[TO DO](./TO%20DO.md)`.

**Réponse :** *à remplir*

---

# H. Capteurs

## Q14

**Le piézo fait l'inverse de ce qui est implémenté**

**Ce que dit Simon.** §3.8 : si le piézo est déclenché, **arrêter** Cortex-Ambiance et **permettre le passage** vers une autre zone. Le capteur est donc un déclencheur de transition.

**Ce que fait le patch.** `presence_07` mesure le niveau RMS de l'entrée micro. Quand le niveau est **bas** (< 0,12), il envoie `s6_cortex_hold 1` qui **gèle** l'horloge de la FSM : le Cortex reste. Au-dessus de 0,45, il relâche.

**Ce sont deux logiques opposées.** Chez Simon, l'événement **pousse** vers la zone suivante. Dans le patch, l'absence de public **retient** dans le Cortex.

**Questions.**

- Garder le hold (silence = on reste) **et** ajouter le piézo comme déclencheur de transition ? Les deux peuvent coexister : ils ne parlent pas du même capteur.
- Ou remplacer le hold par la logique de Simon ?
- **Piézo et micro ne sont pas le même capteur.** Un piézo est un capteur de contact ou de vibration : il faut savoir combien il y en a, où, et sur quoi ils sont collés. Le cahier des charges parle de 2 micros d'ambiance, jamais de piézos. Le matériel n'existe pas encore.
- Paramètres à fixer (points 8 de la liste de Simon) : seuil de déclenchement, arrêt immédiat ou fondu de sortie et sa durée, quelle zone est appelée ensuite, délai minimum avant qu'une ambiance puisse réapparaître.

**Contrainte non négociable, rappel.** Le micro et les piézos ne vont **jamais** vers `dac~`. Ils ne servent qu'à piloter.

**Réponse :** *à remplir*