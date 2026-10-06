"""Genera el kit de logos de ProduAVX (SVG, texto convertido a trazos). Requiere: pip install fonttools"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
FONTS = "/usr/share/fonts/opentype/inter/"
CYAN, VIOLET = "#46e0ff", "#9a6bff"


def leaf(p0, p1, w):
    """Cinta de punta afilada (como las del chevron de la X de referencia), de p0 a p1 con ancho w."""
    (x0, y0), (x1, y1) = p0, p1
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    dx, dy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -dy, dx
    pt = lambda t, o: (x0 + dx * L * t + nx * w * o, y0 + dy * L * t + ny * w * o)
    f = lambda q: f"{q[0]:.1f} {q[1]:.1f}"
    # cinta recta con puntas largas y afiladas (grosor máx. = w)
    return ("M" + f(p0) + "L" + f(pt(.22, .5)) + "L" + f(pt(.78, .5)) + "L" + f(p1)
            + "L" + f(pt(.78, -.5)) + "L" + f(pt(.22, -.5)) + "Z")


def letters(fill, stroke, sw, w, bar):
    """A + X en cintas huecas; el orden de dibujo da el entrelazado de la X."""
    bar = "#6fb4ff" if bar.startswith("url") else bar  # un degradado de caja falla en una línea horizontal
    L = lambda a, b: f'<path d="{leaf(a, b, w)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return (f'<path d="M53 122H83" stroke="{bar}" stroke-width="{sw * 1.3:.1f}" stroke-linecap="round"/>'
            + L((34, 152), (66, 52)) + L((98, 152), (66, 52))
            + L((118, 52), (170, 152)) + L((170, 52), (118, 152)))


def mark(uid, fill, ring, detail=True, sw=4.2, w=17, disc="#0b0b22", crescent="#05050f"):
    """Monograma AX fusionado: disco oscuro con doble anillo y media luna de sombra (referencia P)
    + A y X en cintas huecas de punta afilada (referencia X). fill/ring: color o url(#grad)."""
    if not detail:  # favicon: sin media luna ni anillo fino, trazos más gruesos
        return (f'<circle cx="100" cy="100" r="92" fill="{disc}"/><circle cx="100" cy="100" r="88" fill="none" stroke="{ring}" stroke-width="7"/>'
                f'<g transform="translate(100 100) scale(1.1) translate(-100 -102)">{letters(disc, fill, 7, 20, fill)}</g>')
    return (f'<circle cx="92" cy="110" r="90" fill="{crescent}"/>'
            f'<circle cx="100" cy="100" r="86" fill="{disc}"/>'
            f'<circle cx="100" cy="100" r="86" fill="none" stroke="#9a9ab8" stroke-width="3" opacity=".8"/>'
            f'<circle cx="100" cy="100" r="93" fill="none" stroke="{ring}" stroke-width="6" stroke-linecap="round" stroke-dasharray="520 64" transform="rotate(-62 100 100)"/>'
            f'<g transform="translate(100 100) scale(.92) translate(-100 -102)">{letters(disc, fill, sw, w, fill)}</g>')


def grad(uid):
    return f'<linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'


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


# 1) Monograma a color (header / hero / favicon)
write("produavx-mark.svg", svg(200, 200, mark("a", "url(#ga)", "url(#ga)"), grad("a")))

# 2) Lockups horizontales
for name, c1, tag in (("produavx-logo.svg", "#eeeefa", "#9393b0"), ("produavx-logo-light.svg", "#12121f", "#5b5b78")):
    uid = name[9:10] + ("l" if "light" in name else "d")
    wm, wend = wordmark(uid, c1, f"url(#g{uid})", tag)
    write(name, svg(int(wend) + 12, 200, mark(uid, f"url(#g{uid})", f"url(#g{uid})") + wm, grad(uid)))

# 3) Monocromo (impresión / sellos): disco sólido con letras recortadas
for name, col in (("produavx-mark-white.svg", "#ffffff"), ("produavx-mark-black.svg", "#000000")):
    u = name[14:15]
    cut = letters("#fff", "#000", 4.2, 17, "#000")
    body = (f'<mask id="k{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200"><rect width="200" height="200" fill="#fff"/>'
            f'<g transform="translate(100 100) scale(.92) translate(-100 -102)">{cut}</g></mask>'
            f'<circle cx="100" cy="100" r="86" fill="{col}" mask="url(#k{u})"/>'
            f'<circle cx="100" cy="100" r="93" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-dasharray="520 64" transform="rotate(-62 100 100)"/>')
    write(name, svg(200, 200, body))

# 4) Favicon simplificado
write("produavx-favicon.svg", svg(200, 200, mark("f", "url(#gf)", "url(#gf)", detail=False), grad("f")))
print("ok")
