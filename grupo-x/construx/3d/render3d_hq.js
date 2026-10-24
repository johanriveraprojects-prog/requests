// usage: node render3d_hq.js START END  → frames3d_v3/fNNNNN.jpg (1080x1920, rendered at 2x then downscaled)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), { execFileSync } = require('child_process');
(async () => {
  const [a, z] = [+process.argv[2], +process.argv[3]]; fs.mkdirSync('frames3d_v3', { recursive: true }); fs.mkdirSync('tmp_hq', { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  p.setDefaultTimeout(600000); p.on('pageerror', e => console.log('pageerror:', e.message.slice(0, 300)));
  await p.goto('http://localhost:8765/casa3.html?dpr=2&ao=0'); await p.waitForFunction(() => window.__ready, null, { timeout: 240000 });
  for (let f = a; f <= z; f++) {
    const n = String(f).padStart(5, '0'), tmp = `tmp_hq/t${a}.jpg`;
    await p.evaluate(t => window.__draw(t), f / 30);
    await p.screenshot({ path: tmp, type: 'jpeg', quality: 95 });
    execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', tmp, '-vf', 'scale=1080:1920:flags=lanczos', '-q:v', '2', `frames3d_v3/f${n}.jpg`]);
    if ((f - a) % 10 === 0) console.log('frame', f, new Date().toISOString().slice(11, 19));
  }
  await b.close(); console.log('DONE', a, z);
})();
