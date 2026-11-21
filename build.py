"""Genera carlospitta.com en español (raíz) e inglés (/en/) desde un solo contenido.

Uso: python3 build.py  ->  escribe en ./site/
"""
import pathlib, html, re, json
from urllib.parse import quote
from art import PILLAR_ICONS, hero_scene

OUT = pathlib.Path(__file__).parent / "site"
E = html.escape
EMAIL = "carlos.pitta@uach.cl"   # por confirmar con Carlos

# Páginas: clave interna -> archivo en cada idioma
PAGES = {"home": {"es": "index.html", "en": "index.html"},
         "research": {"es": "investigacion.html", "en": "research.html"},
         "teaching": {"es": "docencia.html", "en": "teaching.html"},
         "about": {"es": "sobre-mi.html", "en": "about.html"}}

T = {
"es": {
 "dir": "", "css": "style.css", "other": "en", "other_label": "EN", "other_title": "English version",
 "nav": [("home", "1% happier"), ("research", "Investigación"), ("teaching", "Docencia"), ("about", "Sobre mí")],
 "nav_label": "Secciones", "skip": "Ir al contenido",
 "desc": "Carlos R. Pitta, economista. 1% happier: economía del comportamiento al servicio de una vida un poco más feliz.",
 "footer": "Carlos R. Pitta, PhD · Instituto de Gestión e Industria, Universidad Austral de Chile, Sede Puerto Montt",
 "lede": "Los economistas pensamos en el margen. La felicidad también se gana ahí: no con una revolución, sino con decisiones un poco mejores, todos los días.",
 "cta1": "Conoce los diez pilares", "cta2": "¿Quién gana en ti?",
 "stage_label": "Un angelito y un diablito discuten en tus hombros",
 "angel": "Angelito", "devil": "Diablito", "next": "Otra tentación",
 "pairs": [["Cómpralo ahora. A crédito, total…", "Espera un mes. Si todavía lo quieres, cómpralo."],
           ["Mañana empiezas. Hoy, otro capítulo.", "Cinco minutos hoy valen más que una hora el lunes."],
           ["Mira lo que tiene tu vecino.", "Mira todo lo que ya tienes tú."],
           ["Respóndele ahora, con todo.", "Respira tres veces antes de contestar."]],
 "big_unit": "millones",
 "why_lede": "de personas viven con depresión, la primera causa de mala salud y discapacidad en el mundo. Y casi la mitad no recibe tratamiento, incluso en los países ricos.",
 "why_src": "Organización Mundial de la Salud, 2017.",
 "why_body": "La infelicidad es también un problema económico. Por eso un economista se pregunta qué decisiones, pequeñas y repetidas, nos hacen vivir mejor. Este sitio no reemplaza la ayuda profesional: si lo estás pasando mal, busca apoyo.",
 "voices_h": "¿Quién gana en ti?",
 "voices_p1": "La economía clásica supone que siempre escuchas al angelito: que decides con calma, con toda la información y pensando en tu yo del futuro. La economía del comportamiento estudia por qué tantas veces gana el diablito.",
 "voices_p2": "Su arma favorita es la impaciencia. Mídela en tres preguntas.",
 "q": "¿Qué prefieres?", "now": "Hoy", "later": "En un mes",
 "amounts": [100000, 110000, 125000, 150000], "locale": "es-CL",
 "step": "Pregunta {n} de 3", "read_p2": "Lee el pilar 02, dinero y finanzas", "again": "Jugar de nuevo",
 "out": [["Gana el angelito.", "Esperaste por un 10% más. Tu impaciencia equivale a menos de 10% al mes. Ojo: 10% mensual ya es más de 200% al año."],
         ["Empate técnico.", "Esperaste por un 25% más, pero no por un 10%. Tu impaciencia está entre 10% y 25% al mes: entre unos 200% y 1.300% al año."],
         ["Gana el diablito, por poco.", "Solo esperaste por un 50% más. Tu impaciencia está entre 25% y 50% al mes: más de 1.300% al año."],
         ["Gana el diablito.", "Ni un 50% más te hizo esperar. Tu impaciencia supera el 50% al mes. Quien te preste para comprar hoy sabe exactamente cuánto vale tu prisa."]],
 "pillars_h": "Diez pilares de la felicidad",
 "pillars_p": "Lo que la economía del comportamiento, la psicología y la experimentación han aprendido sobre una vida más feliz, destilado en diez ideas.",
 "try": "Pruébalo",
 "pillars": [
  ("Salud y belleza", "Nuestras abuelas tenían razón: salud, dinero y amor. Sin salud no se disfruta nada más. La genética no se elige, pero el carisma sí se cultiva.", None),
  ("Dinero y finanzas", "Ser pobre es carísimo, y endeudarse por impaciencia es el camino más corto para serlo. Si dominas tu impaciencia, el interés compuesto empieza a trabajar para ti.", "Antes de comprar a crédito, pregúntate cuánto te costaría esperar un mes."),
  ("Procrastinación", "Si encontraras la lámpara de Aladino, ¿pedirías ser feliz? En experimentos, casi nadie lo pide hasta que alguien se lo recuerda. Postergamos la felicidad porque no la definimos.", "Escribe hoy, en una sola línea, qué significa para ti ser feliz."),
  ("Flujo", "Compararnos con los demás nos roba la calma; dominar algo nos la devuelve. El flujo, perderse en una tarea exigente, es lo que permite dedicar años a ser excelente.", None),
  ("Amor", "Somos animales sociales: los lazos cercanos, románticos o no, están entre lo que más felicidad reporta. Como todo bien, el afecto se valora mejor cuando no se sobreofrece, ni se raciona.", None),
  ("Control", "Aceptar lo que no controlas es liberador. No es resignación: es poner tu energía donde de verdad decides.", "Separa en dos columnas lo que te preocupa: lo que depende de ti y lo que no."),
  ("Confianza, perdón y gratitud", "La desconfianza sale cara para la salud y para las relaciones. Saber perdonar y agradecer está entre lo que mejor anticipa la felicidad a largo plazo.", "Antes de dormir, anota tres cosas que agradeces del día."),
  ("Propósito (ikigai)", "«Haz lo que amas y nunca trabajarás» es un mal consejo. El propósito aparece donde se cruzan lo que amas, lo que haces bien, lo que el mundo necesita y aquello por lo que te pagarían.", None),
  ("Consciencia", "La fuerza de voluntad es un recurso escaso. No puedes controlarla directamente, pero sí tu respiración, y eso ya cambia algo.", "Tres minutos de respiración lenta antes de una decisión importante."),
  ("Espiritualidad", "La pregunta más difícil de todas: qué es la conciencia. Es una frontera donde la economía experimental empieza a tener algo que decir.", None)],
 "offer_h": "¿Quieres llevar esto más lejos?",
 "offer": [("Charlas y talleres", "Para equipos, empresas, colegios y organizaciones que quieren tomar mejores decisiones y vivir mejor con ellas.", "mail", "Escríbeme a "),
           ("Una idea por semana", "Un correo corto con una idea de la economía del comportamiento y una forma de aplicarla.", "soon", "Próximamente"),
           ("La ciencia detrás", "Experimentos en Chile, México e India sobre felicidad, decisiones y comportamiento.", "research", "Ver la investigación")],
 "mail_subject": "Charla o taller 1% happier",
 "draft": "Borrador: esta sección se completa en la próxima versión.",
 "research_t": "Investigación", "research_i": "Economía del comportamiento y experimental, con la felicidad como hilo conductor.",
 "lines": [("Felicidad y bienestar", "Qué hace felices a las personas y cómo se mide: experimentos en India y México, juegos del dictador y datos de felicidad."),
           ("Macroeconomía conductual", "Cómo las expectativas y los sesgos de las personas se agregan en la economía."),
           ("Migración", "Brechas de ingreso entre migrantes y nativos con datos de migración mexicana."),
           ("Crimen y miedo", "Cuánto aumenta la victimización el miedo al delito, con un panel chileno de seis olas.")],
 "pubs_h": "Publicaciones", "and": "y", "thesis": "Tesis doctoral",
 "teaching_t": "Docencia", "teaching_i": "Enseño economía en la Universidad Austral de Chile, Sede Puerto Montt. Reconocimiento a la Calidad Docente 2021 del Instituto de Gestión e Industria.",
 "courses": [("Macroeconomía", "Introducción a la economía, Macroeconomía I y II."),
             ("Econometría", "Econometría I y II, con laboratorios sobre datos chilenos."),
             ("Organización industrial y teoría de juegos", "Estrategia, competencia y decisiones interdependientes."),
             ("Economía de la felicidad", "Clase magistral y curso en desarrollo, de donde nacen los diez pilares.")],
 "about_t": "Sobre mí", "about_i": "Economista del comportamiento, profesor y divulgador.",
 "bio": ["Soy economista mexicano y vivo en el sur de Chile. Estudié Economía en la Universidad Veracruzana, Macroeconomía Aplicada en la Pontificia Universidad Católica de Chile, y la maestría y el doctorado en la Universidad de Florida.",
         "Desde 2011 soy académico del Instituto de Gestión e Industria de la Universidad Austral de Chile, en Puerto Montt. Antes enseñé en la Universidad Diego Portales, la Universidad de Concepción y la Universidad de Florida, y he sido profesor visitante en programas de MBA en Perú, Paraguay y México."],
 "write_me": "Escríbeme a ",
},
"en": {
 "dir": "en/", "css": "../style.css", "other": "es", "other_label": "ES", "other_title": "Versión en español",
 "nav": [("home", "1% happier"), ("research", "Research"), ("teaching", "Teaching"), ("about", "About")],
 "nav_label": "Sections", "skip": "Skip to content",
 "desc": "Carlos R. Pitta, economist. 1% happier: behavioral economics for a slightly happier life.",
 "footer": "Carlos R. Pitta, PhD · Instituto de Gestión e Industria, Universidad Austral de Chile, Puerto Montt",
 "lede": "Economists think at the margin. Happiness is won there too: not with a revolution, but with slightly better decisions, every day.",
 "cta1": "Meet the ten pillars", "cta2": "Who wins in you?",
 "stage_label": "A little angel and a little devil argue on your shoulders",
 "angel": "Angel", "devil": "Devil", "next": "Another temptation",
 "pairs": [["Buy it now. Put it on credit…", "Wait a month. If you still want it, buy it."],
           ["Start tomorrow. One more episode tonight.", "Five minutes today beat an hour on Monday."],
           ["Look at what your neighbor has.", "Look at everything you already have."],
           ["Reply right now. Let them have it.", "Take three breaths before you answer."]],
 "big_unit": "million",
 "why_lede": "people live with depression, the leading cause of ill health and disability worldwide. Nearly half receive no treatment, even in rich countries.",
 "why_src": "World Health Organization, 2017.",
 "why_body": "Unhappiness is also an economic problem. So an economist asks which small, repeated decisions help us live better. This site is not a substitute for professional help: if you are struggling, reach out for support.",
 "voices_h": "Who wins in you?",
 "voices_p1": "Classical economics assumes you always listen to the angel: that you decide calmly, with full information, thinking of your future self. Behavioral economics studies why the devil wins so often.",
 "voices_p2": "Its favorite weapon is impatience. Measure yours in three questions.",
 "q": "Which would you rather have?", "now": "Today", "later": "In one month",
 "amounts": [100, 110, 125, 150], "locale": "en-US",
 "step": "Question {n} of 3", "read_p2": "Read pillar 02, money and finance", "again": "Play again",
 "out": [["The angel wins.", "You waited for 10% more. Your impatience is below 10% a month. Careful: 10% a month is already more than 200% a year."],
         ["A close call.", "You waited for 25% more, but not for 10%. Your impatience is between 10% and 25% a month: roughly 200% to 1,300% a year."],
         ["The devil wins, barely.", "You only waited for 50% more. Your impatience is between 25% and 50% a month: over 1,300% a year."],
         ["The devil wins.", "Not even 50% more made you wait. Your impatience is above 50% a month. Whoever lends you money to buy today knows exactly what your hurry is worth."]],
 "pillars_h": "Ten pillars of happiness",
 "pillars_p": "What behavioral economics, psychology and experiments have learned about a happier life, distilled into ten ideas.",
 "try": "Try this",
 "pillars": [
  ("Health and beauty", "Our grandmothers were right: health, money and love. Without health, nothing else can be enjoyed. You can't choose your genes, but charisma can be cultivated.", None),
  ("Money and finance", "Being poor is expensive, and borrowing out of impatience is the fastest way to get there. Master your impatience and compound interest starts working for you.", "Before buying on credit, ask what it would cost you to wait a month."),
  ("Procrastination", "If you found Aladdin's lamp, would you wish to be happy? In experiments, almost nobody does until someone reminds them. We postpone happiness because we never define it.", "Write today, in one line, what being happy means to you."),
  ("Flow", "Comparing ourselves with others steals our calm; mastering something gives it back. Flow, losing yourself in a demanding task, is what makes years of practice possible.", None),
  ("Love", "We are social animals: close bonds, romantic or not, are among the strongest sources of happiness. Like any good, affection is valued best when it is neither oversupplied nor rationed.", None),
  ("Control", "Accepting what you cannot control is liberating. It is not resignation: it is putting your energy where you actually decide.", "Split your worries into two columns: what depends on you and what doesn't."),
  ("Trust, forgiveness and gratitude", "Distrust is costly for health and relationships. Being able to forgive and to be grateful are among the best predictors of long-run happiness.", "Before bed, write down three things you are grateful for today."),
  ("Purpose (ikigai)", "'Do what you love and you'll never work a day' is bad advice. Purpose appears where what you love, what you are good at, what the world needs and what you can be paid for meet.", None),
  ("Awareness", "Willpower is a scarce resource. You can't control it directly, but you can control your breathing, and that already changes something.", "Three minutes of slow breathing before an important decision."),
  ("Spirituality", "The hardest question of all: what is consciousness? It is a frontier where experimental economics is starting to have something to say.", None)],
 "offer_h": "Want to take this further?",
 "offer": [("Talks and workshops", "For teams, companies, schools and organizations that want to make better decisions and live better with them.", "mail", "Write to me at "),
           ("One idea a week", "A short email with one idea from behavioral economics and a way to use it.", "soon", "Coming soon"),
           ("The science behind it", "Experiments in Chile, Mexico and India on happiness, decisions and behavior.", "research", "See the research")],
 "mail_subject": "1% happier talk or workshop",
 "draft": "Draft: this section will be completed in the next version.",
 "research_t": "Research", "research_i": "Behavioral and experimental economics, with happiness as the common thread.",
 "lines": [("Happiness and well-being", "What makes people happy and how to measure it: experiments in India and Mexico, dictator games and happiness data."),
           ("Behavioral macroeconomics", "How people's expectations and biases add up across the economy."),
           ("Migration", "Earnings gaps between migrants and natives, using Mexican migration data."),
           ("Crime and fear", "How much victimization raises fear of crime, using a six-wave Chilean panel.")],
 "pubs_h": "Publications", "and": "and", "thesis": "PhD dissertation",
 "teaching_t": "Teaching", "teaching_i": "I teach economics at Universidad Austral de Chile in Puerto Montt. Teaching Quality Award 2021, Instituto de Gestión e Industria.",
 "courses": [("Macroeconomics", "Introduction to economics, Macroeconomics I and II."),
             ("Econometrics", "Econometrics I and II, with weekly labs on Chilean data."),
             ("Industrial organization and game theory", "Strategy, competition and interdependent decisions."),
             ("Economics of happiness", "Master lecture and course in development, where the ten pillars come from.")],
 "about_t": "About", "about_i": "Behavioral economist, teacher and science communicator.",
 "bio": ["I am a Mexican economist living in southern Chile. I studied economics at Universidad Veracruzana and applied macroeconomics at Pontificia Universidad Católica de Chile, and earned my MS and PhD at the University of Florida.",
         "Since 2011 I have been on the faculty of the Instituto de Gestión e Industria at Universidad Austral de Chile in Puerto Montt. Before that I taught at Universidad Diego Portales, Universidad de Concepción and the University of Florida, and I have been a visiting professor in MBA programs in Peru, Paraguay and Mexico."],
 "write_me": "Write to me at ",
},
}

