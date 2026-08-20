# scripts/

Travail **courant : Proto 07**. Proto 06 figé. 01–05 archivés.

| Dossier | Contenu |
|---------|---------|
| [`proto07/`](./proto07/) | Moteur 07 + `slice_opacite_v3.py` + `gen_catalogue_xlsx.py` |
| [`proto06/`](./proto06/) | Moteur 06 — **hors service** depuis le 20 août (`SONS/` supprimé). Gardé pour son DSP |
| [`shared/`](./shared/) | Code commun 06 / 07 : `pdbuild.py` (builder de fichiers `.pd`) |
| [`archive/`](./archive/) | Proto 01–05, découpe SONS_PROTOTYPE |
| `test_patch_console.sh` | Test Pd `-nogui` (partagé) |
| `verifier_sons.py` | **Contrôle avant expo** : wav jouables + playlists cohérentes |
| `normaliser_niveaux.py` | Mesure la sonie et calcule un gain par fragment, **sans toucher aux wav** |

À la racine de `scripts/` : **raccourcis** (mêmes commandes qu’avant) vers proto07 / proto06.

```bash
bash scripts/launch_prototype_07_8hp.sh
python3 scripts/gen_prototype_07_8hp.py
python3 scripts/slice_opacite_v3.py
python3 scripts/gen_catalogue_xlsx.py
python3 scripts/verifier_sons.py
```

Équivalent canonique : `scripts/proto07/…`.

## Avant chaque exposition

```bash
python3 scripts/verifier_sons.py && bash scripts/test_patch_console.sh
```

`verifier_sons.py` prend une seconde et attrape le seul défaut qui ne se voit dans aucun log : un wav illisible, vide, muet ou troué, et une playlist qui cite un fichier disparu. Code retour 1 s'il y a une erreur, donc chaînable. Les avertissements de niveau (`très bas`) ne bloquent pas.

`slice_opacite_v3.py` est **incrémental** : il ajoute sans renumeroter, ne vide jamais `SONS_V3/`, et ne touche jamais les masters de `SONS_V3/WIP/`. Il écrit l'inventaire et le registre des ID dans `docs/Matiere/`. `--dry-run` pour voir sans écrire.
`gen_catalogue_xlsx.py` écrit `docs/Matiere/catalogue_fragments.xlsx` en conservant les colonnes déjà remplies.

## Niveaux

```bash
python3 scripts/normaliser_niveaux.py --rapport   # mesurer sans écrire
python3 scripts/normaliser_niveaux.py             # écrire niveau_db et gain_db au registre
```

Mesure la **sonie de parole active** et non le pic — le pic ne dit rien d'utile sur de la parole. N'écrit que deux colonnes du registre, `niveau_db` et `gain_db` : **aucun wav n'est modifié**, la mesure est toujours refaite sur le fichier d'origine, donc relancer le script ne peut pas cumuler deux normalisations.

L'enjeu n'est pas le volume. La saturation étant non linéaire, un fragment 30 dB plus bas ne traverse pas le même timbre : sans normalisation le son de la zone dépend du fichier tiré. Le gain n'est **pas encore appliqué à l'audio** — voir l'en-tête du script pour le point d'injection dans le lecteur.

IA : [`docs/README.md`](../docs/README.md) · état : [`docs/etatactuel.md`](../docs/etatactuel.md) · zones : [`docs/Zones/`](../docs/Zones/) · log : [`docs/log.md`](../docs/log.md).
