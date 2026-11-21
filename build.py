"""Borrador de carlospitta.com. Genera ./site/ (español). Contenido y plantilla en un solo lugar."""
import pathlib, html, re
from art import PILLAR_ICONS, hero_scene

OUT = pathlib.Path(__file__).parent / "site"
E = html.escape
EMAIL = "carlos.pitta@uach.cl"   # por confirmar con Carlos

NAV = [("index.html", "1% happier"), ("investigacion.html", "Investigación"),
       ("docencia.html", "Docencia"), ("sobre-mi.html", "Sobre mí")]

PILLARS = [
 ("Salud y belleza",
  "Nuestras abuelas tenían razón: salud, dinero y amor. Sin salud no se disfruta nada más. La genética no se elige, pero el carisma sí se cultiva.",
  None),
 ("Dinero y finanzas",
  "Ser pobre es carísimo, y endeudarse por impaciencia es el camino más corto para serlo. Si dominas tu impaciencia, el interés compuesto empieza a trabajar para ti.",
  "Antes de comprar a crédito, pregúntate cuánto te costaría esperar un mes."),
 ("Procrastinación",
  "Si encontraras la lámpara de Aladino, ¿pedirías ser feliz? En experimentos, casi nadie lo pide hasta que alguien se lo recuerda. Postergamos la felicidad porque no la definimos.",
  "Escribe hoy, en una sola línea, qué significa para ti ser feliz."),
 ("Flujo",
  "Compararnos con los demás nos roba la calma; dominar algo nos la devuelve. El flujo, perderse en una tarea exigente, es lo que permite dedicar años a ser excelente.",
  None),
 ("Amor",
  "Somos animales sociales: los lazos cercanos, románticos o no, están entre lo que más felicidad reporta. Como todo bien, el afecto se valora mejor cuando no se sobreofrece, ni se raciona.",
  None),
 ("Control",
  "Aceptar lo que no controlas es liberador. No es resignación: es poner tu energía donde de verdad decides.",
  "Separa en dos columnas lo que te preocupa: lo que depende de ti y lo que no."),
 ("Confianza, perdón y gratitud",
  "La desconfianza sale cara para la salud y para las relaciones. Saber perdonar y agradecer está entre lo que mejor anticipa la felicidad a largo plazo.",
  "Antes de dormir, anota tres cosas que agradeces del día."),
 ("Propósito (ikigai)",
  "«Haz lo que amas y nunca trabajarás» es un mal consejo. El propósito aparece donde se cruzan lo que amas, lo que haces bien, lo que el mundo necesita y aquello por lo que te pagarían.",
  None),
 ("Consciencia",
  "La fuerza de voluntad es un recurso escaso. No puedes controlarla directamente, pero sí tu respiración, y eso ya cambia algo.",
  "Tres minutos de respiración lenta antes de una decisión importante."),
 ("Espiritualidad",
  "La pregunta más difícil de todas: qué es la conciencia. Es una frontera donde la economía experimental empieza a tener algo que decir.",
  None),
]

def shell(active, title, body):
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{E(t)}</a></li>' for h, t in NAV)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="Carlos R. Pitta, economista. 1% happier: economía del comportamiento al servicio de una vida un poco más feliz.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,400&family=Schibsted+Grotesk:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Ir al contenido</a>
<header class="top">
  <a class="name" href="index.html">Carlos R. Pitta</a>
  <nav aria-label="Secciones"><ul>{nav}</ul></nav>
  <a class="lang" href="#" title="Versión en inglés: próximamente" aria-disabled="true">EN</a>
</header>
<main id="main">
{body}
</main>
<footer>
  <p>Carlos R. Pitta, PhD · Instituto de Gestión e Industria, Universidad Austral de Chile, Sede Puerto Montt</p>
  <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</footer>
