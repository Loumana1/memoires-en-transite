# Mémoires en transit
**Installation sonore** — Centre Wallonie-Bruxelles, Paris — 11 septembre
*Document de travail évolutif — à compléter et modifier ensemble*

**Légende des couleurs/intervenants :**
* **Vert :** Alassane (Concept, Composition, Sound Design)
* **Bleu :** Simon (Architecture système, Développement technique)

---

## 1. Concept artistique
Mémoires en transit propose une expérience immersive où la mémoire est envisagée comme un processus instable, fragmenté et en constante recomposition.
L’installation articule :
* des archives sonores (Quai Branly, BnF)
* des enregistrements de terrain contemporains

Ces matériaux, hétérogènes par nature (historiques, intimes, médiatiques), ne sont pas unifiés mais mis en tension : ils s’enchevêtrent, se contaminent et produisent un récit non linéaire.
Le temps y est :
* superposé
* contradictoire
* impossible à saisir dans sa totalité

L’expérience sonore est donc ancrée dans le présent de l’écoute.

## 2. Ancrage conceptuel
La relation entre la Belgique et le Congo constitue un socle de recherche.
Le son est utilisé comme médium central car il permet :
* de traverser les frontières
* d’activer la mémoire
* d’engager physiquement le corps

L’installation interroge ainsi la mémoire, l'identité et la transmission.

## 3. Positionnement du médium
Le médium de l’œuvre ne réside pas dans les sons eux-mêmes, mais dans :
* leur mise en relation algorithmique
* leur organisation spatiale
* leur circulation en temps réel

Il s’agit d’un son pensé par et dans un système numérique, où :
* la technologie structure la forme
* la spatialisation structure la perception
* l’algorithme structure le sens

L’œuvre produit une écoute instable, hybride et transnationale.

## 4. Dispositif spatial
* **Salle :** Black Box (~14 m²)
* **Diffusion :** 12 haut-parleurs

Organisation inspirée du cerveau (sans dimension didactique) :
* cortex (réception)
* hippocampe (association)
* mémoire reconstructive
* boucles neuronales

Le cerveau est ici envisagé comme un système de circulation, un filtre et une zone de friction. La mémoire y apparaît comme opaque, filtrée et instable.

## 5. Comportement sonore (logique du système)
Le système sonore doit permettre l'apparition, la transformation, la répétition, la disparition et la circulation.
Les sons circulent comme dans un réseau :
* ils émergent
* se transforment
* disparaissent
* réapparaissent ailleurs

→ La mémoire est un processus, pas un stockage.

## 6. Interaction avec le public
Le corps du visiteur n’est ni utilisateur ni acteur volontaire. 
→ **Il est une interférence involontaire.**

Sa présence :
* perturbe le système
* modifie les flux
* sans jamais les contrôler

Cela reflète le fonctionnement réel de la mémoire.

---

## 7. Système technique

**Environnement de développement**
> **[Simon] : Pure Data (Pd).**
> Pure Data est le garant d'un système extrêmement résilient, sans surcoût de licence, et parfait pour la logique modulaire (fichiers audio pilotés par une machine d'état stochastique). Le développement se fera sur PC dans un premier temps, avec une migration finale sur carte embarquée.
> *→ Réponse : Pure Data pour une flexibilité totale et la transportabilité du code Linux.*

**Spatialisation**
> **[Simon] : Matrice de Routing Dynamique.**
> L'idée est d'abandonner la lourdeur de l'Ambisonics pour une horloge globale couplée à des comportements locaux sur les baffles : la machine à état distribuera le signal de manière dynamique sur les 12 sorties (panning entre HP adjacents, clusters aléatoires). 
> *→ Réponse : Pragmatique, rythmique et beaucoup moins lourd pour le CPU.*

**Architecture de l’algorithme**
> **[Simon] : Machine à États (FSM) & Lecteurs Samplers Locaux.**
> Les zones (Cortex, etc.) représenteront des "états". 4 à 8 lecteurs virtuels piocheront dynamiquement dans les dossiers audio. Une logique de probabilités (modifiée par l'analyse micro) définira les transitions.

**Interaction / captation**
> **[Simon] : Analyse de l'amplitude RMS et des transitoires.**
> On reste simple et robuste : détection de nervosité (mouvements bruyants) et de latence (silence, immobilité) via le spectre d’ambiance.

**Support de diffusion (ordinateur / système autonome)**
> **[Simon] : Raspberry Pi 5.**
> Un nano-ordinateur bootant en « Headless » (ligne de commande Linux) au démarrage. Résistance parfaite aux coupures de courant (redémarrage sans friction à l'allumage physique de l'électricité). L'appareil sera caché ou accroché derrière un baffe.
> *→ Réponse : Machine autonome « Solid State », aucune interface utilisateur sur le site d'exposition.*

---

## 8. Matériel (Prévisions) & Budget

* **Budget alloué :** Entre 500 € et 1 000 € pour l'informatique et les cartes son (le centre finance l'intégralité).
* **Environnement de développement :** Pure Data (Open Source - Gratuit).
* **Diffusion :** 12 Haut-parleurs actifs (Fournis ou loués par la salle).
* **Interaction / captation :** 2 microphones omnidirectionnels ou cardioïdes.
* **Support de diffusion :** 
  * Matériel central : **Raspberry Pi 5** (avec OS sur carte MicroSD / SSD).
  * Interface audio USB : Carte gérant 12+ sorties sous Linux Class-Compliant (Ex: **Focusrite Scarlett 18i20** avec extension ADAT, ou carte MOTU).

