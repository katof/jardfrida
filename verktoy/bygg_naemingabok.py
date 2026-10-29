"""Byggir næmingabókina (naemingabok/index.html) og PDF'ina (pdf/naemingabok.pdf).
    python3 verktoy/naemingabok_myndir.py http://localhost:8790/jardfrida   # myndir fyrst
    python3 verktoy/bygg_naemingabok.py http://localhost:8790/jardfrida
"""
import json, os, random, sys
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOK = os.path.join(ROT, 'naemingabok')
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8790/jardfrida').rstrip('/')
SPRITE = open(os.path.join(BOK, 'sprite.svg.txt'), encoding='utf-8').read()
ORD = json.load(open(os.path.join(BOK, 'ord.json'), encoding='utf-8'))
SKOP = json.load(open(os.path.join(BOK, 'skop.json'), encoding='utf-8'))

# ---------- byggiklossar ----------
def tala(hvor, tekst):
    navn = {'jf':'Jarðfríða', 'malli':'Malli'}[hvor]
    return f'<div class="tala tala-{hvor}"><svg aria-hidden="true"><use href="#{"jf" if hvor=="jf" else "malli"}"></use></svg><p><b>{navn}</b>{tekst}</p></div>'

def bolkur(slag, heiti, *innihald, cls=''):
    return f'<section class="bolkur {cls}"><span class="merki merki-{slag.lower().replace(" ","-").replace("ú","u").replace("ð","d")}">{slag}</span><h3>{heiti}</h3>{"".join(innihald)}</section>'

def p(t): return f'<p>{t}</p>'
def ol(items): return '<ol class="stig">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
def ul(items): return '<ul class="punkt">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def kross(items, cls=''): return f'<ul class="kross {cls}">' + ''.join(f'<li><i></i>{i}</li>' for i in items) + '</ul>'
def linjur(n, spurn=None):
    s = f'<p class="spurn">{spurn}</p>' if spurn else ''
    return s + '<div class="linjur">' + '<span></span>' * n + '</div>'
def ramma(hædd, tekst='', cls=''):
    return f'<div class="ramma {cls}" style="height:{hædd}mm"><span>{tekst}</span></div>'
def mynd(src, tekstur='', breidd=100, cls=''):
    t = f'<figcaption>{tekstur}</figcaption>' if tekstur else ''
    return f'<figure class="mynd {cls}" style="width:{breidd}%"><img src="{src}" alt="">{t}</figure>'
def ráð(t, slag='Gott ráð'): return f'<p class="rad"><b>{slag}:</b> {t}</p>'
def tvey(a, b): return f'<div class="tvey"><div>{a}</div><div>{b}</div></div>'
def felt(heiti, n=1): return f'<div class="felt"><b>{heiti}</b><div class="linjur">' + '<span></span>' * n + '</div></div>'
def partur(nr, heiti, kap): return f'<header class="partur"><span>{kap} · Partur {nr}</span><h2>{heiti}</h2></header>'

def kapittul(nr, heiti, undir, litur, myndir_html):
    return f'''<section class="kapittul" style="--k:{litur}"><span class="kap-nr">Gongd {nr}</span><h1>{heiti}</h1><p>{undir}</p><div class="kap-mynd">{myndir_html}</div></section>'''

def stein_svg(idx, bokst):
    d = SKOP[idx][1]
    return f'<figure class="stein"><svg viewBox="-60 -50 120 100"><path d="{d}" fill="#7E858B" stroke="#1E2326" stroke-width="4" stroke-linejoin="round"/></svg><b>{bokst}</b></figure>'

# ---------- innihaldið ----------
M = 'myndir/'
R = '../myndir/'

forsida = f'''<section class="forsida"><span class="kap-nr">Náttúra og tøkni</span><h1>Jarðfrøði við Jarðfríðu</h1><p class="undir">Næmingabók</p>
<div class="forsida-figurar"><svg class="fs-jf" aria-hidden="true"><use href="#jf"></use></svg><svg class="fs-malli" aria-hidden="true"><use href="#malli"></use></svg></div>
<div class="forsida-navn"><div><b>Navn</b><span></span></div><div><b>Flokkur</b><span></span></div></div></section>'''

