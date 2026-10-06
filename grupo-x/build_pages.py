import os
OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [("index.html", "nav.home", "Inicio"), ("construx.html", "nav.construx", "ConstruX"),
       ("produavx.html", "nav.produavx", "ProduAVX"), ("network.html", "nav.network", ".Network"),
       ("contacto.html", "nav.contact", "Contacto")]

META = {
 "index.html": ("Grupo X Team X — ConstruX & ProduAVX", "Grupo X Team X: construcción (ConstruX) y producción de audio y video (ProduAVX) en un ecosistema organizado y compartido.", "gx", "X", "Grupo X"),
 "construx.html": ("ConstruX — Construcción y remodelación | Grupo X Team X", "ConstruX: construcción de casas, remodelaciones, terrenos, apartamentos y locales.", "construx", "C", "ConstruX"),
 "produavx.html": ("ProduAVX — Producción de audio y video | Grupo X Team X", "ProduAVX: producción de video y audio de escenas únicas con calidad de producción y postproducción.", "produavx", "P", "ProduAVX"),
 "network.html": ("Network — Ecosistema compartido | Grupo X Team X", "El .Network de Grupo X Team X: base de datos compartida, estadísticas y herramientas de CoWork.", "gx", "X", "Grupo X"),
 "contacto.html": ("Contacto | Grupo X Team X", "Contacta a Grupo X Team X, ConstruX o ProduAVX.", "gx", "X", "Grupo X"),
}

def head(page):
    title, desc, brand, mark, name = META[page]
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""} data-i18n="{k}">{d}</a></li>' for h, k, d in NAV)
    dattr = "" if brand == "gx" else f' data-brand="{brand}"'
    return f'''<!doctype html>
<html lang="es"{dattr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="theme-color" content="#0b0b0d">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/base.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="Grupo X Team X">
      <span class="logo-mark">{mark}</span>
      <span>{name}<small>{"Grupo X Team X" if brand != "gx" else "Team X"}</small></span>
    </a>
    <ul class="menu" id="menu">{items}</ul>
    <div class="tools">
      <div class="lang" role="group" aria-label="Language"><button data-lang="es" aria-pressed="true">ES</button><button data-lang="en" aria-pressed="false">EN</button></div>
      <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu">☰</button>
    </div>
  </div>
</header>
<main id="main">
'''

FOOT = '''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="logo" href="index.html"><span class="logo-mark">X</span><span>Grupo X<small>Team X</small></span></a>
        <p style="color:var(--muted);margin-top:14px;max-width:34ch" data-i18n="foot.about">Un equipo trabajando con calidad y organización.</p>
      </div>
      <div><h4 data-i18n="foot.brands">Marcas</h4><ul><li><a href="construx.html">ConstruX</a></li><li><a href="produavx.html">ProduAVX</a></li></ul></div>
      <div><h4 data-i18n="foot.explore">Explorar</h4><ul><li><a href="network.html" data-i18n="nav.network">.Network</a></li><li><a href="contacto.html" data-i18n="nav.contact">Contacto</a></li></ul></div>
    </div>
    <div class="copy"><span>© 2026 Grupo X Team X. <span data-i18n="foot.rights">Todos los derechos reservados.</span></span><span data-i18n="foot.note">Grupo X Team X · ConstruX · ProduAVX</span></div>
  </div>
</footer>
<script src="assets/js/data.js"></script>
<script src="assets/js/i18n.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

def cards(items, cols="g4"):
    out = f'<div class="grid {cols}">'
    for ic, k in items:
        out += f'<div class="card reveal"><div class="icon" aria-hidden="true">{ic}</div><h3 data-i18n="{k}.t"></h3><p data-i18n="{k}.p"></p></div>'
    return out + '</div>'

def steps(prefix):
    return '<div class="steps">' + "".join(
        f'<div class="step reveal"><div><h3 data-i18n="{prefix}{i}.t"></h3><p data-i18n="{prefix}{i}.p"></p></div></div>' for i in range(1, 5)) + '</div>'

PAGES = {}

PAGES["index.html"] = '''
<section class="hero"><div class="bigx" aria-hidden="true">X</div><div class="wrap" style="position:relative">
  <p class="eyebrow" data-i18n="brand.tag">Calidad · Organización · Equipo</p>
  <h1 data-i18n="home.title">Equipos que construyen <em>con propósito</em>.</h1>
  <p class="lead" style="margin-top:22px" data-i18n="home.lead"></p>
  <div class="actions"><a class="btn btn-primary" href="#marcas" data-i18n="home.cta1"></a><a class="btn btn-ghost" href="contacto.html" data-i18n="home.cta2"></a></div>
