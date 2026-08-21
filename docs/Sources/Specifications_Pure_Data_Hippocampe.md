# Installation sonore — Attributs et comportements

## Spécifications pour Pure Data — Zone 3 : Hippocampe

Ce document décrit les attributs et les comportements de la zone **Hippocampe**, ainsi que ceux de la zone associée **Hippocampe–Ambiance**.

Il est destiné à permettre leur traduction dans Pure Data.

> **Principe de lecture pour le code**  
> Lorsque le document indique que « Pure Data identifie » un attribut, cela signifie que Pure Data **lit une métadonnée préalablement attribuée au fragment** dans le tableau de référencement. Pure Data n’a pas à analyser lui-même le sens, la langue, le timbre, le lieu ou le rythme du contenu sonore.

> **Convention de nommage**  
> Le texte source emploie parfois `APPEL_POSSIBLE` et parfois `FAMILLES_CIBLES`, ainsi que `TYPE_ASSOCIATIONS` et `TYPE_ASSOCIATION`. Pour éviter deux noms différents dans le patch, ce document retient `FAMILLES_CIBLES` et `TYPE_ASSOCIATION`. Ces changements de nom ne modifient pas le fond : ils uniformisent uniquement les métadonnées destinées au code.

---

# 1. Fonction générale de la zone Hippocampe

## 1.1. Nature des fragments

L’Hippocampe contient des fragments :

- encore reconnaissables à l’écoute ;
- entendus individuellement les uns des autres ;
- suffisamment autonomes pour appeler plusieurs mémoires ;
- moins superposés et moins dissipés que les paroles de la zone Cortex.

Les fragments peuvent être des mots, des événements sonores identifiables, des phrases, des chants ou des souvenirs plus développés.

## 1.2. Principe associatif

« Appeler plusieurs mémoires » signifie qu’un fragment peut provoquer l’apparition de différents fragments associés et, inversement, être lui-même rappelé par d’autres fragments.

Ces relations :

- ne sont pas uniques ;
- ne sont pas systématiquement réciproques ;
- peuvent varier à chaque activation du système ;
- ne doivent pas produire une narration fixe ;
- ne doivent pas chercher à compléter grammaticalement une phrase.

Lorsqu’un fragment est diffusé, Pure Data lit ses attributs, constitue une liste de fragments compatibles, puis choisit une réponse possible. Selon sa force associative et les règles d’ouverture, le fragment peut également rester seul.

## 1.3. Principe d’aléatoire orienté

L’Hippocampe ne repose ni sur une correspondance fixe entre deux fragments ni sur un hasard entièrement libre.

Les métadonnées doivent permettre un **aléatoire orienté** :

- les rapprochements demeurent cohérents et perceptibles ;
- un même fragment peut appeler plusieurs mémoires différentes ;
- leur signification n’est jamais entièrement déterminée ;
- la multiplicité des connexions rend audible un fonctionnement rhizomatique et l’opacité de la mémoire.

## 1.4. Sensation recherchée

Un fragment doit pouvoir être entendu comme une mémoire identifiable, puis entrer dans une relation variable avec une autre mémoire. Le public peut percevoir une proximité, un contraste, une continuité ou un déplacement, sans que l’installation explique entièrement le lien.

---

# 2. Typologie et durée des fragments

## 2.1. Types de fragments

| Type fonctionnel | Contenu possible | Durée indicative du fichier |
|---|---|---|
| `ELEMENT_IDENTIFIABLE` | Mot ou événement très identifiable | `1–3 s` |
| `FRAGMENT_ASSOCIATIF_PRINCIPAL` | Fragment constituant un point d’association principal | `3–10 s` |
| `SOUVENIR_DEVELOPPE` | Phrase, chant ou souvenir développé | `8–20 s` |
| `EXCEPTION_LONGUE` | Fragment exceptionnel particulièrement chargé de sens | jusqu’à `30 s` |

Les plages de durée se recouvrent. Le type fonctionnel ne peut donc pas être déduit automatiquement de la durée : il doit être renseigné comme métadonnée si Alassane souhaite que Pure Data distingue ces quatre catégories.

## 2.2. Durée du fichier et durée de diffusion

La durée indique la longueur réelle du fichier audio découpé, mais pas nécessairement son temps de diffusion à chaque activation.

Par défaut :

- le fragment peut être joué intégralement.

Si le fragment possède un mode de lecture interruptible :

- Pure Data peut parfois le raccourcir ;
- le faire disparaître progressivement ;
- ou l’interrompre avant sa fin.

| Nom de l’attribut | Valeurs proposées à partir du texte |
|---|---|
| `MODE_LECTURE` | `INTEGRAL` / `INTERRUPTIBLE` |

> **Point à confirmer :** le texte distingue explicitement un mode `interruptible`, mais ne précise pas encore si `MODE_LECTURE` doit être une métadonnée indépendante ou une conséquence automatique de `OUVERTURE = TRES_OUVERT`.

## 2.3. Indépendance entre durée et association

La durée ne détermine pas la manière dont un fragment s’associe aux autres. Un fragment long peut rester seul ou appeler une autre mémoire ; un fragment très court peut également ouvrir plusieurs associations.

---

# 3. Architecture des attributs

Chaque fragment de l’Hippocampe reçoit plusieurs attributs. Un même fragment peut posséder plusieurs valeurs dans une même catégorie lorsque cela est indiqué.

Les cinq dimensions nécessaires dans le texte sont :

1. `FORCE_ASSOCIATIVE` : fréquence avec laquelle le fragment appelle une autre mémoire ;
2. `TYPE_ASSOCIATION` : nature du lien à privilégier ;
3. `FAMILLE_ASSOCIATIVE` : mémoires, thèmes ou catégories portés par le fragment lui-même ;
4. `FAMILLES_CIBLES` : mémoires ou thèmes que le fragment peut faire apparaître ;
5. `OUVERTURE` : sensation d’achèvement ou de suspension, influençant le délai et la forme de la réponse.

La `FAMILLE_ASSOCIATIVE` et les `FAMILLES_CIBLES` ne décrivent pas la même chose :

- `FAMILLE_ASSOCIATIVE` situe le fragment actuel ;
- `FAMILLES_CIBLES` définit les familles dans lesquelles Pure Data peut chercher un fragment associé.

---

# 4. Force associative

## 4.1. Définition

La force associative détermine avec quelle probabilité un fragment appelle une autre mémoire.

| Nom de l’attribut | Valeurs possibles | Conséquence générale |
|---|---|---|
| `FORCE_ASSOCIATIVE` | `1` / `2` / `3` | Plus la valeur est élevée, plus le fragment a de chances de provoquer une association. |

Exemples :

- si `H001_v3_hippocampe` possède `FORCE_ASSOCIATIVE = 3`, il a une forte probabilité d’appeler un autre fragment ;
- si `H002_v3_hippocampe` possède `FORCE_ASSOCIATIVE = 1`, il a davantage de chances de rester seul.

## 4.2. Fonction dans l’installation

La force associative permet de varier le degré d’activité relationnelle des mémoires : certaines restent parfois isolées, tandis que d’autres produisent plus fréquemment une association.

## 4.3. Fonction pour Pure Data

Pure Data utilise cette valeur pour déterminer la probabilité d’effectuer une recherche dans les `FAMILLES_CIBLES` après ou pendant la lecture du fragment.

### Règle H1 — Probabilité d’association

- `FORCE_ASSOCIATIVE = 1` : environ `25 %` de probabilité d’appeler ;
- `FORCE_ASSOCIATIVE = 2` : environ `55 %` ;
- `FORCE_ASSOCIATIVE = 3` : environ `80 %`.

Ces valeurs constituent une **base de test provisoire** à ajuster avec Alassane. Une force 3 ne rend jamais la réponse obligatoire : le silence et l’absence de réponse restent possibles.

> **Paramètre encore à fixer :** validation des pourcentages après les premiers tests et éventuelle influence de `OUVERTURE` sur cette probabilité.

---

# 5. Types d’association

## 5.1. Définition

