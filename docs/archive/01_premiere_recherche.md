# Première recherche — Options d'Architecture Autonome & Déconnectée

> **Statut :** Archive de la phase exploratoire initiale (avril 2026).  
> Les décisions actuelles pour le prototype sont dans [`02_prototype_01_decisions_et_plan.md`](./02_prototype_01_decisions_et_plan.md).  
> Documents connexes de la même période : `Document_de_travail_evolutif.md`, `Document_Technique_Definitif.md`.

Ce document explore les pistes d'une installation 100% autonome, résiliente aux pannes de courant, facile à allumer/éteindre (littéralement en branchant/débranchant la prise) et explorant les alternatives logicielles telles que **Pure Data** et **SuperCollider** fonctionnant sur un nano-ordinateur (**Raspberry Pi**).

---

## 1. Démystification : "Et s'il y a une coupure de courant ?"

Avant de parler du Raspberry Pi, il est important de noter une chose cruciale sur l'ordinateur de l'option précédente : **Un Mac Mini (ou un PC) peut parfaitement redémarrer tout seul après une coupure de courant.** 
* Sur Mac : `Réglages Système > Économie d'énergie > "Démarrer automatiquement après une panne de courant"`.
* En réglant la session sans mot de passe et le patch Max en "Ouverture automatique" avec un objet `loadbang` pour régler le volume/lancer le son, un Mac Mini agit *exactement* comme un objet autonome. Tu branches la prise murale, et en 25 secondes l'œuvre joue.

**Cependant**, l'approche "Nano-ordinateur" (Raspberry Pi) a énormément de charme dans une démarche d'Arts Numériques / Installation : c'est minuscule, ça ne coûte que ~100€, ça chauffe peu et le système Linux peut être optimisé au maximum.

---

## 2. Le Hardware : Brancher 12 baffles sur un Raspberry Pi

Oui, un Raspberry Pi peut envoyer du son vers 12 baffles. Le Raspberry n'a pas de sorties audio multiples natives (juste une prise casque de mauvaise qualité), il faut donc le relier à une **Carte Son / Interface Audio** externe.

**Le cheminement du son :**
`Raspberry Pi (via port USB 3.0) ➔ Interface Audio USB (Class Compliant) ➔ 12 Baffles actifs`

**Les Interfaces Audio compatibles Linux (Class Compliant)** :
Pour avoir 12 sorties analogiques (pour tes 12 haut-parleurs), le standard est de prendre :
1. Une interface de base avec 8 sorties + port ADAT (Ex: **Focusrite 18i20** mk3 ou mk4).
2. Un convertisseur ADAT pour ajouter 8 autres sorties (Ex: **Behringer ADA8200** ou OctoPre).
3. Connecté au Raspberry en USB, l'outil audio sous Linux (ALSA / JACK) verra directement 16 sorties disponibles.

---

## 3. Comparatif des Logiciels (Software)

Puisque Max/MSP n'existe pas sur Linux/Raspberry Pi, nous avons 3 approches pour une box autonome :

### Option A : Pure Data (Pd) - L'Héritier direct
* **Comment ça marche ?** C'est le cousin open-source de Max/MSP. Programmation visuelle par "boîtes" et "câbles".
* **Avantages pour ton projet :** 
  * Très léger. Sur Raspberry Pi, on le lance "Headless" (sans interface graphique, ligne de commande `pd -nogui`) = l'ordinateur utilise toute sa puissance pour l'audio.
  * Il peut tout à fait lire des dossiers dynamiquement.
  * Extrêmement fiable sur des mois d'installation continue.
* **Spatialisation :** Comme conseillé par l'autre IA, on abandonne "l'Ambisonics" complexe pour un simple **Routing Dynamique (Matrice de mixage locale)**. On utilise une horloge globale dans Pd, et des probabilités envoient les fragments aléatoirement sur la sortie cible (1 à 12), ou effectuent des panoramiques simples (VBAP) entre 2 sorties proches.
* **Verdict : C'est le choix n°1 si tu optes pour le Raspberry Pi.** C'est simple à programmer si tu aimes l'approche visuelle (comme un studio d'enregistrement virtuel).

### Option B : SuperCollider - La puissance générative
* **Comment ça marche ?** Programmation par balises de code (texte). Pas de boîtes.
* **Avantages pour ton projet :** 
  * Imbattable intellectuellement pour créer des logiques "génératives" et stochastiques (Chaînes de Markov pour le passage Cortex -> Hippocampe).
  * Consomme encore moins de ressources système. Il sépare le langage (`sclang`) du serveur de synthèse (`scsynth`), ce qui est ultra-résilient.
* **Verdict : Parfait si on souhaite une structure 100% comportementale et algorithmique.** L'apprentissage est beaucoup plus difficile que Pure Data (car 100% code), mais le pilotage de 12 sorties indépendantes avec des horloges aléatoires ne prend que quelques lignes de code.

---

## 4. Architecture de la Boucle Système ("Machine à États")

Que ce soit sur Pure Data ou SuperCollider, le système serait ainsi :

**1. Moteur de Détection (Trigger)** -> L'entrée Micro (branchée sur la carte son) écoute. Un simple algorythme d'Envelope Follower détecte RMS/Pics.
**2. Moteur de Décision (State Machine)** -> Horloge globale. En fonction du RMS (silence, foule, etc.), elle modifie ses pourcentages. (Ex: Si RMS haut -> 80% de chance de passer en état "Reconstruction").
**3. Moteur Joueur (Samplers locaux)** -> 4 à 8 lecteurs audio virtuels tournent en permanence, piochant dans les dossiers. 
**4. Pile d'Effets (FX Bank)** -> Des délais, filtres passe-haut, bitcrusher. L'envoi ("Send") vers ces effets dépend de la décision de l'étape 2. Aucun effet n'est généré aléatoirement : on contrôle simplement le volume du "Send" (envoi) vers chaque effet de la banque selon l'état du système.
**5. Moteur Mémoriel (Grabber)** -> Une simple boucle de 10 secondes qui attrape la sortie de la machine + le mix du micro, et l'exporte sur la carte SD du Raspberry avec date du jour.

---

## 5. Bilan des approches

### **Stratégie 1 : Facilité de programmation + Puissance Pure (Mon Conseil Global)**
* **Matériel :** Mac Mini (Démarrage Auto sur alimentation) caché en régie.
* **Logiciel :** Max/MSP (Interface visuelle facile à déboguer en temps réel).
* **Routing :** Spat5 ou Matrice croisée.

### **Stratégie 2 : Autonomie, Bidouille et Robustesse Maker (La piste que tu explores)**
* **Matériel :** Raspberry Pi 5 + Focusrite 18i20 (connectée en USB).
* **Logiciel :** Pure Data. 
* **Comment l'allumer :** Un script Linux (`crontab` ou `systemd`) lance Pure Data avec le patch au démarrage pendant le boot du système d'exploitation. Tu branches la multiprise, la salle s'anime 30 secondes plus tard.
* **Routing :** Routine matricielle maison (des fades de volumes gérés de manière aléatoire sur la grille des 12 sorties). Moins organique que Spat5, mais beaucoup plus incisif et "rythmique" dans l'espace.

---
**💡 Dis-moi si cette vue d'ensemble avec Pure Data / Raspberry Pi résonne mieux pour le projet ! Si oui, je mettrai notre plan d'implémentation formel à jour avec cette infrastructure logicielle.**
