# Q&A — Prototype 05 (questions ouvertes)

**Projet :** Mémoires en transit  
**Date :** 9 juillet 2026  
**Usage :** liste de questions pour Loumana — **du plus général au plus précis**.  
Les réponses alimenteront `06_prototype_05_plan.md` et les générateurs Python.

**Note :** les **plages numériques** (ms, wet, rotation, durées FSM…) seront calibrées par Loumana à l’écoute ; les questions marquées `[PLAGE]` attendent des bornes min/max testées.

**Références :** décisions déjà actées → `06_prototype_05_plan.md` §14–17.

### Réponses enregistrées (9 juil. 2026)


| #         | Réponse courte                                                                                                                                                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**     | **1 min** = succès (petite pièce, visite courte). **2–3 min** = idéal. *Précisé par Q3 :* en **~3 min**, le visiteur doit avoir vécu **au moins 2 fois** chaque strate — pas seulement « une fois toutes les strates ».                  |
| **2**     | **Oui**, compréhensible avec **panneau** explicatif. Pas trop abstrait : une **couche poétique**, pas une énigme sans entrée.                                                                                                            |
| **3**     | **Cycle 1 :** **BOUCLE → HIPPO → RECON → CORTEX** en **~50 s** (CORTEX = **phase finale** uniquement). **Cycles 2+ :** ordre libre, **fin CORTEX**. **Reset 7 min** → cycle 1. |
| **4**     | Visite réaliste **5–7 min** (15 min = visiteur très passionné, rare). **CORTEX domine le temps cumulé** — strate la plus claire, la moins dérangeante ; variante atténuée / quasi directe privilégiée en AUTO.                           |
| **5**     | **Oui** — BOUCLE comme entrée **définitive** (Paris + Bruxelles).                                                                                                                                                                        |
| **6**     | **En attente** — pas de privilège voix vs radio pour l’instant ; pondération selon quantité de contenu `SONS/` quand disponible.                                                                                                         |
| **7**     | **Aucun silence** programmé entre états. Si coupure : **≤ 100 ms** max.                                                                                                                                                                  |
| **8**     | **Interaction optionnelle** (proto 05 léger) : 1 entrée audio → triggers ; toggle **INPUT_ON** ; risque larsen (micro dynamique + 4 HP) — pas priorité mais souhaité.                                                                    |
| **9**     | **FSM_AUTO actif dès l’ouverture du patch** (loadbang).                                                                                                                                                                                  |
| **10**    | AUTO **off** → reste en mode manuel sur l’état courant ; FORCE utilisable. **Réactivation AUTO** → FSM reprend (pas réservé au démarrage).                                                                                               |
| **12–15** | **Cycle 1 ~50 s** — plages proposées ci-dessous. **Cycle 2 ~2 min**, plus abstrait. BOUCLE ~**15 s** max en cycle 1 (60 s actuel = trop).                                                                                                |
| **16**    | Durées **liées au contenu** et à la **sortie audio** (attendre fin fichier + **queue du delay/FLUID** avant transition).                                                                                                                 |
| **18**    | Transition AUTO : **même morceau** en général ; **switch fichier rare** (variation).                                                                                                                                                        |
| **19**    | **Pas de fondu** par défaut ; fondu = **option** sur certaines transitions.                                                                                                                                                                |
| **20**    | Si fondu : **700 ms**.                                                                                                                                                                                                                     |
| **21**    | **AUTO ⊥ FORCE** : FORCE **inopérant** si `FSM_AUTO = 1` ; pas de superposition des modes.                                                                                                                                                |
| **22**    | Re-clic : **50/50** même variante / autre ; **3 variantes** par état ; une peut être plus extrême (même mentalité).                                                                                                                      |
| **23**    | **3 variantes** par état (tous, y compris RECON).                                                                                                                                                                                         |
| **24**    | Toggle **`CONTRASTE`** : **HAUT** / **BAS** — **défaut = HAUT**. |
| **25**    | Afficher **`variante_id`** en UI (important, panneau MODIFIABLE ou debug). |
| **26**    | PASSAGE en FORCE → **timer AUTO arrêté + réinitialisé** ; pas de processus parallèles. |
| **27**    | Re-clic FORCE : **SPAT + FX seulement** — pas de changement de fichier. |
| **28**    | CORTEX = parole/idées **complète** l’afflux ; **phase finale** du cycle (après RECON). |
| **29**    | Superposition brève = **comportement par défaut** — pensées furtives / influx sur fond clair. |
| **30**    | Overlap unitaire **~2 s** par défaut (calibrer) ; blocs 10–20 s ou **parsemé** ; plancher ~800 ms trop court. |
| **31–32** | **Défaut :** audio principal + **1** couche interférence, **mêmes baffles + mêmes FX**. Variante rare : 2e couche autre baffle ; variante très rare : **3** couches, baffles distincts (à confirmer). |
| **33**    | Filtre+LFO **identique** sur toutes les couches (défaut) ; **très léger**. Phase LFO décalée = **variante très rare**. Intensité ↑ = perturbation comme les overlaps. |
| **34**    | **Oui** — parfois **1 seule couche** (pas de superposition sample). Filtre+LFO = aussi des **perturbations** de la clarté. |
| **35**    | **Pas de média privilégié** pour l’instant ; contenu surtout **voix** — affinage quand `SONS/` complet (Q6 en attente). |
| **36**    | 2 sons : tirage **aléatoire** du 1er HP (1–4), 2e HP = **opposé** (1↔3, 2↔4). Proto 05 : distance **max** ; final 12 HP : **degré de distance** (pas toujours opposé total). |
| **37**    | **2 sons** : **jamais** superposés. **3–4 sons** : séparation **et** superposition alternées ; max **4** simultanés ; overlap 4 voix ~**5 s**. |
| **38**    | Rotation 2 couches : **4 combinaisons** sens × vitesse ; favori probabiliste **opposés + vitesse identique** (~35 %), **pas dominant**. |
| **39**    | Même logique probabiliste Q38 ; plages `rot_speed` **[PLAGE]** à calibrer. |
| **40**    | **Dynamique** : préférence **effets différents par couche** (delay / saturation / filtre…) — **pas** 3 delays simultanés. Option B (mêmes effets, réglages ±) aussi possible. |
| **41**    | **Spatial** : change toujours (nature actuelle validée). **FX** : seul le **delay** doit pouvoir différer (on/off/atténuer) ; pas d’autre effet « obligatoire » à différencier. |
| **43**    | **Croisement** même baffle : **occasionnel** — pas évité, pas encouragé ; **émergent** si rotations opposées. Variante **ping-pong** (2 sons opposés, rebond au croisement) souhaitée. |
| **44**    | Croisement **émergent** (rotation `phi`) — **pas** saut programmé ni tirage aléatoire HP. Ping-pong : preset + probabilité modérée (~25–30 %). |
| **45**    | **Pas** de durée max forcée ni reséparation programmée — croisement = passage naturel (< ~1–2 s typ.). |
| **46**    | RECON **≠** séparation baffles plus stricte qu’HIPPO — même logique spatiale. Différence = **moins d’infos simultanées** + timbre **moins filtré**, **plus saturé** (vivacité) vs HIPPO/BOUCLE. |
| **47**    | **BOUCLE** : **défaut** 1 couche stricte ; superposition **prob.** par moments (F4). Queue delay/reverb à la transition. |
| **48**    | **Performance** : dynamisme **AUTO** (Q37) — pas de mode nommé. **Debug** : toggle `SPAT_LAYOUT` (AUTO / SÉPARATION / SUPERPOSITION / **UNISON**), actif seulement si `FSM_AUTO = 0`. |
| **49**    | **Option B** : 3× FX + 3× `encode_2d`, **1×** `decode_4hp` ; `spatial_jump` en bus HP hybride si mode saut par couche. |
| **50**    | 4e HP : remainder bref ; 3 couches : delay ↓, dernier arrivé part tôt ; **UNISON** par moments. |
| **F1**    | **HIPPO** : fond / superposition (F.0.1) — patterns de mouvement catalogués (F.0.2), pas aléatoire pur. |
| **F2**    | **3 couches** : fond + superpositions ; dernier arrivé part tôt (Q50). |
| **F0.1**  | Fond + superposition : arrivée = séquence ; 2e ajout = ambi ; fond indépendant. |
| **F0.2**  | **Catalogue de trajectoires** : zigzag, tours harmoniques CW/CCW, ping-pong, repos **oscillant** (pas statique). |
| **F4**    | **Delay** HIPPO/BOUCLE : **presque toujours** en strates profondes ; **dynamique** vs superpositions (delay ↓ si voix superposées). Probabilités, pas strict. Filtres HPF/LPF. |
| **F5**    | **HIPPO** : **Phaser** vs **filtre+LFO** — tirage **50/50** entre variantes (pas de préférence). |
| **G1**    | RECON : superposition limitée, spatial = HIPPO, moins filtré / plus saturé — **confirmé** (Q46). |
| **G2**    | **Phi lent indépendant** par couche ; défaut **faible** mais **visible** ; parfois statique selon sample. |
| **G3**    | Phi lent — amplitude jusqu’à **±180°**, **aller-retour** (pas cercle plein) ; patterns type F.0.2. |
| **G4**    | Delay **décalé** par couche, **différent à chaque retour** ; long (profond) → court (haut) ; FX **atténuables / relançables**. |
| **G5**    | **wet / fb bas par défaut** (couche haute) ; **<** BOUCLE/HIPPO ; pics **brefs** et **rapides** si montée — dynamique. |
| **H1**    | **BOUCLE** re-clic FORCE : **même fichier** par défaut ; changement possible mais rare. |
| **H2**    | Sauts BOUCLE : **longs** par défaut ; fenêtres **rapides** 300–400 ms sur **3–4 s** ; dynamique. |
| **H3**    | Delay BOUCLE = **plafond projet** (réf. wet 0,85 / delay 800 / fb 0,70 / LFO 0,5) ; variantes **fortes** privilégiées. |
| **H4**    | BOUCLE : **SPAT=2** (saut) vs **SPAT=3** (séquence) — tirage **50/50**. |
| **H5**    | **Saturation** en BOUCLE : **oui**, **dynamique** (apparaît/disparaît) ; phases **clarté** sans delay → montée sat/phase → retour delay fort. |
| **I1**    | SPAT : **tout possible** (FX sur superposés inclus) ; par état : **BOUCLE/RECON** = saut+seq+rotation ; **RECON** + dry ; **HIPPO/CORTEX** = dry+rotation, flash = saut/seq/rotation. |
| **I7**    | Rotation : **continu** = défaut (SPAT=1) ; perception **baffle par baffle** = **option** souhaitée (SPAT=3 / séquence). |
| **J1**    | Renommage UI : **ECHO** (pas DELAY). |
| **J3**    | Feedback delay : plage **0 – 70 %** (plafond projet). |
| **J4**    | Filtre CORTEX : **HPF 20–1200 Hz**, **LPF 20 000–1200 Hz**, résonance **~1 %**. |
| **J5**    | **LFO sur le delay** (`fluid_lfo`) : **garder**. |
| **J6**    | Saturation : **prédominante** couche principale **BOUCLE** ; **modérée** HIPPO ; **pas** RECON/CORTEX principal ; **oui** sur **superposés** (toutes strates). |
| **J7**    | Compensation sat : **proportionnelle** — plus drive/wet ↑ → volume sortie ↓ ; facteur réf. **×1,5**. |
| **J8**    | Ordre proto FX : **1 saturation → 2 filtre → 3 LFO → 4 phaser**. |
| **K1**    | 5 WAV **insuffisants** pour Paris ; découpe : voix + cheick **×3**, radio campus **×10**. |
| **K2**    | **Pas** d’interdiction extrait × état. |
| **K3**    | Minimum segments par case État×Durée : **à définir** (session classification). |
| **K4**    | Multi-états : **autorisé** — même source dans plusieurs dossiers d’état, sans règle stricte. |
| **K5**    | Durée **max** segment découpé : **1 min 30** (90 s). |
| **L1**    | **Proto 06** (pas 05) pour grosses impl. ; **05 figé** ; deux variantes : **4 HP** (auj.) + **6 HP** (samedi). |
| **L2**    | Sorties carte : **1–2–3–4** (4 HP) ; **1–2–4–5–6** (6 HP) — confirmé toutes sessions. |
| **L3**    | Gain master `*~ 0.65` : **très bien** — conserver. |
| **L4**    | MOTEUR_INTERNE : **masqué en installation** via toggle **INSTALL_MODE** (ON masque / OFF debug). |
| **L5**    | **Presets** présentation / intensité — **oui**, plusieurs niveaux. |
| **L6**    | Console Pd : **zéro error, zéro warning** — aucune tolérance. |
| **N1**    | Assignation buffer ↔ baffle : **mapping fixe** (très important) — pas de rotation à chaque transition. |
| **N2**    | Rotation opposée (sens couche 1 / 2) : **configurable par variante** — pas toujours H/anti-H. |
| **N3**    | Saut + rotation **dans la même variante** HIPPO : **oui**, autorisé. |
| **N6**    | CORTEX : **délai** avant **première** superposition brève — oui (pas immédiat). |
| **N7**    | Max re-clics FORCE — **non pertinent** (question retirée). |
| **N8**    | **Proto 06** : implémenter **au maximum** le Q&A ; 05 figé ; routage propre (éviter confusion 03–05). |


