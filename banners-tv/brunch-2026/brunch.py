"""Banner TV del Miércoles de Brunch (25-nov-2026), mismo estilo que los navideños (gen.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *  # noqa

CARAMELO = "#9A5A1E"

def brunch():
    ink = PINO
    svg = snow_field(41, 18, (90, 70, W - 90, 520), PINO, (0.05, 0.14))
    svg += frame(PINO, CREMA)
    cx, cy, r = W / 2, 905, 300
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r + 16}" fill="none" stroke="url(#oro)" stroke-width="3"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="none" stroke="{PINO}" stroke-width="1" opacity=".4" stroke-dasharray="2 9"/>'
    svg += rule_svg(530, 400, W - 400, ink, .4)
    svg += rule_svg(1905, 420, W - 420, ink, .35, diamond=False)
    html = header(ink, "cada miércoles, algo diferente")
    html += f"""
<div class="abs c" style="top:232px;font-family:Gloock;font-size:128px;line-height:1;color:{ink}">Miércoles de</div>
<div class="abs c" style="top:368px;font-family:ISerif;font-style:italic;font-size:150px;line-height:1;color:{VINO}">Brunch</div>
<div class="abs" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;
  background:url(hero_1x1.jpg) center/cover;box-shadow:0 30px 60px rgba(0,0,0,.28)"></div>
<div class="abs" style="left:{cx + r - 170}px;top:{cy + r - 210}px;width:250px;height:250px;border-radius:50%;
  background:{VINO};color:{CREMA};display:flex;flex-direction:column;align-items:center;justify-content:center;
  transform:rotate(-8deg);box-shadow:0 16px 34px rgba(0,0,0,.35);border:4px solid #E9C877">
  <div style="font-family:Gloock;font-size:118px;line-height:.9"><span style="font-size:52px;vertical-align:48px">$</span>69</div>
  <div class="caps" style="font-size:20px;letter-spacing:.26em;margin-top:6px">el combo</div></div>
<div class="abs c" style="top:1250px;font-family:ISerif;font-size:54px;line-height:1.15;color:{ink};padding:0 120px">
  2 hotcakes con fresa, miel de agave<br>y un toque de Nutella <i style="color:{VINO}">+ capuchino caliente</i></div>
<div class="abs" style="top:1450px;left:120px;width:430px;text-align:center">
  <div class="caps" style="font-size:24px;color:{VINO};letter-spacing:.26em">Hoy</div>
  <div style="font-family:Gloock;font-size:68px;line-height:1.1;color:{ink};margin-top:10px">9 am – 2 pm</div></div>
<div class="abs" style="top:1450px;left:640px;width:430px;text-align:center">
  <div class="caps" style="font-size:24px;color:{VINO};letter-spacing:.26em">Solo</div>
  <div style="font-family:Gloock;font-size:68px;line-height:1.1;color:{ink};margin-top:10px">25 combos</div></div>
<div class="abs c" style="top:1640px">
  <div style="display:inline-block;border:3px dashed rgba(14,42,31,.45);border-radius:18px;padding:18px 56px">
    <div class="caps" style="font-size:22px;color:{VINO};letter-spacing:.3em">Pídelo en caja con el código</div>
    <div style="font-family:Gloock;font-size:92px;line-height:1.05;color:{ink};letter-spacing:.04em">BRUNCH25</div></div></div>
<div class="abs c" style="top:1940px;font-family:ISerif;font-style:italic;font-size:42px;color:{ink};opacity:.85">
  y después de las 2 pm: <b style="font-style:normal;font-family:Gloock;font-weight:400;color:{VINO}">2x1</b> en café caliente</div>
<div class="abs" style="top:{cy + r + 22}px;left:0;right:0;text-align:center;font-family:ISans;font-size:18px;color:{ink};opacity:.45">imagen ilustrativa</div>"""
    svg += f'<line x1="594" y1="1450" x2="594" y2="1580" stroke="{ink}" stroke-width="1" opacity=".3"/>'
    return page(CREMA, svg, html, grain=.16)

if __name__ == "__main__":
    open(os.path.join(OUT, "5-brunch.html"), "w", encoding="utf-8").write(brunch())
    print("ok")
