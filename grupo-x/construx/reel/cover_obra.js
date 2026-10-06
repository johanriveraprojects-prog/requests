// Cover for the construction version: the finished 3D frame + two-line keyword headline.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const bg = path.resolve(process.argv[2]), out = process.argv[3];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const fonts = fs.readFileSync(path.join(__dirname, 'fonts-local.css'), 'utf8').replace(/url\(fonts\//g, 'url(file://' + __dirname + '/fonts/');
  const logo = fs.readFileSync(path.join(__dirname, '../brand/logo.b64'), 'utf8');
  const html = `<style>${fonts}
    html,body{margin:0;background:#000} #c{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;color:#f4f4f4}
    #c img.bg{position:absolute;inset:0;width:100%;height:100%} #c .shade{position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,rgba(6,12,26,.55),rgba(6,12,26,0))}
    #c .t{position:absolute;left:0;right:0;top:250px;text-align:center;text-shadow:0 4px 30px rgba(0,0,0,.55)}
    #c .logo{width:140px;filter:drop-shadow(0 0 22px rgba(255,255,255,.35));margin-bottom:46px}
    #c .k{font-weight:800;font-size:178px;letter-spacing:-.045em;line-height:.9} #c .g{font-weight:500;font-size:112px;letter-spacing:-.03em;color:#e8e8e8;line-height:1;margin-top:8px}
    #c .en{font-family:"Instrument Sans",sans-serif;font-size:42px;color:#e2e2e2;margin-top:34px} #c .chips{font-family:"JetBrains Mono",monospace;font-size:26px;letter-spacing:.2em;text-transform:uppercase;margin-top:44px;color:#f0f0f0}
  </style><div id="c"><img class="bg" src="file://${bg}"><div class="shade"></div>
    <div class="t"><img class="logo" src="data:image/png;base64,${logo}"><div class="k">CONSTRUYE</div><div class="g">tu proyecto</div><div class="en">Build your project</div><div class="chips">Cimientos · Estructura · Acabados</div></div></div>`;
  await p.setContent(html, { waitUntil: 'load' });
  await p.evaluate(async () => { await Promise.all(['800 100px "Bricolage Grotesque"', '500 100px "Bricolage Grotesque"', '400 20px "JetBrains Mono"', '400 20px "Instrument Sans"'].map(f => document.fonts.load(f))); await document.fonts.ready; });
  await p.waitForTimeout(400); await p.screenshot({ path: out, type: 'png' }); await b.close();
})();
