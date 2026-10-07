"""Audio-reactive data for the visualizer reel. Usage: python3 make_viz_data.py song.mp3 start_s dur_s out.js
Needs numpy + ffmpeg. Writes window.VIZ = {fps, bands[frame][48], bass[frame], rms[frame]} (all 0..1)."""
import sys, subprocess, wave, json, tempfile, os
import numpy as np
src, start, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
FPS, NB, SR = 30, 48, 44100
tmp = tempfile.mktemp(suffix='.wav')
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start-0.1),'-t',str(dur+0.2),'-i',src,'-ac','1','-ar',str(SR),tmp],check=True)
w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768; os.remove(tmp)
off = int(0.1*SR); N = 4096; win = np.hanning(N)
edges = np.geomspace(45, 12000, NB+1); freqs = np.fft.rfftfreq(N, 1/SR)
bands, bass, rms = [], [], []
for f in range(int(dur*FPS)):
    c = off + int(f/FPS*SR); seg = x[c-N//2:c+N//2]
    if len(seg) < N: seg = np.pad(seg,(0,N-len(seg)))
    m = np.abs(np.fft.rfft(seg*win))
    row = [m[(freqs>=edges[i])&(freqs<edges[i+1])].mean() if ((freqs>=edges[i])&(freqs<edges[i+1])).any() else 0 for i in range(NB)]
    bands.append(row); bass.append(m[(freqs>=40)&(freqs<130)].mean()); rms.append(np.sqrt((seg[N//2-700:N//2+700]**2).mean()))
B = np.log1p(np.array(bands)*6); B /= np.percentile(B,99.5)          # compress dynamic range
B *= np.linspace(0.85,1.35,NB)                                         # lift the highs (they are quieter)
B = np.clip(B,0,1)
for f in range(1,len(B)): B[f] = np.maximum(B[f], B[f-1]*0.80)         # fast attack, slow release
bs = np.array(bass); bs = np.clip((bs-np.percentile(bs,10))/(np.percentile(bs,98)-np.percentile(bs,10)),0,1)
rs = np.array(rms); rs = np.clip(rs/np.percentile(rs,98),0,1)
d = {'fps':FPS,'bands':np.round(B,2).tolist(),'bass':np.round(bs,2).tolist(),'rms':np.round(rs,2).tolist()}
open(out,'w').write('window.VIZ='+json.dumps(d,separators=(',',':'))+';')
print(len(B),'frames')
