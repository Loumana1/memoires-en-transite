# Q&A créateur — Prototype 07

> **Intention du 16 août 2026** (complété 17 : ligne 21). **Pas une spec.**  
> Maintenant : [`../etatactuel.md`](../etatactuel.md) · pourquoi : [`../log.md`](../log.md).  
> Les FX (Q10, Q20, densité 3–6…) ont été **écrasés** à l’oreille les 17–18 août.

**Pour :** Loumana (artiste / décisionnaire)  
**Date :** 16 août 2026  
**Usage :** répondre dans la colonne **Décision**. Une ligne = une décision.  
Les **propositions** sont là pour que tu puisses écrire *oui* au lieu de tout reformuler.

Les réponses **01–21 sont actées** (16–17 août 2026, Loumana).  
**21** (17 août) : Cortex = flou 06, pas le LPF dur.

État actuel : [`../etatactuel.md`](../etatactuel.md) · log : [`../log.md`](../log.md) · synthèse 16 août : [`../backlog/14_prototype_07_synthese_backlog.md`](../backlog/14_prototype_07_synthese_backlog.md)

### Décisions BLOQUANT actées

| # | Décision |
|---|----------|
| **01** | **Oui.** On abandonne le cycle ~50 s / « 2 fois chaque strate en 3 min ». Paysage qu’on habite. |
| **02** | **Oui.** Cycle 1 AUTO : Cortex **40 s** · Hippo **50 s** · Recon **2 min**. Tirage [min, max] ensuite. |
| **03** | **Pas A.** Les **8 baffles** sont utilisés en Cortex. Le schéma 2+2+2+HP4 n’était qu’une première idée ; viser **plus de mouvement**, pas un sous-ensemble de HP. |
| **04** | Ambiance **pendant tout le Cortex**, **sans FX**, assez audible. **Pas forcément HP4** : un baffle dédié, **fixe pendant le tour**, peut changer d’un tour à l’autre (ex. HP3 une fois, un autre la suivante). |
| **05** | **Oui.** Downmix **mono** à la découpe. |
| **06** | **Non** au fichier unique. Découper l’ambiance en **morceaux de 2–3 min** (jamais plus long). |
| **07** | **Oui.** ≥ 30 s → PRINCIPAL · 1–5 s → COURT · 5–30 s → MOYEN (oreille). |

### Décisions IMPORTANT actées

| # | Décision |
|---|----------|
| **08** | **Plusieurs** sons en Hippo (pas un seul voyageur). |
| **09** | Recon **encore un peu mobile**, comme maintenant — un tout petit peu. |
| **10** | LPF 400–600 Hz **dur** sur les fragments Cortex (au-dessus fortement atténué). **Aucun** LPF / FX sur l’ambiance. |
| **11** | **Oui** — proba 15 % / délai 8–90 s (calibrable). |
| **12** | v1 = **tirage au hasard**. Nomination / classification des samples : on étendra plus tard. |
| **13** | « Fondu » ≠ volume. Cortex→Hippo = **queue de delay** qui résonne encore. Recon→Hippo = **coupe sèche**. Coupes sèches parfois ailleurs. |

### Décisions 14–20 actées

| # | Décision |
|---|----------|
| **14** | **Oui.** On ne touche plus au Proto 06. Tout le 07 = `prototype_07_fsm_8hp.pd` + `presets07.py`. |
| **15** | **Logique piezo/micro dès le 07**, même sans matériel. Toggle **ON/OFF** + entrées piezo et micro prêtes (simu si rien de branché). |
| **16** | Tags **souhaités**, système **pas encore trouvé**. v1 = hasard ; architecture prête à recevoir des tags plus tard. |
| **17** | **Oui** : pré-découpe **faite par l’artiste** + classification pour que les sons « fassent semblant de s’entendre ». Pas encore livrée — le moteur prévoit les dossiers. |
| **18** | **8 HP seulement.** Fini les 4/6 HP pour ce proto. |
| **19** | **Pas trop de random.** Garder la logique de randomness **actuelle** (06). |
| **20** | Ambiance **XOR** next-room, **sur le lit d’ambiance seulement**, tirage à peu près aléatoire (~1 fois sur 2). Ambiance = **dry**, highs un peu coupés. Next-room = highs **presque tous** coupés + **reverb**. Pas les deux en même temps. |
| **21** | **17 août 2026.** Cortex fragments = **son 06** (HPF 400–600, LPF ~2–3 kHz + flfo, sat ~0.5, echo/reverb **un peu plus** que 06). On **abandonne** le LPF 400–600 dur (Q10) sur les fragments — trop sombre, plus de flou. Nappe = toujours **1 HP dédié, dry**. Densité **6–8**. |

