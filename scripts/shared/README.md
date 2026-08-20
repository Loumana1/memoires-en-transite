# scripts/shared/ — code commun aux prototypes

Rien de spécifique à une version ici. Un fichier n'entre dans ce dossier que s'il est utilisé par **au moins deux** prototypes.

| Fichier | Rôle |
|---------|------|
| `pdbuild.py` | Builder minimal de fichiers `.pd` : objets indexés par nom, connexions, subpatches |

## Pourquoi ce dossier existe

`pdbuild.py` vivait dans `proto06/proto06_lib/`, et les générateurs du Proto 07 allaient le chercher là avec un `sys.path.insert` vers `scripts/proto06`. Le prototype courant dépendait donc d'un sous-arbre documenté comme figé — et devenu hors service le 20 août. N'importe qui supprimant `proto06/` cassait le générateur du 07 sans le savoir.

`proto06_lib/pdbuild.py` existe toujours, mais ne contient plus qu'une réexportation, pour que les générateurs et les tests du 06 continuent de fonctionner sans dupliquer le code.

**Toute modification du builder se fait ici.** Elle affecte les deux prototypes : vérifier les deux après coup.

```bash
python3 scripts/gen_prototype_07_8hp.py
for t in scripts/proto06/_test_gen_*.py; do python3 "$t" >/dev/null && echo "OK $t"; done
```
