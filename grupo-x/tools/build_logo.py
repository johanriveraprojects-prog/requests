"""Genera el kit de logos de ProduAVX (SVG, texto convertido a trazos). Requiere: pip install fonttools"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
FONTS = "/usr/share/fonts/opentype/inter/"
CYAN, VIOLET = "#46e0ff", "#9a6bff"


def mark(uid, fill, ring, detail=True, sw=20, hole=5.5):
    """Monograma PX. fill/ring: color sólido o url(#grad). detail=False -> versión simple (favicon)."""
    cut = lambda d: f'<path d="{d}" stroke="#000" stroke-width="{hole}"/>' if detail else ""
    return f'''<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M44 156V46H76C108 46 108 100 76 100H44" stroke="#fff" stroke-width="{sw}"/>
        {cut("M44 148V54M52 46H76C100 46 100 100 76 100H52")}
        <path d="M92 70L168 158" stroke="#fff" stroke-width="{sw}"/>
        {cut("M95 73L165 154")}
        <path d="M170 62L90 158" stroke="#000" stroke-width="{sw + 7}"/>
        <path d="M170 62L90 158" stroke="#fff" stroke-width="{sw}"/>
        {cut("M167 66L93 154")}
      </g></mask>
    <circle cx="100" cy="100" r="93" fill="none" stroke="{ring}" stroke-width="5" stroke-linecap="round" stroke-dasharray="500 80" transform="rotate(-62 100 100)"/>
    <rect width="200" height="200" fill="{fill}" mask="url(#m{uid})"/>'''


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

# 3) Monocromo (impresión / sellos)
for name, col in (("produavx-mark-white.svg", "#ffffff"), ("produavx-mark-black.svg", "#000000")):
    write(name, svg(200, 200, mark(name[14:15], col, col)))

# 4) Favicon simplificado (trazo grueso, sin hueco de cinta, sin anillo fino)
write("produavx-favicon.svg", svg(200, 200,
      '<rect width="200" height="200" rx="40" fill="#07070d"/><g transform="translate(24 24) scale(.88)">'
      + mark("f", "url(#gf)", "url(#gf)", detail=False, sw=26) + "</g>", grad("f")))
print("ok")
