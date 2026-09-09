# Attributs et tags — préparation du terrain

**20 août 2026** (spec) · **23 août 2026** (statut code).  
**Sélecteur C1…C11 : non implémenté.** Ni `gen_paires.py`, ni `gen_ambiance_cortex.py`, ni branchement dormant dans Pd. Ce fichier fige le vocabulaire et l'algorithme **avant** le code. Le Proto 08 tire au hasard dans les playlists — voir [`../Zones/Cortex.md`](../Zones/Cortex.md) §10 B.

Vocabulaire issu de [`../Sources/Simon - Cortex et Cortex-Ambiance.md`](../Sources/Simon%20-%20Cortex%20et%20Cortex-Ambiance.md). Questions ouvertes : [`../Backlog/Q&A.md`](../Backlog/Q&A.md).

---

## 1. Ce qu'un attribut décide, et ce qu'il ne décide pas

C'est la règle qui protège tout le reste. Sans elle, le tableau devient un deuxième endroit où on fait du sound design, et on se retrouve avec deux vérités qui divergent.

| Un attribut peut décider | Un attribut ne décide pas |
|--------------------------|---------------------------|
| **quel** fragment est joué | comment une zone sonne |
| avec **quel autre** fragment il est associé | les valeurs de filtre, saturation, réverbération |
| dans **quel plan** de présence il est placé | la vitesse et le type de mouvement spatial |
| **quand** il apparaît, et selon quel geste (émerger, recouvrir) | la carte des haut-parleurs |

Autrement dit : les attributs pilotent la **distribution** et la **dramaturgie**. Le **timbre** appartient à la zone, et il est figé dans [`../Zones/`](../Zones/).

