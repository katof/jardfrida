"""Tekur myndir av virknu pørtunum á heimasíðuni til næmingabókina.
    python3 verktoy/naemingabok_myndir.py http://localhost:8790/jardfrida
"""
import os, sys
from playwright.sync_api import sync_playwright
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8790/jardfrida').rstrip('/')
UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'naemingabok', 'myndir')
os.makedirs(UT, exist_ok=True)

FJAL = """() => { document.querySelectorAll('#jf-malli-widget, .jf-proto, .jf-proto-rum, #jf-borehole, .jf-depthbar').forEach(e => e.remove());
  document.querySelectorAll('section[role=tabpanel]').forEach(s => s.hidden = false); }"""

def mynd(page, sel, navn, nth=0):
    el = page.locator(sel).nth(nth)
    el.scroll_into_view_if_needed()
    el.screenshot(path=os.path.join(UT, navn + '.png'))

BOKSTAVIR = """(args) => {
  const [boxSel, map] = args;
  const svg = document.querySelector(boxSel + ' svg');
  const NS = 'http://www.w3.org/2000/svg';
  const sett = {};
  Object.entries(map).forEach(([id, bokst]) => { 
    const g = svg.querySelector('[data-hamar="' + id + '"]'); if (!g || sett[id]) return; sett[id] = 1;
    const bb = g.getBBox();
    const [bok, fx] = String(bokst).split('@');
    const breid = {A:590, B:500, C:410, D:320};
    const x = fx ? +fx : Math.min(612, Math.max(28, bb.width > 300 ? breid[bok] : bb.x + bb.width + 22));
    const y = (bb.width < 120 && bb.height > 120) ? bb.y + 60 : bb.y + bb.height / 2;
    bokst = bok;
    const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', x); c.setAttribute('cy', y); c.setAttribute('r', 15);
    c.setAttribute('fill', '#FFF6CF'); c.setAttribute('stroke', '#1E2326'); c.setAttribute('stroke-width', 2.5); svg.appendChild(c);
    const t = document.createElementNS(NS, 'text'); t.setAttribute('x', x); t.setAttribute('y', y + 6); t.setAttribute('text-anchor', 'middle');
    t.setAttribute('font-size', 17); t.setAttribute('font-weight', 700); t.setAttribute('font-family', 'Atkinson Hyperlegible, sans-serif'); t.textContent = bokst; svg.appendChild(t);
  });
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={'width':1100, 'height':1400}, device_scale_factor=2)

    # ---- Tunnilin ----
    page.goto(BASE + '/gongdir/tunnil/', wait_until='load'); page.wait_for_timeout(500); page.evaluate(FJAL)
    page.evaluate("() => { const l = document.getElementById('lens'); if (l) l.style.display = 'none'; const d = document.getElementById('coreDetail'); if (d) d.style.clipPath = 'none'; }")
    mynd(page, '#coreBox', 't-kjarni')
    for d in ['B1', 'B2', 'B3']:
        page.click(f'[data-drill="{d}"]'); page.wait_for_timeout(1500)
    mynd(page, '#mtn', 't-fjall-bora')
    mynd(page, '#tray', 't-kjarnar')
    page.click('#cutBtn'); page.wait_for_timeout(1800)
    mynd(page, '#mtnCut', 't-fjall-skorid')

    # ---- Hvaðani kom Malli? ----
    page.goto(BASE + '/gongdir/hvadani-kom-malli/', wait_until='load')
    page.evaluate("() => { try { localStorage.removeItem('jf-malli-soga'); } catch (e) {} }")
    page.reload(wait_until='load'); page.wait_for_timeout(1800); page.evaluate(FJAL)
    page.evaluate("() => { document.querySelectorAll('#mhPartiklar').forEach(g => g.style.display = 'none'); }")
    for i in range(9):
        if i: page.click('#malliHero'); page.wait_for_timeout(1700 if i == 3 else 1200)
        mynd(page, '#malliHero svg', f'm-soga-{i+1}')
    for i in range(3):
        mynd(page, '#phase-m2 .jf-journey figure svg', f'm-frost-{i+1}', i)
    mynd(page, '#phase-m3 .jf-mynd svg', 'm-is-maling', 0)
    mynd(page, '#phase-m3 .jf-mynd svg', 'm-brekka', 1)
    mynd(page, '#phase-m1 .jf-mynd svg', 'm-dos', 0)
    mynd(page, '#phase-m2 .jf-mynd svg', 'm-sproyta', 0)

    # ---- Hvussu vórðu Føroyar til? ----
    page.goto(BASE + '/gongdir/hvussu-vordu-foroyar-til/', wait_until='load'); page.wait_for_timeout(500); page.evaluate(FJAL)
    page.evaluate("""() => { const s = document.getElementById('jfJord'); s.querySelectorAll('text').forEach(t => t.remove());
      const NS = 'http://www.w3.org/2000/svg';
      const add = (x, y, n) => { const c = document.createElementNS(NS,'circle'); c.setAttribute('cx',x); c.setAttribute('cy',y); c.setAttribute('r',13); c.setAttribute('fill','#fff'); c.setAttribute('stroke','#1E2326'); c.setAttribute('stroke-width',2.5); s.appendChild(c);
        const t = document.createElementNS(NS,'text'); t.setAttribute('x',x); t.setAttribute('y',y+5); t.setAttribute('text-anchor','middle'); t.setAttribute('font-size',15); t.setAttribute('font-weight',700); t.setAttribute('font-family','Atkinson Hyperlegible, sans-serif'); t.textContent = n; s.appendChild(t); };
      const l = document.createElementNS(NS,'path'); l.setAttribute('d','M282 58 L314 22'); l.setAttribute('stroke','#1E2326'); l.setAttribute('stroke-width',2); s.appendChild(l);
      add(322, 16, '1'); add(170, 52, '2'); add(170, 112, '3'); add(170, 172, '4'); }""")
    mynd(page, '#jfJord', 'f-jordin')
    mynd(page, '#jfPlatur', 'f-platur-1')
    page.click('#jfPlaturKn'); page.wait_for_timeout(1900); mynd(page, '#jfPlatur', 'f-platur-2')
    page.wait_for_timeout(2600); mynd(page, '#jfPlatur', 'f-platur-3')
    page.evaluate(BOKSTAVIR, ['.jf-hamar[data-hamar="log"]', {'kol':'A', 'lavafla':'B', 'royd':'C', 'mark':'D'}])
    mynd(page, '.jf-hamar[data-hamar="log"] svg', 'f-hamar-log')
    page.evaluate(BOKSTAVIR, ['.jf-hamar[data-hamar="innskot"]', {'syll':'A@200', 'gjogv':'B', 'gong':'C'}])
    mynd(page, '.jf-hamar[data-hamar="innskot"] svg', 'f-hamar-innskot')
    for k in ['lkEldgos','lkEldgos','lkPausa','lkEldgos','lkEldgos','lkPausa','lkEldgos']:
        page.click('#' + k); page.wait_for_timeout(1500)
    page.click('#lkVik'); page.wait_for_timeout(1700)
    mynd(page, '#lagkaka', 'f-lagkaka')
    b.close()
print('ok', sorted(os.listdir(UT)))
