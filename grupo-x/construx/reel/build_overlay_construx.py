"""Genera 15s/overlay.html (ConstruX) a partir del overlay base: reescribe solo las 4 escenas y el acento ámbar."""
import re, pathlib
here = pathlib.Path(__file__).parent
src = (here / "overlay_VIEJO_nicho.html").read_text(encoding="utf-8")
logo = re.search(r'<img class="logo sm pop" alt="Logo de Grupo X" src="([^"]+)">', src).group(1)

scenes = f'''<section class="scene center" data-name="Gancho" data-dur="3600">
        <div class="brand rise" style="--d:.1s">ConstruX · Grupo X Team X</div>
        <h2 class="hook"><span class="dl es" data-t="¿Tienes el terreno|y no sabes por dónde|empezar?" data-s="0.3" data-d="0.6"></span><span class="dl en" data-t="You own the land.|Where do you start?" data-s="0.55" data-d="0.6"></span></h2>
        <div class="promise rise" style="--d:1.8s"><span class="dl es" data-t="Tu casa, por etapas." data-s="1.8" data-d="0.6"></span><div class="dl en" data-t="Your home, step by step." data-s="2.05" data-d="0.6"></div></div>
      </section>

      <section class="scene" data-name="Problema" data-dur="3600">
        <div class="tag rise">El problema</div>
        <h2 class="slow" style="--d:0s;font-size:8.2cqw"><span class="dl es" data-t="Una obra sin plan|sale cara." data-s="0" data-d="0.8"></span><span class="dl en" data-t="A build without a plan|gets costly." data-s="0.4" data-d="0.8"></span></h2>
      </section>

      <section class="scene" data-name="Método" data-dur="4500">
        <div class="tag rise">El método</div>
        <div class="steps">
          <div class="step" style="--d:0s;--n:1.8s"><b>01</b><div><h3><span class="dl es" data-t="Cimientos" data-s="0" data-d="0.5"></span></h3><p class="dl sub" data-t="Empezamos firmes" data-s="0.15" data-d="0.5"></p><p class="dl en" data-t="Foundation · We start solid" data-s="0.3" data-d="0.5"></p></div></div>
          <div class="step" style="--d:1.8s;--n:3.6s"><b>02</b><div><h3><span class="dl es" data-t="Estructura" data-s="1.8" data-d="0.5"></span></h3><p class="dl sub" data-t="Madera y piedra, bien hechas" data-s="1.95" data-d="0.5"></p><p class="dl en" data-t="Structure · Wood and stone, done right" data-s="2.1" data-d="0.5"></p></div></div>
          <div class="step last" style="--d:3.6s"><b>03</b><div><h3><span class="dl es" data-t="Acabados" data-s="3.6" data-d="0.5"></span></h3><p class="dl sub" data-t="Los detalles que hacen hogar" data-s="3.75" data-d="0.5"></p><p class="dl en" data-t="Finishes · The details that make it home" data-s="3.9" data-d="0.5"></p></div></div>
        </div>
      </section>

      <section class="scene center" data-name="Cierre" data-dur="3300">
        <img class="logo sm pop" alt="Logo de Grupo X" src="{logo}">
        <h2 class="slow" style="--d:.9s;font-size:8.3cqw"><span class="dl es" data-t="ConstruX|Tu casa, hecha realidad." data-s="0.9" data-d="0.7"></span><span class="dl en" data-t="Your home, made real." data-s="1.2" data-d="0.7"></span></h2>
        <div class="pill rise" style="--d:1.8s"><span class="dl es" data-t="Escríbenos para tu proyecto" data-s="1.8" data-d="0.5"></span><span class="dl en" data-t="Message us for your project" data-s="1.95" data-d="0.5"></span></div>
        <div class="brand rise" style="--d:2.4s;font-size:2.7cqw"><span class="dl es" data-t="Grupo X · Team X" data-s="2.4" data-d="0.4"></span></div>
      </section>
'''
a = src.index('<section class="scene center" data-name="Gancho"')
b = src.index('    </div>\n  </div>\n\n  <div class="ctl">')
out = src[:a] + scenes + src[b:]
out = out.replace('var field = document.getElementById("field"), seed = 5;', 'var field = document.getElementById("field"), seed = 5; if (!field) return;')
out = out.replace('<title>Grupo X Reel</title>', '<title>ConstruX Reel</title>')
out = out.replace('</style>', '''.step b { color: #f0b660 !important; text-shadow: 0 0 1.2cqw rgba(0,0,0,.85), 0 .2cqw 1cqw rgba(0,0,0,.9) !important; }
.tag { color: #fff !important; }
.pill { border-color: #f0b660; color: #fff !important; background: rgba(10,10,10,.45); }
.promise .dl.es { color: #ffd08a; }
</style>''', 1)
(here / "15s").mkdir(exist_ok=True)
(here / "15s" / "overlay.html").write_text(out, encoding="utf-8")
print("ok", len(out))
