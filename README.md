# Mémoires en transit / Micro-opacités

**Installation sonore générative · Pure Data · Raspberry Pi**  
Par Loumana · En développement actif (2026)

## À propos

*Mémoires en transit / Micro-opacités* est une installation sonore immersive qui explore les mécanismes de la mémoire à travers des fragments d'archives orales. Le système génératif compose en temps réel une expérience spatiale et temporelle à partir d'extraits de récits personnels, créant une cartographie sonore de la mémoire en mouvement.

L'installation utilise un système à machine d'états finis (FSM) qui orchestre différentes zones de mémoire — **Cortex**, **Hippocampe**, **Reconstruction**, **Boucle** — chacune avec ses propres caractéristiques sonores et spatiales.

⚠️ **Ce projet est en développement actif.** Le code, la documentation et les algorithmes évoluent constamment. La version actuelle (Proto 07/08) est déployée au [Centre Wallonie-Bruxelles à Paris](https://cwb.fr/).

## Architecture technique

- **Pure Data** : moteur audio temps réel
- **Python** : génération de patches et traitement de matière sonore
- **Raspberry Pi** : déploiement autonome (8 HP ou stéréo casque)
- **Spatialisation** : ambisonic 2D (8 HP) ou binaural HRTF (casque)
- **Matière sonore** : fragments d'archives orales (voix, ambiances)

## Documentation

La documentation complète du projet est disponible dans [`docs/`](docs/) :

- **[État actuel du projet](docs/etatactuel.md)** : vue d'ensemble de la version en cours
- **[Zones de mémoire](docs/Zones/)** : description des différents états du système
- **[Pipeline de traitement](docs/Matiere/Pipeline.md)** : workflow de la matière sonore
- **[Journal de développement](docs/log.md)** : historique des décisions et évolutions
- **[Backlog & TODO](docs/Backlog/)** : tâches en cours et questions ouvertes

## Utilisation rapide

### Sur ordinateur (développement)

```bash
# Proto 07 (8 HP)
bash scripts/launch_prototype_07_8hp.sh

# Proto 07 Stéréo (casque)
bash scripts/launch_prototype_07_stereo.sh

# Proto 08 (8 HP)
bash scripts/proto08/launch_prototype_08_8hp.sh
```

### Déploiement Raspberry Pi

Voir [`deploy/debian/README.md`](deploy/debian/README.md) pour les instructions complètes :

```bash
bash deploy/debian/install.sh      # installation des dépendances
bash deploy/debian/launch.sh       # lancement du patch
```

## Structure du dépôt

```
memoires-en-transit/
├── pd/                    # Patches Pure Data
│   ├── lib/              # Abstractions et modules
│   └── prototype_*.pd    # Patches principaux
├── scripts/              # Scripts Python de génération
│   ├── proto07/         # Générateurs Proto 07
│   └── proto08/         # Générateurs Proto 08
├── docs/                 # Documentation complète
├── deploy/              # Scripts de déploiement
└── SONS_V3/             # Matière sonore (non versionnée)
```

## Matière sonore

Le dossier `SONS_V3/` contient toute la matière sonore (non inclus dans git, ~3 Go). Il est généré à partir des archives masters via [`scripts/slice_opacite_v3.py`](scripts/slice_opacite_v3.py).

## Licence & Crédits

Projet en cours de développement par **Loumana**.  
Archives orales : **Simon** (masters dans `SONS_V3/WIP/`).

---

*Pour toute question sur le projet ou son déploiement, consulter d'abord la documentation dans [`docs/`](docs/).*
