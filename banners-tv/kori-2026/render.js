const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const names = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1188, height: 2110 }, deviceScaleFactor: 1 });
  for (const n of names) {
    await page.goto('file://' + path.join(dir, n + '.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(dir, n + '.png') });
  }
  await browser.close();
})();