def href(lang, key, from_lang=None):
    """Enlace a la página `key` en `lang`, visto desde una página en `from_lang`."""
    from_lang = from_lang or lang
    f = PAGES[key][lang]
    if lang == from_lang:
        return f
    return ("en/" + f) if lang == "en" else ("../" + f)

def shell(lang, key, title, body):
    t = T[lang]
    nav = "".join(
        f'<li><a href="{href(lang, k)}"{" aria-current=\"page\"" if k == key else ""}>{E(lbl)}</a></li>'
        for k, lbl in t["nav"])
    other = t["other"]
    alt = f'https://carlospitta.com/{T[other]["dir"]}{PAGES[key][other]}'.replace("/index.html", "/")
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(t["desc"])}">
<link rel="alternate" hreflang="{other}" href="{alt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,400&family=Schibsted+Grotesk:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{t["css"]}">
</head>
<body>
<a class="skip" href="#main">{E(t["skip"])}</a>
<header class="top">
  <a class="name" href="{href(lang, "home")}">Carlos R. Pitta</a>
  <nav aria-label="{E(t["nav_label"])}"><ul>{nav}</ul></nav>
  <a class="lang" href="{href(other, key, lang)}" hreflang="{other}" lang="{other}" title="{E(t["other_title"])}">{t["other_label"]}</a>
