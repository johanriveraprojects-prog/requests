"""Mezclas de las variantes 7 (híbrido cian/violeta + cresta de fuego) y 8 (ícono plano + punto tally rojo/verde)."""
import os, json
from build_logo import OUT, A_OUT, A_HOLE, X_OUT

CY, VI, ORG, YEL, CREAM, BG = "#46e0ff", "#9a6bff", "#ff8a1f", "#ffd166", "#fff1d6", "#0b0b1c"
M = os.path.join(OUT, "mezclas"); os.makedirs(M, exist_ok=True)
FL = ("M112 44C110 28 128 22 122 4C142 14 148 32 138 44Z", "M162 44C160 30 176 24 170 6C190 16 196 32 188 44Z", "M139 50C139 38 150 34 147 18C160 26 164 40 161 50Z")
face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
FIT = lambda s=.82, cy=108: f'translate(100 {cy}) scale({s}) translate(-101 -96)'
DEFS = f'''<linearGradient id="fc" gradientUnits="userSpaceOnUse" x1="20" y1="42" x2="185" y2="150"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>
<linearGradient id="fire" gradientUnits="userSpaceOnUse" x1="0" y1="4" x2="0" y2="48"><stop offset="0" stop-color="{YEL}"/><stop offset="1" stop-color="{ORG}"/></linearGradient>
<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>
<radialGradient id="bgc" cx=".5" cy=".62" r=".72"><stop offset="0" stop-color="#1c1a52"/><stop offset=".6" stop-color="#0d0d26"/><stop offset="1" stop-color="#07070d"/></radialGradient>'''


def tally(x, y, r=10):
    return (f'<clipPath id="t"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath><g clip-path="url(#t)">'
            f'<rect x="{x - r}" y="{y - r}" width="{r}" height="{2 * r}" fill="#ff3b3b"/><rect x="{x}" y="{y - r}" width="{r}" height="{2 * r}" fill="#2ee66b"/></g>')


def letters(fa, fx, stroke="none", sw=0):
    s = f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
    return (f'<path d="{face(A_OUT)} {face(A_HOLE)}" fill="{fa}" fill-rule="evenodd" {s}/><path d="{face(X_OUT)}" fill="{fx}" {s}/>')


flames = "".join(f'<path d="{p}" fill="url(#fire)"/>' for p in FL)
sq = f'<rect width="200" height="200" rx="46" fill="{BG}"/>'
mix = {}
mix[1] = ("Plano degradado", "Cuadrado redondeado: letras planas cian→violeta, cresta naranja, punto tally.",
          sq + f'<g transform="{FIT()}">{flames}{letters("url(#fc)", "url(#fc)")}</g>' + tally(40, 40))
mix[2] = ("Disco Instagram", "Versión circular: aro cian→violeta, letras planas y cresta; ideal de perfil.",
          f'<circle cx="100" cy="100" r="98" fill="url(#bgc)"/><circle cx="100" cy="100" r="94" fill="none" stroke="url(#rg)" stroke-width="5"/>'
          f'<g transform="{FIT(.78, 110)}">{flames}{letters("url(#fc)", "url(#fc)")}</g>' + tally(46, 62))
mix[3] = ("Contorno hueco", "Letras en contorno cian→violeta (trazo grueso) con cresta naranja rellena.",
          sq + f'<g transform="{FIT()}">{flames}{letters("none", "none", "url(#fc)", 7)}</g>' + tally(40, 40))
mix[4] = ("Dúo bicolor", "A cian y X violeta planas (dos voces: audio y video), cresta naranja.",
          sq + f'<g transform="{FIT()}">{flames}{letters(CY, VI)}</g>' + tally(40, 40))

for n, (name, desc, body) in mix.items():
    open(os.path.join(M, f"v{n}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX mezcla {n}"><defs>{DEFS}</defs>{body}</svg>\n')
json.dump({n: [a, b] for n, (a, b, _) in mix.items()}, open(os.path.join(M, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(mix))
