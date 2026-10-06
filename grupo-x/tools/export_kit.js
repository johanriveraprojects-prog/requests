// Exporta a PNG (fondo transparente) cada SVG listado en kit-de-marca/manifest.json al ancho indicado.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const kit = path.join(__dirname, '..', 'kit-de-marca'); const items = JSON.parse(fs.readFileSync(path.join(kit, 'manifest.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const it of items) {
    let svg = fs.readFileSync(path.join(kit, it.svg), 'utf8'); const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const w = it.width, h = Math.round(w * vb[2] / vb[1]);
    svg = svg.replace(/<svg /, `<svg width="${w}" height="${h}" `).replace(/(<svg[^>]*?) width="\d+" height="\d+"(?=[^>]*width="\d+")/, '$1');
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<body style="margin:0;background:transparent">${svg}</body>`);
    const out = path.join(kit, it.png); fs.mkdirSync(path.dirname(out), { recursive: true });
    await p.screenshot({ path: out, omitBackground: true }); await p.close();
    if (it.name === 'favicon') for (const s of [192, 32, 16]) { const q = await b.newPage({ viewport: { width: s, height: s } });
      await q.setContent(`<body style="margin:0;background:transparent">${svg.replace(/width="\d+" height="\d+"/, `width="${s}" height="${s}"`)}</body>`);
      await q.screenshot({ path: path.join(kit, 'favicon', `produavx-favicon-${s}.png`), omitBackground: true }); await q.close(); }
  }
  await b.close();
})();
