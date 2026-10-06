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

## Logo (decisión del usuario: **C principal + A para tamaño pequeño**)
- Monograma **AX** (**A**udio **V**isual **X**) sobre disco oscuro `#0b0b1c`, gradiente cian `#46e0ff` → violeta `#9a6bff`. Reemplaza al PX y a la versión disco+anillos+media luna.
- **Principal (C, monolínea):** trazo único redondeado, ≥ 48 px. Hero, lockups, redes grandes.
- **Pequeña (A, sólida):** letras gruesas, < 48 px: header del sitio (38 px), favicon, destacados de Instagram.
- Wordmark: "Produ" (Inter Display Medium) + "AVX" (Bold, gradiente) con lema "AUDIO · VIDEO · POST".
- Kit en `grupo-x/assets/img/` (se regenera con `python3 grupo-x/tools/build_logo.py`, requiere `pip install fonttools`): `produavx-mark.svg` (C) · `produavx-mark-small.svg` (A) · `produavx-favicon.svg` (A) · `produavx-logo.svg` / `produavx-logo-light.svg` (lockups) · `produavx-mark-white.svg` / `-black.svg` (monocromo, sin disco).
- Instagram: subir ≥ 720 px, 1:1, logo centrado con margen; destacados con la versión A.

## Investigación de logos (oct 2026)
Fuentes consultadas por búsqueda (varias páginas bloqueadas; no se vieron logos reales de productoras de Instagram): [Namecheap](https://www.namecheap.com/guru-guides/logo-design-trends/), [99designs video production](https://99designs.com/inspiration/logos/video-production), [LogoLounge 2026](https://www.logolounge.com/trend/2026-logo-trend-report), [Dribbble video-production-logo](https://dribbble.com/tags/video-production-logo).
Reglas derivadas: monograma en círculo (avatar de Instagram, 1:1, subir ≥720 px, sin texto pequeño); letras superpuestas/ligaduras con personalidad; paleta casi negro + blanco roto + un acento, degradados suaves; sistema adaptable (marca, versión simple, animada, wordmark) y versión monocroma.
Se exploraron tres direcciones (A sólido · B ligadura · C monolínea); el usuario eligió C + A pequeña.

## Logo BÁSICO (alternativa, pendiente de elegir)
AX plano en un solo color (blanco roto `#eeeefa` / tinta `#12121f`), sin degradado, con un **punto "tally" mitad rojo `#ff3b3b` / mitad verde `#2ee66b`** (luz de REC/listo) arriba a la derecha de la X. Archivos `grupo-x/assets/img/produavx-basic-*.svg` (mark, mark-light, mark-mono sin punto, logo, logo-light), generados por `build_logo.py`. El sitio sigue usando el logo C + A hasta que el usuario decida.
