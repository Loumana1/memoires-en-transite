# Installation sonore — Attributs et comportements

## Spécifications pour Pure Data — Zone 4 : Reconstruction

Ce document décrit les attributs et les comportements de la zone **Reconstruction**, ainsi que ceux de la zone associée **Reconstruction–Ambiance**.

Il est destiné à permettre leur traduction dans Pure Data et leur renseignement fragment par fragment dans le tableau de référencement.

> **Principe de lecture pour le code**  
> Lorsque le document indique que « Pure Data identifie » une propriété, cela signifie que Pure Data **lit une métadonnée préalablement attribuée au fragment** dans le tableau. Pure Data n’a pas à comprendre seul le sens d’un mot, à reconnaître une assonance ou à déduire la provenance d’un son.

> **Principe de la banque préparée**  
> Les fragments de Reconstruction ont déjà été choisis, découpés dans Ableton, exportés avec des silences puis séparés en fichiers individuels. Pure Data travaille dans cette banque préparée. Il ne doit pas nécessairement redécouper en direct les fichiers du Cortex ou de l’Hippocampe pour que la Reconstruction fonctionne.

> **Distinction essentielle**  
> `ZONE = RECONSTRUCTION` indique la fonction actuelle du fichier dans l’installation. `PROVENANCE_MATERIAU` indique éventuellement la zone, la source ou le contexte dont sa matière a été extraite avant d’être placée dans la banque Reconstruction.

---

# 1. Fonction générale de la zone Reconstruction

## 1.1. Une banque d’unités de composition

Comme les autres zones, la Reconstruction possède sa propre banque de fichiers préparés. Elle fonctionne cependant différemment :

- dans le Cortex, le fragment demeure principalement une unité diffusée et superposée ;
- dans l’Hippocampe, le fragment demeure une mémoire reconnaissable mise en relation avec une autre ;
- dans la Reconstruction, le fragment devient une **unité de composition** pouvant être combinée à plusieurs autres fragments.

La banque peut contenir :

- mots isolés ;
- fragments de phrases retirés de leur contexte ;
- syllabes ;
- phonèmes ;
- attaques de mots ;
- voyelles prolongées ;
- consonnes ;
- souffles ;
- respirations ;
- hésitations ;
- assonances ;
- sons non verbaux ;
- matières vocales ;
- bruits ;
- pulsations ;
- motifs musicaux ;
- fragments de chants ;
- textures.

Leur point commun n’est pas leur durée ni leur nature sonore, mais leur capacité à participer à un nouvel agencement.

## 1.2. Reterritorialisation provisoire

La déterritorialisation a commencé lorsque les fragments ont été retirés de leur phrase, de leur contexte, de leur chronologie et de leur zone de provenance.

Dans la Reconstruction, la **reterritorialisation** s’effectue lorsque plusieurs fragments déplacés trouvent provisoirement une nouvelle organisation :

- une phrase composite ;
- une continuité phonétique ;
- une fusion de voix ;
- une texture vocale ;
- une pulsation ;
- une forme musicale fragmentaire ;
- un territoire sonore temporaire.

Cette reterritorialisation ne doit pas produire une identité belgo-congolaise stable, homogène ou résolue. Elle produit une **identité-relation en mouvement**, constituée de traces, de rencontres, de différences et de transformations.

La forme peut ensuite :

- se défaire ;
- rester suspendue ;
- perdre certains éléments ;
- se déplacer ;
- devenir moins reconnaissable ;
- être réinjectée dans la circulation générale ;
- ou persister dans la Boucle.

## 1.3. Écriture automatique orientée

La Reconstruction peut être comprise comme une **écriture automatique orientée par les propriétés des fragments**.

Elle ne repose ni sur :

- une phrase écrite à l’avance ;
- un hasard entièrement libre ;
- une succession permanente de petits sons ;
- une recherche de cohérence grammaticale parfaite.

Pure Data utilise les métadonnées pour produire un aléatoire composé. Chaque fragment possède :

- une granularité ;
- une provenance ;
- un ou plusieurs rôles compositionnels ;
- un potentiel compositionnel ;
- des compatibilités ;
- une mutabilité ;
- un degré de reconnaissabilité à préserver ;
- des transformations autorisées ou interdites.

## 1.4. Sensation recherchée

Le public doit pouvoir entendre qu’une forme est en train de se constituer, sans qu’elle devienne entièrement stable ni explicable.

Une phrase peut sembler commencer, être traversée par une autre voix, se prolonger dans une voyelle, rencontrer un souffle, devenir rythme, puis disparaître avant de se fixer.

La Reconstruction ne doit donc pas sonner comme :

- un catalogue de microsons ;
- un glitch permanent ;
- un collage aléatoire sans respiration ;
- une démonstration technique de granularisation.

Elle doit faire entendre une mémoire qui cherche momentanément une forme.

---

# 2. Typologie et durée des fragments

## 2.1. Types de fragments

| `GRANULARITE` | Contenu possible | Durée indicative du fichier | Fonction fréquente |
|---|---|---:|---|
| `MICRO_FRAGMENT` | Attaque, consonne, phonème, bruit de bouche | `0,05–0,5 s` | Ponctuer, rythmer, interrompre |
| `SYLLABE` | Syllabe isolée ou courte unité vocale | `0,15–1 s` | Prolonger, répéter, fusionner |
| `VOYELLE_ASSONANCE` | Voyelle, son tenu, résonance phonétique | `0,3–2 s` | Relier deux voix ou créer une continuité |
| `SOUFFLE_HESITATION` | Souffle, respiration, hésitation | `0,2–3 s` | Espacer, suspendre, relier |
| `MOT` | Mot isolé encore identifiable | `0,4–2,5 s` | Former un noyau, une ouverture ou une rupture |
| `SEGMENT_PHRASE` | Groupe de mots ou phrase coupée | `1,5–7 s` | Donner une direction provisoire à la forme |
| `FRAGMENT_STRUCTURANT` | Fragment verbal ou sonore plus développé | `4–12 s` | Former un socle ou une structure temporelle |
| `SON_PONCTUEL` | Choc, pas, objet, bruit bref | `0,1–3 s` | Ponctuer, rompre, rythmer |
| `TEXTURE_COURTE` | Matière non verbale ou vocale | `1–8 s` | Soutenir ou fondre plusieurs fragments |
| `MOTIF_MUSICAL` | Motif mélodique ou rythmique | `1–10 s` | Pulser, prolonger, structurer |
| `FRAGMENT_MUSICAL_DEVELOPPE` | Phrase musicale ou chant découpé | `8–20 s` | Installer une forme plus longue ou un contraste |

Les plages se recouvrent. Pure Data ne doit pas déduire automatiquement la granularité à partir de la seule durée : `GRANULARITE` est renseignée dans le tableau.

## 2.2. Durée du fichier et durée d’utilisation

La durée du fichier ne détermine pas seule sa fonction.

Un mot de `1 s` peut être :

- joué une seule fois comme noyau ;
- répété comme pulsation ;
- étiré comme prolongement ;
- superposé à une voyelle ;
- interrompu comme rupture.

Un fragment musical de `15 s` peut être :

- joué intégralement ;
- utilisé comme structure sous plusieurs microfragments ;
- traversé par une voix ;
- réduit à un extrait si son mode de lecture l’autorise.

| Paramètre | Fonction |
|---|---|
| `DUREE_FICHIER_S` | Durée totale réelle du fichier |
| `DUREE_MIN_LECTURE_S` | Durée minimale à entendre avant interruption ou transformation |
| `MODE_LECTURE` | `INTEGRAL` / `EXTRAIT_VARIABLE` / `INTERRUPTIBLE` / `REPETABLE` |
| `NOMBRE_REPETITIONS_MAX` | Limite des répétitions autorisées |

## 2.3. Durée des formes reconstruites

La Reconstruction ne diffuse pas nécessairement un fragment isolé : elle peut construire une forme à partir de plusieurs unités.

| `TYPE_FORME` | Durée totale indicative | Nombre indicatif d’unités | Sensation |
|---|---:|---:|---|
| `MICRO_AGENCEMENT` | `2–5 s` | `2–4` | Éclair, surgissement ou ponctuation reconstruite |
| `PHRASE_COMPOSITE` | `5–15 s` | `3–7` | Forme verbale ou sonore provisoirement lisible |
| `FORME_DEVELOPPEE` | `15–35 s` | `5–12` | Mémoire collective ou territoire sonore temporaire |
| `EXCEPTION_LONGUE` | `35–60 s` | variable | Déploiement rare comprenant respirations et évolutions |

Ces valeurs constituent une base de test. Une forme longue doit évoluer et contenir des respirations ; elle ne doit pas être une accumulation continue de microfragments.

### Règle R1 — Variation des échelles

Pure Data doit alterner :

- formes brèves ;
- phrases composites ;
- formes développées ;
- silences.

Il ne doit pas produire en permanence des séquences de mots, souffles et syllabes de même durée.

---

# 3. Architecture des attributs

Chaque fichier de la banque Reconstruction reçoit des attributs décrivant son potentiel de composition.

Les dimensions principales sont :

1. `TYPE_MATIERE` : nature générale du matériau ;
2. `GRANULARITE` : échelle de la découpe ;
3. `PROVENANCE_MATERIAU` : origine de la matière avant son classement en Reconstruction ;
4. `ROLE_COMPOSITIONNEL` : fonction que le fragment peut occuper dans une forme ;
5. `POTENTIEL_COMPOSITIONNEL` : capacité et fréquence d’emploi dans les agencements ;
6. `TYPE_COMPATIBILITE` : logique selon laquelle le fragment peut être rapproché d’un autre ;
7. `MUTABILITE` : profondeur de transformation supportée ;
8. `RECONNAISSABILITE_CIBLE` : degré minimal de reconnaissance à préserver ;
9. `CHARGE_SEMANTIQUE` : importance du sens verbal porté par le fragment ;
10. `SENSIBILITE_SOURCE` : niveau de protection éthique ou artistique du matériau.

