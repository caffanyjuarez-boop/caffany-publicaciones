// Uso: node render.js <video> fotos t1 t2 ...   -> previas PNG
//      node render.js <video> video [fps]       -> mp4 sin audio (cuadros por tubería a ffmpeg)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const BASE = path.dirname(__dirname);
(async () => {
  const [name, mode, ...rest] = process.argv.slice(2);
  const meta = JSON.parse(fs.readFileSync(path.join(BASE, 'html', 'meta.json')));
  const dur = meta[name].dur;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(BASE, 'html', name + '.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
  const outDir = path.join(BASE, 'salida');
  fs.mkdirSync(outDir, { recursive: true });
  if (mode === 'fotos') {
    for (const t of rest) {
      await page.evaluate(t => window.seek(t), +t);
      await page.screenshot({ path: path.join(outDir, `prev_${name}_${t}.png`) });
    }
  } else {
    const fps = +(rest[0] || 30);
    const n = Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', path.join(outDir, `${name}_mudo.mp4`)],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.seek(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(name, i, '/', n);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log(name, 'listo');
  }
  await browser.close();
})();