---

## Comment répondre

- **Oui** = tu valides la proposition telle quelle  
- Sinon : corrige le chiffre, le mapping, ou la phrase  
- Si tu ne sais pas encore : `oreille` (on tranchera en FORCE en salle)

---

## A. BLOQUANT — sans ça le câblage est faux

### Q07-01 — Durées d’état vs visite

**Contexte.** Aujourd’hui le cycle 8HP dure **~53 s** (28 + 9 + 16). Tes nouvelles plages donnent un cycle **~2 à 7 min** (Cortex 20–60 + Hippo 30–90 + Recon 1–4 min). L’ancien Q&A 05 voulait que en **~3 min** le visiteur ait vécu **chaque strate au moins 2 fois**.

**Proposition.** On **abandonne** le cycle 50 s. Proto 07 = **un paysage qu’on habite** : une visite 5–7 min peut n’entendre **qu’un seul** passage Recon. Les strates se répètent sur la session 7 min (reset), pas deux fois en 3 min.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). Cycle 50 s abandonné. Une visite 5–7 min peut n’entendre qu’un Recon. |
| **Si non** | — |

---

### Q07-02 — Plages exactes cycle 1 (AUTO)

**Proposition (milieu de tes fourchettes) :**

| Zone | Min | Défaut AUTO | Max |
|------|-----|-------------|-----|
| Cortex | 20 s | **40 s** | 60 s |
| Hippocampe | 30 s | **50 s** | 90 s |
| Reconstruction | 60 s | **2 min** | 4 min |

Tirage aléatoire dans [min, max] à chaque entrée d’état. Cycle 1 utilise les **défauts**.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). Cortex **40 s** confirmé ; table entière (Hippo 50 s, Recon 2 min) validée. |

---

### Q07-03 — Cortex : 4 baffles « saturés » ou 8 baffles ?

**Contexte.** Tu décris : 2 couches HP1, 2 HP2, 2 HP3, 1 ambiance HP4. L’installation proto est en **8 HP**. Aujourd’hui le 06 met **1 fragment par baffle** sur les 8 + 2 doublons (HP1, HP5).

**Proposition A (fidèle à ton texte, 07 v1) :** HP1–3 saturés (2 fragments chacun) + ambiance HP4. HP5–8 **muets** en Cortex, ou très bas (fuite / distant).

**Proposition B :** même logique 2 fragments / baffle, **étendue** : HP1–3 comme tu dis, et HP5–7 aussi en 2 couches (HP4 + HP8 = ambiances / next-room). Plus dense.

**Proposition C :** garder 1 fragment × 8 baffles **plus** 2ᵉ couche seulement sur HP1–3, + ambiance HP4.

| | |
|--|--|
| **Décision** | **Autre — 8 baffles, plus de mouvement** (16 août 2026). A/B/C rejetés. Le 2+2+2+HP4 était un premier croquis. **Tous les HP** jouent en Cortex. Superpositions possibles, mais pas au prix d’éteindre HP5–8. |
| **Pourquoi ça compte** | Nombre de lecteurs élevé ; l’ambiance occupe **un** HP (voir Q07-04), les 7 autres portent fragments + mouvement. |

---

### Q07-04 — Ambiance Cortex : toujours là ?

Le fichier `opacité fin V2  Cortex ambiance.wav` (26 min, continu, pas de silences).

**Proposition.** Tant qu’on est en Cortex : **ambiance HP4 en continu** (loop), sous les fragments. Elle **coupe** (ou fade 100 ms) en quittant Cortex. Elle ne va jamais dans Hippo / Recon.

| | |
|--|--|
| **Décision** | **Oui pour la présence en Cortex, non pour HP4 figé** (16 août 2026). Un baffle **ambiance**, **dry (aucun effet)**, assez audible. Index HP **tiré au début du tour**, **fixe jusqu’à la sortie** Cortex. Peut être HP3, HP4, etc. Coupe en quittant Cortex. Pas dans Hippo / Recon. |

---

### Q07-05 — Stéréo des masters V2

Les 4 fichiers sont **stéréo**. Le moteur joue en **mono par couche** vers un HP.

**Proposition.** Downmix mono (L+R) à la découpe, comme aujourd’hui. L’espace vient des **baffles**, pas de la stéréo du fichier.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). Mono à la découpe. |

---