Ces attributs décrivent le fragment. Les paramètres tels que `TYPE_FORME`, `DENSITE_COMPOSITION`, `COURBE_RECONNAISSABILITE` et `MODE_SPATIAL_COMPOSITION` décrivent, eux, l’agencement global produit par Pure Data.

---

# 4. Type de matière et granularité

## 4.1. Type de matière

| Attribut | Valeurs possibles |
|---|---|
| `TYPE_MATIERE` | `PAROLE` / `VOIX_NON_VERBALE` / `SOUFFLE` / `SON` / `MUSIQUE` / `TEXTURE` / `SILENCE_ENREGISTRE` |

`TYPE_MATIERE` permet notamment de limiter certaines superpositions et certains traitements.

Exemples :

- deux fragments `PAROLE` fortement chargés de sens ne doivent pas être systématiquement superposés ;
- un `SOUFFLE` peut plus facilement servir de liaison ;
- une `TEXTURE` peut soutenir une parole sans construire une seconde phrase ;
- un fragment `MUSIQUE` peut devenir pulsation ou structure.

## 4.2. Granularité

`GRANULARITE` décrit la forme concrète de la découpe et non son rôle définitif.

Un même `MOT` peut recevoir :

```text
ROLE_COMPOSITIONNEL = NOYAU + RUPTURE
```

Une même `VOYELLE_ASSONANCE` peut recevoir :

```text
ROLE_COMPOSITIONNEL = LIAISON + PROLONGEMENT
```

### Règle R2 — Le type ne détermine pas automatiquement le rôle

Pure Data ne doit pas conclure qu’un souffle est toujours une liaison ou qu’un mot est toujours un noyau. Il lit les rôles autorisés dans le tableau.

---

# 5. Provenance du matériau

## 5.1. Définition

| Attribut | Valeurs possibles |
|---|---|
| `PROVENANCE_MATERIAU` | `CORTEX` / `CORTEX_AMBIANCE` / `HIPPOCAMPE` / `HIPPOCAMPE_AMBIANCE` / `RECONSTRUCTION_ANTERIEURE` / autre source contrôlée |

Des métadonnées complémentaires peuvent préciser :

- `SOURCE_ID` : identifiant du fichier ou de la source d’origine ;
- `CONTEXTE_SOURCE` : `BELGIQUE`, `CONGO`, `DIASPORA`, `INDETERMINE`, etc. ;
- `TYPE_SOURCE` : `FAMILIALE`, `ARCHIVE`, `ADMINISTRATIVE`, `MEDIATIQUE`, `MUSICALE`, etc. ;
- `VOIX_SOURCE` : identifiant anonymisé de la personne si nécessaire.

## 5.2. Fonction artistique

La provenance ne sert pas à restaurer une généalogie fixe. Elle permet à Pure Data de varier les modes de rencontre :

- continuité entre fragments d’une même source ;
- croisement entre sources différentes ;
- fusion entre parole et musique ;
- rencontre entre matériau institutionnel et familial ;
- rencontre entre fragments contextualisés en Belgique et au Congo ;
- agencement où l’une des provenances demeure absente.

### Règle R3 — Pas de binarité obligatoire

Chaque reconstruction ne doit pas obligatoirement contenir un fragment Belgique et un fragment Congo. Une telle règle systématique figerait la Relation en opposition binaire.

Pure Data peut choisir un `MODE_PROVENANCE_FORME` :

| Valeur | Principe |
|---|---|
| `CONTINUITE` | Plusieurs fragments issus d’une même source ou d’un même contexte |
| `CROISEMENT` | Rencontre de deux provenances différentes |
| `HETEROGENE` | Agencement de trois provenances ou types de sources |
| `INDETERMINE` | La provenance n’intervient pas dans la sélection |

---

# 6. Rôle compositionnel

## 6.1. Définition

Le rôle compositionnel indique ce qu’un fragment peut faire dans une forme reconstruite.

| `ROLE_COMPOSITIONNEL` | Fonction dans la forme | Sensation à l’écoute |
|---|---|---|
| `OUVERTURE` | Commencer ou mettre en mouvement la forme | Quelque chose commence à se constituer |
| `NOYAU` | Porter momentanément le centre verbal, musical ou sonore | Un mot, une voix ou un motif devient reconnaissable |
| `LIAISON` | Faire passer d’un fragment à un autre | Une continuité apparaît malgré la différence des sources |
| `PROLONGEMENT` | Étendre une voyelle, un timbre, un rythme ou une résonance | Le fragment continue sous une autre matière |
| `PULSATION` | Donner une répétition ou une organisation rythmique | La forme acquiert un mouvement interne |
| `SOUTIEN` | Maintenir un fond limité sous d’autres unités | Plusieurs fragments peuvent tenir ensemble sans saturation |
| `RUPTURE` | Interrompre, contraster ou déplacer la direction | La forme perd sa trajectoire attendue |
| `FERMETURE` | Produire une fin momentanée | La forme semble se stabiliser ou se refermer |
| `SUSPENSION` | Empêcher la résolution et ouvrir un silence | La forme demeure inachevée |
| `TRACE` | Rester après la disparition des autres éléments | Une présence résiduelle persiste |

Un fragment peut recevoir plusieurs rôles compatibles.

## 6.2. Règles d’emploi

### Règle R4 — Structure minimale d’une forme

Une forme reconstruite doit généralement contenir :

- au moins un `NOYAU`, un `SOUTIEN` ou une `PULSATION` ;
- au moins un autre fragment possédant un rôle complémentaire.

Une succession de trois `RUPTURE` ou de cinq microfragments sans noyau ne constitue pas, par défaut, une forme reconstruite.

### Règle R5 — Ouverture non obligatoire

Une forme peut commencer directement par un noyau, une rupture ou une trace. `OUVERTURE` n’est pas obligatoire.

### Règle R6 — Fermeture non obligatoire

Une forme peut se terminer par `FERMETURE`, mais également par `SUSPENSION`, `DISSOUDRE` ou silence. La reterritorialisation reste ainsi provisoire.

---

# 7. Potentiel compositionnel

## 7.1. Définition

| Attribut | Valeurs possibles |
|---|---|
| `POTENTIEL_COMPOSITIONNEL` | `1` / `2` / `3` |

Le potentiel compositionnel ne mesure pas la qualité du fragment. Il indique sa capacité à être réutilisé dans des agencements variés.

| Valeur | Fonction |
|---|---|
| `1` — usage rare ou protégé | Fragment très spécifique, sensible ou difficile à combiner ; il doit parfois rester seul |
| `2` — usage relationnel | Fragment pouvant occuper plusieurs agencements lorsque certaines compatibilités sont respectées |
| `3` — fragment-charnière | Fragment très autonome ou polyvalent pouvant relier plusieurs types de matières |

Exemples :

- une hésitation ou une voyelle peut avoir `POTENTIEL_COMPOSITIONNEL = 3` si elle relie de nombreuses voix ;
- un mot politiquement très chargé peut avoir `POTENTIEL_COMPOSITIONNEL = 1` afin de ne pas être banalisé ;
- un motif musical peut avoir `POTENTIEL_COMPOSITIONNEL = 2` s’il fonctionne avec certaines familles rythmiques.

### Règle R7 — Pondération de la sélection

Pure Data utilise le potentiel compositionnel comme un poids de sélection, et non comme une obligation.

Base de test possible :

- valeur 1 : poids `1` ;
- valeur 2 : poids `2` ;
- valeur 3 : poids `3`.

Les règles de compatibilité, de répétition récente et de sensibilité restent prioritaires sur ce poids.

---

# 8. Compatibilité entre fragments

## 8.1. Définition

La compatibilité indique selon quelle logique deux fragments peuvent participer au même agencement.

| Attribut | Valeurs possibles |
|---|---|
| `TYPE_COMPATIBILITE` | `PHONETIQUE` / `SEMANTIQUE` / `TIMBRALE` / `RYTHMIQUE` / `ENERGETIQUE` / `CONTRASTE` / `PROVENANCE` |

Un fragment peut posséder plusieurs types de compatibilité.

## 8.2. Types de compatibilité

| Valeur | Principe | Exemple |
|---|---|---|
| `PHONETIQUE` | Rapprocher syllabes, voyelles, consonnes ou assonances | La fin sonore de « relation » rejoint une voyelle tenue d’une autre voix |
| `SEMANTIQUE` | Rapprocher ou déplacer des mots selon leurs charges de sens | « relation » rencontre « horizontal » sans constituer une définition fixe |
| `TIMBRALE` | Fusionner des matières proches ou complémentaires | Un souffle vocal rejoint un bruit d’air ou une résonance |
| `RYTHMIQUE` | Organiser les fragments selon attaques et pulsations | Une syllabe répétée rejoint un motif de likembe |
| `ENERGETIQUE` | Construire une progression ou une détente | Une matière calme est traversée par une attaque plus dense |
| `CONTRASTE` | Maintenir une différence audible et produire une tension | Un mot administratif rencontre une hésitation intime |
| `PROVENANCE` | Organiser continuité ou croisement entre sources | Une archive rejoint une voix familiale ou un fragment de la même personne |

## 8.3. Données nécessaires pour valider une compatibilité

`TYPE_COMPATIBILITE` indique la logique recherchée, mais ne suffit pas toujours à choisir les candidats. Deux méthodes sont possibles.

### Méthode A — Descripteurs dans le tableau

Chaque fragment reçoit, lorsque cela est pertinent :

