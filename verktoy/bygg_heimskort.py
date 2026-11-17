"""Byggir klippiarkið til royndina »Puslispæl við londunum« (pdf/heimskort-puslispael.pdf).

    pip install shapely playwright
    python verktoy/bygg_heimskort.py ne_110m_admin_0_countries.geojson

Kortdátan er Natural Earth (public domain), 1:110 mió:
https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson
Londini eru teknað í einari Lambert-flatartrúgvari mynd við miðdepli í Atlantshavinum,
so tey hava nøkulunda rætt skap og somu stødd í mun til hvørt annað.
Klippilinjan liggur eitt sindur uttan fyri strondina, so tað er lætt at klippa.
"""
import json, math, os, sys
from shapely.geometry import shape, box, Point
from shapely.ops import unary_union
from shapely import transform as _tf
from shapely.affinity import translate, scale as skala

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(sys.argv[1], encoding='utf-8'))
LON0, LAT0 = math.radians(-25), math.radians(20)

def laea(lon, lat):
    l, f = math.radians(lon) - LON0, math.radians(lat)
    k = math.sqrt(2 / (1 + math.sin(LAT0) * math.sin(f) + math.cos(LAT0) * math.cos(f) * math.cos(l)))
    return (k * math.cos(f) * math.sin(l), -k * (math.cos(LAT0) * math.sin(f) - math.sin(LAT0) * math.cos(f) * math.cos(l)))

def lond(test, klipp=None):
    g = unary_union([shape(f['geometry']).buffer(0) for f in DATA['features'] if test(f['properties'])])
    if klipp: g = g.intersection(box(*klipp))
    return _tf(g, lambda xy: [laea(x, y) for x, y in xy])

P = lambda p, k: p.get(k) or p.get(k.lower())
PARTAR = [
    ('Grønland', '#E4EDF2', lond(lambda p: P(p, 'ADMIN') == 'Greenland')),
    ('Evropa', '#E9E2C8', lond(lambda p: P(p, 'CONTINENT') == 'Europe' and P(p, 'ADMIN') != 'Iceland', (-30, 34, 50, 72))),
    ('Afrika', '#F0D9B5', lond(lambda p: P(p, 'CONTINENT') == 'Africa' and P(p, 'ADMIN') != 'Madagascar')),
    ('Suðuramerika', '#D5E3CC', lond(lambda p: (P(p, 'CONTINENT') == 'South America' and P(p, 'ADMIN') != 'Falkland Islands') or P(p, 'ADMIN') == 'France', (-95, -60, -30, 15))),
]

# ---- skala til A4 (mm) ----
W, H, RAND = 210, 297, 11
alt = unary_union([g for _, _, g in PARTAR])
x0, y0, x1, y1 = alt.bounds
s = min((W - 2 * RAND) / (x1 - x0), (H - 2 * RAND - 8) / (y1 - y0))
def mm(g):
    g = skala(g, s, s, origin=(0, 0))
    return translate(g, RAND - x0 * s + ((W - 2 * RAND) - (x1 - x0) * s) / 2, RAND - y0 * s)

BUFFUR = 5      # stórur buffari og so inn aftur: smalir firðir og sund verða latin aftur, so tað er lætt at klippa
bitar = []
for navn, litur, g in PARTAR:
    land = mm(g).simplify(0.25)
    kant = land.buffer(BUFFUR, join_style='round').buffer(-BUFFUR * 0.68, join_style='round')
    if kant.geom_type == 'MultiPolygon': kant = max(kant.geoms, key=lambda q: q.area)
    kant = type(kant)(kant.exterior).simplify(0.35)          # eingi hol í klippilinjuni
    land = land.intersection(kant)
    bitar.append([navn, litur, land, kant])

# Bitarnir skulu klippast út, so teir kunnu liggja, har teir fáa best pláss á arkinum.
# Allir hava somu skalu. (akker: v = vinstra, h = høgra, o = ovast, n = niðast)
STORRI = 1.25
STADUR = {'Grønland': ('v', 'o', 0), 'Evropa': ('h', 'o', 0), 'Afrika': ('h', 'o', 85), 'Suðuramerika': ('v', 'n', 0)}
for b in bitar:
    b[2], b[3] = skala(b[2], STORRI, STORRI, origin=(0, 0)), skala(b[3], STORRI, STORRI, origin=(0, 0))
    ax, ay, ey = STADUR[b[0]]
    bx0, by0, bx1, by1 = b[3].bounds
    dx = RAND - bx0 if ax == 'v' else W - RAND - bx1
    dy = RAND + ey - by0 if ay == 'o' else H - RAND - 3 - by1
    b[2], b[3] = translate(b[2], dx, dy), translate(b[3], dx, dy)
