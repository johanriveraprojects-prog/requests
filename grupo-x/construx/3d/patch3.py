import re
s = open('casa2.html', encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, count)

# ---- resolution: supersampled internal render (DPR from URL), title
rep("<title>Casa rústica</title>", "<title>Casa rústica v3</title>")
rep("const W = 1080, H = 1920, DUR = 15;", "const W = 1080, H = 1920, DUR = 15; const QS = new URLSearchParams(location.search); const DPR = +(QS.get('dpr') || 2), USE_AO = QS.get('ao') === '1';")
rep("renderer.setPixelRatio(1); renderer.setSize(W, H);", "renderer.setPixelRatio(DPR); renderer.setSize(W, H);")
rep("new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });", "new THREE.WebGLRenderTarget(W * DPR, H * DPR, { type: THREE.HalfFloatType, samples: 2 });")
rep("comp.setSize(W, H);", "comp.setPixelRatio(DPR); comp.setSize(W, H);")
rep("dir.shadow.mapSize.set(4096, 4096)", "dir.shadow.mapSize.set(4096, 4096); dir.shadow.radius = 2.2")

# ---- richer textures (stone, bump relief)
rep("const stoneTex = tex(128, 128, (g, w, h) => { speck(g, w, h, '#9a9388', 120, 2500); }, 1);",
"""const stoneTex = tex(256, 256, (g, w, h) => { speck(g, w, h, '#9a9388', 140, 9000); for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(40,36,30,${.1 + rnd() * .2})`; g.lineWidth = .6 + rnd() * 1.2; g.beginPath(); const x = rnd() * w, y = rnd() * h; g.moveTo(x, y); g.lineTo(x + (rnd() - .5) * 60, y + (rnd() - .5) * 60); g.stroke(); } for (let i = 0; i < 160; i++) { g.fillStyle = `rgba(${70 + rnd() * 30},${90 + rnd() * 40},50,${.07 + rnd() * .1})`; g.beginPath(); g.arc(rnd() * w, rnd() * h, 2 + rnd() * 7, 0, 6.283); g.fill(); } }, 1);
const shingTex = tex(256, 256, (g, w, h) => { speck(g, w, h, '#7a5a44', 70, 5000); for (let i = 0; i < 14; i++) { g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(i * (w / 14), 0, 1.5, h); } for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(20,10,5,${.1 + rnd() * .2})`; g.beginPath(); const x = rnd() * w; g.moveTo(x, 0); g.lineTo(x + (rnd() - .5) * 6, h); g.stroke(); } }, 2);""")
rep("const box = (w, h, d, m", """M.glowWin = new THREE.MeshBasicMaterial({ color: 0xffb45a, transparent: true, opacity: 0, depthWrite: false });
M.wood.bumpMap = woodTex; M.wood.bumpScale = 3; M.plank.bumpMap = woodTex; M.plank.bumpScale = 4; M.stone.bumpMap = stoneTex; M.stone.bumpScale = 5; M.conc.bumpMap = concTex; M.conc.bumpScale = 2;
M.shingle.map = shingTex; M.shingle.color.set(0xffffff); M.shingle.bumpMap = shingTex; M.shingle.bumpScale = 3;
M.truck = mat({ color: 0xb3321f, roughness: .45, metalness: .35 }); M.tire = mat({ color: 0x151515, roughness: .9 }); M.sack = mat({ color: 0xe9e2d0, roughness: .95 }); M.leaf = mat({ color: 0x2f6b2a, roughness: .8, side: THREE.DoubleSide }); M.pot = mat({ color: 0xa5543a, roughness: .9 }); M.log = mat({ map: woodTex, color: 0xb08a5e, roughness: .9, bumpMap: woodTex, bumpScale: 3 });
const box = (w, h, d, m""")
# stepped roof shingles use bump texture too (rows use their own materials; tint stays)
rep("new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(.065 + rnd() * .02, .40, .30 + rnd() * .07), roughness: .9, envMapIntensity: .4 })",
    "new THREE.MeshStandardMaterial({ map: shingTex, bumpMap: shingTex, bumpScale: 3, color: new THREE.Color().setHSL(.065 + rnd() * .02, .45, .62 + rnd() * .14), roughness: .9, envMapIntensity: .4 })")

