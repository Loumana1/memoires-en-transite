# Zone Cortex — comportement sonore

**Priorité 1 pour le gel.** Aucun paramètre n'est encore FIGÉ, mais la **structure** l'est depuis le 20 août : voir §3.
Statuts : voir [`README.md`](./README.md). Questions ouvertes : [`../Backlog/Q&A.md`](../Backlog/Q&A.md).

> **Attention en lisant les §4 à §8.** Ils décrivent le Proto **07** tel qu'il sonne aujourd'hui : 6 couches de parole sur 3 baffles, 5 nappes. La cible décidée est 12 couches sur 6 baffles et 2 nappes (§3). Les valeurs restent valables comme point de départ, pas comme description de la cible.

---

## 1. Intention

Un milieu de paroles superposées, **flouté et dissipé**. On doit entendre qu'il y a de la parole, sentir qu'il y en a plusieurs, et sentir qu'elles viennent d'ailleurs — d'une pièce voisine, à travers un mur. On ne doit pas pouvoir suivre ce qui est dit.

Simon note que lors des essais les conversations restaient **encore trop clairement intelligibles**. C'est le principal reproche à lever. Voir [Q18](../Backlog/Q&A.md#q18) : jusqu'où pousser (mots reconnaissables mais sens perdu, ou même pas les mots ?).

Le Cortex est aussi la seule zone qui superpose beaucoup de couches en même temps. Sa signature, c'est la **densité floue**, par opposition à l'Hippocampe qui est mobile et net, et à la Reconstruction qui est lisible.

---

## 2. Invariants — vrais quel que soit le sample

Ce sont les affirmations qui doivent rester vraies même si on remplace toute la matière. À valider, puis à défendre.

1. Aucune couche de parole n'est intelligible seule, même en isolant son HP.
2. Il y a toujours du grave enlevé (HPF) : la parole ne doit pas avoir de corps, de proximité, de poitrine.
3. Il y a toujours de l'aigu enlevé (LPF bas) : pas de consonnes nettes, pas de « s », pas de « t ».
4. Le contenu spectral **bouge lentement** et jamais en phase entre les couches. C'est ce qui donne l'impression de mur, de porte, de respiration du lieu, plutôt que d'un simple filtre statique.
5. Les nappes d'ambiance sont **sèches et continues**. Elles ne sont ni filtrées, ni découpées, ni retardées. Elles sont le milieu, pas un événement.
6. Aucun envoi (delay, réverbération) d'un baffle vers un autre baffle. Chaque HP tient son propre son. Décision d'oreille du 18 août, à conserver sauf prompt contraire.
7. Le micro et les piézos ne vont **jamais** vers `dac~`.

---

## 3. Carte des 8 HP — TRANCHÉ le 20 août

