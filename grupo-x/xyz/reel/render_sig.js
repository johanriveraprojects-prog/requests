// PNG sequence (2160x3840, transparent) of the slow-motion signature. Usage: node render_sig.js outdir
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const dir = __dirname, FPS = 30;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await page.goto('file://' + path.join(dir, 'sig_anim.html'));
  await page.addStyleTag({ content: fs.readFileSync(path.join(dir, 'fonts-local.css'), 'utf8').replace(/url\(fonts\//g, 'url(file://' + dir + '/fonts/') });
  await page.evaluate(async () => { await document.fonts.load('italic 500 100px "Playfair Display"'); await document.fonts.ready; });
  const out = path.join(dir, process.argv[2] || 'sigseq'); fs.mkdirSync(out, { recursive: true });
  const n = Math.round(await page.evaluate(() => window.__total) / 1000 * FPS);
  for (let f = 0; f < n; f++) {
    await page.evaluate(t => window.__seek(t), f * 1000 / FPS);
    await page.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.png'), omitBackground: true });
  }
  await browser.close();
})();
