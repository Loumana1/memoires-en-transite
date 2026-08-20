> **Document source — texte de Simon Mahungu, conservé tel quel.**
> Ce n'est pas une spec applicable en l'état. Le tri du 20 août a produit **24 questions** dans [`../Backlog/Q&A.md`](../Backlog/Q&A.md) : contradictions avec l'implémentation (carte des 8 HP, durée des ambiances, rôle du piézo) et ambiguïtés bloquantes (règles « à privilégier », tables C2 non symétrique, C9/C10 non discriminantes).
> Ce qui en est clair est dans [`../Backlog/TO DO.md`](../Backlog/TO%20DO.md). Ne rien coder d'ici sans passer par ces deux fichiers. Résumé du tri : [`README.md`](./README.md).

---

# Installation sonore — Attributs et comportements

## Spécifications pour Pure Data — Zones 1 et 2

Ce document décrit les attributs et les comportements des deux premières zones de l’installation :

1. **Cortex**
2. **Cortex–Ambiance**

Il est destiné à permettre leur traduction dans Pure Data.

> **Principe de lecture pour le code**  
> Lorsque le document indique que « Pure Data identifie » un attribut, cela signifie que Pure Data **lit une métadonnée préalablement attribuée au fragment** dans le tableau de référencement. Pure Data n’a pas à analyser lui-même le contenu sonore.

---

# 1. Architecture générale des deux zones

## 1.1. Répartition des enceintes

- **Enceintes 1 à 6 : Cortex**
  - Chaque enceinte diffuse deux fragments de parole superposés.
  - Fragment 1 : parole contextualisée en Belgique.
  - Fragment 2 : parole contextualisée au Congo.
- **Enceinte 7 : Cortex–Ambiance musicale**
- **Enceinte 8 : Cortex–Ambiance texture**

Les enceintes 7 et 8 ne doivent pas être placées l’une à côté de l’autre, afin d’agrandir la perception de l’espace.

## 1.2. Principe dramaturgique général

Dans le Cortex, la superposition d’une parole contextualisée en Belgique et d’une parole contextualisée au Congo crée un contraste entre deux contextes.

Les ambiances musicales et les textures constituent le milieu sonore dans lequel ces paroles apparaissent. Elles ont une fonction esthétique et dramaturgique.

## 1.3. Sensation recherchée

L’écoute des conversations et des monologues ne doit pas être trop nette. Elle doit être **floutée et dissipée**, notamment par l’usage d’un filtre et d’une réverbération donnant l’impression que certaines paroles proviennent d’une pièce voisine.

Cette transformation concerne les **paroles du Cortex**, et non les field recordings de Cortex–Ambiance.

---

# 2. Zone Cortex

## 2.1. Structure sonore

Sur chacune des six enceintes du Cortex :

- deux fragments sont présents ;
- les deux fragments sont superposés ;
- l’un est contextualisé en Belgique ;
- l’autre est contextualisé au Congo ;
- les deux fragments doivent avoir des niveaux de présence différents.

## 2.2. Attributs des fragments

Chaque fragment reçoit plusieurs attributs. Un même fragment peut posséder plusieurs valeurs dans une même catégorie.

Exemple :

- type de discours : `familial` + `politique` ;
- fonction sociale : `raconter` + `témoigner`.

### A. Contexte géographique

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `CONTEXTE` | `BELGIQUE` / `CONGO` |

### B. Type de discours

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `TYPE_DISCOURS` | `FAMILIAL` / `MEDIATIQUE` / `ADMINISTRATIF` / `POLITIQUE` / `DESCRIPTIF` |

`TYPE_DISCOURS` peut contenir une ou plusieurs valeurs.

### C. Fonction sociale

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `FONCTION_SOCIALE` | `NOMMER` / `CLASSER` / `RACONTER` / `TEMOIGNER` / `EXPLIQUER` |

`FONCTION_SOCIALE` peut contenir une ou plusieurs valeurs.

### D. Présence dans le mixage

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `PRESENCE` | `ARRIERE_PLAN` / `INTERMEDIAIRE` / `PREMIER_PLAN` |

La présence n’est pas nécessairement une caractéristique fixe du fichier : elle peut être attribuée ou modifiée par Pure Data au moment de la lecture.

---

## 2.3. Règles obligatoires de sélection

### Règle C1 — Contraste de contexte

Pour chaque enceinte du Cortex, Pure Data doit sélectionner :

- un fragment dont `CONTEXTE = BELGIQUE` ;
- un fragment dont `CONTEXTE = CONGO`.

Il ne doit donc pas superposer deux fragments provenant du même contexte sur une même enceinte.