Le type d’association définit la nature de la relation recherchée entre le fragment entendu et le fragment appelé.

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `TYPE_ASSOCIATION` | `SENS` / `TIMBRE` / `LIEU` / `LANGUE` / `CONTRASTE` / `RYTHME` |

`TYPE_ASSOCIATION` peut contenir une ou plusieurs valeurs.

Exemple :

```text
TYPE_ASSOCIATION = SENS + CONTRASTE
```

## 5.2. Fonctions et exemples

| Valeur | Fonction relationnelle | Exemple concret |
|---|---|---|
| `SENS` | Rapprocher des fragments selon une proximité thématique ou sémantique. | Une parole sur la frontière appelle une parole sur le déplacement ou la migration, par exemple un discours de Cheikh Anta Diop. |
| `TIMBRE` | Rapprocher des matières possédant une qualité sonore apparentée. | Une respiration appelle un souffle ou une ambiance de souffle. |
| `LIEU` | Mettre en relation des espaces ou contextes géographiques. | Un tram bruxellois appelle une circulation enregistrée à Kinshasa. |
| `LANGUE` | Rapprocher des voix par la langue. | Une phrase en lingala appelle une autre voix en lingala. |
| `CONTRASTE` | Faire apparaître une opposition perceptible entre deux fragments. | Une parole administrative froide appelle une berceuse familiale. |
| `RYTHME` | Rapprocher des fragments selon une pulsation ou une répétition. | Un rythme appelle un moteur ou un bruit répétitif enregistré en Europe. |

## 5.3. Fonction pour Pure Data

Le type d’association indique selon quelle logique choisir parmi les fragments candidats.

### Règle H2 — Plusieurs types d’association

Lorsqu’un fragment possède plusieurs valeurs de `TYPE_ASSOCIATION`, Pure Data peut sélectionner l’une des logiques disponibles à chaque activation.

Un même fragment `SENS + CONTRASTE` peut ainsi :

- appeler parfois une mémoire proche par le sens ;
- appeler parfois une mémoire produisant un contraste.

> **Donnée nécessaire pour le code :** `TYPE_ASSOCIATION` indique la logique recherchée, mais ne suffit pas à identifier automatiquement les candidats. Il faudra soit renseigner des métadonnées relationnelles complémentaires sur les fragments (`LANGUE`, `LIEU`, `TIMBRE`, `RYTHME`, etc.), soit préparer à l’avance les associations compatibles dans une table. Pure Data ne doit pas analyser seul le signal sonore ou le sens des paroles.

> **Paramètres encore à fixer :** poids respectif de chaque type lorsqu’un fragment en possède plusieurs, possibilité de sélectionner plusieurs types simultanément et règle exacte permettant de valider un contraste.

---

# 6. Famille associative

## 6.1. Définition

La famille associative décrit les mémoires, les thèmes ou les catégories auxquels appartient le fragment lui-même.

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `FAMILLE_ASSOCIATIVE` | Mots-clés multiples renseignés pour chaque fragment |

Un fragment peut appartenir à plusieurs familles.

Exemples de mots-clés présents dans le texte :

- `FRONTIERE` ;
- `ADMINISTRATION` ;
- `IDENTIFICATION` ;
- `DEPLACEMENT` ;
- `DESIR` ;
- `TERRITOIRE` ;
- `FAMILLE` ;
- `CHANT` ;
- `LANGUE` ;
- `TRANSMISSION` ;
- `BRUXELLES` ;
- `ENVIRONNEMENT_URBAIN`.

## 6.2. Exemples de classification

| Fragment | `FAMILLE_ASSOCIATIVE` |
|---|---|
| Parole du douanier | `FRONTIERE + ADMINISTRATION + IDENTIFICATION` |
| Cousine parlant d’un voyage | `DEPLACEMENT + DESIR + TERRITOIRE` |
| Berceuse en lingala | `FAMILLE + CHANT + LANGUE + TRANSMISSION` |
| Bruit de tram | `BRUXELLES + DEPLACEMENT + ENVIRONNEMENT_URBAIN` |

## 6.3. Fonction dans l’installation

La famille associative situe la mémoire portée par le fragment et permet de l’inscrire dans plusieurs réseaux de relations possibles.

## 6.4. Fonction pour Pure Data

Pure Data lit les mots-clés pour déterminer si le fragment peut entrer dans la liste des candidats recherchés par un autre fragment.

La famille associative ne détermine pas encore ce qui apparaîtra ensuite : elle décrit d’abord le fragment actuel.

---

# 7. Familles cibles et appels possibles

## 7.1. Définition

Les familles cibles indiquent les familles de fragments que le fragment actuel peut faire apparaître ensuite.

| Nom retenu dans ce document | Autre formulation présente dans le texte | Valeurs possibles |
|---|---|---|
| `FAMILLES_CIBLES` | `APPEL_POSSIBLE` | Mots-clés multiples renseignés pour chaque fragment |

Pour éviter deux noms différents dans le patch, il est préférable qu’Alassane utilise un seul nom de métadonnée. Dans ce document, le nom principal est `FAMILLES_CIBLES`.

## 7.2. Fonction dans l’installation

Les familles cibles ouvrent plusieurs directions relationnelles à partir d’un même fragment.

## 7.3. Fonction pour Pure Data

Pure Data compare les `FAMILLES_CIBLES` du fragment actif avec les valeurs de `FAMILLE_ASSOCIATIVE` des autres fragments.

### Règle H3 — Constitution de la liste des candidats

Un fragment peut devenir candidat si au moins une de ses valeurs `FAMILLE_ASSOCIATIVE` correspond à une valeur de `FAMILLES_CIBLES` du fragment actif.

Exemple :

```text
Fragment actif :
FAMILLES_CIBLES = DEPLACEMENT + FAMILLE

Fragment candidat :
FAMILLE_ASSOCIATIVE = DEPLACEMENT + DESIR + TERRITOIRE

Résultat :
Le fragment candidat peut être sélectionné grâce à la valeur commune DEPLACEMENT.
```

### Règle H4 — Relations non nécessairement réciproques

Si le fragment A peut appeler le fragment B, le fragment B ne doit pas nécessairement pouvoir rappeler le fragment A.

La relation dépend des `FAMILLES_CIBLES` propres à chaque fragment.

### Règle H5 — Multiplicité des réponses

Plusieurs fragments peuvent appartenir à une même famille cible. Pure Data choisit alors une réponse parmi les candidats compatibles, afin qu’un même fragment ne déclenche pas toujours la même mémoire.

> **Paramètres encore à fixer :** méthode de départage entre plusieurs candidats, prévention d’une répétition immédiate du même fragment et éventuelle augmentation de la probabilité lorsqu’un candidat correspond à plusieurs familles cibles.

---

# 8. Ouverture

## 8.1. Définition

L’ouverture décrit la sensation d’achèvement ou de suspension laissée par le fragment. Elle ne correspond pas simplement à sa durée.

Elle influence :

- le moment où une réponse peut apparaître ;
- la durée du silence ;
- la possibilité de laisser le fragment seul ;
- la manière de terminer ou d’interrompre sa lecture ;
- la position spatiale du fragment associé.

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `OUVERTURE` | `FERME` / `PARTIELLEMENT_SUSPENDU` / `TRES_OUVERT` |

---

## 8.2. Ouverture fermée

### Fonction sensible

Le fragment donne la sensation d’une unité complète. Il peut exister seul. Un fragment suivant n’est pas perçu comme la continuation de la phrase, mais comme une nouvelle mémoire.

Exemple : une berceuse entendue jusqu’à la fin de sa phrase mélodique.

### Règle H6 — Lecture d’un fragment fermé

Pure Data doit :

1. lire le fragment jusqu’au bout depuis une enceinte ;
2. appliquer une sortie douce de `0,5 à 1,5 s` ;
3. laisser un silence de `3 à 6 s` ;
4. décider ensuite, selon la force associative, si un autre fragment apparaît.

Une association reste possible, mais elle ne doit pas donner l’impression d’un enchaînement direct ou d’une phrase poursuivie.

| Paramètre | Valeur |
|---|---|
| Fin de lecture | intégrale |
| Sortie | fondu de `0,5–1,5 s` |
| Silence | `3–6 s` |
| Spatialisation de la réponse | non précisée |