#### Plages cycle 1 proposées (~50 s total) — à valider à l’oreille


| Étape | État | Durée cible | Plage min–max (ms) | Notes |
| ------ | ------------------------- | ----------- | ------------------ | -------------------------------------- |
| Entrée | **BOUCLE** | **14 s** | 12 000 – 16 000 | Profondeur, entrée installation |
| T1 | **HIPPO** | **7 s** | 5 000 – 9 000 | Passage rapide, associations |
| T2 | **RECON** | **16 s** | 14 000 – 18 000 | Recomposition — parmi les plus longs |
| T3 | **CORTEX** | **13 s** | 10 000 – 16 000 | **Phase finale** — clarté / parole |
| | **Total** | **~50 s** | 41 000 – 59 000 | Bornes souples si lié au contenu (Q16) |


#### Plages cycle 2 proposées (~2 min) — ordre libre, fin CORTEX


| Paramètre            | Cible                                                    |
| -------------------- | -------------------------------------------------------- |
| Durée totale cycle 2 | **~120 s** (peut s’étirer si queues delay)               |
| Ordre intermédiaire  | **Libre** (HIPPO, RECON, BOUCLE dans un ordre variable)  |
| Fin obligatoire      | **CORTEX** (clarté)                                      |
| Dominance cumulée    | **CORTEX** tend à accumuler le plus de temps sur 5–7 min |


#### Reset 7 minutes

À **420 000 ms** de session AUTO : **forcer** nouveau cycle 1 complet **BOUCLE → HIPPO → RECON → CORTEX**.

---

## A. Vision générale et narration

1. ~~Quelle est la **durée d’écoute idéale**…~~ → **Répondu** (voir tableau ci-dessus).
2. ~~L’installation doit-elle être **compréhensible**…~~ → **Répondu**.
3. ~~Y a-t-il un **ordre narratif préféré**…~~ → **Répondu** (cycle 1 fixe ; cycles 2+ libres, fin CORTEX ; reset 7 min).
4. ~~Quel état doit dominer…~~ → **Répondu** — **CORTEX** en temps cumulé ; session typique **5–7 min**.
5. ~~La **Boucle** comme entrée…~~ → **Répondu** — oui, définitif.
6. ~~Quand tu dis « mémoire »…~~ → **En attente** (pondération selon contenu).
7. ~~Faut-il des **moments de silence**…~~ → **Répondu** — non ; ≤ 100 ms si coupure.
8. ~~Le public peut-il **interagir**…~~ → **Répondu** — option INPUT + triggers (proto 05 léger).

---

## B. FSM — démarrage et mode AUTO

1. ~~**AUTO au load**…~~ → **Répondu** — actif **dès l’ouverture du patch**.
2. ~~Si l’utilisateur coupe **FSM_AUTO**…~~ → **Répondu** — reste manuel ; réactivation AUTO possible à tout moment.
3. ~~En AUTO, la première transition après BOUCLE…~~ → **Orientée** : toujours **HIPPOCAMPE** (voir Q3, parcours canonique).
4. ~~`[PLAGE]` Durée **BOUCLE**…~~ → **Répondu** — cycle 1 : **~14 s** (plage 12–16 s). Voir tableau réponses.
5. ~~`[PLAGE]` **HIPPOCAMPE**…~~ → **Répondu** — cycle 1 : **~7 s** (5–9 s).
6. ~~`[PLAGE]` **CORTEX**…~~ → **Répondu** — cycle 1 : **~13 s** en **phase finale** ; dominant en cumul sur session.
7. ~~`[PLAGE]` **RECONSTRUCTION**…~~ → **Répondu** — cycle 1 : **~16 s** (14–18 s) — recomposition avant clarté.
8. ~~Les durées AUTO…~~ → **Répondu** — liées au **contenu** et à la **sortie** (queue delay/FLUID).
9. ~~Faut-il une **matrice de transition**…~~ → **Oui** :

**Cycle 1 (obligatoire, ~50 s) :**

```text
BOUCLE (3) ──► HIPPO (1) ──► RECON (2) ──► CORTEX (0)
```

**Cycles 2+ (~2 min, plus abstraits) :**

```text
[ordre libre : HIPPO / RECON / BOUCLE / CORTEX …] ──► CORTEX (0)   ← atterrissage clarté
```

**Reset session à 7 min :** forcer à nouveau le **cycle 1** complet (BOUCLE en premier).

Seul le **premier** cycle impose BOUCLE en tête ; les suivants peuvent permuter les strates intermédiaires.
18. ~~Une transition AUTO doit-elle **toujours** relancer…~~ → **Répondu** — **même morceau** en général ; switch fichier **rare**.
19. ~~Faut-il un **fondu** entre états…~~ → **Répondu** — **non par défaut** ; fondu optionnel (variable).
20. ~~`[PLAGE]` Durée de fondu…~~ → **Répondu** — **700 ms** si fondu actif.

---

## C. FSM — FORCE_ETAT et variantes

21. ~~En **FORCE**, FSM_AUTO…~~ → **Répondu** — exclusif : AUTO on → FORCE ignoré.
22. ~~Re-clic sur le **même** état…~~ → **Répondu** — 50/50 ; 3 variantes.
23. ~~Combien de **variantes** par état…~~ → **Répondu** — **3**.
24. ~~Les variantes doivent-elles être…~~ → **Répondu** — toggle **CONTRASTE HAUT / BAS** (voir ci-dessous).

#### Q24 — Toggle CONTRASTE (précision 9 juil. 2026)

| Mode UI | Comportement |
|---------|--------------|
| **CONTRASTE_HAUT** | Écarts **forts** entre phases FSM et entre variantes — effets et spatial **attirent l’attention** ; différenciation nette de chaque « endroit du cerveau ». |
| **CONTRASTE_BAS** | Différences **toujours audibles** entre strates/variantes, mais **sans** effets qui « sautent aux oreilles » — transitions plus homogènes, moins spectaculaires. |

- Contrôle : **`tgl` ou hradio** dans panneau FSM (MODIFIABLE), ex. `CONTRASTE` 0=bas / 1=haut.
- **Défaut au load : `CONTRASTE_HAUT` (1).**
- S’applique aux **presets variantes** (échelles wet/fb, intensité FX, amplitude spatiale) — pas un simple volume master.
- Utile pour **médiation** (haut) vs **écoute longue** / installation discrète (bas).

25. ~~Faut-il afficher… `variante_id`…~~ → **Répondu** — **oui**, important (floatatom ou label dans panneau FSM).
26. ~~FORCE doit-il **réinitialiser** les timers AUTO…~~ → **Répondu** — **arrêt + reset** du timer AUTO ; **aucun** processus AUTO en arrière-plan en mode FORCE.
27. ~~Un re-clic FORCE doit-il **changer de fichier**…~~ → **Répondu** — **SPAT + FX uniquement** ; le **fichier / matériau** continue ; distribution des audios et altération spat/FX sont **découplés**.

---

## D. CORTEX — sens et comportement (clarification récente)

1. ~~CORTEX = **parole / idées**…~~ → **Répondu** (Q28).
2. ~~La **superposition brève**…~~ → **Répondu** — **comportement par défaut** (Q29).
3. ~~`[PLAGE]` Durée typique…~~ → **Répondu** — voir §D détail (Q30).
4. ~~En CORTEX, combien de couches…~~ → **Répondu** (Q31).
5. ~~La superposition CORTEX se fait sur **les mêmes baffles**…~~ → **Répondu** — **oui** par défaut ; exceptions variantes (Q32).
6. ~~Le **filtre + LFO**…~~ → **Répondu** (Q33).
7. ~~CORTEX peut-il parfois n’avoir **qu’une seule** couche…~~ → **Répondu** — **oui** (Q34).
8. ~~Quels **types de sons** privilégier en CORTEX…~~ → **Répondu (partiel)** — pas de type privilégié pour l’instant ; **voix** majoritaires ; précision **en attente** (catalogue `SONS/` incomplet, lié Q6).

#### Filtre+LFO et perturbations (Q33–34)

| Sujet | Défaut | Variante rare |
|-------|--------|---------------|
| **Filtre+LFO entre couches** | **Identique** (même réglages, même phase) | Phase LFO **décalée** entre couches |
| **Intensité filtre+LFO** | **Très légère** — à peine perceptible | Plus marquée = **interférence de pensée** qui trouble la parole claire |
| **Superposition samples** | Active (défaut Q29) | **Aucune** — 1 seule couche audible possible |
| **Types de perturbation** | (1) fragments samples superposés ; (2) filtre+LFO un peu plus intenses — **même famille** : ce qui **enlève** la clarté |

→ Pas de superposition sample **et** filtre+LFO au minimum = moment de **clarté maximale**.

#### Contenu audio CORTEX (Q35 — partiel)

| État | Guidance actuelle |
|------|-------------------|
| **Média** | **Aucun type privilégié** (radio / discours / archive — pas de règle fixe) |
| **Timbre dominant** | Surtout des **voix** |
| **Statut** | **En attente** — pondération fine quand tous les extraits seront dans `SONS/` (voir Q6) |

#### Détail CORTEX — superposition et durées (acté 9 juil. 2026)

**Métaphore :** fond **clair** (audio principal) + **impulsions** furtives (paroles/fragments courts) — influx électriques qui **interfèrent** sans noyer la clarté.

| Paramètre | Défaut / cible |
|-----------|----------------|
| **Audio principal** | Peut tourner **longtemps** sur le **même** fichier — **~50 s** acceptable pour tests (pas une limite fixe définitive) |
| **Budget interférences** | Sur une période type ~50 s : **~15 s cumulées** d’overlaps possibles — en **bloc** (10–20 s), **parsemé**, ou **absent** |
| **Durée d’un overlap** | **~2 s** par défaut (entendre au moins un mot / quelques mots) ; **&lt; 800 ms** = trop court ; blocs longs possibles |
| **Couches (défaut)** | **1 principal + 1 interférence** — **mêmes baffles**, **même FX** |
| **Variante rare** | 2e interférence sur **autre baffle** (même FX) |
| **Variante très rare** | **3 couches** — baffles **distincts**, même FX (à confirmer en écoute) |

```text
[CORTEX ~50 s]
  p_main ─────────────────────────────────────────►  (clarté, même fichier)
  p_intr ──2s──    ──2s──      ─────10s────         (parsemé ou blocs, ≤ ~15s total)
           └── même baffle + même filtre/LFO que main (défaut)
```

---

## E. Multi-couches — spatial et FX par lecteur (clarification récente)

### Comportement actuel (problème)

```text
p1 + p2 + p3 → mix~ → 1× FX → 1× SPAT → 4 HP
```

→ Tout superposé, mêmes effets, même image spatiale.

### Comportement cible acté (HIPPOCAMPE + RECONSTRUCTION)

36. ~~**Par défaut**, 2 sons = **2 baffles différents**…~~ → **Répondu** — tirage aléatoire + **paire opposée** (voir ci-dessous).
37. ~~**3 sons** = **3 baffles différents**…~~ → **Répondu** — pas toujours 3 HP distincts ; **dynamisme** séparation ↔ superposition (voir E.2).

#### E.1 Assignation 2 couches — tirage + opposé (Q36, acté)

**Proto 05 (4 HP, setup carré) :**