### Règle C2 — Compatibilité selon le type de discours

Le type de discours du premier fragment détermine les types à privilégier pour le deuxième fragment.

| Type du fragment sélectionné | Types compatibles à privilégier pour le deuxième fragment |
|---|---|
| `FAMILIAL` | `ADMINISTRATIF` ou `DESCRIPTIF` |
| `MEDIATIQUE` | `DESCRIPTIF` ou `FAMILIAL` |
| `ADMINISTRATIF` | `FAMILIAL`, `POLITIQUE` ou `MEDIATIQUE` |
| `DESCRIPTIF` | `FAMILIAL`, `POLITIQUE` ou `MEDIATIQUE` |
| `POLITIQUE` | `ADMINISTRATIF` ou `FAMILIAL` |
| `MEDIATIQUE + POLITIQUE` | `FAMILIAL` |
| `MEDIATIQUE + DESCRIPTIF` | `FAMILIAL` |
| `POLITIQUE + DESCRIPTIF` | `FAMILIAL` |

### Règle C3 — Compatibilité selon la fonction sociale

La fonction sociale du premier fragment détermine les fonctions à privilégier pour le deuxième fragment.

| Fonction du fragment sélectionné | Fonctions compatibles à privilégier pour le deuxième fragment |
|---|---|
| `NOMMER` | `RACONTER` ou `TEMOIGNER` |
| `CLASSER` | `RACONTER` ou `TEMOIGNER` |
| `EXPLIQUER` | `RACONTER` ou `TEMOIGNER` |
| `RACONTER` | `NOMMER` ou `CLASSER` |
| `TEMOIGNER` | `NOMMER` ou `CLASSER` |

### Règle C4 — Fragments possédant plusieurs attributs

Lorsqu’un fragment possède plusieurs types de discours ou plusieurs fonctions sociales, Pure Data peut valider une association dès qu’une combinaison compatible existe entre les attributs des deux fragments.

Exemple : un fragment `FAMILIAL + POLITIQUE` peut être associé à un fragment compatible avec l’une de ces deux valeurs.

> **Point à confirmer pour la version finale du code :** lorsqu’une compatibilité existe à la fois sur le type de discours et sur la fonction sociale, faut-il favoriser cette double compatibilité, ou les deux axes doivent-ils rester indépendants et de poids égal ?

---

## 2.4. Règles de présence et de densité

### Règle C5 — Présences différentes

Les deux fragments superposés sur une même enceinte doivent toujours avoir des niveaux de présence différents.

Combinaisons possibles :

- `PREMIER_PLAN` + `ARRIERE_PLAN` ;
- `PREMIER_PLAN` + `INTERMEDIAIRE` ;
- `INTERMEDIAIRE` + `ARRIERE_PLAN`.

### Règle C6 — Opposition entre fonctions

Lorsqu’un fragment `CLASSER` ou `NOMMER` est superposé à un fragment `RACONTER` ou `TEMOIGNER` :

- l’un doit être au premier plan ;
- l’autre doit être à l’arrière-plan.

### Règle C7 — Variation des plans

Pure Data doit intervertir les rôles au fil des occurrences :

- parfois le premier fragment est au premier plan et le deuxième à l’arrière-plan ;
- parfois le premier fragment est à l’arrière-plan et le deuxième au premier plan.

Cette variation vaut également pour les types de discours `FAMILIAL`, `ADMINISTRATIF`, `POLITIQUE`, `MEDIATIQUE` et `DESCRIPTIF`.

### Règle C8 — Limitation de la densité

Pure Data ne peut pas placer deux fragments de parole très denses au même niveau de présence.

Une parole contextualisée en Belgique et une parole contextualisée au Congo ne doivent donc jamais être simultanément au premier plan si toutes les deux sont très denses.

> **Donnée nécessaire dans le tableau :** pour automatiser cette règle, chaque fragment devra recevoir un attribut supplémentaire, par exemple `DENSITE_PAROLE = FAIBLE / MOYENNE / FORTE`.

---

## 2.5. Comportements temporels des paroles

Deux comportements principaux sont prévus :

| Comportement | Description fonctionnelle |
|---|---|
| `EMERGER` | Le deuxième fragment apparaît progressivement au-dessus du premier. |
| `RECOUVRIR` | Le deuxième fragment augmente progressivement sa présence jusqu’à masquer partiellement ou fortement le premier. |

### Règle C9 — Comportements selon la fonction sociale

