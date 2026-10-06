"""AX con un auto (A) y un dron (X) disimulados en las letras. Cuatro niveles de discreción."""
import os, json
from build_logo import OUT, A_OUT, A_HOLE, X_OUT

CY, VI, BG = "#46e0ff", "#9a6bff", "#0b0b1c"
M = os.path.join(OUT, "vehiculos"); os.makedirs(M, exist_ok=True)
face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
FIT = 'translate(100 104) scale(.8) translate(-101 -96)'
sq = f'<rect width="200" height="200" rx="46" fill="{BG}"/>'
Ablock = f'<path d="{face(A_OUT)} {face(A_HOLE)}" fill="{CY}" fill-rule="evenodd"/>'
Xblock = f'<path d="{face(X_OUT)}" fill="{VI}"/>'
ring = lambda x, y, r, c, sw=4.5: f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BG}" stroke="{c}" stroke-width="{sw}"/>'
LED = lambda x, y, r=4.4: (f'<clipPath id="led"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath><g clip-path="url(#led)"><rect x="{x - r}" y="{y - r}" width="{r}" height="{2 * r}" fill="#ff3b3b"/>'
                          f'<rect x="{x}" y="{y - r}" width="{r}" height="{2 * r}" fill="#2ee66b"/></g>')
TIPS_X = [(125, 44), (175, 44), (175, 148), (125, 148)]   # puntas de la X = hélices
FEET_A = [(27, 150), (105, 150)]                           # pies de la A = ruedas

v = {}
# 1 · Sutil: ruedas en los pies de la A y aros de hélice en las puntas de la X
v[1] = ("Sutil", "Solo ruedas (A) y aros de hélice (X): se lee AX; el guiño aparece al mirar de cerca.",
        sq + f'<g transform="{FIT}">{Ablock}{Xblock}' + "".join(ring(x, y, 10, CY) for x, y in FEET_A) + "".join(ring(x, y, 11, VI) for x, y in TIPS_X) + '</g>')
# 2 · Visible: A con chasis y ventanas (auto de frente); X con cuerpo central y luz roja/verde de navegación
v[2] = ("Visible", "A con chasis y ruedas (auto); X con cuerpo central, hélices y luz de navegación roja/verde.",
        sq + f'<g transform="{FIT}">{Ablock}<rect x="27" y="143" width="78" height="8" fill="{CY}"/>{Xblock}'
        + "".join(ring(x, y, 10, CY) for x, y in FEET_A) + "".join(ring(x, y, 11, VI) for x, y in TIPS_X)
        + f'<rect x="138" y="88" width="24" height="16" rx="5" fill="{BG}" stroke="{VI}" stroke-width="4"/>{LED(150, 96)}</g>')
# 3 · Oculto: siluetas diminutas en los espacios vacíos (auto en el hueco de la A, dron en la muesca de la X)
car = (f'<path d="M55 103L55 98Q55 95.5 58 95.5L60 95.5L63 90.5L69 90.5L72 95.5L75 95.5Q77 95.5 77 98L77 103Z" fill="{CY}"/>'
       f'<circle cx="60.5" cy="103" r="2.6" fill="{CY}" stroke="{BG}" stroke-width="1.2"/><circle cx="71.5" cy="103" r="2.6" fill="{CY}" stroke="{BG}" stroke-width="1.2"/>')
drone = (f'<g stroke="{VI}" stroke-width="1.8" stroke-linecap="round"><path d="M142.5 47L147.5 52M157.5 47L152.5 52M147 58L148.8 55M153 58L151.2 55"/></g>'
         f'<rect x="147" y="51" width="6" height="4" rx="1.4" fill="{VI}"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="2.1" fill="none" stroke="{VI}" stroke-width="1.3"/>' for x, y in ((141, 46), (159, 46), (146, 59), (154, 59))))
v[3] = ("Oculto", "Sin ruedas ni aros: un auto diminuto dentro de la A y un dron en la muesca de la X.",
        sq + f'<g transform="{FIT}">{Ablock}{Xblock}{car}{drone}</g>')
# 4 · Monolínea: trazo redondeado; ruedas en los pies de la A y hélices en las puntas de la X
def stroke(d, c, sw=10):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
v[4] = ("Monolínea", "Línea redondeada: A de auto con ruedas en los pies; X de dron con hélices en cada punta.",
        sq + f'<g transform="translate(100 104) scale(.84) translate(-100 -102)">' + stroke("M32 144L64 58L96 144", CY) + stroke("M46 118H82", CY, 8)
        + "".join(ring(x, 150, 9, CY, 5) for x in (32, 96)) + stroke("M118 66L168 138M168 66L118 138", VI)
        + "".join(ring(x, y, 9, VI, 5) for x, y in ((118, 66), (168, 66), (168, 138), (118, 138)))
        + f'<rect x="131" y="94" width="24" height="16" rx="5" fill="{BG}" stroke="{VI}" stroke-width="4"/>{LED(143, 102)}</g>')

for n, (name, desc, body) in v.items():
    open(os.path.join(M, f"v{n}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX auto y dron {n}">{body}</svg>\n')
json.dump({n: [a, b] for n, (a, b, _) in v.items()}, open(os.path.join(M, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(v))