1. Tirer **au hasard** le HP de la **couche A** ∈ {1, 2, 3, 4}.
2. La **couche B** va sur le HP **opposé** (distance maximale dans ce quad) :

| Couche A | Couche B (opposé) |
|----------|-------------------|
| HP **1** | HP **3** |
| HP **2** | HP **4** |
| HP **3** | HP **1** |
| HP **4** | HP **2** |

Formule (index 1–4) : `opposite(h) = h + 2` si h ≤ 2, sinon `h - 2`.

```text
        HP1 ────── HP2
          │   pièce   │
        HP3 ────── HP4

Paires opposées (distance max, proto 05) : (1,3) et (2,4)
```

→ Pas HP1+HP2 **fixes** : le **premier** HP est aléatoire, le second est **contraint** par l’opposition.

**Installation finale (12 HP) — concept à retenir :**

| Concept | Description |
|---------|-------------|
| **Degré de distance** | Les deux couches doivent être séparées par une **distance angulaire / géométrique suffisante** — pas toujours diamétralement opposées |
| **Proto 05** | Cas particulier : 4 HP → opposition **totale** (= distance max) |
| **Proto 08 / final** | Matrice de **distances minimales** entre HP (ex. ≥ 90° ou ≥ N positions sur l’anneau) — à calibrer en salle |

#### E.2 Trois à quatre couches — dynamisme séparation / superposition (Q37, acté)

| Nb couches | Règle |
|------------|--------|
| **2** | **Toujours séparés** sur baffles opposés (Q36) — **pas** de superposition |
| **3–4** | **Dynamique** : par moments **distincts** (baffles différents), par moments **superposés** (même baffle ou image ambisonique convergente) |
| **Maximum** | **4** samples simultanés — plafond dur ; au-delà = trop dérangeant |
| **4 en même temps** | Moment de **malaise** possible, **bref** : **~5 s** max (plus qu’un éclair &gt; 2 s, mais court) |
| **3 en même temps** | Superposition permise ; durée variable (souvent &lt; overlap 4 voix) |

**Non-linéarité exigée** — pas de comportement mécanique :

- apparition des samples **irrégulière** ;
- mouvement via **LFO / filtre**, **rotation ambisonique**, **delay** — parfois convergent, parfois divergent ;
- alternance **séparé ↔ superposé** non prévisible (plages, pas tempo fixe).

```text
2 couches  →  HP opposés (fixe)
3–4 couches →  ═══ séparés ───┐
               ═══ superposés ┘  (alternance dynamique)
4 couches  →  pic ~5 s max (malaise bref) puis reséparation
```

**Assignation 3 couches (proto 05, indicatif)** — à affiner en écoute :

- souvent **3 HP distincts** (1, 2, 3 ou tirage parmi 4) ;
- parfois **2 sur opposés + 1 rejoint** un HP existant (superposition partielle) ;
- **3e couche (dernier arrivé)** : **fixe**, durée **la plus courte** — F2 ;
- règle exacte de tirage : **non fixe** — pilotée par variante / phase FSM.

#### E.3 Rotation sur 2 couches — sens et vitesse (Q38, acté)

**Toutes les combinaisons** doivent être **envisageables** (options activables / tirage probabiliste) :

| Paramètre | Options |
|-----------|---------|
| **Sens** | **Identique** ou **opposé** entre les 2 couches |
| **Vitesse** | **Identique** ou **différente** (`rot_speed` par couche) |

→ 4 combinaisons : (sens×, vit×), (sens×, vit≠), (sens≠, vit×), (sens≠, vit≠).

**Défaut probabiliste** (favori mais **pas dominant**) :

| Tirage | Probabilité | Notes |
|--------|-------------|--------|
| Sens **opposés** + vitesse **identique** | **Plus haute** (modérée) | Préférence artistique |
| 3 autres combinaisons | Chacune **possible** | Doivent rester audibles souvent |

Implémentation : poids dans `fsm_presets` (ex. opposé+égale ~**35 %**, autres ~**20–25 %** — à calibrer).

**Important :** ce n’est **jamais** « toujours opposé » — le favori est une **tendance probabiliste**, pas une règle fixe.

39. ~~`[PLAGE]` `rot_speed` couche A vs B…~~ → **Partiel** — structure probabiliste **confirmée** (identique à Q38) ; valeurs numériques **en attente** calibration (§M).

| Cas tirage | `rot_speed` |
|------------|-------------|
| Vitesse **identique** | Une valeur `v` tirée dans `[rot_min, rot_max]` |
| Vitesse **différente** | `v_a` et `v_b` dans la même plage (ou `v_b = v_a × ratio`) — **[PLAGE] à tester** |
| Sens | Indépendant du tirage vitesse — matrice Q38 |

→ Pas de comportement dominant : même avec favori ~35 %, **≥ 65 %** des événements utilisent les autres combinaisons.
40. ~~Les **effets par couche**…~~ → **Répondu** — voir E.4.

#### E.4 Effets par couche — types différents, pas trois delays (Q40, acté)

**Les deux approches sont possibles** (dynamique, non linéaire) :

| Approche | Description | Usage |
|----------|-------------|--------|
| **A — Effets différents** (préféré) | Chaque couche peut avoir un **type** d’effet distinct | ex. couche 1 **delay**, couche 2 **saturation**, couche 3 **filtre+LFO** |
| **B — Même effet, réglages ±** | Toutes les couches passent par le **même** module | wet / intensité légèrement différents, voire **identiques** |

**À éviter absolument :**

- **3 delays en même temps** avec réglages très différents → **oppressant** dans une **petite pièce**
- Maximum **2 delays** simultanés, et seulement **légèrement** différents si deux delays coexistent

**Règles :**

| Règle | Détail |
|-------|--------|
| **Préférence** | **Option A** — diversité de **types** d’effets, pas de répétition du même effet lourd |
| **Permis** | Passages où **tout** passe par le **même** effet (réglages proches ou identiques) |
| **Petite pièce** | Limiter la **charge** réverbérante / écho (delay cumulé) |
| **Superpositions** | Selon le moment : combinaisons différentes (delay+saturation) **ou** unifiées |

```text
Bon (préféré) :  Son A → delay léger   │  Son B → saturation  │  Son C → filtre
À éviter :       Son A → delay 400ms   │  Son B → delay 800ms │  Son C → delay 1.2s
Acceptable :     Son A → delay         │  Son B → delay (réglages proches seulement)
```

41. ~~Quels paramètres doivent **obligatoirement** différer…~~ → **Répondu** — voir E.5.

#### E.5 Paramètres obligatoires par couche — spatial + delay seul levier FX (Q41, acté)

**Spatialisation — validée :**

| | |
|---|---|
| **Comportement** | La **spatialisation change** entre couches — **à conserver** |
| **Ce qui plaît** | Les **choix de nature** (saut, rotation, opposés…) — pas les réglages numériques en priorité |
| **Obligatoire** | **Oui** — identité spatiale **distincte** par couche quand séparées |

**Effets — seul le delay diffère intentionnellement :**

| Paramètre | Doit différer ? | Rôle |
|-----------|-----------------|------|
| **Spatial** (baffle, sens, mode) | **Oui** | Séparation perceptuelle principale |
| **Delay** (on/off, wet, atténuation) | **Oui** — **seul levier FX prioritaire** | Met du **nuage** autour de l’info ; couper/atténuer = **moins d’information**, changement **plus conséquent** |
| **Saturation, filtre, LFO, wet autre…** | **Non** — pas de préférence à différencier | Peuvent être **identiques** entre couches |
| **Delay toujours actif** | **Non** | Le delay **ne doit pas** être sur **chaque** couche en permanence |

**Logique artistique :**

- Le delay **voile** l’information principale → l’**activer / désactiver / atténuer** par couche est le moyen privilégié de moduler la **densité** et la **clarté**.
- Les autres effets restent **optionnels** et **homogènes** sauf choix ponctuel (Q40 — types différents possibles mais **pas obligatoires**).

```text
Couche A : HP opposé 1  │  delay OFF   │  filtre identique
Couche B : HP opposé 3  │  delay ON léger  │  filtre identique
→ Changement audible = spatial + présence/absence du nuage delay
```

42. ~~`[PLAGE]` Écart minimum audible entre wet couche 1 et couche 2~~ → **Reformulée** — voir note ci-dessous.

> **Clarification (après Q41) :** cette question visait le **`fluid_wet`** du **delay** (intensité du traitement écho) — pas le wet d’un filtre, saturation, etc.  
> Avec Q41, le contraste principal est **delay ON vs OFF** par couche ; calibrer un **écart de wet** n’est utile **que** si **deux couches ont le delay actif en même temps** (cas acceptable Q40, max 2 delays proches).  
> **Question reformulée :** quand 2 couches ont toutes les deux le delay ON, faut-il un écart de wet minimum audible, ou **on/off suffit** sans nuancer le wet ?

43. ~~**Croisement** sur le même baffle…~~ → **Répondu** — voir E.6.

#### E.6 Croisement sur même baffle + variante ping-pong (Q43, acté)

**Fréquence du croisement :**

| | |
|---|---|
| **Niveau** | **Occasionnel** — ni rare ni fréquent |
| **À éviter ?** | **Non** — totalement acceptable |
| **À encourager ?** | **Non** — pas un comportement cible |
| **Attitude** | **Pas grave** — arrivera **d’office** avec certains réglages |

**Mécanisme :**

- Le croisement est surtout **émergent** : si 2 sons **tournent en sens opposé** (Q38), ils **peuvent se croiser** sur le même baffle — comportement **naturel**, pas besoin de le forcer.
- Pas de règle « toujours séparés » stricte au-delà du cas **2 sons** (Q37 : jamais superposés au départ — le croisement en mouvement est autre chose).

**Variante rotation — ping-pong** (souhaitée, à implémenter) :

| | |
|---|---|
| **Contexte** | **2 sons**, rotation **sens opposés** |
| **Départ** | Chacun depuis un **côté opposé** de l’espace (extrémités / baffles opposés) |
| **Croisement** | Quand les deux **se rencontrent** (même baffle / même zone) → **inversion de sens** (rebond) |
| **Effet** | Mouvement **ping-pong** — va-et-vient autour du point de croisement |
| **Statut** | **Variante** de rotation — détails activation Q44 (§E.7) |

```text
  HP1 ←—— son A          son B ——→ HP3
              ↘ croisement ↙
         rebond : A → droite, B → gauche
```

44. ~~Le croisement est-il **programmé**…~~ → **Répondu** — voir E.7.

#### E.7 Mécanisme de croisement — émergent + ping-pong (Q44–45, acté)

**Recommandation approuvée par Loumana (9 juil. 2026) :**

| Option | Verdict |
|--------|---------|
| **Saut programmé** vers le même HP | **Non** — trop artificiel |
| **Tirage aléatoire** de HP | **Non** — imprévisible, peu musical |
| **Émergent** (rotation continue) | **Oui** — comportement par défaut |

**Comportement par défaut :**

1. **Départ** : baffles **opposés** (Q36)
2. **Mouvement** : rotation `phi` par couche, sens ± indépendants (Q38)
3. **Croisement** : **aucune règle dédiée** — conséquence géométrique du mouvement → **occasionnel** (Q43)
4. **Pas de** : « dans X secondes, saute tous les deux sur HP2 »

**Ping-pong** (variante, Q43) :

| | |
|---|---|
| **Activation** | Flag preset `rot_pingpong=1` **+** tirage probabiliste **modéré** (~**25–30 %**) quand config déjà « sens opposés + vitesse identique » |
| **Règle** | **Déterministe** au croisement : si `|phi_A − phi_B| < seuil` → **inversion `SENS`** sur les deux couches |
| **Pas** | Saut HP forcé — rebond via rotation seulement |

**Durée sur même baffle (Q45) :**

| | |
|---|---|
| **Plafond forcé** | **Non** — pas de reséparation programmée |
| **Durée réelle** | Tant que les deux `phi` convergent sur la même zone — typiquement **< 1–2 s** en rotation lente |
| **Implémentation** | Pas de timer « reséparation » ; le mouvement continue naturellement |

```text
Normal :     phi_A, phi_B tournent → croisement parfois (géométrie)
Ping-pong :  seuil croisement → flip SENS (preset + ~25–30 %)
Interdit :   saut programmé vers même HP / tirage HP aléatoire
```

45. ~~`[PLAGE]` Durée max…~~ → **Répondu** — pas de règle fixe (voir ci-dessus).