inngangur = f'''<section class="inngangur"><h2>Hey! Eg eri Jarðfríða</h2>
{tala('jf', '»Eg eri jarðfrøðingur. Eg kanni grót og steinar og leiti eftir sporum, sum siga okkum, hvat er hent við landinum. Í hesi bókini verður tú eisini jarðfrøðingur!«')}
{tala('malli', '»Og eg eri Malli – steinurin í lummanum hjá Jarðfríðu. Eg havi eina langa søgu at siga tær.«')}
<h3>Soleiðis brúkar tú bókina</h3>
<div class="tekn"><div><span class="merki merki-les">Les</span> Her lesa tit og hyggja at myndum.</div><div><span class="merki merki-uppgava">Uppgáva</span> Her skrivar, teknar ella krossar tú í bókina.</div><div><span class="merki merki-roynd">Roynd</span> Her gera tit eina roynd saman.</div><div><span class="merki merki-uti">Úti</span> Her fara tit út.</div><div><span class="merki merki-tosid-saman">Tosið saman</span> Her tosa tit saman um tað, tit hava gjørt.</div></div>
{ráð('Gita fyrst, áðrenn tú kannar. Tað er heilt í lagi at gita skeivt – tað ger ein jarðfrøðingur eisini.', 'Minst til')}
<h3>Innihald</h3><ol class="innihald"><li><b>Jarðfríða kannar fjallið fyri ein tunnil</b><span>Kanna steinar · Mín steinur · Kjarnaboring og tunnil · Tykkara egna fjall</span></li><li><b>Hvaðani kom Malli?</b><span>Søgan hjá Malla · Frostið brýtur grótið · Spor eftir ísinum · Søgan hjá tínum steini</span></li><li><b>Hvussu vórðu Føroyar til?</b><span>Jørðin og pláturnar · Eldgos og lagkøkan · Gongir og syllar · Les landslagið</span></li><li><b>Orðalisti</b></li></ol></section>'''

K1 = 'Gongd 1'
g1 = [kapittul(1, 'Jarðfríða kannar fjallið fyri ein tunnil', 'Vit skulu gera ein tunnil gjøgnum eitt fjall. Kunnu tit hjálpa Jarðfríðu at finna besta staðið?', '#A4533A', f'<img src="{M}t-fjall-bora.png" alt="">'),
partur(1, 'Kanna steinar', K1),
tala('jf', '»Hetta er ein kjarni. Hon vísir grót, sum er borað úr fjallinum. Við sjóneykuni síggi eg smálutir, sum eg annars ikki síggi.«'),
bolkur('Uppgáva', 'Finn seks eyðkenni í kjarnanum',
  mynd(M + 't-kjarni.png', 'Ein kjarni úr fjallinum, teknaður stórur.'),
  p('Hygg væl at kjarnanum. Set ein ring um hvørt eyðkenni, tú finnur, og set kross her:'),
  kross(['Poknur (smá hol)', 'Fyltar poknur (hvítar)', 'Hvítar mineralæðrar', 'Ljós krystall', 'Grøn korn', 'Reyðligur litur'], 'tvikolonna'),
  linjur(3, 'Vel eitt eyðkenni. Hvat kann tað siga okkum um grótið?')),
mynd(R + 'hjalla-04-lup.jpg', 'Hjalla, september 2026. Veruligir kjarnar í goymsluni hjá Jarðfeingi. Hvítu blettirnir eru fyltar poknur.', 62),
tala('jf', '»Nú skulu tit hyggja at veruligum steinum. Teir kunnu tit nerta við!«'),
bolkur('Roynd', 'Nú við veruligum steinum',
  ol(['Kenn eftir steininum. Er hann slættur ella grovur? Tungur ella lættur?', 'Hygg við sjóneykuni. Finnur tú poknur, fyltar poknur, ljós krystall, grøn korn, hvítar mineralæðrar ella reyðligan lit?', 'Er steinurin eins innaní og uttaná? Ofta er uttasta lagið brúnt ella ryðlitt, tí grótið er veðrað.', 'Brúkið samanberingarkortini: Hvønn lit hevur grótið? Hvussu nógvar poknur eru? Hvussu stór eru kornini?']),
  ráð('Ger steinin eitt sindur vátan. So síggja tit litirnar betur.'),
  ramma(70, 'Tekna steinin her')),
tala('malli', '»Eg havi eisini poknur og krystall. Kanst tú finna tey á mær?«'),
partur(2, 'Mín steinur', K1),
tala('jf', '»Nú ert tú jarðfrøðingur! Finn ein stein, og vís flokkinum hann.«'),
bolkur('Uppgáva', 'Mín steinur',
  p('Finn ein stein við skúlan ella heima. Hygg væl at honum, og tekna hann.'),
  ramma(75, 'Tekna steinin her'),
  felt('Hvar fann eg steinin?'), felt('Hvat leggi eg merki til við honum?', 2), felt('Hvat undrist eg á?', 2),
  p('Er steinurin hjá tær rundur ella kantutur?'), kross(['Rundur', 'Kantutur', 'Eitt sindur av báðum'], 'linja'),
  ráð('Hygg at steinunum hjá hinum. Finnið tit ein stein við poknum? Ein við ljósum krystallum? Ein reyðan stein? Ein rundan og ein kantutan stein?', 'Tosið saman')),
partur(3, 'Kjarnaboring og tunnil', K1),
tala('jf', '»Vit skulu gera ein tunnil gjøgnum fjallið. Men vit síggja ikki inn í fjallið. Tí bora vit og taka kjarnar upp.«'),
bolkur('Les', 'Tríggjar boringar',
  tvey(mynd(M + 't-fjall-bora.png', 'Fjallið hjá Jarðfríðu við trimum boriholum: B1, B2 og B3.'), mynd(M + 't-kjarnar.png', 'Kjarnarnir úr B1, B2 og B3.')),
  '<div class="litir"><span><i style="background:#5F7A5B"></i>grønt = mold</span><span><i style="background:#7A8086"></i>grátt = basalt</span><span><i style="background:#2E3236"></i>svart = basalt</span><span><i style="background:#A4533A"></i>reytt = royðugrót / bleytari millumløg</span></div>'),
bolkur('Uppgáva', 'Hvat er inni í fjallinum?',
  p('Hygg at kjarnunum. Tekna á fjallið niðanfyri, hvussu tú heldur, at løgini halda fram millum boriholini. Brúka litirnar úr kjarnunum.'),
  mynd(M + 't-fjall-bora.png', '', 100, 'tekniflata'),
  linjur(2, 'Hví heldur tú, at løgini liggja soleiðis?'),
  ráð('Tað er sjálv metingin, sum hevur týdning – ikki um hon vísir seg at halda.', 'Minst til')),
bolkur('Les', 'Soleiðis sær fjallið hjá Jarðfríðu út innaní',
  mynd(M + 't-fjall-skorid.png', 'Fjallið skorið í helvt. Strikan vísir, hvar tunnilin kann ganga.'),
  linjur(2, 'Hvat passaði á tíni tekning? Hvat var øðrvísi?'),
  tala('jf', '»Best er, at tunnilin í hesum døminum gongur gjøgnum støðugt grót. Reyða lagið er bleytari og kann krevja meira trygging.«'),
  linjur(2, 'Hvar vilt tú hava tunnilin? Hví?')),
mynd(R + 'hjalla-01-kjarnar-hond.jpg', 'Hvør kassi er ein boring. Jarðfrøðingar bora aftur og aftur og samanbera kjarnarnar – júst sum tú gjørdi við B1, B2 og B3.', 62),
partur(4, 'Tykkara egna fjall', K1),
tala('jf', '»Nú skulu tit sjálv vera jarðfrøðingar! Tit gera eitt fjall úr gandadeiggi. Síðan skal eitt annað par finna fram til, hvat er inni í fjallinum hjá tykkum.«'),
bolkur('Roynd', 'Gerið eitt fjall – tvey og tvey',
  ol(['Gerið 3–4 flatar plátur úr gandadeiggi í ymiskum litum.', 'Leggið pláturnar oman á hvørja aðra. Tað eru løgini í fjallinum hjá tykkum.', 'Formið alt til eitt fjall. Dekkið tað við einum tunnum, grønum lagi, so eingin sær løgini.', 'Setið trý tannsteytarar í fjallið: B1, B2 og B3.', 'Býtið um fjall við eitt annað par.', 'Stingið eitt súgvirør beint niður við B1, snarið eitt sindur, og dragið tað upp. Klippið súgvirørið upp, og leggið kjarnan við síðuna av. Gerið tað sama við B2 og B3.']),
  ráð('Sigið ikki hinum, hvussu fjallið hjá tykkum sær út innaní.', 'Loyndarmál')),
bolkur('Uppgáva', 'Gitið – og skerið so fjallið í helvt',
  tvey(ramma(60, 'Okkara gitið: soleiðis heldur okkum, at fjallið sær út innaní'), ramma(60, 'Soleiðis sá tað út, tá ið vit skóru tað í helvt')),
  linjur(2, 'Hvat vísti seg at vera rætt? Hvat var øðrvísi, enn tit væntaðu?'),
  ráð('Tríggjar boringar vísa ikki alt, sum er millum boriholini.', 'Minst til')),
bolkur('Tosið saman', 'Tit hava arbeitt sum jarðfrøðingar!', ul(['Hvat passaði á tekningini? Hvat kom óvart á tykkum?', 'Hví bora jarðfrøðingar, áðrenn teir gera ein tunnil?'])),
]

