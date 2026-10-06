const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort()); await p.goto('file://' + path.join(__dirname, 'guion_avx.html'));
  await p.evaluate(async () => { await Promise.all(['800 30px "Bricolage Grotesque"', '600 12px "Instrument Sans"', '400 12px "Instrument Sans"', '400 10px "JetBrains Mono"', '700 10px "JetBrains Mono"'].map(f => document.fonts.load(f))); await document.fonts.ready; });
  await p.pdf({ path: process.argv[2], width: '210mm', height: '297mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } }); await b.close(); })();