</header>
<main id="main">
{body}
</main>
<footer>
  <p>{E(t["footer"])}</p>
  <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</footer>
</body>
</html>
'''

SCRIPT = r"""
(function(){
  var C=__CFG__, k=0;
  var d=document.getElementById('say-devil'), a=document.getElementById('say-angel');
  document.getElementById('next-temptation').addEventListener('click',function(){
    k=(k+1)%C.pairs.length; d.textContent=C.pairs[k][0]; a.textContent=C.pairs[k][1];
  });
  var later=C.amounts.slice(1), r=0;
  var amt=document.getElementById('later-amt'), step=document.getElementById('step'),
      res=document.getElementById('result'), v=document.getElementById('verdict'),
      ex=document.getElementById('explain'), ch=document.querySelector('#game .choices'), q=document.getElementById('q');
  function fmt(n){return '$'+n.toLocaleString(C.locale);}
  function st(n){return C.step.replace('{n}',n);}
  function show(o){ch.hidden=true;step.hidden=true;q.hidden=true;res.hidden=false;v.textContent=o[0];ex.textContent=o[1];}
  ch.addEventListener('click',function(e){
    var b=e.target.closest('.choice'); if(!b) return;
    if(b.dataset.pick==='later'){ show(C.out[r]); return; }
    r++; if(r>=later.length){ show(C.out[3]); return; }
    amt.textContent=fmt(later[r]); step.textContent=st(r+1);
  });
  document.getElementById('again').addEventListener('click',function(){
    r=0; amt.textContent=fmt(later[0]); step.textContent=st(1);
    ch.hidden=false; step.hidden=false; q.hidden=false; res.hidden=true;
  });
})();
"""

def money(n, locale):
    s = f"{n:,}"
    return "$" + (s.replace(",", ".") if locale == "es-CL" else s)

def home(lang):
    t = T[lang]
    rows = []
    for i, (name, idea, try_) in enumerate(t["pillars"], 1):
        tr = f'<p class="try"><span>{E(t["try"])}</span> {E(try_)}</p>' if try_ else ""
        rows.append(f'''<li class="pillar" id="p{i}">
  <div class="pic">{PILLAR_ICONS[i-1]}<span class="n" aria-hidden="true">{i:02d}</span></div>
  <div><h3>{E(name)}</h3><p>{E(idea)}</p>{tr}</div>
