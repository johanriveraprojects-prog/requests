import random, os
random.seed(33)
W, H = 794, 1123
logo = open('../brand/logo.b64').read()
fonts = open('fonts-local.css').read().replace('url(fonts/', 'url(file://' + os.getcwd() + '/fonts/')
AMB = '#e3a857'
stars = []
for i in range(11):
    stars.append(f'<circle cx="{random.uniform(8,W-8):.0f}" cy="{random.uniform(8,H-8):.0f}" r="{random.uniform(.8,1.5):.2f}" fill="#eaf0ff" opacity="{random.uniform(.35,.85):.2f}"/>')
for i in range(22):
    stars.append(f'<circle cx="{random.uniform(5,W-5):.0f}" cy="{random.uniform(5,H-5):.0f}" r="{random.uniform(.5,.85):.2f}" fill="#c8d2ff" opacity="{random.uniform(.16,.36):.2f}"/>')
sky = f'<svg class="stars" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(stars) + '</svg>'

def row(t, name, vis, es, en, snd, note=''):
    return f'''<div class="row"><div class="tm"><b>{t}</b><span>{name}</span></div>
      <div class="c"><h4>Qué se ve</h4><p>{vis}</p></div>
      <div class="c"><h4>Texto en pantalla</h4><p class="es">{es}</p><p class="en">{en}</p>{note}</div>
      <div class="c"><h4>Sonido</h4><p>{snd}</p></div></div>'''

