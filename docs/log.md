# Log — Mémoires en transit / Proto 07

**Append-only.** Ne pas réécrire une entrée déjà datée.  
Après chaque changement demandé par Loumana : **une strophe ici** + corriger [`etatactuel.md`](./etatactuel.md) si le son ou le câblage a changé.

Le prompt du chat = la décision. Le backlog n’est pas un contrat.

> Les liens des strophes **antérieures au 20 août** peuvent être cassés : les docs ont été réorganisés ce jour-là et ces fichiers sont maintenant dans [`archive/`](./archive/) ou [`Matiere/`](./Matiere/). Les strophes ne sont pas réécrites — c'est un journal.

---

---

---

---

---

---

---

---

## 2026-08-20 — SONS_V3 : pool ambiances partagé + feuille Ambiances

**Prompt :** rangement propre — ambiances à la racine de `SONS_V3/`, partagées entre zones ; feuille **Ambiances** dans le classeur.

**Matière — `SONS_V3/AMBIANCE/`** (69 wav). Zones = paroles seulement (`FRAGMENTS` + `LONG_MOYEN`).

**Code — `sons_v3_paths.py`** · `gen_catalogue_xlsx.py` (4 feuilles) · `slice_opacite_v3.py` · `normaliser_niveaux.py` · `sons_audit07.py`.

**Doc — [`Matiere/Pipeline.md`](./Matiere/Pipeline.md), [`Matiere/Attributs.md`](./Matiere/Attributs.md) §5.**

---

## 2026-08-20 — Classeur : colonnes §5 appliquées

**Prompt :** « oui tu peux rajoute les colonnes » — aligner `catalogue_fragments.xlsx` sur [`Matiere/Attributs.md`](./Matiere/Attributs.md) §5.

**Changement — `scripts/proto07/gen_catalogue_xlsx.py`.** 16 colonnes : `ID`, `Type`, `Durée (s)`, `Nature` (auto) + `Contexte`, `Type discours`, `Fonction sociale`, `Densité parole`, `Type ambiance`, `Activité`, `Continuité`, `Espace`, `Présence humaine`, `Famille son`, `Usage préféré`, `Notes`. Migration : anciennes colonnes Phrase / Attributs / Comportements → `Notes`. Regen : `python3 scripts/gen_catalogue_xlsx.py` (526 lignes, 3 feuilles).

**Doc — [`Matiere/Pipeline.md`](./Matiere/Pipeline.md), [`Backlog/TO DO.md`](./Backlog/TO%20DO.md).** Le classeur est prêt à remplir à l'oreille.

---

## 2026-08-20 — 7 réponses Q&A : sélecteur + ambiances Cortex

**Prompt :** Loumana a répondu à Q5, Q6, Q7, Q13, Q15, Q16, Q17 dans le Q&A.