---

## 8.3. Ouverture partiellement suspendue

### Fonction sensible

Le fragment est compréhensible, mais semble attendre quelque chose. Une autre mémoire peut surgir sans compléter grammaticalement la phrase.

Exemple : la parole d’un douanier, compréhensible mais interrompue de manière à laisser un espace d’attente.

### Règle H7 — Lecture d’un fragment partiellement suspendu

Pure Data doit :

1. diffuser le fragment depuis une enceinte située devant le public ;
2. conserver la coupure telle qu’elle existe dans le fichier ;
3. laisser un silence de `2 à 5 s` ;
4. faire apparaître un fragment associé depuis une enceinte latérale ou arrière.

| Paramètre | Valeur |
|---|---|
| Fin de lecture | coupure originale conservée |
| Silence | `2–5 s` |
| Position du fragment actif | enceinte avant |
| Position de la réponse | enceinte latérale ou arrière |

### Sensation à l’écoute

La parole institutionnelle laisse un espace dans lequel une autre présence peut apparaître, sans produire une continuité grammaticale explicite.

---

## 8.4. Ouverture très ouverte

### Fonction sensible

Le fragment perd sa destination ou sa résolution. L’attente et l’absence deviennent audibles, tandis que son mouvement continue sous une autre forme sonore.

Exemple : une parole de la cousine Keren à Kinshasa, interrompue pendant sa diffusion ou coupée nettement à sa fin.

### Règle H8 — Lecture d’un fragment très ouvert

Pure Data doit pouvoir :

1. diffuser le fragment depuis une enceinte ;
2. soit l’interrompre nettement entre son début et sa fin, soit conserver une coupure nette à la fin ;
3. laisser un silence bref de `1 à 2 s` ;
4. faire démarrer un fragment associé depuis une autre enceinte ;
5. déplacer ensuite ce fragment associé dans l’espace sonore.

| Paramètre | Valeur |
|---|---|
| Fin de lecture | coupure nette pendant la lecture ou à la fin |
| Silence | `1–2 s` |
| Position de la réponse | autre enceinte |
| Comportement spatial de la réponse | déplacement dans l’espace |

### Sensation à l’écoute

La phrase perd sa destination, mais son mouvement continue sous une autre forme sonore. Le trajet verbal devient un trajet acoustique : la déterritorialisation devient perceptible.

> **Paramètres encore à fixer :** probabilité d’une interruption avant la fin, plage temporelle autorisée pour l’interruption, choix de l’enceinte de réponse, vitesse, durée et trajectoire du déplacement.

---

# 9. Règles générales d’association

### Règle H9 — Un fragment peut rester seul

Pure Data ne doit pas produire automatiquement une réponse après chaque fragment. La possibilité de rester seul dépend au minimum de `FORCE_ASSOCIATIVE` et de `OUVERTURE`.

### Règle H10 — Pas de continuation grammaticale obligatoire

Lorsqu’un fragment suspendu appelle une réponse, Pure Data ne cherche pas à compléter sa phrase. Le fragment suivant doit constituer une autre mémoire mise en relation avec la première.

### Règle H11 — Variation des réponses

Un même fragment ne doit pas toujours appeler le même candidat. Pure Data doit varier les réponses compatibles disponibles dans ses familles cibles.

### Règle H12 — Reconnaissance individuelle

Les fragments de l’Hippocampe doivent rester perceptibles et reconnaissables individuellement. Leur traitement, leur superposition éventuelle et leur niveau de présence ne doivent pas les dissoudre comme les paroles du Cortex.

### Règle H13 — Association selon les métadonnées

Pure Data ne déduit pas seul les relations de sens, de langue, de lieu, de timbre, de contraste ou de rythme. Il sélectionne parmi les relations décrites par les métadonnées ou par une table de compatibilité préalablement renseignée.

## 9.1. Architecture des comportements

Les attributs décrivent ce que porte chaque fragment et les relations qu’il peut créer. Les comportements traduisent ensuite ces informations en événements audibles et spatiaux.

| Comportement | Fonction |
|---|---|
| `APPELER` | Le fragment source déclenche la recherche d’une association. |
| `RELIER` | Pure Data articule temporellement, spatialement et sonorement les deux fragments sélectionnés. |
| `REPONDRE` | Le fragment choisi comme réponse entre dans l’espace sonore. |
| `REVENIR` | Un fragment réellement entendu est réactivé ultérieurement. |
| `SE_DEPLACER` | Un fragment circule entre les enceintes. |
| `DISPARAITRE` | Le fragment quitte l’espace sonore selon un mode déterminé. |

Une association complète peut suivre cette séquence :

```text
APPELER → RELIER → REPONDRE → SE_DEPLACER → DISPARAITRE → REVENIR
```

Tous les comportements ne doivent pas être activés à chaque fois. Un fragment peut être diffusé, rester seul, puis disparaître sans appeler de réponse.

### Règle H14 — Séquence générale d’exécution

Lorsqu’un fragment est sélectionné, Pure Data doit :

1. le diffuser selon son `MODE_LECTURE` ;
2. consulter sa `FORCE_ASSOCIATIVE` ;
3. décider si `APPELER` est activé ;
4. si l’appel est activé, lire ses `FAMILLES_CIBLES` ;
5. chercher les fragments dont la `FAMILLE_ASSOCIATIVE` correspond ;
6. sélectionner un `TYPE_ASSOCIATION` autorisé ;
7. choisir un candidat compatible ;
8. consulter l’`OUVERTURE` et le `DELAI_REPONSE` du fragment source ;
9. choisir une variante de `RELIER` ;
10. faire `REPONDRE` le fragment sélectionné ;
11. activer éventuellement `SE_DEPLACER`, `DISPARAITRE` et `REVENIR`.

Si aucun candidat compatible n’est trouvé, Pure Data ne sélectionne pas un fragment complètement aléatoire : le fragment source reste seul.

---

## 9.2. Comportement `APPELER`

`APPELER` signifie qu’un fragment source provoque la recherche et l’apparition possible d’un autre fragment associé. Il dépend principalement de `FORCE_ASSOCIATIVE`, `FAMILLES_CIBLES`, `TYPE_ASSOCIATION`, `OUVERTURE` et `DELAI_REPONSE`.

### Règle H15 — Appel direct

1. Pure Data joue le fragment source.
2. Il attend le délai prévu.
3. Il diffuse un seul fragment associé.

**Sensation :** une mémoire semble en réveiller une autre, sans produire une narration entièrement explicite.

### Règle H16 — Appel superposé

1. Pure Data joue le fragment source.
2. Il déclenche la réponse entre `0,5 et 3 s` avant sa fin.
3. Il réalise un léger croisement de volumes.
4. Le second fragment continue ensuite seul.

Cette variante est surtout autorisée entre :

- une voix et une ambiance ;
- une voix et un souffle ;
- un chant et une texture ;
- deux matières peu denses.

Elle doit être évitée entre deux paroles longues et denses.

**Sensation :** la nouvelle mémoire semble émerger de l’intérieur de la première.

### Règle H17 — Appel différé

Pure Data conserve temporairement le fragment appelé et le diffuse entre `10 et 60 s` plus tard, éventuellement après d’autres événements.

**Sensation :** le lien devient une réminiscence moins évidente intellectuellement, mais encore perceptible.

### Règle H18 — Appel divergent

Un même fragment peut appeler deux réponses différentes, espacées dans le temps :

1. Pure Data sélectionne un premier candidat et le diffuse après le délai prévu ;
2. il conserve un second candidat ;
3. il le diffuse plusieurs secondes plus tard ou le transforme en retour différé.

Il ne faut généralement pas diffuser simultanément plus de deux fragments issus du même appel.

**Sensation :** une mémoire ouvre plusieurs directions plutôt qu’une filiation unique.

### Règle H19 — Appel sans réponse

Même lorsqu’un appel est autorisé, Pure Data peut décider qu’aucune réponse n’apparaît.

**Sensation :** la possibilité reste inaboutie et le silence devient une forme de mémoire absente.