| Descripteur | Exemples de valeurs |
|---|---|
| `PHONETIQUE` | `A`, `E`, `I`, `O`, `OU`, `NASAL`, `CONSONNE_DURE`, etc. |
| `TIMBRE` | `SOUFFLE`, `METALLIQUE`, `GRANULEUX`, `CHAUD`, `SEC`, `RESONANT`, etc. |
| `RYTHME` | `LIBRE`, `PULSE`, `REPETITIF`, `LENT`, `RAPIDE`, etc. |
| `ENERGIE` | `FAIBLE`, `MOYENNE`, `FORTE` |
| `CONTENU_SEMANTIQUE` | Mots-clés contrôlés : `FRONTIERE`, `RELATION`, `FAMILLE`, etc. |
| `PROVENANCE_MATERIAU` | Valeurs définies en section 5 |

Pure Data compare ensuite les descripteurs selon `TYPE_COMPATIBILITE`.

### Méthode B — Compatibilités préparées

Le tableau contient une colonne `COMPATIBLES_AVEC` renseignant :

- des identifiants précis ;
- des groupes d’identifiants ;
- ou des familles de fragments autorisées.

Cette méthode donne davantage de contrôle artistique, mais demande plus de travail de renseignement.

### Règle R8 — Aléatoire orienté par score

Pure Data peut constituer une liste de candidats puis attribuer un score :

- rôle complémentaire trouvé : `+3` ;
- compatibilité principale trouvée : `+3` ;
- deuxième compatibilité trouvée : `+1` ;
- mode de provenance recherché respecté : `+1` ;
- fragment entendu trop récemment : exclusion ou forte pénalité ;
- transformation interdite ou sensibilité incompatible : exclusion.

Pure Data choisit ensuite aléatoirement parmi les meilleurs candidats, sans prendre automatiquement celui qui possède le score maximal.

> Les valeurs de score sont une base de traduction à tester avec Alassane. Leur fonction est de produire un hasard orienté, pas une hiérarchie esthétique définitive.

### Règle R9 — Compatibilité non réciproque possible

Un fragment A peut être autorisé à prolonger B sans que B soit autorisé à prolonger A. La direction dépend notamment de leurs rôles.

---

# 9. Mutabilité, transformation et reconnaissabilité

## 9.1. Mutabilité

| Attribut | Valeurs possibles |
|---|---|
| `MUTABILITE` | `1` / `2` / `3` |

| Valeur | Degré de transformation |
|---|---|
| `1` — faible | Niveau, enveloppe, filtrage léger, spatialisation ; structure temporelle préservée |
| `2` — moyenne | Répétition, étirement modéré, changement modéré de hauteur, découpe partielle, superposition |
| `3` — forte | Microboucle, granularisation, réordonnancement, inversion autorisée, étirement important, transformation spectrale |

## 9.2. Reconnaissabilité

| Attribut | Valeurs possibles |
|---|---|
| `RECONNAISSABILITE_INITIALE` | `1` / `2` / `3` |
| `RECONNAISSABILITE_CIBLE` | `1` / `2` / `3` |

Échelle proposée :

- `1` : origine presque méconnaissable ;
- `2` : trace ou qualité encore perceptible ;
- `3` : mot, voix, motif ou source clairement identifiable.

La `RECONNAISSABILITE_CIBLE` empêche Pure Data de transformer tous les matériaux avec la même profondeur.

### Règle R10 — Relation entre mutabilité et reconnaissabilité

La transformation choisie doit respecter simultanément :

- `MUTABILITE` ;
- `RECONNAISSABILITE_CIBLE` ;
- `SENSIBILITE_SOURCE` ;
- `TRANSFORMATIONS_AUTORISEES`.

Un fragment `MUTABILITE = 3` peut malgré tout conserver une reconnaissabilité élevée si la transformation agit sur son espace ou son rythme plutôt que sur son intelligibilité.

## 9.3. Courbe de reconnaissabilité d’une forme

Pure Data peut attribuer à l’agencement global :

| `COURBE_RECONNAISSABILITE` | Fonction |
|---|---|
| `CLAIR_VERS_OPAQUE` | La forme commence reconnaissable puis se dissout |
| `OPAQUE_VERS_CLAIR` | Une matière indéterminée fait émerger un mot ou une voix |
| `OSCILLANTE` | Reconnaissance et opacité alternent |
| `STABLE` | Le degré de reconnaissance varie peu |

### Règle R11 — Micro-opacité

Une forme ne doit pas être rendue intégralement opaque par défaut. L’opacité devient perceptible parce que certains éléments restent reconnaissables tandis que d’autres échappent, se transforment ou disparaissent.

---

# 10. Charge sémantique et sensibilité de la source

## 10.1. Charge sémantique

| Attribut | Valeurs possibles |
|---|---|
| `CHARGE_SEMANTIQUE` | `FAIBLE` / `MOYENNE` / `FORTE` |

Exemples :

- syllabe sans signification autonome : `FAIBLE` ;
- mot identifiable mais polysémique : `MOYENNE` ;
- déclaration politique, témoignage ou mot historiquement chargé : `FORTE`.

### Règle R12 — Limitation des faux énoncés

Pure Data ne doit pas assembler automatiquement plusieurs fragments `CHARGE_SEMANTIQUE = FORTE` de manière à fabriquer une déclaration claire qui pourrait être attribuée à tort à une personne réelle.

Pour ces fragments, privilégier :

- juxtaposition séparée par un silence ;
- superposition partielle empêchant une fausse citation ;
- maintien des différences de voix ;
- agencement avec souffle, musique ou texture ;
- suspension plutôt que résolution grammaticale.

## 10.2. Sensibilité de la source

| Attribut | Valeurs possibles |
|---|---|
| `SENSIBILITE_SOURCE` | `ORDINAIRE` / `SENSIBLE` / `PROTEGEE` |

Peuvent notamment être `PROTEGEE` :

- témoignages vulnérables ;
- voix familiales intimes ;
- chants rituels ;
- paroles dont la transformation pourrait modifier abusivement le sens.

### Règle R13 — Traitement des sources protégées

Une source `PROTEGEE` peut participer à la Reconstruction, mais uniquement selon les traitements explicitement autorisés dans sa ligne.

Elle peut, par exemple :

- rester reconnaissable comme noyau ;
- être entourée de fragments transformés ;
- fournir un souffle ou une résonance déjà découpée et validée ;
- être spatialisée sans être fortement déformée.

---

# 11. Construction d’une forme reconstruite

## 11.1. Paramètres de forme

Avant de choisir les fichiers, Pure Data détermine un profil d’agencement.

| Paramètre de forme | Valeurs possibles |
|---|---|
| `TYPE_FORME` | `MICRO_AGENCEMENT` / `PHRASE_COMPOSITE` / `FORME_DEVELOPPEE` / `EXCEPTION_LONGUE` |
| `DENSITE_COMPOSITION` | `AEREE` / `MOYENNE` / `DENSE` |
| `COURBE_RECONNAISSABILITE` | `CLAIR_VERS_OPAQUE` / `OPAQUE_VERS_CLAIR` / `OSCILLANTE` / `STABLE` |
| `MODE_PROVENANCE_FORME` | `CONTINUITE` / `CROISEMENT` / `HETEROGENE` / `INDETERMINE` |
| `MODE_SPATIAL_COMPOSITION` | valeurs définies en section 14 |
| `RESOLUTION_FORME` | `FERMETURE` / `SUSPENSION` / `DISSOLUTION` / `TRACE` |

## 11.2. Densité

| Valeur | Règle indicative |
|---|---|
| `AEREE` | `2–5` unités ; silences perceptibles ; généralement `1–2` sons simultanés |
| `MOYENNE` | `4–8` unités ; alternance de succession et de chevauchement ; maximum habituel `3` sons |
| `DENSE` | `6–12` unités ; répétitions ou couches ; maximum habituel `4` sons, dont au plus `2` paroles |

### Règle R14 — Prévenir la succession sans relief

Une forme ne doit pas être constituée uniquement d’unités inférieures à `1 s` jouées successivement.

Pour toute `PHRASE_COMPOSITE` ou `FORME_DEVELOPPEE`, Pure Data doit généralement inclure au moins l’un des éléments suivants :

- un noyau tenu plus longtemps ;
- un segment de phrase ;
- un motif musical ;
- une texture de soutien ;
- un silence structurant ;
- une voyelle ou une résonance prolongée.

## 11.3. Silences internes

Les silences font partie de l’agencement.

| Type de silence | Durée indicative | Fonction |
|---|---:|---|
| `MICRO_SILENCE` | `0,05–0,4 s` | Articulation ou découpe rythmique |
| `SILENCE_LIAISON` | `0,4–2,5 s` | Laisser apparaître la relation entre deux unités |
| `SILENCE_SUSPENSION` | `2–6 s` | Maintenir une forme ouverte |
| `SILENCE_APRES_FORME` | `3–12 s` | Séparer deux reconstructions et éviter le flux permanent |

### Règle R15 — Le silence n’est pas un échec

Pure Data peut terminer une forme sans fermeture sonore et conserver uniquement un silence. La mémoire reconstruite ne doit pas toujours être complétée.

## 11.4. Séquence de sélection

### Règle R16 — Constitution de l’agencement

Pure Data doit pouvoir :

1. choisir un profil de forme ;
2. sélectionner un premier fragment compatible avec un rôle d’entrée ;
3. constituer une liste de candidats selon les rôles complémentaires ;
4. appliquer les compatibilités ;
5. respecter provenance, sensibilité et transformations autorisées ;
6. choisir aléatoirement parmi les candidats valides ;
7. déterminer succession, suture, fusion ou superposition ;
8. appliquer une courbe de reconnaissabilité ;
9. choisir une résolution ;
10. conserver éventuellement la forme dans un buffer.

### Règle R17 — Échec de sélection

Si aucun candidat compatible n’est trouvé :

- Pure Data ne choisit pas un fichier arbitraire ;
- il peut laisser le fragment seul ;
- réduire la taille de la forme ;
- insérer un silence ;
- ou recommencer avec un autre noyau.

---

# 12. Architecture des comportements

Les comportements privilégiés de la Reconstruction sont :

