"""Layout physique des 8 haut-parleurs — Proto 08.

Jusqu'au 22 août 2026 le numéro de haut-parleur servait à trois choses à la
fois : index logique manipulé par le moteur, sortie de la carte son, et
position dans l'espace. « HP3 » voulait dire « la troisième sortie », « le
troisième baffle » et « 90° » sans que rien ne le déclare. Ce module sépare
les trois, ce qui permet de recâbler ou de déplacer un baffle sans toucher au
reste du code.

Convention d'azimut
-------------------
0° est en face de l'auditeur placé au centre, et les angles croissent vers sa
DROITE (sens horaire vu de dessus) : 90° à droite, 180° derrière, 270° à
gauche. C'est la convention déjà employée par le patch (voir le commentaire de
`prototype_01_4hp_ambi.pd`). Elle est l'inverse du standard ambisonique, où
+Y pointe à gauche, mais cela n'a aucune conséquence tant qu'`encode_2d` et le
décodeur partagent la même formule — c'est le cas, les deux utilisent
[1, cos(az), sin(az)]. Ce qui décide du sens réel d'une rotation dans la
salle, c'est le champ `dac` : c'est lui qui relie un azimut à une boîte.

Ce que le décodage utilise réellement
-------------------------------------
La matrice de décodage ordre 1 / 2D ne dépend QUE des azimuts. Ni la distance
ni le rayon du cercle n'y entrent. La distance sert à deux choses distinctes :

  - `trim_db` — l'égalisation de niveau entre baffles. C'est le réglage qui
    compte le plus en pratique, et il se fait à l'oreille en salle, pas par
    calcul : la sensibilité des enceintes et l'acoustique locale pèsent autant
    que la distance.
  - le retard de compensation, calculé par `delays_ms()`. Il n'a de sens que
    parce qu'un centre d'écoute est défini. Il vaut 0 partout tant que les
    distances sont égales, et aucun objet de retard n'est alors généré.
"""
import math
from dataclasses import dataclass

# Vitesse du son à 20 °C, pour convertir un écart de distance en retard.
SPEED_OF_SOUND = 343.0
# En deçà de ce retard, la compensation n'est pas générée : 0,5 ms correspond
# à 17 cm, bien en dessous de la précision de pose des baffles.
DELAY_EPSILON_MS = 0.5


@dataclass(frozen=True)
class Speaker:
    hp: int          # index logique manipulé par le moteur (1..8)
    dac: int         # canal physique de la carte son (argument de dac~)
    az: float        # azimut mesuré, en degrés, convention ci-dessus
    dist_m: float    # distance au centre d'écoute, en mètres
    trim_db: float   # correction de niveau, à régler en salle
    label: str


# Octogone régulier, câblage direct, distances égales. C'est la géométrie que
# tout le code supposait implicitement ; elle est désormais déclarée, donc
# modifiable. Mesurer les azimuts réels et corriger ici suffit à régénérer une
# matrice de décodage juste.
SPEAKERS = [
    Speaker(1, 1,   0.0, 3.0, 0.0, "avant"),
    Speaker(2, 2,  45.0, 3.0, 0.0, "avant droit"),
    Speaker(3, 3,  90.0, 3.0, 0.0, "droite"),
    Speaker(4, 4, 135.0, 3.0, 0.0, "arriere droit"),
    Speaker(5, 5, 180.0, 3.0, 0.0, "arriere"),
    Speaker(6, 6, 225.0, 3.0, 0.0, "arriere gauche"),
    Speaker(7, 7, 270.0, 3.0, -3.0, "gauche"),    # trim provisoire −3 dB (23 août) — live : ; s6_trim7 -6
    Speaker(8, 8, 315.0, 3.0, 0.0, "avant gauche"),
]

NHP = len(SPEAKERS)
_BY_HP = {s.hp: s for s in SPEAKERS}


def fmt(v):
    """Nombre au format Pd : pas de `.0` parasite dans les arguments."""
    return f"{v:g}"


def by_hp(hp):
    return _BY_HP[hp]


def az_of(hp):
    return _BY_HP[hp].az


def dac_of(hp):
    return _BY_HP[hp].dac


def hp_order():
    """Les HP dans l'ordre de leur index logique."""
    return [s.hp for s in sorted(SPEAKERS, key=lambda s: s.hp)]


def azimuths():
    """Azimuts dans l'ordre des HP — l'ordre des sorties du décodeur."""
    return [_BY_HP[hp].az for hp in hp_order()]


def dac_args():
    """Arguments de `dac~` : la n-ième entrée part vers le HP n."""
    return " ".join(str(dac_of(hp)) for hp in hp_order())