K2 = 'Gongd 2'
SOGA = [
 ('Grótbræðing', 'Fyri meira enn 50 milliónum árum var eg gløðandi grótbræðing, sum rann út yvir landið. Í mær vóru gassbløðrur og grøn korn av olivini.'),
 ('Basalt við poknum', 'Eg kólnaði og storknaði til basalt. Har sum gassbløðrurnar vóru, eru nú smá hol, sum kallast poknur.'),
 ('Í fjallinum', 'Fleiri grótløg løgdust oman á meg, og eg gjørdist partur av fjallinum. Vatn seyraði gjøgnum grótið, og mineral úr vatninum settust í nakrar av poknunum og rivunum.'),
 ('Kantutur', 'Vatn frysti í rivunum, og ísurin sprongdi meg leysan úr fjallinum. Ansa tær – eg eri hvassur!'),
 ('Kantutur við skøvum', 'Jøkulsísurin dró meg við sær. Sandur og steinar í ísinum gjørdu skøvur í meg.'),
 ('Eitt sindur avrundaður', 'Nú rulli eg í ánni. Ái! Har fór ein kantur!'),
 ('Avrundaður', 'Hvørja ferð eg stoyti saman við einum øðrum steini, missi eg eitt lítið petti av mær.'),
 ('Næstan rundur', 'Vatnið rullar meg runt og runt. Skøvurnar eru næstan slitnar burtur.'),
 ('Rundur', 'Nú eri eg rundur! Tað tók túsundir av árum. Nú liggi eg í lummanum hjá Jarðfríðu.'),
]
soga_html = '<div class="soga">' + ''.join(f'<figure><img src="{M}m-soga-{i+1}.png" alt=""><figcaption><b>{i+1}. {h}</b>»{t}«</figcaption></figure>' for i, (h, t) in enumerate(SOGA)) + '</div>'
random.seed(4)
rod = list(range(6)); random.shuffle(rod)
stein_html = '<div class="steinar">' + ''.join(stein_svg(idx, 'ABCDEF'[i]) for i, idx in enumerate(rod)) + '</div>'
STEINAR4 = [(1, 2, True), (2, 5, False), (3, 3, True), (4, 5, False)]
def stein_med_skovum(idx, skovur, nr):
    d = SKOP[idx][1]
    sk = '<g stroke="#EDEFE8" stroke-width="2.2" stroke-linecap="round" opacity=".85"><path d="M-26 -6 L10 -16"/><path d="M-20 6 L18 -4"/><path d="M-10 18 L22 8"/></g>' if skovur else ''
    return f'<div class="spor"><svg viewBox="-60 -50 120 100"><path d="{d}" fill="#7E858B" stroke="#1E2326" stroke-width="4" stroke-linejoin="round"/>{sk}</svg><div><b>Steinur {nr}</b>' + kross(['Ísurin kann hava flutt hann', 'Vatnið kann hava rullað hann']) + '<div class="linjur"><span></span></div></div></div>'