</li>''')
    offer = []
    for h, p, kind, lbl in t["offer"]:
        if kind == "mail":
            subj = quote(t["mail_subject"])
            link = f'<p><a href="mailto:{EMAIL}?subject={subj}">{E(lbl)}{EMAIL}</a></p>'
        elif kind == "soon":
            link = f'<p class="soon">{E(lbl)}</p>'
        else:
            link = f'<p><a href="{href(lang, "research")}">{E(lbl)}</a></p>'
        offer.append(f"<div><h3>{E(h)}</h3><p>{E(p)}</p>{link}</div>")
    cfg = json.dumps({"pairs": t["pairs"], "amounts": t["amounts"], "locale": t["locale"],
                      "step": t["step"], "out": t["out"]}, ensure_ascii=False)
    a = t["amounts"]
    body = f'''
<section class="hero">
  <div class="hero-text">
    <h1><span class="one">1%</span> <span class="word">happier</span></h1>
    <p class="lede">{E(t["lede"])}</p>
    <p class="cta"><a class="btn" href="#pilares">{E(t["cta1"])}</a> <a class="btn ghost" href="#impaciencia">{E(t["cta2"])}</a></p>
  </div>
  <figure class="stage" aria-label="{E(t["stage_label"])}">
    {hero_scene()}
    <p class="bubble b-angel" aria-live="polite"><span class="who">{E(t["angel"])}</span><span class="say" id="say-angel">{E(t["pairs"][0][1])}</span></p>
    <p class="bubble b-devil" aria-live="polite"><span class="who">{E(t["devil"])}</span><span class="say" id="say-devil">{E(t["pairs"][0][0])}</span></p>
    <button class="next" type="button" id="next-temptation">{E(t["next"])}</button>
  </figure>
