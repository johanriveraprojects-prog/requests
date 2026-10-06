"""Build the reel audio from fragments of the user's 'radio del trap' pack only (no music).
Usage: python3 make_track.py 15|30"""
import sys, wave
import numpy as np

SR = 44100
src = wave.open('pack.wav')
x = np.frombuffer(src.readframes(src.getnframes()), dtype='<i2').astype(float) / 32768

def cut(a, b, fin=.002, fout=.02):
    s = x[int(a * SR):int(b * SR)].copy()
    i, o = int(fin * SR), int(fout * SR)
    s[:i] *= np.linspace(0, 1, i)
    s[-o:] *= np.linspace(1, 0, o)
    return s

def rate(s, r):                       # resample: shifts pitch, shortens/lengthens
    n = int(len(s) / r)
    return np.interp(np.arange(n) * r, np.arange(len(s)), s)

def norm(s, peak):
    return s / (np.abs(s).max() + 1e-9) * peak

PAIR = norm(cut(1.126, 1.23, fin=.003, fout=.05), .55)   # logo: only the last, clean pulse of the beep (+ short tail)
BEEP = norm(cut(1.126, 1.19, fin=.003, fout=.015), .40)  # key text: same clean last pulse, no stutter
BLIP = norm(cut(0.82, 0.86, fout=.012), .30)     # tiny blip (labels)
BEEP_TO_PAIR = 0.0                               # the beep now starts at the head of the fragment

# (time of the sound, kind, pitch rate)
CUES = {
  15: [(1.2, 'logo', 1), (3.85, 'beep', 1), (7.4, 'beep', 1), (10.2, 'beep', 1.41),
       (12.1, 'logo', 1), (12.6, 'beep', .8), (13.4, 'beep', 1.41)],
  30: [(1.2, 'logo', 1), (4.25, 'beep', 1), (9.4, 'beep', 1), (12.7, 'beep', 1.19), (16.0, 'beep', 1.41),
       (19.3, 'beep', .9), (23.9, 'logo', 1), (24.5, 'beep', .8), (25.7, 'beep', 1.41)],
}
dur = int(sys.argv[1])
N = int(dur * SR)
out = np.zeros(N)
for t, kind, r in CUES[dur]:
    if kind == 'logo':
        s, off = rate(PAIR, r), BEEP_TO_PAIR / r
    elif kind == 'beep':
        s, off = rate(BEEP, r), 0
    else:
        s, off = rate(BLIP, r), 0
    i = int((t - off) * SR)
    out[i:i + len(s)] += s[:N - i]
out = np.tanh(out * 1.1) / np.tanh(1.1)
st = (np.stack([out, out], 1) * 32767).astype('<i2')
with wave.open(f'track{dur}.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print(dur, 'cues', len(CUES[dur]), 'peak', round(float(np.abs(out).max()), 2))
