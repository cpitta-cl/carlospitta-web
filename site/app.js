/* carlospitta.com v2 — interacción */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var C = window.CP || {};
  function $(id) { return document.getElementById(id); }
  function ready(fn) { document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn); }

  ready(function () {
    document.body.classList.add('ready');

    /* ---- cabecera */
    var top = document.querySelector('.top');
    var onScroll = function () { top && top.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    var mb = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
    if (mb && nav) {
      mb.addEventListener('click', function () {
        var o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o ? 'true' : 'false');
      });
      nav.addEventListener('click', function (e) { if (e.target.closest('a')) { nav.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); } });
    }

    if ($('stage')) hero();
    if ($('game')) game();
    if ($('contact-form')) contact();
  });

  /* ---------------------------------------------------------------- portada viva */
  function hero() {
    var stage = $('stage'), P = C.pairs, N = P.length, k = 0, timer = null, typing = null;
    var paused = reduce, visible = true, DWELL = 7000;
    var dv = $('say-devil'), an = $('say-angel'), srD = $('sr-devil'), srA = $('sr-angel');
    var prog = document.querySelector('.tnav .prog i'), pp = $('pp');
    var pupils = stage.querySelector('.pupils');

    function pad(p) { return (p < 10 ? '0' : '') + p; }
    function type(el, txt, done) {
      if (reduce) { el.textContent = txt; done && done(); return; }
      var i = 0; el.innerHTML = '';
      var span = document.createElement('span'), caret = document.createElement('i');
      caret.className = 'caret'; el.appendChild(span); el.appendChild(caret);
      clearInterval(typing);
      typing = setInterval(function () {
        i++; span.textContent = txt.slice(0, i);
        if (i >= txt.length) { clearInterval(typing); setTimeout(function () { caret.remove(); done && done(); }, 350); }
      }, 28);
    }
    function progress(ms) {
      if (!prog) return;
      prog.style.transition = 'none'; prog.style.width = '0';
      if (paused || reduce) return;
      void prog.offsetWidth; prog.style.transition = 'width ' + ms + 'ms linear'; prog.style.width = '100%';
    }
    function show(i) {
      k = (i + N) % N; var p = P[k];
      clearTimeout(timer);
      $('t-count').textContent = C.tcount.replace('{i}', k + 1).replace('{n}', N);
      var pl = $('t-pillar'); pl.href = '#p' + p[2]; pl.textContent = C.tpillar.replace('{p}', pad(p[2]));
      srD.textContent = p[0]; srA.textContent = p[1];
      stage.dataset.turn = 'devil'; an.textContent = '…';
      type(dv, p[0], function () {
        setTimeout(function () {
          stage.dataset.turn = 'angel';
          type(an, p[1], function () {
            setTimeout(function () { stage.dataset.turn = ''; }, 1400);
            schedule();
          });
        }, 650);
      });
    }
    function schedule() {
      clearTimeout(timer);
      progress(DWELL);
      if (paused || !visible) return;
      timer = setTimeout(function () { show(k + 1); }, DWELL);
    }
    $('next-temptation').addEventListener('click', function () { show(k + 1); });
    if (pp) {
      pp.addEventListener('click', function () {
        paused = !paused;
        pp.setAttribute('aria-pressed', paused ? 'true' : 'false');
        pp.setAttribute('aria-label', paused ? C.play : C.pause);
        pp.innerHTML = paused ? '&#9654;' : '&#10073;&#10073;';
        paused ? (clearTimeout(timer), progress(0)) : schedule();
      });
      if (reduce) { pp.hidden = true; }
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        visible ? schedule() : clearTimeout(timer);
      }, { threshold: .25 }).observe(stage);
    }
    /* los ojos siguen el puntero */
    if (pupils && !reduce) {
      var svg = stage.querySelector('svg');
      window.addEventListener('pointermove', function (e) {
        var r = svg.getBoundingClientRect(), cx = r.left + r.width * .5, cy = r.top + r.height * .34;
        var dx = e.clientX - cx, dy = e.clientY - cy, d = Math.hypot(dx, dy) || 1, m = Math.min(4.5, d / 60);
        pupils.style.transform = 'translate(' + (dx / d * m).toFixed(2) + 'px,' + (dy / d * m).toFixed(2) + 'px)';
      }, { passive: true });
    }
    setTimeout(function () { show(0); }, reduce ? 0 : 1300);
  }

  /* ---------------------------------------------------------------- juego */
  function game() {
    var Q = C.quiz, N = Q.length, k = 0, ans = new Array(N).fill(null), done = false;
    function pad(p) { return (p < 10 ? '0' : '') + p; }
    function tally() {
      var a = ans.filter(function (x) { return x === 'angel'; }).length, d = ans.filter(function (x) { return x === 'devil'; }).length;
      $('ta').textContent = a; $('td').textContent = d;
      var tot = a + d; $('tug').style.width = (tot ? 100 * a / tot : 50) + '%';
    }
    function render() {
      var q = Q[k];
      $('q').textContent = q[0];
      var sides = (k % 2 === 0) ? [['devil', q[1]], ['angel', q[2]]] : [['angel', q[2]], ['devil', q[1]]];
      for (var j = 0; j < 2; j++) {
        var b = $('opt' + j); b.dataset.side = sides[j][0];
        b.querySelector('span').textContent = sides[j][1][0]; b.querySelector('strong').textContent = sides[j][1][1];
      }
      $('step').textContent = C.step.replace('{n}', k + 1) + ' · ' + C.tpillar.replace('{p}', pad(k + 1));
    }
    function finish() {
      done = true; var a = ans.filter(function (x) { return x === 'angel'; }).length;
      var o = a >= 9 ? C.out[0] : a >= 6 ? C.out[1] : a >= 4 ? C.out[2] : C.out[3];
      document.querySelector('#game .choices').hidden = true; $('q').hidden = true; $('step').hidden = true;
      $('result').hidden = false; $('verdict').textContent = o[0]; $('explain').textContent = o[1];
      $('score').textContent = C.score.replace('{a}', a);
      var ul = $('lost'); ul.innerHTML = '';
      ans.forEach(function (x, i) {
        if (x === 'devil') { var li = document.createElement('li'), l = document.createElement('a');
          l.href = '#p' + (i + 1); l.textContent = pad(i + 1) + ' ' + C.names[i]; li.appendChild(l); ul.appendChild(li); }
      });
      $('lost-h').hidden = !ul.children.length;
      $('money').hidden = ans[1] !== 'devil';
      $('verdict').focus();
    }
    document.querySelector('#game .choices').addEventListener('click', function (e) {
      var b = e.target.closest('.choice'); if (!b || done) return;
      b.classList.remove('picked'); void b.offsetWidth; b.classList.add('picked');
      ans[k] = b.dataset.side; tally();
      var nx = -1; for (var i = 1; i <= N; i++) { var j = (k + i) % N; if (ans[j] === null) { nx = j; break; } }
      if (nx < 0) { setTimeout(finish, 250); return; }
      k = nx; setTimeout(render, reduce ? 0 : 180);
    });
    $('again').addEventListener('click', function () {
      ans = new Array(N).fill(null); done = false; k = 0; tally();
      document.querySelector('#game .choices').hidden = false; $('q').hidden = false; $('step').hidden = false; $('result').hidden = true;
      render();
    });
    tally();
  }

  /* ---------------------------------------------------------------- contacto */
  function contact() {
    var f = $('contact-form'), st = $('f-status'), btn = f.querySelector('button[type=submit]');
    var t0 = Date.now();
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var data = Object.fromEntries(new FormData(f).entries());
      data.elapsed = Date.now() - t0; data.lang = document.documentElement.lang;
      btn.disabled = true; var lbl = btn.textContent; btn.textContent = C.sending;
      fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () { st.hidden = false; st.className = 'status ok'; st.textContent = C.ok; f.reset(); })
        .catch(function () {
          st.hidden = false; st.className = 'status err'; st.textContent = C.err;
          var a = document.createElement('a'); a.href = 'mailto:' + C.email; a.textContent = C.email; st.appendChild(a); st.appendChild(document.createTextNode('.'));
        })
        .finally(function () { btn.disabled = false; btn.textContent = lbl; st.focus(); });
    });
  }
})();
