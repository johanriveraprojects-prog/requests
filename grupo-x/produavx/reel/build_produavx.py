"""Genera 15s/reel.html (ProduAVX, fondo galaxia + gráficos en movimiento) desde la base del reel anterior."""
import re, pathlib
here = pathlib.Path(__file__).parent
src = (here / "base_nicho.html").read_text(encoding="utf-8")
logo = re.search(r'<img class="logo sm pop" alt="Logo de Grupo X" src="([^"]+)">', src).group(1)

# quitar el bloque de "construction overlay" (fondo transparente) para recuperar la galaxia
a = src.index('/* construction overlay')
b = src.index('</style>', a)
src = src[:a] + src[b:]

bars = []
import math
for i in range(30):
    h = .35 + .65 * abs(math.sin(i * 1.7 + 1))
    p = 0.9 + (i * 37 % 7) * .13
    bars.append(f'<i style="--h:{h:.2f};--p:{p:.2f}s;--o:-{(i*53%10)/10:.1f}s"></i>')
bars = "".join(bars)

css = '''
/* ProduAVX: azul, gráficos en movimiento */
.step b, .tag { color: #86a8ff !important; }
.pill { border-color: #86a8ff; color: #dbe5ff !important; }
.promise .dl.es { color: #bcd0ff; }
.brand { color: #a9bff5 !important; }
.iris { position: absolute; left: 50%; bottom: 25cqw; width: 36cqw; height: 36cqw; margin-left: -18cqw; }
.iris i { position: absolute; inset: 0; border-radius: 50%; border: .45cqw solid rgba(134,168,255,.6); opacity: 0; }
.iris i:nth-child(2) { inset: 5cqw; border-color: rgba(134,168,255,.4); }
.iris i:nth-child(3) { inset: 10cqw; border-style: dashed; border-color: rgba(134,168,255,.7); }
.iris b { position: absolute; left: 50%; top: 50%; width: 9cqw; height: 9cqw; margin: -4.5cqw 0 0 -4.5cqw; border-radius: 50%; background: radial-gradient(circle, #fff 0%, #9db8ff 35%, rgba(134,168,255,0) 72%); opacity: 0; }
.on .iris i:nth-child(1) { animation: irisin 1.6s cubic-bezier(.2,.8,.2,1) .2s both; }
.on .iris i:nth-child(2) { animation: irisin 1.6s cubic-bezier(.2,.8,.2,1) .45s both; }
.on .iris i:nth-child(3) { animation: irisin 1.6s cubic-bezier(.2,.8,.2,1) .7s both, spin 9s linear 2.3s infinite; }
.on .iris b { animation: irisin 1.2s ease-out 1.2s both, pulse 2.4s ease-in-out 2.4s infinite; }
@keyframes irisin { from { opacity: 0; transform: scale(.15); } to { opacity: 1; transform: scale(1); } }
@keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
@keyframes pulse { 50% { transform: scale(1.25); } }

.clap { width: 66cqw; margin-top: 16cqw; }
.clap .bar { height: 11cqw; border-radius: 1.2cqw 1.2cqw 0 0; background: repeating-linear-gradient(115deg, #f2f2f2 0 6cqw, #0a0a0a 6cqw 12cqw); border: .4cqw solid #f2f2f2; transform-origin: 0 100%; }
.clap .body { border: .4cqw solid #f2f2f2; border-top: 0; padding: 5cqw 4.5cqw; display: grid; gap: 2cqw; background: rgba(255,255,255,.04); }
.clap .body span { font-family: var(--f-mono); letter-spacing: .14em; text-transform: uppercase; font-size: 3cqw; color: #bcd0ff; }
.clap .body strong { font-family: var(--f-display); font-size: 6.6cqw; line-height: 1; letter-spacing: -.01em; }
.on .clap { animation: rise .6s cubic-bezier(.2,.8,.2,1) .4s both; }
.on .clap .bar { animation: clapbar .5s cubic-bezier(.5,0,.2,1.4) 1.5s both; }
@keyframes clapbar { from { transform: rotate(-11deg); } to { transform: rotate(0); } }

.wave { display: flex; align-items: center; gap: .8cqw; height: 15cqw; width: 100%; margin-top: 3cqw; }
.wave i { flex: 1; height: 100%; border-radius: 1cqw; background: linear-gradient(180deg, #bcd0ff, #86a8ff); transform: scaleY(.2); opacity: .9; }
.on .wave i { animation: wv var(--p) ease-in-out var(--o) infinite; }
@keyframes wv { 0%, 100% { transform: scaleY(.18); } 50% { transform: scaleY(var(--h)); } }
.tl { position: relative; display: flex; gap: .8cqw; width: 100%; height: 9cqw; margin-top: 2cqw; }
.tl i { display: block; height: 100%; border-radius: 1cqw; opacity: 0; }
.tl i:nth-child(1) { flex: 3; background: #86a8ff; }
.tl i:nth-child(2) { flex: 4; background: #bcd0ff; }
.tl i:nth-child(3) { flex: 3; background: #5b7fe0; }
.on .tl i:nth-child(1) { animation: rise .5s ease-out 0s both; }
.on .tl i:nth-child(2) { animation: rise .5s ease-out 1.8s both; }
.on .tl i:nth-child(3) { animation: rise .5s ease-out 3.6s both; }
.tl u { position: absolute; top: -1.5cqw; bottom: -1.5cqw; width: .6cqw; background: #fff; box-shadow: 0 0 2cqw #fff; left: 0; }
.on .tl u { animation: ph 4.4s linear .1s both; }
@keyframes ph { from { left: 0; } to { left: 100%; } }
.scene * { text-shadow: none; }
'''
src = src.replace('</style>', css + '</style>', 1)

