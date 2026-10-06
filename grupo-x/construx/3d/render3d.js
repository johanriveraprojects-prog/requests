// usage: node render3d.js START END  (frame indexes at 30 fps over 15 s)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [a, z] = [+process.argv[2], +process.argv[3]]; fs.mkdirSync('frames3d', { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('pageerror:', e.message.slice(0, 300)));
  await p.goto('http://localhost:8765/casa2.html'); await p.waitForFunction(() => window.__ready, null, { timeout: 180000 });
  for (let f = a; f <= z; f++) {
    await p.evaluate(t => window.__draw(t), f / 30);
    await p.screenshot({ path: `frames3d/f${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if ((f - a) % 25 === 0) console.log('frame', f, new Date().toISOString().slice(11, 19));
  }
  await b.close(); console.log('DONE', a, z);
})();
