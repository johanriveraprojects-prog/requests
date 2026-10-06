import random, os
random.seed(33)
W, H = 794, 1123
logo = open('../brand/logo.b64').read()
fonts = open('fonts-local.css').read().replace('url(fonts/', 'url(file://' + os.getcwd() + '/fonts/')
AMB = '#86a8ff'
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
<div class="head"><img src="data:image/png;base64,{logo}"><div><div class="mono">Guion · Reel 15 s · Grupo X Team X</div><h1>Produ<b>AVX</b></h1></div><div class="meta mono">Borrador v1<br>9:16 · 1080×1920 · ES / EN</div></div>

<div class="box idea"><h3>Idea central</h3>
<p><strong>"Cada escena, única."</strong> El reel muestra cómo nace una pieza: la <b>luz</b> y la <b>cámara</b> capturan el momento, el <b>sonido</b> se cuida, y la <b>postproducción</b> lo termina al detalle. El mensaje: un momento irrepetible merece una producción cuidada.</p>
<div class="kw"><span>ESCENA ÚNICA</span><span>IMAGEN</span><span>SONIDO</span><span>POSTPRODUCCIÓN</span><span>CALIDAD</span></div></div>

<div class="two"><div class="box"><h3>A quién le hablamos</h3><p>A marcas, negocios, artistas y proyectos que necesitan video y audio cuidados. Incluye a los proyectos de ConstruX: recorridos y avances de obra. <em>Hipótesis: aún no se ha investigado este mercado.</em></p></div>
<div class="box"><h3>Qué debe sentir</h3><p>Confianza: "mi historia queda en manos con criterio y detalle". Que la calidad se note en lo que se ve y en lo que se escucha.</p></div></div>

<h2>Escena por escena <span class="mono">beats de 0,90 s · 7 bips · entrada fuerte a los 11,7 s</span></h2>
{row('0,0 – 3,6 s', 'Gancho', 'Pantalla negra. Se abre el iris de un lente y entra una onda de audio que late. Logo X pequeño arriba.', 'Tu historia merece verse y sonar como es.', 'Your story deserves to look and sound the way it is.', 'Bip a 0,1 s. Música desde el inicio, suave.', '<p class="pr">1,8 s · Cada escena, única. / Every scene, unique.</p>')}
{row('3,6 – 7,2 s', 'Por qué', 'Una claqueta cierra con "ESCENA 1 · TOMA ÚNICA". El foco se ajusta sobre el sujeto.', 'Una escena. Una sola oportunidad.', 'One scene. One chance.', 'Golpe seco de claqueta y bip.', '<p class="pr">Apoyo · Por eso cuidamos cada detalle. / That is why we care about every detail.</p>')}
{row('7,2 – 11,7 s', 'Proceso', 'Iris y luz → la onda de sonido sube y se limpia → línea de tiempo con clips; la imagen pasa de plana a graduada (antes y después).', '<b>01 IMAGEN</b> · Luz y cámara con intención<br><b>02 SONIDO</b> · Captura y mezcla limpias<br><b>03 POSTPRODUCCIÓN</b> · Color y montaje al detalle', '01 Image · Light and camera with intent<br>02 Sound · Clean capture and mix<br>03 Post-production · Color and editing, to the detail', 'Un bip por etapa: 7,2 s · 9,0 s · 10,8 s.')}
{row('11,7 – 15,0 s', 'Cierre', 'El resultado final llena el cuadro 9:16, con imagen graduada y ondas en movimiento. La cámara se aleja y aparece el nombre.', '<b>ProduAVX</b> · Imagen y sonido, bien hechos.<br>Grupo X · Team X<br>Cuéntanos tu escena', 'Image and sound, done right.<br>Tell us about your scene', 'Entrada fuerte a los 11,7 s. Bip del logo 12,1 s y botón de contacto 13,4 s.', '<p class="pr">Contacto: <i>[por definir]</i></p>')}
'''
p2 = f'''
<div class="box"><h3>Eslogan · tres opciones</h3>
<div class="opts"><div class="o r"><b>Cada escena, única.</b><span>Recomendado: es la promesa del reel y resume el rubro.</span></div><div class="o"><b>Imagen y sonido con detalle.</b><span>Descriptivo. Enfatiza el oficio.</span></div><div class="o"><b>Lo que se ve y se escucha, bien hecho.</b><span>Cercano. Enfatiza el resultado.</span></div></div></div>

<div class="two"><div class="box"><h3>Look</h3><p>Gráficos en movimiento hechos en código: iris de lente, ondas de sonido, línea de tiempo y claqueta. Mismo sistema de la marca madre, con fondo negro y estrellas lentas, y acento <b style="color:{AMB}">azul</b> para ProduAVX. Efecto de texto que se decodifica y línea en inglés debajo.</p></div>
<div class="box"><h3>Audio</h3><p>Aquí el audio es el producto: el reel debe sonar impecable. Recomiendo música original o con licencia y una mezcla cuidada. <em>La canción comercial usada hasta ahora puede silenciarse en cuentas de empresa.</em> Los bips del pack se mantienen como marcas de etapa.</p></div></div>

<div class="box"><h3>Descripción para publicar</h3>
<p class="cap"><b>ES</b> · Cada escena es única. Producimos video y audio con foco en la calidad: imagen, sonido y postproducción al detalle. Cuéntanos tu escena y la hacemos ver y sonar como es.<br><b>EN</b> · Every scene is unique. We produce video and audio with a focus on quality: image, sound and post-production, down to the detail. Tell us your scene and we will make it look and sound the way it is.</p>
<p class="tags">#ProduAVX #GrupoXTeamX #produccionaudiovisual #videoproduction #postproduccion #audio #filmmaking</p>
<p class="cap"><b>Comentario fijado</b> · ¿Qué escena quieres contar? / Which scene do you want to tell?</p></div>

<div class="box"><h3>Serie de contenido ProduAVX · siguientes reels</h3>
<ol class="ser"><li><b>Detrás de cámaras.</b> De la toma al resultado final, en 15 segundos.</li>
<li><b>Antes y después de color.</b> La misma toma, plana y graduada, con corte deslizante.</li>
<li><b>Audio sin mezcla y con mezcla.</b> Comparación A/B que se escucha: es el contenido más fácil de recordar.</li>
<li><b>Recorrido de obra de ConstruX.</b> Video de avances y entregas: primera pieza que usa los dos rubros juntos (.Network).</li></ol></div>

<div class="box need"><h3>Necesito que confirmes</h3>
<ul><li>Eslogan elegido.</li><li>Servicios exactos: ¿video, audio o ambos? ¿música, podcast, eventos, publicidad, recorridos?</li><li>Público principal al que quieres llegar primero.</li><li>Muestras reales (clips, mezclas, portafolio): no inventaré trabajos que no existan.</li><li>Contacto para el cierre: usuario, teléfono o enlace.</li><li>País y zona, para ajustar hashtags y mensaje.</li><li>Música del reel: ¿original, con licencia o la canción actual?</li></ul></div>
<div class="foot mono">Grupo X Team X · ProduAVX · Guion v1</div>
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
html = f'<!doctype html><meta charset="utf-8"><title>Guion ProduAVX</title><style>{css}</style><div class="pg">{sky}{p1}</div><div class="pg">{sky}{p2}</div>'
open('guion/guion_avx.html', 'w').write(html); print('ok')
