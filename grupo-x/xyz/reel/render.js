// Usage: node render.js stills | node render.js full
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const dir = __dirname;
const FPS = 30;
(async () => {
  const mode = process.argv[2] || 'stills';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.addInitScript(() => { window.__RENDER = true; });
  await page.goto('file://' + path.join(dir, process.argv[3]));
  await page.addStyleTag({ content: fs.readFileSync(path.join(dir, 'fonts-local.css'), 'utf8').replace(/url\(fonts\//g, 'url(file://' + dir + '/fonts/') });
  await page.evaluate(async () => {
    await Promise.all(['800 100px "Bricolage Grotesque"', '500 20px "Bricolage Grotesque"', '400 20px "JetBrains Mono"', '600 20px "JetBrains Mono"', '400 20px "Instrument Sans"'].map(f => document.fonts.load(f)));
    await document.fonts.ready;
  });
  const total = await page.evaluate(() => window.__total);
  const shot = async (t, file) => {
    await page.evaluate(t => window.__seek(t), t);
    await page.screenshot({ path: file, type: 'jpeg', quality: 94 });
  };
  if (mode === 'stills') {
    fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
    const times = [0, 400, 900];
    for (const t of times) await shot(t, path.join(dir, 'stills', `t${String(t).padStart(5, '0')}.jpg`));
  } else {
    const out = path.join(dir, process.argv[4] || 'frames');
    fs.mkdirSync(out, { recursive: true });
    const n = Math.round(total / 1000 * FPS);
    for (let f = 0; f < n; f++) {
      await shot(f * 1000 / FPS, path.join(out, String(f).padStart(5, '0') + '.jpg'));
      if (f % 100 === 0) console.log('frame', f, '/', n);
    }
  }
  await browser.close();
})();