</section>

<section class="why">
  <p class="big">+300<span>{E(t["big_unit"])}</span></p>
  <div>
    <p class="why-lede">{E(t["why_lede"])}</p>
    <p class="source">{E(t["why_src"])}</p>
    <p>{E(t["why_body"])}</p>
  </div>
</section>

<section class="voices" id="impaciencia">
  <div class="voices-text">
    <h2>{E(t["voices_h"])}</h2>
    <p>{E(t["voices_p1"])}</p>
    <p>{E(t["voices_p2"])}</p>
  </div>
  <div class="game" id="game">
    <p class="q" id="q">{E(t["q"])}</p>
    <div class="choices">
      <button type="button" class="choice" data-pick="now"><span>{E(t["now"])}</span><strong>{money(a[0], t["locale"])}</strong></button>
      <button type="button" class="choice" data-pick="later"><span>{E(t["later"])}</span><strong id="later-amt">{money(a[1], t["locale"])}</strong></button>
    </div>
    <p class="step" id="step">{E(t["step"].replace("{n}", "1"))}</p>
    <div class="result" id="result" hidden>
      <p class="verdict" id="verdict"></p>
      <p id="explain"></p>
      <p><a href="#p2">{E(t["read_p2"])}</a> · <button type="button" class="link" id="again">{E(t["again"])}</button></p>
    </div>
  </div>
