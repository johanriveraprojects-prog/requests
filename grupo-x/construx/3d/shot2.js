const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text().slice(0, 300)); });
  p.on('pageerror', e => console.log('pageerror:', e.message.slice(0, 400)));
  await p.goto('http://localhost:8765/casa2.html'); await p.waitForFunction(() => window.__ready, null, { timeout: 120000 });
  for (const t of JSON.parse(process.argv[2])) { const t0 = Date.now(); const s = await p.evaluate(t => window.__draw(t), t); await p.screenshot({ path: `c2_${String(Math.round(t * 10)).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 92 }); console.log('t', t, 'stage', s.toFixed(2), ((Date.now() - t0) / 1000).toFixed(1) + 's'); }
  await b.close();
})();
