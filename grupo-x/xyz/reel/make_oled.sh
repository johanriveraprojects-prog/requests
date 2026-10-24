#!/bin/sh
# Reel v3: fondo negro OLED puro (sin desenfoque), exportado a 2160x3840 ("4K" vertical), firma en cámara lenta.
# Usage: ./make_oled.sh clip.mp4 salida.mp4 [cancion.mp3 inicio_seg]
# Necesita sigseq/ (node render_sig.js sigseq). Cortes sobre el compás de BUKELE (1 tiempo = 0,496 s).
# Aviso: el clip original es 720p. El escalado a 4K usa Lanczos + nitidez + grano fino; no crea detalle nuevo,
# pero Instagram recomprime menos agresivamente un archivo de alta resolución y alto bitrate.
set -e
cd "$(dirname "$0")"
BEAT=0.496
CUTS="0 3.647 4.647 9.232 10.982 14.233 18.967 25.218"   # 25.218 = empieza la placa de créditos del clip original; se excluye
SIGLEN=4.5
T=$(mktemp -d); PREV=""; TOTAL=0
for c in $CUTS; do
  if [ -n "$PREV" ]; then
    st=$(awk "BEGIN{print $PREV+0.04}"); av=$(awk "BEGIN{print $c-$PREV-0.08}")
    n=$(awk "BEGIN{n=int($av/$BEAT+0.5); if(n<1)n=1; print n}")
    tgt=$(awk "BEGIN{printf \"%.3f\", $n*$BEAT}"); k=$(awk "BEGIN{printf \"%.5f\", $tgt/$av}")
    ffmpeg -v error -y -ss "$st" -t "$av" -i "$1" -an \
      -vf "crop=944:704:30:8,hqdn3d=2.5:2.5:7:7,setpts=PTS-STARTPTS,setpts=PTS*$k,fps=30" \
      -t "$tgt" -c:v libx264 -crf 6 -preset fast -pix_fmt yuv420p "$T/s$PREV.mp4"
    echo "file '$T/s$PREV.mp4'" >> "$T/l.txt"; TOTAL=$(awk "BEGIN{print $TOTAL+$tgt}")
  fi
  PREV=$c
done
ffmpeg -v error -y -f concat -safe 0 -i "$T/l.txt" -c copy "$T/cut.mp4"
D=$TOTAL; FO=$(awk "BEGIN{print $D-1.2}"); SS=$(awk "BEGIN{print $D-$SIGLEN}")
V="-c:v libx264 -preset slow -crf 13 -maxrate 45M -bufsize 90M -profile:v high -level 5.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -t $D -movflags +faststart"
FC="[0:v]scale=2160:-2:flags=lanczos+accurate_rnd,unsharp=5:5:0.8:5:5:0.0,eq=contrast=1.05:saturation=1.06,noise=alls=2:allf=t,pad=2160:3840:(ow-iw)/2:(oh-ih)/2:black,fade=out:st=$FO:d=1.2[m];[m][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
if [ -n "$3" ]; then
  ffmpeg -v error -y -i "$T/cut.mp4" -framerate 30 -itsoffset "$SS" -i sigseq/%05d.png -ss "$4" -t "$D" -i "$3" -filter_complex "$FC" \
    -map "[v]" -map 2:a -af "afade=t=in:d=0.03,afade=t=out:st=$FO:d=1.2" -c:a aac -b:a 256k -ar 48000 $V "$2"
else
  ffmpeg -v error -y -i "$T/cut.mp4" -framerate 30 -itsoffset "$SS" -i sigseq/%05d.png -filter_complex "$FC" -map "[v]" -an $V "$2"
fi
echo "duración: $D s"
rm -rf "$T"
