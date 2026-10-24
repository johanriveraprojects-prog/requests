#!/bin/sh
# Reel v2 "limpio": solo el video + la canción, cortes sobre el compás, firma final pequeña.
# Usage: ./make_clean.sh clip.mp4 salida.mp4 [cancion.mp3 inicio_seg]
# 1) Cada toma (cortes duros detectados) se estira/acorta unos % para durar un número entero de tiempos (1 tiempo = 0,496 s).
# 2) Limpieza: recorte de bordes negros, reducción de ruido, escalado Lanczos a 1080 px de ancho, nitidez y color suaves.
# 3) 9:16: video a ancho completo + copia desenfocada detrás. Firma "XYZ Social Club" (sig.png) con fade al final.
set -e
cd "$(dirname "$0")"
BEAT=0.496
CUTS="0 3.647 4.647 9.232 10.982 14.233 18.967 25.218"   # 25.218 = empieza la placa de créditos del clip original; se excluye
T=$(mktemp -d); LIST=""; PREV=""; TOTAL=0
for c in $CUTS; do
  if [ -n "$PREV" ]; then
    st=$(awk "BEGIN{print $PREV+0.04}"); av=$(awk "BEGIN{print $c-$PREV-0.08}")
    n=$(awk "BEGIN{n=int($av/$BEAT+0.5); if(n<1)n=1; print n}")
    tgt=$(awk "BEGIN{printf \"%.3f\", $n*$BEAT}"); k=$(awk "BEGIN{printf \"%.5f\", $tgt/$av}")
    ffmpeg -v error -y -ss "$st" -t "$av" -i "$1" -an \
      -vf "crop=944:704:30:8,hqdn3d=2.5:2.5:7:7,setpts=PTS-STARTPTS,setpts=PTS*$k,fps=30,scale=1080:-2:flags=lanczos+accurate_rnd" \
      -t "$tgt" -c:v libx264 -crf 8 -preset fast -pix_fmt yuv420p "$T/s$PREV.mp4"
    echo "file '$T/s$PREV.mp4'" >> "$T/l.txt"; TOTAL=$(awk "BEGIN{print $TOTAL+$tgt}")
  fi
  PREV=$c
done
ffmpeg -v error -y -f concat -safe 0 -i "$T/l.txt" -c copy "$T/cut.mp4"
D=$TOTAL; FO=$(awk "BEGIN{print $D-1.2}"); SS=$(awk "BEGIN{print $D-3.9}")
V="-c:v libx264 -preset veryslow -crf 12 -maxrate 30M -bufsize 60M -profile:v high -level 4.2 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -t $D -movflags +faststart"
FC="[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=42,eq=brightness=-0.30:saturation=1.1[bg];[b]unsharp=5:5:0.7:5:5:0.0,eq=contrast=1.05:saturation=1.06[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fade=out:st=$FO:d=1.2[m];[1:v]format=rgba,fade=in:st=$SS:d=0.9:alpha=1[sg];[m][sg]overlay=0:0:format=auto,format=yuv420p[v]"
if [ -n "$3" ]; then
  ffmpeg -v error -y -i "$T/cut.mp4" -loop 1 -i sig.png -ss "$4" -t "$D" -i "$3" -filter_complex "$FC" \
    -map "[v]" -map 2:a -af "afade=t=in:d=0.03,afade=t=out:st=$FO:d=1.2" -c:a aac -b:a 256k -ar 48000 $V "$2"
else
  ffmpeg -v error -y -i "$T/cut.mp4" -loop 1 -i sig.png -filter_complex "$FC" -map "[v]" -an $V "$2"
fi
echo "duración: $D s"
rm -rf "$T"
