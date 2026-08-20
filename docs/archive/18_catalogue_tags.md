# Backlog — catalogue samples + tags

**Pas un contrat.** L’IA n’y touche **que** si Loumana le demande.  
Source matière : [`../source_samples.md`](../source_samples.md) · table : [`../catalogue_samples.csv`](../catalogue_samples.csv).

Issu du guide Ableton Simon 15 août (jamais transcrit ici) **corrigé** par Loumana le 18 août : les 4 pistes = masters reçus ; le travail réel = petits wav + dossiers + tableau d’attributs. Les durées d’états du PDF ne s’imposent pas.

---

## Ouvert

### A — Remplir le catalogue (oreille, pas de code)

Loumana écoute des cycles, puis renseigne `famille` / `tags` / `usage_prefere` / `notes`.

Exemple déjà dit : ambiances **rythmiques** → `usage_prefere=hippo` ; ambiances **pad, melody** → cortex / nappe.

Ça n’a **aucun** effet moteur tant que C n’est pas demandé.

### B — Découpe incrémentale

Souhait : les samples **s’ajoutent**.  
Aujourd’hui : `slice_opacite_v3.py` **vide** `SONS_V3/` (pas `SONS_V2/`).

À faire quand demandé :

- ne plus `rmtree` le pool entier ;
- n’écrire que les nouveaux stems (ou un master nommé) ;
- fusionner le journal 16 **et** le catalogue 18 sur la clé `fichier` : garder les tags déjà remplis, ajouter des lignes vides pour les nouveaux wav.

### C — Le moteur lit les attributs

Aujourd’hui : tirage dans des **dossiers** (`etatactuel.md`). `s6_tag_hook` est vide.

Quand demandé, exemples de règles :

- nappe Cortex : fichiers avec tags `pad` et/ou `melody` (plutôt que « tout `AMBIANCE/` ») ;
- Hippo : inclure les ambiances `rythmique` même si le wav est encore dans `CORTEX/AMBIANCE/` ;
- `usage_prefere` prime sur le dossier si renseigné.

Ne pas coder de graphe A→B (relations Simon) avant d’avoir un catalogue assez rempli.

---

## Hors V1 (reste dans le PDF / envies)

- Table pondérée mot / timbre / souffle / contraste (Hippo A déclenche B).
- Segmentation live des longs WAV **dans** Pd.
- Fiche éthique complète par région (contexte, cadre, marque de pouvoir) — peut aller dans `notes` au fil de l’eau.
