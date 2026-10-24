#!/bin/sh
# Usage: ./compose.sh fondo_9x16.mp4 salida.mp4 [cancion.mp3 inicio_seg]
# fondo_9x16.mp4 = salida de make_bg.sh (1080x1920, 16 s). Superpone el overlay (texto, barras, anillos, firma).
# Con cancion + inicio_seg mezcla el audio (solo para ver/subir bajo tu responsabilidad; ver PUBLICAR_REEL1.md).
# Salida lista para Reels: 1080x1920, 30 fps, H.264 High yuv420p BT.709, AAC 48 kHz, faststart.
set -e
cd "$(dirname "$0")"
[ -d ov ] || node render_overlay.js reel1_viz.html ov
V="-c:v libx264 -preset veryslow -crf 12 -maxrate 30M -bufsize 60M -profile:v high -level 4.2 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -t 16 -movflags +faststart"
FC="[0:v]format=rgba[b];[b][1:v]overlay=format=auto:shortest=1,format=yuv420p[v]"
if [ -n "$3" ]; then
  ffmpeg -v error -y -i "$1" -framerate 30 -i ov/%05d.png -ss "$4" -t 16 -i "$3" -filter_complex "$FC" \
    -map "[v]" -map 2:a -af "afade=t=in:d=0.03,afade=t=out:st=15.2:d=0.8" -c:a aac -b:a 256k -ar 48000 $V "$2"
else
  ffmpeg -v error -y -i "$1" -framerate 30 -i ov/%05d.png -filter_complex "$FC" -map "[v]" -an $V "$2"
fi