### Q07-06 — Plafond 90 s (ancienne règle K5) vs ambiance 26 min

**Proposition.** Fragments découpés : toujours ≤ 90 s. **Exception :** l’ambiance Cortex peut rester un **seul** fichier long (ou 3 tranches ~9 min) pour éviter 20 coupes audibles.

| | |
|--|--|
| **Décision** | **Non** (16 août 2026). Découper en **plusieurs lits de 2–3 min** (plafond ambiance = **180 s**, pas 90 s K5). ~9–13 fichiers pour 26 min 42 s. |

---

### Q07-07 — Reconstruction : le master est-il déjà « fil + bribes » ?

`opacité fin V2  Reconstruction.wav` mélange visiblement des événements et des silences.

**Proposition.** On découpe par silences, puis :
- **≥ 30 s** → `RECONSTRUCTION/PRINCIPAL/`
- **1–5 s** → `RECONSTRUCTION/COURT/` (interrupts)
- **5–30 s** → `RECONSTRUCTION/MOYEN/` (utilisable en principal court **ou** Hippo, tu tranches à l’écoute)

Le moteur Recon = **1 PRINCIPAL en boucle ou enchaîné** + **1 COURT** one-shot de temps en temps.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). Classification PRINCIPAL / COURT / MOYEN comme proposé. |

---

## B. IMPORTANT — comportement des zones

### Q07-08 — Hippocampe circulaire : un son ou plusieurs ?

Tu veux **1→2→3→4→5→6→7→8→7→…→1** pour **suivre** et reconnaître.

**Proposition.** En Hippo : **1 fragment voyageur** sur ce chemin (le « son qu’on suit ») + **0 ou 1** contrechant plus fixe / plus bas. Densité 1–2, jamais 4 comme aujourd’hui.

| | |
|--|--|
| **Décision** | **Plusieurs sons** (16 août 2026). Pas un seul voyageur + contrechant. Plusieurs fragments circulent (nombre exact à l’oreille, **> 1**, toujours **moins** que Cortex). |

---

### Q07-09 — Reconstruction : spatial fixe ou encore un peu mobile ?

**Proposition.** Variante 1 AUTO : **dry ancré** (un baffle, ou paire L/R douce). Variante 2 (FORCE / rare) : mobilité très lente. Le fil doit rester identifiable.

| | |
|--|--|
| **Décision** | **Un tout petit peu mobile**, comme maintenant (16 août 2026). Pas dry ancré strict. Le fil reste identifiable. |

---

### Q07-10 — LPF Cortex 400–600 Hz

« Low pass entre 400/600 » : tout au-dessus est fortement atténué → voix **très** sourde (téléphone dans la pièce d’à côté).

**Proposition.** LPF **autour de 550 Hz** sur **les fragments** Cortex. **Ambiance : aucun FX** (Q07-04) — pas de LPF sur le lit d’ambiance. Un *autre* baffle (fragments) peut porter le muffled / micro-réverb.

| | |
|--|--|
| **Décision** | **Oui, intention dure** (16 août 2026). Tout au-dessus de 400–600 Hz fortement atténué sur les **fragments**. **Pas de LPF sur les ambiances** — elles ne sont pas touchées. |

---

### Q07-11 — Boucle : proba de piocher, pas une durée

**Proposition v1 (chiffres de départ, calibrables) :**

À chaque **sortie de zone** (surtout après Recon, parfois après Hippo) :

- **15 %** → réinjecter **un** fragment du buffer Boucle (vers Cortex ou Recon), puis continuer le cycle
- **85 %** → transition normale sans piocher

Un fragment mis en buffer : délai **8–90 s**, proba de survie **0,6** à chaque évaluation, max **5** retours (puis oubli). Parfois (20 %) il revient **intact**.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). On part de 15 % / 8–90 s ; calibrable à l’oreille. |

---

### Q07-12 — Qu’est-ce qu’on met dans le buffer Boucle ? (v1)

Sans tags ni découpe de syllabes, le 07 v1 ne peut stocker que des **fichiers déjà joués**.

**Proposition.** À chaque lecture **terminée** (Hippo ou Recon COURT, parfois un fragment Cortex), **30 %** de chance d’en copier la référence dans le buffer (chemin + dernière enceinte + gain). Pas de réenregistrement `writesf~` (ça reste Final / proto plus tard).

| | |
|--|--|
| **Décision** | **v1 = hasard** (16 août 2026). Pas de tags pour l’instant. On **étendra** plus tard la nomination / classification de chaque sample. En attendant : piocher au hasard (dans le buffer ou le pool). |

