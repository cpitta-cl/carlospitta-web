"""Genera carlospitta.com (v2) en español (raíz) e inglés (/en/) desde content.py.

Uso: python3 build.py  ->  escribe HTML en ./site/  (los recursos estáticos ya viven ahí)
URLs limpias (sin .html): Cloudflare Pages las resuelve solo.
"""
import pathlib, html, json
from content import T, COURSES, OTHER_UNIS, NEWS, AGENDA, PUBS, EMAIL, PROFILES
from art import PILLAR_ICONS, LINE_ICONS, hero_scene, mini

OUT = pathlib.Path(__file__).parent / "site"
E = html.escape
BASE = "https://carlospitta.com"

URL = {"home": {"es": "/", "en": "/en/"},
       "research": {"es": "/investigacion", "en": "/en/research"},
       "teaching": {"es": "/docencia", "en": "/en/teaching"},
       "news": {"es": "/noticias", "en": "/en/news"},
       "contact": {"es": "/contacto", "en": "/en/contact"},
       "about": {"es": "/sobre-mi", "en": "/en/about"}}

def course_url(lang, slug):
    return ("/cursos/" if lang == "es" else "/en/courses/") + slug

def url_to_file(u):
    if u.endswith("/"):
        return OUT / u.lstrip("/") / "index.html"
    return OUT / (u.lstrip("/") + ".html")

DOC_ICON = ('<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="var(--ink)" stroke-width="2" stroke-linejoin="round">'
            '<path d="M8 3 H19 L25 9 V29 H8Z" fill="#fff"/><path d="M19 3 V9 H25"/><path d="M12 17 H21 M12 21 H21 M12 25 H17" stroke="var(--accent)"/></svg>')

ICONS = {
 "ORCID": '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="16" fill="#A6CE39"/><path d="M10.5 12.3h2.2v10.2h-2.2zM11.6 8.5a1.4 1.4 0 1 1 0 2.8 1.4 1.4 0 0 1 0-2.8zM15 12.3h5.6c3.4 0 5.2 2.4 5.2 5.1 0 2.9-2.1 5.1-5.3 5.1H15zm2.2 2v6.2h3.2c2.3 0 3.2-1.6 3.2-3.1 0-1.6-1-3.1-3.2-3.1z" fill="#fff"/></svg>',
 "ResearchGate": '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="#00CCBB"/><text x="16" y="21.5" text-anchor="middle" font-family="Georgia,serif" font-size="14" font-weight="700" fill="#fff">R<tspan font-size="9" dy="-5">G</tspan></text></svg>',
}

def profile_chips(cls="profiles"):
    return f'<ul class="{cls}">' + "".join(
        f'<li><a href="{u}" rel="me noopener" target="_blank">{ICONS[n]}{n}</a></li>'
        for n, u, h in PROFILES) + "</ul>"

def fmt_date(lang, d):
    t = T[lang]
    if len(d) == 4:
        return d
    y, m = d.split("-")
    mon = t["months"][int(m) - 1]
    return f"{mon} {y}" if lang == "es" else f"{mon} {y}"

# ------------------------------------------------------------------ armazón
def shell(lang, key, title, body, alt_url, cfg=None, desc=None):
    t = T[lang]
    other = t["other"]
    nav = "".join(
        f'<li><a href="{URL[k][lang]}"{" aria-current=\"page\"" if k == key else ""}>{E(lbl)}</a></li>'
        for k, lbl in t["nav"]) + f'<li class="m-only"><a href="{URL["contact"][lang]}">{E(t["contact_nav"])}</a></li>'
    foot_nav = "".join(f'<li><a href="{URL[k][lang]}">{E(lbl)}</a></li>' for k, lbl in t["nav"]) + \
        f'<li><a href="{URL["contact"][lang]}">{E(t["contact_nav"])}</a></li>'
    here = alt_url[lang]
    cfg_js = f'<script>window.CP={json.dumps(cfg, ensure_ascii=False)};</script>' if cfg else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc or t["desc"])}">
