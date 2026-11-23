"""Ilustraciones SVG originales del sitio (trazo índigo, acentos naranjos)."""

I, O, P = "var(--ink)", "var(--accent)", "var(--paper)"

def _svg(body, vb="0 0 80 80", cls="icon"):
    return (f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" fill="none" stroke="{I}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

PILLAR_ICONS = [
 # 01 salud y belleza: corazón con pulso
 _svg(f'<path d="M40 66 C14 48 10 30 22 21 C30 15 38 19 40 26 C42 19 50 15 58 21 C70 30 66 48 40 66Z" fill="{O}" fill-opacity=".18"/>'
      f'<path class="pulse" d="M14 42 H28 L33 32 L39 50 L44 38 L48 42 H66" stroke="{O}"/>'),
 # 02 dinero: barras que crecen y moneda
 _svg(f'<path d="M14 64 H68"/><rect x="18" y="52" width="8" height="12"/><rect x="31" y="45" width="8" height="19"/>'
      f'<rect x="44" y="35" width="8" height="29"/><rect x="57" y="22" width="8" height="42" fill="{O}" fill-opacity=".25"/>'
      f'<circle cx="25" cy="27" r="9" fill="{O}"/><path d="M25 22 V32 M22 25 H27 a2 2 0 0 1 0 4 H23" stroke="{P}" stroke-width="2"/>'),
 # 03 procrastinación: la lámpara de Aladino
 _svg(f'<path d="M16 50 C16 40 30 38 40 40 C50 38 58 42 66 36 C64 46 56 52 46 54 L44 58 H30 L28 54 C22 54 16 53 16 50Z" fill="{O}" fill-opacity=".2"/>'
      f'<path d="M26 58 H48 M34 40 C34 35 42 35 42 40"/><path d="M66 36 C70 30 64 24 60 26 C58 20 66 14 70 16" stroke="{O}"/>'
      f'<circle cx="62" cy="11" r="2" fill="{O}" stroke="none"/>'),
 # 04 flujo: olas y un punto que las surfea
 _svg(f'<path d="M10 52 C20 44 28 60 40 52 C52 44 60 60 70 52"/><path d="M10 62 C20 54 28 70 40 62 C52 54 60 70 70 62" opacity=".5"/>'
      f'<path d="M10 42 C20 34 28 50 40 42 C52 34 60 50 70 42" stroke="{O}"/><circle cx="40" cy="30" r="6" fill="{O}" stroke="none"/>'),
 # 05 amor: dos personas y un corazón
 _svg(f'<circle cx="27" cy="30" r="9"/><circle cx="53" cy="30" r="9"/><path d="M12 66 C12 52 20 46 27 46 C34 46 38 50 40 54 C42 50 46 46 53 46 C60 46 68 52 68 66"/>'
      f'<path d="M40 24 C36 19 30 22 33 27 L40 33 L47 27 C50 22 44 19 40 24Z" fill="{O}" stroke="{O}" stroke-width="1.5"/>'),
 # 06 control: círculo de lo que sí depende de ti
 _svg(f'<circle cx="40" cy="40" r="28" stroke-dasharray="4 5"/><circle cx="40" cy="40" r="13" fill="{O}" fill-opacity=".85" stroke="{O}"/>'
      f'<path d="M35 40 L39 44 L46 36" stroke="{P}"/>'),
 # 07 confianza, perdón y gratitud: diario con tres marcas
 _svg(f'<path d="M14 18 H38 C40 18 40 20 40 22 V64 C40 61 38 60 36 60 H14Z"/><path d="M66 18 H42 C40 18 40 20 40 22 V64 C40 61 42 60 44 60 H66Z"/>'
      f'<path d="M46 29 L49 32 L55 26 M46 40 L49 43 L55 37 M46 51 L49 54 L55 48" stroke="{O}"/><path d="M20 30 H33 M20 40 H33 M20 50 H30" opacity=".5"/>'),
 # 08 propósito: ikigai, cuatro círculos
 _svg(f'<circle cx="40" cy="27" r="15"/><circle cx="27" cy="40" r="15"/><circle cx="53" cy="40" r="15"/><circle cx="40" cy="53" r="15"/>'
      f'<circle cx="40" cy="40" r="5" fill="{O}" stroke="{O}"/>'),
 # 09 consciencia: respiración que se expande
 _svg(f'<circle cx="40" cy="40" r="8" fill="{O}" stroke="{O}"/><circle class="breath" cx="40" cy="40" r="17" opacity=".7"/><circle class="breath b2" cx="40" cy="40" r="27" opacity=".35"/>'),
 # 10 espiritualidad: constelación
 _svg(f'<path d="M16 58 L30 40 L44 48 L56 24 L66 34" opacity=".55"/>'
      + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="none"/>' for x, y, r, c in
                [(16,58,3,I),(30,40,3.5,I),(44,48,3,I),(56,24,5,O),(66,34,3,I),(24,18,1.8,I),(66,62,1.8,I)])),
]

