#!/bin/bash
S=/tmp/claude-0/-home-user-requests/53982224-a5cc-5b68-bac0-24fd8aed5879/scratchpad
cd $S/b3d
while [ $(grep -l DONE hq_0.log hq_113.log hq_226.log hq_338.log 2>/dev/null | wc -l) -lt 4 ]; do sleep 20; done
O=$S/GrupoX_CONSTRUX_HQ_v2; mkdir -p $O
R=/home/user/requests/grupo-x/construx/reel
for v in "dia:overlay_dia:construx-construye-en-el-salvador-HQ-15s" "etapas:overlay:construx-tu-casa-por-etapas-HQ-15s"; do
  IFS=: read k ov name <<< "$v"
  ffmpeg -loglevel error -y -framerate 30 -i $S/b3d/frames3d_v3/f%05d.jpg -framerate 30 -i $R/$ov/o%05d.png -i $S/sfx/mix4_15.mp3 -filter_complex "[0][1]overlay,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -profile:v high -crf 19 -maxrate 11M -bufsize 22M -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart -t 15 $O/$name.mp4
done
ffmpeg -loglevel error -y -i $S/b3d/frames3d_v3/f00449.jpg $O/fondo-final-hq.png
echo ASSEMBLED