Conséquence directe, à défendre : la colonne « Traitement ou comportement autorisé » proposée par Simon au §5.1 est à supprimer. Un fragment n'autorise pas un traitement — la zone l'impose. Voir [Q20](../Backlog/Q&A.md#q20).

Les trois plans de présence sont le seul point de contact entre les deux mondes : **construire** les plans est du timbre, donc maintenant ; **choisir** qui va dans quel plan est de la logique d'attributs, donc plus tard. C'est pour ça qu'ils doivent exister comme presets nommés avant que le sélecteur n'existe.

---

## 2. Vocabulaire — paroles

À figer tel quel. Les noms sont ceux de Simon ; ne pas en inventer de variantes.

| Attribut | Valeurs | Cardinalité |
|----------|---------|-------------|
| `CONTEXTE` | `BELGIQUE` · `CONGO` | une seule |
| `TYPE_DISCOURS` | `FAMILIAL` · `MEDIATIQUE` · `ADMINISTRATIF` · `POLITIQUE` · `DESCRIPTIF` | **plusieurs possibles** |
| `FONCTION_SOCIALE` | `NOMMER` · `CLASSER` · `RACONTER` · `TEMOIGNER` · `EXPLIQUER` | **plusieurs possibles** |
| `DENSITE_PAROLE` | `FAIBLE` · `MOYENNE` · `FORTE` | une seule — **à ajouter au classeur** |

`PRESENCE` (`ARRIERE_PLAN` / `PREMIER_PLAN` — **`INTERMEDIAIRE` abandonné**, [Q10](../Backlog/Q&A.md#q10)) **n'est pas un attribut du fichier.** C'est une décision du moteur au moment de la lecture — **tranché le 20 août** ([Q9](../Backlog/Q&A.md#q9)). Le tableau ne sert qu'à **interdire** certaines combinaisons de plans, via `DENSITE_PAROLE`. Presets : [`../Zones/Cortex.md`](../Zones/Cortex.md) §5 bis ([Q10](../Backlog/Q&A.md#q10)). Voir aussi [Q13](../Backlog/Q&A.md#q13).

Le fait que `TYPE_DISCOURS` et `FONCTION_SOCIALE` acceptent plusieurs valeurs a une conséquence à ne pas sous-estimer : la compatibilité entre deux fragments devient une question d'**intersection d'ensembles**, pas d'égalité. Un fragment `FAMILIAL + POLITIQUE` est compatible avec tout ce qui est compatible avec l'une des deux valeurs (règle C4). Dans le classeur, ces colonnes contiennent donc des listes, séparées par un caractère à fixer — proposition : `+`, comme dans les exemples de Simon.

---

## 2 bis. Règle C2 — symétrie et interdictions — TRANCHÉ le 20 août

[Q8](../Backlog/Q&A.md#q8). La table C2 du document de Simon est **asymétrique** et **incomplète** pour l'implémentation. On **ne modifie pas** le PDF source ; on corrige dans `gen_paires.py`.

### Symétrie

```text
compatible_discours(A, B) =
    table_C2(A, B)   — via C4 si tags multiples sur A ou B
    OU
    table_C2(B, A)
```

C1 impose toujours un fragment `BELGIQUE` et un fragment `CONGO` sur chaque baffle, mais **l'ordre de tirage** (Belgique d'abord ou Congo d'abord) ne doit **plus** changer le résultat C2.

### Interdictions dures (C2 bis)

Appliquées **avant** la table, quelle que soit la symétrie :

| Paire interdite | Note |
|-----------------|------|
| `POLITIQUE` ↔ `MEDIATIQUE` | Simon — jamais associés |
| `POLITIQUE` ↔ `FAMILIAL` | idem logique « pas de familial/media avec politique » |

Test : si `types(A) ∩ {POLITIQUE}` non vide **et** `types(B) ∩ {FAMILIAL, MEDIATIQUE}` non vide → **refus** (dans les deux sens).

Les lignes « `MEDIATIQUE + POLITIQUE` → `FAMILIAL` » du document de Simon décrivent un **premier fragment multi-tags**, pas une autorisation de superposer politique et médiatique sur un même baffle.

---

## 2 ter. Règle C8 — densité et plans — TRANCHÉ le 20 août

[Q13](../Backlog/Q&A.md#q13). C5 impose deux plans **différents** ; C8 précise **lesquels** quand les deux fragments sont très denses.

| Situation | Plans permis |
|-----------|--------------|
| Les deux `DENSITE_PAROLE = FORTE` | **`PREMIER_PLAN` + `ARRIERE_PLAN` uniquement** — pas deux plans « proches » |
| Autres cas | Toute paire de plans distincts (C5), selon attribution du moteur ([Q9](../Backlog/Q&A.md#q9)) |

En **V1** (deux plans seulement, [Q10](../Backlog/Q&A.md#q10) — `INTERMEDIAIRE` abandonné), C8 est **satisfaite automatiquement** dès que C5 est respectée.

**Encore ouvert :** définition de « dense » à l'oreille — à fixer en remplissant `densite_parole`.

---

## 3. Vocabulaire — ambiances

| Attribut | Ambiance musicale | Ambiance texture |
|----------|-------------------|------------------|
| `TYPE_AMBIANCE` | `MUSICALE` | `TEXTURE` |
| `ACTIVITE` | `CALME` · `MOYENNE` | `MOYENNE` · `FORTE` |
| `CONTINUITE` | `STABLE` · `EVOLUTIVE` | `EVENEMENTIELLE` · `STABLE` |
| `ESPACE` | `EXTERIEUR` | `EXTERIEUR` · `INDETERMINE` |
| `PRESENCE_HUMAINE` | `ABSENTE` | `IDENTIFIABLE` · `DIFFUSE` |
| `DUREE` | 30 s → 7 min | 30 s → 7 min |

Remarque utile : les plages de valeurs des deux familles sont presque disjointes. `PRESENCE_HUMAINE = ABSENTE` n'existe qu'en musicale, `EVENEMENTIELLE` et `INDETERMINE` n'existent qu'en texture. La famille est donc quasiment **déductible** des autres attributs — ce qui veut dire soit que `TYPE_AMBIANCE` est redondant, soit que ces plages sont trop strictes et qu'il existera des cas réels qui n'entrent dans aucune des deux colonnes. À vérifier en écoutant la matière.

`DUREE` se mesure automatiquement, ne pas la saisir à la main. Attention : la matière actuelle ne respecte pas du tout cette plage, voir [Q3](../Backlog/Q&A.md#q3).

Trois de ces attributs — `ACTIVITE`, `CONTINUITE`, `PRESENCE_HUMAINE` — ne sont utilisés par **aucune règle** du document de Simon. **Tranché le 20 août** ([Q23](../Backlog/Q&A.md#q23)) : **descriptifs** pour le classeur en V1 ; règles automatiques reportées à `gen_ambiance_cortex.py`.

---

## 4. Vocabulaire — usage sonore (axe propre à Loumana)

Deuxième axe, complémentaire et indépendant de celui de Simon. Celui de Simon décrit **ce que dit** le fragment ; celui-ci décrit **comment il sonne** et donc où il est utile.

| Attribut | Valeurs proposées | Rôle |
|----------|-------------------|------|
| `FAMILLE_SON` | `pad` · `melody` · `rythmique` · `bruit` · `voix` | ce que c'est à l'oreille |
| `USAGE_PREFERE` | `cortex` · `nappe` · `hippo` · `recon` · `boucle` · vide | où ça marche le mieux |

Exemples déjà énoncés : les ambiances **rythmiques** vont bien à l'Hippocampe ; les ambiances **pad** et **melody** vont bien en nappe de Cortex. Avant, ce choix passait par le dossier (`CORTEX/AMBIANCE` vs `HIPPOCAMPE/AMBIANCE`). Depuis le pool partagé `SONS_V3/AMBIANCE/`, c'est **`usage_prefere`** et les attributs Simon qui orientent le moteur.

Règle proposée : **`USAGE_PREFERE` prime sur le dossier** quand il est renseigné. C'est ce qui permet de corriger un mauvais rangement sans déplacer de fichier — donc sans casser les ID.

Cet axe a un avantage pratique décisif : il est **utilisable immédiatement**, sans attendre aucune réponse de Simon, et il ne dépend pas de la distinction Belgique / Congo qui n'existe pas encore dans la matière. C'est le premier à remplir.

---

## 5. Schéma du classeur — TRANCHÉ le 20 août (mis à jour : pool ambiances partagé)

[Q20](../Backlog/Q&A.md#q20) : **une feuille par zone de parole** (Cortex, Hippocampe, Reconstruction) + **une feuille Ambiances** pour le pool partagé `SONS_V3/AMBIANCE/`.

Depuis le 20 août (après-midi) : les ambiances ne vivent plus dans `<zone>/AMBIANCE/`. Un même wav peut servir au Cortex, à l'Hippocampe ou ailleurs ; c'est le classeur (`usage_prefere`, attributs Simon) qui décide **où** et **comment** il est utilisé — plus le dossier de rangement.

### Feuilles Paroles (Cortex · Hippocampe · Reconstruction)

Même colonnes sur les trois feuilles — **paroles seulement** (`FRAGMENTS` + `LONG_MOYEN`).

| Colonne | Source |
|---------|--------|
| `id` · `type` · `duree_s` | auto |
| `contexte` · `type_discours` · `fonction_sociale` · `densite_parole` | oreille |
| `famille_son` · `usage_prefere` · `notes` | oreille |

### Feuille Ambiances (`SONS_V3/AMBIANCE/`)

| Colonne | Source |
|---------|--------|
| `id` · `duree_s` · `master` | auto (`master` = piste V6 d'origine, registre) |
| `type_ambiance` · `activite` · `continuite` · `espace` · `presence_humaine` | oreille |
| `famille_son` · `usage_prefere` · `notes` | oreille |

`type_ambiance` sépare **musicale** et **texture** pour les deux baffles Cortex ([Q1](../Backlog/Q&A.md#q1)). `usage_prefere` (`cortex` · `nappe` · `hippo` · `recon`…) remplace l'ancien rangement par dossier — voir §4.

- **La notion de préférence est retenue** — colonne `usage_prefere`.
- **La colonne « traitement souhaité » reste en suspens** — non créée.

Deux exigences sur `gen_catalogue_xlsx.py` : **conserver** les cellules remplies (clé = `id`) ; ajouter des lignes vides pour les nouveaux fichiers sans écraser l'existant.

### Feuille Reconstruction — schéma Simon — TRANCHÉ le 21 août

[Q32](../Backlog/Q&A.md#q32) : la feuille **Reconstruction** n'utilise **plus** les colonnes paroles Cortex/Hippo ci-dessus. Elle reçoit le vocabulaire Simon §26.1 (`granularite`, `role_compositionnel`, `mutabilite`, `charge_semantique`, `provenance_materiau`, `type_matiere`, `mode_lecture`, `transformations_autorisees`… — liste complète dans la spec source).

| Colonne | Source |
|---------|--------|
| `id` · `duree_s` | auto |
| colonnes §26.1 Simon | oreille — **Simon**, quand la nouvelle banque arrive |
| `notes` | oreille |

**21 août (proto moteur)** : colonnes Simon **présentes mais vides** ; les 287 fichiers actuels servent au développement avec heuristiques (durée, tirage). Pas de re-classement urgent.

---

## 6. Architecture proposée pour le moteur

### Le problème

Les règles de Simon (C1 à C11) sont **relationnelles** : étant donné un fragment A, trouver un fragment B compatible selon deux tables croisées, sur des attributs multivalués, puis leur attribuer deux plans différents, puis choisir un geste temporel. Pure Data est un très mauvais outil pour ça. Écrire ces règles en objets Pd donnerait quelque chose d'illisible, d'impossible à tester, et de silencieusement faux.

### La solution : précalculer les paires en Python

Le projet fait déjà exactement ça pour les playlists : `gen_prototype_07_8hp.py` produit `pd/lib/playlists07/slot_*.txt` et Pure Data se contente de tirer une ligne. On étend le même principe.

```text
catalogue_fragments.xlsx
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼
  gen_paires.py                         gen_ambiance_cortex.py
  C1..C11, C2 symétrique ([Q8])         croisement global parole ↔ ambiance
        │                                      │
        ▼                                      ▼
  paires_cortex.txt                    ambiance_cortex.txt
  (6 lignes = 6 paires, 1 par baffle)  (1 musicale + 1 texture / passage)
        │                                      │
        └──────────────┬───────────────────────┘
                       ▼
              Pure Data : lit les fichiers, applique presets
```

**Par baffle** (`gen_paires.py`) : Belgique + Congo, plans, geste — une ligne **par baffle de parole**.

**Global** (`gen_ambiance_cortex.py`) : **une** musicale + **une** texture pour **tout** l'état Cortex — [Q25](../Backlog/Q&A.md#q25). Le croisement dramaturgique (ex. paroles Congo + milieu européen) se décide **ici**, pas en ajoutant une ambiance sur chaque HP1–6. Voir [`../Zones/Cortex.md`](../Zones/Cortex.md) §7 bis.

### Algorithme de sélection des paires — TRANCHÉ le 20 août

[Q5](../Backlog/Q&A.md#q5), [Q6](../Backlog/Q&A.md#q6), [Q7](../Backlog/Q&A.md#q7), [Q8](../Backlog/Q&A.md#q8).

```text
Pour chaque baffle :
  1. Tirer fragment A (BELGIQUE ou CONGO — ordre libre pour C2 symétrique)
  2. Chercher fragment B (contexte opposé) :
       a. Filtrer C2 (TYPE_DISCOURS, symétrique) + interdictions dures §2 bis
       b. Croiser avec C3 (FONCTION_SOCIALE) si candidats restants
       c. Si vide → relâcher C3 seulement ([Q7] = B)
       d. Si vide → relâcher C2, garder C1 seulement
  3. Tirer uniformément au hasard parmi les candidats restants ([Q6])
  4. En cas de conflit C2 vs C3 → C2 prime ([Q5])
  5. Attribuer plans (moteur, [Q9]) ; appliquer C8 si les deux FORTE ([Q13])
  6. Tirer geste EMERGER/RECOUVRIR 50/50 ([Q11])
```

**Ce que ça donne :**

- **Les règles sont lisibles et testables.** On peut écrire des tests, changer une table, régénérer, comparer. En Pd, rien de tout ça n'est possible.
- **Pure Data reste bête.** Il tire une ligne dans un fichier texte, exactement comme aujourd'hui. Aucun risque d'introduire une erreur de logique dans le patch.
- **On peut inspecter le résultat avant de l'entendre.** Le fichier de paires est du texte : on peut le lire, compter, vérifier qu'une association bizarre n'y est pas.
- **Coût négligeable.** Avec une centaine de fragments de Cortex, le nombre de paires valides après filtrage par C1 (Belgique × Congo) reste de l'ordre de quelques milliers de lignes. C'est un fichier texte minuscule.

### L'audit qui répond à une question ouverte

En même temps que les paires, `gen_paires.py` produit un rapport :

- combien de paires valides au total ;
- combien de fragments ne sont **jamais** utilisables, et pourquoi ;
- combien de paires si on applique C2 et C3 en contrainte dure, contre combien si on relâche C3, contre combien si on relâche les deux.

Ce rapport mesure l'impact du relâchement par étapes ([Q7](../Backlog/Q&A.md#q7) = B) sur un classeur partiel — combien de paires restent si on abandonne C3, puis C2.

C'est la raison pour laquelle **l'audit doit être écrit avant le sélecteur**, et même avant que le classeur ne soit entièrement rempli : il peut tourner sur un remplissage partiel et dire tout de suite si le jeu de règles tient debout.

### Ce que Pure Data doit gagner comme mécanismes

Indépendamment des attributs, et donc dès maintenant :

| Mécanisme | Pourquoi | État (23 août) |
|-----------|----------|----------------|
| Deux gains distincts sous chaque paire | sans ça, aucun plan de présence n'est possible | **PARTIEL** — gains + swap en `cortex_pair_08` ; pas encore 2× `fx_router` distincts par plan |
| Deux presets de plan nommés, forçables à la main | pour les écouter et les figer | **defaults** §5 bis Cortex — chaînes FX complètes à finaliser |
| Un lecteur capable de recevoir un **nom de fichier** plutôt qu'un index de tirage | pour que le sélecteur décide, pas le lecteur | **ABSENT** — `player_state_08` tire un index dans `playlists08/`. **Ne pas** patcher l'anti-doublon dedans : [`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) §10 « Piège » |
| Fondus pilotables pour `EMERGER` et `RECOUVRIR` | les gestes temporels | **FAIT** — `cortex_pair_08` / `cortex_amb_behav_08` |
| `s6_tag_hook` | point d'accroche | présent (hippo) ; **non branché** au sélecteur Cortex |

Les deux premières lignes sont dans [`../Backlog/TO DO.md`](../Backlog/TO%20DO.md) §1 : elles ne dépendent d'aucune réponse et se font pendant le gel du Cortex.

---

## 7. Ordre de travail

Chaque étape est utile même si la suivante n'arrive jamais.

1. ~~**Rendre les ID stables**~~ — **fait le 20 août** ([Q21](../Backlog/Q&A.md#q21) = option A). La découpe est incrémentale, les noms de fichiers ne bougent plus, le classeur conserve ce qui est rempli. Le travail de classification n'est plus jetable.
2. ~~**Trancher la structure des colonnes**~~ — fait le 20 août, [Q20](../Backlog/Q&A.md#q20) et [Q19](../Backlog/Q&A.md#q19). ~~Appliqué dans `gen_catalogue_xlsx.py`~~ — fait le 20 août (16 colonnes, migration des anciennes colonnes Phrase/Attributs/Comportements vers `notes`).
3. **Remplir `famille_son` et `usage_prefere`** — l'axe §4. Ne dépend de personne, améliore déjà le tirage actuel sans changer une seule règle de zone.
4. **Remplir `type_ambiance`** sur les 27 nappes. C'est court, et c'est ce qui débloque les deux baffles d'ambiance du Cortex.
5. **Figer le son du Cortex** ([`../Zones/Cortex.md`](../Zones/Cortex.md)) — structurellement avancé (§10). **Hippocampe** : spec Simon reçue, décisions Q26–Q28, mais **loin du gel** ([`../Zones/Hippocampe.md`](../Zones/Hippocampe.md) §9) — ne pas le traiter au même stade que le Cortex.
6. **Écrire l'audit** `gen_paires.py` en mode rapport seulement, sur un classeur partiellement rempli, pour mesurer si les règles de Simon tiennent — en particulier s'il y a assez de fragments de chaque contexte. [Q4](../Backlog/Q&A.md#q4) reconnaît que la réponse est inconnue.
7. **Répondre à [Q7](../Backlog/Q&A.md#q7)** avec le rapport en main.
8. **Alors seulement** écrire le sélecteur, dans le Proto 08 ([Q24](../Backlog/Q&A.md#q24) = A) : `gen_paires.py` (par baffle) + `gen_ambiance_cortex.py` (global, [Q25](../Backlog/Q&A.md#q25)).

---

## 8. Ce qu'il ne faut pas faire

- **Ne pas coder de graphe « le fragment A déclenche le fragment B »** avant que le classeur ne soit suffisamment rempli. Sur un tableau vide, un graphe de relations ne produit que du hasard déguisé, impossible à évaluer à l'oreille.
- **Ne pas mettre de valeur de traitement dans le tableau.** Voir §1.
- **Ne pas écrire les règles d'association en objets Pure Data.** Voir §6.
- **Ne pas déplacer de fichiers entre dossiers** pour corriger un rangement : utiliser `usage_prefere`. Déplacer change les ID.
- **Le classeur est prêt à remplir** depuis le 20 août : colonnes §5 appliquées. Regen sans perte : `python3 scripts/gen_catalogue_xlsx.py` (clé = `id`).