def trim_linear(hp):
    return 10.0 ** (_BY_HP[hp].trim_db / 20.0)


def delays_ms():
    """Retard par HP pour aligner les arrivées au centre d'écoute.

    Le baffle le plus éloigné sert de référence et reçoit 0 ; les autres sont
    retardés de l'écart. Tout est à 0 si les distances sont égales.
    """
    far = max(s.dist_m for s in SPEAKERS)
    return {s.hp: (far - s.dist_m) / SPEED_OF_SOUND * 1000.0 for s in SPEAKERS}


def needs_delay_compensation():
    return max(delays_ms().values()) >= DELAY_EPSILON_MS


def ring():
    """Les HP dans l'ordre où on les rencontre en tournant dans la salle.

    C'est cet ordre — et non les angles exacts — qui décide si un déplacement
    s'entend comme un déplacement. Il est calculé depuis les azimuts, donc il
    reste juste même si le câblage change.
    """
    return [s.hp for s in sorted(SPEAKERS, key=lambda s: s.az % 360.0)]


def neighbours(hp):
    """(précédent, suivant) autour de l'anneau, au sens des azimuts."""
    r = ring()
    i = r.index(hp)
    return r[(i - 1) % len(r)], r[(i + 1) % len(r)]


def angular_gap(hp_a, hp_b):
    """Écart angulaire absolu entre deux baffles, ramené à 0–180°."""
    d = abs(az_of(hp_a) - az_of(hp_b)) % 360.0
    return min(d, 360.0 - d)


def nearest_hp(az):
    """Le baffle le plus proche d'un azimut donné."""
    return min(SPEAKERS, key=lambda s: angular_distance(s.az, az)).hp


def angular_distance(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def anchors(layer_hp):
    """[(hp, az)] par couche, à partir d'une liste d'index HP.

    Remplace la table d'ancrages écrite à la main : l'azimut n'est plus
    recopié à côté du numéro de baffle, il en découle.
    """
    return [(hp, az_of(hp)) for hp in layer_hp]


def decode_rows():
    """Lignes de la matrice de décodage ordre 1 / 2D : [1, cos(az), sin(az)]."""
    rows = []
    for az in azimuths():
        r = math.radians(az)
        rows.append((1.0, math.cos(r), math.sin(r)))
    return rows


def decode_matrix_msg():
    """Message `matrix` prêt pour `mtx_*~ {NHP} 3`."""
    body = " ".join(
        f"1 {x:.4f} {y:.4f}" for _, x, y in decode_rows()
    )
    return f"matrix {NHP} 3 {body}"


def is_regular():
    """Vrai si les baffles forment un polygone régulier en angle."""
    az = sorted(s.az % 360.0 for s in SPEAKERS)
    step = 360.0 / NHP
    return all(abs(a - i * step) < 1e-6 for i, a in enumerate(az))


def describe():
    """Résumé lisible du layout, pour le journal et les vérifications."""
    lines = [
        f"{NHP} HP · {'octogone regulier' if is_regular() else 'geometrie irreguliere'}"
        f" · compensation de retard "
        f"{'active' if needs_delay_compensation() else 'inutile (distances egales)'}"
    ]
    dl = delays_ms()
    for hp in hp_order():
        s = _BY_HP[hp]
        lines.append(
            f"  HP{s.hp} -> dac {s.dac} · {fmt(s.az):>4}° · {fmt(s.dist_m)} m"
            f" · trim {s.trim_db:+.1f} dB · retard {dl[hp]:.1f} ms · {s.label}"
        )
    return "\n".join(lines)


def validate():
    """Erreurs de saisie qui passeraient sinon inaperçues jusqu'en salle."""
    hps = [s.hp for s in SPEAKERS]
    dacs = [s.dac for s in SPEAKERS]
    if sorted(hps) != list(range(1, NHP + 1)):
        raise SystemExit(f"layout08: index HP non contigus 1..{NHP} : {sorted(hps)}")
    if len(set(dacs)) != NHP:
        raise SystemExit(f"layout08: deux baffles sur la meme sortie : {sorted(dacs)}")
    for s in SPEAKERS:
        if s.dist_m <= 0:
            raise SystemExit(f"layout08: HP{s.hp} a une distance nulle ou negative")
    for a in SPEAKERS:
        for b in SPEAKERS:
            if a.hp < b.hp and angular_distance(a.az, b.az) < 1e-6:
                raise SystemExit(
                    f"layout08: HP{a.hp} et HP{b.hp} ont le meme azimut {fmt(a.az)}°"
                )


validate()


if __name__ == "__main__":
    print(describe())
    print()
    print(decode_matrix_msg())