# ---- windows with trim, sill, shutters hinges and warm interior glow
m = re.search(r"function win\(.*?\n", s)
new_win = """const winGlows = [];
function win(x, z, w, h, front, k) { const g = new THREE.Group(); g.add(box(w + .2, h + .2, .12, M.dark)); g.add(box(w, h, .14, M.glass)); g.add(box(.05, h, .16, M.dark)); g.add(box(w, .05, .16, M.dark));
  const gl = new THREE.Mesh(new THREE.PlaneGeometry(w * .94, h * .94), M.glowWin); gl.position.z = .082; g.add(gl);
  g.add(box(w + .42, .09, .3, M.stone, 0, -(h / 2 + .17), .09)); g.add(box(w + .34, .1, .22, M.wood, 0, h / 2 + .16, .07)); for (const sx of [-1, 1]) g.add(box(.09, h + .3, .2, M.wood, sx * (w / 2 + .1), 0, .07));
  g.add(box(w / 2, h, .05, M.plank, -(w / 2 + w / 4 + .1), 0, .06)); g.add(box(w / 2, h, .05, M.plank, (w / 2 + w / 4 + .1), 0, .06));
  for (const sx of [-1, 1]) for (const yy of [-h * .32, h * .32]) g.add(box(.18, .03, .035, M.metal, sx * (w / 2 + .14), yy, .1));
  const fb = box(w * .9, .16, .22, M.wood, 0, -(h / 2 + .32), .18); g.add(fb); for (let i = 0; i < 7; i++) { const f = new THREE.Mesh(new THREE.IcosahedronGeometry(.07, 0), new THREE.MeshStandardMaterial({ color: [0xf2557b, 0xffd23f, 0xffffff][i % 3], roughness: .6 })); f.position.set(-w * .38 + i * (w * .76 / 6), -(h / 2 + .2), .2); g.add(f); }
  g.position.set(x, BASE + 2.1, z); if (!front) g.rotation.y = Math.PI; winGlows.push(gl); return part(g, .88 + k * .01, .93 + k * .01, 'rise'); }
"""
s = s[:m.start()] + new_win + s[m.end():]

# ---- door panels
rep("door.add(box(.06, .5, .1, M.metal, .38, 0, .1));", "door.add(box(.06, .5, .1, M.metal, .38, 0, .1)); for (const yy of [-.55, .55]) door.add(box(.8, .8, .03, M.dark, 0, yy, .095)); door.add(box(1.5, .1, .3, M.wood, 0, 1.3, .08));")