| Fonction du fragment de départ | Fonction du deuxième fragment | Comportement du deuxième fragment |
|---|---|---|
| `RACONTER` ou `TEMOIGNER` | `CLASSER`, `NOMMER` ou `EXPLIQUER` | `EMERGER` ou `RECOUVRIR` |
| `EXPLIQUER` | `RACONTER` ou `TEMOIGNER` | `EMERGER` ou `RECOUVRIR` |

### Règle C10 — Comportements selon le type de discours

| Type du fragment de départ | Type du deuxième fragment | Comportement du deuxième fragment |
|---|---|---|
| `FAMILIAL` | `ADMINISTRATIF` ou `DESCRIPTIF` | `EMERGER` ou `RECOUVRIR` |
| `MEDIATIQUE` | `DESCRIPTIF` ou `FAMILIAL` | `EMERGER` ou `RECOUVRIR` |
| `ADMINISTRATIF` ou `DESCRIPTIF` | `FAMILIAL`, `POLITIQUE` ou `MEDIATIQUE` | `EMERGER` ou `RECOUVRIR` |
| `POLITIQUE` | `ADMINISTRATIF` ou `FAMILIAL` | `EMERGER` ou `RECOUVRIR` |

### Règle C11 — Variation des comportements

Pure Data doit varier :

- le fragment qui émerge ou recouvre l’autre ;
- le fragment placé au premier plan ;
- le fragment placé à l’arrière-plan.

La variation doit être interchangeable : un même type de fragment ne doit pas toujours occuper la même position hiérarchique.

> **Paramètres encore à fixer :** durées de fondu pour `EMERGER` et `RECOUVRIR`, niveau maximal du fragment qui recouvre, durée de coexistence et probabilités respectives des deux comportements.

---

## 2.6. Traitements sonores du Cortex

### Traitements recherchés

- filtre donnant une sensation de distance ;
- réverbération donnant l’impression d’une parole provenant d’une pièce voisine ;
- niveaux de présence différenciés ;
- résultat global flouté et dissipé.

### Problème constaté lors des essais

Les conversations et les monologues restent encore trop clairement intelligibles. Les réglages du filtre et de la réverbération doivent donc accentuer la sensation de distance.

---

# 3. Zone Cortex–Ambiance

## 3.1. Fonction générale

Cortex–Ambiance accompagne les fragments de parole du Cortex. Cette zone ne constitue pas une nouvelle couche de discours : elle forme le milieu sonore dans lequel les souvenirs et les paroles apparaissent.

Deux familles d’ambiances doivent être distinguées :

1. `AMBIANCE_MUSICALE` ;
2. `AMBIANCE_TEXTURE`.

## 3.2. Répartition spatiale

| Enceinte | Contenu | Fonction |
|---|---|---|
| 7 | Ambiance musicale | Accompagner dramaturgiquement les paroles Belgique/Congo. |
| 8 | Ambiance texture | Installer une matière environnementale autour des paroles Belgique/Congo. |

Les deux enceintes ne sont pas côte à côte, afin d’élargir l’espace sonore.

## 3.3. Durée

Tous les fragments d’ambiance musicale ou de texture durent entre **30 secondes et 7 minutes**.

| Nom de l’attribut | Valeurs possibles |
|---|---|
| `DUREE` | de `30 s` à `7 min` |

---

## 3.4. Attributs des ambiances musicales

Les ambiances musicales sont des field recordings ou des ambiances esthétiques ayant une fonction dramaturgique.

| Catégorie | Nom de l’attribut | Valeurs possibles |
|---|---|---|
| Famille | `TYPE_AMBIANCE` | `MUSICALE` |
| Activité | `ACTIVITE` | `CALME` / `MOYENNE` |
| Continuité | `CONTINUITE` | `STABLE` / `EVOLUTIVE` |
| Espace | `ESPACE` | `EXTERIEUR` |
| Présence humaine | `PRESENCE_HUMAINE` | `ABSENTE` |

Lorsque `ESPACE = EXTERIEUR`, l’ambiance n’est pas filtrée.

## 3.5. Attributs des ambiances textures

Les ambiances textures peuvent contenir notamment : rues, transports, marché, pluie, eau, escalator, métro, environnement congolais ou environnement bruxellois/belge.

| Catégorie | Nom de l’attribut | Valeurs possibles |
|---|---|---|
| Famille | `TYPE_AMBIANCE` | `TEXTURE` |
| Activité | `ACTIVITE` | `MOYENNE` / `FORTE` |
| Continuité | `CONTINUITE` | `EVENEMENTIELLE` / `STABLE` |
| Espace | `ESPACE` | `EXTERIEUR` / `INDETERMINE` |
| Présence humaine | `PRESENCE_HUMAINE` | `IDENTIFIABLE` / `DIFFUSE` |