46. ~~En **RECONSTRUCTION**, la séparation…~~ → **Répondu** — voir E.8.

#### E.8 RECONSTRUCTION vs HIPPOCAMPE — clarté par densité et timbre (Q46, acté)

**Pas une séparation baffles plus stricte :**

| | HIPPOCAMPE | RECONSTRUCTION |
|---|------------|----------------|
| **Règles spatiales** (baffles, opposés, croisement) | **Même logique** — Q36–Q45 s’appliquent **identiquement** |
| **Séparation « plus stricte »** | **Non** — ce n’est **pas** le levier principal |

**Gradient de clarté (montée narrative BOUCLE → CORTEX) :**

| Niveau | Densité perçue | Flou / clarté | Notes |
|--------|----------------|---------------|--------|
| **BOUCLE** | **Plus d’informations** (impression dense) | Flou acceptable — comportement **proto 05 actuel apprécié** | Entrée, obsession |
| **HIPPOCAMPE** | Intermédiaire (2–3 fragments) | Associations, dialogue | |
| **RECONSTRUCTION** | **Moins d’infos simultanées** | **Plus clair** — recomposition lisible | Avant CORTEX |
| **CORTEX** | Peu d’overlaps (Q29–34) | Clarté maximale (parole) | Phase finale |

→ En remontant : **moins flou**, **moins de couches en même temps**.

**Identité timbrale RECONSTRUCTION** (levier principal vs HIPPO / BOUCLE) :

| Paramètre | RECON vs HIPPO / BOUCLE |
|-----------|-------------------------|
| **Filtre** | **Moins filtré** — sons plus **présents**, moins « lointains » |
| **Saturation** | **Plus saturée** — identité **plus vive**, plus de **vivacité** |
| **Delay** | Variable par couche (Q41) — peut être **présent** (nuage) ou **coupé** pour clarifier ; pas le critère spatial |

**Superposition en RECON :**

- Tendance : **presque pas de superposition** prolongée — préférer **moins de couches actives** plutôt que forcer des baffles différents.
- Variante possible : peu de superposition + **delay plus marqué** sur les couches restantes — secondaire par rapport au **filtre / saturation**.

```text
BOUCLE     : dense, flou, « beaucoup » — référence = proto 05 actuel
HIPPO      : dialogue, filtré, 2–3 voix
RECON      : moins de voix à la fois, moins de filtre, plus de saturation — clarté ↑
CORTEX     : clarté parole, overlaps furtifs
```

47. ~~En **BOUCLE** (1 couche dominante)…~~ → **Répondu** — voir E.9.

#### E.9 BOUCLE — une seule couche + queue FX (Q47, acté)

**Couches simultanées en BOUCLE :**

| Règle | Détail |
|-------|--------|
| **2 couches en même temps** | **Jamais** |
| **Comportement** | Passage **strict** d’**une couche à une autre** — comme le **prototype actuel** |
| **Variantes** | Défaut : **1 lecteur** strict ; **probabiliste** : superposition brève ou isolation 1 baffle (F4) |

**Lien entre couches / états — queue delay & reverb :**

| | |
|---|---|
| **Principe** | Quand on **quitte** une couche (ou un état), la **queue** du delay / reverb **continue de résonner** même si le FX est **désactivé** sur la couche suivante |
| **Exemple** | BOUCLE (énorme delay) → HIPPOCAMPE (reverb) : le **delay de la BOUCLE** s’éteint progressivement pendant que HIPPO démarre — **pas de coupure sèche** |
| **Rôle artistique** | **Lier** les strates dans certaines transitions — continuum mémoriel |
| **Lien Q16** | Renforce la règle **contenu + queue FX** avant transition AUTO |

```text
BOUCLE     : [couche A seule] ──strict──► [couche B seule]   (jamais A+B)
Transition : source OFF + delay/reverb tail ON ──► nouvelle couche + nouveaux FX
```

**Implémentation (cible) :**

- Bus **tail / send** séparé ou queue RMS sur sortie FX avant mute ;
- Couper l’**entrée** du lecteur, pas la **résonance** immédiate du delay/reverb.

48. ~~Faut-il un mode explicite **« superposition »**…~~ → **Répondu** — voir E.10.

#### E.10 Layout spatial — AUTO en expo, toggle debug (Q48, acté)

**En performance (FSM_AUTO = 1) :**

| | |
|---|---|
| **Mode nommé** | **Non** — pas de interrupteur SÉPARATION / SUPERPOSITION en circulation normale |
| **Comportement** | **Dynamisme automatique** selon état, variante et tirage (Q37, Q29–31) |

**En debug / écoute (FSM_AUTO = 0) :**

| | |
|---|---|
| **Toggle** | `SPAT_LAYOUT` : **AUTO** \| **SÉPARATION** \| **SUPERPOSITION** \| **UNISON** |
| **Emplacement UI** | Zone **SPATIAL_(MODIFIABLE)** — à côté des autres contrôles manuels |
| **Rôle** | Tester rapidement le routage spatial/FX sans attendre un tirage ou changer d’état |
| **Stabilité** | Override **⊥ FSM_AUTO** — ignoré dès que AUTO est on (même logique que FORCE, Q21) |

| Valeur | Effet debug |
|--------|-------------|
| **AUTO** | Presets / variante courante (pas de forçage) |
| **SÉPARATION** | Force baffles distincts + FX par couche (delay on/off selon preset) |
| **SUPERPOSITION** | Force même image spatiale + même chaîne FX pour toutes les couches actives |
| **UNISON** | **Tous les baffles** = **même** sample + **mêmes** FX (facteur Q50 — aussi en tirage AUTO) |

**Rappel par état (inchangé) :**

- **BOUCLE** : 1 couche stricte (Q47) — toggle peu pertinent
- **2 sons** : séparés par défaut (Q36)
- **3–4 sons** : alternance dynamique (Q37)
- **CORTEX** : superposition brève par défaut (Q29–31)

### Architecture technique (à valider)

49. ~~Acceptes-tu **3 chaînes FX + 3 chaînes SPAT**…~~ → **Répondu** — **Option B** (§E.11).

#### E.11 Architecture multi-bus — Option B (Q49, acté)

**Choix :** **3 FX + 3 encode, 1 decode** — plus léger CPU, adapté Raspberry Pi.

```text
player_1 ─► FX_1 ─► encode_2d (phi₁) ──┐
player_2 ─► FX_2 ─► encode_2d (phi₂) ──┼─► somme W,X,Y ─► 1× decode_4hp ─► 4 HP
player_3 ─► FX_3 ─► encode_2d (phi₃) ──┘
```

| | |
|---|---|
| **FX par couche** | **3×** delay (on/off indépendant — Q41) |
| **Rotation** | **1 phi par couche** → encode → **somme ambi** → **1 decode** |
| **Mode saut HP** | `spatial_jump` **hors ambi** — bus HP séparés par couche, sommés avant `dac~` (hybride proto 05) |
| **Option A rejetée** | 3× decode — trop lourd sans gain audible sur 4 HP |

50. ~~Sur **4 HP**, si 3 couches…~~ → **Répondu** — voir E.12.

#### E.12 4e baffle, densité à 3 couches, facteur UNISON (Q50, acté)

**4e baffle quand 3 couches sur 3 HP :**

| | |
|---|---|
| **Silencieux strict ?** | **Non** — le 4e peut recevoir **remainder** / **reverb** / fuite ambi |
| **Durée** | **Bref** — ne pas laisser traîner (cohérent Q37, Q45) |
| **Rôle** | Colle spatiale, pas une 4e « voix » autonome prolongée |

**Règles quand 3 couches simultanées** (densité déjà élevée) :

| Règle | Détail |
|-------|--------|
| **Durée totale** | **Courte** — le **dernier arrivé** part **le plus tôt** (F2) |
| **Couche fixe** | **Dernier arrivé** = durée **minimale** ; **ambi** (2e ajout) par défaut — fixe = variante rare (F.0.1) |
| **Delay** | **Beaucoup moins** qu’à 1–2 couches — déjà beaucoup d’info à 3 |
| **Lien Q40** | Pas 3 delays lourds ; privilégier **delay off** sur au moins une couche |
| **Lien Q37** | Pic 3–4 voix = moment **non linéaire** et **bref**, pas un plateau long |

```text
3 couches actives →  delay global ↓↓↓  +  1 couche mute tôt  +  4e HP = remainder léger seulement
```

**Facteur UNISON** (nouveau — à intégrer presets + debug) :

| | |
|---|---|
| **Effet** | **Tous les baffles** diffusent le **même** son : **même sample** + **mêmes effets** |
| **Différence vs SUPERPOSITION** | SUPERPOSITION = couches fusionnées ; **UNISON** = copie **identique** sur HP1–HP4 (immersion / mur sonore) |
| **Usage** | **Par moments** — tirage probabiliste ou variante preset (pas permanent) |
| **Debug** | Valeur **UNISON** du toggle `SPAT_LAYOUT` (Q48) |
| **Implémentation** | 1 lecteur → 1 FX → **decode mono identique** sur 4 sorties **ou** gain 1.0 sur chaque HP |

```text
SÉPARATION :  A→HP1   B→HP3   C→HP2
SUPERPOSITION : A+B+C → même phi / mêmes FX
UNISON :      sample X + FX X → HP1 = HP2 = HP3 = HP4 (identique)
```

---

## F. HIPPOCAMPE

#### F.0 Vocabulaire — deux types de « mouvement » (clarification)

Dans le doc, le mot **rotation** / **mouvement** peut désigner **deux modes SPAT distincts** — **les deux restent valides** pour HIPPO et explorables en BOUCLE (ni l’un ne remplace l’autre) :

| Mode | SPAT | Comportement | Paramètres clés |
|------|------|--------------|-----------------|
| **Rotation ambisonique** | **1** | Mouvement **continu** — droite ↔ gauche, avant ↔ arrière (`phi` → encode → decode) | `rot_speed`, `SENS` (Q38) |
| **Séquence HP** | **3** | Saut **binaire** baffle par baffle : HP1 → HP2 → HP3 → HP4 → … | `step_min_ms`, `step_max_ms`, `jump_xfade` (leftover au passage) |

| | |
|---|---|
| **BOUCLE + HIPPO** | Strates **profondes** — **presque tout** peut arriver (modes SPAT, FX, variantes) ; BOUCLE = **1 lecteur actif** strict (Q47), HIPPO = **superpositions** possibles |
| **Opposé** (2 couches) | **SPAT=1** : sens `SENS` contraires · **SPAT=3** : séquence **inversée** (ex. 1→2→3→4 vs 4→3→2→1) |
| **F3** | Plages **séparées** : `rot_speed` (mode 1) **et** `step_min/max` + `xfade` (mode 3) |

#### F.0.1 Modèle fond + superposition — qui bouge comment (acté)

**Scénario visé** (HIPPO surtout ; BOUCLE = 1 sample actif mais **même palette spatiale** en variantes) :

```text
[FOND]     sample déjà en cours — peut bouger de façon INDÉPENDANTE (ambi ou séquence)
              │
              ▼ superposition
[ARRIVÉE 1]  nouveau sample — se balade en SÉQUENCE baffle par baffle (SPAT=3)
              │   · quelques « tours » (cycles HP) puis PAUSE — pas continu en permanence
              ▼ autre sample, même logique de superposition
[ARRIVÉE 2]  2e ajout — se déplace en AMBISONIQUE (SPAT=1) sur le fond + l’autre couche
```

| Rôle | Sample | Superposition | Mode SPAT par défaut | Mouvement |
|------|--------|---------------|----------------------|-----------|
| **Fond** | 1er en cours | — (référence) | ambi **ou** séquence (tirage / preset) | **Indépendant** des arrivées — propre `phi` ou propre séquence |
| **1ère arrivée** | 2e déclenché | **Oui** sur le fond | **SPAT=3** (séquence HP) | Baffle par baffle + **leftover** (`jump_xfade`) ; **tours limités** puis repos |
| **2e arrivée** | 3e déclenché | **Oui** sur fond + 1er | **SPAT=1** (ambi) | Déplacement **continu** de **cette couche seule** ; fond et 1ère arrivée gardent leur propre mouvement |
| **Durée** | Dernier arrivé | — | — | **Le plus court** (Q50) — mute en premier |

**Règles importantes :**