# ---- extra detail block, inserted before smoke
extra = r"""
// ---------- v3 detail: gutters, lanterns, steps, chair, pots, fence, firewood, truck, palms, volcano
for (const sz of [-1, 1]) { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, L + 1.4, 10), M.metal); c.rotation.z = Math.PI / 2; c.castShadow = true; g.add(c); g.position.set(0, eaveY - .16, sz * (D / 2 + .78)); part(g, .84, .9, 'drop'); }
for (const [x, z] of [[L / 2 + .55, D / 2 + .78], [-L / 2 - .55, D / 2 + .78]]) { const g = new THREE.Group(); g.add(box(.09, WH + .2, .09, M.metal, 0, 0, 0)); g.position.set(x, BASE + WH / 2 + .1, z); part(g, .88, .93, 'rise'); }
for (const [x, z] of [[-2.6, D / 2 + 1.9], [1.4, D / 2 + 1.9]]) { const g = new THREE.Group(); g.add(box(.02, .5, .02, M.dark, 0, .25, 0)); g.add(box(.2, .26, .2, M.dark, 0, -.1, 0)); g.add(box(.15, .2, .15, M.glow, 0, -.1, 0)); g.position.set(x, BASE + 2.25, z); part(g, .95, .99, 'drop'); }
part(box(3.8, .2, .6, M.stone, -.6, .1, D / 2 + 2.8), .94, .98, 'rise'); part(box(3.4, .2, .5, M.stone, -.6, .3, D / 2 + 2.55), .95, .99, 'rise');
{ const g = new THREE.Group(); g.add(box(.7, .06, .6, M.plank, 0, .45, 0)); const bk = box(.7, .75, .06, M.plank, 0, .85, -.3); bk.rotation.x = -.18; g.add(bk); for (const sx of [-.34, .34]) { g.add(box(.05, .06, .9, M.wood, sx, .06, 0)); g.add(box(.05, .45, .05, M.wood, sx, .26, .22)); g.add(box(.05, .45, .05, M.wood, sx, .26, -.22)); g.add(box(.05, .06, .5, M.wood, sx, .66, 0)); } g.position.set(.9, BASE + .2, D / 2 + 1.7); g.rotation.y = -.3; part(g, .96, 1, 'rise'); }
for (const [x, z] of [[-2.95, D / 2 + 2.2], [1.75, D / 2 + 2.2], [-.6, D / 2 + .35]]) { const g = new THREE.Group(); const p = new THREE.Mesh(new THREE.CylinderGeometry(.22, .16, .32, 10), M.pot); p.position.y = .16; p.castShadow = true; g.add(p); for (let i = 0; i < 5; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(.16 + rnd() * .06, 1), M.leaf); b.position.set((rnd() - .5) * .3, .45 + rnd() * .2, (rnd() - .5) * .3); b.castShadow = true; g.add(b); } g.position.set(x, BASE + .2, z); part(g, .95 + rnd() * .02, 1, 'rise'); }
{ const fz = D / 2 + 8, secs = []; for (let x = -13; x <= 13; x += 2.2) if (x < -2.4 || x > 1.6) secs.push([x, fz, 0]); for (let z = fz - 2.2; z > -6; z -= 2.2) { secs.push([-13, z, 1]); secs.push([13, z, 1]); }
  secs.forEach(([x, z, side], i) => { const g = new THREE.Group(); g.add(box(.14, 1.25, .14, M.wood, 0, .62, 0)); for (const yy of [.45, .9]) g.add(box(side ? .1 : 2.2, .09, side ? 2.2 : .1, M.wood, side ? 0 : 1.1, yy, side ? -1.1 : 0)); g.position.set(x, hgt(x, z), z); part(g, .9 + i * .0025, .96 + i * .0025, 'rise'); }); }
{ const g = new THREE.Group(); for (let r = 0; r < 4; r++) for (let c = 0; c < 8 - r; c++) { const l = new THREE.Mesh(new THREE.CylinderGeometry(.09, .09, .8, 8), M.log); l.rotation.x = Math.PI / 2; l.position.set(c * .19 + r * .095, .1 + r * .17, 0); l.castShadow = true; g.add(l); } g.position.set(L / 2 + .6, 0, 1.2); g.rotation.y = Math.PI / 2; part(g, .93, .99, 'rise'); }
{ const g = new THREE.Group(); g.add(box(1.9, .18, 4.4, M.dark, 0, .55, 0)); g.add(box(1.85, .55, 1.7, M.truck, 0, .98, 1.15)); g.add(box(1.8, .5, 1.4, M.glass, 0, 1.36, 1.0)); g.add(box(1.85, .6, 1.5, M.truck, 0, 1.25, 1.2)); g.add(box(1.85, .5, 2.6, M.truck, 0, .98, -1.3)); for (const sx of [-.9, .9]) g.add(box(.06, .5, 2.6, M.truck, sx, 1.4, -1.3)); g.add(box(1.8, .5, .06, M.truck, 0, 1.4, -2.55));
  for (const [x, z] of [[-.95, 1.35], [.95, 1.35], [-.95, -1.35], [.95, -1.35]]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.42, .42, .28, 16), M.tire); w.rotation.z = Math.PI / 2; w.position.set(x, .42, z); w.castShadow = true; g.add(w); const hub = new THREE.Mesh(new THREE.CylinderGeometry(.2, .2, .3, 10), M.metal); hub.rotation.z = Math.PI / 2; hub.position.set(x, .42, z); g.add(hub); }
  for (let i = 0; i < 6; i++) g.add(box(.7, .22, .45, M.sack, -.45 + (i % 2) * .9, 1.35 + Math.floor(i / 4) * .22, -1.8 + Math.floor(i / 2) * .5));
  g.position.set(12.5, 0, 3.2); g.rotation.y = -.55; part(g, .02, .04, 'rise'); parts[parts.length - 1].leave = .88; }
for (let i = 0; i < 8; i++) { const sk = box(.7, .22, .45, M.sack, 7.2 + (i % 4) * .55, .12 + Math.floor(i / 4) * .22, 8.2 + (i % 2) * .1); part(sk, .06, .1, 'rise'); parts[parts.length - 1].leave = .9; }
function palm(x, z, sc) { const g = new THREE.Group(); const lean = (rnd() - .5) * .4, n = 9; for (let i = 0; i < n; i++) { const seg = new THREE.Mesh(new THREE.CylinderGeometry(.16 * sc * (1 - i * .03), .2 * sc * (1 - i * .03), 1.1 * sc, 8), M.log); seg.position.set(Math.sin(i * .2) * lean * i * .12 * sc, (.55 + i * 1.05) * sc, 0); seg.rotation.z = lean * .18; seg.castShadow = true; g.add(seg); }
  const topY = (9.4) * sc, topX = Math.sin(8 * .2) * lean * 8 * .12 * sc; for (let i = 0; i < 11; i++) { const fr = new THREE.Mesh(new THREE.PlaneGeometry(.55 * sc, 3.6 * sc, 1, 4), M.leaf); fr.geometry.translate(0, 1.8 * sc, 0); const pa = fr.geometry.attributes.position; for (let k = 0; k < pa.count; k++) pa.setZ(k, -Math.pow(pa.getY(k) / (3.6 * sc), 2) * 1.6 * sc); fr.rotation.set(0, 0, 0); const holder = new THREE.Group(); holder.add(fr); fr.rotation.x = -1.0 - rnd() * .3; holder.rotation.y = i / 11 * 6.283 + rnd() * .3; holder.position.set(topX, topY, 0); fr.castShadow = true; g.add(holder); }
  for (let i = 0; i < 4; i++) { const c = new THREE.Mesh(new THREE.SphereGeometry(.2 * sc, 8, 6), M.log); c.position.set(topX + (rnd() - .5) * .5 * sc, topY - .3 * sc, (rnd() - .5) * .5 * sc); g.add(c); }
  g.position.set(x, hgt(x, z), z); g.rotation.y = rnd() * 6.283; scene.add(g); }
for (const [x, z, sc] of [[-15, 8, 1.0], [16, 10, .9], [-13.5, -8, 1.1], [17.5, -5, 1.0], [-9, 14.5, .8], [8, -14, 1.0], [22, 12, 1.2]]) palm(x, z, sc);
// distant volcano and ridges: aerial perspective gives the sense of scale
function mountain(x, z, rb, rt, hh, hue, seedN) { const g = new THREE.CylinderGeometry(rt, rb, hh, 72, 14, true); const p = g.attributes.position, cc = new Float32Array(p.count * 3); for (let i = 0; i < p.count; i++) { const y = p.getY(i), t = (y + hh / 2) / hh, a = Math.atan2(p.getZ(i), p.getX(i)); const n = 1 + .09 * Math.sin(a * 5 + seedN) + .05 * Math.sin(a * 11 + seedN * 2) + .04 * Math.sin(t * 9 + a * 3); p.setX(i, p.getX(i) * n); p.setZ(i, p.getZ(i) * n); p.setY(i, y + Math.sin(a * 7 + seedN) * hh * .03 * (1 - t));
    const gcol = new THREE.Color().setHSL(hue, .38, .22 + t * .1), rock = new THREE.Color().setHSL(.07, .15, .36 + t * .08), k = clamp((t - .62) / .3); gcol.lerp(rock, k); cc[i*3] = gcol.r; cc[i*3+1] = gcol.g; cc[i*3+2] = gcol.b; }
  g.setAttribute('color', new THREE.BufferAttribute(cc, 3)); g.computeVertexNormals(); const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 1, flatShading: false })); m.position.set(x, hh / 2 - 6, z); scene.add(m); }
mountain(150, -520, 330, 22, 150, .28, 1); mountain(-260, -470, 280, 70, 85, .30, 2); mountain(430, -430, 260, 60, 80, .32, 3); mountain(-520, -280, 240, 60, 70, .29, 4);
// soft contact shadow under the house
const aoCv = document.createElement('canvas'); aoCv.width = aoCv.height = 128; { const g = aoCv.getContext('2d'), gr = g.createRadialGradient(64, 64, 20, 64, 64, 64); gr.addColorStop(0, 'rgba(0,0,0,.9)'); gr.addColorStop(.6, 'rgba(0,0,0,.45)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
const aoMat = new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(aoCv), transparent: true, opacity: 0, depthWrite: false }); const aoM = new THREE.Mesh(new THREE.PlaneGeometry(L + 7, D + 7), aoMat); aoM.rotation.x = -Math.PI / 2; aoM.position.y = .03; scene.add(aoM);
"""
rep("// smoke\n", extra + "// smoke\n")

# ---- drive new effects in setStage
rep("const on = clamp((s - .96) / .04); warm.forEach(l => l.intensity = 14 * on); M.glow.emissiveIntensity = 3 * on;",
    "const on = clamp((s - .96) / .04); warm.forEach(l => l.intensity = 14 * on); M.glow.emissiveIntensity = 3 * on; M.glowWin.opacity = .85 * on; aoMat.opacity = .5 * clamp((s - .06) / .1);")

# ---- optional ambient occlusion
rep("comp.addPass(new UnrealBloomPass(", "if (USE_AO) { const ao = new GTAOPass(scene, camera, W * DPR, H * DPR); ao.output = GTAOPass.OUTPUT.Default; ao.blendIntensity = .9; ao.updateGtaoMaterial({ radius: 1.4, distanceExponent: 1.2, thickness: 1.5, scale: 1.1, samples: 12 }); comp.addPass(ao); }\ncomp.addPass(new UnrealBloomPass(")
rep("import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';", "import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';\nimport { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';")
open('casa3.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