</body>
</html>
'''

def home():
    rows = []
    for i, (name, idea, try_) in enumerate(PILLARS, 1):
        t = f'<p class="try"><span>Pruébalo</span> {E(try_)}</p>' if try_ else ""
        rows.append(f"""<li class="pillar">
  <div class="pic">{PILLAR_ICONS[i-1]}<span class="n" aria-hidden="true">{i:02d}</span></div>
  <div><h3>{E(name)}</h3><p>{E(idea)}</p>{t}</div>
</li>""")
    body = f"""
<section class="hero">
  <div class="hero-text">
    <h1><span class="one">1%</span> <span class="word">happier</span></h1>
    <p class="lede">Los economistas pensamos en el margen. La felicidad también se gana ahí: no con una revolución, sino con decisiones un poco mejores, todos los días.</p>
    <p class="cta"><a class="btn" href="#pilares">Conoce los diez pilares</a> <a class="btn ghost" href="#impaciencia">¿Quién gana en ti?</a></p>
  </div>
  <figure class="stage" aria-label="Un angelito y un diablito discuten en tus hombros">
    {hero_scene()}
    <p class="bubble b-angel" aria-live="polite"><span class="who">Angelito</span><span class="say" id="say-angel">Espera un mes. Si todavía lo quieres, cómpralo.</span></p>
    <p class="bubble b-devil" aria-live="polite"><span class="who">Diablito</span><span class="say" id="say-devil">Cómpralo ahora. A crédito, total…</span></p>
    <button class="next" type="button" id="next-temptation">Otra tentación</button>
  </figure>
</section>

<section class="why">
  <p class="big">+300<span>millones</span></p>
  <div>
    <p class="why-lede">de personas viven con depresión, la primera causa de mala salud y discapacidad en el mundo. Y casi la mitad no recibe tratamiento, incluso en los países ricos.</p>
    <p class="source">Organización Mundial de la Salud, 2017.</p>
    <p>La infelicidad es también un problema económico. Por eso un economista se pregunta qué decisiones, pequeñas y repetidas, nos hacen vivir mejor. Este sitio no reemplaza la ayuda profesional: si lo estás pasando mal, busca apoyo.</p>
  </div>
</section>

<section class="voices" id="impaciencia">
  <div class="voices-text">
    <h2>¿Quién gana en ti?</h2>
    <p>La economía clásica supone que siempre escuchas al angelito: que decides con calma, con toda la información y pensando en tu yo del futuro. La economía del comportamiento estudia por qué tantas veces gana el diablito.</p>
    <p>Su arma favorita es la impaciencia. Mídela en tres preguntas.</p>
  </div>
  <div class="game" id="game">
    <p class="q" id="q">¿Qué prefieres?</p>
    <div class="choices">
      <button type="button" class="choice" data-pick="now"><span>Hoy</span><strong>$100.000</strong></button>
      <button type="button" class="choice" data-pick="later"><span>En un mes</span><strong id="later-amt">$110.000</strong></button>
    </div>
    <p class="step" id="step">Pregunta 1 de 3</p>
    <div class="result" id="result" hidden>
      <p class="verdict" id="verdict"></p>
      <p id="explain"></p>
      <p><a href="#pilar-2">Lee el pilar 02, dinero y finanzas</a> · <button type="button" class="link" id="again">Jugar de nuevo</button></p>
    </div>
  </div>
</section>

<section id="pilares" class="pillars">
  <div class="section-head">
    <h2>Diez pilares de la felicidad</h2>
    <p>Lo que la economía del comportamiento, la psicología y la experimentación han aprendido sobre una vida más feliz, destilado en diez ideas.</p>
  </div>
  <ol class="pillar-list">{"".join(rows)}</ol>
</section>

<section class="offer">
  <h2>¿Quieres llevar esto más lejos?</h2>
  <div class="offer-grid">
    <div><h3>Charlas y talleres</h3><p>Para equipos, empresas, colegios y organizaciones que quieren tomar mejores decisiones y vivir mejor con ellas.</p><p><a href="mailto:{EMAIL}?subject=Charla%20o%20taller%201%25%20happier">Escríbeme a {EMAIL}</a></p></div>
    <div><h3>Una idea por semana</h3><p>Un correo corto con una idea de la economía del comportamiento y una forma de aplicarla.</p><p class="soon">Próximamente</p></div>
    <div><h3>La ciencia detrás</h3><p>Experimentos en Chile, México e India sobre felicidad, decisiones y comportamiento.</p><p><a href="investigacion.html">Ver la investigación</a></p></div>
  </div>
</section>
<script>{SCRIPT}</script>
"""
    n = iter(range(1, 11))
    body = re.sub(r'<li class="pillar">', lambda m: f'<li class="pillar" id="pilar-{next(n)}">', body)
    return shell("index.html", "1% happier — Carlos R. Pitta", body)

SCRIPT = r"""
(function(){
  var pairs=[
    ["Cómpralo ahora. A crédito, total…","Espera un mes. Si todavía lo quieres, cómpralo."],
    ["Mañana empiezas. Hoy, otro capítulo.","Cinco minutos hoy valen más que una hora el lunes."],
    ["Mira lo que tiene tu vecino.","Mira todo lo que ya tienes tú."],
    ["Respóndele ahora, con todo.","Respira tres veces antes de contestar."]
  ], k=0;
  var d=document.getElementById('say-devil'), a=document.getElementById('say-angel');
  document.getElementById('next-temptation').addEventListener('click',function(){
    k=(k+1)%pairs.length; d.textContent=pairs[k][0]; a.textContent=pairs[k][1];
  });
  var later=[110000,125000,150000], r=0;
  var amt=document.getElementById('later-amt'), step=document.getElementById('step'),
      res=document.getElementById('result'), v=document.getElementById('verdict'),
      ex=document.getElementById('explain'), ch=document.querySelector('#game .choices'), q=document.getElementById('q');
  function fmt(n){return '$'+n.toLocaleString('es-CL');}
  function show(title,text){ch.hidden=true;step.hidden=true;q.hidden=true;res.hidden=false;v.textContent=title;ex.textContent=text;}
  var out={
    0:["Gana el angelito.","Esperaste por un 10% más. Tu impaciencia equivale a menos de 10% al mes. Ojo: 10% mensual ya es más de 200% al año."],
    1:["Empate técnico.","Esperaste por un 25% más, pero no por un 10%. Tu impaciencia está entre 10% y 25% al mes: entre unos 200% y 1.300% al año."],
    2:["Gana el diablito, por poco.","Solo esperaste por un 50% más. Tu impaciencia está entre 25% y 50% al mes: más de 1.300% al año."],
    3:["Gana el diablito.","Ni un 50% más te hizo esperar. Tu impaciencia supera el 50% al mes. Quien te preste para comprar hoy sabe exactamente cuánto vale tu prisa."]
  };
  ch.addEventListener('click',function(e){
    var b=e.target.closest('.choice'); if(!b) return;
    if(b.dataset.pick==='later'){ show(out[r][0],out[r][1]); return; }
    r++; if(r>=later.length){ show(out[3][0],out[3][1]); return; }
    amt.textContent=fmt(later[r]); step.textContent='Pregunta '+(r+1)+' de 3';
  });
  document.getElementById('again').addEventListener('click',function(){
    r=0; amt.textContent=fmt(later[0]); step.textContent='Pregunta 1 de 3';
    ch.hidden=false; step.hidden=false; q.hidden=false; res.hidden=true;
  });
})();
"""

def stub(href, title, intro, items_html):
    body = f'''<section class="page">
  <h1 class="page-title">{E(title)}</h1>
  <p class="lede">{E(intro)}</p>
  {items_html}
  <p class="draft-note">Borrador: esta sección se completa en la próxima versión.</p>