---

## 9.3. Comportement `RELIER`

`RELIER` ne sélectionne pas le fragment suivant. Il organise la relation temporelle, sonore et spatiale entre deux fragments déjà choisis.

### Règle H20 — Relier par succession

Le premier fragment se termine, un silence apparaît, puis le second commence.

À privilégier pour :

- deux paroles ;
- une association de `SENS` ;
- une association de `LANGUE` ;
- les fragments dont le contenu doit rester compréhensible.

### Règle H21 — Relier par superposition partielle

La fin du premier fragment et le début du second se chevauchent pendant `0,5 à 3 s`.

À privilégier pour :

- une association de `TIMBRE` ;
- une association de `RYTHME` ;
- une voix reliée à une ambiance ;
- un chant relié à une texture.

### Règle H22 — Relier par relais spatial

Le premier fragment est diffusé depuis une enceinte et le second commence depuis une autre, avec ou sans superposition.

Pure Data peut sélectionner :

- une enceinte voisine ;
- une enceinte opposée ;
- une enceinte située derrière le public ;
- une distance variable selon le contraste recherché.

### Règle H23 — Relier par contraste

Une rupture nette ou un silence clair sépare les fragments. Le second peut apparaître depuis une enceinte éloignée ou opposée et avec une densité différente.

**Sensation :** les fragments demeurent irréductibles l’un à l’autre, mais leur proximité fait apparaître une tension commune.

### Règle H24 — Mode de liaison selon le type d’association

| `TYPE_ASSOCIATION` | Modes à privilégier |
|---|---|
| `SENS` | Succession et préservation de l’intelligibilité |
| `TIMBRE` | Superposition progressive |
| `LIEU` | Relais ou déplacement spatial |
| `LANGUE` | Succession ou appel-réponse |
| `RYTHME` | Chevauchement ou continuité pulsée |
| `CONTRASTE` | Rupture, opposition spatiale ou changement net de densité |

---

## 9.4. Comportement `REPONDRE`

`REPONDRE` décrit la manière dont le fragment sélectionné comme réponse entre dans l’espace sonore. `APPELER` appartient au premier fragment ; `REPONDRE` appartient au fragment qui apparaît ensuite.

### Règle H25 — Réponse immédiate

Le fragment répond entre `0,5 et 3 s` après le premier. Cette variante ne doit pas créer de fausse continuité grammaticale entre deux paroles.

### Règle H26 — Réponse retardée

Le fragment apparaît entre `3 et 15 s` après le premier, afin que le public conserve la première mémoire avant d’en entendre une autre.

### Règle H27 — Réponse spatiale

Le fragment répond depuis une enceinte différente : latérale, opposée, arrière ou éloignée du fragment source.

### Règle H28 — Réponse indirecte

Une parole ne reçoit pas nécessairement une autre parole. Elle peut recevoir un chant, une ambiance, une respiration, un bruit de transport, une texture ou une archive.

### Règle H29 — Réponse fragile

Le fragment apparaît à un niveau plus faible, pendant une durée limitée, ou disparaît avant d’être totalement identifiable. Il doit néanmoins conserver le degré minimal de reconnaissabilité propre à l’Hippocampe.

---

## 9.5. Comportement `REVENIR`

`REVENIR` signifie qu’un fragment réellement diffusé auparavant est conservé dans l’historique de Pure Data et peut être réactivé plus tard. Le retour ne doit pas être choisi indistinctement dans toute la banque sonore.

### Règle H30 — Retour intact

Le même fichier revient intégralement après une latence longue, depuis une autre enceinte.

### Règle H31 — Retour atténué

Le fragment revient avec une ou plusieurs modifications légères :

- volume plus faible ;
- entrée plus lente ;
- légère réduction des fréquences aiguës ;
- sensation de distance.

### Règle H32 — Retour partiel

Si `MODE_LECTURE = INTERRUPTIBLE`, Pure Data peut rejouer une partie encore reconnaissable du fragment, par exemple le début d’une phrase ou sa dernière expression.

### Règle H33 — Retour associatif

Un fragment déjà entendu peut revenir lorsqu’une de ses familles associatives est réactivée par un autre son.

Base de test proposée :

| Paramètre | Base provisoire |
|---|---|
| Latence minimale | `30 s` |
| Latence maximale | plusieurs minutes |
| Nombre maximal de retours | `1 à 3` |
| Retours immédiatement successifs | interdits |

Restent à définir : la probabilité de retour, la durée minimale entre deux retours, le mode de retour autorisé et le changement d’enceinte.

---

## 9.6. Comportement `SE_DEPLACER`

`SE_DEPLACER` organise la circulation d’un fragment entre les huit enceintes. Le mouvement doit rendre la relation perceptible et ne pas devenir un effet spectaculaire systématique.

### Règle H34 — Déplacement d’un point à un autre

Le fragment commence dans une enceinte et termine dans une autre grâce à un croisement progressif des volumes.

### Règle H35 — Relais discontinu

Un fragment ou plusieurs fragments associés apparaissent successivement dans différentes enceintes, sans mouvement continu.

### Règle H36 — Déplacement lent

Un fragment long, comme un chant ou une ambiance, circule progressivement entre `2 et 4` enceintes pendant sa diffusion.

### Règle H37 — Déplacement brusque

Un fragment court disparaît d’une enceinte et réapparaît immédiatement dans une enceinte éloignée. Cette variante doit rester ponctuelle.

Les voix longues doivent généralement se déplacer lentement ou rester stables. Les fragments très courts peuvent supporter des déplacements plus brusques.

Paramètres à définir : enceintes de départ et d’arrivée, nombre d’enceintes traversées, déplacement continu ou discontinu, durée, vitesse, direction, passage éventuel par le centre et variation du volume.

---

## 9.7. Comportement `DISPARAITRE`

`DISPARAITRE` détermine comment un fragment quitte l’espace sonore. La disparition peut confirmer sa complétude, maintenir sa suspension ou empêcher sa reconnaissance totale.

### Règle H38 — Disparition naturelle

Pure Data joue le fragment jusqu’au bout puis applique un fondu de `0,5 à 2 s`. À privilégier pour les fragments `FERME`, les chants et les voix à préserver.

### Règle H39 — Disparition progressive

Le volume diminue pendant `2 à 6 s`. Une légère perte des fréquences aiguës peut accompagner cette baisse.

### Règle H40 — Disparition nette

Pure Data interrompt le fragment par une coupure très courte. Cette variante est réservée aux fragments `INTERRUPTIBLE`, `TRES_OUVERT` ou aux ruptures dramaturgiques explicitement autorisées.

### Règle H41 — Disparition par recouvrement

Un second fragment masque progressivement le premier : le niveau du premier diminue pendant que celui du second augmente.

### Règle H42 — Disparition spatiale

Le fragment se déplace vers une enceinte éloignée tandis que son niveau baisse et que certaines fréquences disparaissent.

### Garde-fous

- le fragment doit être entendu suffisamment longtemps pour rester reconnaissable avant une coupure nette ;
- les fragments `FERME` doivent généralement être joués intégralement ;
- les berceuses, témoignages sensibles et voix familiales ne doivent pas être systématiquement interrompus ;
- la disparition ne doit pas devenir mécanique ;
- les transformations profondes restent réservées à la Reconstruction.

---

## 9.8. Combinaisons autorisées

| Combinaison | Fonction |
|---|---|
| `APPELER → REPONDRE → DISPARAITRE` | Une mémoire répond puis disparaît naturellement. |
| `APPELER → RELIER → REPONDRE → SE_DEPLACER` | Une ambiance associée apparaît ailleurs puis circule. |
| `APPELER → REPONDRE → DISPARAITRE → REVENIR` | La réponse revient plus tard sous une forme éventuellement atténuée. |
| `APPELER → ABSENCE_REPONSE → REVENIR` | La mémoire attendue n’apparaît que beaucoup plus tard. |

### Règle H43 — Limitation des comportements simultanés

Pure Data doit éviter d’activer toutes les possibilités lors d’une même association. Une séquence simple doit rester possible.

## 9.9. Limites dramaturgiques générales

