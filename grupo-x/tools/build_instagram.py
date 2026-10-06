"""Kit Instagram del semáforo 2D: avatar (ícono [●]●●) y 4 portadas de destacados. SVG -> PNG con export_instagram.js"""
import os
from build_semaforo3 import brackets, dot, RED, AMB, GRN, BR, BG
from build_logo import OUT

IG = os.path.join(OUT, "instagram"); os.makedirs(IG, exist_ok=True)


def ig(name, w, h, body):
    open(os.path.join(IG, name), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n')


# Avatar 1080: el ícono de la variante 2 centrado, ~62 % del ancho (zona segura del recorte circular)
s = 3.96
ig("avatar.svg", 1080, 1080, f'<g transform="translate({540 - 96.5 * s:.1f} {540 - 100 * s:.1f}) scale({s})">'
   + brackets(12, 66, 80, 134) + dot(46, 100, 21, RED) + dot(108, 100, 21, AMB) + dot(160, 100, 21, GRN) + '</g>')

# Portadas 1080x1920: una luz del semáforo por portada (el recorte circular toma el centro)
c = (540, 960)
ink = {"rec": "#3d0805", "audio": "#3d2600", "video": "#053a1a"}
wave = "".join(f'<rect x="{540 - 112 + i * 56}" y="{960 - h / 2}" width="36" height="{h}" rx="18" fill="{ink["audio"]}"/>' for i, h in enumerate((70, 150, 230, 150, 70)))
ig("destacado-rec.svg", 1080, 1920, brackets(290, 710, 790, 1210, arm=100, sw=24) + dot(*c, 170, RED) + f'<circle cx="540" cy="960" r="62" fill="{ink["rec"]}"/>')
ig("destacado-audio.svg", 1080, 1920, dot(*c, 220, AMB) + wave)
ig("destacado-video.svg", 1080, 1920, dot(*c, 220, GRN) + f'<path d="M485 860L485 1060L650 960Z" fill="{ink["video"]}" stroke="{ink["video"]}" stroke-width="30" stroke-linejoin="round"/>')
ig("destacado-inicio.svg", 1080, 1920, f'<g transform="translate({540 - 96.5 * 4.4:.1f} {960 - 100 * 4.4:.1f}) scale(4.4)">'
   + brackets(12, 66, 80, 134) + dot(46, 100, 21, RED) + dot(108, 100, 21, AMB) + dot(160, 100, 21, GRN) + '</g>')
print("ok instagram")
