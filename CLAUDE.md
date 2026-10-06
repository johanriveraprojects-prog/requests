# Memoria fija del proyecto — ProduAVX 2026

> **Este código es solo de ProduAVX.** Solo se habla y se trabaja ProduAVX aquí. ConstruX y el resto de Grupo X Team X no tienen páginas ni contenido en este sitio (solo la mención de marca madre en el pie y en el home).
> Este repo es un fork de la librería Python `requests`. **No tocar `src/` ni `tests/`.**
> El proyecto vive en `grupo-x/` (sitio estático HTML/CSS/JS, bilingüe ES/EN, sin build; páginas generadas con `python3 grupo-x/build_pages.py`).
> Rama de desarrollo: `claude/cool-ptolemy-jaf196`. No crear PR salvo que el usuario lo pida.

## ProduAVX
- Producción de Audio y Video. Enfoque: video y audio de **escenas únicas**, con detalle en la calidad de **producción y postproducción**.
- Marca de **Grupo X Team X** (≈ equipo trabajando con calidad y organización; Team X = equipo bilingüe, Grupo X = equipo nativo; bases en inglés para agilidad con inversión extranjera).
- Dentro del ecosistema de la marca madre: documentos organizados en una base de datos, estadísticas para pautar con partners en redes sociales y herramientas que agilizan el CoWork (.Network) — en este sitio se ve como el **Panel** de ProduAVX.
- Diseño especializado de ProduAVX (cinematográfico: oscuro, cian `#46e0ff` / violeta `#9a6bff`), distinto al de otras marcas del grupo.

## Páginas
`index.html` (hero, servicios, proceso, proyectos, marca madre) · `panel.html` (proyectos, estadísticas, documentos, herramientas) · `contacto.html` (formulario mailto, correo placeholder `hola@grupox.team`). Tema vía `data-brand="produavx"`; estilos en `assets/css/base.css`; textos ES/EN en `assets/js/i18n.js`; datos demo en `assets/js/data.js`.

## Logo
Monograma **PX** ("Producción X" / "Producción AVX"): P con bowl + X de cinta de doble trazo entrelazada, dentro de un anillo abierto tipo lente/disco. Gradiente cian `#46e0ff` → violeta `#9a6bff`. Referencias del usuario: X de cinta en dos trazos y P en anillo/lente.
Wordmark: "Produ" (Inter Display Medium) + "AVX" (Bold, gradiente) con lema "AUDIO · VIDEO · POST".
Kit en `grupo-x/assets/img/` (se regenera con `python3 grupo-x/tools/build_logo.py`, requiere `pip install fonttools`):
`produavx-logo.svg` (lockup, fondo oscuro) · `produavx-logo-light.svg` (fondo claro) · `produavx-mark.svg` (monograma, header/hero) · `produavx-mark-white.svg` / `-black.svg` (monocromo) · `produavx-favicon.svg` (simplificado, trazo grueso).
