#!/bin/sh
# Usage: ./compose.sh fondo.mp4 salida.mp4 [cancion.mp3 inicio_seg]
# fondo.mp4 = video generado en Higgsfield (cualquier duración; se repite en bucle y se recorta a 16 s, 9:16).
# Con cancion + inicio_seg mezcla el audio (solo para ver; para publicar usa la biblioteca de Instagram).
set -e
cd "$(dirname "$0")"
[ -d ov ] || node render_overlay.js reel1_viz.html ov
AUDIO=""; MAP=""
if [ -n "$3" ]; then AUDIO="-ss $4 -t 16 -i $3"; MAP="-map 1:v -map 2:a -af afade=t=in:d=0.03,afade=t=out:st=15.2:d=0.8 -c:a aac -b:a 192k"; fi
ffmpeg -v error -y -stream_loop -1 -t 16 -i "$1" -framerate 30 -i ov/%05d.png $AUDIO \
 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=brightness=-0.10:saturation=0.9[bg];[bg][1:v]overlay=format=auto,format=yuv420p[v]" \
 -map "[v]" ${MAP:+-map 2:a -af "afade=t=in:d=0.03,afade=t=out:st=15.2:d=0.8" -c:a aac -b:a 192k} -c:v libx264 -preset slow -crf 18 -r 30 -t 16 -movflags +faststart "$2"
