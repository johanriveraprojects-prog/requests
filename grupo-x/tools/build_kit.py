"""Kit final de marca ProduAVX (semáforo 2D, fondo negro, mira de lente en el REC).
Genera grupo-x/kit-de-marca/{svg,png,instagram,favicon}, catálogo index.html, LEEME.txt y el ZIP.
Uso: python3 build_kit.py && NODE_PATH=$(npm root -g) node export_kit.js && python3 build_kit.py --zip"""
import os, sys, json, shutil, zipfile
from build_semaforo3 import brackets, dot, rec, RED, AMB, GRN, BR, BG
from build_logo import text_path, OUT

ROOT = os.path.abspath(os.path.join(OUT, "..", ".."))                      # grupo-x/
KIT = os.path.join(ROOT, "kit-de-marca")
EXB, BOLD, DARK = "InterDisplay-ExtraBold.otf", "InterDisplay-Bold.otf", "#12121f"
for d in ("svg", "png", "instagram", "favicon"):
    os.makedirs(os.path.join(KIT, d), exist_ok=True)


def wrap(w, h, body, title="ProduAVX"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'


def icon_g(x, y, s, bg=True, bc=BR):
    """Ícono [●]●● (con mira de lente en el rojo) a escala s; bg=True añade el cuadrado negro redondeado."""
    r = f'<rect width="200" height="200" rx="46" fill="{BG}"/>' if bg else ""
    return (f'<g transform="translate({x} {y}) scale({s})">{r}' + brackets(12, 66, 80, 134, c=bc)
            + rec(46, 100, 21) + dot(108, 100, 21, AMB) + dot(160, 100, 21, GRN) + '</g>')


def mono_icon(col):
    """Ícono de una sola tinta: la mira de lente queda calada (transparente) en el primer círculo."""
    k, sw, i0, i1, r = .7071, 21 * .085, 21 * .17, 21 * .46, 21
    segs = "".join(f"M{46 + sx * i0 * k:.2f} {100 + sy * i0 * k:.2f}L{46 + sx * i1 * k:.2f} {100 + sy * i1 * k:.2f}" for sx in (-1, 1) for sy in (-1, 1))
    m = (f'<mask id="mk"><rect width="200" height="200" fill="#fff"/><path d="{segs}" stroke="#000" stroke-width="{sw * 1.15:.2f}" stroke-linecap="round" fill="none"/>'
         f'<circle cx="46" cy="100" r="{r * .72}" fill="none" stroke="#000" stroke-width="{sw * .6:.2f}" opacity=".6"/></mask>')
    return m + brackets(12, 66, 80, 134, c=col) + f'<circle cx="46" cy="100" r="21" fill="{col}" mask="url(#mk)"/>' + dot(108, 100, 21, col) + dot(160, 100, 21, col)


assets = {}   # nombre -> (svg, ancho_png, descripción, carpeta)
# --- Íconos
assets["icono"] = (wrap(200, 200, icon_g(0, 0, 1)), 2048, "Ícono con fondo negro redondeado (app, avatar cuadrado, sello).", "svg")
assets["icono-transparente"] = (wrap(189, 84, f'<g transform="translate(-2 -58)">{icon_g(0, 0, 1, bg=False)}</g>'), 2400, "Ícono sin fondo, para colocar sobre fotos y videos oscuros.", "svg")
assets["icono-transparente-claro"] = (wrap(189, 84, f'<g transform="translate(-2 -58)">{icon_g(0, 0, 1, bg=False, bc=DARK)}</g>'), 2400, "Ícono sin fondo con corchetes oscuros, para fondos claros.", "svg")
assets["monocromo-blanco"] = (wrap(189, 84, f'<g transform="translate(-2 -58)">{mono_icon("#ffffff")}</g>'), 2400, "Una sola tinta, blanco: marca de agua y créditos sobre video.", "svg")
assets["monocromo-negro"] = (wrap(189, 84, f'<g transform="translate(-2 -58)">{mono_icon("#000000")}</g>'), 2400, "Una sola tinta, negro: sellos, grabado e impresión.", "svg")

# --- Logos con nombre
def lockup(textcol):
    d, w = text_path("ProduAVX", EXB, 76, 148, 94, -1)
    return wrap(int(w) + 12, 140, icon_g(8, 10, .6) + f'<path d="{d}" fill="{textcol}"/>'), int(w) + 12
s, w = lockup(BR); assets["logo-horizontal"] = (s, 3200, "Logo principal: ícono + nombre. Para fondos oscuros.", "svg")
s, w = lockup(DARK); assets["logo-horizontal-claro"] = (s, 3200, "Logo principal con nombre oscuro, para fondos blancos o crema.", "svg")

def stacked(textcol, tagcol):
    d, w = text_path("ProduAVX", EXB, 58, 0, 0, -1); dt, wt = text_path("AUDIO · VIDEO · POST", BOLD, 15, 0, 0, 5)
    W = int(w) + 40
    d, _ = text_path("ProduAVX", EXB, 58, (W - w) / 2, 218, -1); dt, _ = text_path("AUDIO · VIDEO · POST", BOLD, 15, (W - wt) / 2, 246, 5)
    return wrap(W, 262, icon_g((W - 150) / 2, 6, .75) + f'<path d="{d}" fill="{textcol}"/><path d="{dt}" fill="{tagcol}"/>')
assets["logo-apilado"] = (stacked(BR, "#9393b0"), 2400, "Ícono arriba, nombre y lema debajo: portadas, tarjetas y créditos.", "svg")
assets["logo-apilado-claro"] = (stacked(DARK, "#5b5b78"), 2400, "Versión apilada para fondos claros.", "svg")

def orec(textcol, bc):
    d1, x1 = text_path("Pr", EXB, 80, 8, 98, -1); cx = x1 + 34
    d2, x2 = text_path("duAVX", EXB, 80, cx + 38, 98, -1)
    return wrap(int(x2) + 62, 140, f'<path d="{d1}" fill="{textcol}"/>' + brackets(cx - 30, 52, cx + 30, 106, arm=11, sw=5.5, c=bc) + rec(cx, 79, 19)
                + f'<path d="{d2}" fill="{textcol}"/>' + dot(x2 + 22, 90, 9, AMB) + dot(x2 + 46, 90, 9, GRN))
assets["logo-o-rec"] = (orec(BR, BR), 3200, "Versión de marca: el punto REC con corchetes es la «o» de Produ.", "svg")
assets["logo-o-rec-claro"] = (orec(DARK, DARK), 3200, "La «o» REC para fondos claros.", "svg")

# --- Favicon
fav = wrap(200, 200, icon_g(0, 0, 1)); assets["favicon"] = (fav, 512, "Favicon / ícono de app (SVG escalable).", "favicon")

# --- Plantillas sociales (1080x1080 y 1080x1920): logo apilado centrado exactamente sobre negro
def social(w, h, yc):
    """Ícono centrado en (w/2, yc); nombre y lema debajo, centrados."""
    sc = 3.0
    d, tw = text_path("ProduAVX", EXB, 120, 0, 0, -2); dt, tt = text_path("AUDIO · VIDEO · POST", BOLD, 30, 0, 0, 10)
    d, _ = text_path("ProduAVX", EXB, 120, (w - tw) / 2, yc + 190, -2); dt, _ = text_path("AUDIO · VIDEO · POST", BOLD, 30, (w - tt) / 2, yc + 265, 10)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{BG}"/>'
            + icon_g(w / 2 - 96.5 * sc, yc - 100 * sc, sc, bg=False) + f'<path d="{d}" fill="{BR}"/><path d="{dt}" fill="#9393b0"/></svg>\n')
