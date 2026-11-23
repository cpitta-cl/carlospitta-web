# carlospitta.com

Sitio personal de Carlos R. Pitta, generado con Python y publicado en Cloudflare Pages.

- `content.py`: todos los textos (español e inglés), cursos, noticias y agenda de investigación.
- `build.py`: genera el HTML en `site/` (`python3 build.py`).
- `art.py`: ilustraciones SVG (angelito, diablito, íconos).
- `site/`: lo que se publica (HTML generado, `style.css`, `app.js`, `img/`, `docs/`).
- `functions/api/contact.js`: recibe el formulario de contacto. Necesita en Cloudflare un KV `CONTACTS` y/o el secreto `RESEND_API_KEY`; sin ellos el formulario ofrece el correo directo.

Cada push a `main` se publica en carlospitta.com; otras ramas generan una vista previa.