<link rel="canonical" href="{BASE}{here}">
<link rel="me" href="{PROFILES[0][1]}">
<link rel="alternate" hreflang="{lang}" href="{BASE}{here}">
<link rel="alternate" hreflang="{other}" href="{BASE}{alt_url[other]}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc or t["desc"])}">
<meta property="og:image" content="{BASE}/img/mx-lab-1.webp">
<meta name="theme-color" content="#1E1B57">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%231E1B57'/%3E%3Ctext x='50%25' y='58%25' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='30' fill='%23D9650A'%3E1%25%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,400&family=Schibsted+Grotesk:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script>document.documentElement.classList.add('js')</script>
{cfg_js}
<script src="/app.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{E(t["skip"])}</a>
<header class="top">
 <div class="top-in">
  <a class="name" href="{URL["home"][lang]}"><span class="dot" aria-hidden="true"></span>Carlos R. Pitta</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{E(t["menu"])}</button>
  <nav class="nav" id="nav" aria-label="{E(t["nav_label"])}"><ul>{nav}</ul></nav>
  <a class="lang" href="{alt_url[other]}" hreflang="{other}" lang="{other}" title="{E(t["other_title"])}">{t["other_label"]}</a>
  <a class="contact-btn" href="{URL["contact"][lang]}"{" aria-current=\"page\"" if key == "contact" else ""}>{E(t["contact_nav"])}</a>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
 <div class="foot-in">
  <div>
   <p class="say">{E(t["footer_cta"])}</p>
   <p><a class="mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
  <nav aria-label="{E(t["nav_label"])}"><ul>{foot_nav}</ul></nav>
 </div>
 <div class="foot-base"><p class="small">{E(t["footer_who"])} · {E(t["footer_where"])}</p></div>
</footer>
</body>
</html>
'''

def page_hero(title, lede, crumb=""):
    return f'''<section class="page-hero"><div class="wrap">{crumb}
  <h1>{E(title)}</h1>
  <p class="lede">{E(lede)}</p>
</div></section>'''

def news_items(lang, items):
    t = T[lang]
    out = []
    for n in items:
        h, p = n[lang]
        out.append(f'<li><div><time datetime="{n["date"]}">{E(fmt_date(lang, n["date"]))}</time><br>'
                   f'<span class="tag">{E(t["tags"][n["tag"]])}</span></div>'
                   f'<div><h3>{E(h)}</h3><p>{E(p)}</p></div></li>')
    return '<ul class="news-list">' + "".join(out) + "</ul>"

# ------------------------------------------------------------------ portada
def home(lang):
    t = T[lang]
    rows = []
    for i, (name, idea, try_) in enumerate(t["pillars"], 1):
        rows.append(f'''<li class="pillar" id="p{i}">
  <div class="pic">{PILLAR_ICONS[i-1]}<span class="n" aria-hidden="true">{i:02d}</span></div>
  <div><h3>{E(name)}</h3><p>{E(idea)}</p><p class="try"><span>{E(t["try"])}</span> {E(try_)}</p></div>
</li>''')
    offer = []
    for h, p, kind, lbl in t["offer"]:
        if kind == "contact":
            link = f'<p><a href="{URL["contact"][lang]}">{E(lbl)}</a></p>'
        elif kind == "soon":
            link = f'<p class="soon">{E(lbl)}</p>'
        else:
            link = f'<p><a href="{URL["research"][lang]}">{E(lbl)}</a></p>'
        offer.append(f"<div><h3>{E(h)}</h3><p>{E(p)}</p>{link}</div>")
    p0 = t["pairs"][0]
    q0 = t["quiz"][0]
    cfg = {"pairs": t["pairs"], "tcount": t["tcount"], "tpillar": t["tpillar"].replace("{p:02d}", "{p}"),
           "quiz": t["quiz"], "step": t["step"], "out": t["out"], "score": t["result_score"],
           "names": [p[0] for p in t["pillars"]], "pause": t["pause"], "play": t["play"]}
    body = f'''
<section class="hero">
 <div class="hero-in">
  <div class="hero-text">
    <h1><span class="one">1<i>%</i></span> <span class="word">happier</span></h1>
    <p class="lede">{E(t["lede"])}</p>
    <p class="cta"><a class="btn" href="#pilares">{E(t["cta1"])}</a> <a class="btn ghost" href="#juego">{E(t["cta2"])}</a></p>
  </div>
  <figure class="stage" id="stage" aria-label="{E(t["stage_label"])}">
    {hero_scene()}
    <p class="bubble b-angel"><span class="who">{E(t["angel"])}</span><span class="say" id="say-angel" aria-hidden="true">{E(p0[1])}</span></p>
    <p class="bubble b-devil"><span class="who">{E(t["devil"])}</span><span class="say" id="say-devil" aria-hidden="true">{E(p0[0])}</span></p>
    <p class="sr" aria-live="polite">{E(t["devil"])}: <span id="sr-devil">{E(p0[0])}</span> {E(t["angel"])}: <span id="sr-angel">{E(p0[1])}</span></p>
    <p class="tnav">
      <button type="button" class="pp" id="pp" aria-pressed="false" aria-label="{E(t["pause"])}">&#10073;&#10073;</button>
      <button type="button" id="next-temptation">{E(t["next"])}</button>
      <span class="prog" aria-hidden="true"><i></i></span>
      <span id="t-count">{E(t["tcount"].format(i=1, n=len(t["pairs"])))}</span> · <a id="t-pillar" href="#p{p0[2]}">{E(t["tpillar"].format(p=p0[2]))}</a>
    </p>
  </figure>
 </div>