</section>'''
    return shell(href, f"{title} — Carlos R. Pitta", body)

def research():
    lines = [
      ("Felicidad y bienestar", "Qué hace felices a las personas y cómo se mide: experimentos en India y México, juegos del dictador y datos de felicidad."),
      ("Macroeconomía conductual", "Cómo las expectativas y los sesgos de las personas se agregan en la economía."),
      ("Migración", "Brechas de ingreso entre migrantes y nativos con datos de migración mexicana."),
      ("Crimen y miedo", "Cuánto aumenta la victimización el miedo al delito, con un panel chileno de seis olas."),
    ]
    items = '<ul class="lines">' + "".join(f"<li><h3>{E(a)}</h3><p>{E(b)}</p></li>" for a, b in lines) + "</ul>"
    pubs = '''<h2>Publicaciones</h2><ul class="pubs">
<li>Pitta, C. R. (2014). Counterfactual decomposition analysis of immigrants-natives earnings using Mexican migration data. <i>Papers and Proceedings of the Journal of International Business and Economy</i>, 15(1).</li>
<li>Pitta, C. R., Spreen, T. H. y Kilmer, R. L. (2007). Non-homogeneous products and the law of one price. <i>Agribusiness</i>, 23(3).</li>
<li>Pitta, C. R. (2019). <i>Essays on the economic impacts of Huanglongbing on Florida’s citrus industry</i>. Tesis doctoral, University of Florida.</li></ul>'''
    return stub("investigacion.html", "Investigación", "Economía del comportamiento y experimental, con la felicidad como hilo conductor.", items + pubs)

def teaching():
    items = '''<ul class="lines">
<li><h3>Macroeconomía</h3><p>Introducción a la economía, Macroeconomía I y II.</p></li>
<li><h3>Econometría</h3><p>Econometría I y II, con laboratorios sobre datos chilenos.</p></li>
<li><h3>Organización industrial y teoría de juegos</h3><p>Estrategia, competencia y decisiones interdependientes.</p></li>
<li><h3>Economía de la felicidad</h3><p>Clase magistral y curso en desarrollo, de donde nacen los diez pilares.</p></li></ul>'''
    return stub("docencia.html", "Docencia", "Enseño economía en la Universidad Austral de Chile, Sede Puerto Montt. Reconocimiento a la Calidad Docente 2021 del Instituto de Gestión e Industria.", items)

def about():
    items = f'''<div class="bio">
<p>Soy economista mexicano y vivo en el sur de Chile. Estudié Economía en la Universidad Veracruzana, Macroeconomía Aplicada en la Pontificia Universidad Católica de Chile, y la maestría y el doctorado en la Universidad de Florida.</p>
<p>Desde 2011 soy académico del Instituto de Gestión e Industria de la Universidad Austral de Chile, en Puerto Montt. Antes enseñé en la Universidad Diego Portales, la Universidad de Concepción y la Universidad de Florida, y he sido profesor visitante en programas de MBA en Perú, Paraguay y México.</p>
<p>Escríbeme a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    return stub("sobre-mi.html", "Sobre mí", "Economista del comportamiento, profesor y divulgador.", items)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = {"index.html": home(), "investigacion.html": research(),
             "docencia.html": teaching(), "sobre-mi.html": about()}
    for n, h in pages.items():
        (OUT / n).write_text(h, encoding="utf-8")
    print("ok", list(pages))

if __name__ == "__main__":
    main()
