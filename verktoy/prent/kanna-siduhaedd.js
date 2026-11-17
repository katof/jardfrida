const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage();
  await p.goto(process.argv[2] || "file:///home/claude/prent/loggbok-malli.html");
  const r = await p.evaluate(() => {
    const mm = 297 / document.querySelector('.sida').getBoundingClientRect().height;
    return [...document.querySelectorAll('.sida')].map((s,i) => {
      const pad = parseFloat(getComputedStyle(s).paddingBottom);
      let last = 0;
      s.querySelectorAll(':scope > *').forEach(el => {
        if (el.classList.contains('botnur')) return;
        const bot = el.getBoundingClientRect().bottom - s.getBoundingClientRect().top;
        if (bot > last) last = bot;
      });
      const h = s.getBoundingClientRect().height;
      return {sida:i, yvir_mm: +(((last - (h - pad)) * mm)).toFixed(1)};
    });
  });
  console.log(r.map(x => `síða ${x.sida}: ${x.yvir_mm > 0 ? '+'+x.yvir_mm+' mm YVIR' : x.yvir_mm+' mm leyst'}`).join('\n'));
  await b.close();
})();
