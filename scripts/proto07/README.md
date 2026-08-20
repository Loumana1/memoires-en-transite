# scripts/proto07/ — courant

| Fichier | Rôle |
|---------|------|
| `launch_prototype_07_8hp.sh` | Lancer Pd |
| `gen_prototype_07_8hp.py` | Régénérer patch + `pd/lib/*_07*` |
| `slice_opacite_v3.py` | Masters `SONS_V3/WIP/` → `SONS_V3/<ETAT>/` · **incrémental, ID stables** · ne vide rien, ne touche jamais `WIP/` · inventaire et registre dans `docs/Matiere/` |
| `amorcer_registre_ids.py` | Migration unique du 20 août : reconstruit `registre_ids.csv` depuis les 526 wav existants |
| `gen_catalogue_xlsx.py` | `docs/Matiere/catalogue_fragments.xlsx` depuis `SONS_V3/` (conserve les colonnes remplies) |
| `proto07_lib/` | presets, générateurs, audit |

La découpe V2 est dans [`../archive/`](../archive/).

Raccourcis à `scripts/` : mêmes noms. DSP 06 partagé, pas recopié.