| Comportement | Fonction |
|---|---|
| `SELECTIONNER` | Choisir les unités de la banque selon le profil de forme |
| `AGENCER` | Organiser les rôles, l’ordre, les silences et la durée globale |
| `SUTURER` | Joindre deux fragments tout en laissant perceptible leur coupure |
| `FUSIONNER` | Produire une continuité entre deux matières |
| `SUPERPOSER` | Faire coexister plusieurs unités pendant une durée contrôlée |
| `TRANSFORMER` | Modifier la matière selon sa mutabilité |
| `REPETER` | Réactiver une unité pour produire insistance ou pulsation |
| `SUSPENDRE` | Interrompre ou laisser la forme sans résolution |
| `DISSOUDRE` | Défaire progressivement l’agencement |
| `REINJECTER` | Remettre un résultat ou ses traces dans la circulation générale |

Une forme peut suivre, par exemple :

```text
SELECTIONNER → AGENCER → SUTURER → TRANSFORMER → SUSPENDRE
```

ou :

```text
SELECTIONNER → AGENCER → FUSIONNER → SUPERPOSER → DISSOUDRE → REINJECTER
```

Tous les comportements ne doivent jamais être activés simultanément.

## 12.1. Comportement `SELECTIONNER`

### Règle R18 — Sélection par rôles

Pure Data choisit d’abord les rôles nécessaires au profil de forme, puis recherche les fichiers capables de les occuper.

Il ne doit pas choisir cinq fichiers puis leur attribuer arbitrairement une fonction après coup.

### Règle R19 — Sélection pondérée

La sélection tient compte :

- du `POTENTIEL_COMPOSITIONNEL` ;
- du rôle recherché ;
- des compatibilités ;
- du mode de provenance ;
- de la mutabilité nécessaire ;
- de l’historique récent ;
- de la sensibilité de la source.

### Règle R20 — Prévention des répétitions

Pure Data doit éviter :

- le même fragment dans deux formes successives ;
- le même couple de fragments trop rapproché ;
- le même noyau utilisé trop fréquemment ;
- les mêmes enchaînements de rôles à chaque activation.

## 12.2. Comportement `AGENCER`

`AGENCER` organise la forme globale sans rechercher une phrase grammaticale parfaite.

### Règle R21 — Agencement par fonction

Pure Data peut organiser :

- ouverture → noyau → liaison → noyau → suspension ;
- pulsation → noyau → prolongement → rupture ;
- trace → noyau → fusion → dissolution ;
- rupture → silence → noyau → fermeture.

### Règle R22 — Variabilité de la structure

Le même profil ne doit pas être répété systématiquement. Les rôles peuvent être absents, inversés ou interrompus, à condition que la forme conserve un minimum de relief.

## 12.3. Comportement `SUTURER`

La suture relie deux fragments sans effacer complètement leur séparation.

Variantes :

### Règle R23 — Suture par coupe

Le second fragment commence immédiatement après le premier, avec un fondu très court de `10–100 ms` destiné uniquement à éviter un clic numérique.

**Sensation :** deux fragments différents forment une phrase cassée dont la couture reste audible.

### Règle R24 — Suture par silence

Un silence de `0,1–2 s` sépare les fragments.

**Sensation :** la relation se construit dans l’intervalle plutôt que dans la continuité.

### Règle R25 — Suture par élément-liant

Une voyelle, un souffle, une assonance ou une texture courte est placé entre deux noyaux.

**Sensation :** la matière d’une voix paraît traverser l’autre sans les rendre identiques.

### Règle R26 — Suture spatiale

Le premier fragment termine sur une enceinte et le second commence sur une autre. Un élément-liant peut circuler entre les deux.

## 12.4. Comportement `FUSIONNER`

La fusion produit une continuité plus forte que la suture. Les sources doivent néanmoins pouvoir rester partiellement distinctes.

### Règle R27 — Fusion par chevauchement

Deux fragments se chevauchent pendant `0,2–3 s` avec des enveloppes complémentaires.

À privilégier pour :

- voyelle et souffle ;
- deux timbres compatibles ;
- voix et musique ;
- syllabe et texture ;
- motif rythmique et son ponctuel.

### Règle R28 — Fusion phonétique

La fin sonore d’un fragment est prolongée par une syllabe, une assonance ou une voyelle compatible provenant d’une autre source.

### Règle R29 — Fusion timbrale

Un filtre, une réverbération commune ou une enveloppe partagée rapproche deux matières sans supprimer toutes leurs différences.

### Règle R30 — Fusion profonde

Si les deux fragments possèdent une mutabilité suffisante, Pure Data peut utiliser :

- granularisation ;
- modulation croisée ;
- gel spectral ;
- mélange dans un buffer ;
- étirement important.

Cette variante dépend des modules réellement disponibles dans le patch et doit rester ponctuelle.

### Garde-fou

La fusion ne signifie pas que les voix belges et congolaises doivent devenir indistinguables. Certaines relations doivent préserver la différence et l’irréductibilité des sources.

## 12.5. Comportement `SUPERPOSER`

### Règle R31 — Superposition hiérarchisée

Les fragments superposés reçoivent des niveaux et des fonctions différents :

- noyau au premier plan ;
- soutien ou prolongement au plan intermédiaire ;
- trace à l’arrière-plan.

### Règle R32 — Limites de superposition

Base de test :

- maximum habituel : `3` fragments simultanés ;
- maximum exceptionnel : `4` ;
- maximum de paroles sémantiquement fortes : `2`, à des plans différents ;
- pas de quatre microfragments au même niveau sonore.

### Règle R33 — Superposition non permanente

La forme doit pouvoir alterner entre :

- unité seule ;
- duo ;
- couche plus dense ;
- retour au silence.

## 12.6. Comportement `TRANSFORMER`

### Règle R34 — Transformation selon les métadonnées

Pure Data choisit uniquement parmi `TRANSFORMATIONS_AUTORISEES` et respecte `MUTABILITE`, `RECONNAISSABILITE_CIBLE` et `SENSIBILITE_SOURCE`.

Familles de traitements possibles :

| Traitement | Fonction sensible |
|---|---|
| `ETIRER` | Faire durer une trace ou suspendre un mot |
| `COMPRIMER_TEMPS` | Rendre un souvenir plus furtif ou nerveux |
| `CHANGER_HAUTEUR` | Rapprocher ou éloigner des timbres, déstabiliser une identité vocale |
| `FILTRER` | Faire perdre ou émerger certaines fréquences |
| `GRANULARISER` | Transformer le fragment en particules tout en conservant parfois une trace |
| `INVERSER` | Retirer temporairement la direction habituelle du son |
| `GELER` | Transformer un instant en matière prolongée |
| `MODIFIER_ENVELOPPE` | Retirer l’attaque, prolonger la fin ou rendre la source fragile |
| `SPATIALISER` | Modifier la position et la relation entre les unités |

### Bases techniques provisoires

| `MUTABILITE` | Étirement indicatif | Hauteur indicative | Transformations principales |
|---|---|---|---|
| `1` | `0,9–1,1×` | aucune ou ±`1` demi-ton | niveau, filtre léger, enveloppe, espace |
| `2` | `0,65–1,5×` | jusqu’à ±`3` demi-tons | répétition, découpe, étirement, superposition |
| `3` | `0,25–2,5×` | jusqu’à ±`12` demi-tons si autorisé | granularisation, inversion, gel, réordonnancement |

Ces valeurs sont des bases de test, non des obligations artistiques.

## 12.7. Comportement `REPETER`

### Règle R35 — Répétition simple

Un mot, une syllabe ou un son revient `1 à 4` fois avec de légères variations de durée, de niveau ou d’espace.

### Règle R36 — Répétition pulsée

Le fragment devient une pulsation temporaire. Les intervalles peuvent être réguliers pendant une courte période, puis se dérégler.

### Règle R37 — Répétition d’érosion

À chaque retour, le fragment perd :

- une partie de ses fréquences ;
- de sa durée ;
- de son niveau ;
- ou de sa reconnaissabilité.

### Règle R38 — Limite

La répétition ne doit pas transformer toute la Reconstruction en bégaiement ou en beat permanent. Les fragments longs, sensibles ou fortement sémantiques reçoivent un nombre maximal plus faible.

## 12.8. Comportement `SUSPENDRE`

### Règle R39 — Suspension par coupure

La forme s’interrompt avant l’apparition d’une fermeture attendue.

### Règle R40 — Suspension par prolongement

Une voyelle, un souffle, une résonance ou une texture reste seule pendant `1–6 s` après la disparition des noyaux.

### Règle R41 — Suspension par silence

Pure Data retire tous les éléments et laisse un silence de `2–8 s`.

**Sensation :** la reterritorialisation existe, mais refuse de se fixer en résultat définitif.

## 12.9. Comportement `DISSOUDRE`

### Règle R42 — Dissolution par niveaux

Les fragments disparaissent l’un après l’autre, du premier plan vers l’arrière-plan ou inversement.

### Règle R43 — Dissolution fréquentielle

Les fréquences aiguës, graves ou médiums disparaissent progressivement selon la matière.

### Règle R44 — Dissolution granulaire

La forme se fragmente en grains de plus en plus espacés jusqu’au silence.

### Règle R45 — Dissolution spatiale

Les unités convergées se dispersent vers plusieurs enceintes tandis que leur niveau baisse.

### Règle R46 — Résidu

Un seul fragment `TRACE`, un souffle ou une texture peut demeurer après la dissolution.

## 12.10. Comportement `REINJECTER`

`REINJECTER` remet en circulation soit les constituants de la forme, soit le résultat sonore réellement produit.

### Mode A — Réinjection des constituants

Pure Data conserve dans l’historique :

- les identifiants utilisés ;
- leur ordre ;
- leurs transformations ;
- leur position spatiale.

Il peut ensuite rappeler un fragment ou reproduire une variante de l’agencement.

### Mode B — Réinjection du résultat enregistré

