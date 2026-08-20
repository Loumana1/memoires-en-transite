# scripts/proto06/ — figé, et désormais hors service

Générateurs 4 / 6 / 8 HP, `proto06_lib/`, découpe `SONS_FINAL` → `SONS/`.

**Depuis le 20 août 2026, ces scripts ne peuvent plus tourner** : `SONS/` et `SONS_FINAL/` ont été supprimés, `SONS_V3/` est le seul dossier audio. Concrètement, `slice_sons_final.py` et `build_cortex_beds.py` s'arrêtent faute de source, et les patches 06 générés sont muets — les playlists pointent sur des fichiers qui n'existent plus.

Le code reste ici parce que le **DSP** du 06 est encore utilisé par le 07 : `fx_router_06`, `spatial_router_06`, `decode_8hp_06`. C'est la seule raison.

Ne pas changer le **comportement** (`presets06.py`). Réutiliser seulement le DSP depuis le 07.

Pour faire sonner le 06 à nouveau il faudrait le remapper sur `SONS_V3/`, dont l'arborescence est différente (`FRAGMENTS` / `AMBIANCE` / `LONG_MOYEN` au lieu de `COURT` / `MOYEN` / `LONG` par état). Ce n'est pas prévu : le 07 est le prototype courant.

Raccourcis : `scripts/launch_prototype_06_8hp.sh` · `python3 scripts/gen_prototype_06_8hp.py`
