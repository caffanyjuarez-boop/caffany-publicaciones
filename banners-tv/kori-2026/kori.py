"""Banner TV pop-up Kori Matcha × Caffany (sábado 28-nov-2026, 1–9 pm), mismo estilo que los navideños (gen.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *  # noqa

LIMA = "#C9E34A"


def kori():
    ink = CREMA
    svg = snow_field(53, 22, (90, 70, W - 90, 560), CREMA, (0.05, 0.14))
    svg += frame(CREMA, PINO)
    cx, cy, r = W / 2, 930, 300
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r + 16}" fill="none" stroke="url(#oro)" stroke-width="3"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="none" stroke="{CREMA}" stroke-width="1" opacity=".35" stroke-dasharray="2 9"/>'
    svg += rule_svg(560, 400, W - 400, ink, .4)
    svg += rule_svg(1905, 420, W - 420, ink, .3, diamond=False)
    svg += f'<line x1="594" y1="1480" x2="594" y2="1610" stroke="{ink}" stroke-width="1" opacity=".3"/>'
    html = header(ink, "pop-up · sábado 28 de noviembre")
    html += f"""
<div class="abs c" style="top:226px;font-family:Gloock;font-size:150px;line-height:1;color:{ink}">Kori <span style="font-family:ISerif;font-style:italic;color:{LIMA}">Matcha</span></div>
<div class="abs c" style="top:396px;font-family:ISerif;font-style:italic;font-size:76px;line-height:1;color:{ink};opacity:.92">hoy, aquí en Caffany</div>
<div class="abs c" style="top:586px;z-index:3"><span class="caps" style="display:inline-block;background:{LIMA};color:{PINO};
  font-size:40px;letter-spacing:.3em;padding:18px 34px 18px 46px;border-radius:999px;border:3px solid #E9C877;
  box-shadow:0 12px 28px rgba(0,0,0,.35)">Solo hoy</span></div>
<div class="abs" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;background:{CREMA};
  box-shadow:0 30px 60px rgba(0,0,0,.35)"></div>
<img class="abs" src="salad_cesar.png" style="left:{cx - 20}px;top:{cy - 70}px;width:300px;height:300px;border-radius:50%;
  border:10px solid #fff;box-shadow:0 14px 30px rgba(0,0,0,.3)">
<img class="abs" src="vaso_kori.png" style="left:{cx - 290}px;top:{cy - 205}px;height:470px;transform:rotate(-6deg);
  filter:drop-shadow(0 16px 22px rgba(0,0,0,.35))">
<div class="abs" style="left:{cx + r - 150}px;top:{cy - r - 40}px;width:250px;height:250px;border-radius:50%;
  background:{LIMA};color:{PINO};display:flex;flex-direction:column;align-items:center;justify-content:center;
  transform:rotate(8deg);box-shadow:0 16px 34px rgba(0,0,0,.4);border:4px solid #E9C877">
  <div style="font-family:Gloock;font-size:110px;line-height:.9"><span style="font-size:48px;vertical-align:46px">$</span>219</div>
  <div class="caps" style="font-size:20px;letter-spacing:.26em;margin-top:6px">el combo</div></div>
<div class="abs c" style="top:1290px;font-family:ISerif;font-size:58px;line-height:1.15;color:{ink};padding:0 110px">
  Matcha de especialidad de Kori<br><i style="color:{LIMA}">+ Ensalada César Caffany</i></div>
<div class="abs" style="top:1480px;left:120px;width:430px;text-align:center">
  <div class="caps" style="font-size:24px;color:{LIMA};letter-spacing:.26em">Horario</div>
  <div style="font-family:Gloock;font-size:72px;line-height:1.1;color:{ink};margin-top:10px">1 pm – 9 pm</div></div>
<div class="abs" style="top:1480px;left:640px;width:430px;text-align:center">
  <div class="caps" style="font-size:24px;color:{LIMA};letter-spacing:.26em">Disponible</div>
  <div style="font-family:Gloock;font-size:72px;line-height:1.1;color:{ink};margin-top:10px">hasta agotar</div></div>
<div class="abs c" style="top:1670px">
  <div style="display:inline-flex;align-items:center;gap:30px;background:{CREMA};border-radius:22px;padding:16px 40px;
    box-shadow:0 14px 30px rgba(0,0,0,.3)">
    <img src="kori_logo_limpio.png" style="height:110px;mix-blend-mode:multiply">
    <div style="text-align:left;color:{PINO}">
      <div class="caps" style="font-size:20px;letter-spacing:.28em;color:#6b7a3a">De la UACJ a Caffany</div>
      <div style="font-family:Gloock;font-size:52px;line-height:1.1">@_korimatcha</div></div></div></div>
<div class="abs c" style="top:1940px;font-family:ISerif;font-style:italic;font-size:42px;color:{ink};opacity:.85">
  pídelo en caja: <b style="font-style:normal;font-family:Gloock;font-weight:400;color:{LIMA}">“el combo Kori”</b></div>"""
    return page(PINO, svg, html, grain=.14)


if __name__ == "__main__":
    open(os.path.join(OUT, "6-kori.html"), "w", encoding="utf-8").write(kori())
    print("ok")
