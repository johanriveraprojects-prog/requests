"""Semáforo 2D plano: tres círculos (rojo, ámbar, verde); el rojo enmarcado por corchetes de visor = REC."""
import os, json
from build_logo import OUT, text_path, svg as wrap

RED, AMB, GRN = "#ff3b30", "#ffb300", "#2ee66b"
BR, BG = "#eeeefa", "#000000"
M = os.path.join(OUT, "semaforo-2d"); os.makedirs(M, exist_ok=True)


def brackets(x1, y1, x2, y2, arm=12, sw=6, c=BR, corners=False):
    """Corchetes [ ] (o 4 esquinas de visor si corners=True) alrededor del recuadro (x1,y1)-(x2,y2)."""
    L = f'M{x1 + arm} {y1}H{x1}V{y2}H{x1 + arm}'
    R = f'M{x2 - arm} {y1}H{x2}V{y2}H{x2 - arm}'
    if corners:
        L = f'M{x1} {y1 + arm}V{y1}H{x1 + arm}M{x1} {y2 - arm}V{y2}H{x1 + arm}'
        R = f'M{x2 - arm} {y1}H{x2}V{y1 + arm}M{x2 - arm} {y2}H{x2}V{y2 - arm}'
    return f'<path d="{L} {R}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter"/>'


dot = lambda x, y, r, c: f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rec(x, y, r):
    """Punto rojo REC con una mira de lente negra: X de cuatro trazos finos con hueco central y un aro tenue
    (se lee como centro de enfoque, no como botón de cerrar)."""
    k, sw = .7071, max(r * .085, 1.4)
    i0, i1 = r * .17, r * .46   # radio interior (hueco) y exterior de los trazos
    segs = "".join(f"M{x + sx * i0 * k:.2f} {y + sy * i0 * k:.2f}L{x + sx * i1 * k:.2f} {y + sy * i1 * k:.2f}" for sx in (-1, 1) for sy in (-1, 1))
    return (dot(x, y, r, RED)
            + f'<circle cx="{x}" cy="{y}" r="{r * .72:.2f}" fill="none" stroke="#000" stroke-width="{sw * .6:.2f}" opacity=".28"/>'
            + f'<path d="{segs}" fill="none" stroke="#000" stroke-width="{sw:.2f}" stroke-linecap="round" opacity=".7"/>'
            + f'<circle cx="{x}" cy="{y}" r="{max(r * .05, .8):.2f}" fill="#000" opacity=".7"/>')


sq = f'<rect width="200" height="200" rx="46" fill="{BG}"/>'
v = {}
# 1 · Vertical: [●] sobre ● ●
v[1] = ("Vertical con corchetes", "Tres círculos planos apilados; el rojo va entre corchetes [ ● ] = REC.",
        sq + brackets(60, 20, 140, 84) + rec(100, 52, 21) + dot(100, 108, 21, AMB) + dot(100, 156, 21, GRN))
# 2 · Horizontal: [●] ● ●
v[2] = ("Horizontal con corchetes", "En fila: [ ● ]  ●  ●. Se lee como una línea de tiempo y como semáforo.",
        sq + brackets(12, 66, 80, 134) + rec(46, 100, 21) + dot(108, 100, 21, AMB) + dot(160, 100, 21, GRN))
# 3 · Visor: esquinas de enfoque alrededor de un rojo grande; ámbar y verde pequeños debajo
v[3] = ("Visor de cámara", "El rojo (REC) dentro de un marco de enfoque de cuatro esquinas; ámbar y verde abajo.",
        sq + brackets(40, 22, 160, 124, arm=18, sw=6, corners=True) + rec(100, 73, 28) + dot(78, 160, 14, AMB) + dot(122, 160, 14, GRN))
# 4 · Avatar: disco oscuro con la composición vertical, un poco mayor
v[4] = ("Avatar circular", "Disco plano con el semáforo vertical: lectura inmediata como foto de perfil.",
        f'<circle cx="100" cy="100" r="98" fill="{BG}"/><circle cx="100" cy="100" r="94" fill="none" stroke="#2c2c40" stroke-width="4"/>'
        + brackets(56, 22, 144, 88, arm=13) + rec(100, 55, 23) + dot(100, 112, 23, AMB) + dot(100, 160, 17, GRN).replace('r="17"', 'r="23"').replace('cy="160"', 'cy="165"'))
# 5 · Lockup con nombre
d, wend = text_path("ProduAVX", "InterDisplay-ExtraBold.otf", 78, 204, 94, -1)
lock = (brackets(8, 30, 64, 110, arm=11, sw=5.5) + rec(36, 70, 17) + dot(88, 70, 17, AMB) + dot(136, 70, 17, GRN) + f'<path d="{d}" fill="{BR}"/>')
v[5] = ("Con nombre", "Los tres círculos con [●] y el nombre en blanco: versión horizontal para portadas.", None)

for n, (name, desc, body) in v.items():
    if n == 5:
        open(os.path.join(M, "v5.svg"), "w", encoding="utf-8").write(wrap(int(wend) + 12, 140, lock, "", "ProduAVX semáforo"))
    else:
        open(os.path.join(M, f"v{n}.svg"), "w", encoding="utf-8").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX semáforo {n}">{body}</svg>\n')
json.dump({n: [a, b] for n, (a, b, _) in v.items()}, open(os.path.join(M, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(v))