Pure Data enregistre la sortie de la Reconstruction dans un buffer temporaire. Ce buffer devient une nouvelle trace pouvant :

- revenir dans la Reconstruction ;
- être utilisée par Reconstruction–Ambiance ;
- alimenter la Boucle ;
- réapparaître ultérieurement comme mémoire reconstruite.

### Règle R47 — Condition technique

Le Mode B nécessite l’enregistrement réel de la sortie dans un buffer. Sans ce buffer, Pure Data peut rejouer les fichiers et les paramètres de l’agencement, mais il ne possède pas automatiquement un nouveau fichier fusionné.

### Règle R48 — Identité temporaire du résultat

Une reconstruction enregistrée doit recevoir au minimum :

- un identifiant temporaire ;
- sa date ou son ordre de création ;
- ses fragments sources ;
- son degré moyen de reconnaissabilité ;
- sa durée ;
- un nombre maximal de retours.

---

# 13. Combinaisons de comportements et limites dramaturgiques

## 13.1. Combinaisons possibles

| Combinaison | Fonction |
|---|---|
| `AGENCER → SUTURER → SUSPENDRE` | Construire une phrase cassée puis la laisser ouverte |
| `AGENCER → FUSIONNER → TRANSFORMER → DISSOUDRE` | Produire un territoire sonore puis le défaire |
| `AGENCER → SUPERPOSER → REPETER → SUSPENDRE` | Créer une mémoire insistante puis interrompue |
| `AGENCER → FUSIONNER → REINJECTER` | Transformer l’agencement en trace disponible pour la Boucle |
| `AGENCER → SUTURER → DISSOUDRE → TRACE` | Laisser un résidu après une construction provisoire |

## 13.2. Limites générales

### Règle R49 — Complexité variable

Pure Data doit permettre des formes simples. Il ne faut pas activer fusion, granularisation, répétition, déplacement et dissolution profonde dans chaque reconstruction.

### Règle R50 — Respiration

Après une forme développée ou dense, privilégier :

- un silence ;
- un fragment seul ;
- ou une ambiance très faible.

### Règle R51 — Préservation de la différence

La fusion ne doit pas être la seule forme de relation. Suture, contraste, intervalle et silence permettent de maintenir l’opacité et l’irréductibilité des sources.

### Règle R52 — Limitation du sens fabriqué

Lorsque plusieurs mots reconnaissables sont agencés, Pure Data doit éviter de produire systématiquement des phrases affirmatives plausibles. L’écriture automatique peut suggérer un sens, mais ne doit pas fabriquer une fausse citation stable.

---

# 14. Répartition spatiale sur huit enceintes

## 14.1. Principe général

Dans la Reconstruction, l’espace matérialise la formation puis la dissolution d’un territoire provisoire.

Les fragments peuvent :

- apparaître séparément ;
- se rapprocher ;
- converger ;
- fusionner sur une même zone spatiale ;
- rester en constellation ;
- puis se disperser.

Le mouvement ne doit pas devenir une rotation décorative permanente.

## 14.2. Modes spatiaux de composition

| `MODE_SPATIAL_COMPOSITION` | Fonction |
|---|---|
| `CONVERGENCE` | Des fragments apparaissent sur plusieurs enceintes puis se rapprochent vers une ou deux enceintes |
| `CONSTELLATION` | Plusieurs unités restent séparées sur différents points tout en formant une relation |
| `SUTURE_SPATIALE` | Un fragment ou un liant passe d’une enceinte à une autre pour joindre deux sources |
| `HALO` | Un noyau localisé est entouré de prolongements ou de traces faibles |
| `BASCULE` | La forme passe nettement d’un côté de l’espace à l’autre |
| `DISPERSION` | Une forme unifiée se défait vers plusieurs enceintes |
| `FIXE_LOCALISE` | La reconstruction demeure sur une ou deux enceintes |

## 14.3. Spatialisation selon les rôles

| Rôle | Spatialisation à privilégier |
|---|---|
| `OUVERTURE` | Une enceinte localisée ou un surgissement latéral |
| `NOYAU` | Position relativement stable sur une enceinte ou un duo asymétrique |
| `LIAISON` | Trajet entre deux points, relais ou fondu spatial |
| `PROLONGEMENT` | Deux ou trois enceintes à faible niveau autour du noyau |
| `PULSATION` | Relais limité entre deux ou trois enceintes |
| `RUPTURE` | Enceinte opposée ou changement brusque de position |
| `FERMETURE` | Convergence vers un point ou arrêt commun |
| `SUSPENSION` | Éloignement, position arrière ou disparition dans le silence |
| `TRACE` | Une enceinte éloignée à faible niveau |

## 14.4. Limitation spatiale

### Règle R53 — Nombre d’enceintes

Base de test :

- forme localisée : `1–2` enceintes ;
- forme relationnelle : `2–4` enceintes ;
- forme développée : `3–6` enceintes ;
- huit enceintes simultanées : exception, avec niveaux inégaux et fonction précise.

### Règle R54 — Convergence perceptible

Pour rendre la reterritorialisation audible, certaines formes doivent passer d’éléments spatialement séparés à une zone plus concentrée. La convergence doit être lente ou articulée suffisamment clairement pour être perçue.

### Règle R55 — Dispersion perceptible

La dissolution peut inverser ce mouvement : une forme provisoirement unifiée se fragmente et s’éloigne dans l’espace.

---

# 15. Traitements sonores de la Reconstruction

## 15.1. Traitements permis

La Reconstruction est la zone où les transformations les plus profondes deviennent possibles :

- découpe supplémentaire si autorisée ;
- changement de vitesse ;
- changement de hauteur ;
- répétition ;
- microboucle ;
- inversion ;
- filtrage ;
- réverbération ;
- delay ponctuel ;
- étirement ;
- gel spectral ;
- granularisation ;
- modification d’enveloppe ;
- superposition ;
- fondu croisé ;
- enregistrement dans un buffer ;
- spatialisation dynamique.

## 15.2. Traitements non automatiques

Le fait qu’un traitement soit possible dans la zone ne signifie pas qu’il est autorisé pour tous les fichiers.

Chaque ligne doit préciser :

```text
TRANSFORMATIONS_AUTORISEES
TRANSFORMATIONS_INTERDITES
TRAITEMENT_MAX
```

## 15.3. Garde-fous

- ne pas granulariser toutes les voix ;
- ne pas ajouter du delay à tous les sons ;
- ne pas modifier systématiquement la hauteur des voix ;
- préserver les sources `PROTEGEE` ;
- éviter que les effets masquent constamment les relations entre les fragments ;
- maintenir des alternances entre matière intacte, légèrement transformée et profondément reconstruite.

---

# 16. Exemple complet de reconstruction

## 16.1. Fragments disponibles

| Fragment | Attributs principaux possibles |
|---|---|
| « d’arriver jusque… » | `SEGMENT_PHRASE`, `OUVERTURE + SUSPENSION`, charge `MOYENNE`, mutabilité `1–2` |
| souffle court | `SOUFFLE_HESITATION`, `LIAISON`, potentiel `3`, mutabilité `3` |
| « une relation » | `MOT` ou groupe court, `NOYAU`, charge `MOYENNE`, reconnaissabilité cible `3` |
| voyelle provenant d’une autre voix | `VOYELLE_ASSONANCE`, `PROLONGEMENT + LIAISON`, mutabilité `3` |
| « horizontal » | `MOT`, `NOYAU + FERMETURE`, charge `MOYENNE`, reconnaissabilité cible `2–3` |
| motif musical bref | `MOTIF_MUSICAL`, `PULSATION + SOUTIEN`, mutabilité `2` |

## 16.2. Déroulement possible

1. Pure Data choisit `TYPE_FORME = PHRASE_COMPOSITE`.
2. Il choisit `DENSITE_COMPOSITION = AEREE`.
3. Il joue « d’arriver jusque… » sur une enceinte latérale.
4. Après `0,7 s`, un souffle apparaît depuis une enceinte arrière et se déplace lentement.
5. Le souffle se fond dans la première voyelle de « une relation ».
6. « une relation » apparaît clairement sur une autre enceinte et devient le noyau.
7. Une voyelle d’une autre voix prolonge la fin du mot pendant `1,5 s`.
8. Un motif musical très faible forme une pulsation irrégulière.
9. « horizontal » apparaît depuis une enceinte opposée.
10. Au lieu de produire une conclusion stable, sa dernière syllabe est étirée puis filtrée.
11. La pulsation et les voix disparaissent ; seul le souffle reste pendant `2 s`.
12. La forme se termine par un silence de `5 s`.
13. Si le buffer est activé, la forme produite peut être conservée comme nouvelle trace.

## 16.3. Sensation recherchée

Une phrase semble se construire entre plusieurs voix et plusieurs sources. Certains mots restent compréhensibles, mais la relation qu’ils forment demeure instable. Le souffle et la musique empêchent la composition de devenir une déclaration fixe. L’espace rapproche momentanément les fragments, puis les sépare de nouveau.

---

# 17. Zone Reconstruction–Ambiance

## 17.1. Fonction générale

Reconstruction–Ambiance ne restitue pas le milieu d’origine comme Cortex–Ambiance et ne fait pas seulement apparaître un milieu associé comme Hippocampe–Ambiance.

Elle produit le **milieu provisoire créé par la reconstruction elle-même**.

Cette zone peut être constituée de matières déjà préparées dans une banque dédiée :

- résidus de field recordings ;
- souffles étirés ;
- fragments musicaux transformables ;
- résonances ;
- bruits urbains filtrés ;
- pulsations extraites de sons ;
- nappes ;
- microboucles ;
- traces vocales ;
- mélanges préparés dans Ableton.

Elle peut également, si le patch le permet, recevoir une copie transformée ou enregistrée des résultats de la Reconstruction.

### Règle RA1 — Pas de fond permanent

Reconstruction–Ambiance ne constitue pas une nappe continue. Elle peut :

