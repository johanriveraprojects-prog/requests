// usage: node render_overlay.js START END   → overlay/o%05d.png (transparent)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [a, z] = [+process.argv[2], +process.argv[3]]; const out = path.join(__dirname, 'overlay'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.addInitScript(() => { window.__RENDER = true; });
  await p.goto('file://' + path.join(__dirname, '15s/overlay.html'));
  await p.addStyleTag({ content: fs.readFileSync(path.join(__dirname, 'fonts-local.css'), 'utf8').replace(/url\(fonts\//g, 'url(file://' + __dirname + '/fonts/') });
  await p.evaluate(async () => { await Promise.all(['800 100px "Bricolage Grotesque"', '500 20px "Bricolage Grotesque"', '400 20px "JetBrains Mono"', '600 20px "JetBrains Mono"', '400 20px "Instrument Sans"'].map(f => document.fonts.load(f))); await document.fonts.ready; });
  for (let f = a; f <= z; f++) { await p.evaluate(t => window.__seek(t), f * 1000 / 30); await p.screenshot({ path: path.join(out, 'o' + String(f).padStart(5, '0') + '.png'), type: 'png', omitBackground: true }); }
  await b.close(); console.log('overlay done', a, z);
})();
