# Proto 06 — Dossier de passation technique (handoff agent)

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Statut :** document de relais pour implémentation directe par un nouvel agent (sans refaire le cadrage).  
**Périmètre :** **Proto 06 uniquement** (4HP + 6HP), en partant du proto 05 figé.

---

## 1) Objectif de ce document

Donner à un nouvel agent un plan d'exécution technique prêt à coder, avec:

- décisions actées consolidées;
- séparation stricte `4HP` vs `6HP`;
- stratégie de migration propre depuis proto 05 (sans régression);
- architecture fichiers/scripts/libs;
- backlog atomique priorisé;
- plan de tests console/routage/audio;
- garde-fous anti-erreurs (mapping, double routage, confusion de patch).

**Règle absolue:** `prototype_05_fsm.pd` est **figé** (référence), toute implémentation va dans Proto 06.

---

## 2) Classement des docs source (ordre de travail recommandé)

### A. Source de vérité décisions (priorité maximale)

1. `docs/archive/09_qa_prototype_05.md`  
   - Q&A consolidé, arbitrages détaillés, contraintes figées, points calibrage.

### B. Architecture / méthode de construction

2. `docs/archive/06_prototype_05_plan.md`  
   - principes architecture Pd, logique FSM, conventions de patch et discipline de test.

### C. Roadmap / périmètre versions

3. `docs/archive/07_roadmap_prototypes_finale.md`  
   - versions 4HP/6HP, gel proto 05, phasage.

### D. Contenu / classification sons

4. `docs/archive/08_grille_contenu_sons.md`  
   - organisation SONS, rôle des états, contraintes de segments.

### E. Référence implémentation existante (à cloner, pas étendre)

5. `scripts/archive/gen_prototype_05.py`  
6. `pd/prototype_05_fsm.pd`

---

## 3) Décisions figées (ne pas rediscuter pendant le codage)

## 3.1 Périmètre / versioning

- Proto 05 figé, non extensible.
- Proto 06 = nouveau prototype avec **2 variantes séparées**:
  - `4HP` (sorties 1-2-3-4)
  - `6HP` (sorties 1-2-4-5-6)

## 3.2 Scripts générateurs

- **Deux scripts distincts obligatoires**:
  - `scripts/gen_prototype_06_4hp.py`
  - `scripts/gen_prototype_06_6hp.py`
- Les scripts peuvent partager des libs communes, mais restent séparés.

## 3.3 Audio / console / sécurité

- Gain master validé: `*~ 0.65` (conserver).
- Console Pd: **zéro error, zéro warning**.

## 3.4 Mapping et spatial

- Mapping buffers/couches **fixe**:
  - couche 1 -> HP1
  - couche 2 -> HP3
  - couche 3 -> HP4
- Sens de rotation configurable par variante.
- SPAT mixte autorisé (ex. couche A saute, couche B tourne).
- CORTEX: délai avant première superposition.

## 3.5 INSTALL_MODE

- `INSTALL_MODE = ON`: masque moteur interne + debug.
- `INSTALL_MODE = OFF`: affiche debug complet.

## 3.6 Géométrie 6HP (nouvel arbitrage acté)

- Base: 4 baffles en rectangle.
- +2 baffles supplémentaires au milieu du plus grand côté du rectangle.
- Cette géométrie pilote les presets spatiaux 6HP et le décodage 6 sorties.

## 3.7 Noms opératoires presets V0 (français)

Presets à implémenter dès V0:

- `mode_presentation`
- `mode_edition_complete`
- `mode_automatique`
- `mode_danse`

---

## 4) Architecture cible Proto 06

## 4.1 Fichiers principaux à créer

- `pd/prototype_06_fsm_4hp.pd`
- `pd/prototype_06_fsm_6hp.pd`
- `scripts/gen_prototype_06_4hp.py`
- `scripts/gen_prototype_06_6hp.py`

## 4.2 Libs Pd communes recommandées

Créer des abstractions `*_06` pour isoler Proto 06 de Proto 05:

- `pd/lib/fsm_memory_06.pd`
- `pd/lib/fsm_presets_06.pd`
- `pd/lib/player_state_06.pd`
- `pd/lib/spatial_router_06.pd`
- `pd/lib/fx_router_06.pd`
- `pd/lib/install_mode_06.pd`
- `pd/lib/decode_4hp_06.pd`
- `pd/lib/decode_6hp_06.pd`

