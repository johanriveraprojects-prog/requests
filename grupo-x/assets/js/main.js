(function () {
  var D = window.GX_DATA, I = window.GX_I18N;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var el = function (tag, cls, txt) { var n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; };
  var brandName = { construx: "ConstruX", produavx: "ProduAVX" };

  // Navegación móvil
  var burger = $(".burger"), menu = $(".menu");
  if (burger) burger.addEventListener("click", function () {
    var open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
  });

  // Reveal on scroll
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: .12 });
    $$(".reveal").forEach(function (n) { io.observe(n); });
  } else { $$(".reveal").forEach(function (n) { n.classList.add("in"); }); }

  // Tarjetas de proyecto por marca
  function renderCards() {
    $$("[data-projects]").forEach(function (box) {
      var b = box.dataset.projects, lang = I.get();
      box.textContent = "";
      D.projects.filter(function (p) { return p.brand === b; }).forEach(function (p) {
        var c = el("article", "card proj");
        var th = el("div", "thumb " + (p.brand === "construx" ? "th-cx" : "th-av"), p.id);
        var body = el("div", "body");
        var meta = el("div", "meta");
        meta.appendChild(el("span", null, p.city + " · " + p.year));
        meta.appendChild(el("span", null, I.t("status." + p.status)));
        body.appendChild(meta);
        body.appendChild(el("h3", null, p[lang]));
        c.appendChild(th); c.appendChild(body); box.appendChild(c);
      });
    });
  }

  // .Network: tabla + filtros + estadísticas + documentos
  var filter = "all";
  function renderTable() {
    var tb = $("#proj-body"); if (!tb) return;
    var lang = I.get(); tb.textContent = "";
    D.projects.filter(function (p) { return filter === "all" || p.brand === filter; }).forEach(function (p) {
      var tr = el("tr");
      tr.appendChild(el("td", null, p.id));
      tr.appendChild(el("td", null, p[lang] + (p.shared ? " ⇄" : "")));
      tr.appendChild(el("td", null, brandName[p.brand]));
      tr.appendChild(el("td", null, p.city));
      var td = el("td"); td.appendChild(el("span", "status", I.t("status." + p.status))); tr.appendChild(td);
      tb.appendChild(tr);
    });
  }
  function renderBars() {
    var box = $("#reach-bars"); if (box) {
      box.textContent = "";
      var max = Math.max.apply(null, D.partners.map(function (p) { return p.reach; }));
      D.partners.forEach(function (p) {
        var r = el("div", "bar");
        r.appendChild(el("span", null, p.channel));
        var tr = el("div", "track"), f = el("div", "fill");
        tr.appendChild(f); r.appendChild(tr); r.appendChild(el("b", null, p.reach + "k"));
        box.appendChild(r);
        requestAnimationFrame(function () { f.style.width = (p.reach / max * 100) + "%"; });
      });
    }
    var mix = $("#mix-bars"); if (mix) {
      mix.textContent = "";
      ["construx", "produavx"].forEach(function (b, i) {
        var n = D.projects.filter(function (p) { return p.brand === b; }).length;
        var r = el("div", "bar");
        r.appendChild(el("span", null, brandName[b]));
        var tr = el("div", "track"), f = el("div", "fill" + (i ? " b2" : ""));
        tr.appendChild(f); r.appendChild(tr); r.appendChild(el("b", null, String(n)));
        mix.appendChild(r);
        requestAnimationFrame(function () { f.style.width = (n / D.projects.length * 100) + "%"; });
      });
    }
  }
  function renderDocs() {
    var ul = $("#docs"); if (!ul) return;
    var lang = I.get(); ul.textContent = "";
    D.documents.forEach(function (d) {
      var li = el("li");
      li.appendChild(el("span", null, "📄 " + d.name));
      li.appendChild(el("span", "pill", d[lang] + " · " + (d.brand === "gx" ? "Grupo X" : brandName[d.brand])));
      li.style.cssText = "display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid var(--line)";
      ul.appendChild(li);
    });
  }
  $$("#filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      filter = b.dataset.f;
      $$("#filters button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      renderTable();
    });
  });
  var count = $("#count-projects"); if (count) count.textContent = D.projects.length;

  // Formulario de contacto (sin backend: abre el cliente de correo)
  var form = $("#contact-form");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = new FormData(form), msg = $(".form-msg", form);
    var name = (f.get("name") || "").toString().trim(), email = (f.get("email") || "").toString().trim(), text = (f.get("msg") || "").toString().trim();
    if (!name || !email || !text) { msg.textContent = I.t("form.err"); return; }
    var body = name + " <" + email + ">\n\n" + text;
    window.location.href = "mailto:hola@grupox.team?subject=" + encodeURIComponent("[" + f.get("brand") + "] " + name) + "&body=" + encodeURIComponent(body);
    msg.textContent = I.t("form.ok");
  });

  function renderAll() { renderCards(); renderTable(); renderBars(); renderDocs(); }
  document.addEventListener("gx:lang", renderAll);
  document.addEventListener("DOMContentLoaded", renderAll);
})();
