# Proto 07 sur Debian / Raspberry Pi

Même patch que sur le Mac : `pd/prototype_07_fsm_8hp.pd`.  
Ces scripts lancent **Pure Data du système** (pas l’app macOS).

SSH : `simon@installation1.local` (minuscules — `Simon` est refusé).

## 1. Copier le projet (depuis le Mac)

Dans un Terminal **sur le Mac** (pas sur le Pi) :

```bash
ssh simon@installation1.local
```

(sortir avec `exit`, puis copier :)

```bash
rsync -avz --progress \
  --exclude '.git' \
  --exclude '*.pd_darwin' \
  --exclude '*.pd_darwin.dylib' \
  --exclude 'pd/externals/pd-iem' \
  --exclude 'pd/externals/pd-iemmatrix-master' \
  --exclude 'SONS_V3/WIP/' \
  /Users/loumana/Documents/Coding/memoires-en-transit/ \
  simon@installation1.local:~/memoires-en-transit/
```

`SONS_V3/WIP/` contient les **masters** (2,6 Go) : le Pi n'en a aucun besoin, il ne lit que les wav découpés. Ne pas l'exclure ferait passer 2,6 Go sur le réseau à chaque déploiement.

## 2. Une fois sur le Pi — l’ordre

Les trois scripts ne se lancent **pas ensemble** à chaque fois.

| Script | Quand | Quoi |
|--------|--------|------|
| `install.sh` | **une fois** (ou après un `rsync` des sources iem) | Pd + compile les libs |
| `launch.sh` | pour **tester maintenant** | démarre Proto 07 |
| `install-service.sh` | **quand le son est bon** | Pd au boot, tout seul |

`launch.sh` (sauf `--noaudio`) allume **AUDIO_ON**, **INSTALL_MODE** et **FSM_AUTO** (mode présentation). Pas besoin de cliquer.

Ne pas lancer `launch.sh` **et** le service en même temps (deux Pd).

```bash
cd ~/memoires-en-transit
bash deploy/debian/install.sh          # déjà fait chez toi
bash deploy/debian/launch.sh --nogui   # test
```

Carte son USB 8 sorties (Focusrite Scarlett) :

```bash
bash deploy/debian/launch.sh --list
bash deploy/debian/launch.sh --nogui
```

Sans `--device`, le script prend la Scarlett (souvent **5** = plug-in).  
**Ne pas** passer `--device 1` : c’est le HDMI du Pi, pas la Focusrite.  
Si ALSA refuse encore : `--device 4` (hardware) ou `--channels 20` (18i20).

## 3. Démarrage auto à l’allumage du Pi

**Ne pas enlever le mot de passe** (`simon`). Il sert au SSH depuis le Mac et à `sudo`.  
Au boot, systemd lance Pd **sans que personne se connecte**.

Quand le son est bon au test `launch.sh`, arrêter ce Pd (Ctrl+C), puis **une fois** :

```bash
cd ~/memoires-en-transit
sudo bash deploy/debian/install-service.sh
sudo systemctl start memoires-en-transit
sudo reboot
```

`sudo` demande `simon` une fois (normal). Après reboot : Pd part tout seul, mode installation, FSM AUTO, audio.

Ne pas relancer `launch.sh` en même temps (deux Pd).

| | |
|--|--|
| Ça tourne ? | `systemctl status memoires-en-transit` |
| Logs | `journalctl -u memoires-en-transit -f` |
| Stop maintenant | `sudo systemctl stop memoires-en-transit` |
| Plus de démarrage auto | `sudo systemctl disable --now memoires-en-transit` |

## Dépannage

| | |
|--|--|
| `Externals iem pas compilés` | `bash deploy/debian/install.sh` |
| Pas de son | `--list` : Scarlett = 4/5, pas 0/1 (HDMI) |
| `ALSA input ... No such file` | normal si HDMI ; le lanceur ouvre `--noadc` |
| `ALSA ... 524` | mauvais device, ou 8 ch sur le hardware ; `--device 5` |
| `random: no method for 'float'` | Pd Debian 0.55 (Mac 0.56) — corrigé dans les libs 07 |
| `priority scheduling failed` | pas grave (groupe `audio`) |
| Groupes | `groups` doit contenir `audio` |
| Logs service | `journalctl -u memoires-en-transit -f` |