p1 = f'''
<div class="head"><img src="data:image/png;base64,{logo}"><div><div class="mono">Guion · Reel 15 s · Grupo X Team X</div><h1>Constru<b>X</b></h1></div><div class="meta mono">Borrador v1<br>9:16 · 1080×1920 · ES / EN</div></div>

<div class="box idea"><h3>Idea central</h3>
<p><strong>"Tu casa, por etapas."</strong> Una casa rústica de madera y piedra se levanta frente a la cámara mientras el texto explica el camino: <b>cimientos, estructura, acabados</b>. El mensaje: tú pones el sueño, nosotros lo construimos contigo, con orden y calidad.</p>
<div class="kw"><span>TERRENO</span><span>CIMIENTOS</span><span>ESTRUCTURA</span><span>ACABADOS</span><span>HOGAR</span></div></div>

<div class="two"><div class="box"><h3>A quién le hablamos</h3><p>A quien tiene un <strong>terreno</strong> o una casa por <strong>remodelar</strong>, en pueblo o en ciudad, y construye por primera vez o por etapas. <em>Hipótesis tomada de la investigación; falta validarla con personas reales.</em></p></div>
<div class="box"><h3>Qué debe sentir</h3><p>Seguridad y orden: "no estoy solo en esto". La obra se ve como un camino claro, no como un gasto incierto.</p></div></div>

<h2>Escena por escena <span class="mono">beats de 0,90 s · 7 bips · canción entra fuerte a los 11,7 s</span></h2>
{row('0,0 – 3,6 s', 'Gancho', 'Terreno verde al amanecer. Estacas y cuerda marcan dónde irá la casa. El dron avanza lento. Logo X pequeño arriba.', '¿Tienes el terreno y no sabes por dónde empezar?', 'You own the land. Where do you start?', 'Bip a 0,1 s. Canción desde el inicio, suave.', '<p class="pr">1,8 s · Tu casa, por etapas. / Your home, step by step.</p>')}
{row('3,6 – 7,2 s', 'Por qué', 'Se vierte la losa. Excavadora y obreros trabajando. La cámara orbita despacio.', 'Una obra sin plan sale cara.', 'A build without a plan gets costly.', 'Bip en la primera palabra.', '<p class="pr">Apoyo · Aquí se construye con orden. / Here we build with order.</p>')}
{row('7,2 – 11,7 s', 'Método', 'Los muros de piedra suben, se arma la estructura de madera, llega el techo. Andamios y materiales a la vista.', '<b>01 CIMIENTOS</b> · Empezamos firmes<br><b>02 ESTRUCTURA</b> · Madera y piedra, bien hechas<br><b>03 ACABADOS</b> · Los detalles que hacen hogar', '01 Foundations · We start solid<br>02 Structure · Wood and stone, done right<br>03 Finishing · The details that make it home', 'Un bip por etapa: 7,2 s · 9,0 s · 10,8 s.')}
{row('11,7 – 15,0 s', 'Cierre', 'Casa terminada con luz dorada. Se encienden las luces del porche y sale humo de la chimenea. La cámara se aleja.', '<b>ConstruX</b> · Tu casa, hecha realidad.<br>Grupo X · Team X<br>Escríbenos para tu proyecto', 'Your home, made real.<br>Message us about your project', 'Entrada fuerte de la canción a los 11,7 s. Bip del logo 12,1 s y botón de contacto 13,4 s.', '<p class="pr">Contacto: <i>[por definir]</i></p>')}
'''
p2 = f'''
<div class="box"><h3>Eslogan · tres opciones</h3>
<div class="opts"><div class="o r"><b>Tu casa, por etapas.</b><span>Recomendado: ya es la promesa del reel y se recuerda.</span></div><div class="o"><b>Construimos contigo.</b><span>Más cercano. Enfatiza el equipo.</span></div><div class="o"><b>Obra bien hecha, paso a paso.</b><span>Más técnico. Enfatiza calidad.</span></div></div></div>

<div class="two"><div class="box"><h3>Look</h3><p>Render 3D de la casa rústica ya hecho (450 fotogramas). Texto en la mitad superior sobre el cielo, la casa abajo. Palabras clave en <b style="color:{AMB}">ámbar</b>, el color de ConstruX en el sistema de marca. Efecto de texto que se decodifica y línea en inglés debajo.</p></div>
<div class="box"><h3>Audio</h3><p>Canción tuya ralentizada 0,86× y bips de tu pack, anclados a los pulsos. <em>Es una obra comercial: en cuentas de empresa puede silenciarse. Para publicar sin riesgo, usar música con licencia.</em> Opcional: viento, pájaros y martillo si tienes efectos propios.</p></div></div>

<div class="box"><h3>Descripción para publicar</h3>
<p class="cap"><b>ES</b> · ¿Tienes el terreno y no sabes por dónde empezar? Construimos tu casa por etapas: cimientos, estructura y acabados. Madera, piedra y obra bien hecha. Escríbenos y cuéntanos tu proyecto.<br><b>EN</b> · You own the land and don't know where to start? We build your home step by step: foundations, structure and finishing. Wood, stone and work done right. Message us and tell us about your project.</p>
<p class="tags">#ConstruX #GrupoXTeamX #construccion #casaderustica #terreno #remodelacion #homebuilding #ruralhome</p>
<p class="cap"><b>Comentario fijado</b> · ¿Qué etapa te preocupa más: cimientos, estructura o acabados? / Which stage worries you most?</p></div>

<div class="box"><h3>Serie de contenido ConstruX · siguientes reels</h3>
<ol class="ser"><li><b>Remodelación antes y después.</b> Un espacio se transforma en 3D, con el mismo efecto de etapas.</li>
<li><b>Errores que encarecen tu obra.</b> Tres consejos: estudio de suelos, no cambiar planos a mitad de obra, cuidar la estructura (país sísmico). <em>Guía general, no sustituye a un profesional.</em></li>
<li><b>Antes de comprar un terreno.</b> Qué revisar: acceso, agua, suelo, permisos.</li>
<li><b>Apartamento o local.</b> Mismo método de etapas aplicado a otros espacios.</li></ol></div>

<div class="box need"><h3>Necesito que confirmes</h3>
<ul><li>Eslogan elegido y, si lo hay, tu propio texto de apertura.</li><li>Contacto para el cierre: usuario, teléfono o enlace.</li><li>País y zona donde opera ConstruX, para ajustar mensaje y hashtags (por ejemplo #ElSalvador).</li><li>Qué incluye el servicio: ¿también planos y permisos, o solo obra?</li><li>Si hay obras reales, fotos o renders propios para añadir credibilidad.</li><li>Música: ¿se mantiene la canción o se cambia por una con licencia?</li></ul></div>
<div class="foot mono">Grupo X Team X · ConstruX · Guion v1</div>
'''
css = f'''{fonts}
@page {{ size: 210mm 297mm; margin: 0 }}
html,body{{margin:0;background:#000}}
.pg{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#000;color:#f0f0f0;font-family:"Instrument Sans",sans-serif;padding:34px 38px;box-sizing:border-box;page-break-after:always}}
.pg:last-child{{page-break-after:auto}}
.stars{{position:absolute;left:0;top:0}}
.pg>*:not(.stars){{position:relative}}
.mono{{font-family:"JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.16em;color:#9c9c9c;font-size:9px}}
.head{{display:flex;align-items:center;gap:16px;margin-bottom:16px}} .head img{{width:52px;filter:drop-shadow(0 0 12px rgba(255,255,255,.35))}}
.head h1{{margin:2px 0 0;font:800 40px/1 "Bricolage Grotesque";letter-spacing:-.025em}} .head h1 b{{color:{AMB}}} .meta{{margin-left:auto;text-align:right;line-height:1.7}}
.box{{border:1px solid #3d3d3d;border-radius:11px;background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.014));padding:11px 15px;margin-bottom:11px}}
.box h3{{margin:0 0 5px;font:700 11px "JetBrains Mono";text-transform:uppercase;letter-spacing:.14em;color:{AMB}}}
.box p{{margin:0;font-size:12.2px;line-height:1.42;color:#dcdcdc}} .box em{{color:#a9a9a9}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:11px}} .two .box{{margin-bottom:11px}}
.kw{{display:flex;gap:7px;margin-top:8px}} .kw span{{border:1px solid {AMB};color:{AMB};border-radius:20px;font:600 9.5px "JetBrains Mono";letter-spacing:.12em;padding:3px 9px}}
h2{{font:800 17px "Bricolage Grotesque";margin:6px 0 8px;letter-spacing:-.01em}} h2 .mono{{margin-left:8px;font-size:8.5px}}
.row{{display:grid;grid-template-columns:108px 1fr 1.18fr .8fr;gap:10px;border:1px solid #3d3d3d;border-radius:11px;background:rgba(255,255,255,.03);padding:10px 12px;margin-bottom:9px}}
.tm b{{display:block;font:700 12.5px "JetBrains Mono";color:{AMB}}} .tm span{{display:block;margin-top:5px;font:800 15px "Bricolage Grotesque"}}
.c h4{{margin:0 0 4px;font:600 8.5px "JetBrains Mono";text-transform:uppercase;letter-spacing:.14em;color:#8f8f8f}}
.c p{{margin:0;font-size:11.4px;line-height:1.38;color:#dcdcdc}} .c .es{{font-weight:600;color:#fff}} .c .en{{color:#b3b3b3;margin-top:4px;font-size:10.8px}} .c .pr{{margin-top:6px;color:{AMB};font-size:10.6px}}
.opts{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}} .o{{border:1px solid #444;border-radius:9px;padding:8px 10px}} .o.r{{border-color:{AMB};background:rgba(227,168,87,.08)}}
.o b{{display:block;font:800 14px "Bricolage Grotesque";margin-bottom:3px}} .o span{{font-size:10.6px;color:#bdbdbd;line-height:1.3}}
.cap{{margin-bottom:6px!important}} .tags{{color:{AMB}!important;font:500 11px "JetBrains Mono"!important;margin:2px 0 7px!important}}
.ser{{margin:0;padding-left:17px;font-size:11.8px;line-height:1.4;color:#dcdcdc}} .ser li{{margin-bottom:4px}}
.need{{border-color:{AMB}}} .need ul{{margin:0;padding-left:17px;font-size:11.8px;line-height:1.45;color:#e2e2e2}}
.foot{{position:absolute!important;left:38px;right:38px;bottom:18px;text-align:center}}
'''
html = f'<!doctype html><meta charset="utf-8"><title>Guion ConstruX</title><style>{css}</style><div class="pg">{sky}{p1}</div><div class="pg">{sky}{p2}</div>'
open('guion/guion.html', 'w').write(html); print('ok')
