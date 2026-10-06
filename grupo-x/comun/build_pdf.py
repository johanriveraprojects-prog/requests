import random, base64
random.seed(21)
W, H = 1123, 794
logo = open('../brand/logo.b64').read()

# ---- sparse galaxy: ~80% fewer than the reel (64 stars -> 13, 130 dust -> 26)
stars = []
for i in range(13):
    x, y = random.uniform(10, W - 10), random.uniform(8, H - 8)
    r = random.uniform(.9, 1.7); o = random.uniform(.45, .95)
    stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#eaf0ff" opacity="{o:.2f}"/>')
    if i < 2:   # the two big sparkles, small and sharp like the reel
        x, y = [(96, 172), (1032, 178)][i]; L = 7
        stars.append(f'<g stroke="#f0f4ff" stroke-width=".8" opacity=".85"><line x1="{x-L:.1f}" y1="{y:.1f}" x2="{x+L:.1f}" y2="{y:.1f}"/><line x1="{x:.1f}" y1="{y-L:.1f}" x2="{x:.1f}" y2="{y+L:.1f}"/></g>')
for i in range(26):
    x, y = random.uniform(5, W - 5), random.uniform(5, H - 5)
    stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(.5,.9):.2f}" fill="#c8d2ff" opacity="{random.uniform(.18,.4):.2f}"/>')
stars = '\n'.join(stars)