### Règle H44 — Limitation de la chaîne associative

Une chaîne doit généralement être limitée à `2 ou 3 fragments`.

### Règle H45 — Limitation de la superposition

L’Hippocampe doit généralement être limité à `2 fragments simultanés`. Il faut éviter la superposition de deux paroles longues et denses.

### Règle H46 — Préservation des silences et des sources

Pure Data doit :

- conserver de véritables silences ;
- varier les délais ;
- empêcher la répétition immédiate d’un même couple ;
- varier les familles qui répondent ;
- préserver la reconnaissabilité des sources ;
- réserver les recompositions syllabiques, la granularisation et les changements profonds à la Reconstruction.

Le rhizome ne vient pas d’une accumulation illimitée, mais du fait qu’un même fragment possède plusieurs directions possibles sans qu’aucune ne devienne définitive.

---

# 10. Exemple complet — Parole du douanier

## 10.1. Fragment de départ

> « Est-ce que la personne que j’ai en face de moi… »

| Attribut | Valeur |
|---|---|
| `FAMILLE_ASSOCIATIVE` | `FRONTIERE + ADMINISTRATION + IDENTIFICATION` |
| `FAMILLES_CIBLES` | `DEPLACEMENT + FAMILLE` |
| `TYPE_ASSOCIATION` | `SENS + CONTRASTE` |
| `OUVERTURE` | `PARTIELLEMENT_SUSPENDU` |
| `FORCE_ASSOCIATIVE` | `3` |
| `DELAI_REPONSE` | `2–5 s` |

## 10.2. Déroulement possible

1. Pure Data joue la parole depuis une enceinte située devant le public.
2. La phrase se termine en suspension.
3. `FORCE_ASSOCIATIVE = 3` donne une forte probabilité d’activer `APPELER`.
4. Pure Data choisit `FAMILLE` dans `FAMILLES_CIBLES`.
5. Il sélectionne `CONTRASTE` comme type d’association.
6. Il recherche un fragment dont `FAMILLE_ASSOCIATIVE` contient `FAMILLE`.
7. Il sélectionne la berceuse en lingala.
8. Après `3 s` de silence, la berceuse `REPOND` depuis une enceinte arrière.
9. Elle apparaît progressivement pendant environ `2 s`.
10. Elle reste reconnaissable et se déploie sans superposition avec la parole du douanier.
11. Elle `DISPARAIT` naturellement.
12. Pure Data conserve les deux fragments dans son historique.
13. Plusieurs minutes plus tard, une partie reconnaissable de la berceuse peut `REVENIR` depuis une autre enceinte.

## 10.3. Sensation recherchée

Une parole institutionnelle liée au contrôle et à l’identification ouvre sur une mémoire familiale chantée. Leur relation est perceptible, mais elle n’est ni expliquée ni stabilisée. Le système produit une forme provisoire d’identité-relation, tout en maintenant l’opacité propre à chacun des fragments.

> **Paramètre encore à fixer :** le niveau d’entrée de la berceuse doit être traduit en valeur de gain ou en catégorie de présence.

---

# 11. Zone Hippocampe–Ambiance

## 11.1. Fonction générale

Hippocampe–Ambiance accompagne les **relations** entre les fragments de l’Hippocampe. Cette zone ne forme pas un fond sonore continu : elle fait apparaître les milieux sensoriels, affectifs, musicaux ou territoriaux qu’un fragment peut réveiller par association.

Une parole peut faire apparaître :

- une berceuse ;
- un motif de likembe ;
- une chanson fredonnée ;
- une circulation urbaine ;
- un souffle ;
- une vibration mécanique ;
- une résonance intérieure ;
- une ambiance nocturne.

Inversement, une ambiance peut rappeler une parole, un chant ou une autre ambiance.

### Règle HA1 — Apparition intermittente

Une ambiance ne doit pas accompagner systématiquement chaque parole. Elle apparaît ponctuellement lorsqu’une voix, un mot, un timbre, un rythme, une langue ou un lieu l’appelle.

Elle peut :

1. émerger ;
2. établir une relation avec un fragment ;
3. demeurer un certain temps ;
4. se déplacer éventuellement ;
5. disparaître ;
6. ou revenir plus tard.

## 11.2. Catégories d’ambiances

| Valeur de `TYPE_AMBIANCE` | Contenus possibles | Fonction dominante |
|---|---|---|
| `MUSICALE` | Mélodie, chant, berceuse, fredonnement, motif rythmique, musique radiophonique, voix accompagnée de likembe | Milieu affectif, mélodique, rythmique ou mémoriel |
| `TEXTURE` | Souffle, vent, moteur, tram, circulation, foule, résonance, bruit d’archive, texture domestique ou urbaine | Milieu matériel, environnemental, territorial ou corporel |

Ces deux catégories utilisent les mêmes attributs associatifs, mais ne se comportent pas de la même manière à l’écoute.

---

## 11.3. Durée des ambiances

La durée inscrite dans le tableau correspond à la durée réelle du fichier. Pure Data peut ne diffuser qu’une partie du fichier si son `MODE_LECTURE` l’autorise.

### A. Ambiances musicales

| Type fonctionnel | Durée conseillée | Fonction perceptible |
|---|---|---|
| `MOTIF_MUSICAL_BREF` | `4–10 s` | Ponctuation ou souvenir mélodique/rythmique immédiatement reconnaissable |
| `PHRASE_MUSICALE` | `10–25 s` | Relation identifiable avec une parole, une personne ou une situation |
| `MILIEU_MUSICAL_DEVELOPPE` | `25–45 s` | Installation temporaire d’un espace affectif ou mémoriel |
| `EXCEPTION_MUSICALE_LONGUE` | `45–60 s` | Berceuse, chant familial ou rituel dont le développement doit être respecté |

Les chants familiaux, rituels ou particulièrement sensibles doivent, par défaut, être joués intégralement ou pendant une durée minimale suffisante pour ne pas devenir de simples échantillons décoratifs.

### B. Ambiances-textures

| Type fonctionnel | Durée conseillée | Fonction perceptible |
|---|---|---|
| `EVENEMENT_SONORE` | `2–8 s` | Souffle, passage, choc, démarrage ou geste identifiable |
| `TEXTURE_ASSOCIATIVE` | `8–20 s` | Évocation d’un lieu, d’une matière ou d’un état |
| `MILIEU_EVOLUTIF` | `20–45 s` | Présence spatiale accompagnant ou reliant plusieurs fragments |
| `EXCEPTION_TEXTURE_LONGUE` | `45–90 s` | Field recording possédant une véritable évolution interne |

Une texture longue ne doit être conservée que si elle évolue réellement. Une texture stable de `60 s` risquerait de devenir un fond sonore immobile.

### Règle HA2 — Paramètres temporels

| Métadonnée | Fonction |
|---|---|
| `DUREE_FICHIER_S` | Durée totale réelle |
| `DUREE_MIN_LECTURE_S` | Durée minimale avant interruption possible |
| `MODE_LECTURE` | `INTEGRAL` / `EXTRAIT_VARIABLE` / `INTERRUPTIBLE` |
| `DELAI_REPONSE` | Délai avant l’apparition d’un fragment associé |
| `SILENCE_APRES` | Respiration après la disparition |

Entre deux activations, un silence variable de `3 à 15 s` peut être prévu afin d’empêcher l’ambiance de devenir un accompagnement permanent.

---

## 11.4. Répartition spatiale sur huit enceintes

La spatialisation doit rendre perceptible une relation entre les fragments et non produire une circulation spectaculaire permanente.

| `MODE_SPATIAL` | Fonction |
|---|---|
| `LOCALISE` | Une seule enceinte : souvenir situé, intime ou précis |
| `DUO_DISSYMETRIQUE` | Deux enceintes à des niveaux différents : présence principale et résonance secondaire |
| `RELAIS` | Passage successif entre `2 et 4` enceintes |
| `HALO` | Présence diffuse sur `3 ou 4` enceintes autour d’une parole localisée |
| `TRAJET_LENT` | Déplacement progressif par fondu entre `2 et 4` enceintes |
| `OPPOSITION` | Deux fragments sur des enceintes éloignées ou opposées |

