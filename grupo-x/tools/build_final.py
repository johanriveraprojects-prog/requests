"""Logo FINAL de ProduAVX: AX de bloque con cresta de llamas, degradado cálido, contorno oscuro, chispa y toque verde.
Ideas tomadas de una ilustración de referencia (llamas en capas, rojo→naranja→amarillo, contorno grueso, chispa de 4 puntas);
no se copia ningún personaje ni marca. Genera SVG del logo y SVG de portadas para Instagram (PNG con export_instagram.js)."""
import os
from build_logo import text_path, svg, write, extrude, A_OUT, A_HOLE, X_OUT, OUT

INK, DEEP = "#1a0404", "#6e0e10"
CREAM, YEL, ORG, RED, GREEN = "#fff1d6", "#ffd166", "#ff8a1f", "#d62718", "#3fae49"

DEFS = f'''
<radialGradient id="bgf" cx=".5" cy=".62" r=".72"><stop offset="0" stop-color="#5a0f12"/><stop offset=".6" stop-color="#1b0709"/><stop offset="1" stop-color="#0a0306"/></radialGradient>
<linearGradient id="fl" gradientUnits="userSpaceOnUse" x1="0" y1="42" x2="0" y2="150"><stop offset="0" stop-color="{YEL}"/><stop offset=".45" stop-color="{ORG}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="fire" gradientUnits="userSpaceOnUse" x1="0" y1="4" x2="0" y2="48"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".5" stop-color="{YEL}"/><stop offset="1" stop-color="{ORG}"/></linearGradient>
<linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORG}"/><stop offset="1" stop-color="{YEL}"/></linearGradient>'''

STAR = "M0 -10Q1.5 -1.5 10 0Q1.5 1.5 0 10Q-1.5 1.5 -10 0Q-1.5 -1.5 0 -10Z"
sparkle = lambda x, y, k: f'<path d="{STAR}" transform="translate({x} {y}) scale({k})" fill="{YEL}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'


def letters(sw=3.4, d=7):
    face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
    flames = "".join(f'<path d="{p}" fill="url(#fire)" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>' for p in (
        "M112 44C110 28 128 22 122 4C142 14 148 32 138 44Z",       # llama del brazo izquierdo
        "M162 44C160 30 176 24 170 6C190 16 196 32 188 44Z",       # llama del brazo derecho
        "M139 50C139 38 150 34 147 18C160 26 164 40 161 50Z"))     # llama central (entre los brazos)
    leaf = f'<path d="M64 44C58 32 66 22 80 24C78 32 74 38 72 44Z" fill="{GREEN}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
    ext = extrude(A_OUT, d, d * .9, DEEP, INK, sw) + extrude(X_OUT, d, d * .9, DEEP, INK, sw)
    faces = (f'<path d="{face(A_OUT)} {face(A_HOLE)}" fill="url(#fl)" fill-rule="evenodd" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
             f'<path d="{face(X_OUT)}" fill="url(#fl)" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
    return flames + leaf + ext + faces


def disc(inner, ring=True):
    r = f'<circle cx="100" cy="100" r="95" fill="none" stroke="url(#rg)" stroke-width="5"/>' if ring else ""
    return f'<circle cx="100" cy="100" r="98" fill="url(#bgf)"/>{r}' + inner


def mark_body():
    return disc(f'{sparkle(34, 52, 1)}{sparkle(160, 166, .6)}'
                f'<g transform="translate(100 106) scale(.8) translate(-101 -96)">{letters()}</g>')


write("produavx-final-mark.svg", svg(200, 200, mark_body(), DEFS))

# Lockup con nombre
t = "ProduAVX"
d, wend = text_path(t, "InterDisplay-ExtraBold.otf", 92, 226, 122, -1)
name = f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/><path d="{d}" fill="{CREAM}"/>'
tag, _ = text_path("AUDIO · VIDEO · POST", "InterDisplay-Bold.otf", 19, 230, 158, 6)
write("produavx-final-logo.svg", svg(int(wend) + 14, 200, mark_body() + name + f'<path d="{tag}" fill="{ORG}"/>', DEFS))

# Monocromo (marca de agua / créditos): silueta plana sin degradados
mono = lambda c: svg(200, 200, f'<g transform="translate(100 106) scale(.8) translate(-101 -96)" fill="{c}" stroke="{c}" stroke-width="2" stroke-linejoin="round">'
    f'<path d="M112 44C110 28 128 22 122 4C142 14 148 32 138 44Z"/><path d="M162 44C160 30 176 24 170 6C190 16 196 32 188 44Z"/><path d="M139 50C139 38 150 34 147 18C160 26 164 40 161 50Z"/>'
    f'<path d="M{" L".join(f"{x} {y}" for x, y in A_OUT)}Z M{" L".join(f"{x} {y}" for x, y in A_HOLE)}Z" fill-rule="evenodd"/>'
    f'<path d="M{" L".join(f"{x} {y}" for x, y in X_OUT)}Z"/></g>')
write("produavx-final-mono-white.svg", mono("#ffffff"))
write("produavx-final-mono-black.svg", mono("#000000"))

# --- Instagram: avatar y portadas de destacados (SVG; PNG con export_instagram.js) ---
IG = os.path.join(OUT, "instagram"); os.makedirs(IG, exist_ok=True)


def ig(name, w, h, body):
    open(os.path.join(IG, name), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{DEFS}</defs>'
        f'<rect width="{w}" height="{h}" fill="#0a0306"/>{body}</svg>\n')


# Avatar 1:1, logo centrado con margen para el recorte circular
ig("avatar.svg", 1080, 1080, f'<g transform="translate(540 540) scale(5.1) translate(-100 -100)">{mark_body()}</g>')

# Portadas de destacados 1080x1920 (el recorte circular toma el centro)
G = lambda p, extra="": f'<path d="{p}" fill="url(#fl2)" stroke="{INK}" stroke-width="4" stroke-linejoin="round" {extra}/>'
glyphs = {
    "reels": G("M78 62L142 100L78 138Z"),
    "audio": "".join(f'<rect x="{x}" y="{100 - h / 2}" width="14" height="{h}" rx="7" fill="url(#fl2)" stroke="{INK}" stroke-width="4"/>' for x, h in ((52, 36), (72, 70), (92, 100), (112, 64), (132, 40))),
    "set": (f'<rect x="56" y="88" width="88" height="56" rx="5" fill="url(#fl2)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M54 62L146 78L142 92L50 76Z" fill="{CREAM}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'),
}
F2 = f'<linearGradient id="fl2" gradientUnits="userSpaceOnUse" x1="0" y1="50" x2="0" y2="150"><stop offset="0" stop-color="{YEL}"/><stop offset=".5" stop-color="{ORG}"/><stop offset="1" stop-color="{RED}"/></linearGradient>'
for k, g in glyphs.items():
    ig(f"destacado-{k}.svg", 1080, 1920, f'<defs>{F2}</defs><g transform="translate(540 960) scale(4.3) translate(-100 -100)">{disc(sparkle(36, 54, .9) + sparkle(162, 164, .55) + g)}</g>')
print("ok final")
