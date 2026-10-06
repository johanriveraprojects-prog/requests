"""Tres direcciones del monograma AX, derivadas de la investigación de tendencias (ver CLAUDE.md)."""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img", "concepts")
os.makedirs(OUT, exist_ok=True)
CY, VI, BG = "#46e0ff", "#9a6bff", "#0b0b1c"
GRAD = f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="30" y1="40" x2="175" y2="160"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>'

def svg(defs, body, name):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ProduAVX AX"><defs>{GRAD}{defs}</defs>'
        f'<circle cx="100" cy="100" r="98" fill="{BG}"/>{body}</svg>\n')

# A · Sólido de avatar: letras gruesas y planas, máxima lectura a 40 px (perfil circular de Instagram)
svg("", f'''<g transform="translate(100 102) scale(.88) translate(-100 -102)" fill="none" stroke="url(#g)" stroke-width="21" stroke-linejoin="miter">
  <path d="M32 152L66 54L100 152"/><path d="M48 122H84" stroke-width="15"/>
  <path d="M116 54L172 152M172 54L116 152"/></g>''', "ax-a-solido.svg")

# B · Ligadura superpuesta: A cian y X violeta se solapan; la intersección brilla (tendencia: caracteres superpuestos)
svg(f'<mask id="ma"><g fill="none" stroke="#fff" stroke-width="20"><path d="M26 152L60 54L94 152"/><path d="M42 122H78" stroke-width="13"/></g></mask>',
    f'''<g transform="translate(106 102) scale(.9) translate(-92 -102)" fill="none">
  <g stroke="{CY}" stroke-width="20"><path d="M26 152L60 54L94 152"/><path d="M42 122H78" stroke-width="13"/></g>
  <g stroke="{VI}" stroke-width="20" opacity=".95"><path d="M76 54L134 152M134 54L76 152" /></g>
  <g stroke="#eaf9ff" stroke-width="20" mask="url(#ma)"><path d="M76 54L134 152M134 54L76 152"/></g></g>''', "ax-b-ligadura.svg")

# C · Monolínea moderna: trazo único redondeado y degradado tonal (neo-minimalismo cálido)
svg("", f'''<g transform="translate(100 102) scale(.9) translate(-100 -102)" fill="none" stroke="url(#g)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round">
  <path d="M30 152L64 54L98 152"/><path d="M45 122H83"/>
  <path d="M116 54L172 152M172 54L116 152"/></g>''', "ax-c-monolinea.svg")
print("ok")
