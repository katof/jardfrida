"""Bygg »Jarðfríða – alt tilfarið« sum eina PDF-bók til prentingar.

Koyr frá mappuni við síðuni (krevur python-playwright, pypdf og reportlab):
    python3 -m http.server 8790   # í eini mappu, har /jardfrida peikar á repoið
    python3 verktoy/bygg_bok.py http://localhost:8790/jardfrida

Úrslitið verður goymt í pdf/jardfrida-alt-tilfarid.pdf
"""
import io, os, sys, tempfile
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8790/jardfrida').rstrip('/')
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(ROT, 'pdf', 'jardfrida-alt-tilfarid.pdf')

# (heiti í innihaldsyvirlitinum, slag, kelda, undirheiti)
INNIHALD = [
    ('Um tilfarið', 'web', '/um-tilfarid/', None),
    ('Gongd 1 · Jarðfríða kannar fjallið fyri ein tunnil', 'web', '/gongdir/tunnil/', None),
    ('Mín loggbók – Jarðfríða kannar fjallið', 'pdf', 'pdf/min-loggbok-jardfrida-kannar-fjallid.pdf', 'Gongd 1'),
    ('Gongd 2 · Hvaðani kom Malli?', 'web', '/gongdir/hvadani-kom-malli/', None),
    ('Mín loggbók – Hvaðani kom Malli?', 'pdf', 'pdf/min-loggbok-hvadani-kom-malli.pdf', 'Gongd 2'),
    ('Gongd 3 · Hvussu vórðu Føroyar til?', 'web', '/gongdir/hvussu-vordu-foroyar-til/', None),
    ('Orðalisti', 'web', '/ordalisti/', None),
    ('Til læraran', 'web', '/laerari/', None),
    ('Lærarvegleiðing', 'pdf', 'pdf/laerarvegleiding.pdf', 'Til læraran'),
    ('Samanberingarkort', 'pdf', 'pdf/samanberingarkort.pdf', 'Til læraran'),
    ('Okkara grótsavn', 'pdf', 'pdf/okkara-grotsavn.pdf', 'Til læraran'),
]

PRENT_CSS = """
@page { size:A4; margin:14mm 14mm 18mm; }
* { -webkit-print-color-adjust:exact !important; print-color-adjust:exact !important; }
html, body, body.jf-sida, .jf, .main-section { background:#fff !important; }
.jf-wrap { max-width:none !important; }
.jf { padding:0 !important; }
.jf-bok-partur { break-before:page; margin:0 0 14px; padding-bottom:8px; border-bottom:3px solid #1E2326;
  font:700 22pt/1.15 "Fraunces", Georgia, serif; color:#1E2326; }
.jf-bok-partur span { display:block; margin-bottom:4px; font:600 9pt/1 "IBM Plex Mono", monospace;
  letter-spacing:.08em; text-transform:uppercase; color:#2A6A80; }
.jf-bok-partur, h2, h3 { break-after:avoid; }
figure, .jf-coursecard, .jf-say, .jf-feedback, .jf-hint, tr, li, .jf-section-box, .jf-mark-kort, .jf-jord, .jf-hamar { break-inside:avoid; }
.jf-stack { gap:14px !important; }
figure img, .jf-foto img { max-height:100mm; width:auto !important; max-width:100%; margin:0 auto; }
a { color:inherit !important; text-decoration:none !important; }
"""

PRENT_JS = """
() => {
  const burt = '.jf-proto, .jf-proto-rum, #jf-borehole, .jf-depthbar, #jf-malli-widget, .jf-topbar, .jf-footer, .jf-toast, .jf-premia, .jf-malli-flyg, .jf-lk-aftur, #malliAftur, .jf-bok-kort, .jf-tjekt-stat, .jf-kent-lab, .jf-ord-stat, .jf-ordleit, .jf-ordtal';
  document.querySelectorAll(burt).forEach(e => e.remove());
  document.querySelectorAll('details').forEach(d => d.open = true);
  document.querySelectorAll('.jf-phase').forEach(t => {
    const sec = document.getElementById(t.getAttribute('aria-controls'));
    if (!sec) return;
    sec.hidden = false;
    const n = (t.querySelector('.jf-n') || {}).textContent || '';
    const heiti = [...t.childNodes].filter(x => x.nodeType === 3).map(x => x.textContent).join('').trim();
    const h = document.createElement('div');
    h.className = 'jf-bok-partur';
    h.innerHTML = '<span>Partur ' + n + '</span>' + heiti;
    sec.prepend(h);
  });
  document.querySelectorAll('.jf-phases').forEach(n => n.remove());
}
"""

def fyrireika(page, slod):
    """Smá ting, so myndirnar í bókini vísa nakað."""
    if 'hvussu-vordu' in slod:
        page.evaluate("""() => {
          const k = id => document.getElementById(id);
          ['lkEldgos','lkEldgos','lkPausa','lkEldgos','lkEldgos','lkPausa','lkEldgos'].forEach(i => k(i) && k(i).click());
        }""")
        page.wait_for_timeout(2600)
        page.evaluate("() => { const b = document.getElementById('jfPlaturKn'); b && b.click(); }")
        page.wait_for_timeout(4500)

def web_til_pdf(page, slod, fil):
    page.goto(BASE + slod, wait_until='load')
    page.wait_for_timeout(700)
    fyrireika(page, slod)
    page.add_style_tag(content=PRENT_CSS)
    page.evaluate(PRENT_JS)
    page.emulate_media(media='print')
    page.wait_for_timeout(400)
    page.pdf(path=fil, format='A4', print_background=True, prefer_css_page_size=True)

