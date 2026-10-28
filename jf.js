/* Jarðfrøði við Jarðfríðu – felags skript
   Borikjarnin til vinstru vísir, hvar á síðuni tú ert:
   hvørt merki er eitt avsnit á síðuni. Trýst á eitt merki
   fyri at fara hagar. */
(function () {
  document.body.classList.add('jf-sida');

  var rot = document.getElementById('jf-borehole');
  if (!rot || rot.dataset.jfKlart) return;
  rot.dataset.jfKlart = '1';

  var fill  = document.getElementById('jf-bore-fill');
  var bar   = document.getElementById('jf-depth-fill');
  var ticks = document.getElementById('jf-bore-ticks');
  var tube  = rot.querySelector('.jf-bore-tube');
  if (!fill || !bar || !ticks || !tube) return;

  var bidar = false;
  var merki = [];          // [{el, top, span}]
  var MAX = 18;            // stavir í einum merki

  function synligur(el) {
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  }

  function stytt(t) {
    t = t.replace(/\s+/g, ' ').trim();
    return t.length > MAX ? t.slice(0, MAX - 1).trim() + '…' : t;
  }

  /* Avsnitini: yvirskriftir í síðuni (ikki tær í Malla-orðalistanum) */
  function finnAvsnit() {
    var sel = '.jf-wrap h1, .jf-wrap h2, .jf-wrap [data-jf-merki]';
    var all = Array.prototype.slice.call(document.querySelectorAll(sel));
    var ut = [], sidst = -1;
    all.forEach(function (el) {
      if (!synligur(el)) return;
      if (el.closest('#jf-malli-widget, .jf-footer, [hidden]')) return;
      var top = el.getBoundingClientRect().top + window.scrollY;
      if (top - sidst < 40) return;          // ov tætt
      sidst = top;
      ut.push({ el: el, top: top, tekstur: el.getAttribute('data-jf-merki') || el.textContent });
    });
    return ut;
  }

  function byggjaMerki() {
    var haedd = tube.clientHeight;
    if (!haedd) return;
    var longd = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    fill.style.setProperty('--jf-bore-height', haedd + 'px');
    ticks.innerHTML = '';
    merki = finnAvsnit();

    if (merki.length < 2) {                  // stutt síða: vís metrar sum áður
      for (var m = 0; m <= 100; m += 20) {
        var s = document.createElement('span');
        s.style.top = (m / 100 * haedd) + 'px';
        s.textContent = m + ' m';
        ticks.appendChild(s);
      }
      return;
    }

    merki.forEach(function (a, i) {
      var s = document.createElement('span');
      var mark = Math.min(1, Math.max(0, (a.top - 80) / longd));
      s.style.top = (mark * haedd) + 'px';
      s.textContent = stytt(a.tekstur);
      s.title = a.tekstur.replace(/\s+/g, ' ').trim();
      s.setAttribute('role', 'link');
      s.tabIndex = 0;
      s.addEventListener('click', function () { farTil(a.el); });
      s.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); farTil(a.el); }
      });
      a.span = s;
      ticks.appendChild(s);
    });
  }

  function farTil(el) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var y = el.getBoundingClientRect().top + window.scrollY - 72;
    window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
  }

  function dagfora() {
    bidar = false;
    var longd = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    var partur = Math.max(0, Math.min(1, window.scrollY / longd));
    fill.style.height = (partur * 100) + '%';
    bar.style.width   = (partur * 100) + '%';

    /* Hvat avsnit ert tú í? */
    var her = window.scrollY + window.innerHeight * 0.35;
    var valt = null;
    merki.forEach(function (a) { if (a.span && a.top <= her) valt = a; });
    if (!valt && merki.length) valt = merki[0];
    merki.forEach(function (a) { if (a.span) a.span.classList.toggle('er-her', a === valt); });
  }

  function bida() {
    if (bidar) return;
    bidar = true;
    requestAnimationFrame(dagfora);
  }

  var umbyggja;
  function seinni() {
    clearTimeout(umbyggja);
    umbyggja = setTimeout(function () { byggjaMerki(); dagfora(); }, 150);
  }

  byggjaMerki();
  dagfora();

  window.addEventListener('scroll', bida, { passive: true });
  window.addEventListener('resize', seinni);
  window.addEventListener('load', seinni);
  /* Teigar og fjald avsnit broyta síðuna – bygg merkini umaftur */
  document.addEventListener('click', seinni, true);

  if ('ResizeObserver' in window) {
    new ResizeObserver(seinni).observe(document.body);
  }
})();