| Règle | Détail |
|-------|--------|
| **Pas de mouvement continu permanent** | Phase active (**pattern** P1–P6) → **repos oscillant** P7 — jamais métronome infini |
| **Indépendance** | Chaque couche = **bus FX + encode** séparés (Q49 B) → le fond **ne suit pas** l’arrivée |
| **Séquence = superposition** | C’est bien le **nouvel élément** qui **traverse les baffles** en séquence **par-dessus** le fond — pas le fond qui « devient » séquence par obligation |
| **Ambi = 2e ajout** | L’**ambisonique** concerne surtout le **deuxième sample superposé** (3e couche active) ; le fond peut aussi être ambi, mais **à son rythme** |
| **BOUCLE (Q47)** | **Un seul** `readsf~` actif à la fois — pas de 2 samples superposés ; le « fond » = sample courant + **queue FX** de la couche précédente |

**Lien F2 (ajusté) :** à 3 couches actives, le **dernier arrivé** (2e superposition) = **ambi** + **durée la plus courte** ; position **fixe** = variante rare ou 3e accent très bref (F2 initial), pas la règle principale.

```text
Exemple 3 couches HIPPO :
  t=0   Fond MLK — ambi lent, indépendant
  t=2   Arrivée radio — séquence HP1→2→3→4 (2 tours) puis pause
  t=5   Arrivée voix — ambi, sens opposé au fond ; mute en premier à t≈7
```

#### F.0.2 Catalogue de trajectoires — tours non linéaires + repos oscillant (acté)

**Principe des « tours » :**

| | |
|---|---|
| **Ce n’est pas** | Un cercle **rempli** en continu, ni une boucle **linéaire** obligatoire 1→2→3→4→1… |
| **C’est** | Une **plage de mouvement** où le sample **s’écarte** de son baffle d’origine, puis **revient** vers une zone d’ancrage |
| **Fin de phase** | Pas de **statique** strict — passage au **repos oscillant** (voir P7) |

**Pas d’aléatoire pur :** tirage dans un **catalogue** de patterns nommés (`fsm_presets` / `spatial_stepseq`) — poids probabilistes, pas `random(4)` sur chaque saut.

##### Patterns séquence (SPAT=3) — brouillon à valider à l’écoute

| ID | Nom | Description | Exemple (4 HP) |
|----|-----|-------------|----------------|
| **P1** | **Zigzag** / va-et-vient | Aller-retour, peut **revenir** sur le baffle précédent ; sensation droite↔gauche | `1 → 4 → 3 → 4 → 1 → 2 → 3` |
| **P2** | **Tour harmonique CW** | Cycle **complet** horaire, une ou **plusieurs** boucles | `1 → 2 → 3 → 4 → 1` (×N) |
| **P3** | **Tour harmonique CCW** | Cycle **complet** antihoraire | `1 → 4 → 3 → 2 → 1` (×N) |
| **P4** | **Ping-pong croisement** | 2 samples, sens opposés, **rebond** au croisement (Q43–44) | A: 1→2→… B: 4→3→… → flip au meet |
| **P5** | **Ping-pong parallèle** | 2 samples, **sans** croisement — va-et-vient sur baffles opposés | A: 1↔3 , B: 2↔4 |
| **P6** | **Croisement + dépassement** | Les deux **se croisent** et **continuent** (pas de rebond) | trajectoires qui se traversent |

→ Retour possible sur le **baffle juste avant** (ex. 4 → 3 → **4**) — **autorisé** et souhaité pour P1.

##### Phase repos — oscillation lente (hybride séquentiel + ambi)

| ID | Nom | Comportement |
|----|-----|--------------|
| **P7** | **Repos oscillant** | Après P1–P6 : **pas** fixe — **oscillation lente** autour d’un **`anchor_hp`** (baffle pivot) |
| | | Séquentiel **léger** (micro-sauts) **+** **`phi` ambi** lent : sensation arrière/gauche puis droite, toujours **autour** du pivot |
| | | Durée **variable** (moment plus ou moins long) avant prochaine phase active |

```text
Phase active (P1 zigzag)     Phase repos (P7)
HP1 → HP4 → HP3 → HP4 …  →   oscillation lente autour de HP3 (anchor)
                               (ambi + micro-séquence, pas silence spatial)
```

**Implémentation cible :**

| Composant | Rôle |
|-----------|------|
| `spatial_stepseq.pd` | Tables de patterns P1–P6 (listes HP, pas seulement +1 mod 4) |
| `fsm_presets` | `pattern_id`, `pattern_tours` ou durée phase, `anchor_hp`, poids par pattern |
| Couche ambi (SPAT=1) | P7 et 2e superposition (F.0.1) — `phi` LFO lent autour de l’ancre |

**À faire ensuite :** calibrer poids des patterns (§M) — éviter que l’expérience soit **trop aléatoire**.

1. ~~HIPPO = **dialogue de fragments**…~~ → **Répondu** — voir F.1.

#### F.1 Dialogue spatial — interlocuteurs en mouvement (acté)

| | |
|---|---|
| **Interlocuteurs** | **Oui** — 2–3 voix spatialisées comme un **dialogue** (baffles **opposés** / séparés — Q36) |
| **Statique ?** | **Jamais** vraiment fixe — après phase active → **repos oscillant** (P7, F.0.2) |
| **Mouvement** | Modèle **fond + superposition** (F.0.1) : arrivée → **séquence** ; 2e ajout → **ambi** ; fond **indépendant** |
| **Effet visé** | Fragments qui **se superposent** au fond en **traversant** l’espace — pas tout en mouvement continu |

```text
Fond (déjà là)     —— mouvement propre (ambi ou séquence, indépendant)
+ Arrivée 1        —— séquence HP, quelques tours, leftover au passage
+ Arrivée 2 (opt.) —— ambi sur cette couche ; part la première
```

2. ~~Rotation opposée : prioritaire sur **2 couches**…~~ → **Répondu** — voir F.2.

#### F.2 Trois couches — rôles fond / arrivées (acté, précisé F.0.1)

| Nb couches | Rôles |
|------------|-------|
| **1** | **Fond** seul — mouvement libre (BOUCLE : 1 lecteur strict, Q47) |
| **2** | **Fond** + **1ère arrivée** : fond indépendant ; arrivée en **séquence HP** (SPAT=3), tours limités |
| **3** | **Fond** + **arrivée 1** (séquence) + **arrivée 2** (**ambi**, SPAT=1) — **dernier arrivé** = le plus court (Q50) |

| Couche | Mouvement (défaut) |
|--------|-------------------|
| **Fond** | Indépendant — ambi **ou** séquence (preset) |
| **1ère superposition** | **SPAT=3** — pattern catalogué (P1–P6), phase limitée puis **P7** |
| **2e superposition** (3e active) | **SPAT=1** — ambi **de cette couche** ; fond + 1ère gardent leur trajectoire |
| **Dernier arrivé** | **Durée minimale** ; souvent le 2e ajout (ambi) — pas « fixe » par défaut (variante fixe possible, rare) |

**RECONSTRUCTION :** même logique spatiale qu’HIPPO (Q46) — règle applicable aussi à 3 couches en RECON.

3. ~~`[PLAGE]` Vitesse rotation HIPPO…~~ → **Reformulée** — voir ci-dessous.

> **F3 — deux jeux de plages** (calibration à l’écoute, §M) :
>
> | Mode | Paramètres | Question |
> |------|------------|----------|
> | **SPAT=1** (ambi) | `rot_speed` min / max (pas 0.01) | Vitesse de rotation continue |
> | **SPAT=3** (séquence) | `step_min_ms` / `step_max_ms` | Temps sur chaque baffle avant le suivant |
> | **SPAT=3** | `jump_xfade` min / max (ms) | **Leftover** — fondu / queue au passage entre baffles |
> | **Tours** | `seq_tours_min` / `seq_tours_max` | Cycles du **pattern** (pas forcément tour complet linéaire) |
> | **Patterns** | `pattern_id` + **poids** | Catalogue **P1–P7** (F.0.2) — **pas** saut HP aléatoire pur |
> | **Repos** | `anchor_hp` + osc. lente | Phase **P7** après mouvement actif |
>
> → Calibrer à l’écoute (§M). Voir **F.0.1** (rôles) et **F.0.2** (trajectoires).

4. ~~Delay sur HIPPO…~~ → **Répondu** — voir F.4.

#### F.4 Delay, densité d’information et filtres — probabilités (acté)

**Principe global (toutes procédures) :** **probabilités** et **dynamique** — **pas** de règles strictes « delay obligatoire / absent » par variante.

**Objectif HIPPO (et strates profondes) :**

| | |
|---|---|
| **Sensation** | **Beaucoup d’informations** — mais **pas trop en même temps** |
| **Moyens** | **Delay** (remplit l’espace) **ou** **superpositions** (voix + dB) — plutôt **l’un ou l’autre**, sans règle fixe |
| **Référence sonore** | Son **HIPPO actuel** (proto 05) **apprécié** — delay FLUID + filtrage + ambisonique : **à conserver** comme base |

**Balance delay ↔ superposition (dynamique, probabiliste) :**

| Situation | Tendance delay | Notes |
|-----------|----------------|-------|
| **Peu / pas de superposition** | **Plus** de delay (wet ↑) | Le delay **comble** l’espace informationnel |
| **Voix / éléments superposés** | **Peu** de delay (wet ↓, parfois off) | Les couches **ajoutent** déjà info + niveau |
| **Les deux forts en même temps** | **À éviter** souvent — tirage défavorable | Surcharge (Q40 — pas 3 delays lourds) |
| **Filtres** | HPF / LPF pour **atténuer** quand la densité monte | Complément au delay variable |

→ Implémentation : **poids** dans `fsm_presets` selon `nb_couches_actives`, `layout` (séparation / superposition), pas un booléen `delay_on` fixe par variante.

**Strates profondes — BOUCLE + HIPPO :**

| État | Delay | Superposition |
|------|-------|---------------|
| **HIPPOCAMPE** | **Presque tout le temps** — mais **mesuré**, ajusté aux arrivées (F.0.1) | Fond + arrivées (dynamique) |
| **BOUCLE** | **Presque tout le temps** (comportement actuel apprécié) | **Par moments** : voix superposées **ou** sample **isolé sur un baffle** — **probabiliste**, pas permanent |

**Précision BOUCLE (affine Q47) :**

| Q47 (acté) | F4 (précision) |
|------------|----------------|
| Pas de **2 lecteurs** actifs en permanence | **Variante probabiliste** : superposition **brève** ou 2e voix **par moments** |
| Saut **strict** couche → couche (défaut) | **Ou** isolation totale sur **1 baffle** (tirage) |
| Queue FX entre couches | Inchangé |

```text
Densité informationnelle ≈ f(nb_voix_superposées, delay_wet, filtres)
  superposition ↑  →  delay_wet ↓  (tendance probabiliste)
  superposition ↓  →  delay_wet ↑
```

**Lien Q41 :** le delay reste le **levier FX principal** par couche — ici piloté par **contexte** (superposition présente ou non), pas par état seul.

5. ~~Phaser vs filtre+LFO en HIPPO…~~ → **Répondu** — voir F.5.

#### F.5 Phaser vs filtre+LFO — 50/50 (acté)

| | |
|---|---|
| **Tirage** | **50/50** entre **phaser** et **filtre+LFO** sur les variantes HIPPO |
| **Préférence** | **Aucune** — les deux traitements sont **équiprobables** |
| **Cohérence** | S’inscrit dans l’approche **probabiliste** (F4, Q22) — pas de règle fixe par variante |
| **Delay** | Inchangé (F4) — phaser / filtre+LFO en **complément**, pas en remplacement du delay dynamique |

→ Implémentation : poids **~50 %** `fx_phaser` / **~50 %** `fx_filter_lfo` dans le pool variantes HIPPO (`fsm_presets`).

---

## G. RECONSTRUCTION

1. ~~RECON = **mémoire recomposée**…~~ → **Répondu** — **Oui**, confirmé (Q46).

#### G.1 Identité RECONSTRUCTION (acté)

| | |
|---|---|
| **Superposition** | **Limitée** |
| **Spatial** | **Identique à HIPPO** (F.0.1, patterns F.0.2) |
| **Timbre** | **Moins filtré**, **plus saturé** que HIPPO / BOUCLE (Q46) |
| **Densité** | **Moins** de couches simultanées qu’HIPPO — montée vers la clarté |

