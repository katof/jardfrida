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
bolkur('Roynd', 'Sukurmolar í krukku',
  p('Steinar kunnu verða rundari, tá ið teir stoyta saman og slitna. Nú skulu tit kanna hetta við sukurmolum.'),
  p('<b>Tit skulu brúka:</b> seks til átta sukurmolar, eina reina krukku við loki, eitt myrkt pappír og eitt ur ella eina telefon at taka tíð.'),
  linjur(1, 'Gitið fyrst: Hvat halda tit fer at henda við sukurmolunum, tá ið tit rista krukkuna?'),
  ol(['Hyggið at einum sukurmola. Teljið kantarnar og hornini. Teknið hann.', 'Leggið hann á pappírið.', 'Leggið hinar sukurmolarnar í krukkuna og setið lokið á.', 'Ristið krukkuna í ein minutt.', 'Takið ein sukurmola upp og leggið hann á pappírið.', 'Ristið krukkuna aftur í ein minutt. Takið ein sukurmola upp hvørja ferð.', 'Samanberið sukurmolarnar. Hvat er hent við hornunum?', 'Hyggið í botnin á krukkuni. Hvat liggur har?']),
  tvey(ramma(45, 'Sukurmolin, áðrenn tit rista'), ramma(45, 'Sukurmolin, sum varð ristur longst')),
  linjur(2, 'Hví verða sukurmolarnir rundari? Hvussu líkist hetta steinum, sum verða skolaðir aftur og fram í fjøruni? Hvat er øðrvísi?'),
  ráð('Sukur er nógv bleytari enn grót. Royndin vísir, hvussu stoytir og slit kunnu broyta skap á einum steini.', 'Gev gætur'),
  ráð('Í krukkuni tekur tað minuttir. Í ánni og í fjøruni tók tað Malla sera langa tíð.', 'Hetta er eitt modell'),
  ráð('Brúkið eina reina krukku og vaskið hendurnar. Etið ikki sukurmolarnar, sum tit hava brúkt í royndini.', 'Til mat')),
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
g3 = [kapittul(3, 'Hvussu vórðu Føroyar til?', 'Føroyar eru bygdar upp av basaltfláum, sum komu til við eldgosum fyri meira enn 50 milliónum árum síðan. Men hvussu vita vit tað? Vit kunnu finna nógv spor í føroysku fjøllunum. Nú skalt tú kanna nøkur av teimum.', '#C0391F', f'<img src="{M}f-lagkaka.png" alt="">'),
partur(1, 'Jørðin og pláturnar', K3),
tala('jf', '»Áðrenn vit kanna Føroyar, skulu vit vita eitt sindur um jørðina. Hon er umleið 4,6 milliardir ára gomul.«'),
bolkur('Uppgáva', 'Inni í jørðini',
  tvey(mynd(M + 'f-jordin.png', ''), p('Jørðin hevur fleiri løg. Uttast er jarðarskorpan. Undir henni er kápan. Innast er kjarnin.') + p('Skriva navnið á løgunum:') + '<div class="ordbanki">Jarðarskorpan · Kápan · Uttari kjarnin · Innari kjarnin</div>' + ''.join(felt(f'{n}') for n in '1234')),
  p('<b>Jørðin er sum ein blomma.</b> Vit kunnu samanbera jørðina við eina blommu. Hon hevur skal uttast, fruktkjøt undir skalinum og ein stein í miðjuni. Men jørðin er ikki bygd júst sum ein blomma. Løgini eru øðrvísi, og tey eru ikki líka tjúkk.'),
  linjur(2, 'Hvør partur av blommuni líkist jarðarskorpuni? Hvat í blommuni líkist kjarnanum?'),
  ráð('Frá miðjuni á jørðini út á yvirflatan eru í miðal umleið 6.371 km. Innari kjarnin er meira enn 5.500 °C heitur.', 'Visti tú')),
bolkur('Les', 'Pláturnar flyta seg',
  p('Jarðarskorpan og ovasti parturin av kápuni eru brotin sundur í stórar <b>plátur</b>. Pláturnar flyta seg. Tær kunnu flyta seg sundur, burtur frá hvørji aðrari, ella saman, ímóti hvørji aðrari. Tær kunnu eisini flyta seg fram við hvørji aðrari.'),
  p('Pláturnar flyta seg vanliga bara nakrar sentimetrar um árið.'),
  linjur(1, 'Gita fyrst: Hvat kann koma upp úr jørðini, tá ið pláturnar fara sundur?'),
  '<div class="trý stórar">' + ''.join(f'<figure><img src="{M}f-platur-{i}.png" alt=""><figcaption><b>{i}.</b> {t}</figcaption></figure>' for i, t in [(1, 'Her liggja Grønland og Evropa saman á somu plátu.'), (2, 'Pláturnar fara sundur, og ein riva kemur ímillum.'), (3, 'Magma kemur upp í rivuna. Eldgos eftir eldgos!')]) + '</div>',
  ráð('Hóast pláturnar flyta seg so lítið hvørt ár, kunnu tær flyta seg sera langt í fleiri milliónir ár.', 'Visti tú')),
bolkur('Uppgáva', 'Føroyar og Grønland',
  p('Fyri nógvum milliónum árum síðan vóru Grønland og Evropa nógv nærri hvørjum øðrum enn nú. Síðani fóru pláturnar hvør sín veg. Nýggjur havbotnur varð til, og Norðuratlantshavið gjørdist breiðari.'),
  tala('malli', '»Fyri nógvum milliónum árum síðan vóru Føroyar og Grønland nógv nærri hvørjum øðrum. Nú er eitt stórt hav ímillum.«'),
  p('<b>Rokna.</b> Í hesum døminum rokna vit við, at tvær plátur flyta seg 2 cm frá hvørji aðrari um árið. Hvussu langt fara tær frá hvørji aðrari eftir 100 árum?'),
  '<div class="rokn"><span>2 cm × 100 ár =</span><i></i><span>cm. Tað eru</span><i></i><span>metrar.</span></div>',
  linjur(2, 'Hvat man henda, um pláturnar halda fram at flyta seg í fleiri milliónir ár?'),
  ráð('2 cm um árið er eitt rokningardømi. Talið vísir ikki, hvussu skjótt Føroyar og Grønland veruliga flyta seg frá hvørjum øðrum.', 'Gev gætur')),
bolkur('Roynd', 'Puslispæl við londunum',
  p('Passa londini saman?'),
  ol(['Tit fáa eitt klippiark við londunum frá læraranum. Klipp Grønland, Evropa, Afrika og Suðuramerika út.', 'Royn at leggja londini saman sum eitt puslispæl.', 'Hygg at strondunum, firðunum og víkunum. Hvørjir brikkar kunnu setast saman?', 'Hvar heldur tú, at Føroyar vóru, áðrenn Norðuratlantshavið gjørdist so breitt sum nú?']),
  linjur(2, 'Hvat vísir puslispælið okkum? Passa allar strendurnar heilt saman? Hví man tað vera?')),
bolkur('Tosið saman', 'Pláturnar', ul(['Á einum korti, sum vísir jørðina fyri 68 milliónum árum síðan, er einki Ísland. Hví man tað vera?', 'Hvat hendi, tá ið pláturnar fóru sundur?', 'Hví merkja vit ikki, at pláturnar flyta seg?', 'Hvussu kunnu jarðfrøðingar vita, at londini hava verið nærri hvørjum øðrum?'])),
partur(2, 'Eldgos og lagkøkan', K3),
tala('jf', '»Tá ið Grønland og Evropa fóru frá hvørjum øðrum, var nógv eldgos á okkara leiðum. Magma kom upp úr jørðini. Tá ið magma kemur upp á yvirflatan, nevna vit hana lava. Lava fleyt út yvir landið og kólnaði. Soleiðis vórðu stórar basaltfláir til.«'),
bolkur('Uppgáva', 'Hamarin er ein søgubók',
  p('Hygg at einum hamri í Føroyum. Tú sært strípur í grótinum. Tær vísa, at hamarin er bygdur upp av fleiri fláum. Hvør flógv kann siga okkum nakað um tað, sum hendi fyri nógvum milliónum árum síðan.'),
  mynd(M + 'f-hamar-log.png', '', 72),
  p('Skriva røtta bókstavin við hvørt orð:'),
  '<div class="bokst"><div><i></i><b>Lavaflá</b> – eitt lag av basalti frá einum eldgosi.</div><div><i></i><b>Mark</b> – ein tunn linja millum tvær lavafláir. Steðgurin millum eldgosini kann hava verið stuttur.</div><div><i></i><b>Royðugrót</b> – eitt reyðligt lag millum lavafláirnar. Tað kann vera frá einum longum steðgi millum eldgosini.</div><div><i></i><b>Kol</b> – í einum sera longum steðgi vaks nógvur gróður. Hann gjørdist til kol.</div></div>'),
ráð('Tá ið lavafláirnar leggjast hvør oman á aðra, er niðara fláin vanliga eldri. Men seinni kann magma eisini trýsta seg inn í grótið, sum longu er harðnað.', 'Visti tú'),
bolkur('Uppgáva', 'Hvat siga mørkini?',
  p('Hygg at teimum báðum myndunum. Hvat kann tað siga okkum? Set kross við tað svarið, sum tú heldur passar best.'),
  '<div class="tvey"><div class="markkort">' + mark_svg(True) + '<b>Mynd 1: Ein tjúkk reyðlig lind er millum tvær basaltfláir.</b>' + kross(['Tað kann hava gingið long tíð millum eldgosini. Plantur og mold kunnu hava verið har.', 'Eldgosini komu so tætt, at einki annað hendi ímillum.']) + '</div><div class="markkort">' + mark_svg(False) + '<b>Mynd 2: Bara ein tunn strika er millum basaltfláirnar.</b>' + kross(['Tað kann hava verið stutt millum eldgosini.', 'Strikan prógvar, at fleiri milliónir ár gingu millum eldgosini.']) + '</div></div>',
  linjur(2, 'Kunnu vit vita, hvussu langur steðgurin var, bara við at hyggja at litinum? Hvat annað kundu jarðfrøðingar kannað?'),
  ráð('Millum basaltfláirnar kunnu vit finna royðugrót, leir, sand og onkuntíð kol. Tað kann siga okkum nakað um, hvat hendi, meðan einki eldgos var.', 'Visti tú')),
bolkur('Uppgáva', 'Tekna tína egnu lagkøku',
  mynd(M + 'f-lagkaka.png', 'Ein lagkøka, sum Jarðfríða hevur bygt: basaltfláir, steðgir og ein vík.', 85),
  p('Tekna títt egna land, flá fyri flá. Avger sjálv/ur, hvar steðgirnir millum eldgosini vóru stuttir, og hvar teir vóru langir. Tekna so eina vík ígjøgnum fláirnar.'),
  '<div class="litir"><span><i style="background:#7A8086"></i>grátt = basaltflá</span><span><i style="background:#A4533A"></i>reytt = royðugrót (langur steðgur)</span><span><i style="background:#24282B"></i>svart = kol</span></div>',
  ramma(70, ''),
  linjur(2, 'Hvat hendir, tá ið lava kólnar? Hvussu líkist hetta einari lagkøku?'),
  ráð('Lagkøkan er eitt modell. Í veruleikanum komu fláirnar ikki allar líka skjótt. Summi eldgos vóru stór, onnur smærri. Millum eldgosini kundi ganga stutt ella long tíð.', 'Gev gætur')),
bolkur('Roynd', 'Lagkøka í glasi',
  p('Nú skulu tit byggja eitt modell av einum føroyskum hamri.'),
  p('<b>Tit skulu brúka:</b> eitt gjøgnumskygt glas ella eina avskorna plastfløsku, gráan sand, reyðan sand, eitt sindur av svørtum sandi og eitt súgvirør.'),
  ol(['Hellið eitt lag av gráum sandi í glasið. Tað skal vísa eina basaltflá.', 'Hellið eitt tunt lag av reyðum sandi omaná. Tað skal vísa tilfar, sum savnaðist millum eldgosini.', 'Hellið meira gráan sand í glasið. Nú hava tit tvær basaltfláir.', 'Haldið fram, til tit hava fimm ella seks løg. Avgerið, hvar steðgirnir millum eldgosini vóru stuttir, og hvar teir vóru langir.', 'Leggið eisini eitt tunt lag av svørtum sandi. Tað kann vísa eina kolalind.', 'Stingið eitt súgvirør niður ígjøgnum løgini. Tað skal vísa eina gong.']),
  ramma(34, 'Teknið glasið, og skrivið, hvat tey ymisku løgini vísa'),
  linjur(2, 'Hvørji løg eru elst? Hvørji eru yngst? Hví er gongin yngri enn løgini, sum hon sker seg ígjøgnum?'),
  ráð('Sandurin vísir bara, hvussu løg kunnu liggja hvør oman á aðra. Basalt er hart grót, og gongir verða til, tá ið magma trýstir seg inn í rivur og harðnar.', 'Gev gætur'),
  ráð('Sandur kann dálka og støva. Farið varliga við glasíløtum. Ein vaksin skal skera plastfløskuna, um tit brúka eina slíka.', 'Trygd')),
partur(3, 'Gongir og syllar', K3),
tala('jf', '»Tá ið basaltfláirnar vóru vorðnar til, kom meira magma upp úr jørðini. Nakað av magma trýsti seg inn í rivur og millum fláirnar. Har kólnaði hon og varð til hart grót.«'),
bolkur('Uppgáva', 'Gongir og syllar í hamrinum',
  mynd(M + 'f-hamar-innskot.png', '', 72),
  p('Hygg at myndini. Skriva røtta bókstavin við hvørt orð:'),
  '<div class="bokst"><div><i></i><b>Gong</b> – verður til, tá ið magma trýstir seg inn í eina rivu og harðnar. Gongin sker seg ofta upp ígjøgnum eldri basaltfláir.</div><div><i></i><b>Syll</b> – verður til, tá ið magma trýstir seg inn millum basaltfláirnar og harðnar har.</div><div><i></i><b>Gjógv</b> – ein djúp riva ella kluft í landslagnum. Vatn, frost og havalda kunnu við tíðini gera rivur størri og skapa gjáir.</div></div>',
  linjur(2, 'Hvussu sært tú mun á einari gong og einari syll?')),
ráð('Í Føroyum eru nógvar gongir og syllar. Jarðfrøðingar kunnu kenna tær aftur, tí grótið ofta er øðrvísi enn grótið rundan um.', 'Dømi úr Føroyum'),
bolkur('Uppgáva', 'Hvat kom fyrst?',
  p('Nú skalt tú finna út av, hvat hendi fyrst. Skriva 1 við tað elsta og 4 við tað yngsta.'),
  '<div class="bokst">' + ''.join(f'<div><i></i><b>{t}</b></div>' for t in ['Gongin', 'Fyrsta lavafláin', 'Ovara lavafláin', 'Royðugrótið']) + '</div>',
  linjur(2, 'Hví má gongin vera yngri enn fláirnar, sum hon sker seg ígjøgnum?')),
bolkur('Roynd', 'Gongir í gelé',
  p('Nú skulu tit kanna, hvussu ein løgur kann trýsta seg gjøgnum annað tilfar.'),
  p('<b>Tit skulu brúka:</b>') + ul(['stívt gelé í einum gjøgnumskygdum koppi', 'eina reina sproytu uttan nál', 'eitt sindur av matolju']),
  linjur(1, 'Gita fyrst: Hvat heldur tú fer at henda, tá ið tú trýstir olju inn í geléið?'),
  ol(['Gerið gelé og latið tað stívna.', 'Fyllið eitt sindur av matolju í sproytuna.', 'Stingið sproytuna varliga inn í geléið.', 'Trýstið spakuliga og hyggið, hvussu oljan flytur seg.', 'Rennur oljan út sum ein dropi, ella ger hon eina rivu?', 'Hvat hendir, um tit trýsta eitt sindur meira?']),
  ramma(40, 'Teknið tað, sum tit síggja'),
  linjur(2, 'Hvussu líkist hetta einari gong í gróti? Hvat er øðrvísi?'),
  ráð('Gelé er ikki grót, og olja er ikki magma. Royndin kann vísa, hvussu ein løgur trýstir seg gjøgnum annað tilfar. Hon vísir ikki, hvussu magma kólnar og verður til grót.', 'Gev gætur'),
  ráð('Brúkið bara sproytur uttan nál. Vaskið hendurnar aftaná. Geléið skal ikki etast, tá ið tit hava gjørt royndina.', 'Trygd')),
bolkur('Tosið saman', 'Gongir', ul(['Hví er ein gong vanliga yngri enn fláirnar, sum hon sker seg ígjøgnum?', 'Hvussu kann ein gong verða sjónlig í landslagnum?', 'Hvar í Føroyum kunnu vit síggja gongir?', 'Hvussu kunnu vit kanna, um tað, vit síggja, veruliga er ein gong?'])),
partur(4, 'Les landslagið', K3),
tala('jf', '»Nú hava tit lært um basaltfláir, royðugrót, gongir og syllar. Men kunnu tit finna tey úti í náttúruni? Tað skulu tit nú kanna.«'),
bolkur('Úti', 'Áðrenn tit fara út',
  tvey(p('<b>Takið við tykkum:</b>') + ul(['bókina og ein blýant', 'eina telefon ella ein teldil at taka myndir við', 'sjóneyku, um tit hava']),
       p('<b>Trygd:</b>') + ul(['Farið altíð saman við einum vaksnum.', 'Haldið tykkum frá bergbrúnum og brøttum brekkum.', 'Farið ikki undir bergveggir, har steinar kunnu detta oman.', 'Vaskið hendurnar, tá ið tit koma heim.'])),
  ráð('Kunnu tit ikki fara út? Brúkið myndir í staðin. Finnið myndir av føroyskum hamrum, til dømis hjá Jarðfeingi ella í Trap Føroyar. Gerið somu uppgávurnar við myndunum.', 'Inni')),
bolkur('Úti', '1 · Teljið fláirnar',
  p('Finnið ein hamar ella eina fjallalíð, har tit síggja strípur í grótinum. Hyggið væl at grótinum. Takið eina mynd, og teknið mørkini millum fláirnar.'),
  ramma(55, 'Teknið hamarin og mørkini millum fláirnar'),
  felt('Hvussu nógvar basaltfláir kunnu tit telja?'),
  linjur(2, 'Hvar eru mørkini lætt at síggja? Hvar eru tey torfør at finna?')),
bolkur('Úti', '2 · Leitið eftir royðugróti',
  p('Síggja tit eina reyðliga lind millum basaltfláirnar? Hon kann vera royðugrót. Hyggið nærri at henni.'),
  felt('Er lindin tjúkk ella tunn?'), felt('Sæst sama lindin báðumegin eina vík ella ein dal?'),
  linjur(2, 'Hvat kann lindin siga okkum um tíðina millum eldgosini?'),
  ráð('Ikki alt reytt grót er royðugrót. Jarðfrøðingar kanna eisini, hvat grótið er gjørt av, og hvussu tað er vorðið til.', 'Gev gætur')),
bolkur('Úti', '3 · Finnið eina gong',
  p('Leitið eftir einum grótparti, sum sker seg ígjøgnum basaltfláirnar. Kann tað vera ein gong? Hvussu sær grótið út?'),
  ramma(36, 'Teknið gongina, og skrivið, hvat er elst, og hvat er yngst'),
  linjur(2, 'Hvat kom fyrst: basaltfláirnar ella gongin? Hvussu vita tit tað?')),
bolkur('Uppgáva', 'At enda',
  p('Nú hava tit kannað, hvussu Føroyar vórðu bygdar upp av basaltfláum. Tit hava eisini lært, at grótið kann siga okkum nakað um tað, sum hendi fyri milliónum árum síðan.'),
  linjur(2, 'Hvat hevur tú lært um Føroyar?'), linjur(1, 'Hvat undrar teg enn?'), linjur(2, 'Hvat hevði tú spurt ein jarðfrøðing um?')),
tala('malli', '»Nú vita tit, hvussu eldgosini vóru við til at byggja Føroyar upp. Men hvat hendi, tá ið eldgosini steðgaðu? Tað er ein onnur søga.«'),
]