spor_html = ''.join(stein_med_skovum(i, s, n) for n, i, s in STEINAR4)

g2 = [kapittul(2, 'Hvaðani kom Malli?', 'Hey, eg eiti Malli. Eg var einaferð partur av einum fjalli – hvassur í kantinum. Nú eri eg rundur og liggi í lummanum hjá Jarðfríðu. Hvat hendi við mær á leiðini?', '#2A6A80', f'<img src="{M}m-soga-9.png" alt="">'),
partur(1, 'Søgan hjá Malla', K2),
bolkur('Les', 'Ferðin hjá Malla', p('Les søguna hjá Malla – frá gløðandi grótbræðing til ein rundan stein.'), soga_html, cls='breiður'),
tala('jf', '»Ein steinur ber spor eftir tí, sum hann hevur verið út fyri. Vit kunnu lesa sporini – men vit kunnu ikki vita alt við vissu.«'),
bolkur('Uppgáva', 'Legg steinarnar í røð',
  p('Hygg at teimum seks steinunum. Skriva bókstavirnar í røð: fyrst tann við flestum kantum, síðst tann rundasta.'),
  stein_html,
  '<div class="rodfelt"><span>flestir kantar</span>' + '<i></i>' * 6 + '<span>rundastur</span></div>',
  linjur(2, 'Hví legði tú steinarnar soleiðis?')),
bolkur('Roynd', 'Ristið steinpettini rundari',
  tvey(mynd(M + 'm-dos.png', 'Ein góð rúgva av pettum – tey skulu kunna skumpa hvørt annað.'), p('Í dósini gera tit eitt lítið modell av eini á. Steinpettini skumpa hvørt annað, og kantarnir slítast av.')),
  ol(['Fyllið dósina góðan triðing upp við kantutum steinpettum – helst petti av múrsteini ella betongi. Tey slítast skjótari enn basalt.', 'Veljið eitt petti, merkið tað, og teknið tað niðanfyri.', 'Leggið eisini tvey hørð basaltpetti í dósina til samanberingar.', 'Gitið fyrst: Hvat hendir við kantunum, tá ið tit rista dósina?', 'Setið lokið væl á, og ristið dósina í tveir minuttir. Gerið tað fýra ferðir í alt.', 'Hellið innihaldið út á hvítt pappír. Er dust á pappírinum? Hvat er hent við basaltinum?']),
  tvey(ramma(45, 'Pettið, áðrenn tit rista'), ramma(45, 'Pettið eftir fjórðu ferð')),
  linjur(2, 'Hvat er broytt?'),
  ráð('Í dósini tekur tað minuttir. Í ánni og í fjøruni tók tað Malla sera langa tíð.', 'Hetta er eitt modell')),
partur(2, 'Frostið brýtur grótið', K2),
bolkur('Roynd', 'Latið vatnið frysta í sproytuni',
  tvey(mynd(M + 'm-sproyta.png', 'Oddurin er tættaður við leikleiri, og stempulin er tikin úr.'), ol(['Fyllið eina sproytu uttan nál við køldum vatni og eitt sindur av matliti.', 'Tættið oddin við leikleiri, og takið stempulin úr.', 'Mátið vatnssúluna við einari linjal.', 'Setið sproytuna beint upp í frystaran, til vatnið er fryst.', 'Mátið íssúluna.'])),
  p('Gitið fyrst: Verður íssúlan …'), kross(['longri', 'styttri', 'eins long sum vatnssúlan'], 'linja'),
  '<div class="rokn"><span>Vatnssúlan</span><i></i><span>mm</span><span>Íssúlan</span><i></i><span>mm</span><span>Munurin</span><i></i><span>mm</span></div>',
  ráð('Brúkið ikki glas til vatn, sum skal frysta í einum afturlatnum íláti.', 'Ansið eftir')),
bolkur('Les', 'Frá sproytuni til fjallið',
  '<div class="trý">' + ''.join(f'<figure><img src="{M}m-frost-{i}.png" alt=""><figcaption>{t}</figcaption></figure>' for i, t in [(1, 'Vatn rennur niður í eina rivu.'), (2, 'Vatnið frystir og fyllir meira. Ísurin trýstir – aftur og aftur.'), (3, 'Eitt petti brotnar av.')]) + '</div>',
  linjur(2, 'Hví liggja ofta kantutir steinar undir hamrum?')),
tala('malli', '»Kanska breyt eg meg leysan soleiðis! Jarðfeingi sigur »frostsprongt grót« um grót, sum er brotið niður á henda hátt.«'),
partur(3, 'Spor eftir ísinum', K2),
bolkur('Roynd', 'Gníggið ísin yvir málingina',
  mynd(M + 'm-is-maling.png', 'Eitt málað træpetti og tríggir ísterningar: ein reinur, ein við sandi og ein við grúsi.', 80),
  ol(['Gitið fyrst: Hvat fer at henda við málingini?', 'Gníggið ein reinan ísterning fram og aftur yvir træpettið. Koma skøvur í málingina?', 'Trýstið ein ísterning niður í sand, og gníggið hann sama veg.', 'Roynið eisini at trýsta ísterningin í grús.', 'Kannið málingina við sjóneykuni.']),
  ramma(40, 'Tekna skøvurnar, tú sært'),
  linjur(2, 'Var tað ísurin sjálvur ella tilfarið í honum, sum gjørdi skøvurnar?'),
  ráð('Brúkið klút ella vøtt um ísterningin, so verða hendurnar ikki ov kaldar.')),
bolkur('Roynd', 'Látið ísin skríða oman brekkuna',
  mynd(M + 'm-brekka.png', 'Brekkan: ein djúpur bakki, sum stendur á skák á einari ella tveimum bókum.', 70),
  ol(['Dagin fyri: Fyllið eina plastdós við vatni, sandi og smásteinum, og setið hana í frystaran.', 'Oysið sand og smásteinar í ein djúpan bakka, og leggið hann á skák á bókum.', 'Leggið ísklumpin ovast, og skumpið hann varliga oman brekkuna.', 'Latið ísin liggja niðast, til hann er bráðnaður.']),
  tvey(ramma(42, 'Brekkan áðrenn'), ramma(42, 'Brekkan aftaná')),
  tala('jf', '»Tað, sum liggur eftir, tá ið ísurin er bráðnaður, eitur morena: blandað, leyst tilfar – grót, sandur og leirur – sum jøkulsísur hevur flutt við sær og lagt frá sær.«')),
bolkur('Uppgáva', 'Ísurin ella vatnið?', p('Hygg at skapinum og skøvunum. Hvat kunnu sporini benda á? Set kross, og skriva hví.'), spor_html,
  ráð('Ein rundur steinur ella ein skøva er ikki í sjálvum sær prógv. Hygg eftir fleiri sporum.', 'Minst til')),
partur(4, 'Søgan hjá tínum steini', K2),
bolkur('Úti', 'Áðrenn tit fara út',
  tvey(p('<b>Takið við tykkum:</b>') + ul(['bókina og ein blýant', 'eina sjóneyku', 'ein posa til steinin, tú vilt hava heim við']), linjur(3, 'Gitið fyrst: Hvørjar steinar finna tit – kantutar, rundar ella steinar við skøvum?')),
  ráð('Ansið væl eftir sjónum, ánni og ferðsluni. Steinar í fjøruni kunnu vera hálir.', 'Trygd')),
bolkur('Úti', 'Lesið sporini á trimum steinum',
  '<table class="spor-talva"><thead><tr><th></th><th>Steinur 1</th><th>Steinur 2</th><th>Steinur 3</th></tr></thead><tbody>' +
  ''.join(f'<tr><th>{r}</th><td></td><td></td><td></td></tr>' for r in ['Kantutur ella rundur?', 'Slættur ella grovur?', 'Spor (skøvur, poknur, krystall …)', 'Hvar lá hann?', 'Hvat kann vera hent? (frost, ísur, vatn)']) + '</tbody></table>'),
bolkur('Úti', 'Hyggið eisini at landslagnum', p('Set kross við tað, sum tit síggja nærhendis:'),
  kross(['Kantutir steinar undir einum hamri', 'Ein dalur við skapi sum eitt U', 'Ein dalur við skapi sum eitt V', 'Rundir steinar í fjøruni ella í ánni', 'Skøvur í føstum gróti'])),
bolkur('Uppgáva', 'Grótkortið hjá mær',
  '<div class="grotkort"><div class="gk-hovd"><span>Okkara grótsavn</span><span>nr. ____</span></div>' + ramma(62, 'Tekna steinin – bert tað, tú veruliga sært') + felt('Steinurin eitur') + felt('Eg fann hann') + '<p class="spurn">Hvat kann vera hent við steininum?</p>' + kross(['Frost', 'Ísur', 'Vatn', 'Eg veit ikki enn'], 'linja') + felt('Eg eiti') + '</div>'),
bolkur('Tosið saman', 'Tit hava lisið søguna hjá einum steini!', ul(['Hvat helt tú fyrst – og hvat heldur tú nú?', 'Hvør steinur hevur týðilig spor eftir slit?', 'Er nakað um ferðina hjá steininum, sum tit ikki kunnu vita við vissu?'])),
]

