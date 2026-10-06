// Exporta a PNG los SVG de assets/img/instagram (y el avatar a 720 px). Uso: NODE_PATH=$(npm root -g) node export_instagram.js
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const dir = path.join(__dirname, '..', 'assets', 'img', 'instagram');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const f of fs.readdirSync(dir).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    const p = await b.newPage({ viewport: { width: +w, height: +h } });
    await p.setContent(`<body style="margin:0">${svg}</body>`);
    await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) });
    if (f === 'avatar.svg') { await p.setViewportSize({ width: 720, height: 720 }); await p.evaluate(() => { const s = document.querySelector('svg'); s.setAttribute('width', 720); s.setAttribute('height', 720); });
      await p.screenshot({ path: path.join(dir, 'avatar-720.png') }); }
    await p.close();
  }
  await b.close();
})();