assets["post-1080"] = (social(1080, 1080, 400), 1080, "Plantilla de publicación cuadrada 1080×1080 con logo centrado.", "instagram")
assets["historia-1080x1920"] = (social(1080, 1920, 800), 1080, "Plantilla de historia 1080×1920 con logo centrado.", "instagram")

manifest = []
for name, (svg, pw, desc, folder) in assets.items():
    open(os.path.join(KIT, "svg" if folder != "favicon" else "favicon", f"produavx-{name}.svg"), "w", encoding="utf-8").write(svg)
    manifest.append({"name": name, "svg": os.path.join("svg" if folder != "favicon" else "favicon", f"produavx-{name}.svg"), "png": os.path.join("png" if folder == "svg" else folder, f"produavx-{name}.png"), "width": pw, "desc": desc})
json.dump(manifest, open(os.path.join(KIT, "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok svg", len(assets))


if "--zip" in sys.argv:
    IG_SRC = os.path.join(OUT, "instagram")
    extra = [("avatar-2160.png", "Foto de perfil 2160×2160 (master).", "avatar-2160"), ("avatar.png", "Foto de perfil 1080×1080 (la que se sube a Instagram).", "avatar-1080"),
             ("avatar-720.png", "Foto de perfil 720×720.", "avatar-720"), ("destacado-rec.png", "Portada de destacado «REC» 1080×1920.", "destacado-rec"),
             ("destacado-audio.png", "Portada de destacado «Audio» 1080×1920.", "destacado-audio"), ("destacado-video.png", "Portada de destacado «Video» 1080×1920.", "destacado-video"),
             ("destacado-inicio.png", "Portada de destacado «Inicio» 1080×1920.", "destacado-inicio")]
    cards = []
    for src, desc, nm in extra:
        shutil.copy(os.path.join(IG_SRC, src), os.path.join(KIT, "instagram", f"produavx-{nm}.png"))
        cards.append(("Instagram", nm, desc, None, f"instagram/produavx-{nm}.png"))
    groups = {"Logos": ["logo-horizontal", "logo-horizontal-claro", "logo-apilado", "logo-apilado-claro", "logo-o-rec", "logo-o-rec-claro"],
              "Íconos y monocromo": ["icono", "icono-transparente", "icono-transparente-claro", "monocromo-blanco", "monocromo-negro"],
              "Favicon": ["favicon"], "Plantillas sociales": ["post-1080", "historia-1080x1920"]}
    man = {m["name"]: m for m in json.load(open(os.path.join(KIT, "manifest.json"), encoding="utf-8"))}
    sections = []
    for g, names in groups.items():
        sections.append((g, [(n, man[n]["desc"], man[n]["svg"] if not n.startswith(("post", "historia")) else None, man[n]["png"]) for n in names]))
    sections.append(("Instagram: perfil y destacados", [(nm, d, None, f"instagram/produavx-{nm}.png") for _, d, nm in extra]))
    light = lambda n: any(k in n for k in ("claro", "negro"))
    def card(n, d, svg, png):
        bg = "#f4ead6" if light(n) else "#14141c"
        tall = "destacado" in n or "historia" in n
        btn = (f'<a class="b" href="{svg}" download>SVG</a>' if svg else "") + f'<a class="b p" href="{png}" download>PNG</a>'
        return (f'<div class="c"><div class="pv" style="background:{bg}"><img src="{png}" alt="{n}" style="max-height:{190 if tall else 120}px"></div>'
                f'<h3>{n}</h3><p>{d}</p><div class="bt">{btn}</div></div>')
    html = "".join(f'<h2>{g}</h2><div class="g">' + "".join(card(*i) for i in items) + "</div>" for g, items in sections)
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kit de marca ProduAVX</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#000;color:#eeeefa;font:15px/1.5 Inter,system-ui,sans-serif;padding:32px 20px 60px}}main{{max-width:1100px;margin:0 auto}}
h1{{font-size:2rem;margin:0 0 6px}}h2{{margin:40px 0 14px;font-size:1.1rem;letter-spacing:.06em;text-transform:uppercase;color:#ffb300}}.lead{{color:#9393b0;margin:0 0 20px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}}.c{{background:#0e0e16;border:1px solid #23232f;border-radius:14px;padding:14px}}
.pv{{border-radius:10px;height:150px;display:grid;place-items:center;padding:10px;box-sizing:border-box}}.pv img{{max-width:100%;display:block}}
.c h3{{margin:12px 0 2px;font-size:.95rem}}.c p{{margin:0 0 10px;color:#9393b0;font-size:.82rem;min-height:36px}}.bt{{display:flex;gap:8px}}
.b{{flex:1;text-align:center;padding:8px 0;border-radius:8px;border:1px solid #3a3a4c;color:#eeeefa;text-decoration:none;font-weight:600;font-size:.85rem}}.b.p{{background:#ff3b30;border-color:#ff3b30;color:#fff}}
.all{{display:inline-block;margin:6px 0 4px;padding:12px 22px;border-radius:999px;background:#2ee66b;color:#04210f;font-weight:700;text-decoration:none}}
.sw{{display:flex;gap:12px;flex-wrap:wrap}}.sw div{{width:120px;border-radius:10px;overflow:hidden;border:1px solid #23232f;font-size:.8rem}}.sw i{{display:block;height:54px}}.sw span{{display:block;padding:6px 8px;background:#0e0e16}}</style></head><body><main>
<h1>Kit de marca ProduAVX</h1><p class="lead">Semáforo 2D · corchetes REC · fondo negro. Descarga cada archivo por separado (SVG vectorial o PNG de alta resolución) o el kit completo.</p>
<a class="all" href="../ProduAVX-kit-de-marca.zip" download>Descargar kit completo (ZIP)</a>{html}
<h2>Colores y tipografía</h2><div class="sw"><div><i style="background:#000"></i><span>Negro #000000</span></div><div><i style="background:#eeeefa"></i><span>Blanco roto #EEEEFA</span></div><div><i style="background:#ff3b30"></i><span>Rojo REC #FF3B30</span></div><div><i style="background:#ffb300"></i><span>Ámbar #FFB300</span></div><div><i style="background:#2ee66b"></i><span>Verde #2EE66B</span></div><div><i style="background:#12121f"></i><span>Tinta #12121F</span></div></div>
<p class="lead" style="margin-top:14px">Tipografía del nombre: Inter Display ExtraBold. Lema: Inter Display Bold, con espaciado amplio.</p></main></body></html>'''
    open(os.path.join(KIT, "index.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(KIT, "LEEME.txt"), "w", encoding="utf-8").write("""KIT DE MARCA PRODUAVX
======================
Concepto: semáforo 2D. Rojo = REC (con corchetes de visor y una mira de lente negra), ámbar = audio, verde = video.
Fondo de marca: negro puro.

CARPETAS
  svg/        Vectoriales: escalan sin perder calidad (impresión, rotulación, edición).
  png/        PNG de alta resolución con fondo transparente (2400-3200 px de ancho).
  instagram/  Foto de perfil (2160/1080/720), 4 portadas de destacados 1080x1920, plantillas de post e historia.
  favicon/    Favicon SVG y PNG 512/192/32/16.
  index.html  Catálogo con botones para descargar cada archivo.

COLORES
  Negro #000000 · Blanco roto #EEEEFA · Rojo REC #FF3B30 · Ámbar #FFB300 · Verde #2EE66B · Tinta #12121F
TIPOGRAFIA
  Nombre: Inter Display ExtraBold. Lema (AUDIO · VIDEO · POST): Inter Display Bold, espaciado amplio.

USO
  - Fondo oscuro: logo-horizontal / logo-apilado / icono-transparente.
  - Fondo claro: variantes "claro".
  - Una sola tinta: monocromo-blanco o monocromo-negro (marca de agua, sellos).
  - No usar el ícono por debajo de 24 px de alto; no cambiar el orden de los colores (rojo, ámbar, verde).
  - Instagram: subir avatar-1080 (o el master 2160); el logo ya trae margen para el recorte circular.
""")
    zp = os.path.join(ROOT, "ProduAVX-kit-de-marca.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(KIT):
            for f in sorted(fs):
                if f != "manifest.json":
                    full = os.path.join(dp, f); z.write(full, os.path.join("ProduAVX-kit-de-marca", os.path.relpath(full, KIT)))
    print("zip", os.path.getsize(zp) // 1024, "KB")
