# Memoria fija del proyecto — Grupo X Team X / ProduAVX 2026

> Este repo es un fork de la librería Python `requests`. **No tocar `src/` ni `tests/`.**
> El proyecto de trabajo vive en `grupo-x/` (sitio estático HTML/CSS/JS, bilingüe ES/EN, sin build).
> Rama de desarrollo: `claude/cool-ptolemy-jaf196`. No crear PR salvo que el usuario lo pida.

## Qué es Grupo X ≈ Team X
Sinónimo de un equipo trabajando con calidad y organización. Es la entidad que controla, por separado, proyectos en dos rubros:

1. **ConstruX** — Construcción y obras civiles n.c.p. Enfoque: construcción de casas y remodelación de espacios (terrenos, apartamentos, viviendas, locales).
2. **ProduAVX** — Producción de Audio y Video. Enfoque: video y audio de escenas únicas, con detalle en la calidad de producción y postproducción.

## Cómo actúan las dos marcas dentro de Grupo X Team X
- Bajo la imagen de la marca principal, fusionan contenidos en un **ecosistema organizado y compartido** con el diseño.
- Ese ecosistema gestiona **documentos organizados en una misma base de datos compartida**, de la que se obtienen **estadísticas** para pautar entre sí y con marcas conocidas de los partners en redes sociales.
- Así se crea un **.Network** con herramientas tecnológicas que agilizan el **CoWork**: conectar personas y crear con equipos proyectos con propósito.

## Por qué "Grupo X Team X"
Mezcla la interconexión de equipos que manejan el dominio de una inversión del extranjero, con bases en inglés para mayor agilidad. **Team X** = equipo bilingüe; **Grupo X** = equipo nativo.

## ¿Son iguales las marcas?
No. Al ser dos rubros, cada una tiene **diseño especializado**. La organización y conexión entre ellas es una herramienta de marketing visual para fiabilidad y consolidación dentro de las empresas y la web.

## Decisiones de diseño/implementación acordadas
- Stack: HTML/CSS/JS estático, multi-página, ES/EN con selector de idioma.
- Marca madre neutra (negro/blanco + acento X); ConstruX cálido (concreto/ámbar); ProduAVX cinematográfico (oscuro/cian-violeta).
- Un único sistema de componentes compartido (`grupo-x/assets/css/base.css`) con tema por marca vía `data-brand`.

## Logo ProduAVX
- Monograma **PX** ("Producción X" / "Producción AVX"): P con bowl + X de cinta de doble trazo entrelazada, dentro de un anillo tipo lente/disco abierto. Referencias del usuario: X de cinta negra (dos trazos) y P en anillo/lente.
- Archivo: `grupo-x/assets/img/produavx-mark.svg` (gradiente cian `#46e0ff` → violeta `#9a6bff`). Se usa en header, hero y favicon de `produavx.html`.