</section>

<section class="band ink">
 <div class="wrap why-in">
  <p class="big">+300<span>{E(t["big_unit"])}</span></p>
  <div>
    <p class="why-lede">{E(t["why_lede"])}</p>
    <p class="source">{E(t["why_src"])}</p>
    <p>{E(t["why_body"])}</p>
  </div>
 </div>
</section>

<section class="band" id="juego">
 <div class="wrap voices-in">
  <div>
    <h2>{E(t["voices_h"])}</h2>
    <p>{E(t["voices_p1"])}</p>
    <p>{E(t["voices_p2"])}</p>
  </div>
  <div class="game" id="game">
    <div class="tally" aria-label="{E(t["tally"])}">
      <span style="display:flex;align-items:center;gap:.4rem">{mini("angel")}<b id="ta">0</b></span>
      <span class="tug" aria-hidden="true"><i id="tug"></i></span>
      <span style="display:flex;align-items:center;gap:.4rem"><b id="td">0</b>{mini("devil")}</span>
    </div>
    <p class="q" id="q">{E(q0[0])}</p>
    <div class="choices">
      <button type="button" class="choice" id="opt0" data-side="devil"><span>{E(q0[1][0])}</span><strong>{E(q0[1][1])}</strong></button>
      <button type="button" class="choice" id="opt1" data-side="angel"><span>{E(q0[2][0])}</span><strong>{E(q0[2][1])}</strong></button>
    </div>
    <p class="step" id="step">{E(t["step"].replace("{n}", "1"))} · {E(t["tpillar"].format(p=1))}</p>
    <div class="result" id="result" hidden>
      <p class="verdict" id="verdict" tabindex="-1"></p>
      <p id="score"></p>
      <p id="explain"></p>
      <p id="lost-h" class="lost-h">{E(t["lost_h"])}</p>
      <ul id="lost" class="lost"></ul>
      <p id="money" class="money" hidden>{E(t["money_note"])}</p>
      <p><button type="button" class="link" id="again">{E(t["again"])}</button></p>
    </div>
  </div>
 </div>
</section>

<section id="pilares" class="band white">
 <div class="wrap">
  <div class="head"><h2>{E(t["pillars_h"])}</h2><p>{E(t["pillars_p"])}</p></div>
  <ol class="pillar-list">{"".join(rows)}</ol>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <div class="head"><h2>{E(t["field_h"])}</h2><p>{E(t["field_p"])}</p></div>
  <div class="field-grid">
    <figure class="tall"><img src="/img/mx-lab-1.webp" alt="" loading="lazy" width="1400" height="1050"><figcaption>{E(t["field_mx"])}</figcaption></figure>
    <figure><img src="/img/in-ghats-s.webp" alt="" loading="lazy"><figcaption>{E(t["field_in"])}</figcaption></figure>
    <figure><img src="/img/mx-lab-2-s.webp" alt="" loading="lazy"></figure>
    <figure><img src="/img/mx-lab-4-s.webp" alt="" loading="lazy"></figure>
    <figure><img src="/img/in-ganga-s.webp" alt="" loading="lazy"></figure>
  </div>
  <p class="more"><a href="{URL["research"][lang]}">{E(t["field_link"])}</a></p>
 </div>
</section>

<section class="band white">
 <div class="wrap">
  <div class="head"><h2>{E(t["news_h"])}</h2></div>
  {news_items(lang, NEWS[:3])}
  <p class="more"><a href="{URL["news"][lang]}">{E(t["news_all"])}</a></p>
 </div>
</section>

<section class="band warm">
 <div class="wrap">
  <div class="head"><h2>{E(t["offer_h"])}</h2></div>
  <div class="offer-grid">{"".join(offer)}</div>
 </div>
