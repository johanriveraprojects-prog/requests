import os
OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [("index.html", "nav.home", "Inicio"), ("index.html#servicios", "nav.services", "Servicios"),
       ("index.html#proyectos", "nav.work", "Proyectos"), ("panel.html", "nav.network", "Panel"),
       ("contacto.html", "nav.contact", "Contacto")]

META = {
 "index.html": ("ProduAVX — Producción de audio y video", "ProduAVX: producción de video y audio de escenas únicas con calidad de producción y postproducción.", "produavx", "P", "ProduAVX"),
 "panel.html": ("Panel | ProduAVX", "Panel de ProduAVX: proyectos, documentos y estadísticas.", "produavx", "P", "ProduAVX"),
 "contacto.html": ("Contacto | ProduAVX", "Contacta a ProduAVX para tu proyecto de video o audio.", "produavx", "P", "ProduAVX"),
}

def head(page):
    title, desc, brand, mark, name = META[page]
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""} data-i18n="{k}">{d}</a></li>' for h, k, d in NAV)
    markhtml = '<img class="logo-img" src="assets/img/produavx-mark-small.svg" alt="" width="38" height="38">'
    icon = "produavx-favicon.svg"
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
<link rel="icon" href="assets/img/{icon}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/base.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="ProduAVX">
      {markhtml}
      <span>{name}<small>Grupo X Team X</small></span>
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
        <a class="logo" href="index.html"><img class="logo-img" src="assets/img/produavx-mark-small.svg" alt="" width="38" height="38"><span>ProduAVX<small>Grupo X Team X</small></span></a>
        <p style="color:var(--muted);margin-top:14px;max-width:38ch" data-i18n="foot.parent"></p>
      </div>
      <div><h4 data-i18n="foot.explore">Explorar</h4><ul><li><a href="index.html#servicios" data-i18n="nav.services"></a></li><li><a href="index.html#proyectos" data-i18n="nav.work"></a></li><li><a href="panel.html" data-i18n="nav.network"></a></li></ul></div>
      <div><h4 data-i18n="nav.contact">Contacto</h4><ul><li><a href="contacto.html" data-i18n="home.cta2"></a></li></ul></div>
    </div>
    <div class="copy"><span>© 2026 ProduAVX. <span data-i18n="foot.rights"></span></span><span data-i18n="foot.note"></span></div>
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
  <img class="hero-mark" src="assets/img/produavx-mark.svg" alt="ProduAVX (AX)" width="240" height="240">
  <p class="eyebrow" data-i18n="av.rubro"></p>
  <h1 data-i18n="av.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="av.lead"></p>
  <div class="actions"><a class="btn btn-primary" href="contacto.html" data-i18n="home.cta2"></a><a class="btn btn-ghost" href="#proyectos" data-i18n="home.cta1"></a></div>
</div></section>
<section class="alt" id="servicios"><div class="wrap"><h2 data-i18n="av.s.title"></h2><div style="margin-top:26px">''' + cards([("🎬", "av.s1"), ("🎙️", "av.s2"), ("🎞️", "av.s3"), ("📱", "av.s4")]) + '''</div></div></section>
<section><div class="wrap"><h2 data-i18n="av.p.title"></h2><div style="margin-top:26px">''' + steps("av.p") + '''</div></div></section>
<section class="alt" id="proyectos"><div class="wrap"><h2 data-i18n="av.work"></h2><div class="grid g4" data-projects="produavx" style="margin-top:26px"></div></div></section>
<section><div class="wrap center"><p class="eyebrow">Grupo X Team X</p><h2 data-i18n="home.parent.t"></h2><p class="lead" data-i18n="home.parent.p"></p></div></section>
'''

PAGES["panel.html"] = '''
<section class="hero"><div class="wrap" style="position:relative">
  <p class="eyebrow">ProduAVX</p>
  <h1 data-i18n="net.title2"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="net.lead2"></p>
</div></section>
<section class="alt"><div class="wrap">
  <h2 data-i18n="net.projects"></h2>
  <div class="card" style="overflow-x:auto"><table>
    <thead><tr><th data-i18n="net.col.id"></th><th data-i18n="net.col.name"></th><th data-i18n="net.col.brand"></th><th data-i18n="net.col.city"></th><th data-i18n="net.col.status"></th></tr></thead>
    <tbody id="proj-body"></tbody></table></div>
</div></section>
<section><div class="wrap">
  <h2 data-i18n="net.stats.title"></h2><p class="lead" data-i18n="net.stats.lead"></p>
  <div class="dash" style="margin-top:28px">
    <div class="card"><div class="bars" id="reach-bars"></div></div>
    <div class="card"><h3 data-i18n="net.stats.mix2"></h3><div class="bars" id="mix-bars" style="margin-top:14px"></div></div>
  </div>
</div></section>
<section class="alt"><div class="wrap"><h2 data-i18n="net.docs.title"></h2><div class="card"><ul id="docs" style="list-style:none"></ul></div></div></section>
<section><div class="wrap"><h2 data-i18n="nav.cw"></h2><div style="margin-top:26px">''' + cards([("🗂️", "cw1"), ("🖼️", "cw2"), ("📅", "cw3"), ("📣", "cw4")]) + '''</div></div></section>
'''

PAGES["contacto.html"] = '''
<section class="hero"><div class="wrap" style="position:relative">
  <p class="eyebrow">ProduAVX</p>
  <h1 data-i18n="contact.title"></h1>
  <p class="lead" style="margin-top:22px" data-i18n="contact.lead"></p>
</div></section>
<section class="alt"><div class="wrap" style="max-width:680px">
  <form id="contact-form" novalidate>
    <label><span data-i18n="form.name"></span><input name="name" autocomplete="name" required></label>
    <label><span data-i18n="form.email"></span><input name="email" type="email" autocomplete="email" required></label>
    <label><span data-i18n="form.brand"></span><select name="brand">
      <option value="Video" data-i18n="form.opt.av"></option><option value="Audio" data-i18n="form.opt.cx"></option>
      <option value="Post" data-i18n="form.opt.both"></option><option value="Partner" data-i18n="form.opt.partner"></option></select></label>
    <label><span data-i18n="form.msg"></span><textarea name="msg" required></textarea></label>
    <button class="btn btn-primary" type="submit" data-i18n="form.send"></button>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>
'''

for page, body in PAGES.items():
    with open(os.path.join(OUT, page), "w", encoding="utf-8") as f:
        f.write(head(page) + body + FOOT)

print("ok")