**Sélecteur ([Q5–Q7](../Backlog/Q&A.md)).** C2 prime sur C3 · relâchement par étapes (C3 puis C2, jamais C1) · tirage **uniforme** sans bonus double compatibilité · C8 : deux `FORTE` → extrémités des plans ([Q13](../Backlog/Q&A.md#q13)).

**Ambiances Cortex.** AM lente OK ([Q15](../Backlog/Q&A.md#q15)) · pas de `SE_DEPLACER` en Cortex ([Q16](../Backlog/Q&A.md#q16)) · mutex recouvrement musicale/texture ([Q17](../Backlog/Q&A.md#q17)).

**Changement — [`Matiere/Attributs.md`](./Matiere/Attributs.md) §2 ter, §6 (algorithme) · [`Zones/Cortex.md`](./Zones/Cortex.md) §7, §7 bis.**

**Encore ouvert :** Q10 (réverb/LFO), Q12 (C9/C10), Q18, Q14 (piézo).

---

## 2026-08-20 — Q8 : table C2 symétrisée + interdictions dures

**Prompt :** la table C2 de Simon est asymétrique ; réponse Loumana.

**Réponse [Q8](./Backlog/Q&A.md#q8) = B — symétriser.** `compatible(A,B) = C2(A,B) ∨ C2(B,A)` (avec C4 pour tags multiples). C1 garde Belgique + Congo par baffle, mais l'ordre de tirage ne biaise plus C2.

**Interdictions dures (C2 bis) :** jamais `POLITIQUE` + `MEDIATIQUE` (Simon) ; jamais `POLITIQUE` + `FAMILIAL` / `MEDIATIQUE` (familial/media + politique).

**Changement — [`Matiere/Attributs.md`](./Matiere/Attributs.md) §2 bis.** Le PDF de Simon reste intact ; la correction vit dans `gen_paires.py`.

**Pas fait :** `gen_paires.py` n'existe pas encore.

---

## 2026-08-20 — Q25 : ambiances globales, croisement au niveau de l'état Cortex

**Prompt :** formaliser la décision — pas d'ambiance par baffle ; croisement parole/ambiance (ex. Congo + milieu européen) au niveau global.

**Réponse [Q25](./Backlog/Q&A.md#q25) = B — global.**

- **6 baffles parole** : paires Belgique/Congo, plans, gestes — **indépendants par baffle**.
- **2 baffles ambiance** : une musicale + une texture, **communes à toute la salle** pendant le Cortex.
- Le croisement dramaturgique se décide **une fois par passage** dans le Cortex, pas six fois.
- Le Proto 07 (5 nappes sur HP4–8) est une **déviation abandonnée**.
- **`INTERMEDIAIRE`** (Simon §2.2.D) = profondeur de **parole**, pas ambiance par baffle → **3ᵉ plan reporté V1** ; deux plans suffisent pour commencer.

**Changement — [`Zones/Cortex.md`](./Zones/Cortex.md) §7 bis** · [`Matiere/Attributs.md`](./Matiere/Attributs.md) §6 (schéma `gen_paires` + `gen_ambiance_cortex`).

**Pas fait :** `gen_ambiance_cortex.py` n'existe pas. Proto 08 : tirage aléatoire d'une paire d'ambiances en attendant.

---

## 2026-08-20 — Q11 : EMERGER/RECOUVRIR remplace le pulse

**Prompt :** Loumana répond à [Q11](./Backlog/Q&A.md#q11).

**Choix d'architecture.** **`EMERGER` / `RECOUVRIR` remplace `cortex_pulse_07`.** Fini le re-déclenchement toutes les 10 s : chaque paire lit ses fragments une fois, le geste se joue à l'intérieur.

**Paramètres.**

| | EMERGER | RECOUVRIR |
|--|---------|-----------|
| Durée du fondu | **6 – 10 s** | **3 – 6 s** |
| Cible | niveau du plan assigné | idem — pas de dB au-dessus du preset |
| Probabilité | **50 %** | **50 %** |

**Clarification « niveau max ».** La question posait « partiellement ou fortement » en dB. Réponse : le plafond **est** le niveau normal du plan (`PREMIER_PLAN`, `ARRIERE_PLAN`, etc.). Le masquage vient du contraste entre plans + fondu relatif, pas d'un sur-gain.

**Décalage.** Les 12 paires ne gestent **pas** en même temps — décalage aléatoire par paire avant le fondu.

**Coexistence — trois cas, pas une durée fixe :** permanente (deux plans stables) ; geste dès t = 0 ; durée du sample qui limite ou prolonge le geste.

**Extension.** D'autres mouvements à ajouter plus tard — champ `geste` extensible prévu au Proto 08.

**Changement — [`Zones/Cortex.md`](./Zones/Cortex.md) §8 bis.** Spec complète. [Q12](./Backlog/Q&A.md#q12) : tables C9/C10 probablement redondantes pour la V1.

**Pas fait :** aucun code Pd.

---

## 2026-08-20 — Q9 tranché, Q10 partiel : deux plans de présence

**Prompt :** Loumana a répondu à [Q9](./Backlog/Q&A.md#q9) et partiellement à [Q10](./Backlog/Q&A.md#q10).

**[Q9](./Backlog/Q&A.md#q9) = décision du moteur.** Pure Data attribue le plan à chaque lecture ; pas de colonne `PRESENCE` au classeur. Le tableau sert seulement à interdire certaines combinaisons via `DENSITE_PAROLE` (C8, à préciser en [Q13](./Backlog/Q&A.md#q13)). Cohérent avec la normalisation (`gain_db` au registre, présence au moteur) et C7 (variation des rôles).

**[Q10](./Backlog/Q&A.md#q10) = deux plans sur trois.**

| Plan | Gain | LPF | Réverb | HPF |
|------|------|-----|--------|-----|
| `PREMIER_PLAN` | normal | 800→2000 Hz, vitesse propre | moins qu'aujourd'hui | 300 Hz |
| `ARRIERE_PLAN` | −2 dB | 500→1000 Hz | oui | aucun |
| `INTERMEDIAIRE` | — | — | — | — |

**Ce que ça implique.** La distance perçue ne repose pas surtout sur le gain (−2 dB seulement entre premier et arrière) : c'est surtout **filtre + réverb + HPF** qui séparent les plans. L'arrière-plan n'a **pas de HPF** (plus de corps / proximité) mais un LPF plus bas et plus de réverb — cohérent avec « pièce voisine ». Le premier plan monte le HPF à 300 Hz et ouvre le balayage dès 800 Hz.

**Changement — [`Zones/Cortex.md`](./Zones/Cortex.md) §5 bis.** Table des presets + architecture Proto 08 (deux chaînes FX sous chaque paire, gain de normalisation avant le preset).

**Pas fait :** aucun code Pd. Le Proto 08 n'existe pas encore. **`INTERMEDIAIRE`** et les niveaux exacts de réverb restent ouverts.

---

## 2026-08-20 — Niveaux : l'écart de 49 dB vient de l'intro du master Cortex

**Prompt :** « il y a beaucoup de dB de différence entre chaque sample, je voudrais les normaliser, est-ce que tu penses que c'est une bonne idée ? »

**Ce que la mesure a corrigé.** Le chiffre de 42 dB annoncé la veille était un écart de **pics**, ce qui ne dit rien d'utile sur de la parole. Mesuré en sonie de parole active (RMS par blocs de 50 ms, blocs à moins de 30 dB du plus fort), l'écart réel est de **49 dB** — mais il n'est pas réparti sur la matière, il est localisé. Les **250 premières secondes du master Cortex sont 27 dB sous le reste** : médiane −49,0 dBFS sur l'intro contre −22,3 dBFS ensuite. Les douze fragments les plus faibles viennent tous des 208 premières secondes. Le master Reconstruction n'a pas ce défaut (2 fichiers isolés sur 288). En écartant l'intro, l'étendue du Cortex tombe de 47 à 19 dB, et la **moitié centrale de toutes les paroles tient dans 8 dB** — ce qui est normal.

**Pourquoi normaliser quand même, et la vraie raison.** Ce n'est pas une question de volume. La **saturation est non linéaire** : les couches du Cortex passent par `sat` 0,50 à 0,65, donc un fragment à −14 dBFS attaque le saturateur et un fragment à −45 dBFS ne le touche pas. Le *timbre* de la zone dépend aujourd'hui du fichier tiré, ce qui contredit frontalement le principe en cours d'établissement — la zone impose son timbre, pas le fichier. Second motif, décisif : les **plans de présence** de [Q10](./Backlog/Q&A.md#q10) sont des écarts de 6 à 10 dB, inaudibles comme intention sur une matière qui bouge de 49 dB. La normalisation est donc un **préalable à Q10**, pas un confort.

**À noter — normaliser, c'est répondre à [Q9](./Backlog/Q&A.md#q9).** Q9 demande si la présence est un attribut du fichier ou une décision du moteur. Aplatir la matière suppose la seconde réponse. Si une part de la distance est censée être inscrite au mixage par Simon, l'aplatissement détruit son intention. Les deux questions n'en font qu'une, et c'est celle-là qu'il faudra trancher pour de bon.

**Changement — `scripts/normaliser_niveaux.py`.** Mesure les 526 fragments et inscrit deux colonnes dans le registre, `niveau_db` et `gain_db`. **Aucun wav n'est modifié** : la mesure est toujours refaite sur le fichier d'origine, donc relancer le script ne peut pas cumuler deux normalisations, et le geste reste réversible et auditable. Cibles séparées, −23 dBFS pour les paroles et −45 dBFS pour les ambiances : le but n'est pas d'aligner les deux familles mais de rendre chacune cohérente, pour que l'équilibre parole/ambiance devienne un réglage du moteur au lieu d'une propriété de la matière. Résultat : paroles de 49 à 26 dB d'étendue, ambiances de 48 à 1 dB, gain médian **+1,0 dB** et 38 % des fichiers qui bougent de 3 dB ou moins. C'est volontairement peu : la correction se concentre sur les aberrants.

**Le garde-fou qui compte — plafond de gain à +12 dB.** Sans lui, les tranches quasi vides seraient amplifiées de 30 dB et produiraient du souffle sur un haut-parleur : `C002` est à −54,9 dBFS pour un fond à −57,7, soit **moins de 3 dB d'écart** — ce n'est pas une voix discrète, c'est du fond de salle gardé par le détecteur de silence. 31 fragments sont plafonnés. Mais le rapport montre que le plafond bloque aussi de la matière réelle : `C011`, `C013` et `C015` ont 14 à 23 dB de dynamique interne, donc du contenu véritable, simplement mixé 25 dB trop bas. Raison de plus pour traiter la cause dans le master plutôt que le symptôme au gain.

**Changement — `slice_opacite_v3.py`.** `REG_FIELDS` déclare désormais `niveau_db` et `gain_db`, et l'écriture du registre passe en `restval=""`. Sans ça, la prochaine découpe aurait silencieusement effacé les deux colonnes.

**Pas fait :** le gain n'est **pas encore appliqué au son**. Le point d'injection est identifié — chaque lecteur a déjà un `*~ 0.9` en sortie de `readsf~` dans `player_state_07` — et le câblage passe par un troisième mot dans les lignes des playlists. Ça se fera dans le Proto 08, avec les plans de présence qui ont besoin de la même plomberie. Rien n'a donc changé à l'écoute pour l'instant.

---

## 2026-08-20 — 8 réponses au Q&A : carte des HP tranchée, Proto 08 décidé

**Prompt :** Loumana a répondu à huit questions du Q&A.

**Réponses.** [Q1](./Backlog/Q&A.md#q1) = **A** (suivre Simon : 6 baffles de parole × 2 fragments). [Q2](./Backlog/Q&A.md#q2) : la définition de zone du projet est conservée ; l'ambiance du Cortex tient deux baffles **fixes**, pas forcément HP7/HP8 ; celle de l'Hippocampe bouge lentement de baffle en baffle et doit être une matière **totalement différente** ; la Reconstruction n'en veut pas. [Q3](./Backlog/Q&A.md#q3) = **B** (seuil de 30 s). [Q4](./Backlog/Q&A.md#q4) : Belgique/Congo viendra du tableau, pas encore documenté, ça répète en cas de pénurie, non implémenté pour l'instant. [Q19](./Backlog/Q&A.md#q19) : pas à pas, le vocabulaire s'applique à tous les fragments, l'Hippocampe arrive. [Q20](./Backlog/Q&A.md#q20) : une feuille par zone, avec préférences ; « traitement souhaité » en suspens. [Q21](./Backlog/Q&A.md#q21) = **A**. [Q24](./Backlog/Q&A.md#q24) = **A** (Proto 08).

**Ce que ça change — le Cortex passe à 12 voix.** C'était la contradiction la plus lourde du projet, elle est tranchée en faveur de Simon : 6 baffles de parole portant 2 fragments chacun, et 2 baffles d'ambiance. Conséquences chiffrées, toutes portées dans [`Zones/Cortex.md`](./Zones/Cortex.md) §3 : 14 lecteurs au lieu de 11, le balayage de LPF à étendre de 6 à 12 oscillateurs sans rapport simple entre eux, 6 paires permutant sur 6 baffles au lieu de 3 sur 3, et plus aucun baffle libre. Vérifié au passage : la rotation des paroles **n'est pas** perdue, le principe « autant de paires que de baffles » est simplement étendu.

**Le vrai risque de cette décision** n'est pas le CPU, c'est que l'ambiance passe de 5 nappes à 2 : l'espace autour des paroles se vide beaucoup. Et surtout, douze voix filtrées au même niveau ne font pas une superposition, elles font du bruit. Les **plans de présence** cessent donc d'être une amélioration pour devenir une condition. [Q10](./Backlog/Q&A.md#q10) et [Q11](./Backlog/Q&A.md#q11) sont passées en tête de l'ordre de priorité du Q&A, devant les questions de sélection — elles ne dépendent d'aucun tag et s'écoutent sur la matière actuelle.

**Ce qui est décidé sans être bloquant.** Le Proto 08 se construit avec le tirage au hasard : [Q4](./Backlog/Q&A.md#q4) diffère la règle C1 jusqu'à ce que le tableau existe. C'est exactement la séparation demandée depuis le début — figer le son de la zone d'abord, brancher la logique de choix ensuite. À noter que [Q4](./Backlog/Q&A.md#q4) reconnaît ne pas savoir s'il y a assez de fragments par contexte : avec 6 paires il en faut 6 + 6 à chaque instant, donc l'audit `gen_paires.py` en mode rapport doit précéder l'écriture de la moindre règle.

**Le classeur est débloqué.** [Q20](./Backlog/Q&A.md#q20) confirme la structure en 3 feuilles, une par zone, et [Q19](./Backlog/Q&A.md#q19) étend le vocabulaire à tous les fragments : les trois feuilles ont donc les mêmes colonnes. Schéma arrêté dans [`Matiere/Attributs.md`](./Matiere/Attributs.md) §5, avec une colonne `nature` pour que paroles et ambiances cohabitent dans la même feuille sans mélanger leurs attributs. La colonne « traitement souhaité » n'est **pas** créée, la réponse étant « peut-être, je ne sais pas encore ».

**Deux dépendances matière nouvelles.** L'Hippocampe a besoin d'un master d'ambiance propre : le repli actuel sur les nappes du Cortex, jusqu'ici présenté comme un arrangement acceptable, ne l'est plus — [Q2](./Backlog/Q&A.md#q2) exige une matière totalement différente, et filtrer autrement la même matière ne change pas de lieu. Et la colonne `type_ambiance` doit être remplie sur les 27 nappes, sinon les deux baffles *musical* et *texture* tirent dans le même sac.

**Changement — ancres du Q&A.** Le formateur de l'éditeur a supprimé les 24 ancres `<a id="qn">` en enregistrant, cassant d'un coup les 64 liens internes du projet. Les intitulés sont maintenant réduits à `## Qn` avec le titre en gras dessous : le slug natif est alors exactement `#qn`, les liens existants fonctionnent sans modification, et aucun formatage ne peut plus les casser. Consigne inscrite en tête du fichier pour que personne ne « corrige » ça.

**Pas fait :** aucun code. Le Proto 08 n'existe pas encore, seule sa spécification est écrite.

---

## 2026-08-20 — Robustesse d'expo : vérif des sons, retry USB, découplage pdbuild

**Prompt :** faire d'abord les trois points utiles de l'audit reçu.

**Pourquoi :** l'audit contenait douze points, dont un seul vraiment dangereux à appliquer et trois qui valaient le coup. Le fil directeur retenu : pour une installation, le risque n'est pas le plantage, c'est **le silence que personne ne remarque**.

**Changement — `scripts/verifier_sons.py`.** Nouveau contrôle à lancer avant chaque expo. Il lit les 526 wav en une seconde et vérifie format (mono 48 kHz 16 bits), durée, fichiers muets, trous internes de plus de 5 s, saturation ; puis que les **3481 références** des 27 playlists existent bien sur le disque ; puis que le registre des ID et le disque disent la même chose. Code retour 1 s'il y a une erreur, donc chaînable avec `test_patch_console.sh`. Testé avec trois fichiers pièges (illisible, muet, stéréo 44,1 kHz) : les trois sont attrapés. Motivation historique : le calibrage du 06 avait trouvé 8 segments morts dont 14 s de silence pur, et `sons_audit07` ne faisait plus cette vérification.

**Résultat de la première passe.** Aucune erreur. Mais un vrai constat d'écoute : **42 dB d'écart** entre le fragment le plus faible et le plus fort, pic médian −9 dBFS, et 15 fragments entre −35 et −42 dBFS. Ce ne sont pas des fichiers défectueux — c'est la densité perçue du Cortex qui varie au hasard selon le tirage. Reste à trancher à l'oreille.

**Changement — retry USB dans `launch.sh`.** La détection de la Scarlett faisait un seul `timeout 8` puis `exit 1`. Au démarrage du Pi, l'énumération USB peut dépasser 8 s : le service tombait et l'expo restait muette. Maintenant quatre tentatives à délais croissants (0, 3, 6, 12 s), `timeout` à 15 s, le device retenu tracé dans `deploy/debian/derniere_carte.log`. En cas d'échec, croisement avec `aplay -l` pour distinguer « carte pas branchée » de « Pd ne sait plus l'annoncer » — le parsing dépend du format de `pd -listdev`, qui peut changer d'une version à l'autre — et la sortie brute est conservée pour autopsie. Parseur awk revérifié sur une sortie simulée : il retient bien le device *plug-in* de la Scarlett.

**Changement — `pdbuild` découplé.** `gen_patch07.py` et `gen_libs07.py` importaient `proto06_lib.pdbuild` via un `sys.path.insert` vers `scripts/proto06`. Le générateur du prototype courant dépendait donc d'un sous-arbre figé et, depuis ce matin, hors service : supprimer `proto06/` cassait le 07. Le builder est maintenant dans [`scripts/shared/`](../scripts/shared/), et `proto06_lib/pdbuild.py` n'est plus qu'une réexportation — une seule source, les deux prototypes marchent. Vérifié : patch 07 régénéré à l'identique, générateur 06 et ses quatre tests toujours OK.

**Changement — `.gitignore`.** `SONS_V3/`, `__pycache__/`, externals compilés, `.DS_Store`. Prépare le `git init` qui reste le point 0 du backlog.

**Ce qui a été écarté de l'audit, et pourquoi.** Sa suggestion d'ajouter `StartLimitBurst=5` au service systemd est **à ne pas appliquer** : elle ferait abandonner systemd après quelques échecs, laissant l'installation morte jusqu'à une intervention SSH, alors qu'un redémarrage infini est exactement ce qu'on veut en exposition. `WatchdogSec` est inapplicable tel quel — il suppose des battements de cœur `sd_notify` que Pd n'envoie pas. `LimitRTPRIO` est sans objet, `launch.sh` ne passe pas `-rt`. Et son inventaire des dossiers audio était périmé et faux : il affirmait que `SONS_FINAL/` et `SONS_PROTOTYPE/` n'étaient référencés nulle part, alors que `proto06/slice_sons_final.py`, `build_cortex_beds.py` et `pd/lib/player_folder.pd` les lisaient.

**Mesure au passage.** Vérification de la condition laissée en suspens sous [Q3](./Backlog/Q&A.md#q3) : les masters **contiennent bien** 17 plages continues de 30 s et plus, dont sept autour de 60 s et une de 91 s. La réponse B est donc réalisable. Les « 7 minutes » de Simon n'existent pas dans la matière. Et le tri manuel du 18 août appliquait déjà la règle : médiane 41,6 s pour les 27 fichiers gardés en `AMBIANCE`, 4,6 s pour les 42 déplacés en `FRAGMENTS`.

**Pas fait :** la détection d'un Pd gelé, seul vrai trou restant. Le durcissement du service en `Restart=always` + `StartLimitIntervalSec=0`. Et la règle des 30 s n'est pas encore inscrite dans la découpe.

---

## 2026-08-20 — Un seul dossier audio · découpe incrémentale, ID stables (Q21 = A)

**Prompt :** réponse A à Q21. Supprimer les autres dossiers audio et ne garder que `SONS_V3`. « Wip contient les originaux. »

**Pourquoi :** cinq dossiers audio pour 5,9 Go, dont trois morts, et deux jeux de masters concurrents. Personne ne savait plus lequel était la source. Et la découpe renumérotait tout à chaque passage, ce qui rendait impossible le travail de classification à l’oreille qui est le prochain gros chantier.

**Changement — matière.** Supprimés : `SONS/` (144 Mo), `SONS_V2/` (204 Mo), `SONS_FINAL/` (1,2 Go, masters V2), `SONS_PROTOTYPE/` (1,5 Go). 3 Go libérés. `SONS_V3/` est le seul dossier audio ; ses masters V6 sont dans `SONS_V3/WIP/`, intacts, confirmés sauvegardés ailleurs. Les 526 wav découpés n’ont pas bougé, les pools du patch sont identiques (Cortex 132, ambiance 27 sur 5 baffles).

**Changement — découpe incrémentale.** `slice_opacite_v3.py` ne vide plus `SONS_V3/` et ne renumérote plus. Un segment est apparié à son ID par (master, état, rôle, temps de début ± 0,3 s), donc il survit à un petit changement de détection de silence. Un segment nouveau prend le numéro suivant ; un numéro attribué ne sera jamais réattribué. Registre : `Matiere/registre_ids.csv`, amorcé depuis l’inventaire du 18 août par `amorcer_registre_ids.py`. Vérifié : 0 nouveau, 526 réutilisés, 0 orphelin.

**Changement — le rangement manuel gagne.** Les 42 `A0xx` déplacés à la main vers `CORTEX/FRAGMENTS` le 18 août étaient sur le point d’être remis en `AMBIANCE` par le calcul automatique. La règle est maintenant que le disque gagne sur le calcul : un déplacement décidé à l’oreille n’est jamais défait tout seul. `--reclasser` pour forcer.

**Trois bugs trouvés en passant.** `slice_opacite_v3.py` cherchait ses masters dans `SONS_V2/WIP`, disparu le 18 août : le script était **cassé** et personne ne l’avait remarqué. Pire, comme les masters sont maintenant *dans* `SONS_V3/WIP` et que le script faisait `rmtree(SONS_V3)`, corriger ce chemin sans toucher au reste aurait **supprimé les masters de Simon**. Le `rmtree` a disparu. Enfin, le rsync de déploiement Pi n’excluait pas `SONS_V3/WIP` : 2,6 Go de masters partaient sur le réseau à chaque copie.

**Conséquence assumée :** les patches Proto 06 sont muets, ils lisaient `SONS/`. `proto06/slice_sons_final.py` et `build_cortex_beds.py` ne peuvent plus tourner. Le dossier reste pour son DSP, réutilisé par le 07. Muets aussi, et sans importance : les patches `prototype_01`, `02`, `04` et les deux `_test_*`, qui lisaient `SONS_PROTOTYPE/wav/` via `pd/lib/player_folder.pd`.

**Pas fait :** la structure des colonnes du classeur ne correspond toujours pas au vocabulaire d’`Attributs.md` — une seule colonne « Attributs » fourre-tout. À trancher ([Q20](./Backlog/Q&A.md#q20)) avant de passer des heures à remplir. Toujours pas de git.

---

## 2026-08-20 — Réorganisation des docs · Zones/ · Backlog Q&A + TO DO

**Prompt :** nettoyer et réorganiser `docs/`, sans numéros dans les noms. Archiver l’historique des samples et l’ancien backlog. Lire le document de Simon sur le Cortex et Cortex-Ambiance, mettre dans un Q&A ce qui est à trancher et dans un backlog ce qui est clair. Commencer à figer le fonctionnement des zones (timbre, effets, mouvement) indépendamment des samples. Préparer le terrain pour la sélection par tags.

**Pourquoi :** les documents reçus mélangent des intentions claires, des comportements ambigus et des règles qui contredisent ce qui est déjà validé à l’oreille. Tant que les trois arrivent mélangés, chaque implémentation casse quelque chose qui marchait. Le tri se fait maintenant, avant de coder.

**Changement — arborescence.** Nouveau : [`Zones/`](./Zones/) (un fichier par zone, statut de gel par paramètre), [`Matiere/`](./Matiere/) (`Pipeline.md`, `Attributs.md`, classeur), [`Backlog/`](./Backlog/) (`Q&A.md`, `TO DO.md`), [`Sources/`](./Sources/) (documents reçus, tels quels). Archivés : inventaires de découpe V2/V3, `catalogue_samples.csv`, `source_samples.md`, backlog 14 et 18. Rien n’a été supprimé — le projet n’est pas sous git.

**Changement — tri du document de Simon.** 24 questions dans `Q&A.md`, dont 8 qu’il soulève lui-même. Contradictions dures : carte des 8 HP (6 baffles de parole + 2 ambiances chez lui, 3 paires + 5 nappes dans le patch), durée des ambiances (30 s minimum contre des atomes de 2 s), rôle du piézo (déclencher une transition contre geler le Cortex). Ambiguïtés bloquantes : « à privilégier » sans règle de repli, table C2 non symétrique, tables C9/C10 dont toutes les lignes donnent la même réponse. Bloquant découvert en relisant le code : la découpe renumérote tout, donc les ID ne sont pas stables et la classification serait perdue.

**Changement — code.** Aucun changement de son. Uniquement des chemins : `slice_opacite_v3.py` et `gen_catalogue_xlsx.py` écrivent maintenant dans `docs/Matiere/`. Liens corrigés dans les README racine, `docs/` et `scripts/`.

**Pas fait :** rien de figé, aucun FX touché. Le gel des zones demande des séances d’écoute, et la carte des HP doit être tranchée avant ([Q1](./Backlog/Q&A.md#q1)).

---

## 2026-08-18 — Catalogue Excel 3 feuilles (ID + type en vert)

**Prompt :** fichier Excel, une page par zone (Cortex, Hippo, Recon), colonnes ID / type / phrase / attributs / comportements. Préremplir ID et type en vert.

**Pourquoi :** classer les samples à l’oreille (Belgique / Congo) sans que le moteur lise encore le tableau.

**Changement :** [`catalogue_fragments.xlsx`](./catalogue_fragments.xlsx) depuis `SONS_V3/` (court = FRAGMENTS, long = LONG_MOYEN, ambiance = nappe). Regen : `python3 scripts/gen_catalogue_xlsx.py` (conserve les colonnes déjà remplies).

---

## 2026-08-18 — Pi : documenter le boot auto (sans enlever le mot de passe)

**Prompt :** documenter le lancement dès l’allumage du Raspberry ; est-ce qu’il faut enlever le mot de passe ?

**Pourquoi :** le mot de passe `simon` est pour SSH / `sudo`, pas pour Pd. systemd lance le patch sans login.

**Changement :** §3 dans [`deploy/debian/README.md`](../deploy/debian/README.md) (`install-service.sh`, reboot, status / disable). Pas de nouveau code.

---

## 2026-08-18 — Pi : Scarlett device 4/5, Pd 0.55 random

**Prompt :** lancé le script, Focusrite vue, erreurs ALSA + `random: no method for 'float'`.

**Pourquoi :** `--device 1` / défaut = HDMI du Pi (pas la Scarlett 18i20 = Pd **4** hardware / **5** plug-in). `-channels 8` ouvrait aussi l’entrée HDMI inexistante. Pd Debian **0.55** n’accepte pas un float à gauche de `[random]` (Mac 0.56 oui).

**Changement :** `launch.sh` choisit la Scarlett, `-noadc -outchannels 8`. Libs 07 : bang/`seed` vers `[random]`, pas un float. Re-`rsync` puis `bash deploy/debian/launch.sh --nogui` **sans** `--device 1`.

---

## 2026-08-18 — Pi : mode installation au lancement Debian

**Prompt :** si on lance install / launch / service, est-ce le mode installation direct ?

**Pourquoi :** le boot Pd restait en édition, AUDIO_ON off — silence en `--nogui`.

**Changement :** `launch.sh` envoie `r6_boot_expo` → INSTALL + AUTO + AUDIO_ON. Mac inchangé. Re-`rsync` le patch avant de tester sur le Pi.

---

## 2026-08-18 — Lancer Proto 07 sur Raspberry Pi / Debian

**Prompt :** dossier + script Debian pour lancer le projet sur Raspberry Pi.

**Pourquoi :** le launch Mac pointe vers Pd.app ; les listes `[text]` avaient un chemin absolu Mac.

**Changement :** `deploy/debian/` (`install.sh`, `launch.sh`, service systemd). Playlists en chemin relatif. Relancer Pd sur Mac aussi (mêmes listes).

---

## 2026-08-18 — Cortex : C0xx court + moyen absents

**Prompt :** on n’entend pas les fragments C0xx court ni moyen.

**Pourquoi :** les moyens (≥13 s) restaient dans `LONG_MOYEN`, hors pool. Les listes commençaient par les Axx déplacés. Le pulse 2,8 s coupait les longs.

**Changement :** pool = **48 C court + 42 C moyen + 42 A-frag**. C d’abord. Pulse **10 s**. Fragments un peu plus fort. Relancer Pd — SAMPLES HP1–3 doivent montrer des `C0xx`.

---

## 2026-08-18 — Cortex : LPF 1500, sweep 500–2000

**Prompt :** filtre trop fermé ; mettre 1500, dynamique, bouge de 500 à 2000.

**Pourquoi :** LP 600 écrasait trop. Le LFO interne 06 (±800 Hz) ne tombait pas dans 500–2000.

**Changement :** centre **1500 Hz**. Chaque couche L1–L6 parcourt **500–2000 Hz** (vitesses un peu différentes), seulement en Cortex. Relancer Pd.

---

## 2026-08-18 — Cortex : AMBIANCE exclusive, LP 600, nappes +2 dB

**Prompt :** nappes = seulement `SONS_V3/CORTEX/AMBIANCE` ; le reste déplacé dans FRAGMENTS doit jouer ; nappes +2 dB ; plus de filtre LP 600 et de HPF/phi.

**Pourquoi :** des ambiances déplacées pouvaient encore se mélanger au pool ; LPF trop ouvert (~1,5 kHz).

**Changement :** nappes = **27** fichiers AMBIANCE seulement (5 baffles). Fragments = **90** FRAGMENTS. Nappes **+2 dB**. Fragments LPF **600 Hz**, HPF ~450–630, flfo fort. Relancer Pd.

---

## 2026-08-18 — Cortex : plus de send, 5 nappes, moins de reverb

**Prompt :** enlever les baffles send delay/reverb ; 5 baffles d’ambiance en même temps, chacun un autre ; moins de delay et de reverb.

**Pourquoi :** HP6–8 n’étaient que l’écho des paires. Une seule nappe. Wet trop haut.

**Changement :** plus de send. **HP1–3** = 3 paires de fragments. **HP4–8** = 5 nappes différentes (69 fichiers, pools disjoints), sèches. Fragments wet **~0,10**, fb **~6 %**. Relancer Pd.

---

## 2026-08-18 — Cortex : 4 paires + nappe HP5 + send HP6-8

**Prompt :** au démarrage seules ~3 couches ; 1 baffle = 2 samples, 4 baffles, puis 1 baffle ambiance, 3 baffles delay/reverb ; garder LFO / déplacement harmonieux ou aléatoire ; petits fragments ; enchaînement pas consistant.

**Pourquoi :** densité Cortex tirait 6–8 mais le moteur partait à n=1 ; 1 couche / HP ; eof des fragments ne relançait pas assez.

**Changement :** 8 couches dès le loadbang, pool **FRAGMENTS** seulement. HP1–4 = 4 paires (rotation +1 ou saut, LFO lent). HP5 = nappe. HP6–8 = send delay (HP8 un peu de fb). Pulse ~2,8 s pour enchaîner. Hippo/Recon inchangés (spatial 1:1). Relancer Pd.

---

## 2026-08-18 — Cortex : plus de reverb + filtre

**Prompt :** remettre plus de reverb et de filtre dans le Cortex.

**Pourquoi :** après le delay discret, trop sec / trop ouvert.

**Changement :** fragments wet **~0,28–0,40**, fb **~16–24 %**, LPF **~1,2–2 kHz**, flfo plus fort. Nappe toujours sèche. Regen. Relancer Pd (ou FORCE Cortex).

---

## 2026-08-18 — start sans open (listes [text])

**Prompt :** encore `readsf~ start requested with no prior open`.

**Pourquoi :** `[text]` ne coupe pas sur les retours à la ligne sans `read -c` / `;`. Le `start` partait même si `open` n’avait rien reçu. Lancement depuis `scripts/` aussi.

**Changement :** `read -c` chemin absolu ; `start` seulement après `open` ; `cd` racine du projet dans le launch.

---

## 2026-08-18 — `$1` / `open` dans le lecteur

**Prompt :** erreurs Pd `$1/$2 argument number out of range` et `readsf~ start` sans `open`.

**Pourquoi :** dans une abstraction, `open $1` = l’argument loop (0/1), pas le nom du wav.

**Changement :** `list split` + `list prepend open` (vanilla). Relancer Pd.

---

## 2026-08-18 — Pd ne s’ouvrait plus (lecteur trop gros)

**Prompt :** `./launch_prototype_07_8hp.sh` n’ouvre pas.

**Pourquoi :** 526 wav × 10 copies du lecteur = ~19 000 objets. Pd chargeait les libs puis restait bloqué (Ctrl+C).

**Changement :** `player_state_07` lit des listes `[text]` (`pd/lib/playlists07/`). Même tirage, patch léger. Relancer le script.

---

## 2026-08-18 — SONS_V3 (sélection V6) dans le 07

**Prompt :** 4 nouveaux masters = sélection complète ; créer `SONS_V3` avec sous-dossiers hippo etc. ; découpe silences ; brancher proto 07 ; dans chaque strate : fragment, ambiance, long/moyen.

**Pourquoi :** nouvelle matière Ableton V6. `SONS_V2` reste l’ancienne sélection.

**Changement :** `scripts/slice_opacite_v3.py` → **526** wav dans `SONS_V3/<ETAT>/{FRAGMENTS,AMBIANCE,LONG_MOYEN}`. Lecteur 07 lit V3 (L9 Hippo replie sur nappe Cortex : Hippo/Recon AMBIANCE vides). `SONS/` et `SONS_V2/` intacts. Regen. Relancer Pd.

---

## 2026-08-18 — Source samples + catalogue tags

**Prompt :** le guide Ableton Simon n’avait pas été mis en backlog ; écarts (surtout durées d’états) ; les 4 pistes = ce qui arrive de Simon, puis découpe en petits wav classés ; clarifier le pipeline samples dans docs ; dossiers **et** tableau CSV d’attributs (ex. ambiance rythmique → Hippo, pad+melody → Cortex).

**Pourquoi :** le PDF décrit le métier Ableton, pas le patch. Les tags servent à répertorier et **choisir** les samples après écoute, pas à recopier les durées Simon.

**Changement (docs seulement) :** [`source_samples.md`](./source_samples.md) · [`catalogue_samples.csv`](./catalogue_samples.csv) (237 lignes, tags vides) · backlog [`backlog/18_catalogue_tags.md`](./backlog/18_catalogue_tags.md). Moteur inchangé.

---

## 2026-08-18 — Doc : état / log / envies

**Prompt :** arrêter de faire comme si on piochait le backlog ; documenter le pourquoi des changements d’oreille ; l’intention du 16 août n’est plus vérité absolue (surtout les FX).

**Pourquoi :** travail à la hâte (prompt → modif). Les Q&A / UC / vagues se contredisaient avec le patch.

**Changement :** `etatactuel.md` = maintenant. Ce fichier = journal. Backlog = envies. Q&A 15 + journal 17 + synthèse 14 → intention historique (`archive/` / `backlog/14`).

---

## 2026-08-17 — Cortex : tout `ECART/` dans le pool

**Prompt :** ce qui est dans `SONS_V2/CORTEX/ECART` n’est pas un écart ; tout utiliser.

**Pourquoi :** le dossier était seulement « hors 13–30 s » à la découpe, pas un rebut d’écoute.

**Changement :** `sons_audit07` — pool Cortex = FRAGMENTS + ECART (**47** fichiers). Dossiers inchangés. Regen lecteur.

---

## 2026-08-17 — Cortex : distorsion + delay discret

**Prompt :** de la distorsion ; un delay pas fort, feedback **5–7 %**.

**Pourquoi :** après le retour flou 06, trop d’écho / pas assez de grit.

**Changement :** sat **~0,52–0,65** ; delay wet **~0,11–0,16** ; **fb 0,05–0,07**. Filtre flou inchangé. Regen.

---

## 2026-08-17 — Cortex : son 06 + nappe 1 HP

**Prompt :** ça ne sonne pas comme je veux. Refaire comme **avant**, avec **1 baffle dédié ambiance**. Il manque le flou, un peu de reverb, le jeu de filtre.

**Pourquoi :** le LPF ~500 Hz + sat 0,72 (Q&A 10 / guide Simon) écrasait le flou 06.

**Changement :** HPF 400–600, LPF **~2–3 kHz + flfo**, sat ~0,5, ovl 50–80 ms, densité **6–8**. Nappe **dry**, 1 HP. Abandon du LPF dur sur les fragments.

---

## 2026-08-17 — Nappe Cortex inaudible ?

**Prompt :** je n’entends pas la nappe ; y a-t-il un filtre ?

**Pourquoi :** diagnostic.

**Constat (pas de code) :** en Cortex, pas de LPF fort sur L9 (18 kHz). Un seul baffle tiré au hasard ; fragments peuvent masquer. Filtre 5 kHz = Hippo seulement.

---

## 2026-08-17 — Scripts rangés

**Prompt :** nettoyer `scripts/`, sous-dossiers, archiver avant proto 6.

**Changement :** `scripts/proto07/` · `proto06/` · `archive/` + raccourcis à `scripts/`.

---

## 2026-08-17 — Docs 01–09 archivés

**Prompt :** archiver tout ce qui est avant le 10.

**Changement :** `docs/archive/` (puis 10–13 y sont aussi).

---

## 2026-08-16 — Proto 07 moteur + SONS_V2

Intention du jour (Q&A 01–20, vagues 0–8) : cycle 40/50/120, 06 figé, 8 HP, nappe 1 HP, matière V2.  
Le détail FX de ce jour (LPF 400–600 dur, XOR next-room, densité 3–6) a **été écrasé** les 17–18 août — voir les strophes ci-dessus, pas le Q&A 15.