for i, b in enumerate(bitar):
    for o in bitar[i + 1:]:
        assert b[3].distance(o[3]) >= 3, (b[0], o[0], b[3].distance(o[3]))

def d(g):
    ut = []
    for pol in (g.geoms if hasattr(g, 'geoms') else [g]):
        if pol.geom_type != 'Polygon': continue
        for ring in [pol.exterior, *pol.interiors]:
            ut.append('M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in ring.coords[:-1]) + 'Z')
    return ''.join(ut)

svg = []
for navn, litur, land, kant in bitar:
    c = land.representative_point() if navn != 'Evropa' else Point(land.centroid.x + 6, land.centroid.y + 4)
    svg.append(f'<path d="{d(kant)}" fill="#fff" stroke="#1E2326" stroke-width=".7" stroke-linejoin="round"/>'
               f'<path d="{d(land)}" fill="{litur}" stroke="#6B7278" stroke-width=".25" fill-rule="evenodd" stroke-linejoin="round"/>'
               f'<text x="{c.x:.1f}" y="{c.y:.1f}" class="navn">{navn}</text>')

# ---- tekstur og Føroya-brikkur í havinum ----
gr = next(b for b in bitar if b[0] == 'Grønland')[3].bounds
af = next(b for b in bitar if b[0] == 'Afrika')[3].bounds
sa = next(b for b in bitar if b[0] == 'Suðuramerika')[3].bounds
tx, ty = gr[2] + 9, RAND + 12        # millum Grønland og Evropa
svg.append(f'''<text x="{tx}" y="{ty}" class="heiti">Puslispæl</text><text x="{tx}" y="{ty + 9.5}" class="heiti">við londunum</text>
<text x="{tx}" y="{ty + 19}" class="t">Klipp londini út eftir svørtu strikuni.</text>
<text x="{tx}" y="{ty + 24.5}" class="t">Royn at leggja tey saman</text>
<text x="{tx}" y="{ty + 30}" class="t">sum eitt puslispæl.</text>
<circle cx="{tx + 9}" cy="{ty + 45}" r="8.5" fill="#fff" stroke="#1E2326" stroke-width=".7"/>
<circle cx="{tx + 9}" cy="{ty + 42.5}" r="1.3" fill="#C0391F"/><text x="{tx + 9}" y="{ty + 48.3}" class="fo">Føroyar</text>
<text x="{tx + 21}" y="{ty + 43.5}" class="t">Klipp eisini Føroyar út.</text>
<text x="{tx + 21}" y="{ty + 49}" class="t">Hvar heldur tú, at tær vóru?</text>
<text x="{W - RAND}" y="{H - 7}" class="fot" text-anchor="end">Jarðfrøði við Jarðfríðu · Hvussu vórðu Føroyar til? · Kort: Natural Earth</text>''')

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm"><style>
text{{font-family:"Atkinson Hyperlegible",Arial,sans-serif;fill:#1E2326}}
.heiti{{font-family:"Fraunces",Georgia,serif;font-weight:700;font-size:9px}}
.t{{font-size:4px}} .navn{{font-size:4.6px;font-weight:700;text-anchor:middle}} .fo{{font-size:2.9px;font-weight:700;text-anchor:middle}} .fot{{font-size:2.5px;fill:#777}}
</style>{"".join(svg)}</svg>'''
open(os.path.join(ROT, 'myndir', 'heimskort-puslispael.svg'), 'w', encoding='utf-8', newline='\n').write(SVG)
print('svg ok', [(b[0], [round(v) for v in b[3].bounds]) for b in bitar])

SKRIFTIR = open(os.path.join(ROT, 'skriftir.css'), encoding='utf-8').read().replace('/jardfrida/skriftir/', 'skriftir/')   # fílurnar verða lisnar beinleiðis
html = f'<!doctype html><html lang="fo"><head><meta charset="utf-8"><style>{SKRIFTIR}@page{{size:A4;margin:0}}html,body{{margin:0;background:#fff}}svg{{display:block}}</style></head><body>{SVG}</body></html>'
tmp = os.path.join(ROT, '_heimskort.html')
open(tmp, 'w', encoding='utf-8').write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    try: b = pw.chromium.launch()
    except Exception: b = pw.chromium.launch(channel='msedge')
    pg = b.new_page(); pg.goto('file:///' + tmp.replace('\\', '/'), wait_until='load'); pg.wait_for_timeout(800)
    pg.pdf(path=os.path.join(ROT, 'pdf', 'heimskort-puslispael.pdf'), format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
os.remove(tmp)
print('pdf ok')
