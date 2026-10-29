/* Jarðfrøði við Jarðfríðu – felags skript
   1) Borikjarnin til vinstru vísir dýpdina (0–100 m) og yvirlitsbarrin uppi.
   2) Tjekt listar (.jf-avmerk) kunnu krossast av; støðan verður goymd í browsaranum. */
(function () {
  document.body.classList.add('jf-sida');

  function goym(lykil, v) { try { localStorage.setItem(lykil, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function hent(lykil) { try { return JSON.parse(localStorage.getItem(lykil)); } catch (e) { return null; } }

  /* Tal við røttum bending: »Eitt av 6 gjørt« / »2 av 6 gjørd«, »1 av 25 er kent« / »2 av 25 eru kend« */
  function gjortTekst(k, n) { return k === 1 ? 'Eitt av ' + n + ' gjørt' : k + ' av ' + n + ' gjørd'; }
  function kentTekst(k, n)  { return k === 1 ? '1 av ' + n + ' er kent' : k + ' av ' + n + ' eru kend'; }

  /* ---------- Toast (melding í nedast) ---------- */
  var toastEl, toastTid, toastRad = [], toastVisir = false;
  function visToast(tekst, tid) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'jf-toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastEl);
    }
    toastVisir = true;
    toastEl.textContent = tekst;
    toastEl.classList.add('er-synlig');
    clearTimeout(toastTid);
    toastTid = setTimeout(function () {
      toastEl.classList.remove('er-synlig');
      toastVisir = false;
      if (toastRad.length) { var n = toastRad.shift(); setTimeout(function () { visToast(n[0], n[1]); }, 250); }
    }, tid || 2600);
  }
  /* Vanlig melding: kemur beinanvegin. Bíðimelding (merki) kemur aftaná tí, ið longu sæst. */
  function melding(tekst) { visToast(tekst); }
  function meldingAftana(tekst, tid) { if (toastVisir) toastRad.push([tekst, tid]); else visToast(tekst, tid); }

  /* ---------- Merkini hjá Malla ---------- */
  var MERKI = [
    { id:'sjoneyka',     navn:'Gløggi eygleiðarin',  hvussu:'Finn øll seks eyðkennini í borikjarnanum við sjóneykuni.', gongd:'Tunnilsgongdin', farv:'#2A6A80',
      ikon:'<circle cx="21" cy="21" r="10" fill="none" stroke="#fff" stroke-width="4"/><path d="M28 28 L37 37" stroke="#fff" stroke-width="5" stroke-linecap="round"/>' },
    { id:'tunnil',       navn:'Tunnilsbyggjari', hvussu:'Vel, hvar tunnilin skal ganga gjøgnum fjallið.', gongd:'Tunnilsgongdin', farv:'#6E747A',
      ikon:'<path d="M6 36 L18 12 L26 22 L31 15 L42 36 Z" fill="#fff"/><path d="M17 36 v-5 a5 5 0 0 1 10 0 v5 Z" fill="#6E747A"/>' },
    { id:'malli-tunnil', navn:'Malli í tunlinum', hvussu:'Far við Malla inn í tunnilin.', gongd:'Tunnilsgongdin', farv:'#A4533A',
      ikon:'<path d="M8 38 v-12 a16 16 0 0 1 32 0 v12 Z" fill="#fff"/><ellipse cx="24" cy="32" rx="8" ry="6" fill="#A4533A"/><circle cx="21.5" cy="31" r="1.4" fill="#fff"/><circle cx="26.5" cy="31" r="1.4" fill="#fff"/>' },
    { id:'malli-funnin', navn:'Malli funnin!', hvussu:'Finn Malla, sum hevur fjalt seg.', gongd:'Hvaðani kom Malli?', farv:'#5E7D35',
      ikon:'<ellipse cx="24" cy="26" rx="15" ry="12" fill="#fff"/><circle cx="19" cy="24" r="2.4" fill="#5E7D35"/><circle cx="29" cy="24" r="2.4" fill="#5E7D35"/><path d="M19 30 Q24 34 29 30" stroke="#5E7D35" stroke-width="2.4" fill="none" stroke-linecap="round"/>' },
    { id:'steinakort',   navn:'Steinakortið',  hvussu:'Ger eitt kort um steinin hjá tær og tak tað niður.', gongd:'Hvaðani kom Malli?', farv:'#B7821F',
      ikon:'<rect x="9" y="11" width="30" height="26" rx="3" fill="#fff"/><ellipse cx="19" cy="22" rx="6" ry="5" fill="#B7821F"/><path d="M28 19 h7 M28 24 h7 M14 31 h21" stroke="#B7821F" stroke-width="2.4" stroke-linecap="round"/>' },
    { id:'ord',          navn:'Orðasnillingur', hvussu:'Set kross við øll orðini í orðalistanum.', gongd:'Orðalistin', farv:'#2E3236',
      ikon:'<path d="M10 13 h11 a3 3 0 0 1 3 3 v21 a3 3 0 0 0 -3 -3 h-11 Z M38 13 h-11 a3 3 0 0 0 -3 3 v21 a3 3 0 0 1 3 -3 h11 Z" fill="#fff"/>' }
  ];
  var MERKILYKIL = 'jf-merki';
  function mini() { var m = hent(MERKILYKIL); return (m && typeof m === 'object') ? m : {}; }
  /* Gullsteyp: liturin og myndin á merkinum sita á steypinum */
  function steypSvg(m, fingin, stort) {
    var G = fingin ? 'url(#jfGull' + (stort ? 'S' : '') + ')' : '#DAD6CD';
    var K = fingin ? '#1E2326' : '#B5B0A6';
    var gid = 'jfGull' + (stort ? 'S' : '');
    return '<svg viewBox="0 0 48 48" aria-hidden="true"' + (stort ? ' class="jf-steyp-stort"' : '') + '>' +
      (fingin ? '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE38A"/><stop offset=".45" stop-color="#F2C230"/><stop offset="1" stop-color="#B8860B"/></linearGradient></defs>' : '') +
      '<path d="M13 11 H7 Q6 22 16 24 M35 11 H41 Q42 22 32 24" fill="none" stroke="' + K + '" stroke-width="2.6" stroke-linecap="round"/>' +
      '<path d="M12 7 H36 V17 Q36 30 24 30 Q12 30 12 17 Z" fill="' + G + '" stroke="' + K + '" stroke-width="2" stroke-linejoin="round"/>' +
      '<rect x="21.5" y="30" width="5" height="5" fill="' + G + '" stroke="' + K + '" stroke-width="1.6"/>' +
      '<rect x="15" y="35" width="18" height="4.5" rx="1" fill="' + G + '" stroke="' + K + '" stroke-width="1.6"/>' +
      '<rect x="12" y="39.5" width="24" height="4.5" rx="1" fill="' + (fingin ? '#3A3F44' : '#CFCBC1') + '" stroke="' + K + '" stroke-width="1.6"/>' +
      (fingin
        ? '<circle cx="24" cy="17.5" r="8" fill="' + m.farv + '" stroke="#1E2326" stroke-width="1.4"/><g transform="translate(24 17.5) scale(.3) translate(-24 -24)">' + m.ikon + '</g>' +
          '<path d="M15 10 Q14 18 17 23" stroke="#FFF6CF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".8"/>'
        : '<text x="24" y="23" text-anchor="middle" font-size="13" font-weight="700" fill="#8D877C" font-family="system-ui,sans-serif">?</text>') +
      '</svg>';
  }
  function merkiSvg(m, fingin) { return steypSvg(m, fingin, false); }
  function savnadTekst(tal) { return 'Tú hevur savnað ' + tal + ' av ' + MERKI.length + ' merkjum.'; }

  /* Stóra premian: kemur fram, tá ið tú fært eitt gullsteyp */
  function visPremiu(m, tal) {
    var gamal = document.querySelector('.jf-premia');
    if (gamal) gamal.remove();
    var bak = document.createElement('div');
    bak.className = 'jf-premia';
    var aForsidu = !!document.getElementById('jf-merki');
    var gl = '';
    for (var i = 0; i < 14; i++) gl += '<i style="--x:' + (Math.random() * 100).toFixed(0) + '%;--d:' + (Math.random() * .6).toFixed(2) + 's;--r:' + (Math.random() * 360).toFixed(0) + 'deg"></i>';
    bak.innerHTML =
      '<div class="jf-premia-glitur" aria-hidden="true">' + gl + '</div>' +
      '<div class="jf-premia-kort" role="dialog" aria-modal="true" aria-labelledby="jfPremiaHeiti">' +
        steypSvg(m, true, true) +
        '<p class="jf-premia-yvir">Tú fekst eitt merki!</p>' +
        '<h2 id="jfPremiaHeiti">' + m.navn + '</h2>' +
        '<p class="jf-premia-hvi">' + m.hvussu + '</p>' +
        '<p class="jf-premia-tal">' + (tal === MERKI.length ? 'Nú hevur tú savnað øll seks merkini! Tú ert ein rættur jarðfrøðingur!' : savnadTekst(tal)) + '</p>' +
        '<div class="jf-premia-knappar">' +
          (aForsidu ? '' : '<a class="jf-premia-sí" href="/jardfrida/#merki">Sí øll merkini</a>') +
          '<button type="button" class="jf-premia-aftur">Halt fram</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(bak);
    var aftur = bak.querySelector('.jf-premia-aftur');
    function lat() { bak.classList.remove('er-synlig'); document.removeEventListener('keydown', esc); setTimeout(function () { bak.remove(); }, 250); }
    function esc(e) { if (e.key === 'Escape') lat(); }
    aftur.addEventListener('click', lat);
    bak.addEventListener('click', function (e) { if (e.target === bak) lat(); });
    document.addEventListener('keydown', esc);
    requestAnimationFrame(function () { bak.classList.add('er-synlig'); aftur.focus({ preventScroll: true }); });
  }
  function teknaMerki() {
    var stad = document.getElementById('jf-merki');
    if (!stad) return;
    var mitt = mini(), tal = 0;
    var html = '<ul class="jf-merki-listi">';
    MERKI.forEach(function (m) {
      var f = !!mitt[m.id]; if (f) tal++;
      html += '<li class="jf-merki-kort' + (f ? ' er-fingið' : '') + '">' + merkiSvg(m, f) +
        '<div><b>' + m.navn + '</b><span>' + m.hvussu + '</span><small>' + m.gongd + '</small>' + (f ? '<em class="jf-merki-status er-vunnid">✓ Vunnið</em>' : '<em class="jf-merki-status ikki-vunnid">Enn ikki lært</em>') + '</div></li>';
    });
    html += '</ul><p class="jf-tjekt-stat jf-merki-stat"><span>' +
      savnadTekst(tal) + (tal === MERKI.length ? ' 🏆' : '') + '</span>' +
      (tal ? '<button type="button" class="jf-tjekt-nulstill" id="jf-merki-nul">Strika øll merkini</button>' : '') + '</p>';
    stad.innerHTML = html;
    var nul = document.getElementById('jf-merki-nul');
    if (nul) nul.addEventListener('click', function () { goym(MERKILYKIL, {}); teknaMerki(); melding('Øll merkini eru strikað'); });
  }
  window.jfMerki = {
    gev: function (id) {
      var m = MERKI.filter(function (x) { return x.id === id; })[0];
      if (!m) return;
      var mitt = mini();
      if (mitt[id]) return;                     // longu fingið
      mitt[id] = new Date().toISOString().slice(0, 10);
      goym(MERKILYKIL, mitt);
      var tal = Object.keys(mitt).filter(function (k) { return MERKI.some(function (x) { return x.id === k; }); }).length;
      setTimeout(function () { visPremiu(m, tal); }, toastVisir ? 900 : 0);
      teknaMerki();
    }
  };
  teknaMerki();

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
      tekst.textContent = gjortTekst(k, items.length);
      items.forEach(function (li, i) {
        li.classList.toggle('jf-klar', !!gjort[i]);
        var box = li.querySelector('input');
        if (box) box.checked = !!gjort[i];
      });
      if (sigMelding) {
        if (k === items.length) melding('Allur listin er klár! ✓');
        else melding('Goymt í kaganum – ' + gjortTekst(k, items.length));
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
      melding('Alt á listanum er strikað');
    });

    vis(false);
  });


  /* ---------- 4) Ordalistin: »Eg kann hetta« – goymt í browsaranum ---------- */
  var ordDl = document.getElementById('jf-ordlisti');
  if (ordDl) {
    var ordLykil = 'jf-ord-kent:' + location.pathname;
    var kent = hent(ordLykil);
    if (!kent || typeof kent !== 'object') kent = {};
    var orðini = Array.prototype.slice.call(ordDl.querySelectorAll('.jf-ord'));
    var statOrd = document.createElement('p');
    statOrd.className = 'jf-tjekt-stat jf-ord-stat';
    var statTekst = document.createElement('span');
    var nulOrd = document.createElement('button');
    nulOrd.type = 'button';
    nulOrd.className = 'jf-tjekt-nulstill';
    nulOrd.textContent = 'Byrja umaftur';
    statOrd.appendChild(statTekst);
    statOrd.appendChild(nulOrd);
    ordDl.parentNode.insertBefore(statOrd, ordDl);

    function ordLyklar(o) { return o.getAttribute('data-lyk') || ''; }

    function ordVis(sigMelding) {
      var k = 0;
      orðini.forEach(function (o) {
        var lyk = ordLyklar(o);
        var v = !!kent[lyk];
        if (v) k++;
        o.classList.toggle('jf-kent', v);
        var box = o.querySelector('input');
        if (box) box.checked = v;
      });
      statTekst.textContent = kentTekst(k, orðini.length);
      if (sigMelding) melding(k === orðini.length ? 'Øll orðini eru kend! ✓' : 'Goymt í kaganum – ' + kentTekst(k, orðini.length));
      if (sigMelding && k === orðini.length) window.jfMerki.gev('ord');
    }

    orðini.forEach(function (o) {
      var dt = o.querySelector('dt');
      if (!dt) return;
      var lyk = dt.textContent.replace(/\s+/g, ' ').trim();
      o.setAttribute('data-lyk', lyk);
      var etiketta = document.createElement('label');
      etiketta.className = 'jf-kent-lab';
      var box = document.createElement('input');
      box.type = 'checkbox';
      etiketta.appendChild(box);
      etiketta.appendChild(document.createTextNode(' Eg kenni orðið'));
      dt.appendChild(etiketta);
      box.addEventListener('change', function () {
        if (box.checked) kent[lyk] = true; else delete kent[lyk];
        goym(ordLykil, kent);
        ordVis(true);
      });
    });

    nulOrd.addEventListener('click', function () {
      kent = {};
      goym(ordLykil, kent);
      ordVis(false);
      melding('Alt á listanum er strikað');
    });

    ordVis(false);
  }
})();