Note: si des libs 05 sont réutilisées, les encapsuler clairement pour éviter les collisions de comportement.

## 4.3 Principe de séparation 4HP / 6HP

- `4HP`: version de référence fonctionnelle d'abord.
- `6HP`: dérivée de la logique 4HP, avec adaptation uniquement:
  - décodage/sorties;
  - presets spatiaux dépendants géométrie 6HP.
- La FSM, les variantes, INSTALL_MODE, logique FORCE/AUTO restent alignés entre 4HP et 6HP.

---

## 5) Stratégie de migration depuis Proto 05 (propre, isolée, non-régression)

## 5.1 Copie de base

- Cloner les structures de `gen_prototype_05.py` et `prototype_05_fsm.pd`.
- Ne pas modifier `prototype_05_fsm.pd`.
- Créer tous les points d'entrée Proto 06 sous nouveaux noms.

## 5.2 Isolation technique

- Suffixer/nommer les composants Proto 06 explicitement (`_06`) pour éviter les mélanges.
- Éviter tout recâblage manuel massif directement dans le patch final; privilégier génération script.
- Centraliser la logique presets/FSM dans `fsm_presets_06` et `fsm_memory_06`.

## 5.3 Non-régression

- Conserver un test smoke Proto 05 (chargement propre) pendant l'implémentation 06.
- Vérifier à chaque phase que 06 n'introduit pas de warning global.

---

## 6) Plan technique par phases (implémentation)

## Phase 0 — Initialisation

- Créer les 2 scripts générateurs 06.
- Générer squelette `prototype_06_fsm_4hp.pd` et `prototype_06_fsm_6hp.pd`.
- Brancher déclarations/libs minimales et panels UI.

## Phase 1 — V0 4HP stable

- Sorties `dac~ 1 2 3 4`.
- Gain `*~ 0.65`.
- FSM de base + presets + affichage état.
- INSTALL_MODE ON/OFF opérationnel.
- Console propre au boot et en transitions.

## Phase 2 — Routage couches et SPAT (4HP)

- Implémenter mapping fixe couche->ancre HP.
- SPAT mixte par couche (jump/rotation/sequence).
- Sens rotation configurable par variante.
- CORTEX overlap delay.

## Phase 3 — Presets V0 et variantes (4HP)

- Implémenter presets V0 français:
  - `mode_presentation`
  - `mode_edition_complete`
  - `mode_automatique`
  - `mode_danse`
- Intégrer 3 variantes/état + `variante_id`.
- Implémenter logique FORCE/AUTO exclusive.

## Phase 4 — Validation et gel v0

- Tests patch + console + audio (section 8).
- Corrections bloquantes.
- DoD v0 atteint.

## Phase 5 — Dérivation 6HP

- Adapter décodage géométrie 6HP.
- Sorties `dac~ 1 2 4 5 6`.
- Ajuster presets spatiaux selon géométrie rectangle+2 milieux grand côté.
- Refaire suite de tests.

## Phase 6 — Validation et gel v1

- DoD 6HP atteint.
- Vérification finale non-régression 4HP.

---

## 7) Plan presets/variantes (FSM, SPAT, ECHO/FX, superpositions, INSTALL_MODE)

## 7.1 Cadre global

- 3 variantes par état.
- `CONTRASTE` haut/bas (défaut haut).
- `variante_id` visible en UI.
- FORCE re-clic: variation SPAT/FX, pas de changement fichier par défaut.

## 7.2 Presets opératoires V0 (français)

- `mode_presentation`
  - priorité lisibilité publique, transitions propres, intensité modérée.
- `mode_edition_complete`
  - debug étendu, contrôle manuel visible, paramètres accessibles.
- `mode_automatique`
  - FSM_AUTO dominant, comportement narratif standard installation.
- `mode_danse`
  - dynamique plus marquée, mobilité spatiale et contrastes renforcés.

## 7.3 INSTALL_MODE et presets

- En `mode_presentation` et `mode_automatique`, `INSTALL_MODE` est attendu ON par défaut.
- En `mode_edition_complete`, `INSTALL_MODE` OFF par défaut.
- `mode_danse` selon contexte (répétition/performance), configurable.

