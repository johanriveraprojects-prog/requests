// Exporta a PNG los SVG de assets/img/instagram. El avatar sale en 1080, 720 y 2160 (master). Uso: NODE_PATH=$(npm root -g) node export_instagram.js
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const dir = path.join(__dirname, '..', 'assets', 'img', 'instagram');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const shot = async (svg, w, h, out, scale = 1) => {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: scale }); const p = await ctx.newPage();
    await p.setContent(`<body style="margin:0">${svg.replace(/width="\d+" height="\d+"/, `width="${w}" height="${h}"`)}</body>`);
    await p.screenshot({ path: path.join(dir, out) }); await ctx.close();
  };
  for (const f of fs.readdirSync(dir).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8'); const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/); const base = f.replace('.svg', '');
    await shot(svg, +w, +h, base + '.png');
    if (base === 'avatar') { await shot(svg, 720, 720, 'avatar-720.png'); await shot(svg, 1080, 1080, 'avatar-2160.png', 2); }
  }
  await b.close();
})();