</section>

<section id="pilares" class="pillars">
  <div class="section-head">
    <h2>{E(t["pillars_h"])}</h2>
    <p>{E(t["pillars_p"])}</p>
  </div>
  <ol class="pillar-list">{"".join(rows)}</ol>
</section>

<section class="offer">
  <h2>{E(t["offer_h"])}</h2>
  <div class="offer-grid">{"".join(offer)}</div>
</section>
<script>{SCRIPT.replace("__CFG__", cfg)}</script>
'''
    return shell(lang, "home", "1% happier — Carlos R. Pitta", body)

def inner(lang, key, title, intro, items_html):
    body = f'''<section class="page">
  <h1 class="page-title">{E(title)}</h1>
  <p class="lede">{E(intro)}</p>
  {items_html}
  <p class="draft-note">{E(T[lang]["draft"])}</p>
</section>'''
    return shell(lang, key, f"{title} — Carlos R. Pitta", body)

def research(lang):
    t = T[lang]
    items = '<ul class="lines">' + "".join(f"<li><h3>{E(a)}</h3><p>{E(b)}</p></li>" for a, b in t["lines"]) + "</ul>"
    pubs = f'''<h2>{E(t["pubs_h"])}</h2><ul class="pubs">
<li>Pitta, C. R. (2014). Counterfactual decomposition analysis of immigrants-natives earnings using Mexican migration data. <i>Papers and Proceedings of the Journal of International Business and Economy</i>, 15(1).</li>
<li>Pitta, C. R., Spreen, T. H. {t["and"]} Kilmer, R. L. (2007). Non-homogeneous products and the law of one price. <i>Agribusiness</i>, 23(3).</li>
<li>Pitta, C. R. (2019). <i>Essays on the economic impacts of Huanglongbing on Florida’s citrus industry</i>. {t["thesis"]}, University of Florida.</li></ul>'''
    return inner(lang, "research", t["research_t"], t["research_i"], items + pubs)

def teaching(lang):
    t = T[lang]
    items = '<ul class="lines">' + "".join(f"<li><h3>{E(a)}</h3><p>{E(b)}</p></li>" for a, b in t["courses"]) + "</ul>"
    return inner(lang, "teaching", t["teaching_t"], t["teaching_i"], items)

def about(lang):
    t = T[lang]
    items = '<div class="bio">' + "".join(f"<p>{E(p)}</p>" for p in t["bio"]) + \
            f'<p>{E(t["write_me"])}<a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'
    return inner(lang, "about", t["about_t"], t["about_i"], items)

def main():
    built = []
    for lang in ("es", "en"):
        d = OUT / T[lang]["dir"]
        d.mkdir(parents=True, exist_ok=True)
        for key, fn in (("home", home), ("research", research), ("teaching", teaching), ("about", about)):
            p = d / PAGES[key][lang]
            p.write_text(fn(lang), encoding="utf-8")
            built.append(str(p.relative_to(OUT)))
    print("ok", built)

if __name__ == "__main__":
    main()
