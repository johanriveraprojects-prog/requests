# Fondo con Higgsfield para el Reel 1 (visualizer)
2026-10-07. El reel mantiene el estilo (texto que se decodifica, barras y anillos al ritmo de la canción). Solo cambia el fondo: un video generado con Higgsfield.

## Cómo se arma
1. Generas el fondo en Higgsfield (prompts abajo) y descargas el MP4.
2. Me lo mandas por el chat (adjunto) o lo dejas en `reel/fondo.mp4`.
3. Se compone con un solo comando: `reel/compose.sh fondo.mp4 salida.mp4`
   - El video se escala a 1080×1920, se repite en bucle y se recorta a 16 s.
   - Encima van el texto, las barras y los anillos, sincronizados con 1:15 → 1:31 de BUKELE.
   - Para ver con la canción: `./compose.sh fondo.mp4 salida.mp4 cancion.mp3 75.37` (solo para ver; para publicar, sube sin audio y pon BUKELE desde la biblioteca de Instagram).

## Configuración en Higgsfield
- Formato **9:16**, duración **10 s** (o dos clips de 5 s si el modelo no llega a 10).
- Modelo: `seedance_2_5` (video general) o `kling3_0` (si quieres varias tomas). Prueba primero un clip.
- **No pidas texto dentro del video**: la IA lo deforma. El texto lo pongo yo encima.
- Pídele que el tercio superior y el centro estén relativamente calmos, porque ahí va el texto.
- Sin logos ni marcas. Sin rostros de personas reales o famosas.

## Prompts (en inglés rinden mejor)
**A. Ciudad de noche (recomendado, el más seguro)**
> Vertical 9:16 cinematic night street, wet asphalt reflecting neon green light, slow forward dolly down an empty city street in Central America, light fog, tiny rain, deep blacks, high contrast, 35mm film grain, desaturated except neon green accents, moody trap music video aesthetic, no text, no logos, no people in the foreground.

**B. Pop-art cómic con ojos con lágrima (coincide con tu foto de perfil)**
> Vertical 9:16 animated black-and-white pop-art comic illustration, close-up of stylized eyes with long lashes and a single tear sliding down the cheek, halftone dots, ink lines, subtle paper grain, slow zoom out, faint neon green glow on the tear and highlights, dark background, graphic novel style, no text.

**C. Estudio / productor**
> Vertical 9:16 dark home studio at night, close shot of hands on a MIDI pad and a laptop screen glowing green, soft smoke, small LED lights flickering, shallow depth of field, slow handheld camera drift, cinematic, high contrast, no faces, no text, no logos.

**D. Mezcla (si quieres algo más "viral")**
> Same as A, but with fast whip-pan cuts every 2 seconds, glitch transitions and light streaks, synced to a trap beat feel, neon green and white only, no text.

## Sobre la referencia de Instagram
No pude abrir el link (Instagram está bloqueado desde este entorno y exige iniciar sesión). Para copiar su estilo, mándame 3-4 capturas de pantalla del video o descríbelo (colores, movimiento de cámara, qué se ve) y ajusto el prompt. También puedes adjuntar el MP4 de referencia si lo tienes, solo para estudiar el ritmo y los cortes, no para publicarlo.
