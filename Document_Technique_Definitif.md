# Cahier des Charges Technique & Décisions (Document Définitif)

Ce document acte les **décisions finales** prises pour l'installation "Mémoires en transit". Il fait suite aux documents de recherche initiaux. Il fige l'architecture matérielle, logicielle, budgétaire, spatiale et calendaire.

---

## 1. Calendrier des Expositions

L'installation a deux temporalités et espaces de diffusion confirmés :
1. **11 Septembre 2026** : Centre Wallonie-Bruxelles (Paris).
   * **Durée** : Exposition éphémère (24 heures).
2. **Novembre 2026** : Musée des Beaux-Arts / Bozar (Bruxelles).
   * **Durée** : Exposition en continu (5 jours de suite).

---

## 2. Choix Matériel (Hardware)
**Budget alloué par le centre :** Entre **500 € et 1 000 €** (financement technique assuré).

* **Cerveau Central : Raspberry Pi 5**
  * Objectif : Système "Solid State", totalement autonome et transportable d'une exposition à l'autre sans dépendre d'un ordinateur personnel. Résistance absolue aux coupures de courant (se rallume tout seul au branchement physique).
* **Carte Son (Interface Audio) :**
  * Une interface USB certifiée "Class-Compliant" (reconnue nativement par Linux sans driver).
  * Référence retenue : Focusrite Scarlett 18i20 (8 sorties analogiques suffisent pour l'installation).
* **Diffusion :**
  * **8 baffles actifs** (fournis ou loués par la salle / budget scénographie). Carte Simon : **6 baffles de parole + 2 baffles d'ambiance** (non adjacents).
* **Captation :**
  * 2 microphones d'ambiance discrets (omnidirectionnels ou cardioïdes) ; piézos en complément selon la salle.

---

## 3. Choix Logiciel (Software)

* **Environnement de développement : Pure Data (Pd)**
  * **Phase 1 :** Le développement et le sound design seront faits sur l'ordinateur de travail principal (PC/Mac) pour bénéficier de l'interface visuelle.
  * **Phase 2 :** Migration finale sur le Raspberry Pi où Pure Data tournera sans écran graphique ("Headless") pour optimiser 100% de la puissance processeur sur l'audio.

### Spatialisation : L'équivalent de "Spat5" dans Pure Data
Il ne s'agit pas de revoir l'ambition spatiale à la baisse. Le panning organique de type "Spat" est totalement réalisable dans Pure Data.
* **L'outil retenu : `iem_ambi` (La librairie IEM Ambisonics).**
  * Développée par l'Institut d'Électroacoustique de Graz, c'est l'étalon-or de l'Ambisonics open-source.
  * Tout comme Spat5, elle permet de détacher le son du baffle et de faire « tourner » ou « diffuser » une masse sonore dans l'espace des **8 haut-parleurs** via un encodeur/décodeur Ambisonique (ordre 1 / 2D).
  * En Cortex, les paroles sont ancrées **directement** sur les baffles ; l'ambisonics sert surtout Hippocampe / Reconstruction / Boucle, plus des gestes spatiaux momentanés (voyage phi, échange avant/arrière).

### Architecture Algorithmique
* **Moteurs de Lecture (`readsfs~` / Arrays) :** Plusieurs lecteurs piocheront dynamiquement les fichiers `.wav` structurés dans les sous-dossiers (Court / Moyen / Long).
* **Machine à États Probabiliste (FSM) :** Une horloge interne déclenchée et perturbée par le détecteur de mouvement (transitoires et RMS des micros) choisira le transfert des sons entre le CORTEX, l'HIPPOCAMPE et la BOUCLE.
* **Mémoire fantôme :** Sauvegarde ponctuelle (via l'objet `writesf~`) de la résonance du réseau vers le dossier `MEMOIRE_VIVANTE`. 

---

## 4. Planning de Production

* **Mai - Juin :** Cadrage technique. Configuration de l'environnement Pure Data (PC). Prototypage du moteur de spatialisation Ambisonics (IEM) ou VBAP sur un réseau de speakers virtuels.
* **Fin Juin :** Finalisation de l'algorithme "Machine à États" (probabilités, temps, triggers micro).
* **Fin Juillet :** Migration du patch fonctionnel sur le Raspberry Pi. Déploiement sur la vraie carte son (**8 canaux**). Tests de stress (coupures de courant).
* **Août :** Remplissage des serveurs avec les matériaux sonores définitifs (Field recordings, Quai Branly, BnF). Mixage et paramétrages des ambiances.
* **Début Septembre :** Déploiement in situ au **CWB Paris**, calibration précise de la salle.
* **Novembre :** Redéploiement (plug & play) au **Bozar, Bruxelles**.