---

## 8) Plan de tests (obligatoire avant validation)

## 8.1 Tests patch/console

- Boot patch 4HP: zéro error/warning.
- Changement d'état répété: zéro error/warning.
- Toggle AUTO/FORCE/INSTALL_MODE en boucle: zéro error/warning.

## 8.2 Tests routage audio

### 4HP

- Vérifier sorties actives: 1,2,3,4.
- Vérifier mapping fixe couche 1/2/3 vers ancres.
- Vérifier absence de double chemin non voulu.

### 6HP

- Vérifier sorties actives: 1,2,4,5,6 (3 non utilisée).
- Vérifier cohérence spatiale avec géométrie 6HP définie.

## 8.3 Tests perceptifs

- CORTEX: principal d'abord, superposition après délai.
- SPAT mixte réellement audible.
- Rotation sens variant perceptible.
- Presets V0 distincts à l'écoute.

---

## 9) Risques critiques et mitigations

- **Risque:** confusion mapping couche vs routage dynamique.  
  **Mitigation:** verrouiller ancrage couche dans `spatial_router_06` + tests dédiés.

- **Risque:** divergence 4HP/6HP difficile à maintenir.  
  **Mitigation:** scripts séparés mais libs communes clairement versionnées.

- **Risque:** warnings Pd ignorés.  
  **Mitigation:** test console bloquant à chaque phase.

- **Risque:** dérive des décisions actées pendant codage.  
  **Mitigation:** section 3 traitée comme contrat immuable.

- **Risque:** régression proto 05 involontaire.  
  **Mitigation:** aucun edit 05 + smoke test de chargement 05.

---

## 10) Definition of Done

## 10.1 DoD v0 — `prototype_06_fsm_4hp.pd`

- Patch généré et lançable.
- Sorties 1-2-3-4 correctes.
- Gain master `0.65` appliqué.
- Mapping fixe respecté.
- SPAT mixte opérationnel.
- CORTEX overlap delay opérationnel.
- INSTALL_MODE conforme.
- Presets V0 FR disponibles.
- Console 100% propre.

## 10.2 DoD v1 — `prototype_06_fsm_6hp.pd`

- Patch généré et lançable.
- Sorties 1-2-4-5-6 correctes.
- Géométrie 6HP appliquée dans les presets/routage.
- Comportements FSM/presets alignés avec 4HP.
- Console 100% propre.
- Validation audio de séparation spatiale réalisée.

---

## 11) Checklist atomique priorisée (pour l'agent qui code)

### P0 (bloquant)

- [ ] Créer `gen_prototype_06_4hp.py`
- [ ] Créer `gen_prototype_06_6hp.py`
- [ ] Générer les deux patches 06
- [ ] Verrouiller sorties et gain
- [ ] Installer INSTALL_MODE
- [ ] Passer test console propre

### P1 (fonctionnel)

- [ ] Implémenter mapping fixe couches
- [ ] Implémenter SPAT mixte + sens configurable
- [ ] Implémenter CORTEX overlap delay
- [ ] Implémenter presets V0 FR + UI variante_id

### P2 (robustesse)

- [ ] Finaliser presets 6HP sur géométrie actée
- [ ] Tester non-régression 4HP/05
- [ ] Documenter calibrations à l'oreille (séparées du figé)

---

## 12) Ce qui est figé vs ce qui reste à calibrer

## Figé

- séparation 4HP/6HP
- deux scripts séparés
- géométrie 6HP décrite
- mapping fixe couches
- gain master 0.65
- INSTALL_MODE ON/OFF
- console sans erreurs/warnings
- presets V0 noms FR

## À calibrer à l'oreille (sans changer l'architecture)

- plages temporelles fines (rotation, jump, overlaps)
- pondérations probabilistes exactes des variantes
- intensités FX détaillées selon état
- micro-ajustements de spatialisation 6HP en salle

---

## 13) Consigne de prise de relais (nouvel agent)

Commencer directement par:

1. lire ce document en entier;
2. implémenter P0 sans déviation;
3. valider console propre;
4. implémenter P1 puis tests;
5. dériver 6HP en respectant la géométrie actée;
6. ne pas toucher Proto 05.

Ce document fait office de contrat technique de codage Proto 06.