---

### Q07-13 — Transitions : coupe sèche ou fondu ?

Ancien Q&A : **pas de fondu**, coupe ≤ 100 ms. Tes durées plus longues rendent une coupe Cortex (opaque, dense) → Hippo (un son qui tourne) plus brutale.

**Proposition.** **Fondu 400–700 ms** seulement Cortex→Hippo et Hippo→Recon. Recon→… : coupe courte OK. Jamais de silence programmé.

| | |
|--|--|
| **Décision** | **Fondu ≠ volume** (16 août 2026). C’est la **queue FX** : en Cortex→Hippo, le delay **continue de résonner** un peu. **Recon→Hippo = coupe sèche**. Des coupes sèches **parfois** ailleurs. Hippo→Recon : queue par défaut (sauf si l’oreille dit coupe). Jamais de silence programmé. |

---

### Q07-14 — Figé Proto 06 ?

**Proposition.** On **ne touche plus** aux patches `prototype_06_fsm_*`. Tout le 07 vit dans `prototype_07_fsm_8hp.pd` + `presets07.py`, pour A/B en salle.

| | |
|--|--|
| **Décision** | **Oui** (16 août 2026). Proto 06 figé. Tout le travail = Proto 07 (patch + presets à part), A/B en salle. |

---

## C. PEUT ATTENDRE — mais mieux si tranché tôt

### Q07-15 — Piezo dans le 07 ou après la matière ?

Tu as écrit : *pas de mouvement = ça reste dans le Cortex* / *N2 piezo = beaucoup de mouvement = changement*.

**Proposition.** Vague 8 seulement, **après** que Cortex/Hippo/Recon sonnent. En attendant : slider `rms_sim` pour tester UC-C12. Pas de micro salle (larsen).

| | |
|--|--|
| **Décision** | **Logique dès le 07** (16 août 2026). Matériel pas encore là. Implémenter l’analyse + **toggle ON/OFF** et des **entrées piezo et micro** (simu si rien de branché). Pas de monitoring `adc~` → HP (larsen). |

---

### Q07-16 — Associations Hippo : hasard contrôlé ou vrai graphe ?

« Le mot *autre* peut déclencher une voix familiale, une fiche, une respiration… »

**Proposition 07.** **Pas de tags.** Quand un fragment Hippo se termine (ou à 70 % de sa durée), **tirage pondéré** d’un autre fichier du pool, autre enceinte = « réponse ». Même fichier interdit tout de suite. Le graphe tagué (langue, lieu, timbre) = proto suivant / Final.

| | |
|--|--|
| **Décision** | **Tags voulus, pas encore de système** (16 août 2026). v1 = hasard (Q07-12). Prévoir un crochet (table / dossier / métadonnées) pour brancher les tags **quand** la classification existera. |

---

### Q07-17 — Reconstruction linguistique (phrase → « Irréductible »)

**Proposition.** **Hors 07 moteur.** Si tu veux cet effet **maintenant**, il faut des **fichiers déjà coupés** (phrase / mots / reste) dans `RECONSTRUCTION/DEGRE_1|2|3/`. L’algo ne « comprend » pas la parole.

| | |
|--|--|
| **Décision** | **Oui, plus tard côté contenu** (16 août 2026). Pré-découpe **faite par l’artiste**. Classification pour que les sons « fassent semblant de s’entendre » — **pas encore faite**. Le 07 prévoit `RECONSTRUCTION/DEGRE_*` (ou équivalent) ; on ne bloque pas la vague 1 dessus. |

---

### Q07-18 — 4 HP / 6 HP

**Proposition.** Proto 07 = **8 HP seulement**. 4/6 restent en 06 legacy pour le studio réduit.

| | |
|--|--|
| **Décision** | **8 HP seulement** (16 août 2026). Fini les petits haut-parleurs pour ce proto. 4/6 = legacy 06, plus d’évolution. |

---

### Q07-19 — Variabilité : « jamais deux fois pareil » à quel grain ?

**Proposition 07.** Varier : **quel** fichier, **quand** (dans les plages), **quelle** enceinte de départ Hippo, **quelle** variante FX (3), **quel** HP ambiance **d’un tour à l’autre**. Ne **pas** varier : LPF sombre sur fragments Cortex, circularité Hippo, dry Recon, ambiance **sans FX**. Trop de random tuerait la lisibilité des **trois climats**.

| | |
|--|--|
| **Décision** | **Oui — pas trop de random** (16 août 2026). Garder la **logique de randomness actuelle** (06). Ne pas en ajouter une couche. |

