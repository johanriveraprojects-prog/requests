"""v2 audio: the client's song (first seconds, slowed to 0.86x) as bed + clean bips from the client's pack, all snapped to the 0.9016 s beat grid."""
import sys, wave
import numpy as np

SR = 44100
def load(path):
    w = wave.open(path); n = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float) / 32768
    return x.reshape(-1, n) if n > 1 else np.stack([x, x], 1)

pk = wave.open('pack.wav')
pack = np.frombuffer(pk.readframes(pk.getnframes()), dtype='<i2').astype(float) / 32768
def cut(a, b, fin=.002, fout=.02):
    s = pack[int(a*SR):int(b*SR)].copy(); i, o = int(fin*SR), int(fout*SR)
    s[:i] *= np.linspace(0, 1, i); s[-o:] *= np.linspace(1, 0, o); return s
def rate(s, r):
    n = int(len(s)/r); return np.interp(np.arange(n)*r, np.arange(len(s)), s)
def norm(s, p): return s / (np.abs(s).max()+1e-9) * p
LOGO = norm(cut(1.126, 1.23, fin=.003, fout=.05), .55)
BEEP = norm(cut(1.126, 1.19, fin=.003, fout=.015), .40)

CUES = {
 15: [(1.80, 'logo', 1), (3.61, 'beep', 1), (7.21, 'beep', 1), (10.82, 'beep', 1.41),
      (11.72, 'logo', 1), (12.62, 'beep', .8), (13.52, 'beep', 1.41)],
 30: [(1.80, 'logo', 1), (4.51, 'beep', 1), (9.02, 'beep', 1), (12.62, 'beep', 1.19), (16.23, 'beep', 1.41),
      (18.93, 'beep', .9), (23.44, 'logo', 1), (24.34, 'beep', .8), (26.15, 'beep', 1.41)],
}
SONG = {15: ('song15.wav', 0.0), 30: ('song30.wav', 9.016)}     # (file, output start in s)
SONG_GAIN = .55

dur = int(sys.argv[1]); N = dur * SR
bips = np.zeros(N)
for t, kind, r in CUES[dur]:
    s = rate(LOGO if kind == 'logo' else BEEP, r)
    i = int(t * SR); bips[i:i+len(s)] += s[:N-i]
song = np.zeros((N, 2))
sf, start = SONG[dur]
x = load(sf); i0 = int(start * SR); n = min(len(x), N - i0)
x = x[:n]
fin = int(.6 * SR); x[:fin] *= np.linspace(0, 1, fin)[:, None]
fout = int(1.0 * SR); x[-fout:] *= np.linspace(1, 0, fout)[:, None]
song[i0:i0+n] = x * SONG_GAIN
mix = song + bips[:, None]
mix = np.tanh(mix * 1.05) / np.tanh(1.05)
mix *= min(1, .95 / np.abs(mix).max())
pcm = (mix * 32767).astype('<i2')
with wave.open(f'mix{dur}.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
# verify where the song's big entrance lands (song only, 0.25 s windows)
mono = song.mean(1); hop = int(.05 * SR); m = len(mono)//hop
db = 20*np.log10(np.sqrt((mono[:m*hop].reshape(m, hop)**2).mean(1)) + 1e-6)
k = int(.25/.05)
for i in range(k*3, m):
    if db[i] - db[i-k*3:i-k].mean() > 10 and db[i] > -22:
        print(f'{dur}s: song entrance lands at {i*.05:.2f} s (target {dict({15: 11.72, 30: 23.44})[dur]}), peak {np.abs(mix).max():.2f}'); break