</section>
'''
    return shell(lang, "home", "1% happier — Carlos R. Pitta", body, URL["home"], cfg)

# ------------------------------------------------------------------ investigación
def research(lang):
    t = T[lang]
    lines = '<ul class="lines">' + "".join(
        f'<li>{LINE_ICONS[i]}<div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>' for i, (a, b) in enumerate(t["lines"])) + "</ul>"
    agenda = '<ul class="agenda">' + "".join(
        f'<li><div><h3>{E(a)}</h3><p>{E(b)}</p></div><div class="meta"><span class="chip">{E(t["wip"])}</span><br>{E(c)}</div></li>'
        for a, b, c in AGENDA[lang]) + "</ul>"
    exp = f'''<div class="exp">
  <figure><img src="/img/mx-lab-3.webp" alt="" loading="lazy" width="1400" height="1050"><figcaption>{E(t["field_mx"])}</figcaption></figure>
  <figure><img src="/img/in-sarnath-s.webp" alt="" loading="lazy" style="aspect-ratio:4/3"><figcaption>{E(t["field_in"])}</figcaption></figure>
  <figure><img src="/img/mx-lab-5-s.webp" alt="" loading="lazy"></figure>
  <figure><img src="/img/in-delhi-s.webp" alt="" loading="lazy"></figure>
</div>'''
    pubs = "<ol class=\"pubs\" reversed>" + "".join(
        f"<li>{p.format(thesis=E(t['thesis']), **{'and': E(t['and'])})}</li>" for p in PUBS) + "</ol>"
    body = page_hero(t["research_t"], t["research_i"]) + f'''
<section class="page-body"><div class="wrap">
  <h2 style="margin-top:0">{E(t["lines_h"])}</h2>
  {lines}
  <h2>{E(t["agenda_h"])}</h2>
  <p>{E(t["agenda_p"])}</p>
  {agenda}
  <h2>{E(t["field2_h"])}</h2>
  {exp}
  <h2>{E(t["pubs_h"])}</h2>
  {pubs}
</div></section>'''
    return shell(lang, "research", f'{t["research_t"]} — Carlos R. Pitta', body, URL["research"])

# ------------------------------------------------------------------ docencia
def teaching(lang):
    t = T[lang]
    cards = []
    for c in COURSES:
        d = c[lang]
        meta = [f'<span>{E(c["term"][lang])}</span>', f'<span>{E(t["units_n"].format(n=len(d["units"])))}</span>']
        if "programa" in c["docs"]:
            meta.append(f'<span class="has">{E(t["syllabus"])}</span>')
        if "clase00" in c["docs"]:
            meta.append(f'<span class="has">{E(t["lecture0"])}</span>')
        cards.append(f'''<article class="course"><span class="code">{c["code"]}</span>
  <h3><a href="{course_url(lang, c["slug"])}">{E(d["title"])}</a></h3>
  <p>{E(d["desc"])}</p><div class="meta">{"".join(meta)}</div></article>''')
    tl = []
    for u in OTHER_UNIS:
        name, city, courses = u[lang]
        lis = "".join(
            (f'<li><a href="/docs/otras/{f}.pdf">{E(cn)}</a></li>' if f else f'<li>{E(cn)}</li>') for cn, f in courses)
        tl.append(f'<li><span class="yr">{u["years"]}</span><div><h3>{E(name)}</h3><p class="city">{E(city)}</p><ul>{lis}</ul></div></li>')
    body = page_hero(t["teaching_t"], t["teaching_i"]) + f'''
<section class="page-body"><div class="wrap">
  <h2 style="margin-top:0">{E(t["uach_h"])}</h2>
  <p>{E(t["uach_p"])}</p>
  <div class="courses">{"".join(cards)}</div>
  <h2>{E(t["other_h"])}</h2>
  <p>{E(t["other_p"])}</p>
  <ol class="timeline">{"".join(tl)}</ol>
</div></section>'''
    return shell(lang, "teaching", f'{t["teaching_t"]} — Carlos R. Pitta', body, URL["teaching"])

def course(lang, c):
    t = T[lang]; d = c[lang]
    units = '<ol class="units">' + "".join(f"<li><div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>" for a, b in d["units"]) + "</ol>"
    dls = []
    if "programa" in c["docs"]:
        dls.append(f'<a href="/docs/{c["slug"]}-programa.pdf">{DOC_ICON}{E(t["dl_syllabus"])}</a>')
    if "clase00" in c["docs"]:
        dls.append(f'<a href="/docs/{c["slug"]}-clase00.pdf">{DOC_ICON}{E(t["dl_lecture0"])}</a>')
    crumb = f'<p class="crumb"><a href="{URL["teaching"][lang]}">← {E(t["course_back"])}</a> · {c["code"]}</p>'
    body = page_hero(d["title"], d["desc"], crumb) + f'''
