// Sequential seek like the video render, then measure how much of an inactive scene is still visible
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const file = process.argv[2], times = JSON.parse(process.argv[3]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.addInitScript(() => { window.__RENDER = true; });
  await p.goto('file://' + path.join(__dirname, file));
  const total = await p.evaluate(() => window.__total);
  let worst = 0, where = '';
  for (let t = 0; t < total; t += 100) {
    const r = await p.evaluate(t => {
      window.__seek(t);
      let n = 0, names = [];
      document.querySelectorAll('.scene:not(.on) .dl').forEach(el => {
        const cs = getComputedStyle(el); let o = 1, e = el;
        while (e && e.classList && !e.classList.contains('stage')) { o *= parseFloat(getComputedStyle(e).opacity); e = e.parentElement; }
        if (cs.visibility === 'visible' && o > 0.01) { n++; names.push(el.textContent.slice(0, 12)); }
      });
      return { n, names };
    }, t);
    if (r.n > worst) { worst = r.n; where = t + ' ms ' + r.names.join(','); }
  }
  console.log(file, 'max ghost text elements from inactive scenes:', worst, where);
  await b.close();
})();