### Règle HA3 — Spatialisation d’une ambiance musicale

Une ambiance musicale doit généralement rester identifiable et située :

- une enceinte pour une présence intime ;
- deux enceintes asymétriques pour une mémoire qui se dédouble ;
- deux ou trois enceintes successives pour un retour ou une transmission ;
- jamais les huit enceintes simultanément par défaut.

Une berceuse peut apparaître sur une enceinte proche, disparaître, puis revenir plus faiblement sur une enceinte éloignée. Elle change alors de position mémorielle sans devenir une chanson tournant autour du public.

### Règle HA4 — Spatialisation d’une ambiance-texture

Une texture peut occuper un espace plus large :

- deux enceintes pour établir un passage ;
- trois ou quatre enceintes pour produire un halo ;
- plusieurs enceintes successives pour suggérer un déplacement territorial ;
- une seule enceinte si l’événement doit rester localisable.

La même texture ne doit pas être diffusée au même niveau sur les huit enceintes.

### Règle HA5 — Limitation de la superposition

Par défaut, Pure Data limite la diffusion à :

- une parole principale ;
- une ambiance principale ;
- éventuellement une seconde présence très faible.

Si une ambiance musicale et une texture sont présentes ensemble, l’une doit rester clairement à l’arrière-plan. Comme base de test, l’ambiance secondaire peut être placée environ `8 à 14 dB` sous le fragment principal.

---

## 11.5. Attributs des ambiances musicales

### A. Force associative

| Valeur | Fonction sensible | Exemple |
|---|---|---|
| `1` — présence protégée | L’ambiance apparaît principalement pour elle-même et peut s’éteindre sans appel. | Une berceuse familiale jouée presque intégralement sans interruption administrative. |
| `2` — passage possible | Elle peut rester seule ou appeler un fragment. | Une chanson fredonnée appelle parfois une voix familiale, un souffle ou une ambiance domestique. |
| `3` — nœud associatif | Elle ouvre fréquemment une nouvelle branche. | Un motif de likembe appelle un moteur, des pas, une voix collective ou un récit de déplacement. |

Base de test propre aux ambiances : `25 %`, `50 %` et `75 %` pour les forces 1, 2 et 3.

> **Point à confirmer :** cette base diffère légèrement de celle proposée pour les fragments de l’Hippocampe (`25 %`, `55 %`, `80 %`). Il faut décider si les deux échelles restent distinctes ou deviennent communes.

### B. Famille associative

Une ambiance musicale peut recevoir trois ou quatre familles dans un vocabulaire contrôlé.

| Ambiance musicale | `FAMILLE_ASSOCIATIVE` possible |
|---|---|
| Berceuse en lingala | `FAMILLE + ENFANCE + LANGUE + TRANSMISSION + APAISEMENT` |
| Chanson populaire fredonnée par la cousine | `FAMILLE + INTIMITE + CULTURE_POPULAIRE + REAPPROPRIATION` |
| Chant avec likembe | `CHANT + COMMUNAUTE + TRANSMISSION + RYTHME + TERRITOIRE` |
| Chant exprimant une libération | `CORPS + LIBERATION + MOUVEMENT + COMMUNAUTE` |

### C. Types d’association

| `TYPE_ASSOCIATION` | Exemple |
|---|---|
| `SENS` | Une parole et un chant partagent l’enfance, le départ ou la frontière. |
| `TIMBRE` | Un fredonnement appelle un souffle ; le métal du likembe appelle un bruit mécanique. |
| `LIEU` | Une musique associée à Kinshasa appelle un espace bruxellois, ou inversement. |
| `LANGUE` | Une berceuse en lingala appelle une voix parlée en lingala. |
| `RYTHME` | Un motif de likembe appelle des pas, un moteur ou une machine. |
| `CONTRASTE` | Une berceuse paisible rencontre une parole administrative ou une rupture sonore. |

### Règle HA6 — Limite du contraste

Pure Data ne doit pas confronter automatiquement tout chant congolais à une archive coloniale ou à un son de violence. Les contrastes autorisés doivent être définis dans le tableau afin d’éviter une lecture répétitive et réductrice.

### D. Familles cibles

Exemples :

- berceuse → `FAMILLE + ENFANCE + NUIT + SOUFFLE + VOIX_LINGALA` ;
- motif de likembe → `CORPS + MOUVEMENT + MACHINE + COMMUNAUTE + DEPLACEMENT` ;
- chanson fredonnée → `FAMILLE + DESIR + CULTURE_POPULAIRE + INTIMITE`.

Une ambiance ne doit pas appeler toutes les familles auxquelles elle appartient. `FAMILLE_ASSOCIATIVE` décrit ce qu’elle porte ; `FAMILLES_CIBLES` indique vers quoi elle peut conduire.

### E. Ouverture musicale

| `OUVERTURE` | Règles de lecture et de réponse | Sensation |
|---|---|---|
| `FERME` | Lecture intégrale privilégiée ; fondu `1–3 s` ; silence possible `4–12 s` ; absence de réponse autorisée | Le souvenir paraît momentanément complet. |
| `PARTIELLEMENT_SUSPENDU` | Partie significative préservée ; réponse après `1,5–6 s` ; léger chevauchement possible ; réponse sur une autre enceinte | Une mémoire en appelle doucement une autre. |
| `TRES_OUVERT` | Interruption après la durée minimale ; coupure ou fondu très court ; réponse après `0,5–3 s` ou silence marqué `6–15 s` | La mémoire reste ouverte sans être complétée automatiquement. |

---

## 11.6. Traitements des ambiances musicales

Dans l’Hippocampe, la musique doit rester reconnaissable. La transformation profonde appartient à la Reconstruction.

### Traitements permis

- légère modification du niveau ;
- filtrage modéré créant proximité ou éloignement ;
- réverbération légère ;
- fondu de `1 à 4 s` ;
- répétition d’un motif `1 à 3 fois` avec intervalles irréguliers ;
- retour du fragment sur une autre enceinte ;
- ralentissement ou accélération légère, autour de `10 à 15 %` maximum ;
- modification éventuelle de hauteur d’environ un demi-ton à un ton si le matériau le permet.

### Traitements à éviter

- granularisation profonde ;
- inversion systématique ;
- fortes modifications de hauteur ;
- boucles parfaitement régulières ;
- superposition de deux longues chansons ;
- delays abondants rendant les paroles incompréhensibles.

Les chants familiaux ou rituels peuvent recevoir :

```text
TRAITEMENT_MAX = LEGER
MODE_LECTURE = INTEGRAL
RECONNAISSABILITE_MIN = 3
```

---

## 11.7. Attributs des ambiances-textures

Les textures suivent la même logique associative, mais leurs attributs sont perçus à travers leur matière, leur évolution et leur espace plutôt qu’à travers une phrase musicale.

### A. Force associative

| Valeur | Fonction |
|---|---|
| `1` | La texture accompagne ou demeure seule sans provoquer systématiquement une suite. |
| `2` | Elle peut former un passage vers un autre fragment. |
| `3` | Elle constitue un signal territorial, rythmique ou timbral fort déclenchant fréquemment une association. |

Exemple : une respiration légère peut recevoir une force 1, tandis qu’un tram identifiable peut recevoir une force 3 et appeler un récit de déplacement ou une circulation enregistrée à Kinshasa.

### B. Famille associative

| Texture | `FAMILLE_ASSOCIATIVE` possible |
|---|---|
| Souffle | `CORPS + INTIMITE + VOIX + FRAGILITE` |
| Tram bruxellois | `BRUXELLES + DEPLACEMENT + VILLE + METAL` |
| Circulation de Kinshasa | `KINSHASA + DEPLACEMENT + FOULE + MOTEUR` |
| Ambiance nocturne | `NUIT + FAMILLE + DISTANCE + INTERIEUR_EXTERIEUR` |
| Bruit d’archive | `ARCHIVE + MEDIUM + DISTANCE + EFFACEMENT` |
| Son de guerre | `CONFLIT + RUPTURE + VIOLENCE + TERRITOIRE` |