2. ~~SPAT manuel (phi)…~~ → **Répondu** — voir G.2–G.3.

#### G.2 Phi — lent, indépendant, sample-dépendant (acté)

| | |
|---|---|
| **Défaut** | **`phi` lent**, **indépendant par couche** (SPAT=1 ambi) |
| **Intensité** | **Faible** par défaut (on approche CORTEX) — mais encore **un peu flou**, mouvement **visible** |
| **Vitesse** | **Pas trop rapide** — on doit **sentir** que ça bouge |
| **Sample** | Couches liées aux **samples** en entrée — parfois **statique** (sans `phi`) selon le fichier |
| **vs HIPPO** | Moins de mouvement / moins de densité ; **plus clair** qu’en strates profondes |

#### G.3 Plages phi RECON — aller-retour, pas cercle plein (acté)

| Paramètre | Cible |
|-----------|--------|
| **Vitesse** | **Assez lente** — `[PLAGE]` deg/s à calibrer (§M) |
| **Amplitude** | Jusqu’à **±180°** — **autorisé** et souhaité |
| **Trajectoire** | **Aller-retour** — peut **partir et revenir** ; **pas** de rotation circulaire qui **remplit** le cercle en continu (comme F.0.2) |
| **Patterns** | Réutiliser logique **P1 / P7** adaptée ambi : oscillation autour d’une position, pas tour complet obligatoire |

```text
phi :  0° ──► 120° ──► 180° ──► 90° ──► …   (va-et-vient, pas 0→360 en boucle)
```

3. ~~`[PLAGE]` Vitesse phi…~~ → **Orienté** — lent, ±180°, aller-retour (G.3) ; bornes numériques §M.

4. ~~Delay long + feedback…~~ → **Répondu** — voir G.4.

#### G.4 Delay et FX — décalé, dynamique, atténuable (acté)

| | |
|---|---|
| **Par couche** | Delay + feedback **décalés** — **temps différent** sur chaque couche |
| **À chaque retour** | Même couche réactivée → delay peut être **nettement différent** (nouveau tirage dans plage) |
| **Catégories** | **Long** pour couches « **basses** » / profondes · **Plus court** pour couches « **hautes** » / proches clarté — toujours **dynamique** |
| **Densité** | Alternance **beaucoup d’info** ↔ **peu d’info** (ou info **atténuée**) — même logique probabiliste que F4 |
| **FX violents** | Tous les effets **peuvent** être forts — il faut pouvoir les **atténuer** et les **relancer** (`wet`/`on` dynamiques par couche) |

```text
Couche A (profonde) : delay long 420ms, fb 0.6
Couche B (haute)      : delay court 180ms, fb 0.3
Reprise couche A      : delay 380ms (nouveau tirage — pas copie figée)
```

**Lien Q41 :** delay = levier principal — ici **variable** à chaque activation de couche.

5. ~~`[PLAGE]` wet / fb RECON…~~ → **Répondu** — voir G.5.

#### G.5 Wet / feedback RECON — bas par défaut, pics brefs (acté)

**Position dans la montée narrative :** RECON = strate **haute** (proche CORTEX) → **wet** et **feedback** **plus bas** que BOUCLE et HIPPO.

| | |
|---|---|
| **Défaut** | **Assez bas** — `wet` et `fb` **modérés / contenus** (à calibrer §M) |
| **vs strates profondes** | **Inférieur** aux niveaux BOUCLE / HIPPO — moins de « nuage » delay |
| **Pics** | Si montée forte : **instantanée** et **brève** — pas de plateau long à wet élevé |
| **Dynamique** | Effets **variables** — atténuation / relance (G.4) ; cohérent F4 (densité info) |

**Plages indicatives (à affiner à l’oreille — §M) :**

| Paramètre | RECON (défaut) | BOUCLE / HIPPO (réf.) |
|-----------|----------------|------------------------|
| `fluid_wet` | **bas** — ex. ~0.15–0.35 | souvent **plus haut** |
| `fluid_fb` | **bas** — ex. ~0.2–0.45 | souvent **plus haut** |
| **Pic bref** | spike possible → retour bas en **< ~2 s** | — |

```text
RECON défaut :  wet ▁▁▁▂▁▁▁  (bas, stable)
Pic autorisé :  wet ▁▁▁▅▁▁▁  (montée rapide, courte)
```

→ Implémentation : enveloppe **AD** courte sur `wet`/`fb` si tirage « pic » ; plafond RECON **<** presets HIPPO dans `fsm_presets`.

---

## H. BOUCLE

0. ~~Couches simultanées…~~ → **Répondu** — voir E.9, F4 (défaut 1 lecteur ; superposition **prob.**).

1. ~~BOUCLE = **obsession** — re-clics…~~ → **Répondu** — voir H.1.

#### H.1 Fichier au re-clic FORCE — même par défaut (acté)

| | |
|---|---|
| **Défaut** | **Garder le même fichier** — obsession, phrase dominante qui revient |
| **Changement** | **Possible** mais **non prioritaire** — tranquillement, pas à chaque clic |
| **Lien Q27** | Re-clic = **SPAT + FX** ; `open` nouveau fichier = **exception** |

2. ~~`[PLAGE]` jump_min / jump_max BOUCLE…~~ → **Répondu** — voir H.2.

#### H.2 Sauts spatiaux BOUCLE — longs, puis rapides brefs (acté)

| Mode | Comportement |
|------|--------------|
| **Défaut** | Intervalles **assez longs** entre sauts HP — séjour sur chaque baffle |
| **Rapide** | **300–400 ms** entre sauts — sur une fenêtre **courte** (~**3–4 s**) seulement |
| **Dynamique** | Alternance long ↔ burst rapide — pas métronome fixe (§16.5) |

**Plages proposées (§M — à valider) :**

| Paramètre | Lent (défaut) | Rapide (burst) |
|-----------|---------------|----------------|
| `jump_min_ms` | **3 000** | **300** |
| `jump_max_ms` | **10 000** | **400** |
| Durée burst | — | **3 000 – 4 000 ms** |

3. ~~Variante delay léger vs fort…~~ → **Répondu** — voir H.3.

#### H.3 Delay BOUCLE — plafond du projet + plages par strate (acté)

**Référence approuvée (proto 05 actuel — ne jamais dépasser) :**

| Paramètre | Valeur **plafond** BOUCLE |
|-----------|---------------------------|
| `fluid_wet` | **0,85** |
| `fluid_delay` | **800 ms** |
| `fluid_fb` | **0,70** |
| `fluid_lfo` | **0,50** |

→ **BOUCLE = delay le plus fort de tout le projet** ; HIPPO / RECON / CORTEX **toujours en dessous**.

**Variantes BOUCLE :** privilégier delay **fort** (comportement actuel apprécié) ; léger = **minoritaire** (~**20–30 %** tirage).

**Plages de tirage par strate** (différent à chaque activation — §M) :

| Strate | `wet` | `delay` (ms) | `fb` | `lfo` | Notes |
|--------|-------|--------------|------|-------|-------|
| **BOUCLE** | 0,65 – **0,85** | 600 – **800** | 0,50 – **0,70** | 0,35 – **0,50** | **Plafond** = tableau ci-dessus |
| **HIPPO** | 0,30 – 0,65 | 250 – 600 | 0,25 – 0,55 | 0,15 – 0,45 | ↓ si superposition (F4) |
| **RECON** | 0,15 – 0,35 | 150 – 400 | 0,20 – 0,45 | 0,10 – 0,35 | Pic bref possible (G5) |
| **CORTEX** | **off** | — | — | — | Filtre+LFO (pas delay) |

```text
Intensité delay :  BOUCLE ████████░░  HIPPO █████░░░░░  RECON ███░░░░░░░  CORTEX ░
```

→ Chaque reprise de couche : **nouveau tirage** dans la plage (G4 RECON, dynamique global).

4. ~~SPAT séquence vs saut en BOUCLE…~~ → **Répondu** — voir H.4.

#### H.4 SPAT BOUCLE — saut vs séquence 50/50 (acté)

| | |
|---|---|
| **SPAT=2** (saut HP) | **50 %** |
| **SPAT=3** (séquence HP) | **50 %** |
| **Préférence** | **Aucune** — équiprobable à chaque variante / tirage |

→ Implémentation : poids **~50/50** dans `fsm_presets` BOUCLE.

5. ~~Saturation marquée en BOUCLE…~~ → **Répondu** — voir H.5.

#### H.5 Saturation BOUCLE — dynamique, phases clarté (acté)

| | |
|---|---|
| **Saturation** | **Oui** en BOUCLE — module dès **proto 07** (ou atténuation proto 05 si pas encore dispo) |
| **Statique ?** | **Non** — doit **apparaître** et **disparaître** (macro dynamique) |
| **Cohérence** | Même logique **probabiliste** que delay (F4, H3) |

**Cycle macro exemple (au sein d’une phase BOUCLE) :**

```text
1. Clarté      : delay OFF ou très faible     (~quelques s)
2. Montée      : saturation + phaser ↑        (~2–4 s)
3. Retour      : delay fort (~70 % wet/fb réf. H3), sans distorsion
4. (répétition ou sortie d’état)
```

| Phase | Delay | Saturation / phaser |
|-------|-------|---------------------|
| **Clarté dans BOUCLE** | **off** ou **très faible** | **off** ou minimal |
| **Montée** (2–4 s) | réduit | **saturation + phase** augmentent |
| **Retour obsession** | **fort** (plafond H3, ~70 %) | **off** — pas de disto persistante |

→ Même dans la strate la plus **profonde**, des **îlots de clarté** sont possibles avant de replonger dans le delay dense.

**Implémentation :** séquence d’états FX interne ou `preset_phase` dans FSM BOUCLE ; durées **2–4 s** pour la montée sat/phase (§M).

---

## I. SPAT — modes et plages

1. ~~Quels modes SPAT sont **autorisés** par état ?~~ → **Répondu** — voir I.1.

#### I.1 Modes SPAT autorisés par état (acté)

**Règle globale :** *a priori*, **tous les modes** peuvent exister **partout** — y compris l’application des **FX sur les samples superposés**. Les tableaux ci-dessous décrivent les **familles privilégiées** par strate, pas une interdiction technique absolue (sauf debug `SPAT_LAYOUT`).

| État | Manuel 0 (dry) | Rotation 1 | Saut 2 | Séquence 3 |
|------|----------------|------------|--------|------------|
| **BOUCLE** | **non** (strates profondes) | **oui** | **oui** (50 % vs seq, H4) | **oui** (50 % vs saut, H4) |
| **RECON** | **oui** | **oui** | **oui** | **oui** |
| **HIPPO** | **oui** (base) | **oui** (base) | flash superposition | flash superposition |
| **CORTEX** | **oui** (base) | **oui** (base) | flash superposition | flash superposition |

**Logique par strate :**

| Strate | Modes « normaux » | Raison |
|--------|-------------------|--------|
| **BOUCLE** | **saut + séquence + rotation** — **pas** dry/manuel | Chaos déjà fort (sample de base + superpositions probables) → spatial **actif** |
| **RECON** | **dry + saut + séquence + rotation** | Même logique de chaos sur superposition / base ; **dry** possible pour respiration |
| **HIPPO** | **dry + rotation** en régime courant | Strate intermédiaire — mouvement **continu** ou **fixe** |
| **CORTEX** | **dry + rotation** en régime courant | Clarté / parole — ancrage ou rotation lente |

**Superposition flash (HIPPO + CORTEX) :** lors d’un overlap bref, le spatial de la couche flash peut être **séquence**, **saut** ou **rotation** — tirage parmi ces trois (pas dry).

```text
HIPPO / CORTEX (régime)
  couche principale     → SPAT=0 (dry) ou SPAT=1 (rotation)
  flash superposition   → SPAT=2 | SPAT=3 | SPAT=1  (bref)

BOUCLE / RECON (régime)
  pas de dry par défaut (BOUCLE) / dry possible (RECON)
  → saut | séquence | rotation selon variante
```

**Cohérences existantes :**

- **H4** : entre **saut** et **séquence** en BOUCLE → **50/50** ; **rotation** s’ajoute au pool BOUCLE (poids §M).
- **F.0.1** : arrivée HIPPO en séquence, 2e en ambi — compatible avec « flash = seq/saut/rotation ».
- **G2–G3** : RECON phi lent aller-retour — compatible avec rotation + dry.

