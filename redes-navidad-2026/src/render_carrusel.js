// Uso: node render_carrusel.js carrusel_malvavisco  -> salida/carrusel_malvavisco_1.png ...
const { chromium } = require('playwright');
const path = require('path');
const BASE = path.dirname(__dirname);
(async () => {
  const name = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(BASE, 'html', name + '.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const secs = await p.$$('section');
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: path.join(BASE, 'salida', `${name}_${i + 1}.png`) });
  await b.close();
  console.log(name, secs.length);
})();