</div></section>

<section class="alt"><div class="wrap">
  <p class="eyebrow" data-i18n="home.what.eyebrow"></p>
  <h2 data-i18n="home.what.title" style="max-width:20ch"></h2>
  <p class="lead" data-i18n="home.what.lead"></p>
  <div class="stats" style="margin-top:44px">
    <div class="stat"><b>2</b><span data-i18n="stat.1"></span></div>
    <div class="stat"><b>ES·EN</b><span data-i18n="stat.2"></span></div>
    <div class="stat"><b>1</b><span data-i18n="stat.3"></span></div>
    <div class="stat"><b id="count-projects">8</b><span data-i18n="stat.4"></span></div>
  </div>
</div></section>

<section id="marcas"><div class="wrap">
  <h2 data-i18n="home.brands.title"></h2>
  <div class="grid g2" style="margin-top:28px">
    <a class="card brand-card cx reveal" href="construx.html">
      <div><span class="tag" data-i18n="cx.rubro"></span><h3 data-i18n="cx.name"></h3><p data-i18n="cx.short" style="margin-top:10px"></p></div>
      <span class="arrow" data-i18n="cta.visit"></span>
    </a>
    <a class="card brand-card av reveal" href="produavx.html">
      <div><span class="tag" data-i18n="av.rubro"></span><h3 data-i18n="av.name"></h3><p data-i18n="av.short" style="margin-top:10px"></p></div>
      <span class="arrow" data-i18n="cta.visit"></span>
    </a>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <p class="eyebrow" data-i18n="home.eco.eyebrow"></p>
  <h2 data-i18n="home.eco.title"></h2>
  <p class="lead" data-i18n="home.eco.lead"></p>
  <div style="margin-top:34px">''' + cards([("🗄️", "eco.1"), ("📊", "eco.2"), ("🤝", "eco.3")], "g3") + '''</div>
  <p style="margin-top:26px"><a class="btn btn-ghost" href="network.html"><span data-i18n="nav.network"></span> →</a></p>
</div></section>

<section><div class="wrap">
  <p class="eyebrow" data-i18n="home.why.eyebrow"></p>
  <h2 data-i18n="home.why.title"></h2>
  <p class="lead" data-i18n="home.why.lead"></p>
  <div class="grid g2" style="margin-top:34px">
    <div class="card reveal"><div class="icon" aria-hidden="true">🌐</div><h3 data-i18n="why.team"></h3><p data-i18n="why.team.p"></p></div>
    <div class="card reveal"><div class="icon" aria-hidden="true">📍</div><h3 data-i18n="why.group"></h3><p data-i18n="why.group.p"></p></div>
  </div>
</div></section>

<section class="alt"><div class="wrap center">
  <h2 data-i18n="home.same.title"></h2>
  <p class="lead" data-i18n="home.same.p"></p>
</div></section>
'''

PAGES["construx.html"] = '''
<section class="hero"><div class="bigx" aria-hidden="true">X</div><div class="wrap" style="position:relative">
  <p class="eyebrow" data-i18n="cx.rubro"></p>
  <h1 data-i18n="cx.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="cx.lead"></p>
  <div class="actions"><a class="btn btn-primary" href="contacto.html" data-i18n="home.cta2"></a><a class="btn btn-ghost" href="#proyectos" data-i18n="cx.work"></a></div>
</div></section>
<section class="alt"><div class="wrap"><h2 data-i18n="cx.s.title"></h2><div style="margin-top:26px">''' + cards([("🏠", "cx.s1"), ("🛠️", "cx.s2"), ("🏬", "cx.s3"), ("🌄", "cx.s4")]) + '''</div></div></section>
<section><div class="wrap"><h2 data-i18n="cx.p.title"></h2><div style="margin-top:26px">''' + steps("cx.p") + '''</div></div></section>
<section class="alt" id="proyectos"><div class="wrap"><h2 data-i18n="cx.work"></h2><div class="grid g4" data-projects="construx" style="margin-top:26px"></div></div></section>
'''

PAGES["produavx.html"] = '''
<section class="hero"><div class="bigx" aria-hidden="true">X</div><div class="wrap" style="position:relative">
  <p class="eyebrow" data-i18n="av.rubro"></p>
  <h1 data-i18n="av.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="av.lead"></p>
  <div class="actions"><a class="btn btn-primary" href="contacto.html" data-i18n="home.cta2"></a><a class="btn btn-ghost" href="#proyectos" data-i18n="av.work"></a></div>