**Implémentation :** `fsm_presets` — champ `spat_mode` + `spat_mode_flash` (HIPPO/CORTEX) ; validation des combinaisons par `variante_id`.

| État   | Manuel 0 | Rotation 1 | Saut 2 | Séquence 3 |
| ------ | -------- | ---------- | ------ | ---------- |
| CORTEX | **oui** (base) | **oui** (base) | flash | flash |
| HIPPO  | **oui** (base) | **oui** (base) | flash | flash |
| RECON  | **oui** | **oui** | **oui** | **oui** |
| BOUCLE | **non** | **oui** | **oui** (H4) | **oui** (H4) |


1. `[PLAGE]` Saut CORTEX : `jump_min_ms` / `jump_max_ms` = … / … ?
2. `[PLAGE]` Saut BOUCLE : `jump_min_ms` / `jump_max_ms` = … / … ?
3. `[PLAGE]` Séquence HIPPO : `step_min_ms` / `step_max_ms` = … / … ?
4. `[PLAGE]` `jump_xfade` par état : min / max (ms) ?
5. `[PLAGE]` `rot_speed` global : min / max, pas 0.01 ?
6. ~~Mode **séquence HP**…~~ → **Répondu** — **les deux** : SPAT=1 (ambi) **et** SPAT=3 (séquence) restent en HIPPO — variantes / tirages, **pas** de remplacement (F.0).
7. ~~En rotation ambisonique…~~ → **Répondu** — voir I.7.

#### I.7 Rotation — continu (défaut) vs baffle par baffle (option) (acté)

| | |
|---|---|
| **Défaut** | Mouvement **continu** ambisonique (**SPAT=1**) — **très bien**, à conserver |
| **Option** | Perception **baffle par baffle** aussi **souhaitée** — pas de remplacement du continu |
| **Implémentation** | **SPAT=3** (séquence HP) ou variante preset ; tirage parmi les variantes / patterns |

```text
Rotation « organique »     SPAT=1  — phi continu → encode → decode  (DÉFAUT)
Lecture discrète HP        SPAT=3  — HP1→2→3→4 + leftover           (OPTION)
```

→ Les **deux** restent dans le pool (§13.3) : le continu domine en **régime courant** HIPPO/CORTEX/RECON ; la séquence sert les **arrivées** (F.0.1), les **flash** (I.1), et les variantes où l’on veut une **lecture pédagogique** baffle par baffle.

**Pas de fusion** des deux modes en un seul — ce sont des **perceptions distinctes**, complémentaires.

---

## J. Effets — Delay, filtre, phaser, saturation

1. ~~Renommage UI…~~ → **Répondu** — voir J.1.

#### J.1 Renommage UI — ECHO (acté)

| | |
|---|---|
| **Label UI** | **ECHO** |
| **DELAY** | Non retenu comme label principal |
| **Sous-label** | Aucun — un seul nom : **ECHO** |

→ Renommer `FLUID_FX` → **`ECHO`** dans l’UI ; messages internes `fluid_*` peuvent rester en code jusqu’au refactor.

2. ~~`[PLAGE]` wet delay global…~~ → **Non tranché** — voir J.2.

#### J.2 Wet delay global — à calibrer (§M)

| | |
|---|---|
| **Décision** | **Pas encore fixée** — session d’écoute |
| **Références** | Plafond BOUCLE **H3** (wet 0,85) ; RECON bas **G5** ; CORTEX **off** |

→ Conserver les plages §M existantes ; valider le plafond « confortable » hors BOUCLE à l’oreille.

3. ~~`[PLAGE]` feedback delay…~~ → **Répondu** — voir J.3.

#### J.3 Feedback delay — plafond 0–70 % (acté)

| | |
|---|---|
| **Plage** | **0 % – 70 %** (`fluid_fb` ∈ [0, 0,70]) |
| **Plafond projet** | **0,70** — cohérent **H3** (BOUCLE) |
| **CORTEX** | Delay **off** — fb non applicable |

→ Les autres états restent **sous** ce plafond (G5 RECON bas par défaut).

4. ~~Filtre+LFO CORTEX…~~ → **Répondu** — voir J.4.

#### J.4 Filtre CORTEX — HPF / LPF / résonance (acté)

Module **filtre + LFO** (proto 07) — plages de tirage par variante :

| Paramètre | Min | Max | Notes |
|-----------|-----|-----|-------|
| **HPF** (coupe-bas) | **20 Hz** | **1 200 Hz** | Respiration / masque progressif |
| **LPF** (coupe-haut) | **1 200 Hz** | **20 000 Hz** | De très ouvert à plus sombre |
| **Résonance** | — | **~1 %** | **Très peu** — pas de résonance marquée |

→ LFO rate / mix : **à calibrer §M** (défaut très léger, §15.7 plan).

5. ~~LFO sur le delay…~~ → **Répondu** — voir J.5.

#### J.5 LFO sur le delay — garder (acté)

| | |
|---|---|
| **`fluid_lfo`** | **Garder** — modulation du temps de delay |
| **Plafond** | Réf. **H3** BOUCLE : 0,50 max ; autres états en dessous |

6. ~~Saturation…~~ → **Répondu** — voir J.6.

#### J.6 Saturation — routage par couche (acté)

| Cible | Saturation |
|-------|------------|
| **Couche principale BOUCLE** | **Prédominante** — dynamique (H5) |
| **Couche principale HIPPO** | **Oui**, **moins forte** que BOUCLE |
| **Couche principale RECON** | **Non** |
| **Couche principale CORTEX** | **Non** |
| **Samples superposés** (toutes strates) | **Oui** — peut apparaître sur **toute** couche d’overlap |

```text
Principal     BOUCLE ████████░░  HIPPO ████░░░░░░  RECON ░  CORTEX ░
Superposé     toutes strates → saturation possible (intensité selon preset)
```

**Cohérence G1 :** RECON « plus saturé » que HIPPO/BOUCLE = **moins de filtre** + vivacité timbrale — **pas** saturation fixe sur la couche principale (J.6 prime pour le module sat).

**Implémentation (Q49 B) :** saturation sur **bus par couche** ; flag `sat_on_main` vs `sat_on_overlay`.

7. ~~Atténuation highs post-saturation…~~ → **Répondu** — voir J.7.

#### J.7 Compensation de gain saturation — proportionnelle ×1,5 (acté)

| | |
|---|---|
| **Principe** | **Proportionnalité** : plus on **monte** le drive / gain d’entrée ou le **dry/wet** de la saturation, plus on **baisse** le volume de sortie |
| **Facteur** | **×1,5** — coefficient de référence pour la courbe de compensation |
| **But** | Éviter les pics de niveau quand la sat s’intensifie (H5, J6) |

**Formule indicative (Pd) :**

```text
sat_amount = combine(drive, sat_wet)     // intensité d’entrée 0..1
gain_comp  = 1 / (1 + sat_amount × 1.5)  // à affiner à l’oreille (§M)
out~ = saturate(in~) *~ gain_comp
```

→ Pas un plafond fixe en dB : la **réduction suit** l’intensité du module. Atténuation highs post-sat possible en plus — **à calibrer** si besoin.

8. ~~Ordre de priorité implémentation FX…~~ → **Répondu** — voir J.8.

#### J.8 Ordre d’implémentation FX (acté)

| Priorité | Module | Notes |
|----------|--------|-------|
| **1** | **Saturation** | BOUCLE / superposés (J6) — proto 07 en premier |
| **2** | **Filtre** (HPF/LPF) | CORTEX (J4) ; HPF/LPF HIPPO/BOUCLE (F4) |
| **3** | **LFO** | Sur filtre (CORTEX) ; `fluid_lfo` ECHO déjà en place (J5) |
| **4** | **Phaser** | HIPPO 50/50 vs filtre+LFO (F5) — en dernier |

```text
Proto 07 :  saturation → filtre → LFO → phaser
             (inverse de la proposition initiale J.8)
```

→ **Section J : complète** (J.1–J.8 actés ou renvoyés §M).

---

## K. Contenu audio — SONS/

1. ~~Les 5 WAV actuels suffisent…~~ → **Répondu** — voir K.1.

#### K.1 Matériel disponible — insuffisant pour Paris (acté)

| | |
|---|---|
| **Suffisant pour Paris ?** | **Non** — matériel encore trop limité |
| **Matériel actuel** | **Seul stock disponible** ; reste des archives **récupéré récemment** |
| **Découpe demandée** | Sources longues → parties égales (3 ou 10 selon fichier) |

**Fichiers créés** (`scripts/split_long_sources_thirds.sh`) :

| Source | Parties | Durée / partie | Préfixe |
|--------|---------|----------------|---------|
| `Voix pour la danse fin.wav` (~9 min) | **3** | ~3 min 7 s | `parts/voix_danse_part{1,2,3}.wav` |
| `cheick anta diop.wav` (~8 min) | **3** | ~2 min 42 s | `parts/cheick_diop_part{1,2,3}.wav` |
| `radio campus rencontre.wav` (~120 min) | **10** | ~12 min | `parts/radio_campus_part{01..10}.wav` |

→ Si d’autres découpages sont souhaités, ajuster le script (`split_parts` + nombre).

**Durées sources complètes** (réf.) :

| Fichier | Durée |
|---------|-------|
| `radio campus rencontre.wav` | **~120 min** → **10 × ~12 min** |
| `Voix pour la danse fin.wav` | **~9 min 20** |
| `cheick anta diop.wav` | **~8 min** |
| `Martin Luther King.wav` | **~2 min 25** |
| `keren 5 bon.wav` | **~1 min** |

2. ~~Interdire certains extraits…~~ → **Répondu** — voir K.2.

#### K.2 Interdictions extrait × état — non (acté)

| | |
|---|---|
| **Règle** | **Aucune interdiction** — tout extrait peut servir dans tout état |
| **Tirage** | Pondération / variantes possibles plus tard, pas de blocage dur |

3. ~~Minimum segments par case…~~ → **Répondu** — voir K.3.

#### K.3 Minimum segments État × Durée — à définir

| | |
|---|---|
| **Décision** | **Pas encore fixée** |
| **Prochaine étape** | Session de **classification** à l’oreille + inventaire `SONS/` |

4. ~~Fichiers multi-états…~~ → **Répondu** — voir K.4.

#### K.4 Multi-états — clarification (acté)

**Question :** le **même extrait source** (ex. `keren 5 bon.wav`) est découpé et placé dans **plusieurs dossiers d’état** (`SONS/BOUCLE/…`, `SONS/HIPPOCAMPE/…`, etc.). Faut-il **éviter** ou **favoriser** ça ?

| | |
|---|---|
| **Réponse** | **Autorisé** — pas de règle stricte |
| **Pratique actuelle** | `slice_extracts.sh` place déjà le même source dans 2–4 états |
| **Préférence** | Ni à éviter ni à imposer — **neutre** |

5. ~~Durée max segment…~~ → **Répondu** — voir K.5.

#### K.5 Durée max segment — 1 min 30 (acté)

| | |
|---|---|
| **Plafond** | **90 s** (**1 min 30**) par segment découpé dans `SONS/` |
| **Impact grille** | `MOYEN` / `LONG` actuels (> 60 s) à **réviser** — voir §08 |

→ **Section K : complète** (K.3 en attente classification).

---

## L. Technique, matériel, installation

1. ~~Config définitive proto 05…~~ → **Répondu** — voir L.1.

#### L.1 Nommage prototype — Proto 06 (4 HP + 6 HP) (acté)

| | |
|---|---|
| **Proto 05** | **Figé** — état actuel du code (`prototype_05_fsm.pd`) ; **pas** les grosses implémentations Q&A |
| **Proto 06** | **Nouveau prototype** — toute l’implémentation lourde (FSM complète, multi-bus, FX, presets, SONS…) |
| **Variantes proto 06** | **Deux patches** distincts |

| Variante | HP | Session | Fichier cible (à créer) |
|----------|-----|---------|-------------------------|
| **Proto 06 — 4 HP** | 4 | **Aujourd’hui** (test) | `pd/prototype_06_fsm_4hp.pd` |
| **Proto 06 — 6 HP** | 6 | **Samedi** (nouvelle paire HP) | `pd/prototype_06_fsm_6hp.pd` |