K3 = 'Gongd 3'
mark_svg = lambda royd: ('<svg viewBox="0 0 200 86"><rect x="0" y="0" width="200" height="36" fill="#7A8086"/><rect x="0" y="36" width="200" height="14" fill="#A4533A"/><rect x="0" y="50" width="200" height="36" fill="#656B71"/></svg>' if royd else
                         '<svg viewBox="0 0 200 86"><rect x="0" y="0" width="200" height="42" fill="#7A8086"/><rect x="0" y="42" width="200" height="44" fill="#656B71"/><path d="M0 42 L200 42" stroke="#1E2326" stroke-width="2.5"/></svg>')
g3 = [kapittul(3, 'Hvussu vórðu Føroyar til?', 'Føroyar eru bygdar av risastórum eldgosum fyri meira enn 50 milliónum árum – lag fyri lag, eins og ein lagkøka.', '#C0391F', f'<img src="{M}f-lagkaka.png" alt="">'),
partur(1, 'Jørðin og pláturnar', K3),
tala('jf', '»Áðrenn vit hyggja at Føroyum, skulu vit vita, hvussu jørðin sjálv er bygd. Hon er umleið 4,6 milliardir ára gomul.«'),
bolkur('Uppgáva', 'Inni í jørðini',
  tvey(mynd(M + 'f-jordin.png', ''), p('Jørðin er sum ein ferskja. Skorpan er tunn sum hýðið. Kápan er sum aldinið. Í miðjuni er ein kjarni – sum steinurin í ferskjuni.') + p('Skriva navnið á lagunum:') + '<div class="ordbanki">Skorpan · Kápan · Uttari kjarnin · Innari kjarnin</div>' + ''.join(felt(f'{n}') for n in '1234')),
  ráð('Inn í miðjuna á jørðini eru umleið 6.371 km. Innari kjarnin er heitari enn 5.500 °C.', 'Visti tú')),
bolkur('Les', 'Pláturnar fara sundur',
  p('Skorpan á jørðini er brotin sundur í stór pettir, sum kallast <b>plátur</b>. Tær liggja á kápuni og flyta seg sera spakuliga – bert nakrir sentimetrar um árið.'),
  '<div class="trý stórar">' + ''.join(f'<figure><img src="{M}f-platur-{i}.png" alt=""><figcaption><b>{i}.</b> {t}</figcaption></figure>' for i, t in [(1, 'Grønland og Evropa liggja saman á somu plátu.'), (2, 'Hitin í kápuni togar í pláturnar. Tær fara sundur, og grótbræðing kemur upp í rivuna.'), (3, 'Eldgos eftir eldgos byggja nýtt land, lag omaná lag. Her vórðu Føroyar til.')]) + '</div>',
  linjur(2, 'Hví komu eldgos har, sum pláturnar fóru sundur?')),
bolkur('Uppgáva', 'Rokna sjálv/ur',
  tala('malli', '»Fyrr var bert umleið 100 km til Grønlands – tað kundi tú súkklað! Í dag flyta Føroyar og Grønland seg umleið 2 cm frá hvørjum øðrum um árið.«'),
  p('Um tú verður 100 ár – hvussu langt eru Føroyar og Grønland so flutt hvør frá aðrari?'),
  '<div class="rokn"><span>2 cm × 100 ár =</span><i></i><span>cm. Tað eru</span><i></i><span>metrar.</span></div>'),
bolkur('Roynd', 'Púsluspæl við londunum', ol(['Klipp Grønland, Evropa, Afrika og Suðuramerika út úr einum heimskorti.', 'Royn at leggja tey saman sum eitt púsluspæl. Hvørji passa best?', 'Hvar skulu Føroyar liggja?'])),
partur(2, 'Eldgos og lagkøkan', K3),
tala('jf', '»Tá ið Grønland og Evropa fóru sundur, kom risastór nøgd av grótbræðing upp. Eldgos eftir eldgos bygdu eitt flatt land av basalti – lag omaná lag. Tað er Føroyar!«'),
bolkur('Uppgáva', 'Hamarin er ein søgubók',
  p('Hygg at einum hamri í Føroyum. Tú sært strípur – tað eru løgini. Tað niðasta er elst.'),
  mynd(M + 'f-hamar-log.png', ''),
  p('Skriva røtta bókstavin við hvørt orð:'),
  '<div class="bokst"><div><i></i><b>Lavaflá</b> – eitt lag av basalti frá einum eldgosi.</div><div><i></i><b>Mark</b> – ein tunn linja millum tvær lavafláir. Pausan var stutt.</div><div><i></i><b>Royðugrót</b> – eitt reytt lag frá eini long pausu, tá ið plantur vuksu.</div><div><i></i><b>Kol</b> – í eini sera long pausu gjørdist nógvur gróður til kol.</div></div>'),
bolkur('Uppgáva', 'Hvat siga mørkini?',
  '<div class="tvey"><div class="markkort">' + mark_svg(True) + '<b>Eitt tjúkt reytt lag liggur millum tvær lavafláir.</b>' + kross(['Pausan var long – plantur og trø vuksu.', 'Eldgosini komu beint aftaná hvørt annað.']) + '</div><div class="markkort">' + mark_svg(False) + '<b>Bert ein tunn linja – einki reytt.</b>' + kross(['Pausan var long – plantur og trø vuksu.', 'Pausan var stutt – einki kundi vaksa.']) + '</div></div>'),
bolkur('Uppgáva', 'Tekna tína egnu lagkøku',
  mynd(M + 'f-lagkaka.png', 'Ein lagkøka, sum Jarðfríða hevur bygt: lavafláir, pausur og ein vík.', 85),
  p('Tekna títt egna land, lag fyri lag. Avger sjálv/ur, hvar pausurnar vóru stuttar, og hvar tær vóru langar. Tekna so eina vík ígjøgnum løgini.'),
  '<div class="litir"><span><i style="background:#7A8086"></i>grátt = lavaflá</span><span><i style="background:#A4533A"></i>reytt = royðugrót (long pausa)</span><span><i style="background:#24282B"></i>svart = kol</span></div>',
  ramma(70, '')),
bolkur('Roynd', 'Lagkøka í glasi',
  ol(['Takið eitt gjøgnumskygt glas.', 'Hellið eitt lag av gráum sandi í. Tað er ein lavaflá.', 'Hellið eitt tunt lag av reyðum sandi í – ein long pausa. Kanska eisini eitt sera tunt lag av svørtum – kol.', 'Haldið fram, til tit hava 5–6 løg.', 'Stingið eitt sugarør beint niður við glaskantin. Hellið svartan sand niður í sugarørið, og takið tað varliga upp. Nú hava tit eina gong!']),
  ráð('Sandur kann litast við krít ella matlit. Salt riggar eisini.', 'Ábending')),
partur(3, 'Gongir og syllar', K3),
tala('jf', '»Ikki øll grótbræðingin kom upp á yvirflatan. Onkur partur trýsti seg inn í løgini og storknaði har. Tað kalla vit eitt innskot.«'),
bolkur('Uppgáva', 'Gongir og syllar í hamrinum',
  mynd(M + 'f-hamar-innskot.png', ''),
  p('Skriva røtta bókstavin við hvørt orð:'),
  '<div class="bokst"><div><i></i><b>Gong</b> – ein strípa av basalti, sum skerst upp ígjøgnum løgini.</div><div><i></i><b>Syll</b> – grótbræðing, sum trýsti seg inn millum tvey løg og storknaði sum eitt tjúkt, flatt lag við basaltsúlum.</div><div><i></i><b>Gjógv</b> – var gongin bleytari enn løgini rundan um, slítur veður og vatn hana burtur.</div></div>',
  tvey('<p><b>Soleiðis kennir tú eina gong</b></p>' + ul(['Ein strípa, sum gongur á skrá ella beint upp ígjøgnum løgini.', 'Ofta dimmari og nakrir fá metrar breið.', 'Er hon harðari enn løgini, stendur hon fram sum ein veggur. Er hon bleytari, verður hon til eina gjógv.']),
       '<p><b>Dømi í Føroyum</b></p>' + ul(['Í Føroyum eru kortløgd meira enn 800 gongir.', 'Ein av teimum longstu er á Suðuroy – umleið 21 km long.', 'Streymoyarsyllin sæst sum ein høgur hamar á Skælingi.']))),
bolkur('Uppgáva', 'Hvat kom fyrst?',
  p('Skriva 1 við tað elsta, 2 við tað næstelsta, 3 og 4 við tað yngsta.'),
  '<div class="bokst">' + ''.join(f'<div><i></i><b>{t}</b></div>' for t in ['Gongin', 'Fyrsta lavafláin', 'Ovasta lavafláin', 'Royðugrótið']) + '</div>',
  linjur(2, 'Hví er ein gong yngri enn løgini, hon skerst ígjøgnum?')),
bolkur('Roynd', 'Gongir í gelé',
  p('Tit gera gelé og síggja, hvussu grótbræðing kløvur seg veg – og aftaná kunnu tit eta tað!'),
  ol(['Gerið ljóst gelé í gjøgnumskygdum koppum dagin fyri.', 'Fyllið eina reina sprøytu uttan nál við fløtu ella mjólk og eitt sindur av matliti. Tað er grótbræðingin.', 'Stingið sprøytuna niður í geléið, og trýstið varliga.', 'Hyggið eftir: Rennur fløtan út sum ein dropi – ella sum ein tunn, flat plata?', 'Nú kunnu tit eta tykkara gongir!']),
  ramma(40, 'Tekna, hvussu fløtan fór'),
  ráð('Brúkið bert rein amboð, sum eru til mat, og vaskið hendurnar. Hugsið um ofnæmi.', 'Skal geléið etast')),
partur(4, 'Les landslagið', K3),
tala('jf', '»Nú skulu tit lesa søguna í landslagnum sjálv. Tit kunnu gera tað næstan allastaðni í Føroyum – har tit síggja ein hamar ella ein fjallasíðu.«'),
bolkur('Úti', 'Áðrenn tit fara út', ráð('Farið ongantíð upp undir bergveggir uttan hjálm og trygdarskógvar. Hyggið helst á avstand. Vaksin skulu altíð vera við. Spyrjið um loyvi, um økið er privat.', 'Trygd')),
bolkur('Úti', '1 · Telið løgini', p('Finnið ein hamar ella eina fjallasíðu, har tit síggja strípur. Teknið eina skitsu, og teknið mørkini millum løgini.'), ramma(55, 'Skitsa av hamrinum'), felt('Hvussu nógvar lavafláir kunnu tit telja?')),
bolkur('Úti', '2 · Leitið eftir pausum', kross(['Vit síggja eitt reytt lag – ein long pausa.', 'Vit síggja bert eitt mark – ein stutt pausa.', 'Løgini passa saman á báðum síðum av eini vík ella einum dali.'])),
bolkur('Úti', '3 · Finnið eina gong', p('Leitið eftir eini strípu, sum skerst upp ígjøgnum løgini – ella eftir eini beinari gjógv.'), ramma(50, 'Tekna gongina. Skriva »eldri« og »yngri«.'), linjur(1, 'Hví halda tit, at tað er ein gong?')),
tala('malli', '»Nú vita tit, hvussu landið varð til. Men hvat hendi so, tá ið eldgosini sløknaðu? Tað er ein onnur søga – um ís!«'),
]