---

## 9. Logique mémorielle du système (Rappel)
Organisation en 4 dynamiques :
1. **Réception (cortex)** → sons bruts, saturation, afflux d’informations
2. **Association (hippocampe)** → fragments qui dialoguent, reconnaissance partielle
3. **Reconstruction** → transformation, déformation, mémoire instable
4. **Boucle** → réapparition, disparition, circulation continue

→ Écoute non linéaire.

## 10. Interaction corporelle — logique simplifiée
Le système repose sur une captation minimale :
* microphones d’ambiance
* analyse d’énergie sonore
* détection d’activité globale

Sont volontairement exclus : la reconnaissance vocale, l'identification, le tracking précis.

## 11. Règles comportementales (principes)
* **Présence / densité :** Forte présence → saturation ou clarification. Excès → perte de sens.
* **Immobilité :** Favorise émergence d’archives, permet consolidation mémorielle.
* **Mouvement rapide :** Rupture des liens, retour au bruit, fragmentation.
* **Position spatiale :** Centre → saturation. Bords → filtrage. Coins → résonance.

---

## 12. Questions structurantes (Résolutions)

**1. Évolution du prototype**
> **[Simon] :** Oui. Le patch Max sera configuré avec l'objet `folder` pour scanner les répertoires en temps réel. Tu pourras injecter de nouveaux sons la veille du vernissage ou un an plus tard, le système s'occupera d'instancier les mémoires de manière organique. C'est un **système totalement ouvert**.

**2. Mémoire sonore cumulative (dimension écologique)**
> **[Simon] :** Oui. Le système aura un module "Enregistreur fantôme". Lors de moments d'intérêt ou avec une routine très lente (par ex. tous les 50000 ms), il capte l'acoustique sèche de la pièce + des bouts du système, le découpe, et le dépose sans intervention humaine dans le dossier `MEMOIRE_VIVANTE/` pour l'insérer dans les boucles à venir.

---

## 13. Planning et Diffusions

**Échéances de diffusion :**
* **Exposition 1 (11 Septembre) :** Centre Wallonie-Bruxelles (Paris). Représentation unique de **24h**. 
* **Exposition 2 (Novembre) :** Musée des Beaux-Arts / Bozar (Bruxelles). Représentation en continu sur **5 jours de suite**.

**Calendrier de Développement :**
* **Mai / Juin :** Cadrage technique, choix matériels, prototypage de la boucle noyau dans **Pure Data** (sur PC).
* **Fin juin :** Tests d'interaction micro et programmation de la Machine à États (cortex, hippocampe, reconstruction).
* **Fin juillet :** Migration du patch sur **Raspberry Pi**, tests sur interface audio 12 sorties, validations de la robustesse (tests de redémarrage après coupure).
* **Août :** Travail esthétique, remplissage des dossiers et arborescences (avec les *vrais* buffers audio de ton sound design).
* **Début septembre :** Installation au CWB Paris, étalonnage de l'amplitude selon l'acoustique sèche/humide du lieu.
* **Novembre :** Re-déploiement automatisé au Bozar pour l'expo de 5 jours.

---

## 14 à 24. Processus de création des matériaux sonores (Charte Alassane)

Les points 14 à 24 du manifeste sont actés. La préparation rigoureuse par catégories temporelles et par états psychiques (Cortex/Hippocampe/Reconstruction/Boucle) va permettre un développement informatique quasi granulaire, avec une correspondance directe `Durée ↔ Comportement`.

**Arborescence de travail confirmée :**
```text
SONS/
├── CORTEX/ (LONG/ MOYEN/ COURT/)
├── HIPPOCAMPE/ (LONG/ MOYEN/ COURT/)
├── RECONSTRUCTION/ (LONG/ MOYEN/ COURT/)
├── BOUCLE/ (LONG/ MOYEN/ COURT/)
└── MEMOIRE_VIVANTE/
```
Un son n’est pas un fichier, mais un *comportement potentiel*. L’installation ne diffuse pas des sons, elle organise leur circulation.