### C. Types d’association à privilégier

| `TYPE_ASSOCIATION` | Exemple |
|---|---|
| `TIMBRE` | Souffle vers vent ; métal du tram vers likembe |
| `LIEU` | Circulation de Bruxelles vers Kinshasa |
| `RYTHME` | Moteur vers motif musical ou pas |
| `CONTRASTE` | Espace calme vers rupture mécanique |
| `SENS` | Frontière sonore vers parole sur le contrôle |
| `LANGUE` | Seulement si la texture contient une présence vocale identifiable |

### D. Familles cibles

Exemples :

- souffle → `VOIX + FAMILLE + VENT + FRAGILITE` ;
- tram → `DEPLACEMENT + FRONTIERE + KINSHASA + TERRITOIRE` ;
- moteur → `RYTHME + LIKEMBE + MOUVEMENT + VILLE` ;
- bruit d’archive → `ARCHIVE + VOIX + DISTANCE + EFFACEMENT`.

### E. Ouverture des textures

Pour une texture, l’ouverture dépend de l’évolution du geste sonore et non d’une phrase grammaticale.

| `OUVERTURE` | Description | Règle Pure Data |
|---|---|---|
| `FERME` | L’événement possède une fin identifiable : tram qui passe, porte qui se ferme, expiration qui finit. | Préserver la fin naturelle puis laisser `3–10 s` de délai. |
| `PARTIELLEMENT_SUSPENDU` | La texture pourrait continuer mais peut être remplacée. | Fondu croisé de `2–6 s` avec un fragment associé. |
| `TRES_OUVERT` | La texture est interrompue pendant une montée, un cycle ou un mouvement. | Disparition rapide, puis réponse après `0–2 s` ou silence beaucoup plus long. |

---

## 11.8. Traitements des ambiances-textures

Les textures peuvent être davantage transformées que les musiques, mais leur origine doit rester perceptible dans l’Hippocampe.

### Traitements permis

- filtrage progressif ;
- renforcement ou retrait de certaines fréquences ;
- modification lente du niveau ;
- fondu spatial entre plusieurs enceintes ;
- étirement léger, entre environ `0,8 et 1,2 fois` la durée ;
- isolation d’une zone fréquentielle ;
- rapprochement ou éloignement progressif ;
- disparition derrière une parole ;
- réintroduction ultérieure plus faible ou filtrée.

### Règle HA7 — Préservation des field recordings

Les field recordings doivent rester majoritairement secs. Le delay ne doit pas être systématique ; il peut être réservé à certains souffles, résonances ou résidus mécaniques lorsqu’il sert précisément la relation.

### Règle HA8 — Diminution sous une parole

Pour préserver l’intelligibilité d’une parole, Pure Data peut diminuer automatiquement l’ambiance de `4 à 10 dB` pendant sa diffusion.

---

## 11.9. Comportements des ambiances

### Règle HA9 — `APPELER`

Une ambiance provoque l’apparition possible d’un fragment compatible selon sa force, ses familles, ses types d’association et ses familles cibles.

- `MUSICALE` : un motif ou une fin de phrase appelle une voix, un lieu ou une texture ;
- `TEXTURE` : un timbre, un rythme ou un événement territorial appelle une autre mémoire.

L’appel ne se produit pas à chaque diffusion.

### Règle HA10 — `RELIER`

- `MUSICALE` : le rythme ou le motif reste brièvement présent sous le fragment suivant ;
- `TEXTURE` : un fondu croisé de `2 à 6 s` relie deux lieux ou deux matières.

`RELIER` ne signifie pas seulement jouer deux sons ensemble : le mode choisi doit rendre audible ce qu’ils partagent ou ce qui les oppose.

### Règle HA11 — `REPONDRE`

- `MUSICALE` : l’ambiance entre après un délai, sur une enceinte différente, sous une forme reconnaissable ;
- `TEXTURE` : elle surgit comme le lieu, la matière ou la sensation réveillée par une parole.

### Règle HA12 — `REVENIR`

Pure Data sélectionne une ambiance dans l’historique récent et la réactive plus tard.

- `MUSICALE` : retour intact ou légèrement atténué, après plusieurs dizaines de secondes ou plusieurs minutes, éventuellement sur une autre enceinte ;
- `TEXTURE` : retour plus éloigné, filtré, court ou faible.

Un même fragment doit généralement être limité à `1 à 3` réapparitions.

### Règle HA13 — `SE_DEPLACER`

- `MUSICALE` : déplacement lent et limité entre `1 et 3` enceintes, sans rotation spectaculaire ;
- `TEXTURE` : trajet entre `2 et 4` enceintes ou constitution d’un halo.

### Règle HA14 — `DISPARAITRE`

- `MUSICALE` : fin de phrase ou fondu ; coupure brusque seulement si `OUVERTURE = TRES_OUVERT` et `MODE_LECTURE = INTERRUPTIBLE` ;
- `TEXTURE` : fin naturelle, éloignement spatial, filtrage progressif, masquage par une autre matière ou coupure.

La disparition ne constitue pas un effacement définitif : l’ambiance peut rester dans l’historique et redevenir disponible pour `REVENIR`.

---

## 11.10. Exemple complet — Parole, ambiance et réponse

Fragment source :

> « Est-ce que la personne que j’ai en face de moi… »

Déroulement possible :

1. Pure Data diffuse la parole du douanier.
2. Il laisse `2 s` de silence.
3. Il fait apparaître un environnement de gare ou de frontière depuis une enceinte arrière.
4. Il maintient cette ambiance pendant `8 à 20 s`.
5. Dans cet environnement, il fait surgir la voix de la cousine parlant d’un endroit où elle souhaite aller.
6. Il fait ensuite disparaître progressivement l’ambiance.

**Sensation :** l’ambiance ne décrit pas littéralement la scène. Elle crée un passage sensible entre contrôle, déplacement et désir.

---

## 11.11. Principe dramaturgique

Dans Cortex–Ambiance, le public entend encore le milieu d’où provient la mémoire.

Dans Hippocampe–Ambiance, il entend le milieu qu’un fragment réveille, parfois par le sens, le lieu, le rythme, le timbre, la langue ou le contraste.

L’ambiance ne doit pas constamment confirmer l’origine d’une parole. Elle peut l’éloigner de son premier contexte et la connecter à une autre époque, un autre territoire ou une autre mémoire. C’est ici que commence la déterritorialisation : le fragment reste reconnaissable, mais il n’appartient déjà plus à une seule situation.

Les associations restent orientées par les attributs sans produire une interprétation définitive. Le même chant, la même parole ou la même texture peut emprunter plusieurs chemins. Cette circulation variable rend perceptibles le rhizome, l’identité-relation et l’opacité de la mémoire.

---

# 12. Ordre logique proposé pour Pure Data

```text
1. Charger les métadonnées des fragments Hippocampe et Hippocampe–Ambiance.
2. Charger l’historique récent, les compteurs de retours et les couples récemment utilisés.
3. Sélectionner un fragment source.
4. Lire son MODE_LECTURE, sa DUREE_MIN_LECTURE et son OUVERTURE.
5. Déterminer sa forme de lecture :
   a. intégrale ;
   b. coupure originale ;
   c. interruption autorisée.
6. Lire sa FORCE_ASSOCIATIVE et effectuer le tirage de APPELER.
7. Si APPELER n’est pas activé, laisser le fragment seul puis choisir DISPARAITRE.
8. Si APPELER est activé :
   a. lire ses FAMILLES_CIBLES ;
   b. chercher les fragments dont FAMILLE_ASSOCIATIVE correspond ;
   c. appliquer la logique indiquée par TYPE_ASSOCIATION ;
   d. constituer la liste des candidats compatibles ;
   e. exclure les répétitions interdites ;
   f. si la liste est vide, laisser le fragment seul ;
   g. sinon choisir un candidat avec variation aléatoire.
9. Choisir la variante de APPELER : direct, superposé, différé, divergent ou sans réponse.
10. Choisir RELIER selon TYPE_ASSOCIATION : succession, superposition, relais ou contraste.
11. Appliquer OUVERTURE et DELAI_REPONSE.
12. Choisir la variante de REPONDRE : immédiate, retardée, spatiale, indirecte ou fragile.
13. Vérifier les limites de densité et de superposition avant la diffusion.
14. Déterminer le MODE_SPATIAL et les enceintes de diffusion.
15. Activer éventuellement SE_DEPLACER selon la durée et la nature du fragment.
16. Choisir DISPARAITRE : naturel, progressif, net, par recouvrement ou spatial.
17. Inscrire dans l’historique tous les fragments réellement entendus.
18. Effectuer ultérieurement le tirage de REVENIR parmi les fragments de l’historique.
19. Limiter la chaîne associative à deux ou trois fragments et les retours à la valeur autorisée.
20. Préserver un silence avant de recommencer sans construire de narration fixe.
```