</div></section>
<section class="alt"><div class="wrap"><h2 data-i18n="av.s.title"></h2><div style="margin-top:26px">''' + cards([("🎬", "av.s1"), ("🎙️", "av.s2"), ("🎞️", "av.s3"), ("📱", "av.s4")]) + '''</div></div></section>
<section><div class="wrap"><h2 data-i18n="av.p.title"></h2><div style="margin-top:26px">''' + steps("av.p") + '''</div></div></section>
<section class="alt" id="proyectos"><div class="wrap"><h2 data-i18n="av.work"></h2><div class="grid g4" data-projects="produavx" style="margin-top:26px"></div></div></section>
'''

PAGES["network.html"] = '''
<section class="hero"><div class="bigx" aria-hidden="true">.X</div><div class="wrap" style="position:relative">
  <p class="eyebrow">Grupo X Team X</p>
  <h1 data-i18n="net.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="net.lead"></p>
</div></section>
<section class="alt"><div class="wrap">
  <h2 data-i18n="net.projects"></h2>
  <div class="filters" id="filters" role="group">
    <button data-f="all" aria-pressed="true" data-i18n="net.f.all"></button>
    <button data-f="construx" aria-pressed="false" data-i18n="net.f.construx"></button>
    <button data-f="produavx" aria-pressed="false" data-i18n="net.f.produavx"></button>
  </div>
  <div class="card" style="overflow-x:auto"><table>
    <thead><tr><th data-i18n="net.col.id"></th><th data-i18n="net.col.name"></th><th data-i18n="net.col.brand"></th><th data-i18n="net.col.city"></th><th data-i18n="net.col.status"></th></tr></thead>
    <tbody id="proj-body"></tbody></table></div>
  <p style="color:var(--muted);font-size:.85rem;margin-top:10px">⇄ <span data-i18n="net.shared"></span></p>
</div></section>
<section><div class="wrap">
  <h2 data-i18n="net.stats.title"></h2><p class="lead" data-i18n="net.stats.lead"></p>
  <div class="dash" style="margin-top:28px">
    <div class="card"><div class="bars" id="reach-bars"></div></div>
    <div class="card"><h3 data-i18n="net.stats.mix"></h3><div class="bars" id="mix-bars" style="margin-top:14px"></div></div>
  </div>
</div></section>
<section class="alt"><div class="wrap"><h2 data-i18n="net.docs.title"></h2><div class="card"><ul id="docs" style="list-style:none"></ul></div></div></section>
<section><div class="wrap"><h2 data-i18n="net.cowork.title"></h2><div style="margin-top:26px">''' + cards([("🗂️", "net.cw1"), ("🖼️", "net.cw2"), ("📅", "net.cw3"), ("📣", "net.cw4")]) + '''</div></div></section>
'''

PAGES["contacto.html"] = '''
<section class="hero"><div class="wrap" style="position:relative">
  <p class="eyebrow">Grupo X Team X</p>
  <h1 data-i18n="contact.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="contact.lead"></p>
</div></section>
<section class="alt"><div class="wrap" style="max-width:680px">
  <form id="contact-form" novalidate>
    <label><span data-i18n="form.name"></span><input name="name" autocomplete="name" required></label>
    <label><span data-i18n="form.email"></span><input name="email" type="email" autocomplete="email" required></label>
    <label><span data-i18n="form.brand"></span><select name="brand">
      <option value="ConstruX" data-i18n="form.opt.cx"></option><option value="ProduAVX" data-i18n="form.opt.av"></option>
      <option value="Grupo X" data-i18n="form.opt.both"></option><option value="Partner" data-i18n="form.opt.partner"></option></select></label>
    <label><span data-i18n="form.msg"></span><textarea name="msg" required></textarea></label>
    <button class="btn btn-primary" type="submit" data-i18n="form.send"></button>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>
'''

for page, body in PAGES.items():
    with open(os.path.join(OUT, page), "w", encoding="utf-8") as f:
        f.write(head(page) + body + FOOT)

open(os.path.join(OUT, "assets/img/favicon.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b0b0d"/>'
    '<path d="M16 16l32 32M48 16L16 48" stroke="#f2f2f4" stroke-width="8" stroke-linecap="round"/></svg>')
print("ok")
