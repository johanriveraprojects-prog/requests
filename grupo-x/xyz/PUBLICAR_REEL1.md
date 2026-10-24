# Reel 1 · Cómo publicarlo
Actualizado 2026-10-07. Archivos en `reel/`.

## Archivos
- `XYZ_reel1_visualizer_SIN_AUDIO.mp4`: **el que se sube**. 1080×1920, 16 s, visualizer sincronizado con la canción.
- `XYZ_reel1_visualizer_con_BUKELE.mp4`: solo para ver cómo queda (no está en el repo).
- `XYZ_portada_reel1.png`: portada.
- Se creó con `reel1_viz.html`, `make_viz_data.py` y `render.js`.

## Audio: usar la biblioteca de Instagram, no el MP3 pegado
BUKELE (Fanta Rosario × Bizarrap, del disco *La Amenaza*, 24-sep-2026) es una obra comercial. Si el MP3 va metido en el video, Instagram puede silenciarlo o dar reclamo. Hazlo así:
1. Sube `SIN_AUDIO.mp4`.
2. Toca **Audio** → busca "BUKELE" → fija el inicio en **1:15** (el visualizer está sincronizado con ese punto: 1:15,4 a 1:31,4).
3. Volumen del audio original en 0.
- Si la cuenta es de empresa y la canción no aparece, pasa la cuenta a **Creador** (Configuración → Tipo de cuenta). Si aun así no está, usa otra canción de la biblioteca o un beat de un miembro del club con su permiso.
- Aviso: el título "BUKELE" coincide con el apellido del presidente de El Salvador. Para tu público puede leerse como guiño político. Si no quieres esa lectura, cambia de tema.

## Portada (referencia de engagement)
La imagen que mandaste (palabras gigantes en varios idiomas sobre una foto: "Dinero / Money / Plata / お金") se tomó solo como **idea de estilo**. No usé la foto, que es de otras personas.
Aplicado a XYZ: **Últimos / Last / Primeros / 最初**. Dos idiomas y un kanji, que es lo que detiene el dedo, y la frase "Comenta tu palabra ↓" para provocar comentarios.
Para el grid del perfil, el texto queda en la zona central (recorte 4:5 seguro). Súbela como portada del reel.

## Caption (lista para pegar)
```
Somos las últimas letras. 🖤
XYZ Social Club: el club de los últimos, para toda la cadena del trap latino: artistas, productores, beatmakers, ingenieros, videógrafos, diseñadores, DJs y fans.

Los últimos serán los primeros.

👇 Comenta tu palabra: Últimos / Last / Primeros / 最初… escribe la tuya, en tu idioma.
Entra al club: link en bio.

#traplatino #musicaurbana #beatmakers #XYZSocialClub #ElClubDeLosUltimos
```

## Palabras clave (Instagram lee el texto del caption, la portada y lo que dices)
Usar de forma natural, sin repetir: **trap latino**, **música urbana**, **club social**, **productores y beatmakers**, **artistas independientes**, **Centroamérica / El Salvador** (si quieres foco local), **colaboración**.
Para sumar a la tendencia de este mes (SoundCloud 2026): **plugg / chugg**. Úsalas solo si el reel o el post realmente va de eso.