---

### Q07-20 — Ambiance vs « next-room »

Les deux **ne coexistent pas** sur le même lit. C’est un **XOR** sur **la couche ambiance seulement** (pas un fragment ailleurs).

| Mode | Traitement |
|------|------------|
| **Ambiance** | Matière déjà « ambiance » — **dry**, assez dry. Highs un peu coupés, **pas totalement**. |
| **Next-room** | Highs **presque tous** coupés + **reverb**. |

**Tirage** à l’entrée d’un tour Cortex (~ **1 fois sur 2**, calibrable). Pendant le tour : un seul mode, fixe. Index HP toujours fixe pendant le tour (Q07-04).

| | |
|--|--|
| **Décision** | **Acté** (16 août 2026). XOR aléatoire ambiance / next-room sur le lit d’ambiance. Pas les deux à la fois. |

---

## D. Rappel — déjà tranché (ne pas rouvrir)

| Sujet | Décision |
|-------|----------|
| Sens du mot CORTEX | Zone **profonde / opaque**, pas la clarté |
| Ordre de base | Cortex → Hippo → Recon (Boucle n’est pas l’entrée) |
| Recon = lisible | L’opacité vit au Cortex |
| Cycle visite | Plus de cycle 50 s ; Cortex 40 s / Hippo 50 s / Recon 2 min en AUTO |
| Cortex spatial | **8 HP** actifs ; plus de mouvement (pas 2+2+2+HP4 seul) |
| Ambiance Cortex | 1 HP dédié, fixe pendant le tour ; **ambiance dry** XOR **next-room** (Q07-20) |
| Ambiance fichiers | Tranches **2–3 min**, mono |
| Hippo densité | **Plusieurs** sons circulaires (moins que Cortex) |
| Recon spatial | Un **tout petit peu** mobile, comme le 06 actuel |
| LPF Cortex | 400–600 Hz **dur** sur **fragments** ; lit ambiance = dry ou next-room (pas le LPF fragments) |
| Boucle v1 | 15 % de piocher ; contenu = **hasard** (tags plus tard, Q07-16) |
| Transitions | Queue **delay** Cortex→Hippo ; **coupe sèche** Recon→Hippo ; pas de fondu volume |
| Proto 06 | **Figé** ; tout le neuf = Proto 07 8HP |
| HP | **8 seulement** (plus de 4/6 pour ce proto) |
| Présence | Logique + toggle piezo/micro dès le 07 (matériel plus tard) |
| Variabilité | Randomness **comme le 06**, pas plus |
| Recon linguistique | Pré-coupe + classification artiste, dossiers prévus, contenu pas encore là |
| Pas de silence entre états | Oui |
| AUTO ⊥ FORCE | Oui |
| Gain master 0,65 | Oui |
| Console Pd propre | Oui |
| 05 et 06 | **Figés** |

---

## E. Mini-réponses rapides (optionnel)

Si tu préfères un bloc unique :

```text
Q07-01: OUI — abandon cycle 50 s
Q07-02: OUI — Cortex 40 s / Hippo 50 s / Recon 2 min
Q07-03: 8 HP tous utilisés ; plus de mouvement (pas A)
Q07-04: ambiance dry, 1 HP dédié, PAS forcément 4 ; fixe pendant le tour
Q07-05: OUI — mono à la découpe
Q07-06: NON fichier unique — tranches ambiance 2–3 min
Q07-07: OUI — PRINCIPAL / COURT / MOYEN
Q07-08: PLUSIEURS sons Hippo (circulaire)
Q07-09: un tout petit peu mobile, comme maintenant
Q07-10: LPF 400-600 DUR sur fragments ; ambiance intacte
Q07-11: OUI — 15 % / 8-90 s
Q07-12: v1 hasard ; classification plus tard
Q07-13: fondu = queue delay Cortex→Hippo ; coupe sèche Recon→Hippo
Q07-14: OUI — 06 figé, tout dans prototype_07
Q07-15: logique piezo/micro + toggle ON/OFF dès le 07 (pas le matériel)
Q07-16: tags voulus, pas de système encore ; v1 hasard
Q07-17: OUI — pré-coupe + classification artiste (pas encore livrée)
Q07-18: 8 HP seulement
Q07-19: pas trop de random ; garder la logique actuelle
Q07-20: XOR ambiance dry / next-room (highs presque off + reverb) sur le lit d'ambiance ~1/2
```

**Q&A 01–20 complet.** Prochaine étape : vague 1 (découpe `Opacité fin V2`).