- précéder une forme reconstruite ;
- apparaître pendant sa construction ;
- relier ses éléments ;
- se former à partir d’elle ;
- ou demeurer comme résidu après sa dissolution.

## 17.2. Catégories

| `TYPE_AMBIANCE` | Contenu | Fonction dominante |
|---|---|---|
| `MUSICALE_RECONSTRUITE` | Motif, chant, harmonie ou pulsation transformés | Produire un milieu affectif ou rythmique instable |
| `TEXTURE_RECONSTRUITE` | Souffle, bruit, field recording, résonance ou matière filtrée | Produire un territoire matériel provisoire |
| `HYBRIDE` | Fusion de musique, voix, bruit ou ambiance | Rendre l’origine plurielle ou partiellement indécidable |

---

# 18. Durée des ambiances reconstruites

## 18.1. Ambiances musicales reconstruites

| Type fonctionnel | Durée indicative | Fonction |
|---|---:|---|
| `RESIDU_MUSICAL` | `3–10 s` | Trace mélodique ou rythmique après une reconstruction |
| `MOTIF_RECONSTRUIT` | `8–20 s` | Pulsation ou forme musicale temporaire |
| `MILIEU_MUSICAL_RECONSTRUIT` | `20–45 s` | Environnement affectif ou rythmique évolutif |
| `EXCEPTION_MUSICALE_LONGUE` | `45–75 s` | Déploiement rare possédant une mutation interne |

## 18.2. Textures reconstruites

| Type fonctionnel | Durée indicative | Fonction |
|---|---:|---|
| `TRACE_TEXTURELLE` | `2–8 s` | Résidu, souffle ou matière brève |
| `TRANSITION_TEXTURELLE` | `6–15 s` | Relier deux formes ou deux états |
| `MILIEU_TEXTUREL_RECONSTRUIT` | `15–45 s` | Environnement provisoire évolutif |
| `EXCEPTION_TEXTURELLE_LONGUE` | `45–90 s` | Milieu rare comprenant plusieurs mutations |

## 18.3. Hybrides

Une ambiance `HYBRIDE` peut durer environ `10–60 s`, selon son évolution. Sa durée ne doit pas être prolongée uniquement parce qu’elle est complexe.

### Règle RA2 — Durée réelle et durée de diffusion

Comme dans les autres zones, le tableau doit distinguer :

- `DUREE_FICHIER_S` ;
- `DUREE_MIN_LECTURE_S` ;
- `MODE_LECTURE` ;
- `SILENCE_APRES`.

Base de silence après une ambiance reconstruite : `3–12 s`, pouvant aller jusqu’à `15 s` après une ambiance dense.

---

# 19. Attributs de Reconstruction–Ambiance

## 19.1. Attributs principaux

| Attribut | Valeurs possibles | Fonction |
|---|---|---|
| `TYPE_AMBIANCE` | `MUSICALE_RECONSTRUITE` / `TEXTURE_RECONSTRUITE` / `HYBRIDE` | Nature générale |
| `PROVENANCE_MATERIAU` | une ou plusieurs zones ou sources | Origine des traces utilisées |
| `ROLE_AMBIANCE` | `SOCLE` / `LIANT` / `ENVELOPPE` / `CONTREPOINT` / `TRANSITION` / `RESIDU` | Fonction auprès de la forme reconstruite |
| `POTENTIEL_FUSION` | `1` / `2` / `3` | Capacité à accueillir ou rejoindre d’autres matières |
| `TYPE_COMPATIBILITE` | `TIMBRALE` / `RYTHMIQUE` / `ENERGETIQUE` / `SEMANTIQUE` / `CONTRASTE` / `PROVENANCE` | Logique de rencontre |
| `MUTABILITE` | `1` / `2` / `3` | Profondeur de transformation possible |
| `RECONNAISSABILITE_CIBLE` | `1` / `2` / `3` | Niveau minimal de trace à préserver |
| `DENSITE` | `FAIBLE` / `MOYENNE` / `FORTE` | Quantité et épaisseur de matière |
| `STABILITE` | `INSTABLE` / `EVOLUTIVE` / `SEDIMENTEE` | Manière dont le milieu tient dans le temps |

## 19.2. Rôle des ambiances

| `ROLE_AMBIANCE` | Fonction | Sensation |
|---|---|---|
| `SOCLE` | Soutenir temporairement plusieurs fragments | Les éléments semblent partager un même territoire |
| `LIANT` | Faire passer entre deux matières | Une continuité apparaît entre des sources différentes |
| `ENVELOPPE` | Entourer un noyau sans le masquer | La voix paraît contenue dans un milieu en formation |
| `CONTREPOINT` | Maintenir une différence ou une tension | L’ambiance résiste à la direction de la parole |
| `TRANSITION` | Relier deux formes reconstruites | Le territoire sonore change progressivement |
| `RESIDU` | Demeurer après la disparition des fragments | La forme passée laisse une trace |

## 19.3. Potentiel de fusion

| Valeur | Fonction |
|---|---|
| `1` | Ambiance spécifique ou protégée, généralement diffusée seule ou faiblement transformée |
| `2` | Ambiance pouvant accueillir une voix, une texture ou une transformation compatible |
| `3` | Matière-charnière pouvant fusionner plusieurs fragments ou devenir le milieu d’une forme |

Le potentiel de fusion ne doit pas rendre l’ambiance omniprésente. Il pondère sa sélection lorsque Pure Data recherche un socle, un liant ou une enveloppe.

## 19.4. Compatibilités

### Ambiances musicales reconstruites

À privilégier :

- `RYTHMIQUE` : motif musical avec syllabes, pas, moteur ou sons ponctuels ;
- `TIMBRALE` : chant avec voyelle ou résonance ;
- `ENERGETIQUE` : progression musicale avec montée de densité ;
- `CONTRASTE` : musique stable traversée par une parole interrompue ;
- `PROVENANCE` : motif transformé rejoignant une autre trace de sa source.

### Textures reconstruites

À privilégier :

- `TIMBRALE` : souffle, vent, filtre ou résonance ;
- `ENERGETIQUE` : densification ou raréfaction ;
- `RYTHMIQUE` : texture cyclique avec pulsation ;
- `PROVENANCE` : plusieurs résidus d’un même lieu ou de lieux croisés ;
- `CONTRASTE` : matière diffuse interrompue par un son net.

### Ambiances hybrides

Elles peuvent utiliser plusieurs compatibilités, mais doivent conserver une hiérarchie perceptible. Une hybridation ne signifie pas que toutes les matières doivent être également présentes.

## 19.5. Mutabilité et stabilité

### `STABILITE = INSTABLE`

- variations rapides ou discontinues ;
- durée souvent courte ;
- apparition et disparition fragiles ;
- peut se transformer avant d’être totalement reconnue.

### `STABILITE = EVOLUTIVE`

- transformation progressive ;
- passage entre plusieurs densités ;
- déplacement lent ;
- durée moyenne ou longue.

### `STABILITE = SEDIMENTEE`

- matière relativement stable ;
- évolution lente ;
- peut servir de socle ;
- doit néanmoins disparaître afin de ne pas devenir une ambiance permanente.

---

# 20. Traitements de Reconstruction–Ambiance

## 20.1. Ambiances musicales reconstruites

Traitements possibles selon `MUTABILITE` :

- étirement ;
- changement de hauteur ;
- microboucle ;
- filtrage ;
- répétition irrégulière ;
- déphasage léger ;
- réverbération ;
- delay ponctuel ;
- granularisation ;
- extraction d’une pulsation ;
- suppression progressive de la mélodie ;
- fusion avec voix, souffle ou texture.

### Règle RA3 — Trace musicale

Même fortement transformée, une ambiance musicale peut conserver au moins un indice :

- contour mélodique ;
- rythme ;
- timbre ;
- attaque ;
- voix ;
- ou provenance spatiale.

Si `RECONNAISSABILITE_CIBLE = 1`, cet indice peut être très faible.

## 20.2. Textures reconstruites

Traitements possibles :

- filtrage profond ;
- étirement ;
- gel spectral ;
- découpe ;
- granularisation ;
- modification d’enveloppe ;
- pulsation extraite ;
- déplacement spatial ;
- densification par couches ;
- raréfaction ;
- fusion de plusieurs résidus ;
- perte progressive de fréquences.

### Règle RA4 — Différence avec les field recordings du Cortex

Les textures de Reconstruction–Ambiance peuvent recevoir des traitements profonds. Elles ne sont plus chargées de préserver la continuité documentaire du field recording comme dans Cortex–Ambiance.

Cependant, `TRANSFORMATIONS_AUTORISEES` et `SENSIBILITE_SOURCE` restent prioritaires.

## 20.3. Ambiances hybrides

Une ambiance hybride peut être produite par :

- fondu entre musique et texture ;
- pulsation extraite d’un bruit ;
- voix transformée devenue nappe ;
- résidu urbain accordé avec un fragment musical ;
- fusion dans un buffer.

### Règle RA5 — Hiérarchie interne

Pure Data doit attribuer une présence principale et une présence secondaire. L’hybridation ne doit pas devenir une masse indifférenciée à chaque activation.

---

# 21. Comportements de Reconstruction–Ambiance

Les comportements privilégiés sont :

| Comportement | Fonction |
|---|---|
| `EMERGER` | Faire apparaître progressivement le milieu reconstruit |
| `SOUTENIR` | Maintenir temporairement une forme sans la recouvrir |
| `ENVELOPPER` | Déployer l’ambiance autour d’un noyau localisé |
| `FUSIONNER` | Rejoindre un fragment ou une autre ambiance |
| `MUTER` | Passer progressivement d’un état sonore à un autre |
| `SE_CONDENSER` | Rassembler plusieurs traces en un milieu plus présent |
| `SE_DISPERSER` | Défaire spatialement et spectralement le milieu |
| `LAISSER_TRACE` | Maintenir un résidu après la forme principale |
| `REINJECTER` | Alimenter l’historique, la Reconstruction ou la Boucle |

