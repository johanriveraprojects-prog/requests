const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 640, height: 360 } });
  const r = await p.evaluate(() => {
    const c = document.createElement('canvas'); const gl = c.getContext('webgl2') || c.getContext('webgl');
    if (!gl) return 'no webgl';
    const e = gl.getExtension('WEBGL_debug_renderer_info');
    return { version: gl.getParameter(gl.VERSION), renderer: e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a', maxTex: gl.getParameter(gl.MAX_TEXTURE_SIZE) };
  });
  console.log(JSON.stringify(r));
  await b.close();
})();