<section class="page-body"><div class="wrap course-page">
  <div>
    <h2 style="margin-top:0">{E(t["course_units_h"])}</h2>
    {units}
    <h2>{E(t["course_text_h"])}</h2>
    <p>{E(d["text"])}</p>
  </div>
  <aside class="aside">
    <h2>{E(t["course_dl_h"])}</h2>
    <div class="dl">{"".join(dls)}</div>
    <p class="term">{E(t["course_term"])}: {E(c["term"][lang])}</p>
  </aside>
</div></section>'''
    alt = {l: course_url(l, c["slug"]) for l in ("es", "en")}
    return shell(lang, "teaching", f'{d["title"]} ({c["code"]}) — Carlos R. Pitta', body, alt, desc=d["desc"])

# ------------------------------------------------------------------ noticias, contacto, sobre mí
def news(lang):
    t = T[lang]
    body = page_hero(t["news_t"], t["news_i"]) + f'<section class="page-body"><div class="wrap">{news_items(lang, NEWS)}</div></section>'
    return shell(lang, "news", f'{t["news_t"]} — Carlos R. Pitta', body, URL["news"])

def contact(lang):
    t = T[lang]
    opts = "".join(f"<option>{E(o)}</option>" for o in t["f_kinds"])
    cfg = {"sending": t["f_sending"], "ok": t["f_ok"], "err": t["f_err"], "email": EMAIL}
    body = page_hero(t["contact_t"], t["contact_i"]) + f'''
<section class="page-body"><div class="wrap contact-in">
  <div>
    <p>{E(t["f_direct"])}</p>
    <p><a class="mail-big" href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p style="margin-top:2rem">{E(t["footer_where"])}</p>
  </div>
  <form class="form" id="contact-form" novalidate>
    <div class="row">
      <label>{E(t["f_name"])}<input name="name" autocomplete="name" required maxlength="120"></label>
      <label>{E(t["f_email"])}<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
    </div>
    <div class="row">
      <label>{E(t["f_org"])}<input name="org" autocomplete="organization" maxlength="160"></label>
      <label>{E(t["f_kind"])}<select name="kind">{opts}</select></label>
    </div>
    <label>{E(t["f_msg"])}<textarea name="message" required maxlength="5000"></textarea></label>
    <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
    <label class="check"><input type="checkbox" name="consent" value="yes" required><span>{E(t["f_consent"])}</span></label>
    <p class="status" id="f-status" role="status" tabindex="-1" hidden></p>
    <p style="margin:0"><button class="btn" type="submit">{E(t["f_send"])}</button></p>
  </form>
</div></section>'''
    return shell(lang, "contact", f'{t["contact_t"]} — Carlos R. Pitta', body, URL["contact"], cfg)

def about(lang):
    t = T[lang]
    bio = "".join(f"<p>{E(p)}</p>" for p in t["bio"])
    body = page_hero(t["about_t"], t["about_i"]) + f'''
<section class="page-body"><div class="wrap about-in">
  <div>{bio}<p>{E(t["write_me"])}<a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    {profile_chips()}</div>
  <figure><img src="/img/mx-lab-3.webp" alt="" width="1400" height="1050"><figcaption>{E(t["about_photo"])}</figcaption></figure>
</div></section>'''
    return shell(lang, "about", f'{t["about_t"]} — Carlos R. Pitta', body, URL["about"])

# ------------------------------------------------------------------ salida
def write(u, text, built):
    p = url_to_file(u)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    built.append(str(p.relative_to(OUT)))

def main():
    built = []
    for lang in ("es", "en"):
        for key, fn in (("home", home), ("research", research), ("teaching", teaching),
                        ("news", news), ("contact", contact), ("about", about)):
            write(URL[key][lang], fn(lang), built)
        for c in COURSES:
            write(course_url(lang, c["slug"]), course(lang, c), built)
    urls = [u for k in URL for u in URL[k].values()] + [course_url(l, c["slug"]) for l in ("es", "en") for c in COURSES]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                     + "".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print("ok", len(built), "páginas")

if __name__ == "__main__":
    main()