→ Le Q&A `09_*` et le plan `06_*` décrivent la **cible proto 06** ; le générateur partira de `gen_prototype_06.py` (à créer).

**Décalage roadmap :** l’ancien « proto 06 interaction (piezo) » devient **proto 07** — voir `07_roadmap_prototypes_finale.md` §1.

2. ~~Sorties carte…~~ → **Répondu** — voir L.2.

#### L.2 Sorties carte son — confirmées (acté)

| Config | Sorties `dac~` | Notes |
|--------|--------------|-------|
| **4 HP** | **1, 2, 3, 4** | **Confirmé** toutes sessions |
| **6 HP** | **1, 2, 4, 5, 6** | Sortie **3 non utilisée** — confirmé pour session samedi |

3. ~~Niveau master…~~ → **Répondu** — voir L.3.

#### L.3 Gain master par HP — conserver (acté)

| | |
|---|---|
| **Valeur actuelle** | `*~ 0.65` par sortie HP |
| **Décision** | **Très bien** — **ne pas changer** (plage validée) |

4. ~~Panneau MOTEUR_INTERNE…~~ → **Répondu** — voir L.4.

#### L.4 Panneau MOTEUR_INTERNE — explication (pas encore tranché)

**De quoi s’agit-il ?**

Le patch Pd est divisé en **deux zones visuelles** (voir `gen_prototype_05.py`) :

```text
┌─────────────────────────────────────────────┐  ← y ≈ 40–700
│  TRANSPORT_(MODIFIABLE)                     │
│  ETAT_FSM_(MODIFIABLE)                      │  Panneaux « utilisateur »
│  SPATIAL_(MODIFIABLE)                       │  — réglages, FSM, debug
│  FLUID_FX / ECHO_(MODIFIABLE)               │
├─────────────────────────────────────────────┤  ← y ≈ 730
│  MOTEUR_INTERNE_(NON_MODIFIABLE)            │  ~1500×640 px — fond gris
│  encode/decode, lecteurs, dac~, câblage…    │  le vrai moteur audio
└─────────────────────────────────────────────┘
```

**« Masquer en mode installation »** = en expo / présentation, **cacher la zone du bas** (et éventuellement les panneaux debug du haut) pour n’afficher qu’une interface **épurée** — ou **rien du tout** si tout est en AUTO.

| Avantage masquer | Inconvénient |
|------------------|--------------|
| Fenêtre **plus petite**, visuel **propre** | Debug sur place **plus difficile** |
| Moins de clics accidentels sur le moteur | Il faut un toggle **INSTALL_MODE** / **DEBUG** pour rouvrir |
| Aspect **installation finie** (pas « patch de dev ») | |

**Décision proto 06 (actée) :** toggle `INSTALL_MODE` — **ON** = masque `MOTEUR_INTERNE` + panneaux SPAT/ECHO debug ; **OFF** = tout visible (session réglage).

5. ~~Preset présentation…~~ → **Répondu** — voir L.5.

#### L.5 Presets présentation / intensité (acté)

| | |
|---|---|
| **Souhaité ?** | **Oui** |
| **Usage** | Plusieurs **presets** pour tester des **niveaux d’intensité** (FX, densité, AUTO…) |
| **Exemple** | Preset « présentation » : FORCE actif, AUTO off, intensité modérée ; preset « stress » : variantes agressives |

→ Implémentation proto 06 : banque `PRESET_INTENSITE` (nom + snapshot SPAT/FX/FSM) — détail §M à définir.

6. ~~Console Pd…~~ → **Répondu** — voir L.6.

#### L.6 Console Pd — zéro error, zéro warning (acté)

| | |
|---|---|
| **Errors** | **Aucune** tolérée |
| **Warnings** | **Aucun** toléré non plus |
| **Test** | `scripts/test_patch_console.sh` doit sortir **propre** avant merge / session |

→ La question initiale visait le cas « warning bénin connu » en dev — **rejeté** : objectif **console 100 % propre**.

→ **Section L : complète** (L.4 validé : INSTALL_MODE activable).

---

## M. Calibrage — session d’écoute

*Valeurs **proposées** (9 juil. 2026) pour cycle 1 — à **valider à l’oreille**.*


| Paramètre                   | État / contexte       | Min proposé | Max proposé | Validé ? |
| --------------------------- | --------------------- | ----------- | ----------- | -------- |
| Durée AUTO **cycle 1** | BOUCLE | 12 s | 16 s | ☐ |
| Durée AUTO **cycle 1** | HIPPO | 5 s | 9 s | ☐ |
| Durée AUTO **cycle 1** | RECON | 14 s | 18 s | ☐ |
| Durée AUTO **cycle 1** | CORTEX (final) | 10 s | 16 s | ☐ |
| Durée **cycle 2** total     | tous                  | 90 s        | 150 s       | ☐        |
| `jump_min_ms`               | BOUCLE lent           | 3 000       | 10 000      | ☐ H2     |
| `jump_max_ms`               | BOUCLE lent           | 6 000       | 12 000      | ☐ H2     |
| `jump_min_ms`               | BOUCLE burst rapide   | 300         | 400         | ☐ H2     |
| Durée burst rapide BOUCLE   |                       | 3 s         | 4 s         | ☐ H2     |
| `fluid_wet`                 | BOUCLE (plafond H3)   | 0,65        | **0,85**    | ☐        |
| `fluid_delay`               | BOUCLE (plafond H3)   | 600         | **800**     | ☐        |
| `fluid_fb`                  | BOUCLE (plafond H3)   | 0,50        | **0,70**    | ☐        |
| `fluid_lfo`                 | BOUCLE (plafond H3)   | 0,35        | **0,50**    | ☐        |
| `fluid_wet`                 | HIPPO                 | 0,30        | 0,65        | ☐ H3     |
| `fluid_delay`               | HIPPO                 | 250         | 600         | ☐ H3     |
| `fluid_wet`                 | RECON (défaut, G5)    | ~0.15       | ~0.35       | ☐        |
| `fluid_fb` (plafond J3)    | global (hors CORTEX)  | 0           | **0,70**    | ☐ J3     |
| `filter_hpf`               | CORTEX (J4)           | 20          | 1 200       | ☐        |
| `filter_lpf`               | CORTEX (J4)           | 1 200       | 20 000      | ☐        |
| `filter_resonance`         | CORTEX (J4)           | —           | **~1 %**    | ☐        |
| `fluid_wet` global         | hors CORTEX (J2)      | —           | —           | ☐ TBD    |
| Saturation drive principal | BOUCLE (J6)           | —           | —           | ☐        |
| Saturation drive principal | HIPPO (J6)            | —           | < BOUCLE    | ☐        |
| Facteur compensation sat   | gain_comp (J7)        | —           | **×1,5**    | ☐        |
| Poids variante delay fort   | BOUCLE                | 70 %        | 80 %        | ☐ H3     |
| Poids SPAT saut vs séquence | BOUCLE (H4)           | 50 %        | 50 %        | ☐        |
| Poids SPAT rotation BOUCLE  | vs saut/seq (I1)      | —           | —           | ☐        |
| Poids SPAT flash            | HIPPO/CORTEX (I1)     | 33 %        | 33 %        | ☐        |
| Durée phase clarté BOUCLE   | delay off/faible (H5) | 2 s         | 6 s         | ☐        |
| Durée montée sat/phase      | BOUCLE (H5)           | 2 s         | 4 s         | ☐        |
| `rot_speed` (couche unique) | HIPPO/RECON           |             |             | ☐        |
| `rot_speed` ratio A/B si vitesses ≠ | HIPPO/RECON   | 0,5         | 2,0         | ☐        |
| Poids tirage opposé + vit. égale | rotation 2 couches | 25 %    | 40 %        | ☐        |
| Durée max segment `SONS/`   | plafond (K5)          | —           | **90 s**    | ☐        |
| Gain master par HP           | `*~` (L3)             | **0.65**    | **0.65**    | ☑        |
| Délai 1ère superposition CORTEX | entrée état (N6) | 2 s | 8 s | ☐ |
| Budget overlaps / ~50 s CORTEX | cumul | 0 s | 15 s | ☐ |
| Durée max sample principal CORTEX | test | — | ~50 s | ☐ |
| Overlap 4 samples simultanés | HIPPO/RECON | 2 s | 5 s (max) | ☐ |
| Fréquence croisement baffle | HIPPO | occasionnel (émergent) | — | ☑ Q43–44 |
| Poids tirage ping-pong | rotation 2 couches opposées | 25 % | 30 % | ☐ |


---

## N. Questions très précises (implémentation)

1. ~~Assignation baffle / buffer…~~ → **Répondu** — voir N.1.

#### N.1 Mapping buffer ↔ baffle — fixe (acté)

| | |
|---|---|
| **Décision** | **Mapping fixe** — **très important** |
| **Rotation du mapping** | **Non** — pas de réassignation HP à chaque transition FSM |

**Table indicative proto 06** (à coder dans `fsm_presets` / `layer_hp_map`) :

| Slot lecteur | Baffle ancre (fixe) |
|--------------|---------------------|
| Couche 1 | **HP1** |
| Couche 2 | **HP3** |
| Couche 3 | **HP4** |

→ Le **mouvement** spatial (saut, séquence, rotation) part de ces ancres ; les **slots** ne permutent pas entre HP à chaque état.

**Note Q36 :** le tirage « premier HP aléatoire + opposé » concernait la **séparation dynamique** ; N.1 fixe l’**assignation de base** des buffers — les deux coexistent si le preset le précise (ancre fixe + pattern relatif).

2. ~~Rotation opposée…~~ → **Répondu** — voir N.2.

#### N.2 Sens de rotation — configurable par variante (acté)

| | |
|---|---|
| **Toujours** couche 1 H + couche 2 anti-H ? | **Non** |
| **Décision** | **Configuration variable** par `variante_id` / preset |
| **Champs** | `SENS` par couche (0 = horaire, 1 = antihoraire) — tirage ou preset |

3. ~~Couche saute + autre tourne…~~ → **Répondu** — voir N.3.

#### N.3 Modes SPAT mixtes dans une variante — autorisé (acté)

| | |
|---|---|
| **HIPPO (et autres)** | Une couche en **saut** (SPAT=2) + une autre en **rotation** (SPAT=1) dans la **même variante** |
| **Décision** | **Oui** — totalement autorisé (cohérent F.0.1, I.1) |

4. ~~Reséparation forcée…~~ → **Non** — pas de timer reséparation (Q45).
5. ~~`[PLAGE]` X = …~~ → **N/A** (Q45).

6. ~~Délai avant première superposition CORTEX…~~ → **Répondu** — voir N.6.

#### N.6 CORTEX — délai avant première superposition (acté)

| | |
|---|---|
| **Immédiat ?** | **Non** |
| **Décision** | **Délai** avant la **première** superposition brève à l’entrée CORTEX |
| **Plage** | À calibrer §M (`cortex_overlap_delay_ms`) |

→ Le principal démarre seul ; la première « pensée furtive » arrive **après** ce délai.

7. ~~Nombre max re-clics FORCE…~~ → **Non pertinent** — voir N.7.

#### N.7 Re-clics FORCE — question retirée

| | |
|---|---|
| **Pertinence** | **Non** — sujet écarté |
| **Raison** | Pas de limite narrative à coder ; FORCE reste disponible sans compteur |

8. ~~Proto 05 / 06…~~ → **Répondu** — voir N.8.

#### N.8 Périmètre proto 06 — implémenter le Q&A au maximum (acté)

| | |
|---|---|
| **Proto 05** | **Figé tel quel** — **ne plus parler d’extension 05** |
| **Proto 06** | **Nouveau patch** — reprise de la **base** 05 sans mélanger les routages |
| **Objectif** | Implémenter **le plus possible** de ce document Q&A |
| **Leçon 03–05** | Routages confus (04/05) → **figer** architecture multi-bus **dès 06** |

```text
prototype_05_fsm.pd     →  archive / référence (gelé)
prototype_06_fsm_4hp    →  cible implémentation Q&A
prototype_06_fsm_6hp    →  variante 6 HP (samedi)
```

→ **Section N : complète.**

---

## Comment répondre

- Q&A **sections A–N : complètes** (9 juil. 2026).
- **Prochaine étape :** session **§M** (calibrage à l’oreille) + **`gen_prototype_06.py`**.
- Les réponses alimentent le **proto 06** ; le proto 05 reste **gelé**.