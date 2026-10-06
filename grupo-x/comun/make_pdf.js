const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.goto('file://' + path.join(__dirname, 'grupo-x-team-x.html'));
  await p.evaluate(async () => { await Promise.all(['800 30px "Bricolage Grotesque"', '700 14px "Instrument Sans"', '400 12px "Instrument Sans"', '400 10px "JetBrains Mono"'].map(f => document.fonts.load(f))); await document.fonts.ready; });
  await p.screenshot({ path: path.join(__dirname, 'vista.png') });
  await p.pdf({ path: process.argv[2], width: '297mm', height: '210mm', printBackground: true, pageRanges: '1', margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await b.close();
})();
