"""Variantes numeradas del logo AX para decidir (las ya elegidas se consolidan luego en build_final.py)."""
import os, math
from build_logo import text_path, write, extrude, A_OUT, A_HOLE, X_OUT, OUT

INK, DEEP = "#1a0404", "#6e0e10"
CREAM, YEL, ORG, RED, GREEN, CY, VI = "#fff1d6", "#ffd166", "#ff8a1f", "#d62718", "#3fae49", "#46e0ff", "#9a6bff"
V = os.path.join(OUT, "variantes"); os.makedirs(V, exist_ok=True)

DEFS = f'''
<radialGradient id="bg" cx=".5" cy=".62" r=".72"><stop offset="0" stop-color="#5a0f12"/><stop offset=".6" stop-color="#1b0709"/><stop offset="1" stop-color="#0a0306"/></radialGradient>
<radialGradient id="bgc" cx=".5" cy=".62" r=".72"><stop offset="0" stop-color="#1c1a52"/><stop offset=".6" stop-color="#0d0d26"/><stop offset="1" stop-color="#07070d"/></radialGradient>
<linearGradient id="fl" gradientUnits="userSpaceOnUse" x1="0" y1="42" x2="0" y2="150"><stop offset="0" stop-color="{YEL}"/><stop offset=".45" stop-color="{ORG}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="fc" gradientUnits="userSpaceOnUse" x1="20" y1="42" x2="180" y2="150"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>
<linearGradient id="fire" gradientUnits="userSpaceOnUse" x1="0" y1="4" x2="0" y2="48"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="{YEL}"/><stop offset="1" stop-color="{ORG}"/></linearGradient>
<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORG}"/><stop offset="1" stop-color="{YEL}"/></linearGradient>'''

FL = ("M112 44C110 28 128 22 122 4C142 14 148 32 138 44Z", "M162 44C160 30 176 24 170 6C190 16 196 32 188 44Z", "M139 50C139 38 150 34 147 18C160 26 164 40 161 50Z")
LEAF = "M64 44C58 32 66 22 80 24C78 32 74 38 72 44Z"
STAR = "M0 -10Q1.5 -1.5 10 0Q1.5 1.5 0 10Q-1.5 1.5 -10 0Q-1.5 -1.5 0 -10Z"
spark = lambda x, y, k, c=YEL: f'<path d="{STAR}" transform="translate({x} {y}) scale({k})" fill="{c}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
FIT = lambda s=.8, cy=106: f'translate(100 {cy}) scale({s}) translate(-101 -96)'