## 21.1. `EMERGER`

### Règle RA6 — Émergence progressive

L’ambiance entre par un fondu de `1–6 s`, éventuellement précédé d’une seule trace faible.

### Règle RA7 — Émergence depuis un fragment

Une voyelle, un souffle, un bruit ou un motif entendu dans la Reconstruction est prolongé jusqu’à devenir l’ambiance.

**Sensation :** le milieu semble naître de l’intérieur de la forme reconstruite.

## 21.2. `SOUTENIR`

### Règle RA8 — Niveau de soutien

L’ambiance reste généralement `6–15 dB` sous le noyau principal, selon sa densité.

### Règle RA9 — Ducking

Lorsqu’une parole reconnaissable apparaît, Pure Data peut diminuer l’ambiance de `3–9 dB` afin de maintenir une hiérarchie.

## 21.3. `ENVELOPPER`

L’ambiance entoure un noyau spatialement sans être diffusée à niveau égal partout.

- noyau : `1` enceinte ou duo asymétrique ;
- ambiance : `2–4` enceintes à niveaux inégaux ;
- entrée et sortie : progressives.

## 21.4. `FUSIONNER`

### Règle RA10 — Fusion contrôlée

L’ambiance peut fusionner avec :

- une voyelle ;
- un souffle ;
- une texture ;
- un motif musical ;
- une sortie enregistrée dans le buffer.

La fusion avec une parole sémantiquement forte doit préserver son intelligibilité ou empêcher qu’elle soit transformée en faux énoncé.

## 21.5. `MUTER`

### Règle RA11 — Mutation progressive

Pendant `5–30 s`, Pure Data peut modifier progressivement :

- densité ;
- filtre ;
- vitesse ;
- hauteur ;
- granularité ;
- position spatiale ;
- proportion entre les sources.

Une mutation doit conduire d’un état perceptible à un autre, et non faire varier tous les paramètres au hasard.

## 21.6. `SE_CONDENSER`

Plusieurs traces faibles convergent pour former un milieu plus dense.

### Règle RA12 — Limite de densité

Base de test :

- `2–4` couches ;
- une couche principale ;
- pas de quatre couches au même niveau ;
- durée de condensation `3–15 s`.

## 21.7. `SE_DISPERSER`

L’ambiance se défait par :

- éloignement entre les enceintes ;
- diminution des niveaux ;
- perte de fréquences ;
- espacement des grains ;
- disparition successive des couches.

## 21.8. `LAISSER_TRACE`

Après la disparition d’une reconstruction, Pure Data peut conserver :

- un souffle ;
- une résonance ;
- une pulsation faible ;
- une syllabe étirée ;
- une matière filtrée.

Durée indicative de la trace : `2–12 s`, exceptionnellement plus longue si elle évolue.

## 21.9. `REINJECTER`

L’ambiance ou sa trace peut :

- revenir plus tard sous une forme transformée ;
- devenir le socle d’une nouvelle reconstruction ;
- être enregistrée dans le buffer ;
- alimenter la Boucle.

Le nombre de retours doit être limité et inscrit dans l’historique.

---

# 22. Spatialisation de Reconstruction–Ambiance

## 22.1. Modes spatiaux

| `MODE_SPATIAL` | Fonction |
|---|---|
| `LOCALISE` | Trace ou ambiance située sur une enceinte |
| `DUO_DISSYMETRIQUE` | Deux points de présence inégaux |
| `HALO` | Milieu autour d’un noyau |
| `CONVERGENCE` | Plusieurs traces se rassemblent |
| `TRAJET_LENT` | Mutation spatiale entre deux à quatre enceintes |
| `DISPERSION` | Le milieu se défait vers plusieurs points |
| `CONSTELLATION` | Plusieurs sources restent distinctes dans un même milieu |

## 22.2. Nombre d’enceintes

| Type | Base de diffusion |
|---|---|
| `MUSICALE_RECONSTRUITE` | `1–3` enceintes |
| `TEXTURE_RECONSTRUITE` | `2–5` enceintes |
| `HYBRIDE` | `2–4` enceintes |
| Exception développée | jusqu’à `6` enceintes, niveaux inégaux |

### Règle RA13 — Pas d’omniprésence automatique

Les huit enceintes à niveau identique ne doivent pas être utilisées par défaut. Une ambiance totalement diffuse supprimerait la perception de sa formation et de sa transformation.

### Règle RA14 — Relation avec le noyau

L’ambiance doit généralement occuper une position différente de celle du noyau ou l’entourer à plus faible niveau. Si elle converge sur le noyau, ce mouvement doit correspondre à un comportement de fusion ou de reterritorialisation perceptible.

---

# 23. Limites dramaturgiques de Reconstruction–Ambiance

### Règle RA15 — Une ambiance principale

Pure Data doit généralement limiter la scène à :

- une forme reconstruite principale ;
- une ambiance reconstruite principale ;
- éventuellement une trace secondaire faible.

### Règle RA16 — Alternance des fonctions

Reconstruction–Ambiance doit alterner entre :

- absence ;
- socle ;
- enveloppe ;
- transition ;
- résidu.

Elle ne doit pas soutenir toutes les reconstructions de la même manière.

### Règle RA17 — Préservation de l’opacité

L’opacité ne doit pas être traduite uniquement par une accumulation d’effets. Elle provient aussi :

- du maintien de sources distinctes ;
- des intervalles ;
- des fragments qui ne fusionnent pas ;
- des traces dont l’origine reste incertaine ;
- de la transformation partielle ;
- du silence.

---

# 24. Relation entre Reconstruction, Reconstruction–Ambiance et Boucle

## 24.1. Reconstruction vers Reconstruction–Ambiance

Une forme reconstruite peut laisser un fragment, une résonance ou un buffer qui devient ambiance.

## 24.2. Reconstruction–Ambiance vers Reconstruction

Une ambiance peut fournir :

- un socle ;
- une pulsation ;
- une texture de liaison ;
- un résidu servant d’ouverture à une nouvelle forme.

## 24.3. Vers la Boucle

La Boucle n’est pas une piste Ableton supplémentaire. Elle constitue une logique de persistance, de latence et de réactivation.

Elle peut conserver :

- l’identifiant d’un fragment ;
- une recette d’agencement ;
- une trace d’ambiance ;
- ou, si le buffer est implémenté, le résultat sonore d’une reconstruction.

### Règle R56 — Retour non identique

Lorsqu’une forme reconstruite revient, au moins un paramètre peut varier :

- enceinte ;
- délai ;
- niveau ;
- filtrage ;
- durée ;
- nombre d’éléments ;
- reconnaissabilité.

Le retour intact reste possible, mais ne doit pas être la seule variante.

---

# 25. Ordre logique proposé pour Pure Data

```text
1. Charger les métadonnées de Reconstruction et Reconstruction–Ambiance.
2. Charger l’historique récent, les couples utilisés, les formes enregistrées et les compteurs de retours.
3. Choisir TYPE_FORME, DENSITE_COMPOSITION, COURBE_RECONNAISSABILITE,
   MODE_PROVENANCE_FORME, MODE_SPATIAL_COMPOSITION et RESOLUTION_FORME.
4. Définir les rôles nécessaires à la forme.
5. Chercher un premier fragment capable d’occuper le rôle d’entrée ou de noyau.
6. Pondérer sa sélection selon POTENTIEL_COMPOSITIONNEL et l’historique récent.
7. Pour chaque rôle suivant :
   a. constituer la liste des candidats ;
   b. vérifier TYPE_COMPATIBILITE ;
   c. comparer les descripteurs ou COMPATIBLES_AVEC ;
   d. vérifier MODE_PROVENANCE_FORME ;
   e. vérifier SENSIBILITE_SOURCE et CHARGE_SEMANTIQUE ;
   f. exclure les transformations interdites ;
   g. attribuer un score puis choisir aléatoirement parmi les candidats valides.
8. Si aucun candidat n’est trouvé, réduire la forme, insérer un silence ou changer de noyau.
9. Choisir pour chaque jonction : SUTURER, FUSIONNER, SUPERPOSER ou laisser un silence.
10. Choisir les transformations selon MUTABILITE, RECONNAISSABILITE_CIBLE et TRANSFORMATIONS_AUTORISEES.
11. Distribuer les rôles dans l’espace selon MODE_SPATIAL_COMPOSITION.
12. Vérifier les limites de densité, de paroles simultanées et d’enceintes actives.
13. Diffuser la forme en suivant COURBE_RECONNAISSABILITE.
14. Appliquer la résolution : FERMETURE, SUSPENSION, DISSOLUTION ou TRACE.
15. Inscrire les fragments et paramètres réellement utilisés dans l’historique.
16. Si le buffer de Reconstruction est activé, enregistrer la sortie et créer un identifiant temporaire.
17. Décider si une ambiance reconstruite doit apparaître avant, pendant ou après la forme.
18. Pour l’ambiance, appliquer ROLE_AMBIANCE, POTENTIEL_FUSION, STABILITE,
    MUTABILITE, DENSITE et MODE_SPATIAL.
19. Décider si le résultat, la recette ou une trace est REINJECTE dans la Boucle.
20. Laisser SILENCE_APRES_FORME avant une nouvelle activation.
```

---

# 26. Structure du tableau de référencement

## 26.1. Fragments de Reconstruction

