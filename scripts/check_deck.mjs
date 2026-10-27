// Deck checker: per slide and per animation step, reports overflow past the
// content area, clipped containers, min font size and the free space at the bottom.
import { chromium } from '/home/mateuseap/.local/share/mise/installs/npm-playwright/latest/node_modules/playwright/index.mjs';
import path from 'node:path';
if (!process.argv[2]) { console.error('uso: node scripts/check_deck.mjs /caminho/index.html [slides]'); process.exit(2);
}
const file = path.resolve(process.argv[2]);
const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null;
const browser = await chromium.launch({ executablePath: '/usr/bin/chromium' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.goto('file://' + file);
await page.waitForTimeout(400);
const total = await page.evaluate(() => document.querySelectorAll('.slide').length);
let problems = 0;
for (let i = 1; i <= total; i++) {
  if (only && !only.includes(i)) continue;
  const steps = await page.evaluate(n => +(document.querySelectorAll('.slide')[n - 1].dataset.steps || 0), i);
  for (let s = 0; s <= steps; s++) {
    await page.goto('file://' + file + '#' + i + (s ? '.' + s : ''));
    await page.reload();
    await page.waitForTimeout(450);
    const r = await page.evaluate(() => {
      const slide = document.querySelector('.slide.active');
      const sb = slide.getBoundingClientRect();
      const out = { bottom: 0, minFont: 99, minFontText: '', overflow: [], clipped: [] };
      for (const el of slide.querySelectorAll('*')) {
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
        let hidden = false;
        for (let p = el; p && p !== slide; p = p.parentElement) {
          const pcs = getComputedStyle(p);
          if (pcs.display === 'none' || +pcs.opacity === 0) { hidden = true; break; }
        }
        if (hidden) continue;
        const b = el.getBoundingClientRect();
        if (b.width === 0 || b.height === 0) continue;
        const y = b.bottom - sb.top, x = b.right - sb.left;
        if (y > out.bottom) out.bottom = Math.round(y);
        if (y > 842 || x > 1604) out.overflow.push(`${el.tagName}.${el.className} y=${Math.round(y)} x=${Math.round(x)}`);
        const ownText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (ownText) {
          const fs = parseFloat(cs.fontSize);
          if (fs < out.minFont) { out.minFont = fs; out.minFontText = el.textContent.trim().slice(0, 40); }
        }
        if (['hidden', 'clip'].includes(cs.overflow) && el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0)
          out.clipped.push(`${el.tagName}.${el.className} ${el.scrollHeight}>${el.clientHeight}`);
        if (['hidden', 'clip'].includes(cs.overflow) && el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0)
          out.clipped.push(`${el.tagName}.${el.className} w ${el.scrollWidth}>${el.clientWidth}`);
      }
      out.title = slide.dataset.title;
      return out;
    });
    const bad = r.overflow.length || r.clipped.length;
    if (bad) problems++;
    console.log(`${String(i).padStart(2)}.${s} ${bad ? 'FAIL' : 'ok  '} bottom=${r.bottom} free=${842 - r.bottom} minFont=${r.minFont} [${r.minFontText}] ${r.title}`);
    for (const o of r.overflow.slice(0, 4)) console.log('      overflow ' + o);
    for (const c of r.clipped.slice(0, 4)) console.log('      clipped  ' + c);
  }
}
await browser.close();
console.log(problems ? `PROBLEMS: ${problems}` : 'ALL OK');
process.exit(problems ? 1 : 0);
