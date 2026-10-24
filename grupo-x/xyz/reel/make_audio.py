"""Original audio for XYZ reel 1 (no third-party music). 16 s, 140 BPM half-time trap sketch. Usage: python3 make_audio.py out.wav"""
import sys, wave
import numpy as np
SR=44100; DUR=16.0
n=int(SR*DUR); x=np.zeros(n)
rng=np.random.default_rng(7)
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(n,i+len(sig))
    if i<n: x[i:j]+=sig[:j-i]*g
def env(l,a=.003,d=3.0): 
    t=np.arange(l)/SR; e=np.minimum(1,t/a)*np.exp(-t*d); return e
def bass(f,l=.55,d=3.2):
    t=np.arange(int(l*SR))/SR
    fr=f*(1+1.2*np.exp(-t*40))            # pitch drop at start
    ph=2*np.pi*np.cumsum(fr)/SR
    s=np.sin(ph)+0.12*np.sin(2*ph)
    return np.tanh(1.6*s)*env(len(t),.004,d)
def hat(l=.05,g=.5):
    s=rng.standard_normal(int(l*SR)); s=np.diff(s,prepend=0)
    return s*env(len(s),.0005,70)*g
def clap(l=.22):
    s=rng.standard_normal(int(l*SR)); s=np.diff(s,prepend=0)
    e=np.zeros(len(s)); 
    for o in (0,.012,.026): 
        k=int(o*SR); e[k:]+=np.exp(-np.arange(len(s)-k)/SR*55)
    return s*e*.5
def tick(f=1800,l=.06):
    t=np.arange(int(l*SR))/SR; return np.sin(2*np.pi*f*t)*env(len(t),.0005,60)*.5
beat=60/140; step=beat/4
notes=[43.65,43.65,38.89,41.20]            # F1, F1, D#1, E1 (dark minor movement), one per bar
bars=int(DUR/(beat*4))+1
for b in range(bars):
    t0=b*beat*4; f=notes[b%4]
    if t0+.6>DUR: break
    for off,l in ((0,.9),(beat*1.5,.5),(beat*2.75,.45)):
        add(bass(f,l),t0+off,.9)
    add(clap(),t0+beat*2,.8)
    for s_ in range(16):
        t=t0+s_*step
        g=.55 if s_%2==0 else .3
        add(hat(g=g),t)
        if b%2==1 and s_>=13: add(hat(g=.45),t+step/2)   # roll at end of odd bars
# scene hits: tick on each new line
for t in (0,2.7,4.9,7.1,9.5): add(tick(),t,.9)
for t in (9.5,10.1,10.7,11.3,11.9): add(tick(2600,.04),t+.0,.5)
# final impact at 12.1 s + riser before it
t=np.arange(int(2.1*SR))/SR
riser=np.diff(rng.standard_normal(len(t)),prepend=0)*(t/2.1)**2*.25
add(riser,10.0,1.0)
add(bass(32.7,1.8,1.6),12.1,1.3)
# fade out
fo=int(.8*SR); x[-fo:]*=np.linspace(1,0,fo)
x/=np.abs(x).max(); x*=.88
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype('<i2').tobytes())