AMB, BLU = '#e3a857', '#86a8ff'
html = f'''<!doctype html><meta charset="utf-8"><title>Grupo X Team X</title>
<style>
{open('fonts-local.css').read().replace('url(fonts/', 'url(file://' + __import__('os').getcwd().replace('/pdf','') + '/fonts/')}
@page {{ size: 297mm 210mm; margin: 0 }}
html,body{{margin:0;background:#000}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#000;color:#f2f2f2;font-family:"Instrument Sans",system-ui,sans-serif}}
.neb{{position:absolute;inset:0;background:radial-gradient(520px 340px at 78% 22%,rgba(120,120,190,.10),transparent 70%),radial-gradient(560px 380px at 14% 80%,rgba(100,130,170,.08),transparent 70%)}}
svg{{position:absolute;left:0;top:0}}
.abs{{position:absolute}}
.mono{{font-family:"JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.18em;color:#9c9c9c}}
.hub{{left:331px;top:14px;width:461px;height:140px;text-align:center}}
.hub img{{width:62px;filter:drop-shadow(0 0 14px rgba(255,255,255,.4))}}
.hub h1{{margin:6px 0 0;font:800 31px/1 "Bricolage Grotesque",sans-serif;letter-spacing:-.02em}}
.hub .sub{{margin-top:7px;font-size:13.5px;color:#e6e6e6}}
.hub .sub2{{margin-top:3px;font-size:11px}}
.card{{border:1px solid var(--c);border-radius:14px;background:linear-gradient(160deg,rgba(255,255,255,.055),rgba(255,255,255,.015));padding:15px 20px;box-sizing:border-box;box-shadow:0 0 30px -10px var(--c)}}
.card .tag{{font-size:10px;color:var(--c)}}
.card h2{{margin:5px 0 2px;font:800 34px/1 "Bricolage Grotesque",sans-serif;letter-spacing:-.025em}}
.card h2 b{{color:var(--c);font-weight:800}}
.card .rubro{{font-size:13.5px;color:#f0f0f0;font-weight:600}}
.card ul{{margin:9px 0 0;padding:0;list-style:none;font-size:12.5px;line-height:1.38;color:#cfcfcf}}
.card li{{position:relative;padding-left:15px;margin-top:3px}} .card li:before{{content:"";position:absolute;left:0;top:.55em;width:7px;height:2px;background:var(--c)}}
.pill{{border:1px solid #555;border-radius:20px;background:#000;font-size:10px;padding:4px 10px;text-align:center;color:#d9d9d9}}
.net{{border:1px solid rgba(255,255,255,.35);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02))}}
.net .t{{left:18px;top:9px;font:800 19px/1 "Bricolage Grotesque",sans-serif}} .net .t span{{font:400 11.5px "Instrument Sans";color:#b8b8b8;margin-left:10px;letter-spacing:0}}
.mod{{border:1px solid #4a4a4a;border-radius:10px;background:rgba(0,0,0,.45);padding:9px 12px;box-sizing:border-box}}
.mod h3{{margin:0;font:700 13.5px/1.1 "Instrument Sans";color:#fff}} .mod p{{margin:4px 0 0;font-size:11.5px;line-height:1.3;color:#bdbdbd}}
.chip{{border:1px solid #6b6b6b;border-radius:12px;background:rgba(255,255,255,.04);padding:10px 16px;box-sizing:border-box;font-size:12.2px;line-height:1.32;color:#d6d6d6}}
.chip b{{display:block;font:800 17px/1 "Bricolage Grotesque";color:#fff;margin-bottom:4px}}
.foot{{left:0;width:{W}px;text-align:center;font-size:11.5px;color:#a8a8a8}}
</style>
<div class="page">
<div class="neb"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{stars}</svg>

<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
 <defs>
  <filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
  <linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{AMB}"/></linearGradient>
  <linearGradient id="gB" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{BLU}"/></linearGradient>
  <marker id="arr" markerWidth="7" markerHeight="7" refX="5.5" refY="3.5" orient="auto-start-reverse"><path d="M0 0L7 3.5L0 7z" fill="#e8e8e8"/></marker>
 </defs>
 <!-- hub -> brands -->
 <path d="M561 174 C561 204 263 196 263 228" fill="none" stroke="url(#gA)" stroke-width="1.6"/>
 <path d="M561 174 C561 204 860 196 860 228" fill="none" stroke="url(#gB)" stroke-width="1.6"/>
 <!-- brand <-> brand (same visual DNA) -->
 <line x1="478" y1="322" x2="645" y2="322" stroke="#8a8a8a" stroke-width="1.2" stroke-dasharray="4 4" marker-start="url(#arr)" marker-end="url(#arr)"/>
 <!-- brands <-> network -->
 <line x1="263" y1="416" x2="263" y2="458" stroke="{AMB}" stroke-width="1.6" marker-start="url(#arr)" marker-end="url(#arr)"/>
 <line x1="860" y1="416" x2="860" y2="458" stroke="{BLU}" stroke-width="1.6" marker-start="url(#arr)" marker-end="url(#arr)"/>
 <!-- inside network -->
 <line x1="424" y1="531" x2="448" y2="531" stroke="#bdbdbd" stroke-width="1.2"/><line x1="698" y1="531" x2="722" y2="531" stroke="#bdbdbd" stroke-width="1.2"/>
 <!-- network -> partners -->
 <path d="M561 584 C561 604 361 598 361 616" fill="none" stroke="#9c9c9c" stroke-width="1.2"/><line x1="561" y1="584" x2="561" y2="616" stroke="#9c9c9c" stroke-width="1.2"/><path d="M561 584 C561 604 761 598 761 616" fill="none" stroke="#9c9c9c" stroke-width="1.2"/>
 <!-- team x <-> grupo x -->
 <line x1="552" y1="716" x2="571" y2="716" stroke="#d0d0d0" stroke-width="1.4"/>
 <!-- glowing nodes -->
 <g fill="#fff"><circle cx="561" cy="174" r="4"/><circle cx="263" cy="228" r="4" fill="{AMB}"/><circle cx="860" cy="228" r="4" fill="{BLU}"/><circle cx="561" cy="322" r="3.5"/>
  <circle cx="263" cy="437" r="3.5" fill="{AMB}"/><circle cx="860" cy="437" r="3.5" fill="{BLU}"/><circle cx="561" cy="584" r="3.5"/></g>
 <g filter="url(#gl)" opacity=".9"><circle cx="561" cy="174" r="6" fill="#fff"/><circle cx="263" cy="228" r="6" fill="{AMB}"/><circle cx="860" cy="228" r="6" fill="{BLU}"/></g>
 <g fill="#000" stroke="#d0d0d0" stroke-width="1.3"><circle cx="361" cy="626" r="9"/><circle cx="561" cy="626" r="9"/><circle cx="761" cy="626" r="9"/></g>
 <g fill="#d0d0d0"><circle cx="361" cy="626" r="2.6"/><circle cx="561" cy="626" r="2.6"/><circle cx="761" cy="626" r="2.6"/></g>
</svg>

<div class="abs mono" style="left:44px;top:22px;font-size:10px">Concepto · v1</div>
<div class="abs mono" style="right:44px;top:22px;font-size:10px">Documento para compartir</div>

<div class="abs hub"><img src="data:image/png;base64,{logo}" alt=""><h1>GRUPO X · TEAM X</h1>
 <div class="sub">Un equipo trabajando con calidad y organización.</div>
 <div class="sub2 mono" style="letter-spacing:.12em;font-size:9.5px">Entidad que controla los proyectos por separado en dos rubros</div></div>

<div class="abs card" style="--c:{AMB};left:48px;top:230px;width:430px;height:188px">
 <div class="tag mono">Rubro 1</div><h2>Constru<b>X</b></h2><div class="rubro">Construcción y obras civiles n.c.p.</div>
 <ul><li>Construcción de casas y remodelaciones de espacios.</li><li>Terrenos, apartamentos, viviendas y locales.</li></ul></div>
<div class="abs card" style="--c:{BLU};left:645px;top:230px;width:430px;height:188px">
 <div class="tag mono">Rubro 2</div><h2>Produ<b>AVX</b></h2><div class="rubro">Producción de audio y video</div>
 <ul><li>Escenas únicas de video y audio.</li><li>Foco y detalle en la calidad de producción y postproducción.</li></ul></div>
<div class="abs pill" style="left:501px;top:308px;width:120px">mismo ADN visual<br><span style="color:#8d8d8d">identidad propia por rubro</span></div>

<div class="abs pill" style="left:272px;top:430px;width:100px;border-color:{AMB}55">datos · documentos</div>
<div class="abs pill" style="left:869px;top:430px;width:100px;border-color:{BLU}55">datos · documentos</div>

<div class="abs net" style="left:150px;top:460px;width:823px;height:124px">
 <div class="abs t">.Network<span>ecosistema organizado y compartido</span></div>
 <div class="abs mod" style="left:24px;top:40px;width:250px;height:72px"><h3>Base de datos compartida</h3><p>Documentos organizados en un mismo lugar.</p></div>
 <div class="abs mod" style="left:298px;top:40px;width:250px;height:72px"><h3>Estadísticas</h3><p>Para pautar entre sí y con marcas aliadas.</p></div>
 <div class="abs mod" style="left:572px;top:40px;width:227px;height:72px"><h3>Herramientas tecnológicas</h3><p>Agilizan el CoWork entre equipos.</p></div>
</div>

<div class="abs" style="left:211px;top:640px;width:700px;text-align:center;font-size:11.5px;color:#cfcfcf">Partners · marcas conocidas en redes sociales</div>

<div class="abs mono" style="left:0;width:{W}px;text-align:center;top:668px;font-size:10px;color:#bdbdbd">¿Por qué Grupo X Team X?</div>
<div class="abs chip" style="left:150px;top:686px;width:396px;height:68px"><b>Team X</b>Equipo bilingüe: bases en inglés para mayor agilidad con inversión del extranjero.</div>
<div class="abs chip" style="left:577px;top:686px;width:396px;height:68px"><b>Grupo X</b>Equipo nativo, con el dominio y la cercanía del lugar.</div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="pointer-events:none"><circle cx="561.5" cy="720" r="11" fill="#000" stroke="#d0d0d0" stroke-width="1.3"/><text x="561.5" y="724.5" text-anchor="middle" font-size="13" fill="#fff" font-family="Instrument Sans">⇄</text></svg>

<div class="abs foot" style="top:766px">Conectar personas y crear, en equipo, proyectos que se construyen con propósito.</div>
</div>'''
open('pdf/grupo-x-team-x.html', 'w').write(html)
print('html ok', len(html))
