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
print("ok")
