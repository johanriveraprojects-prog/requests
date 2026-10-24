s = open('casa3.html', encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)
# 1) UV fit so grain follows each beam
rep("const box = (w, h, d, m", """function uvFit(geo, w, h, d) { const dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]], uv = geo.attributes.uv, K = 1.6;
  for (let f = 0; f < 6; f++) { const [a, b] = dims[f]; for (let k = 0; k < 4; k++) { const i = f * 4 + k, u = uv.getX(i), v = uv.getY(i); if (a > b) uv.setXY(i, v * b / K, u * a / K); else uv.setXY(i, u * a / K, v * b / K); } } return geo; }
const box = (w, h, d, m""")
rep("new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m)", "new THREE.Mesh(uvFit(new THREE.BoxGeometry(w, h, d), w, h, d), m)")
# 2) tree and frond materials
rep("// trees\n", """const leafTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#4c7a2e'; g.fillRect(0, 0, w, h); for (let i = 0; i < 1400; i++) { const l = 28 + rnd() * 40; g.fillStyle = `hsla(${88 + rnd() * 30},${45 + rnd() * 25}%,${l}%,${.35 + rnd() * .4})`; g.beginPath(); g.ellipse(rnd() * w, rnd() * h, 3 + rnd() * 6, 1.5 + rnd() * 3, rnd() * 3, 0, 6.283); g.fill(); } }, 4);
const treeMat = (hh, ss, ll) => new THREE.MeshStandardMaterial({ map: leafTex, bumpMap: leafTex, bumpScale: 4, color: new THREE.Color().setHSL(hh, ss, ll).multiplyScalar(2.1), roughness: 1, envMapIntensity: .5 });
const frondTex = (() => { const c = document.createElement('canvas'); c.width = 128; c.height = 512; const g = c.getContext('2d'); g.strokeStyle = '#2e5a1e'; g.lineWidth = 4; g.beginPath(); g.moveTo(64, 512); g.lineTo(64, 6); g.stroke();
  for (let i = 0; i < 46; i++) { const t = i / 46, y = 500 - t * 480, len = 56 * Math.sin(Math.PI * Math.min(1, t * .85 + .12)); for (const sx of [-1, 1]) { g.strokeStyle = `hsl(${95 + rnd() * 25},${50 + rnd() * 20}%,${22 + rnd() * 16}%)`; g.lineWidth = 3.2 - t * 1.4; g.beginPath(); g.moveTo(64, y); g.quadraticCurveTo(64 + sx * len * .6, y - len * .15, 64 + sx * len, y + len * .45); g.stroke(); } } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; })();
M.frond = new THREE.MeshStandardMaterial({ map: frondTex, alphaTest: .4, side: THREE.DoubleSide, roughness: .75, envMapIntensity: .8 });
// trees
""")
rep("new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(.34 + rnd() * .03, .5, .14 + rnd() * .04), roughness: 1, flatShading: true })", "treeMat(.34 + rnd() * .03, .55, .13 + rnd() * .05)")
rep("new THREE.ConeGeometry((1.6 - i * .26) * s, 1.8 * s, 8)", "new THREE.ConeGeometry((1.6 - i * .26) * s, 1.8 * s, 14)")
rep("new THREE.IcosahedronGeometry((1.5 + rnd() * .7) * s, 1), new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(.23 + rnd() * .06, .55, .2 + rnd() * .08), roughness: 1, flatShading: true })", "new THREE.IcosahedronGeometry((1.5 + rnd() * .7) * s, 3), treeMat(.24 + rnd() * .05, .6, .14 + rnd() * .07)")
# 3) palms: leaflet fronds, fewer and away from the camera arc
rep("const fr = new THREE.Mesh(new THREE.PlaneGeometry(.55 * sc, 3.6 * sc, 1, 4), M.leaf);", "const fr = new THREE.Mesh(new THREE.PlaneGeometry(1.9 * sc, 3.8 * sc, 1, 6), M.frond);")
rep("fr.geometry.translate(0, 1.8 * sc, 0); const pa = fr.geometry.attributes.position; for (let k = 0; k < pa.count; k++) pa.setZ(k, -Math.pow(pa.getY(k) / (3.6 * sc), 2) * 1.6 * sc);", "fr.geometry.translate(0, 1.9 * sc, 0); const pa = fr.geometry.attributes.position; for (let k = 0; k < pa.count; k++) pa.setZ(k, -Math.pow(pa.getY(k) / (3.8 * sc), 2) * 1.8 * sc);")
rep("for (const [x, z, sc] of [[-15, 8, 1.0], [16, 10, .9], [-13.5, -8, 1.1], [17.5, -5, 1.0], [-9, 14.5, .8], [8, -14, 1.0], [22, 12, 1.2]]) palm(x, z, sc);", "for (const [x, z, sc] of [[-15, 8, 1.0], [-13.5, -8, 1.1], [-9.5, 15, .8], [8, -14, 1.0], [17.5, -7, 1.0], [-29, 18, 1.2], [31, -19, 1.2], [-6, -22, 1.1]]) palm(x, z, sc);")
# 4) denser, thinner grass
rep("const n = 5200, geo = new THREE.ConeGeometry(.06, .5, 3);", "const n = 16000, geo = new THREE.ConeGeometry(.04, .55, 3);")
open('casa3.html', 'w', encoding='utf-8').write(s); print('ok')