[Q1](../Backlog/Q&A.md#q1) = **option A**, [Q2](../Backlog/Q&A.md#q2) répondu. La cible est la spec de Simon.

| | Cible décidée | Implémentation actuelle (18 août) |
|--|--|--|
| Paroles | **6 baffles**, 2 fragments superposés chacun → **12 fragments simultanés** | HP1–3, 3 paires, 6 fragments |
| Ambiances | **2 baffles**, une musicale et une texture, **fixes** pendant le Cortex | HP4–8, 5 nappes du même pool |

Deux précisions issues de [Q2](../Backlog/Q&A.md#q2), qui ne sont pas dans la spec :

- Ce ne sont **pas forcément HP7 et HP8**. Les deux baffles d'ambiance peuvent être n'importe lesquels des huit ; ce qui compte est qu'ils soient **fixes** pendant toute la durée du Cortex, et **pas côte à côte** dans la salle. Les six autres portent la parole.
- La définition de « zone » qui fait foi est celle du projet : une zone est un **moment du cycle**, pas un rôle spatial permanent. « Cortex-Ambiance » n'est donc pas une zone, ce sont **deux couches de l'état Cortex**. Elles s'arrêtent avec lui.
- **Croisement parole/ambiance = global** ([Q25](../Backlog/Q&A.md#q25)) : une paire d'ambiances (musicale + texture) pour **tout** le Cortex, jamais une ambiance par baffle de parole. §7 bis.

### Ce que ça implique concrètement

| Conséquence | Détail |
|--|--|
| 14 lecteurs au lieu de 11 | 12 paroles + 2 nappes, contre 6 + 5 aujourd'hui |
| Le balayage de LPF passe à 12 oscillateurs | §5 n'en définit que 6, et ils doivent rester non harmoniques entre eux |
| 6 paires permutent sur 6 baffles | même principe qu'aujourd'hui (3 sur 3), simplement étendu — pas de perte de mouvement |
| L'espace autour des paroles se vide | on passe de 5 nappes à 2. C'est le vrai risque à l'oreille de cette décision |
| Deux familles d'ambiance à séparer | `CORTEX/AMBIANCE` est un pool unique. Il faut *musicale* et *texture* distinctes |
| Plus aucun baffle libre | 6 + 2 = 8 exactement. Aucune marge |
| **Les plans de présence deviennent indispensables** | douze voix filtrées au même niveau ne font pas une superposition, elles font du bruit. C'est ce qui fait passer [Q10](../Backlog/Q&A.md#q10) et [Q11](../Backlog/Q&A.md#q11) en tête de priorité |

Cette réécriture touche `cortex_pair_07`, `cortex_amb_07`, `cortex_ctrl_07`, `FSM_N_8HP[0]`, les ancrages et le nombre de lecteurs. Elle se fait donc dans un **Proto 08** ([Q24](../Backlog/Q&A.md#q24) = A), pas dans le 07.

**Le choix des samples reste hors sujet ici.** La règle C1 (un fragment Belgique + un fragment Congo par baffle) est **différée** : [Q4](../Backlog/Q&A.md#q4) confirme que l'information n'existe pas encore et viendra du tableau de classification. Le Proto 08 peut donc être construit avec la carte à 12 voix et un tirage au hasard, le sélecteur se branchant plus tard. C'est exactement la séparation voulue : figer le son de la zone d'abord, la logique de choix ensuite.

---

## 4. Chaîne de traitement — fragments de parole

Ordre du signal, couche par couche :

```text
player_state_07 → *~ 0.22 → gate ~3 ms → fx_router_06 → cortex_pair_07 → HP
                                          │
                                          └─ sat → HPF+LPF → delay/wet
```

En Cortex les fragments **ne passent pas** par l'encodage ambisonique ni par `decode_8hp_06` : `cortex_pair_07` sort directement sur les canaux 1 à 3. Le routage ambisonique ne sert qu'en Hippocampe, Reconstruction et Boucle.

Valeurs, par couche L1 → L6 (`presets07.py`, fonction `_CX`) :

| Paramètre | Valeur | Statut | Note |
|-----------|--------|--------|------|
| gain d'entrée | `0.22` | OREILLE | identique sur les 6 couches |
| saturation | `0.50` à `0.65` selon la couche et la variante | OREILLE | désaccordée exprès entre couches |
| HPF | `450` à `630 Hz` selon la couche | OREILLE | c'est lui qui enlève le corps de la voix |
| LPF | balayage **500 → 2000 Hz**, centre 1250 | OREILLE | voir §5, c'est le cœur du timbre |
| `flfo` (LFO de filtre interne à `fx_router_06`) | `0` | FIGÉ de fait | désactivé pour ne pas doubler le balayage de `cortex_ctrl_07` |
| wet delay | `0.10` | OREILLE | très peu |
| temps de delay | `180 ms` | OREILLE | |
| feedback | `0.06` | OREILLE | |
| `lfo` d'amplitude | `0.06` | OREILLE | |
| mode spatial | `0` (sec sur le HP d'ancrage) | OREILLE | contourné par `cortex_pair_07` en Cortex |

**Manque identifié : il n'y a pas de vraie réverbération en Cortex.** Simon demande « une réverbération donnant l'impression d'une parole provenant d'une pièce voisine ». Ce qui existe aujourd'hui est un delay à 180 ms avec 6 % de feedback et 10 % de wet — ce n'est pas une pièce, c'est un écho court. C'est probablement la raison principale pour laquelle la parole reste trop nette. → [TO DO](../Backlog/TO%20DO.md), tâche haute priorité.

---

## 5. Le balayage de filtre — signature de la zone

`pd/lib/cortex_ctrl_07.pd`. C'est le mécanisme qui fait que le Cortex ne sonne pas comme un filtre passe-bas ordinaire.

Chaque couche L1–L6 a son propre oscillateur lent qui pilote son LPF, rafraîchi toutes les 50 ms :

```text
LPF(couche n) = clip( 1250 + 750 · sin(2π · f_n · t) , 500 , 2000 )
```

| Couche | Fréquence du LFO | Période |
|--------|------------------|---------|
| L1 | 0,070 Hz | ~14,3 s |
| L2 | 0,090 Hz | ~11,1 s |
| L3 | 0,110 Hz | ~9,1 s |
| L4 | 0,130 Hz | ~7,7 s |
| L5 | 0,150 Hz | ~6,7 s |
| L6 | 0,170 Hz | ~5,9 s |

Les fréquences sont volontairement non harmoniques entre elles, donc les six couches ne sont jamais ouvertes ni fermées en même temps. C'est ce qui produit la sensation de masse qui respire.

**À étendre à 12 couches** depuis [Q1](../Backlog/Q&A.md#q1) = A. Ne pas se contenter de prolonger la suite de 0,020 Hz en 0,020 : avec douze oscillateurs il faut vérifier qu'aucune paire n'est dans un rapport simple, sinon deux couches respirent ensemble et la masse se met à pulser. C'est un réglage à faire à l'oreille, pas une formule.

**Statut : OREILLE.** À figer en priorité. Trois choses à décider :
- la **borne haute** (2000 Hz aujourd'hui) : c'est elle qui laisse passer l'intelligibilité aux moments d'ouverture ;
- la **borne basse** (500 Hz) ;
- la **vitesse** : le balayage doit-il rester audible comme un mouvement, ou devenir assez lent pour être perçu seulement comme une instabilité ?

Le paramètre `presets07.py → lpf=1500` n'est qu'une valeur initiale, écrasée par `cortex_ctrl_07` dès que l'état Cortex démarre. Ne pas la prendre pour le réglage réel.

---

## 5 bis. Plans de présence — TRANCHÉ le 20 août (V1)

[Q9](../Backlog/Q&A.md#q9) = **décision du moteur** : le plan n'est pas une colonne du classeur, Pure Data l'attribue à chaque lecture (C7 : les rôles varient). [Q10](../Backlog/Q&A.md#q10) = **deux plans seulement** ; le 3ᵉ plan Simon (`INTERMEDIAIRE`) est **abandonné** pour ce projet.

| Plan | Gain | LPF (balayage) | Réverb (delay V1) | HPF | LFO | Sample |
|------|------|----------------|-------------------|-----|-----|--------|
| `PREMIER_PLAN` | 0 dB | **800 → 2000 Hz** | wet **0,06** · 120 ms · fb 0,04 | **300 Hz** | osc. **#7** | **fixe** |
| `ARRIERE_PLAN` | **−2 dB** | **500 → 1000 Hz** | wet **0,12** · 200 ms · fb 0,08 | aucun | osc. **#0–5** | **fixe** |

Référence 07 (remplacée par les plans) : HPF 450–630 Hz, LPF 500–2000 via `cortex_ctrl_07`, wet 0,10 / delay 180 ms.

**Ce que ça change par rapport au §4.** Les plans **remplacent** le traitement uniforme par **deux chaînes distinctes sous chaque paire** : un fragment en `PREMIER_PLAN`, l'autre en `ARRIERE_PLAN`. Chaque plan a ses bornes LPF, sa vitesse de LFO et sa réverb.

**Architecture Proto 08.** Sous `cortex_pair_08`, chaque fragment passe par son propre `fx_router` avec le preset de plan choisi par le moteur, **puis** les deux sorties sont sommées. Deux gains séparés et interchangeables (C5–C7). Le gain de normalisation (`gain_db` du registre) s'applique **avant** le preset de plan, sur le `*~` en sortie de `readsf~`.

**Révision à l'oreille.** Les chiffres ci-dessus sont les **defaults Proto 08**. Une vraie réverb « pièce voisine » sur l'arrière-plan reste un plus ([TO DO](../Backlog/TO%20DO.md) §1). L'intelligibilité cible ([Q18](../Backlog/Q&A.md#q18)) peut affiner filtre/réverb sans rouvrir Q10.

**Priorité.** Indispensable depuis [Q1](../Backlog/Q&A.md#q1) = A : 12 voix au même plan = bruit, pas superposition.

---

## 6. Mouvement des paroles — rotation par paires

`pd/lib/cortex_pair_07.pd`.

Les 6 couches sont appariées de façon fixe : **L1+L2**, **L3+L4**, **L5+L6**. Chaque paire est sommée, reçoit une modulation d'amplitude lente, puis est envoyée sur **un** des trois baffles HP1/HP2/HP3.

| Élément | Valeur | Statut |
|---------|--------|--------|
| AM paire 1 (L1+L2) | 0,045 Hz, profondeur 0,14 autour de 0,82 → 0,68…0,96 | OREILLE |
| AM paire 2 (L3+L4) | 0,063 Hz, même profondeur | OREILLE |
| AM paire 3 (L5+L6) | 0,081 Hz, même profondeur | OREILLE |
| Horloge de rotation | `metro 2600 ms` | OREILLE |
| Probabilité de rotation | 62 % à chaque tick | OREILLE |
| Fondu de rotation | `12 ms` — c'est un saut, pas un panoramique | OREILLE |
| Décalage entre paires | 0 / 1 / 2 modulo 3 | FIGÉ de fait |

Le décalage garantit que deux paires ne se retrouvent jamais sur le même baffle : les trois paires permutent entre HP1, HP2 et HP3 sans collision.

**En Proto 08 : 6 paires sur 6 baffles**, décalage modulo 6. Le principe ne change pas — autant de paires que de baffles, donc une permutation du contenu sans collision. Le mouvement n'est pas perdu, il est seulement plus large.

**Problème connu — en cours de résolution.** À l'intérieur d'une paire, les deux fragments sont **sommés à poids égal** (un simple `+~`). [Q9](../Backlog/Q&A.md#q9) tranche : le moteur attribue le plan ; [Q10](../Backlog/Q&A.md#q10) fixe deux presets (§5 bis). Il manque l'implémentation sous `cortex_pair_08` : deux chaînes FX + deux gains interchangeables.
→ [Q11](../Backlog/Q&A.md#q11) et [TO DO](../Backlog/TO%20DO.md) §0 bis.

C'est le seul endroit où le comportement de zone et la logique de samples se touchent vraiment : **les plans de présence sont du timbre** (gain, filtre, réverbération), donc construits en §5 bis ; **qui va dans quel plan** est de la logique du moteur, plus tard via tags. Deux presets nommés, testables à la main dans le Proto 08.

---

## 7. Chaîne de traitement — nappes d'ambiance

`pd/lib/cortex_amb_07.pd`. Cinq lecteurs dédiés (slots 32 à 36), un par baffle HP4 → HP8.

```text
player_state_07 → *~ 0.25 → gate Cortex → AM lente → HP (4..8), direct
```

| Élément | Valeur | Statut |
|---------|--------|--------|
| gain | `0.25` | OREILLE |
| saturation | `0` | FIGÉ de fait |
| HPF | `30 Hz` | FIGÉ de fait |
| LPF | `18000 Hz` — donc pas de filtrage audible | OREILLE |
| wet / feedback | `0` / `0` — **aucune** réverbération, **aucun** delay | OREILLE, conforme à Simon |
| AM par nappe | 0,030 · … · 0,074 Hz, profondeur 0,10 | OREILLE — **acceptée** ([Q15](../Backlog/Q&A.md#q15)) |
| mouvement spatial | **aucun en Cortex** — baffle fixe | **TRANCHÉ** ([Q16](../Backlog/Q&A.md#q16)) |

Conforme à l'interdiction de Simon : pas de delay, pas de découpe rapide, pas de granulaire. [Q15](../Backlog/Q&A.md#q15) : la **modulation d'amplitude lente** (13–33 s) est **acceptée** — ce n'est pas une découpe. **Idée future :** HPF bref ~350 Hz au déclenchement piézo ([Q15](../Backlog/Q&A.md#q15), [Q14](../Backlog/Q&A.md#q14)) — hors V1.

Écarts avec la cible décidée le 20 août :

- **Cinq nappes au lieu de deux.** [Q1](../Backlog/Q&A.md#q1) = A ramène l'ambiance du Cortex à **deux baffles fixes**. Les cinq lecteurs actuels deviennent deux. À écouter de près : c'est la partie de la décision qui vide le plus l'espace.
- **Une seule famille.** `CORTEX/AMBIANCE` est un pool indifférencié. Il faut séparer **musicale** et **texture** : ce sont les deux baffles, et Simon leur donne des attributs et des comportements différents. Comment séparer — deux dossiers ou un attribut dans le tableau — est à trancher avec [Q20](../Backlog/Q&A.md#q20).
- **Durée des atomes.** [Q3](../Backlog/Q&A.md#q3) = B : le seuil de découpe passe de 2 s à **30 s minimum**. Mesuré le 20 août, la matière le permet — 17 segments de 30 s et plus, dont un de 91 s. Conséquence sur `cortex_amb_pulse_07` : re-déclencher toutes les 14 s une nappe de 60 s n'a plus de sens, il faut lire en entier ou enchaîner en fondu.
- **Aucun mouvement.** ~~Simon prévoit `SE_DEPLACER`…~~ **Tranché** ([Q16](../Backlog/Q&A.md#q16)) : texture **fixe** sur son baffle en Cortex ; `SE_DEPLACER` reporté à l'Hippocampe si besoin.

---

## 7 bis. Ambiances — milieu global, pas par baffle — TRANCHÉ le 20 août

[Q25](../Backlog/Q&A.md#q25). Complète [Q1](../Backlog/Q&A.md#q1) et [Q2](../Backlog/Q&A.md#q2).

### Principe

Pendant un passage dans le Cortex :

```text
HP1..6  →  6 paires de paroles (Belgique + Congo, plans, gestes) — indépendantes par baffle
HPa, HPb →  1 ambiance musicale + 1 ambiance texture — COMMUNES à toute la salle
```

Le **contraste Belgique/Congo** se joue **dans chaque paire** (règle C1).  
Le **contraste parole/milieu** (ex. Congo au premier plan + texture « européenne ») se joue **entre l'ensemble des paroles et les deux nappes globales** — pas entre chaque baffle et sa propre ambiance.

### Ce qui est exclu

- Ambiance locale sur chaque baffle de parole.
- Cinq ou six nappes différentes simultanées (Proto 07) — **déviation abandonnée**.
- `INTERMEDIAIRE` comme « couche d'ambiance sur tous les baffles » — ce n'est **pas** la spec écrite de Simon (§2.2.D = profondeur de **parole**).

### Comportements ambiance ([Q15](../Backlog/Q&A.md#q15), [Q16](../Backlog/Q&A.md#q16), [Q17](../Backlog/Q&A.md#q17))

| Règle | Décision |
|-------|----------|
| AM lente sur les nappes | **Oui** — petite respiration de volume, continuité préservée |
| `SE_DEPLACER` (texture) | **Non en Cortex** — baffle fixe ; pas de circulation spatiale |
| `RECOUVRIR` musicale + texture | **Mutex** — jamais les deux en recouvrement actif en même temps |

**Future (piézo, [Q14](../Backlog/Q&A.md#q14)) :** HPF momentané ~350 Hz sur les nappes — effet bref, non V1.

### Sélection (futur sélecteur)

À chaque entrée dans l'état Cortex, **une décision** :

1. Tirer / construire les 6 paires de paroles (par baffle).
2. Choisir **une** ambiance musicale et **une** texture en fonction des attributs dominants ou d'une règle de contraste — ex. majorité `CONGO` au premier plan → privilégier texture `ESPACE = EXTERIEUR` + registre bruxellois/européen.
3. Les deux nappes restent **stables** sur leurs deux baffles fixes pendant toute la durée du Cortex (40 s).

Le croisement d'attributs ambiance/parole vit dans **`gen_ambiance_cortex.py`** (à écrire), pas dans `cortex_pair_08`.

### Proto 08 (provisoire)

Tant que le sélecteur n'existe pas : tirage au hasard d'**une** musicale et d'**une** texture, identiques pour tout le monde — pas cinq nappes indépendantes.

---

## 8. Déclenchement et densité

| Élément | Valeur | Source | Statut |
|---------|--------|--------|--------|
| Durée de l'état Cortex dans le cycle AUTO | `40 s` | `CYCLE1_8HP` | OREILLE |
| Couches de parole actives | `6` | `FSM_N_8HP[0]` | OUVERT — dépend de [Q1](../Backlog/Q&A.md#q1) |
| Cascade de démarrage | 80 ms entre couches | patch | OREILLE |
| Décalage de la 2ᵉ couche d'une paire | `ovl` = 45 / 80 / 50 ms selon la variante | `presets07.py` | OREILLE |
| Re-déclenchement des paroles | ~~`metro 10 s`~~ → **abandonné** ; gestes §8 bis | [Q11](../Backlog/Q&A.md#q11) | **TRANCHÉ** |
| Re-déclenchement des nappes | `metro 14 s` | `cortex_amb_pulse_07` | OREILLE |
| Tirage | hasard, en évitant le dernier fichier **de cette couche** | `player_state_07` | provisoire — remplacé par les tags |

**Tension à résoudre.** ~~Le pulse à 10 s relance les paroles indépendamment de leur durée.~~ **Tranché le 20 août** ([Q11](../Backlog/Q&A.md#q11)) : le pulse est **abandonné** ; `EMERGER` / `RECOUVRIR` le remplace. Détail §8 bis.

---

## 8 bis. Gestes temporels — TRANCHÉ le 20 août

[Q11](../Backlog/Q&A.md#q11). Remplace `cortex_pulse_07` dans le Proto 08.

### Principe

Chaque paire (2 fragments sur 1 baffle) lit **une fois** par passage dans le Cortex. Le geste se joue **entre** les deux fragments de la paire, pas par re-déclenchement externe.

```
Fragment A (plan 1) ──┐
                      ├──► somme ──► baffle
Fragment B (plan 2) ──┘
         ▲
    geste EMERGER ou RECOUVRIR (fondu de présence)
```

### Les deux gestes

| Geste | Durée du fondu | Effet |
|-------|----------------|-------|
| `EMERGER` | **6 – 10 s** | le 2ᵉ fragment **apparaît** progressivement à côté du 1ᵉʳ, jusqu'au niveau de **son plan** |
| `RECOUVRIR` | **3 – 6 s** | le 2ᵉ fragment **monte** jusqu'au niveau de **son plan** et masque le 1ᵉʳ par contraste de présence — le plafond **est** le preset du plan, pas un dB au-dessus |

**Clarification « niveau max ».** Simon écrit « partiellement ou fortement » ; la réponse retenue est : pas de cible dB supplémentaire. Le fragment qui recouvre atteint simplement **son niveau normal** pour le plan qui lui a été assigné (`PREMIER_PLAN` = référence, `ARRIERE_PLAN` = −2 dB + filtre, etc.). Le masquage vient du **contraste entre les deux plans** et de la montée relative, pas d'un sur-gain.

### Décalage entre paires

Les **12 paires ne gestent pas en même temps**. Chaque paire reçoit un **décalage aléatoire** avant le début du fondu (étendre l'idée de l'échelonnement 80–880 ms du pulse, mais à l'échelle des fondus 3–10 s). Objectif : éviter que douze émergences partent d'un coup.

### Modes de coexistence (par paire, tirage ou déduction)

| Mode | Comportement |
|------|--------------|
| **Permanente** | les deux fragments restent à leur plan respectif toute la durée du sample — pas de fondu |
| **Dès t = 0** | le geste (`EMERGER` ou `RECOUVRIR`) démarre **à l'ouverture** du sample |
| **Liée à la durée** | si le sample est plus court que le fondu, le geste est **partiel** ; si plus long, fondu puis **coexistence stable** |

Le choix du mode dépend probablement de la durée du sample et du geste tiré — à préciser à l'implémentation.

### Tirage

- **Geste** : `EMERGER` ou `RECOUVRIR`, **50 / 50**, indépendamment par paire à chaque occurrence.
- **Plans** : attribués par le moteur ([Q9](../Backlog/Q&A.md#q9)), pas le classeur.
- **Autres mouvements** : à ajouter plus tard — prévoir un champ `geste` extensible dans le Proto 08.

### Ce qui disparaît

| Ancien | Sort |
|--------|------|
| `cortex_pulse_07` (`metro 10 s`) | **supprimé** — incompatible avec des fondus de 6–10 s |
| Re-déclenchement indépendant de la durée du sample | **supprimé** — une lecture par fragment par passage |

`cortex_amb_pulse_07` (napes) reste un sujet à part — voir §7 et [Q3](../Backlog/Q&A.md#q3).

---

## 9. Ce qu'il faut faire pour figer cette zone

Dans cet ordre, parce que chaque étape rend la suivante possible :

1. ~~**Trancher la carte des 8 HP**~~ — fait le 20 août, [Q1](../Backlog/Q&A.md#q1) = A. §3.
2. **Monter le Proto 08** avec la carte à 12 voix + 2 nappes, en gardant le tirage au hasard. C'est du câblage, pas du réglage : à ce stade on ne cherche pas encore le bon son, on cherche la bonne structure.
3. **Implémenter les plans de présence** dans le Proto 08 — spec §5 bis ([Q10](../Backlog/Q&A.md#q10) fermée). Forçables à la main pour écouter sur la même paire.
4. **Ajouter une vraie réverbération « pièce voisine »** sur les paroles, et régler la distance à l'oreille avec le LPF. C'est ce qui répond au reproche d'intelligibilité de Simon. → [Q18](../Backlog/Q&A.md#q18).
5. ~~**Trancher le conflit pulse / `EMERGER`-`RECOUVRIR`**~~ — fait le 20 août, [Q11](../Backlog/Q&A.md#q11). §8 bis. Pulse supprimé.
6. **Implémenter les gestes** (`EMERGER` 6–10 s, `RECOUVRIR` 3–6 s, décalage par paire, 50/50) dans `cortex_pair_08`.
7. **Figer le balayage de LPF** sur 12 couches : bornes, vitesse, et non-harmonicité des douze oscillateurs.
8. **Figer la rotation par paires** sur 6 baffles : horloge, probabilité, fondu.
9. **Figer les deux nappes** : gain, AM, lecture longue (≥ 30 s), séparation musicale / texture.
10. Écrire `FIGÉ` dans ce fichier et une strophe dans [`../log.md`](../log.md). À partir de là, plus de modification sans prompt explicite.

Les étapes 2 à 8 se font **sans toucher au choix des samples**. C'est exactement le but : quand les tags arriveront, le son de la zone sera déjà un acquis.