def forsida_html(innihald):
    rad = ''.join(
        f'<li class="{"undir" if u else ""}"><span>{t}</span><i></i><b>{s}</b></li>' for t, s, u in innihald)
    jf = open(os.path.join(ROT, 'favicon.svg'), encoding='utf-8').read()
    return f"""<!doctype html><html lang="fo"><head><meta charset="utf-8">
<link rel="stylesheet" href="{BASE}/skriftir.css"><style>
@page {{ size:A4; margin:0; }}
* {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; box-sizing:border-box; }}
body {{ margin:0; font-family:"Atkinson Hyperlegible", sans-serif; color:#1E2326; }}
.forsida {{ height:297mm; padding:30mm 22mm; background:#F4F1E8; display:flex; flex-direction:column; break-after:page;
  background-image:linear-gradient(to bottom, #F4F1E8 0 70%, #7A8086 70% 76%, #A4533A 76% 78%, #656B71 78% 88%, #4F555B 88% 100%); }}
.forsida .merki {{ font:600 10pt "IBM Plex Mono", monospace; letter-spacing:.1em; text-transform:uppercase; color:#2A6A80; }}
.forsida h1 {{ font:700 44pt/1.05 "Fraunces", serif; margin:10mm 0 6mm; }}
.forsida p {{ font-size:15pt; line-height:1.45; max-width:140mm; margin:0; }}
.forsida svg {{ width:62mm; height:auto; margin-top:14mm; }}
.forsida .fot {{ margin-top:auto; color:#fff; font:600 10pt "IBM Plex Mono", monospace; }}
.innihald {{ padding:24mm 22mm; }}
.innihald h2 {{ font:700 26pt "Fraunces", serif; margin:0 0 10mm; }}
.innihald ol {{ list-style:none; margin:0; padding:0; }}
.innihald li {{ display:flex; align-items:baseline; gap:6px; font-size:13pt; font-weight:700; margin:0 0 5mm; }}
.innihald li.undir {{ font-weight:400; font-size:11.5pt; margin:-2mm 0 4mm 8mm; }}
.innihald li i {{ flex:1; border-bottom:1.5px dotted #8A9095; transform:translateY(-3px); }}
.innihald li b {{ font:600 11pt "IBM Plex Mono", monospace; }}
.innihald .nota {{ margin-top:12mm; font-size:10.5pt; color:#585F65; line-height:1.5; }}
</style></head><body>
<section class="forsida"><span class="merki">Náttúra og tøkni · Prototypa</span>
<h1>Jarðfrøði við Jarðfríðu</h1><p>Alt tilfarið í eini bók – gongdirnar, orðalistin, loggbøkurnar og tilfarið til læraran.</p>
{jf}<span class="fot">Nám · Jarðfeingi · 2026</span></section>
<section class="innihald"><h2>Innihald</h2><ol>{rad}</ol>
<p class="nota">Bókin er gjørd til prentingar. Tey virknu partarnir á heimasíðuni – sum sjóneykan, lagkøkan og Malli – virka bert á netinum. Í bókini sæst ein mynd av teimum.</p></section>
</body></html>"""

def stimpla(writer, fra):
    """Síðutal niðast til høgru á øllum síðum aftaná forsíðuna."""
    for i, p in enumerate(writer.pages):
        if i < fra: continue
        w, h = float(p.mediabox.width), float(p.mediabox.height)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h))
        c.setFont('Helvetica', 8)
        c.setFillGray(0.35)
        c.drawRightString(w - 28, 18, str(i + 1))
        c.save()
        buf.seek(0)
        p.merge_page(PdfReader(buf).pages[0])

def main():
    tmp = tempfile.mkdtemp()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={'width':1100, 'height':1400})
        filir = []
        for i, (t, slag, kelda, _) in enumerate(INNIHALD):
            if slag == 'web':
                f = os.path.join(tmp, f'{i:02d}.pdf'); web_til_pdf(page, kelda, f)
            else:
                f = os.path.join(ROT, kelda)
            filir.append(f)
        talsidur = [len(PdfReader(f).pages) for f in filir]
        # forsíða + innihald (2 síður), síðan alt hitt
        start, s = [], 3
        for n in talsidur: start.append(s); s += n
        innihald = [(t, start[i], u) for i, (t, _, _, u) in enumerate(INNIHALD)]
        fp = os.path.join(tmp, 'forsida.pdf')
        page.set_content(forsida_html(innihald), wait_until='load')
        page.wait_for_timeout(600)
        page.pdf(path=fp, format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    w = PdfWriter()
    w.append(fp)
    yvir = {}
    for (t, _, _, u), f in zip(INNIHALD, filir):
        n0 = len(w.pages)
        w.append(f)
        foreldur = yvir.get(u) if u else None
        o = w.add_outline_item(t, n0, parent=foreldur)
        if not u: yvir[t.split(' · ')[0] if t.startswith('Gongd') else t] = o
    stimpla(w, 1)
    w.add_metadata({'/Title':'Jarðfrøði við Jarðfríðu – alt tilfarið', '/Author':'Nám og Jarðfeingi'})
    w.page_mode = '/UseOutlines'
    with open(UT, 'wb') as fh: w.write(fh)
    print('Goymt:', UT, len(w.pages), 'síður')

if __name__ == '__main__':
    main()
