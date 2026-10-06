"""Kit de logos ProduAVX (SVG, texto a trazos). Requiere: pip install fonttools
Marca principal = monolínea (C). Versión pequeña (<48 px: favicon, header, destacados) = sólida (A)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
FONTS = "/usr/share/fonts/opentype/inter/"
CYAN, VIOLET = "#46e0ff", "#9a6bff"


def text_path(txt, font, size, x, y, spacing=0.0):
    f = TTFont(FONTS + font)
    gs, cmap, upem = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    k, d = size / upem, []
    for ch in txt:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, y)))
        d.append(pen.getCommands())
        x += gs[g].width * k + spacing
    return " ".join(d), x


def wordmark(uid, c1, c2, tag):
    d1, x = text_path("Produ", "InterDisplay-Medium.otf", 104, 222, 112, -1.5)
    d2, x2 = text_path("AVX", "InterDisplay-Bold.otf", 104, x, 112, -1.5)
    dt, _ = text_path("AUDIO · VIDEO · POST", "InterDisplay-Medium.otf", 20, 226, 152, 6.2)
    return f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/><path d="{dt}" fill="{tag}" opacity=".85"/>', x2


def svg(w, h, body, defs="", title="ProduAVX"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title><defs>{defs}</defs>{body}</svg>\n')


def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(s)


BG = "#0b0b1c"


def grad(uid):
    return (f'<linearGradient id="g{uid}" gradientUnits="userSpaceOnUse" x1="30" y1="40" x2="175" y2="160">'
            f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')


def letters_line(stroke):
    """AX monolínea: trazo único redondeado (marca principal)."""
    return (f'<g transform="translate(100 102) scale(.9) translate(-100 -102)" fill="none" stroke="{stroke}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M30 152L64 54L98 152"/><path d="M45 122H83"/><path d="M116 54L172 152M172 54L116 152"/></g>')


def letters_solid(stroke):
    """AX sólido: letras gruesas para tamaños pequeños."""
    return (f'<g transform="translate(100 102) scale(.88) translate(-100 -102)" fill="none" stroke="{stroke}" stroke-width="21" stroke-linejoin="miter">'
            '<path d="M32 152L66 54L100 152"/><path d="M48 122H84" stroke-width="15"/><path d="M123 54L177 152M177 54L123 152"/></g>')


def mark(uid, stroke, small=False, disc=BG):
    body = f'<circle cx="100" cy="100" r="98" fill="{disc}"/>' if disc else ""
    return body + (letters_solid(stroke) if small else letters_line(stroke))


# 1) Marca principal (monolínea) y versión pequeña (sólida), con disco
write("produavx-mark.svg", svg(200, 200, mark("a", "url(#ga)"), grad("a")))
write("produavx-mark-small.svg", svg(200, 200, mark("s", "url(#gs)", small=True), grad("s")))
write("produavx-favicon.svg", svg(200, 200, mark("f", "url(#gf)", small=True), grad("f")))

# 2) Lockups horizontales (marca principal + nombre)
for name, c1, tag in (("produavx-logo.svg", "#eeeefa", "#9393b0"), ("produavx-logo-light.svg", "#12121f", "#5b5b78")):
    uid = "d" if name == "produavx-logo.svg" else "l"
    wm, wend = wordmark(uid, c1, f"url(#t{uid})", tag)
    tg = (f'<linearGradient id="t{uid}" gradientUnits="userSpaceOnUse" x1="{wend - 190:.0f}" y1="40" x2="{wend:.0f}" y2="120">'
          f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    write(name, svg(int(wend) + 12, 200, mark(uid, f"url(#g{uid})") + wm, grad(uid) + tg))

# 3) Monocromo sin disco (marca de agua, créditos, grabado)
for name, col in (("produavx-mark-white.svg", "#ffffff"), ("produavx-mark-black.svg", "#000000")):
    write(name, svg(200, 200, mark("m", col, disc=None)))

# 4) Familia BÁSICA: AX plano de un solo color + punto tally mitad rojo / mitad verde (luz de cámara)
RED, GREEN = "#ff3b3b", "#2ee66b"


def basic(ink, bg=None, dot=True):
    disc = f'<rect width="200" height="200" rx="44" fill="{bg}"/>' if bg else ""
    tally = (f'<defs><clipPath id="tl"><circle cx="178" cy="46" r="11"/></clipPath></defs>'
             f'<g clip-path="url(#tl)"><rect x="160" y="30" width="18" height="32" fill="{RED}"/><rect x="178" y="30" width="18" height="32" fill="{GREEN}"/></g>') if dot else ""
    return (disc + f'<g fill="none" stroke="{ink}" stroke-width="13" stroke-linejoin="miter">'
            '<path d="M22 152L58 56L94 152"/><path d="M38 122H78"/><path d="M110 56L162 152M162 56L110 152"/></g>' + tally)


write("produavx-basic-mark.svg", svg(200, 200, basic("#eeeefa", "#0b0b1c")))
write("produavx-basic-mark-light.svg", svg(200, 200, basic("#12121f", "#ffffff")))
write("produavx-basic-mark-mono.svg", svg(200, 200, basic("#000000", None, dot=False)))
for name, ink, tag in (("produavx-basic-logo.svg", "#eeeefa", "#9393b0"), ("produavx-basic-logo-light.svg", "#12121f", "#5b5b78")):
    wm, wend = wordmark("b", ink, ink, tag)
    write(name, svg(int(wend) + 12, 200, basic(ink, None) + wm))

# 5) Familia CÓMIC RETRO: letras de bloque rojas con extrusión amarilla y contorno negro
# (técnica inspirada en logotipos de cómic con relieve; geometría propia de A y X, profundidad hacia abajo-derecha)
COMIC_RED, COMIC_YEL, COMIC_INK = "#e8322c", "#ffd60a", "#111111"
A_OUT = [(14, 150), (48, 42), (84, 42), (118, 150), (92, 150), (85, 126), (47, 126), (40, 150)]
A_HOLE = [(55, 104), (77, 104), (66, 68)]
X_OUT = [(112, 42), (138, 42), (150, 66), (162, 42), (188, 42), (164, 96), (188, 150), (162, 150), (150, 126), (138, 150), (112, 150), (136, 96)]


def extrude(poly, dx, dy, yel, ink, sw):
    """Caras laterales de la extrusión: solo aristas que miran hacia (dx, dy)."""
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    sign = 1 if area > 0 else -1
    out = ""
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
        nx, ny = (y1 - y0) * sign, -(x1 - x0) * sign  # normal exterior
        if nx * dx + ny * dy > 0:
            out += (f'<path d="M{x0} {y0}L{x1} {y1}L{x1 + dx} {y1 + dy}L{x0 + dx} {y0 + dy}Z" fill="{yel}" stroke="{ink}" '
                    f'stroke-width="{sw}" stroke-linejoin="round"/>')
    return out


def comic(red=COMIC_RED, yel=COMIC_YEL, ink=COMIC_INK, sw=3.6, d=15):
    dx, dy = d, d * .9
    ext = extrude(A_OUT, dx, dy, yel, ink, sw) + extrude(X_OUT, dx, dy, yel, ink, sw)
    face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
    faces = (f'<path d="{face(A_OUT)} {face(A_HOLE)}" fill="{red}" fill-rule="evenodd" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>'
             f'<path d="{face(X_OUT)}" fill="{red}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>')
    return f'<g transform="translate(-2 4)">{ext}{faces}</g>'


write("produavx-comic-mark.svg", svg(210, 200, comic()))
d1, wend = text_path("ProduAVX", "InterDisplay-ExtraBold.otf", 96, 232, 124, -1)
write("produavx-comic-logo.svg", svg(int(wend) + 14, 200, comic() + f'<path d="{d1}" fill="#eeeefa" stroke="{COMIC_INK}" stroke-width="0"/>'))
write("produavx-comic-logo-light.svg", svg(int(wend) + 14, 200, comic() + f'<path d="{d1}" fill="#12121f"/>'))
print("ok")