EKSTRA = [
 ('Gong', 'Ein gong verður til, tá ið magma trýstir seg inn í eina rivu og harðnar. Gongin sker seg ofta upp ígjøgnum eldri basaltfláir.'),
 ('Jarðarskorpa', 'Uttasta lagið á jørðini – har vit búgva.'),
 ('Kápa', 'Tjúkkasta lagið inni í jørðini, millum jarðarskorpuna og kjarnan.'),
 ('Lava', 'Tá ið magma kemur upp á yvirflatan, nevna vit hana lava.'),
 ('Lavaflá', 'Eitt lag av basalti frá einum eldgosi. Vit siga eisini basaltflá.'),
 ('Pláta', 'Eitt stórt petti av jarðarskorpuni og ovasta partinum av kápuni. Pláturnar flyta seg vanliga bara nakrar sentimetrar um árið.'),
 ('Steinrenning', 'Spor eftir plantu ella djóri, sum er vorðið til grót (fossil).'),
 ('Syll', 'Ein syll verður til, tá ið magma trýstir seg inn millum basaltfláirnar og harðnar har.'),
]
STAVRAD = 'aábcdðeéfghiíjklmnoópqrstuúvwxyýzæø'
ord = sorted(ORD + EKSTRA, key=lambda x: [STAVRAD.find(c) for c in x[0].lower()])
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
