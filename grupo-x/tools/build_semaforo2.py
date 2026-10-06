"""Semáforo ProduAVX desde cero (sin letras). Luces con símbolos de producción: rojo REC, ámbar audio, verde video."""
import os, json, random
from build_logo import OUT

RED, AMB, GRN = "#ff3b30", "#ffb300", "#2ee66b"
INK = {RED: "#3d0805", AMB: "#3d2600", GRN: "#053a1a"}
HOUSE, EDGE, BG = "#14141f", "#2c2c40", "#07070d"
M = os.path.join(OUT, "semaforo-nuevo"); os.makedirs(M, exist_ok=True)

DEFS = "".join(
    f'<radialGradient id="l{i}" cx=".38" cy=".32" r=".85"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{c}"/><stop offset="1" stop-color="{lo}"/></radialGradient>'
    for i, (c, hi, lo) in enumerate(((RED, "#ff9a90", "#a3140c"), (AMB, "#ffe08a", "#b87a00"), (GRN, "#a8ffc8", "#12a84a"))))
DEFS += f'<linearGradient id="rv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}"/><stop offset=".5" stop-color="{AMB}"/><stop offset="1" stop-color="{GRN}"/></linearGradient>'
DEFS += f'<radialGradient id="bgd" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#1b1b2e"/><stop offset="1" stop-color="{BG}"/></radialGradient>'


def sym(kind, cx, cy, c):
    k = INK[c]
    if kind == "rec":
        return f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{k}"/><circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{k}" stroke-width="2.6"/>'
    if kind == "audio":
        return "".join(f'<rect x="{cx - 11 + i * 5.5:.1f}" y="{cy - h / 2}" width="3.6" height="{h}" rx="1.8" fill="{k}"/>' for i, h in enumerate((7, 15, 23, 15, 7)))
    if kind == "play":
        return f'<path d="M{cx - 6} {cy - 9.5}L{cx + 10} {cy}L{cx - 6} {cy + 9.5}Z" fill="{k}" stroke="{k}" stroke-width="2" stroke-linejoin="round"/>'
    return ""


def light(i, cx, cy, r, kind, c, glow=True):
    g = f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="{c}" opacity=".16"/>' if glow else ""
    return (g + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#l{i})" stroke="{BG}" stroke-width="3"/>'
            f'<ellipse cx="{cx - r * .3:.1f}" cy="{cy - r * .45:.1f}" rx="{r * .4:.1f}" ry="{r * .2:.1f}" fill="#fff" opacity=".35"/>' + sym(kind, cx, cy, c))


KINDS = [(RED, "rec"), (AMB, "audio"), (GRN, "play")]
v = {}

def housing_v(cx, with_sym=True):
    x = cx - 44
    body = f'<rect x="{x}" y="6" width="88" height="188" rx="28" fill="{HOUSE}" stroke="{EDGE}" stroke-width="4"/>'
    for (c, k), y, i in zip(KINDS, (50, 100, 150), range(3)):
        body += f'<path d="M{cx - 27} {y - 17}Q{cx} {y - 36} {cx + 27} {y - 17}" fill="none" stroke="{BG}" stroke-width="6" stroke-linecap="round"/>'
        body += light(i, cx, y, 20, k if with_sym else "", c)
    return body

# 1 · Clásico: semáforo vertical limpio, luces vacías (el más puro)
v[1] = ("Clásico limpio", "Semáforo vertical sin símbolos: tres tonos y visores. El más puro y reconocible.", housing_v(100, False))
# 2 · Con símbolos de producción
v[2] = ("Símbolos de producción", "Rojo = REC · ámbar = audio (onda) · verde = video (play). El significado vive en las luces.", housing_v(100))
# 3 · Horizontal con símbolos
body = f'<rect x="6" y="54" width="188" height="92" rx="34" fill="{HOUSE}" stroke="{EDGE}" stroke-width="4"/>'
for (c, k), x, i in zip(KINDS, (46, 100, 154), range(3)):
    body += light(i, x, 100, 22, k, c)
v[3] = ("Horizontal", "Los mismos símbolos en horizontal: banner de portada y encabezado.", body)
# 4 · Avatar: sin carcasa, tres luces en disco con aro de semáforo
body = f'<circle cx="100" cy="100" r="98" fill="url(#bgd)"/><circle cx="100" cy="100" r="93" fill="none" stroke="url(#rv)" stroke-width="6"/>'
for (c, k), y, i in zip(KINDS, (48, 100, 152), range(3)):
    body += light(i, 100, y, 21, k, c)
v[4] = ("Avatar circular", "Sin carcasa: tres luces en un disco con aro rojo→ámbar→verde; pensado para perfil de Instagram.", body)
# 5 · Desintegración: el semáforo se deshace en partículas hacia la izquierda (las letras que se disuelven)
rnd = random.Random(7)
parts = ""
for n in range(46):
    x = rnd.uniform(8, 64); y = rnd.uniform(16, 184); t = 1 - (x - 8) / 60
    c = rnd.choice((RED, AMB, GRN)); s = rnd.uniform(2, 6.5) * (.5 + .5 * (1 - t))
    parts += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s * .25:.1f}" fill="{c}" opacity="{.15 + .7 * (1 - t):.2f}" transform="rotate({rnd.randint(0, 60)} {x:.1f} {y:.1f})"/>'
v[5] = ("Desintegración", "El semáforo se disuelve en partículas de los tres tonos: guiño a las letras que se deshicieron.", parts + housing_v(120))

for n, (name, desc, body) in v.items():
    open(os.path.join(M, f"v{n}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX semáforo {n}"><defs>{DEFS}</defs>{body}</svg>\n')
json.dump({n: [a, b] for n, (a, b, _) in v.items()}, open(os.path.join(M, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(v))