## Hashtags: solo 5
Según las fuentes que revisé, Instagram limita a **5 hashtags** por publicación desde diciembre de 2025 y recomienda 3-5 relevantes. Mezcla recomendada: grandes + medianos + de nicho/marca.
| Hashtag | Papel |
|---|---|
| #traplatino | grande, tema |
| #musicaurbana | grande, tema |
| #beatmakers | mediano, productores |
| #XYZSocialClub | marca |
| #ElClubDeLosUltimos | marca, nicho |
Cambia 1-2 por semana según lo que hable el post (por ejemplo #plugg o #chugg en el post de beats). No uses los 30 de antes.

## Menciones (según la tendencia del momento)
El tema del momento es el disco *La Amenaza* (Fanta Rosario, 24-sep-2026). Etiqueta en la caption o en el primer comentario: **@ de Fanta Rosario y @ de Bizarrap**, porque el audio es de ellos. No tengo sus usuarios verificados: cópialos desde sus perfiles oficiales (con la marca azul). Una mención de cortesía no garantiza que te repostee; no lo prometas ni lo pidas en el texto.
- Mencionar solo lo que es real: que usas su canción. No sugerir colaboración ni respaldo.
- Si más adelante hay artistas del club, ellos van primero en las menciones.

## Comentario fijado (primer comentario)
> Dinos tu palabra 👇 La mejor la ponemos en la portada del próximo reel.
(Esto convierte los comentarios en contenido: el día 21 del calendario puede reposear a los que respondan.)

## Hora recomendada
- **Miércoles 07-10 (día 1 del calendario), 7:30 pm hora de El Salvador** (UTC-6). Si ya pasó de las 9 pm, publicar **jueves 08-10 a las 7:30 pm**.
- Por qué: los estudios que revisé coinciden en que Reels rinde en tres ventanas, 8-12 h, 14-16 h y **18-21 h**; el miércoles y el jueves son de los mejores días (Sprout, Buffer). Son datos mayormente de EE. UU. y no de Centroamérica, así que el 7:30 pm es un punto de partida.
- Metricool está conectado, pero a la cuenta `grupoxteamx`, no a la de XYZ, y es nueva. No hay datos propios de XYZ todavía.
- Después de 7 días, mira Estadísticas → Audiencia → **Horas más activas** y mueve la publicación a esa hora.
- Los primeros 30-60 minutos importan: quédate respondiendo cada comentario.
- Mismo día: súbelo también a TikTok (misma hora) y a Facebook Reels. Cada red con su audio de biblioteca.

## Antes de publicar
1. Archivar los 4 posts de terceros.
2. Bio actualizada con el link.
3. Etiquetas y @ copiadas de perfiles oficiales.
4. Ver el video completo una vez, con sonido, en el celular.

## Versión final con video de fondo (2026-10-07)
- `reel/XYZ_reel1_FINAL_SIN_AUDIO.mp4` y `reel/XYZ_reel1_FINAL_con_cancion.mp4` (esta última queda solo local).
- Formato de Reels: 1080×1920, 30 fps, H.264 High, AAC 48 kHz, ~5,5 Mbps, 16 s.
- Cortes del video re-editados sobre los tiempos de la canción (1 tiempo = 0,496 s; 6 compases de video + 2 de firma).
- Firma final: "XYZ Social Club" en Playfair Display Italic, rojo con degradado, fondo negro con líneas onduladas (según tu imagen de referencia).
- Regenerar: `reel/make_bg.sh clip.mp4 bg.mp4` y luego `reel/compose.sh bg.mp4 salida.mp4 [cancion.mp3 75.37]`.
- Si el clip de fondo es de otra persona (por ejemplo un fragmento de un videoclip), también necesita su permiso para publicarse.

## Reel v2 "limpio" (2026-10-07): solo el video + la canción + firma
- Archivos: `reel/XYZ_reel_v2_con_cancion.mp4` y `reel/XYZ_reel_v2_SIN_AUDIO.mp4` (locales, no se suben al repo por tamaño y por el clip de terceros).
- 1080×1920, 30 fps, H.264 High, ~9 Mbps, AAC 48 kHz, 23,8 s.
- Sin visualizer, sin textos ni colores anteriores. Solo: video limpio (bordes negros recortados, menos ruido, nitidez), cortes sobre los tiempos de BUKELE (1:15), y al final **"XYZ Social Club"** pequeño y centrado en Playfair Display Italic rojo.
- Se quitó del clip original la placa final de créditos (a los 25,2 s).
- Regenerar: `reel/make_clean.sh clip.mp4 salida.mp4 [cancion.mp3 75.37]`.

## Reel v3 (2026-10-07): fondo negro OLED, 2160×3840, firma en cámara lenta
- `reel/XYZ_reel_v3_4K_con_cancion.mp4` y `reel/XYZ_reel_v3_4K_SIN_AUDIO.mp4` (locales; ~130 MB cada uno).
- Fondo negro puro (sin desenfoque), el video centrado a ancho completo. Firma "XYZ Social Club" que aparece letra por letra, saliendo de un desenfoque, con el espaciado cerrándose muy despacio (4,5 s).
- Maestro: 2160×3840, 30 fps, H.264 High 5.1, ~44 Mbps (130 MB; no se puede enviar por el chat, límite 30 MB). Para enviar y subir: copias HEVC (`XYZ_reel_v3_4K_HEVC_*.mp4`) a ~8 Mbps, ~24 MB, mismo 2160×3840.
- **Sobre el "4K":** el clip original es 720p. El escalado (Lanczos + nitidez + grano fino) no crea detalle nuevo; ayuda a que Instagram, que recomprime todo a 1080p, degrade menos. Según las guías que revisé, Instagram acepta 4K pero lo baja a 1080 al procesar; el máximo útil es 1440×2560.
- Corrección: las versiones anteriores tenían los negros subidos (luma 30 en vez de 16) por un ajuste de rango que ya quité. La v3 tiene negro real.
- Regenerar: `node reel/render_sig.js sigseq` y `reel/make_oled.sh clip.mp4 salida.mp4 [cancion.mp3 75.37]`.
