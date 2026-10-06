"""Logo AX/AVX como semáforo: rojo (REC), ámbar (listo), verde (en vivo). Cuatro formas de usar los tonos."""
import os, json
from build_logo import OUT, text_path, A_OUT, A_HOLE, X_OUT

RED, AMB, GRN = "#ff3b30", "#ffb300", "#2ee66b"
INK = {RED: "#3d0805", AMB: "#3d2600", GRN: "#053a1a"}
HOUSE, EDGE, BG = "#14141f", "#2c2c40", "#0b0b14"
M = os.path.join(OUT, "semaforo"); os.makedirs(M, exist_ok=True)
face = lambda pts: "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"

DEFS = "".join(
    f'<radialGradient id="l{i}" cx=".38" cy=".32" r=".85"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{c}"/><stop offset="1" stop-color="{lo}"/></radialGradient>'
    for i, (c, hi, lo) in enumerate(((RED, "#ff9a90", "#a3140c"), (AMB, "#ffe08a", "#b87a00"), (GRN, "#a8ffc8", "#12a84a"))))
DEFS += f'<linearGradient id="tl" gradientUnits="userSpaceOnUse" x1="14" y1="0" x2="188" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset=".5" stop-color="{AMB}"/><stop offset="1" stop-color="{GRN}"/></linearGradient>'


def letter(ch, cx, cy, size, color):
    """Letra convertida a trazos, centrada en (cx, cy)."""
    _, w = text_path(ch, "InterDisplay-ExtraBold.otf", size, 0, 0)
    d, _ = text_path(ch, "InterDisplay-ExtraBold.otf", size, cx - w / 2, cy + size * .36)
    return f'<path d="{d}" fill="{color}"/>'


def light(i, cx, cy, r, ch, c):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="{c}" opacity=".16"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#l{i})" stroke="{BG}" stroke-width="3"/>'
            f'<ellipse cx="{cx - r * .3}" cy="{cy - r * .45}" rx="{r * .4}" ry="{r * .2}" fill="#fff" opacity=".35"/>' + letter(ch, cx, cy, r * 1.5, INK[c]))


cols = [(RED, "A"), (AMB, "V"), (GRN, "X")]
v = {}
# 1 · Semáforo vertical AVX
v[1] = ("Semáforo AVX", "Tres luces apiladas, cada una con una letra: A roja, V ámbar, X verde. Se lee AVX.",
        f'<rect x="50" y="6" width="100" height="188" rx="28" fill="{HOUSE}" stroke="{EDGE}" stroke-width="4"/>'
        + "".join(f'<path d="M{x - 30} {y - 18}Q{x} {y - 40} {x + 30} {y - 18}" fill="none" stroke="{BG}" stroke-width="6" stroke-linecap="round"/>' for x, y in ((100, 46), (100, 100), (100, 154)))
        + "".join(light(i, 100, y, 21, ch, c) for i, ((c, ch), y) in enumerate(zip(cols, (52, 100, 148)))))
# 2 · Semáforo horizontal AVX (se lee como wordmark; ideal de banner)
v[2] = ("Semáforo horizontal", "Misma idea en horizontal: A · V · X como tres luces; funciona como banner y avatar ancho.",
        f'<rect x="6" y="54" width="188" height="92" rx="34" fill="{HOUSE}" stroke="{EDGE}" stroke-width="4"/>'
        + "".join(light(i, x, 100, 22, ch, c) for i, ((c, ch), x) in enumerate(zip(cols, (46, 100, 154)))))
# 3 · AX + semáforo diminuto (sutil): letras planas y una mini luz de tres tonos junto a la X
mini = (f'<rect x="162" y="14" width="26" height="70" rx="10" fill="{HOUSE}" stroke="{EDGE}" stroke-width="2.5"/>'
        + "".join(f'<circle cx="175" cy="{y}" r="6.5" fill="{c}"/>' for y, c in ((30, RED), (49, AMB), (68, GRN))))
v[3] = ("AX + mini semáforo", "Monograma AX plano crema; un semáforo diminuto como detalle (sustituye al punto rojo/verde).",
        f'<rect width="200" height="200" rx="46" fill="{BG}"/><g transform="translate(86 112) scale(.74) translate(-101 -96)"><path d="{face(A_OUT)} {face(A_HOLE)}" fill="#fff1d6" fill-rule="evenodd"/><path d="{face(X_OUT)}" fill="#fff1d6"/></g>' + mini)
# 4 · Tonos de semáforo en las letras: A roja→ámbar, X ámbar→verde
v[4] = ("Letras con tonos", "AX plano con un solo degradado rojo → ámbar → verde: el semáforo está en el color.",
        f'<rect width="200" height="200" rx="46" fill="{BG}"/><g transform="translate(100 106) scale(.82) translate(-101 -96)"><path d="{face(A_OUT)} {face(A_HOLE)}" fill="url(#tl)" fill-rule="evenodd"/><path d="{face(X_OUT)}" fill="url(#tl)"/></g>')

for n, (name, desc, body) in v.items():
    open(os.path.join(M, f"v{n}.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX semáforo {n}"><defs>{DEFS}</defs>{body}</svg>\n')
json.dump({n: [a, b] for n, (a, b, _) in v.items()}, open(os.path.join(M, "variantes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(v))