EKSTRA = [
 ('Gong', 'Ein strípa av basalti, sum skerst upp ígjøgnum løgini. Grótbræðing trýsti seg upp ígjøgnum eina rivu og storknaði.'),
 ('Kápa', 'Tjúkkasta lagið inni í jørðini, millum skorpuna og kjarnan.'),
 ('Lavaflá', 'Eitt lag av basalti frá einum eldgosi.'),
 ('Pláta', 'Eitt stórt petti av skorpuni á jørðini. Pláturnar flyta seg sera spakuliga.'),
 ('Skorpa', 'Ovasta lagið á jørðini – har vit búgva.'),
 ('Steinrenning', 'Spor eftir plantu ella djóri, sum er vorðið til grót (fossil).'),
 ('Syll', 'Grótbræðing, sum trýsti seg inn millum tvey løg og storknaði sum eitt tjúkt, flatt lag.'),
]
ord = sorted(ORD + EKSTRA, key=lambda x: x[0].lower())
ordalisti = '<section class="ordalisti"><header class="partur"><span>Aftast í bókini</span><h2>Orðalisti</h2></header><dl>' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in ord) + '</dl></section>'

CSS = open(os.path.join(BOK, 'bok.css'), encoding='utf-8').read()
html = f'''<!doctype html><html lang="fo"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jarðfrøði við Jarðfríðu – næmingabók</title><link rel="stylesheet" href="../skriftir.css"><style>{CSS}</style></head><body>
{SPRITE}
{forsida}{inngangur}
{''.join(g1)}{''.join(g2)}{''.join(g3)}{ordalisti}
</body></html>'''
open(os.path.join(BOK, 'index.html'), 'w', encoding='utf-8').write(html)
print('html ok')

from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page()
    pg.goto(BASE + '/naemingabok/', wait_until='load'); pg.wait_for_timeout(1200)
    fot = '<div style="width:100%;font:8px Helvetica,Arial,sans-serif;color:#777;padding:0 14mm;display:flex;justify-content:space-between"><span>Jarðfrøði við Jarðfríðu · Næmingabók</span><span class="pageNumber"></span></div>'
    pg.pdf(path=os.path.join(ROT, 'pdf', 'naemingabok.pdf'), format='A4', print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template='<span></span>', footer_template=fot)
    b.close()
print('pdf ok')
