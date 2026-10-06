"""Mezclas de las variantes 2 (horizontal [●]●●) y 5 (con nombre) del semáforo 2D."""
import os, json
from build_logo import OUT, text_path, svg as wrap
from build_semaforo3 import brackets, dot, rec, RED, AMB, GRN, BR, BG

M = os.path.join(OUT, "semaforo-mix"); os.makedirs(M, exist_ok=True)
EXB, BOLD = "InterDisplay-ExtraBold.otf", "InterDisplay-Bold.otf"
DARK = "#12121f"


def icon(x, y, s):
    """Ícono de la variante 2 (cuadrado redondeado con [●] ● ●) a escala s, esquina sup-izq en (x, y)."""
    return (f'<g transform="translate({x} {y}) scale({s})"><rect width="200" height="200" rx="46" fill="{BG}"/>'
            + brackets(12, 66, 80, 134) + rec(46, 100, 21) + dot(108, 100, 21, AMB) + dot(160, 100, 21, GRN) + '</g>')


out = {}
# 1 · Ícono (2) + nombre (5): el lockup más directo
d, w = text_path("ProduAVX", EXB, 76, 148, 94, -1)
out[1] = ("Ícono + nombre", "El ícono cuadrado de la 2 junto al nombre de la 5: versión principal horizontal.",
          wrap(int(w) + 12, 140, icon(8, 10, .6) + f'<path d="{d}" fill="{BR}"/>', "", "ProduAVX"), "dark")
# 2 · Cápsula: los tres círculos dentro de una pastilla plana, con el nombre
d, w = text_path("ProduAVX", EXB, 76, 204, 94, -1)
cap = (f'<rect x="6" y="28" width="178" height="84" rx="42" fill="#14141f"/>' + brackets(18, 46, 74, 94, arm=10, sw=5)
       + rec(46, 70, 16) + dot(98, 70, 16, AMB) + dot(144, 70, 16, GRN))
out[2] = ("Cápsula", "Los tres círculos en una pastilla plana (semáforo horizontal) + nombre.",
          wrap(int(w) + 12, 140, cap + f'<path d="{d}" fill="{BR}"/>', "", "ProduAVX"), "dark")
# 3 · El punto REC con corchetes ES la "o" de Produ; ámbar y verde cierran el nombre como puntos suspensivos
d1, x1 = text_path("Pr", EXB, 80, 8, 98, -1)
cx = x1 + 34
d2, x2 = text_path("duAVX", EXB, 80, cx + 38, 98, -1)
logo3 = (f'<path d="{d1}" fill="{BR}"/>' + brackets(cx - 30, 52, cx + 30, 106, arm=11, sw=5.5) + rec(cx, 79, 19)
         + f'<path d="{d2}" fill="{BR}"/>' + dot(x2 + 22, 90, 9, AMB) + dot(x2 + 46, 90, 9, GRN))
out[3] = ("La 'o' es REC", "El punto rojo con corchetes sustituye la 'o' de Produ; ámbar y verde cierran el nombre.",
          wrap(int(x2) + 62, 140, logo3, "", "ProduAVX"), "dark")
# 4 · Apilado: ícono arriba y nombre debajo (portadas, tarjetas, avatar ancho)
d, w = text_path("ProduAVX", EXB, 58, 0, 0, -1)
dt, wt = text_path("AUDIO · VIDEO · POST", BOLD, 15, 0, 0, 5)
W = int(w) + 40
d, _ = text_path("ProduAVX", EXB, 58, (W - w) / 2, 218, -1)
dt, _ = text_path("AUDIO · VIDEO · POST", BOLD, 15, (W - wt) / 2, 246, 5)
out[4] = ("Apilado", "Ícono arriba, nombre y lema debajo, centrado: portadas, tarjetas y créditos.",
          wrap(W, 262, icon((W - 150) / 2, 6, .75) + f'<path d="{d}" fill="{BR}"/><path d="{dt}" fill="#9393b0"/>', "", "ProduAVX"), "dark")
# 5 · Para fondo claro: ícono oscuro + nombre en tinta
d, w = text_path("ProduAVX", EXB, 76, 148, 94, -1)
out[5] = ("Fondo claro", "La mezcla 1 con el nombre en tinta oscura, para fondos blancos o crema.",
          wrap(int(w) + 12, 140, icon(8, 10, .6) + f'<path d="{d}" fill="{DARK}"/>', "", "ProduAVX"), "light")

meta = {}
for n, (name, desc, svg, bgm) in out.items():
    open(os.path.join(M, f"mix{n}.svg"), "w", encoding="utf-8").write(svg)
    meta[n] = [name, desc, bgm]
json.dump(meta, open(os.path.join(M, "mezclas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(out))
