// Motor de animación determinista: seek(t) deja la página como debe verse en el segundo t.
(function () {
  const T = window.DUR;
  const clamp = v => v < 0 ? 0 : v > 1 ? 1 : v;
  const eo = p => 1 - Math.pow(1 - p, 3);
  const back = p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };

  const els = [...document.querySelectorAll('[data-in]')].map(e => {
    const d = e.dataset;
    return {
      e, tin: +d.in, tout: d.out !== undefined ? +d.out : 1e9, a: d.a || 'fade', d: +(d.d || .45),
      loop: d.loop || '', rot: +(d.rot || 0),
      cnt: d.count ? d.count.split(',').map(Number) : null, cd: +(d.cd || .8),
      st: d.st !== undefined ? +d.st : null,
      sc: d.sc ? d.sc.split(',').map(Number) : null,
      num: e.querySelector('.num'), lines: [...e.querySelectorAll('.line')]
    };
  }).filter(o => o.tout > o.tin);

  // nieve determinista
  const cv = document.getElementById('snow'), cx = cv.getContext('2d');
  const R = i => { const x = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
  const flakes = Array.from({ length: 90 }, (_, i) => ({
    x: R(i) * 1080, y: R(i + 99) * 1960, v: 35 + R(i + 7) * 85, r: 1.5 + R(i + 3) * 4.5, o: .25 + R(i + 5) * .55, s: R(i + 11) * 6.28
  }));
  function snow(t) {
    cx.clearRect(0, 0, 1080, 1920);
    for (const f of flakes) {
      const y = ((f.y + f.v * t) % 1960) - 20, x = f.x + Math.sin(t * .7 + f.s) * 22;
      cx.globalAlpha = f.o; cx.fillStyle = '#F3EAD8';
      cx.beginPath(); cx.arc(x, y, f.r, 0, 6.2832); cx.fill();
    }
    cx.globalAlpha = 1;
  }

  // subtítulos por bloques de hasta 3 palabras (corte en puntuación)
  const words = window.WORDS, chunks = [];
  let cur = [];
  words.forEach((w, i) => {
    cur.push(w);
    if (cur.length >= 3 || /[.,?!…:]$/.test(w.text) || i === words.length - 1) { chunks.push(cur); cur = []; }
  });
  chunks.forEach((c, i) => { c.s = c[0].start - .06; c.e = i < chunks.length - 1 ? chunks[i + 1][0].start - .06 : c[c.length - 1].end + .4; });
  const subs = document.getElementById('subs');
  let shown = -1;
  function captions(t) {
    let k = -1;
    if (t < window.FIN_SUBS) for (let i = 0; i < chunks.length; i++) if (t >= chunks[i].s && t < chunks[i].e) { k = i; break; }
    if (k !== shown) {
      subs.innerHTML = k < 0 ? '' : chunks[k].map(w => `<span>${w.text}</span>`).join(' ');
      shown = k;
    }
    if (k < 0) return;
    const sp = subs.children, c = chunks[k];
    for (let j = 0; j < c.length; j++) sp[j].className = t >= c[j].start - .02 ? 'on' : '';
    const p = clamp((t - c.s) / .14);
    subs.style.transform = `scale(${.86 + .14 * eo(p)})`;
    subs.style.opacity = clamp(p * 2);
  }

  window.seek = function (t) {
    for (const o of els) {
      if (t < o.tin - 1e-4 || t >= o.tout + .28) { o.e.style.visibility = 'hidden'; continue; }
      o.e.style.visibility = 'visible';
      const p = clamp((t - o.tin) / o.d), q = eo(p);
      let tx = 0, ty = 0, sc = 1, op = 1, rot = o.rot, clip = null;
      switch (o.a) {
        case 'fade': op = q; break;
        case 'up': ty = (1 - q) * 90; op = q; break;
        case 'down': ty = -(1 - q) * 90; op = q; break;
        case 'left': tx = -(1 - q) * 170; op = q; break;
        case 'right': tx = (1 - q) * 170; op = q; break;
        case 'pop': sc = .3 + .7 * back(p); op = clamp(p * 3); break;
        case 'stamp': sc = 1 + (1 - q) * 1.3; op = clamp(p * 2.5); break;
        case 'zoomin': sc = 1 + (1 - q) * .22; op = clamp(p * 2); break;
        case 'wipe': clip = `inset(0 ${(1 - q) * 100}% 0 0)`; break;
      }
      const life = t - o.tin, span = Math.max(Math.min(o.tout, T) - o.tin, .5);
      if (o.loop.includes('float')) ty += Math.sin(life * 2.1 + o.tin) * 11;
      if (o.loop.includes('drift')) sc *= 1 + .08 * clamp(life / span);
      if (o.loop.includes('spin')) rot += life * 22;
      if (o.loop.includes('pulse')) sc *= 1 + .04 * Math.sin(life * 7);
      if (o.sc) sc *= 1 + (o.sc[2] - 1) * eo(clamp((t - o.sc[0]) / (o.sc[1] - o.sc[0])));
      if (t >= o.tout) { const r = clamp((t - o.tout) / .25); op *= 1 - r; sc *= 1 - .07 * r; }
      o.e.style.opacity = op;
      o.e.style.transform = `translate(${tx}px,${ty}px) scale(${sc}) rotate(${rot}deg)`;
      if (clip !== null) o.e.style.clipPath = clip;
      if (o.cnt && o.num) {
        const r = eo(clamp((t - o.tin) / o.cd));
        o.num.textContent = Math.round(o.cnt[0] + (o.cnt[1] - o.cnt[0]) * r).toLocaleString('es-MX');
      }
      if (o.st !== null) { const r = eo(clamp((t - o.st) / .3)); o.lines.forEach(l => l.style.width = (r * 108) + '%'); }
    }
    snow(t); captions(t);
    document.getElementById('bar').style.width = (clamp(t / T) * 100) + '%';
  };
  window.seek(0);
})();