def P(d, fill, sw=3.4, stroke=INK, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def block(fill="url(#fl)", deep=DEEP, d=7, sw=3.4, border=None):
    ext = extrude(A_OUT, d, d * .9, deep, INK, sw) + extrude(X_OUT, d, d * .9, deep, INK, sw) if d else ""
    fa = f'{face(A_OUT)} {face(A_HOLE)}'
    out = ""
    if border:  # borde tipo adhesivo
        out += P(fa, border, 12, border, 'fill-rule="evenodd"') + P(face(X_OUT), border, 12, border)
    return out + ext + P(fa, fill, sw, INK, 'fill-rule="evenodd"') + P(face(X_OUT), fill, sw) 


def flames(fill="url(#fire)", sw=3.4):
    return "".join(P(f, fill, sw) for f in FL)


def disc(inner, bg="url(#bg)", ring="url(#rg)"):
    return f'<circle cx="100" cy="100" r="98" fill="{bg}"/><circle cx="100" cy="100" r="95" fill="none" stroke="{ring}" stroke-width="5"/>' + inner


variants = {}

# 1 · Final actual (referencia): volumen + cresta + chispa + hoja
variants[1] = ("Final actual", "Volumen oscuro, cresta de llamas, chispa y hoja verde.",
    disc(spark(34, 52, 1) + spark(160, 166, .6) + f'<g transform="{FIT()}">{flames()}{P(LEAF, GREEN)}{block()}</g>'))

# 2 · Adhesivo: plano con borde crema grueso, sin volumen (se lee sobre cualquier fondo)
variants[2] = ("Adhesivo (sticker)", "Plano con borde crema: se ve sobre cualquier foto o fondo.",
    f'<circle cx="100" cy="100" r="98" fill="url(#bg)"/><g transform="{FIT(.84, 108)}">'
    + "".join(P(f, CREAM, 12, CREAM) for f in FL) + block(border=CREAM, d=0) + flames() + P(LEAF, GREEN) + '</g>')

# 3 · Monolínea de fuego: trazo redondeado con degradado y una sola llama continua
variants[3] = ("Monolínea de fuego", "Trazo único; elegante, cercano a la línea C ya elegida.",
    disc(f'<g transform="{FIT(.86, 108)}" fill="none" stroke="url(#fl)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M22 152L58 56L94 152"/><path d="M38 124H78"/><path d="M112 70L168 152M168 70L112 152"/>'
         f'<path d="M140 62C128 44 148 40 140 18C160 30 162 50 150 64" stroke="url(#fire)" stroke-width="8"/></g>'))

# 4 · Escudo / insignia
variants[4] = ("Escudo", "Insignia de estudio: más formal y de marca registrada.",
    f'<path d="M100 4L186 28V104C186 152 146 180 100 196C54 180 14 152 14 104V28Z" fill="url(#bg)" stroke="url(#rg)" stroke-width="6" stroke-linejoin="round"/>'
    + spark(40, 50, .8) + spark(160, 50, .8) + f'<g transform="{FIT(.7, 106)}">{flames()}{P(LEAF, GREEN)}{block()}</g>')

# 5 · X de llamas: la X son dos hojas de fuego cruzadas (puntas afiladas hacia arriba); la A, de bloque


def leaf(p0, p1, w):
    """Hoja de punta afilada de p0 a p1, ancho máx. w (borde recto con puntas largas)."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); dx, dy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -dy, dx
    pt = lambda t, o: (x0 + dx * L * t + nx * w * o, y0 + dy * L * t + ny * w * o)
    f = lambda q: f"{q[0]:.1f} {q[1]:.1f}"
    return "M" + f(p0) + "L" + f(pt(.3, .5)) + "L" + f(pt(.7, .5)) + "L" + f(p1) + "L" + f(pt(.7, -.5)) + "L" + f(pt(.3, -.5)) + "Z"


variants[5] = ("X de llamas", "La X nace del fuego: dos hojas cruzadas; la A, sólida.",
    disc(spark(34, 52, 1) + f'<g transform="{FIT()}">{extrude(A_OUT, 7, 6.3, DEEP, INK, 3.4)}{P(face(A_OUT) + " " + face(A_HOLE), "url(#fl)", 3.4, INK, "fill-rule=\"evenodd\"")}'
         + P(leaf((112, 152), (180, 38), 36), "url(#fl)") + P(leaf((182, 152), (114, 38), 36), "url(#fl)") + '</g>'))

# 6 · Lente de cámara: aperture + AX; hace evidente "video"
ap = "".join(f'<line x1="100" y1="100" x2="{100 + 80 * math.cos(math.radians(a)):.1f}" y2="{100 + 80 * math.sin(math.radians(a)):.1f}" stroke="#3a1410" stroke-width="2.2"/>' for a in range(0, 360, 60))
variants[6] = ("Lente", "Disco como lente con diafragma; comunica video al instante.",
    f'<circle cx="100" cy="100" r="98" fill="#0a0306"/><circle cx="100" cy="100" r="95" fill="none" stroke="url(#rg)" stroke-width="5"/><circle cx="100" cy="100" r="84" fill="url(#bg)" stroke="#3a1410" stroke-width="3"/>{ap}'
    + f'<circle cx="100" cy="100" r="60" fill="url(#bg)" stroke="#3a1410" stroke-width="2"/><g transform="{FIT(.62, 108)}">{flames()}{P(LEAF, GREEN)}{block(d=5)}</g><circle cx="160" cy="40" r="6" fill="{RED}" stroke="{INK}" stroke-width="2"/>')

# 7 · Híbrido cian/violeta del sitio + cresta de fuego (no obliga a re-temar la web)
variants[7] = ("Híbrido sitio", "Letras cian→violeta del sitio con la cresta de fuego como acento.",
    disc(spark(34, 52, 1, CY) + spark(160, 166, .6, VI) + f'<g transform="{FIT()}">{flames()}{block(fill="url(#fc)", deep="#2a1a6e")}</g>', bg="url(#bgc)", ring="url(#fc)"))

# 8 · Ícono plano: cuadrado redondeado, letras crema planas, una llama y el punto rojo/verde
variants[8] = ("Ícono plano", "Mínimo y plano: letras crema, una llama naranja y punto tally.",
    f'<rect width="200" height="200" rx="46" fill="#12060a"/><g transform="{FIT(.82, 108)}"><path d="{FL[2].replace("139 50","139 52")}" transform="translate(-2 -2)" fill="{ORG}"/><path d="{FL[1]}" fill="{ORG}"/><path d="{FL[0]}" fill="{ORG}"/>'
    f'<path d="{face(A_OUT)} {face(A_HOLE)}" fill="{CREAM}" fill-rule="evenodd"/><path d="{face(X_OUT)}" fill="{CREAM}"/></g>'
    f'<clipPath id="t"><circle cx="40" cy="40" r="10"/></clipPath><g clip-path="url(#t)"><rect x="28" y="28" width="12" height="24" fill="#ff3b3b"/><rect x="40" y="28" width="12" height="24" fill="#2ee66b"/></g>')

for n, (name, desc, body) in variants.items():
    open(os.path.join(V, f"v{n}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX variante {n}"><defs>{DEFS}</defs>{body}</svg>\n')
import json; json.dump({n: [a, b] for n, (a, b, _) in variants.items()}, open(os.path.join(V, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(variants))