scenes = f'''<section class="scene center" data-name="Gancho" data-dur="3600">
        <div class="brand rise" style="--d:.1s">ProduAVX · Grupo X Team X</div>
        <h2 class="hook"><span class="dl es" data-t="Tu historia merece|verse y sonar|como es." data-s="0.3" data-d="0.6"></span><span class="dl en" data-t="Your story deserves|to look and sound|the way it is." data-s="0.55" data-d="0.6"></span></h2>
        <div class="promise rise" style="--d:1.8s"><span class="dl es" data-t="Cada escena, única." data-s="1.8" data-d="0.6"></span><div class="dl en" data-t="Every scene, unique." data-s="2.05" data-d="0.6"></div></div>
        <div class="iris"><i></i><i></i><i></i><b></b></div>
      </section>

      <section class="scene center" data-name="Problema" data-dur="3600">
        <div class="tag rise">El problema</div>
        <h2 class="slow" style="--d:0s;font-size:8.6cqw"><span class="dl es" data-t="Una escena.|Una sola oportunidad." data-s="0" data-d="0.8"></span><span class="dl en" data-t="One scene.|One chance." data-s="0.4" data-d="0.8"></span></h2>
        <div class="clap"><div class="bar"></div><div class="body"><span>ProduAVX</span><strong>ESCENA 1 · TOMA ÚNICA</strong><span>Scene 1 · Single take</span></div></div>
      </section>

      <section class="scene" data-name="Proceso" data-dur="4500">
        <div class="tag rise">El proceso</div>
        <div class="steps">
          <div class="step" style="--d:0s;--n:1.8s"><b>01</b><div><h3><span class="dl es" data-t="Imagen" data-s="0" data-d="0.5"></span></h3><p class="dl sub" data-t="Luz y cámara con intención" data-s="0.15" data-d="0.5"></p><p class="dl en" data-t="Image · Light and camera with intent" data-s="0.3" data-d="0.5"></p></div></div>
          <div class="step" style="--d:1.8s;--n:3.6s"><b>02</b><div><h3><span class="dl es" data-t="Sonido" data-s="1.8" data-d="0.5"></span></h3><p class="dl sub" data-t="Captura y mezcla limpias" data-s="1.95" data-d="0.5"></p><p class="dl en" data-t="Sound · Clean capture and mix" data-s="2.1" data-d="0.5"></p></div></div>
          <div class="step last" style="--d:3.6s"><b>03</b><div><h3><span class="dl es" data-t="Postproducción" data-s="3.6" data-d="0.5"></span></h3><p class="dl sub" data-t="Color y montaje al detalle" data-s="3.75" data-d="0.5"></p><p class="dl en" data-t="Post · Color and edit, in detail" data-s="3.9" data-d="0.5"></p></div></div>
        </div>
        <div class="wave">{bars}</div>
        <div class="tl"><i></i><i></i><i></i><u></u></div>
      </section>

      <section class="scene center" data-name="Cierre" data-dur="3300">
        <img class="logo sm pop" alt="Logo de Grupo X" src="{logo}">
        <h2 class="slow" style="--d:.9s;font-size:8.3cqw"><span class="dl es" data-t="ProduAVX|Imagen y sonido,|bien hechos." data-s="0.9" data-d="0.7"></span><span class="dl en" data-t="Image and sound, done right." data-s="1.2" data-d="0.7"></span></h2>
        <div class="pill rise" style="--d:1.8s"><span class="dl es" data-t="Cuéntanos tu escena" data-s="1.8" data-d="0.5"></span><span class="dl en" data-t="Tell us your scene" data-s="1.95" data-d="0.5"></span></div>
        <div class="brand rise" style="--d:2.4s;font-size:2.7cqw"><span class="dl es" data-t="Grupo X · Team X" data-s="2.4" data-d="0.4"></span></div>
      </section>
'''
a = src.index('<section class="scene center" data-name="Gancho"')
b = src.index('    </div>\n  </div>\n\n  <div class="ctl">')
out = src[:a] + scenes + src[b:]
out = out.replace('var field = document.getElementById("field"), seed = 5;', 'var field = document.getElementById("field"), seed = 5; if (!field) return;')
out = out.replace('<title>Grupo X Reel</title>', '<title>ProduAVX Reel</title>')
(here / "15s").mkdir(exist_ok=True)
(here / "15s" / "reel.html").write_text(out, encoding="utf-8")
print("ok", len(out))