Lorsque `ESPACE = EXTERIEUR`, l’ambiance n’est pas filtrée.

---

## 3.6. Comportements des ambiances

### Ambiance musicale

| Valeur du comportement | Description |
|---|---|
| `RESTER` | L’ambiance demeure stable pendant sa période de lecture. |
| `EMERGER` | L’ambiance apparaît progressivement. |
| `RECOUVRIR` | L’ambiance augmente progressivement jusqu’à recouvrir partiellement les paroles du Cortex. |

### Ambiance texture

| Valeur du comportement | Description |
|---|---|
| `SE_DEPLACER` | La texture circule dans l’espace sonore. |
| `RECOUVRIR` | La texture augmente progressivement jusqu’à recouvrir partiellement les paroles du Cortex. |

> **Paramètres encore à fixer :** vitesse et trajectoire de `SE_DEPLACER`, durées de fondu, niveau maximal de recouvrement et probabilités de chaque comportement.

---

## 3.7. Traitements interdits sur les ambiances

Pour les ambiances musicales et les textures, éviter :

- le delay ;
- les découpes rapides ;
- la fragmentation granulaire.

Les ambiances doivent conserver leur continuité, car elles constituent le milieu dans lequel les autres souvenirs apparaissent.

---

## 3.8. Action des capteurs piézoélectriques

Les capteurs piézoélectriques servent à arrêter l’ambiance afin de permettre le passage d’une zone à une autre.

### Événement à prévoir dans Pure Data

```text
SI piezo_declenche = vrai
ALORS arrêter Cortex–Ambiance
ET permettre le passage vers une autre zone
```

> **Paramètres encore à fixer :** seuil de déclenchement du piézo, arrêt immédiat ou fondu de sortie, durée du fondu éventuel, zone activée ensuite et délai avant qu’une ambiance puisse réapparaître.

---

# 4. Ordre logique proposé pour Pure Data

```text
1. Charger les métadonnées de tous les fragments.
2. Choisir une enceinte du Cortex parmi les enceintes 1 à 6.
3. Sélectionner un fragment CONTEXTE = BELGIQUE.
4. Chercher un fragment CONTEXTE = CONGO compatible :
   a. selon TYPE_DISCOURS ;
   b. selon FONCTION_SOCIALE.
5. Vérifier la densité des deux paroles.
6. Attribuer deux niveaux de PRESENCE différents.
7. Choisir le comportement EMERGER ou RECOUVRIR.
8. Appliquer les traitements de distance aux paroles.
9. Lire une ambiance musicale sur l’enceinte 7.
10. Lire une ambiance texture sur l’enceinte 8.
11. Maintenir la continuité des ambiances sans delay ni fragmentation rapide.
12. Si un piézo est déclenché, arrêter Cortex–Ambiance et autoriser le passage vers une autre zone.
```

---

# 5. Structure du tableau de référencement

## 5.1. Fragments du Cortex

| ID | Durée-type | Contexte | Type de discours | Fonction sociale | Densité de parole | Traitement ou comportement autorisé |
|---|---|---|---|---|---|---|
| `C002_V3_cortex.wav` | `COURT` | `CONGO` | à renseigner | à renseigner | à renseigner | à renseigner |

## 5.2. Fragments de Cortex–Ambiance

| ID | Type d’ambiance | Durée | Activité | Continuité | Espace | Présence humaine | Comportements autorisés |
|---|---|---|---|---|---|---|---|
| à renseigner | `MUSICALE` ou `TEXTURE` | `30 s–7 min` | à renseigner | à renseigner | à renseigner | à renseigner | à renseigner |

---

# 6. Points à confirmer avant de figer le patch

Ces points ne modifient pas le principe artistique, mais nécessitent une valeur ou une règle supplémentaire pour que le comportement soit entièrement déterminé dans Pure Data :

1. Définir la priorité entre `TYPE_DISCOURS` et `FONCTION_SOCIALE` lorsqu’ils proposent des associations différentes.
2. Définir si une double compatibilité doit augmenter la probabilité de sélection d’une paire.
3. Ajouter et renseigner l’attribut `DENSITE_PAROLE`.
4. Fixer les probabilités de `EMERGER` et `RECOUVRIR`.
5. Fixer les durées de fondu et les niveaux correspondant aux trois plans de présence.
6. Définir si les enceintes 7 et 8 peuvent recouvrir les paroles simultanément.
7. Définir la trajectoire spatiale de `SE_DEPLACER` pour les textures.
8. Définir précisément la réaction au piézo et la zone appelée ensuite.