---

# 13. Structure du tableau de référencement

## 13.1. Fragments de l’Hippocampe

| ID | Type fonctionnel | Durée fichier | Durée min. lecture | Mode lecture | Force | Type association | Famille associative | Familles cibles | Ouverture | Délai réponse | Densité | Comportements autorisés |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `H001_v3_hippocampe.wav` | à renseigner | à renseigner | à renseigner | `INTEGRAL` ou `INTERRUPTIBLE` | `1–3` | une ou plusieurs valeurs | mots-clés | mots-clés | `FERME`, `PARTIELLEMENT_SUSPENDU` ou `TRES_OUVERT` | à renseigner | à renseigner | à renseigner |

## 13.2. Fragments de l’Hippocampe–Ambiance

| Colonne | Valeurs possibles |
|---|---|
| `ID` | Nom du fichier |
| `TYPE_AMBIANCE` | `MUSICALE` / `TEXTURE` |
| `TYPE_FONCTIONNEL` | Une des catégories temporelles définies en 11.3 |
| `ROLE_AMBIANCE` | `SOLO` / `REPONSE` / `LIAISON` / `ACCOMPAGNEMENT` / `RETOUR` |
| `DUREE_FICHIER_S` | Durée réelle |
| `DUREE_MIN_LECTURE_S` | Durée minimale avant interruption |
| `MODE_LECTURE` | `INTEGRAL` / `EXTRAIT_VARIABLE` / `INTERRUPTIBLE` |
| `FORCE_ASSOCIATIVE` | `1` / `2` / `3` |
| `TYPE_ASSOCIATION` | `SENS` / `TIMBRE` / `LIEU` / `LANGUE` / `RYTHME` / `CONTRASTE` |
| `FAMILLE_ASSOCIATIVE` | Mots-clés multiples |
| `FAMILLES_CIBLES` | Mots-clés multiples |
| `OUVERTURE` | `FERME` / `PARTIELLEMENT_SUSPENDU` / `TRES_OUVERT` |
| `DELAI_REPONSE` | Plage en secondes |
| `SILENCE_APRES` | Plage en secondes |
| `NIVEAU_PRESENCE` | `PREMIER_PLAN` / `INTERMEDIAIRE` / `ARRIERE_PLAN` |
| `MODE_SPATIAL` | `LOCALISE` / `DUO_DISSYMETRIQUE` / `RELAIS` / `HALO` / `TRAJET_LENT` / `OPPOSITION` |
| `NB_ENCEINTES_MAX` | `1–4` par défaut |
| `GAIN_RELATIF_DB` | Niveau par rapport au fragment principal |
| `TRAITEMENT_MAX` | `INTACT` / `LEGER` / `MODERE` |
| `RECONNAISSABILITE_MIN` | `1–3` |
| `SUPERPOSITION_AUTORISEE` | Types de fragments compatibles |
| `CHEVAUCHEMENT_MIN_MAX_S` | Durée possible du chevauchement |
| `MODE_DISPARITION` | `FIN_NATURELLE` / `FONDU` / `FILTRAGE` / `ELOIGNEMENT` / `COUPURE` |
| `RETOUR_AUTORISE` | `OUI` / `NON` |
| `NOMBRE_RETOURS_MAX` | généralement `0–3` |

Ces paramètres d’exécution ne constituent pas de nouveaux attributs conceptuels. Ils traduisent les attributs et comportements déjà définis.

## 13.3. Métadonnées relationnelles éventuellement nécessaires

Si Alassane choisit une sélection automatique par critères plutôt qu’une table d’associations préparée, le tableau devra probablement contenir des colonnes supplémentaires :

| Attribut possible | Fonction |
|---|---|
| `LANGUE` | Identifier les rapprochements de type `LANGUE`. |
| `LIEU` | Identifier les rapprochements ou écarts de type `LIEU`. |
| `TIMBRE` | Classer les matières pour les rapprochements de type `TIMBRE`. |
| `RYTHME` | Classer les pulsations ou répétitions pour les rapprochements de type `RYTHME`. |
| `QUALITE_SENSIBLE` ou table dédiée | Définir les relations de `CONTRASTE`. |

Ces colonnes ne constituent pas de nouveaux principes artistiques. Elles représentent une condition technique possible pour traduire les types d’association sans demander à Pure Data d’analyser le son.

---

# 14. Points à confirmer avant de figer le patch

Ces points ne modifient pas le principe artistique, mais nécessitent une valeur ou une règle supplémentaire pour que le comportement soit entièrement déterminé dans Pure Data :

1. Tester puis valider les pourcentages `25/55/80 %` proposés pour les fragments.
2. Décider si les ambiances conservent leur échelle provisoire `25/50/75 %` ou utilisent la même échelle que les fragments.
3. Définir comment `OUVERTURE` modifie éventuellement la probabilité produite par `FORCE_ASSOCIATIVE`.
4. Confirmer si `MODE_LECTURE` est une métadonnée indépendante ou une conséquence de `OUVERTURE`.
5. Choisir entre deux méthodes pour coder `TYPE_ASSOCIATION` : métadonnées relationnelles complémentaires ou table d’associations préparée.
6. Définir le poids des différents types lorsqu’un fragment possède plusieurs valeurs de `TYPE_ASSOCIATION`.
7. Définir si plusieurs types d’association peuvent être exigés simultanément pour valider un candidat.
8. Définir précisément les relations autorisées pour `CONTRASTE`, notamment afin d’éviter les oppositions réductrices.
9. Valider définitivement les noms `FAMILLES_CIBLES` et `TYPE_ASSOCIATION` utilisés dans ce document.
10. Définir si une correspondance avec plusieurs familles cibles augmente la probabilité de sélection d’un candidat.
11. Définir la taille de l’historique récent et la méthode exacte empêchant la répétition immédiate d’un fragment ou d’une paire.
12. Définir la spatialisation du fragment suivant lorsque `OUVERTURE = FERME`.
13. Pour `OUVERTURE = TRES_OUVERT`, fixer la probabilité et le point possible d’une interruption avant la fin.
14. Fixer la vitesse, la durée et la trajectoire de chaque variante de `SE_DEPLACER`.
15. Définir les probabilités respectives des variantes de `APPELER`, `RELIER`, `REPONDRE`, `DISPARAITRE` et `REVENIR`.
16. Fixer la probabilité de retour, les latences maximales et la durée minimale entre deux retours.
17. Définir le délai précis séparant les deux réponses d’un appel divergent.
18. Définir l’attribut ou la règle permettant d’identifier deux paroles « longues et denses ».
19. Définir le gain ou la catégorie de présence du fragment qui répond.
20. Confirmer les gains proposés : ambiance secondaire `8–14 dB` sous le fragment principal et diminution sous une parole de `4–10 dB`.
21. Définir les conditions autorisant les légères modifications de vitesse et de hauteur des ambiances musicales.
22. Définir quels field recordings peuvent recevoir un delay ponctuel et lesquels doivent rester entièrement secs.
23. Fixer le vocabulaire contrôlé des `FAMILLE_ASSOCIATIVE` et `FAMILLES_CIBLES`.
24. Définir la réaction des capteurs piézoélectriques dans cette zone, car elle n’est pas précisée dans le texte source.
25. Définir la règle de passage de l’Hippocampe vers la Reconstruction et vers les autres zones.
