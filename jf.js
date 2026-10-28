/* Jarðfrøði við Jarðfríðu – felags skript
   1) Borikjarnin til vinstru vísir dýpdina (0–100 m) og yvirlitsbarrin uppi.
   2) Tjekt listar (.jf-avmerk) kunnu krossast av; støðan verður goymd í browsaranum.
   3) »Far aftur til, har tú vart seinast« – ein pil, ið sendir tær aftur til staðið, tú fór frá. */
(function () {
  document.body.classList.add('jf-sida');

  function goym(lykil, v) { try { localStorage.setItem(lykil, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function hent(lykil) { try { return JSON.parse(localStorage.getItem(lykil)); } catch (e) { return null; } }

  /* ---------- Toast (melding í nedast) ---------- */
  var toastEl, toastTid;
  function melding(tekst) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'jf-toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = tekst;
    toastEl.classList.add('er-synlig');
    clearTimeout(toastTid);
    toastTid = setTimeout(function () { toastEl.classList.remove('er-synlig'); }, 2600);
  }

  /* ---------- 1) Borikjarnin: 0–100 m ---------- */
  var rot = document.getElementById('jf-borehole');
  if (rot && !rot.dataset.jfKlart) {
    rot.dataset.jfKlart = '1';
    var fill  = document.getElementById('jf-bore-fill');
    var bar   = document.getElementById('jf-depth-fill');
    var ticks = document.getElementById('jf-bore-ticks');
    var tube  = rot.querySelector('.jf-bore-tube');
    if (fill && bar && ticks && tube) {
      var bidar = false;

      var byggja = function () {
        var haedd = tube.clientHeight;
        if (!haedd) return;
        ticks.innerHTML = '';
        fill.style.setProperty('--jf-bore-height', haedd + 'px');
        for (var m = 0; m <= 100; m += 20) {
          var s = document.createElement('span');
          s.style.top = (m / 100 * haedd) + 'px';
          s.textContent = m + ' m';
          ticks.appendChild(s);
        }
      };

      var dagfora = function () {
        bidar = false;
        var longd = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
        var partur = Math.max(0, Math.min(1, window.scrollY / longd));
        fill.style.height = (partur * 100) + '%';
        bar.style.width   = (partur * 100) + '%';
      };

      var bida = function () {
        if (bidar) return;
        bidar = true;
        requestAnimationFrame(dagfora);
      };

      byggja();
      dagfora();
      window.addEventListener('scroll', bida, { passive: true });
      window.addEventListener('resize', function () { byggja(); dagfora(); });
      window.addEventListener('load', function () { byggja(); dagfora(); });
      if ('ResizeObserver' in window) {
        new ResizeObserver(function () { byggja(); dagfora(); }).observe(document.body);
      }
    }
  }

  /* ---------- 2) Tjekt listar ---------- */
  var listar = Array.prototype.slice.call(document.querySelectorAll('.jf-avmerk'));
  listar.forEach(function (ul, n) {
    var lykil = 'jf-tjekt:' + location.pathname + ':' + n;
    var gjort = hent(lykil);
    if (!Array.isArray(gjort)) gjort = [];
    var items = Array.prototype.slice.call(ul.children);

    /* Stýring ovast: tal av klárum og knøttur at byrja umaftur */
    var stat = document.createElement('div');
    stat.className = 'jf-tjekt-stat';
    var tekst = document.createElement('span');
    var nulstill = document.createElement('button');
    nulstill.type = 'button';
    nulstill.className = 'jf-tjekt-nulstill';
    nulstill.textContent = 'Byrja umaftur';
    stat.appendChild(tekst);
    stat.appendChild(nulstill);
    ul.parentNode.insertBefore(stat, ul);

    function teldu() {
      var klarar = 0;
      items.forEach(function (li, i) { if (gjort[i]) klarar++; });
      return klarar;
    }

    function vis(sigMelding) {
      var k = teldu();
      tekst.textContent = k + ' av ' + items.length + ' klárar';
      items.forEach(function (li, i) {
        li.classList.toggle('jf-klar', !!gjort[i]);
        var box = li.querySelector('input');
        if (box) box.checked = !!gjort[i];
      });
      if (sigMelding) {
        if (k === items.length) melding('Allur listin er klár! ✓');
        else melding('Gemt í browsaranum – ' + k + ' av ' + items.length);
      }
    }

    items.forEach(function (li, i) {
      li.classList.add('jf-tjekt');
      var etiketta = document.createElement('label');
      var box = document.createElement('input');
      box.type = 'checkbox';
      box.addEventListener('change', function () {
        gjort[i] = box.checked;
        goym(lykil, gjort);
        vis(true);
      });
      while (li.firstChild) etiketta.appendChild(li.firstChild);
      etiketta.insertBefore(box, etiketta.firstChild);
      li.appendChild(etiketta);
    });

    nulstill.addEventListener('click', function () {
      gjort = [];
      goym(lykil, gjort);
      vis(false);
      melding('Listin er byrjað umaftur');
    });

    vis(false);
  });

  /* ---------- 3) Far aftur til, har tú vart seinast ---------- */
  var SEINAST = 'jf-seinast', HOPP = 'jf-hopp';
  var her = location.pathname.replace(/\/+$/, '') || '/';

  /* Komin til síðu, ið vit fóru til frá annarstaðni: vís pil aftur */
  var hopp = hent(HOPP);
  if (hopp && hopp.u === her) {
    try { localStorage.removeItem(HOPP); } catch (e) {}
    window.addEventListener('load', function () {
      setTimeout(function () { window.scrollTo({ top: hopp.y, behavior: 'auto' }); }, 0);
    });
  }

  var fyrra = hent(SEINAST);
  if (fyrra && fyrra.u && fyrra.u !== her) {
    var pil = document.createElement('button');
    pil.type = 'button';
    pil.className = 'jf-seinast-pil';
    pil.innerHTML = '<span aria-hidden="true">←</span> <span>Far aftur til, har tú vart seinast</span>';
    pil.title = fyrra.n || fyrra.u;
    pil.addEventListener('click', function () {
      goym(HOPP, { u: fyrra.u, y: fyrra.y || 0 });
      location.href = fyrra.u;
    });
    document.body.appendChild(pil);
    requestAnimationFrame(function () { pil.classList.add('er-synlig'); });
  }

  /* Goym hvar tú ert, tá ið tú fert úr síðuni */
  function goymStað() {
    goym(SEINAST, {
      u: her,
      y: Math.round(window.scrollY),
      n: (document.title || '').split(' · ')[0].slice(0, 60)
    });
  }
  window.addEventListener('pagehide', goymStað);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') goymStað();
  });
})();