# Íconos pequeños para líneas de investigación
LINE_ICONS = [
 _svg(f'<circle cx="40" cy="40" r="24"/><path d="M30 46 C34 52 46 52 50 46" stroke="{O}"/><circle cx="32" cy="34" r="2.5" fill="{I}" stroke="none"/><circle cx="48" cy="34" r="2.5" fill="{I}" stroke="none"/>'),
 _svg(f'<path d="M12 60 C24 60 26 26 40 26 C54 26 56 46 68 46" stroke="{O}"/><path d="M12 66 H68 M12 16 V66"/>'),
 _svg(f'<path d="M14 50 C22 40 30 40 38 46"/><path d="M42 34 C50 28 60 28 66 34" stroke="{O}"/><path d="M58 26 L66 34 L58 40" stroke="{O}"/><circle cx="20" cy="30" r="6"/>'),
 _svg(f'<path d="M40 14 L62 22 V40 C62 54 52 62 40 66 C28 62 18 54 18 40 V22Z"/><path d="M32 40 L38 46 L50 34" stroke="{O}"/>'),
]

def hero_scene():
    """Una persona con un angelito y un diablito en los hombros, con partes animables."""
    return f'''<svg class="scene" viewBox="50 90 320 255" aria-hidden="true" fill="none" stroke="{I}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <g class="person">
    <path d="M70 380 C70 300 120 262 210 262 C300 262 350 300 350 380" fill="#fff"/>
    <path d="M188 262 V236 H232 V262"/>
    <g class="head">
      <ellipse cx="210" cy="176" rx="62" ry="70" fill="#fff"/>
      <path d="M152 160 C150 112 186 98 214 102 C246 106 270 124 268 166 C258 140 236 128 212 130 C190 132 168 140 152 160Z" fill="{I}"/>
      <g class="eyes"><g class="pupils">
        <circle cx="188" cy="182" r="4.5" fill="{I}" stroke="none"/><circle cx="232" cy="182" r="4.5" fill="{I}" stroke="none"/>
      </g></g>
      <path class="mouth" d="M196 214 C206 220 216 220 226 213"/>
      <path class="brows" d="M175 166 C181 162 188 162 194 165 M226 165 C232 162 239 162 245 166" stroke-width="2.5"/>
    </g>
  </g>
  <g class="angel">
    <g class="bob">
      <ellipse class="halo" cx="112" cy="194" rx="15" ry="4.5" stroke="{O}" stroke-width="3"/>
      <path class="wing wl" d="M98 236 C82 224 78 208 90 204 C98 202 102 212 104 222" fill="#fff"/>
      <path class="wing wr" d="M126 236 C142 224 146 208 134 204 C126 202 122 212 120 222" fill="#fff"/>
      <circle cx="112" cy="218" r="11" fill="#fff"/>
      <path d="M100 262 L104 234 H120 L124 262Z" fill="#fff"/>
      <g class="blink"><circle cx="108" cy="217" r="1.7" fill="{I}" stroke="none"/><circle cx="116" cy="217" r="1.7" fill="{I}" stroke="none"/></g>
      <path d="M108 223 C110 225 114 225 116 223" stroke-width="2"/>
    </g>
  </g>
  <g class="devil">
    <g class="bob">
      <path d="M298 206 L292 190 L304 202 M318 202 L330 190 L324 206" fill="{O}" stroke="{O}"/>
      <path class="tail" d="M323 252 C340 252 342 236 334 232 L340 226 L330 228" stroke="{O}"/>
      <circle cx="311" cy="218" r="11" fill="{O}" stroke="{O}"/>
      <path d="M299 262 L303 234 H319 L323 262Z" fill="{O}" stroke="{O}"/>
      <g class="blink"><circle cx="307" cy="217" r="1.7" fill="#fff" stroke="none"/><circle cx="315" cy="217" r="1.7" fill="#fff" stroke="none"/></g>
      <path d="M306 222 C309 225 313 225 316 222 L318 219" stroke="#fff" stroke-width="2"/>
    </g>
  </g>
</svg>'''

def mini(side):
    """Caritas para el marcador del juego."""
    if side == "angel":
        return (f'<svg viewBox="0 0 40 40" aria-hidden="true" fill="#fff" stroke="{I}" stroke-width="2.5">'
                f'<ellipse cx="20" cy="7" rx="9" ry="3" fill="none" stroke="{O}"/><circle cx="20" cy="23" r="12"/>'
                f'<circle cx="16" cy="22" r="1.5" fill="{I}" stroke="none"/><circle cx="24" cy="22" r="1.5" fill="{I}" stroke="none"/></svg>')
    return (f'<svg viewBox="0 0 40 40" aria-hidden="true" fill="{O}" stroke="{O}" stroke-width="2.5">'
            f'<path d="M10 14 L8 4 L16 11 M30 14 L32 4 L24 11"/><circle cx="20" cy="23" r="12"/>'
            f'<circle cx="16" cy="22" r="1.5" fill="#fff" stroke="none"/><circle cx="24" cy="22" r="1.5" fill="#fff" stroke="none"/></svg>')
