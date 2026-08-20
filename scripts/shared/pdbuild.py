"""Builder minimal de fichiers .pd (Pure Data vanilla). Partagé 06 / 07.

Vivait dans `proto06_lib/` jusqu'au 20 août 2026. Déplacé ici parce que le
Proto 07 en dépend alors que le Proto 06 est figé et hors service : le
générateur du prototype courant ne doit pas casser si on touche au 06.
`proto06_lib/pdbuild.py` n'est plus qu'une réexportation.

Chaque objet ajouté avec add() est indexé par nom pour les connexions.
Les commentaires (#X text) comptent comme objets dans l'index Pd — text()
incrémente donc aussi le compteur.
"""


class P:
    def __init__(self, w=800, h=600, x=0, y=0, font=10):
        self.w, self.h, self.x, self.y, self.font = w, h, x, y, font
        self.items = []   # str (une ligne) ou list[str] (subpatch inline)
        self.idx = {}
        self.n = 0
        self.conns = []

    def add(self, name, line):
        if name in self.idx:
            raise SystemExit(f"objet dupliqué: {name}")
        self.idx[name] = self.n
        self.n += 1
        self.items.append(line)

    def obj(self, name, x, y, body):
        self.add(name, f"#X obj {x} {y} {body};")

    def msg(self, name, x, y, body):
        self.add(name, f"#X msg {x} {y} {body};")

    def text(self, x, y, body):
        self.n += 1
        self.items.append(f"#X text {x} {y} {body};")

    def sub(self, name, x, y, subname, child):
        """Insère un subpatch (canvas enfant complet, fermé) comme objet."""
        lines = [f"#N canvas {child.x} {child.y} {child.w} {child.h} {subname} 0;"]
        lines += child.flat_lines()
        lines.append(f"#X restore {x} {y} pd {subname};")
        self.idx[name] = self.n
        self.n += 1
        self.items.append(lines)

    def con(self, src, outlet, dst, inlet):
        self.conns.append((src, outlet, dst, inlet))

    def flat_lines(self):
        out = []
        for it in self.items:
            if isinstance(it, list):
                out.extend(it)
            else:
                out.append(it)
        for s, o, d, i in self.conns:
            out.append(f"#X connect {self.idx[s]} {o} {self.idx[d]} {i};")
        return out

    def write(self, path, declare=None):
        lines = [f"#N canvas {self.x} {self.y} {self.w} {self.h} {self.font};"]
        if declare:
            lines.append(declare)
        lines += self.flat_lines()
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
