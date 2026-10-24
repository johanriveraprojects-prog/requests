#!/bin/sh
# Re-cuts a landscape clip onto the beat grid of BUKELE (1:15 → 1:31, one beat = 0.496 s) and frames it for 9:16.
# Usage: ./make_bg.sh clip.mp4 out_bg.mp4     (the clip's own audio is dropped)
# Cuts: SHOT_START:BEATS pairs below = where each shot starts in the source and how many beats it lasts (24 beats = 6 bars).
set -e
BEAT=0.496
SHOTS="0.10:4 3.75:2 4.75:4 9.33:3 11.08:4 14.33:4 19.07:3"
T=$(mktemp -d); i=0; LIST=""
for sh in $SHOTS; do
  st=${sh%%:*}; n=${sh##*:}; d=$(awk "BEGIN{printf \"%.3f\", $n*$BEAT}")
  ffmpeg -v error -y -ss "$st" -t "$d" -i "$1" -an -vf "fps=30,setpts=PTS-STARTPTS" -c:v libx264 -crf 14 -pix_fmt yuv420p "$T/s$i.mp4"
  echo "file '$T/s$i.mp4'" >> "$T/l.txt"; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i "$T/l.txt" -c copy "$T/cut.mp4"
# blurred full-bleed copy behind, sharp full-width copy in the middle; hold last frame to reach 16 s
ffmpeg -v error -y -i "$T/cut.mp4" -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=38,eq=brightness=-0.28:saturation=1.1[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=0:740,tpad=stop_mode=clone:stop_duration=6,trim=duration=16,setpts=PTS-STARTPTS,format=yuv420p" -r 30 -c:v libx264 -crf 16 -an "$2"
rm -rf "$T"