| Colonne | Valeurs possibles ou fonction |
|---|---|
| `ID` | Nom du fichier individuel |
| `ZONE` | `RECONSTRUCTION` |
| `TYPE_MATIERE` | `PAROLE` / `VOIX_NON_VERBALE` / `SOUFFLE` / `SON` / `MUSIQUE` / `TEXTURE` / `SILENCE_ENREGISTRE` |
| `GRANULARITE` | Une valeur de la section 2.1 |
| `DUREE_FICHIER_S` | Durée réelle |
| `DUREE_MIN_LECTURE_S` | Durée minimale avant interruption |
| `MODE_LECTURE` | `INTEGRAL` / `EXTRAIT_VARIABLE` / `INTERRUPTIBLE` / `REPETABLE` |
| `PROVENANCE_MATERIAU` | Zone ou source antérieure |
| `SOURCE_ID` | Identifiant d’origine si disponible |
| `CONTEXTE_SOURCE` | `BELGIQUE` / `CONGO` / `DIASPORA` / `INDETERMINE` / autre valeur contrôlée |
| `TYPE_SOURCE` | `FAMILIALE` / `ARCHIVE` / `ADMINISTRATIVE` / `MEDIATIQUE` / `MUSICALE` / autre |
| `ROLE_COMPOSITIONNEL` | Une ou plusieurs valeurs de la section 6 |
| `POTENTIEL_COMPOSITIONNEL` | `1` / `2` / `3` |
| `TYPE_COMPATIBILITE` | Une ou plusieurs valeurs de la section 8 |
| `COMPATIBLES_AVEC` | IDs, groupes ou familles autorisés si méthode B |
| `PHONETIQUE` | Descripteur si pertinent |
| `TIMBRE` | Descripteur si pertinent |
| `RYTHME` | Descripteur si pertinent |
| `ENERGIE` | `FAIBLE` / `MOYENNE` / `FORTE` |
| `CONTENU_SEMANTIQUE` | Mots-clés contrôlés si pertinent |
| `MUTABILITE` | `1` / `2` / `3` |
| `RECONNAISSABILITE_INITIALE` | `1` / `2` / `3` |
| `RECONNAISSABILITE_CIBLE` | `1` / `2` / `3` |
| `CHARGE_SEMANTIQUE` | `FAIBLE` / `MOYENNE` / `FORTE` |
| `SENSIBILITE_SOURCE` | `ORDINAIRE` / `SENSIBLE` / `PROTEGEE` |
| `TRANSFORMATIONS_AUTORISEES` | Liste contrôlée |
| `TRANSFORMATIONS_INTERDITES` | Liste contrôlée |
| `NOMBRE_REPETITIONS_MAX` | Valeur entière |
| `COMPORTEMENTS_AUTORISES` | Liste des comportements de la section 12 |
| `NB_UTILISATIONS_MAX_FENETRE` | Limitation de répétition dans l’historique |
| `COMMENTAIRE_ARTISTIQUE` | Précision exceptionnelle non codée |

## 26.2. Paramètres d’une forme reconstruite

Ces paramètres peuvent être tirés par Pure Data et ne constituent pas nécessairement des colonnes fixes attachées à chaque fichier.

| Paramètre | Valeurs |
|---|---|
| `TYPE_FORME` | quatre valeurs de la section 2.3 |
| `DENSITE_COMPOSITION` | `AEREE` / `MOYENNE` / `DENSE` |
| `COURBE_RECONNAISSABILITE` | `CLAIR_VERS_OPAQUE` / `OPAQUE_VERS_CLAIR` / `OSCILLANTE` / `STABLE` |
| `MODE_PROVENANCE_FORME` | `CONTINUITE` / `CROISEMENT` / `HETEROGENE` / `INDETERMINE` |
| `MODE_SPATIAL_COMPOSITION` | valeurs de la section 14 |
| `RESOLUTION_FORME` | `FERMETURE` / `SUSPENSION` / `DISSOLUTION` / `TRACE` |
| `SILENCE_APRES_FORME` | plage en secondes |
| `ENREGISTREMENT_BUFFER` | `OUI` / `NON` |

## 26.3. Fragments de Reconstruction–Ambiance

| Colonne | Valeurs possibles ou fonction |
|---|---|
| `ID` | Nom du fichier |
| `ZONE` | `RECONSTRUCTION_AMBIANCE` |
| `TYPE_AMBIANCE` | `MUSICALE_RECONSTRUITE` / `TEXTURE_RECONSTRUITE` / `HYBRIDE` |
| `TYPE_FONCTIONNEL` | Une catégorie de la section 18 |
| `ROLE_AMBIANCE` | `SOCLE` / `LIANT` / `ENVELOPPE` / `CONTREPOINT` / `TRANSITION` / `RESIDU` |
| `DUREE_FICHIER_S` | Durée réelle |
| `DUREE_MIN_LECTURE_S` | Durée minimale |
| `MODE_LECTURE` | `INTEGRAL` / `EXTRAIT_VARIABLE` / `INTERRUPTIBLE` / `REPETABLE` |
| `PROVENANCE_MATERIAU` | Une ou plusieurs provenances |
| `POTENTIEL_FUSION` | `1` / `2` / `3` |
| `TYPE_COMPATIBILITE` | Valeurs de la section 19.1 |
| `MUTABILITE` | `1` / `2` / `3` |
| `RECONNAISSABILITE_CIBLE` | `1` / `2` / `3` |
| `DENSITE` | `FAIBLE` / `MOYENNE` / `FORTE` |
| `STABILITE` | `INSTABLE` / `EVOLUTIVE` / `SEDIMENTEE` |
| `NIVEAU_PRESENCE` | `PREMIER_PLAN` / `INTERMEDIAIRE` / `ARRIERE_PLAN` |
| `MODE_SPATIAL` | Valeurs de la section 22 |
| `NB_ENCEINTES_MAX` | Base selon le type d’ambiance |
| `GAIN_RELATIF_DB` | Niveau par rapport au noyau principal |
| `TRANSFORMATIONS_AUTORISEES` | Liste contrôlée |
| `TRANSFORMATIONS_INTERDITES` | Liste contrôlée |
| `COMPORTEMENTS_AUTORISES` | Liste des comportements de la section 21 |
| `SILENCE_APRES` | Plage en secondes |
| `RETOUR_AUTORISE` | `OUI` / `NON` |
| `NOMBRE_RETOURS_MAX` | Valeur entière |

---

# 27. Points à confirmer avant de figer le patch

Ces points ne remettent pas en cause le principe artistique. Ils nécessitent une décision technique ou des tests avec Alassane.

1. Confirmer les noms définitifs des attributs et leur format exact dans le tableau.
2. Décider si `PROVENANCE_MATERIAU` reprend uniquement la zone antérieure ou également la source précise.
3. Choisir entre les descripteurs de compatibilité, une table `COMPATIBLES_AVEC`, ou une combinaison des deux.
4. Tester les scores proposés pour la compatibilité et les poids `1/2/3` du potentiel compositionnel.
5. Définir la fenêtre d’historique empêchant la répétition d’un fragment, d’un couple ou d’un noyau.
6. Confirmer les durées et nombres d’unités des quatre `TYPE_FORME`.
7. Définir les probabilités respectives des densités `AEREE`, `MOYENNE` et `DENSE`.
8. Définir les probabilités des quatre courbes de reconnaissabilité.
9. Définir les probabilités de `CONTINUITE`, `CROISEMENT`, `HETEROGENE` et `INDETERMINE`.
10. Confirmer les nombres maximaux de fragments, de paroles et d’enceintes simultanés.
11. Définir les durées exactes des sutures, fusions, silences et chevauchements après écoute des premiers tests.
12. Confirmer les plages de vitesse, de hauteur et d’étirement supportées par les modules Pure Data disponibles.
13. Définir quels fragments autorisent granularisation, inversion, gel spectral et découpe supplémentaire.
14. Définir les règles spécifiques aux sources `SENSIBLE` et `PROTEGEE`.
15. Décider comment empêcher techniquement la fabrication de fausses déclarations à partir de mots fortement chargés.
16. Confirmer si Pure Data peut enregistrer la sortie de Reconstruction dans un buffer.
17. Si le buffer est possible, définir sa durée maximale, son écrasement, son identifiant et son nombre de retours.
18. Si le buffer n’est pas possible, confirmer que la Boucle conserve les identifiants et la recette de l’agencement.
19. Définir comment une forme passe vers Reconstruction–Ambiance et comment une ambiance peut redevenir socle d’une forme.
20. Définir la règle exacte de réinjection vers la Boucle et les autres zones.
21. Définir les probabilités et durées de `MUTER`, `SE_CONDENSER`, `SE_DISPERSER` et `LAISSER_TRACE`.
22. Confirmer les gains proposés pour `SOUTENIR` et le ducking sous les paroles.
23. Définir les réactions des capteurs piézoélectriques dans Reconstruction et Reconstruction–Ambiance.
24. Décider si une intervention du public peut modifier la densité, la mutabilité, la spatialisation ou seulement provoquer une transition entre zones.
25. Valider la relation générale entre Cortex, Hippocampe, Reconstruction et Boucle après les premiers tests d’écoute.

---

# 28. Synthèse dramaturgique

Le Cortex accumule et superpose des fragments encore rattachés à des contextes.

L’Hippocampe met des mémoires reconnaissables en relation et leur permet d’appeler plusieurs directions.

La Reconstruction transforme les fragments préparés en unités de composition. Elle les agence selon leurs rôles, leurs compatibilités, leur provenance, leur mutabilité et leur reconnaissabilité. Elle produit ainsi une écriture automatique orientée : une forme se crée sans être écrite à l’avance, mais elle n’est jamais abandonnée à un hasard indifférencié.

Reconstruction–Ambiance constitue le milieu provisoire né de cette forme : un socle, une enveloppe, une transition ou un résidu composé de traces musicales, vocales et texturales.

La reterritorialisation devient audible lorsque des fragments auparavant séparés convergent et tiennent momentanément ensemble. Elle demeure toutefois provisoire : la forme se suspend, se dissout, laisse une trace et retourne dans la circulation.

L’installation ne reconstruit donc pas une mémoire belge et congolaise complète ni une identité réconciliée. Elle fait entendre des identités-relations en mouvement, dont certaines connexions deviennent perceptibles tandis que d’autres demeurent opaques.
