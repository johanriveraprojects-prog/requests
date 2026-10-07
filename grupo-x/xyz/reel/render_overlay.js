// Transparent PNG frames of the visualizer overlay. Usage: node render_overlay.js reel1_viz.html outdir
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const dir = __dirname, FPS = 30;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.goto('file://' + path.join(dir, process.argv[2]) + '?overlay=1');
  await page.addStyleTag({ content: fs.readFileSync(path.join(dir, 'fonts-local.css'), 'utf8').replace(/url\(fonts\//g, 'url(file://' + dir + '/fonts/') });
  await page.evaluate(async () => { await Promise.all(['800 100px "Bricolage Grotesque"', '600 20px "JetBrains Mono"', '500 20px "Instrument Sans"'].map(f => document.fonts.load(f))); await document.fonts.ready; });
  const out = path.join(dir, process.argv[3] || 'ov'); fs.mkdirSync(out, { recursive: true });
  const n = Math.round(await page.evaluate(() => window.__total) / 1000 * FPS);
  for (let f = 0; f < n; f++) {
    await page.evaluate(t => window.__seek(t), f * 1000 / FPS);
    await page.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.png'), omitBackground: true });
  }
  await browser.close();
})();
