"""Genera los 4 flyers navideños de Caffany (HTML) para renderizar a PNG 1188x2110."""
import math, os

FONTS = "/root/.claude/skills/synced/00b5ca32-0a36-4555-a7f0-e18e9ec26a25_b827725b-720c-4425-ac5d-3ede28ac4c94/canvas-design/canvas-fonts"
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1188, 2110

PINO = "#0E2A1F"
PINO2 = "#14382A"
VINO = "#5E1019"
VINO2 = "#7A1823"
CREMA = "#F3EAD8"
TINTA = "#1B1410"
ORO_A, ORO_B, ORO_C = "#A87A2E", "#F4DDA0", "#B98B3C"


def snowflake(cx, cy, r, color, op, sw=2.0, rot=0):
    """Copo geométrico de seis brazos con ramas."""
    parts = []
    for k in range(6):
        a = math.radians(rot + k * 60)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        parts.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        for f, L in ((0.45, 0.30), (0.72, 0.20)):
            bx, by = cx + r * f * math.cos(a), cy + r * f * math.sin(a)
            for s in (-1, 1):
                b = a + s * math.radians(42)
                parts.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + r * L * math.cos(b):.1f}" y2="{by + r * L * math.sin(b):.1f}"/>')
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.09:.1f}" fill="{color}" stroke="none"/>')
    return f'<g stroke="{color}" stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="{op}">{"".join(parts)}</g>'


def star4(cx, cy, r, color, op=1):
    p = []
    for k in range(8):
        a = math.radians(k * 45 - 90)
        rr = r if k % 2 == 0 else r * 0.22
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{color}" opacity="{op}"/>'


def snow_field(seed, n, area, color, op_range=(0.10, 0.28), rmin=10, rmax=34):
    """Patrón sistemático (rejilla con jitter determinista) de copos."""
    x0, y0, x1, y1 = area
    out = []
    cols = 6
    rows = max(1, n // cols)
    for j in range(rows):
        for i in range(cols):
            h = (seed * 9301 + i * 49297 + j * 233280) % 1000 / 1000
            h2 = (seed * 1103 + i * 12345 + j * 6789) % 1000 / 1000
            x = x0 + (i + 0.5 + (h - 0.5) * 0.6) * (x1 - x0) / cols
            y = y0 + (j + 0.5 + (h2 - 0.5) * 0.6) * (y1 - y0) / rows
            r = rmin + (rmax - rmin) * h2
            op = op_range[0] + (op_range[1] - op_range[0]) * h
            if (i + j) % 3 == 0:
                out.append(snowflake(x, y, r, color, op, sw=1.6, rot=h * 30))
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2 + 3 * h:.1f}" fill="{color}" opacity="{op * 1.3:.2f}"/>')
    return "".join(out)


def frame(color_line, star_color):
    m1, m2 = 44, 58
    s = [f'<rect x="{m1}" y="{m1}" width="{W - 2 * m1}" height="{H - 2 * m1}" fill="none" stroke="url(#oro)" stroke-width="3"/>',
         f'<rect x="{m2}" y="{m2}" width="{W - 2 * m2}" height="{H - 2 * m2}" fill="none" stroke="{color_line}" stroke-width="1.2" opacity=".55"/>']
    for (cx, cy) in ((m1, m1), (W - m1, m1), (m1, H - m1), (W - m1, H - m1)):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{star_color}"/>')
        s.append(star4(cx, cy, 30, "url(#oro)"))
    return "".join(s)


def page(bg, body_svg, body_html, grain=0.10, extra_css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Gloock;src:url(file://{FONTS}/Gloock-Regular.ttf)}}
@font-face{{font-family:ISerif;src:url(file://{FONTS}/InstrumentSerif-Regular.ttf)}}
@font-face{{font-family:ISerif;font-style:italic;src:url(file://{FONTS}/InstrumentSerif-Italic.ttf)}}
@font-face{{font-family:ISans;src:url(file://{FONTS}/InstrumentSans-Regular.ttf)}}
@font-face{{font-family:ISans;font-weight:700;src:url(file://{FONTS}/InstrumentSans-Bold.ttf)}}
html,body{{margin:0;padding:0}}
body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{bg};font-family:ISans}}
svg.layer{{position:absolute;inset:0}}
.abs{{position:absolute}}
.oro{{background:linear-gradient(115deg,{ORO_A} 0%,{ORO_B} 38%,{ORO_C} 62%,{ORO_B} 82%,{ORO_A} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.caps{{font-family:ISans;font-weight:700;letter-spacing:.32em;text-transform:uppercase}}
.c{{left:0;right:0;text-align:center}}
{extra_css}
</style></head><body>
<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="oro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORO_A}"/><stop offset=".4" stop-color="{ORO_B}"/><stop offset=".65" stop-color="{ORO_C}"/><stop offset=".85" stop-color="{ORO_B}"/><stop offset="1" stop-color="{ORO_A}"/></linearGradient>
<radialGradient id="luz" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>
<radialGradient id="sombra" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<filter id="grano"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#luz)"/>
{body_svg}
<rect width="{W}" height="{H}" filter="url(#grano)" opacity="{grain}" style="mix-blend-mode:overlay"/>
</svg>
{body_html}
</body></html>"""


def header(color_small, sub="Navidad · 2026"):
    return f"""
<div class="abs c caps" style="top:112px;font-size:30px;color:{color_small}">Caffany</div>
<div class="abs c" style="top:150px;font-family:ISerif;font-style:italic;font-size:36px;color:{color_small};opacity:.8">{sub}</div>"""


def rule_svg(y, x0, x1, color, op=.7, diamond=True):
    s = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{color}" stroke-width="1.5" opacity="{op}"/>'
    if diamond:
        cx = (x0 + x1) / 2
        s += f'<rect x="{cx - 7}" y="{y - 7}" width="14" height="14" transform="rotate(45 {cx} {y})" fill="url(#oro)"/>'
    return s


# ---------------------------------------------------------------- 1. RECOMPENSAS
def recompensas():
    rows = [("60", "Galleta de avena", "la de siempre, recién horneada"),
            ("100", "$50 en tu orden", "en lo que quieras"),
            ("150", "Bebida 16 oz", "la que tú elijas"),
            ("200", "Bebida jumbo 32 oz", "la que tú elijas"),
            ("300", "Poke o ensalada", "hasta $199"),
            ("450", "Tu comida, gratis", "hasta $300 en tu orden")]
    y0, step = 610, 205
    svg = snow_field(3, 12, (90, 80, W - 90, 520), CREMA, (0.08, 0.24))
    svg += snow_field(5, 12, (90, 1880, W - 90, 2040), CREMA, (0.05, 0.14), 8, 22)
    svg += frame(CREMA, PINO)
    # escalera: línea vertical con nodos crecientes
    lx = 190
    svg += f'<line x1="{lx}" y1="{y0 + 30}" x2="{lx}" y2="{y0 + step * 5 + 70}" stroke="url(#oro)" stroke-width="2.5"/>'
    html = header(CREMA)
    html += f"""
<div class="abs c" style="top:238px;font-family:Gloock;font-size:150px;line-height:1;color:{CREMA};letter-spacing:-.01em">Recompensas</div>
<div class="abs c oro" style="top:392px;font-family:ISerif;font-style:italic;font-size:76px;line-height:1">canjea tus puntos</div>"""
    svg += rule_svg(530, 330, W - 330, CREMA, .5)
    for i, (pts, nombre, det) in enumerate(rows):
        y = y0 + i * step
        r = 12 + i * 3.2
        svg += f'<circle cx="{lx}" cy="{y + 66}" r="{r + 9}" fill="{PINO}"/>'
        svg += f'<circle cx="{lx}" cy="{y + 66}" r="{r}" fill="url(#oro)"/>'
        if i < 5:
            svg += f'<line x1="300" y1="{y + step - 22}" x2="{W - 110}" y2="{y + step - 22}" stroke="{CREMA}" stroke-width="1" opacity=".18" stroke-dasharray="2 10"/>'
        html += f"""
<div class="abs oro" style="top:{y}px;left:250px;width:250px;text-align:right;font-family:Gloock;font-size:118px;line-height:1">{pts}</div>
<div class="abs caps" style="top:{y + 126}px;left:250px;width:250px;text-align:right;font-size:20px;color:{CREMA};opacity:.6;letter-spacing:.4em">puntos</div>
<div class="abs" style="top:{y + 14}px;left:548px;width:560px;font-family:ISerif;font-size:64px;line-height:1.02;color:{CREMA}">{nombre}</div>
<div class="abs" style="top:{y + 92}px;left:550px;width:560px;font-family:ISerif;font-style:italic;font-size:36px;color:{CREMA};opacity:.62">{det}</div>"""
    html += f"""
<div class="abs c caps" style="top:1888px;font-size:28px;color:{CREMA};letter-spacing:.24em">1 punto por cada $5</div>
<div class="abs c" style="top:1938px;font-family:ISerif;font-style:italic;font-size:44px;color:{CREMA};opacity:.85">pide en caja que te registren</div>"""
    svg += rule_svg(1858, 380, W - 380, CREMA, .45, diamond=False)
    return page(PINO, svg, html)


# ---------------------------------------------------------------- 2. MALVAVISCO
# retícula: 5 huecos iguales 320x476 (fotos 2:3, base del vaso al 94 %)
CW, CH = 320, 476
HOT = {"cafe": (240, 536, CW, CH), "matcha": (628, 536, CW, CH)}
CUPS = {"izq": (70, 1134, CW, CH), "cen": (434, 1134, CW, CH), "der": (798, 1134, CW, CH)}


def malvavisco():
    svg = snow_field(11, 18, (90, 70, W - 90, 520), CREMA, (0.07, 0.22))
    svg += snow_field(13, 6, (90, 1690, W - 90, 1760), CREMA, (0.05, 0.14), 8, 20)
    svg += frame(CREMA, VINO)
    for k, (x, y, w, h) in list(HOT.items()) + list(CUPS.items()):
        svg += f'<ellipse cx="{x + w / 2}" cy="{y + h * .94}" rx="{w * .30}" ry="16" fill="url(#sombra)"/>'
    html = header(CREMA, "edición de invierno")
    html += f"""
<div class="abs c" style="top:214px;font-family:Gloock;font-size:132px;line-height:1;color:{CREMA}">Malvavisco</div>
<div class="abs c oro" style="top:344px;font-family:ISerif;font-style:italic;font-size:104px;line-height:1">tostado</div>"""
    svg += rule_svg(478, 400, W - 400, CREMA, .45)

    def tag(y, txt):
        nonlocal svg, html
        html += f'<div class="abs c caps" style="top:{y}px;font-size:24px;color:{ORO_B};letter-spacing:.36em">{txt}</div>'
        svg += f'<line x1="330" y1="{y + 13}" x2="470" y2="{y + 13}" stroke="url(#oro)" stroke-width="1.5"/><line x1="718" y1="{y + 13}" x2="858" y2="{y + 13}" stroke="url(#oro)" stroke-width="1.5"/>'

    tag(506, "calientes")
    for name, (x, y, w, h) in (("Café", HOT["cafe"]), ("Matcha", HOT["matcha"])):
        html += f'<div class="abs caps" style="top:{y + h * .94 + 18:.0f}px;left:{x - 40}px;width:{w + 80}px;text-align:center;font-size:26px;color:{CREMA}">{name}</div>'
    tag(1088, "frías")
    for name, k in (("Frappé", "izq"), ("Café frío", "cen"), ("Matcha", "der")):
        x, y, w, h = CUPS[k]
        html += f'<div class="abs caps" style="top:{y + h * .94 + 18:.0f}px;left:{x - 40}px;width:{w + 80}px;text-align:center;font-size:26px;color:{CREMA}">{name}</div>'
    svg += rule_svg(1700, 420, W - 420, CREMA, .35, diamond=False)
    cx, cy, R = 594, 1870, 104
    svg += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#oro)"/><circle cx="{cx}" cy="{cy}" r="{R - 11}" fill="none" stroke="{VINO}" stroke-width="2" stroke-dasharray="3 7"/>'
    html += f"""
<div class="abs" style="top:{cy - 66}px;left:{cx - 100}px;width:200px;text-align:center;font-family:Gloock;font-size:84px;line-height:1;color:{VINO}">$99</div>
<div class="abs caps" style="top:{cy + 24}px;left:{cx - 100}px;width:200px;text-align:center;font-size:18px;color:{VINO};letter-spacing:.2em">c/u · 16 oz</div>
<div class="abs" style="top:{cy - 42}px;left:96px;width:340px;font-family:ISerif;font-style:italic;font-size:36px;line-height:1.15;color:{CREMA};opacity:.85;text-align:right">decorados a mano por nuestro equipo</div>
<div class="abs caps" style="top:{cy - 36}px;left:752px;width:340px;font-size:21px;line-height:1.8;color:{CREMA};opacity:.75;letter-spacing:.26em">sólo por<br>temporada</div>"""
    return page(VINO, svg, html, grain=.12)


# ---------------------------------------------------------------- 3. PUNTOS DOBLES
def dobles():
    svg = snow_field(21, 18, (90, 70, W - 90, 520), CREMA, (0.08, 0.24))
    svg += snow_field(23, 12, (90, 1720, W - 90, 2030), CREMA, (0.05, 0.15), 8, 24)
    svg += frame(CREMA, PINO)
    html = header(CREMA)
    html += f"""
<div class="abs c" style="top:236px;font-family:Gloock;font-size:150px;line-height:1;color:{CREMA}">Puntos</div>
<div class="abs c oro" style="top:378px;font-family:ISerif;font-style:italic;font-size:124px;line-height:1">dobles</div>
<div class="abs c oro" style="top:520px;font-family:Gloock;font-size:520px;line-height:1;letter-spacing:-.02em">×2</div>"""
    # calendario
    dias = ["L", "M", "M", "J", "V", "S", "D"]
    bw, gap = 118, 18
    tot = 7 * bw + 6 * gap
    x0 = (W - tot) / 2
    yc = 1150
    for i, d in enumerate(dias):
        x = x0 + i * (bw + gap)
        on = i < 4
        if on:
            svg += f'<rect x="{x}" y="{yc}" width="{bw}" height="{bw}" rx="8" fill="url(#oro)"/>'
        else:
            svg += f'<rect x="{x + 1}" y="{yc + 1}" width="{bw - 2}" height="{bw - 2}" rx="8" fill="none" stroke="{CREMA}" stroke-width="1.5" opacity=".28"/>'
        col = PINO if on else CREMA
        op = 1 if on else .35
        html += f'<div class="abs" style="top:{yc + 18}px;left:{x}px;width:{bw}px;text-align:center;font-family:Gloock;font-size:70px;line-height:1;color:{col};opacity:{op}">{d}</div>'
    html += f"""
<div class="abs c caps" style="top:{yc + 160}px;font-size:32px;color:{CREMA};letter-spacing:.3em">lunes a jueves</div>"""
    svg += rule_svg(1385, 380, W - 380, CREMA, .45)
    html += f"""
<div class="abs c" style="top:1440px;font-family:ISerif;font-size:58px;line-height:1.15;color:{CREMA}">Cada $100 de consumo te da</div>
<div class="abs c" style="top:1520px;font-family:Gloock;font-size:96px;line-height:1.1;color:{CREMA}"><span style="opacity:.42;text-decoration:line-through;text-decoration-thickness:4px">20</span>&nbsp;&nbsp;<span class="oro">40 puntos</span></div>
<div class="abs c" style="top:1690px;font-family:ISerif;font-style:italic;font-size:48px;color:{CREMA};opacity:.85">llega más rápido a tu bebida gratis</div>
<div class="abs c caps" style="top:1900px;font-size:28px;color:{CREMA};letter-spacing:.24em">pide en caja que te registren</div>"""
    return page(PINO2, svg, html)


# ---------------------------------------------------------------- 4. REFILL
TERMO = (379, 860, 430, 640)


def refill():
    ink = PINO
    svg = snow_field(31, 18, (90, 70, W - 90, 520), PINO, (0.05, 0.14))
    svg += frame(PINO, CREMA)
    x, y, w, h = TERMO
    # disco dorado detrás del termo
    svg += f'<circle cx="{x + w / 2}" cy="{y + h * .52}" r="330" fill="{PINO}"/>'
    svg += f'<circle cx="{x + w / 2}" cy="{y + h * .52}" r="346" fill="none" stroke="url(#oro)" stroke-width="3"/>'
    svg += f'<circle cx="{x + w / 2}" cy="{y + h * .52}" r="360" fill="none" stroke="{PINO}" stroke-width="1" opacity=".4" stroke-dasharray="2 9"/>'
    svg += snow_field(37, 12, (x + w / 2 - 300, y + h * .52 - 300, x + w / 2 + 300, y + h * .52 + 300), CREMA, (0.08, 0.22), 8, 22)
    svg += f'<ellipse cx="{x + w / 2}" cy="{y + h - 10}" rx="150" ry="22" fill="url(#sombra)"/>'
    html = header(ink, "refill")
    html += f"""
<div class="abs c" style="top:236px;font-family:Gloock;font-size:150px;line-height:1;color:{ink}">Trae tu termo</div>
<div class="abs c" style="top:404px;font-family:ISerif;font-style:italic;font-size:64px;line-height:1;color:{VINO2}">y te lo llenamos con cualquier bebida</div>"""
    svg += rule_svg(530, 400, W - 400, ink, .4)
    html += f"""
<div class="abs c" style="top:580px;font-family:Gloock;font-size:190px;line-height:1;color:{VINO}">$10 menos</div>"""
    # notas al pie en dos columnas
    html += f"""
<div class="abs" style="top:1640px;left:120px;width:430px">
  <div class="caps" style="font-size:24px;color:{VINO};letter-spacing:.26em">¿Más de 32 oz?</div>
  <div style="font-family:ISerif;font-size:50px;line-height:1.1;color:{ink};margin-top:14px">Lo llenamos por +$10</div>
  <div style="font-family:ISerif;font-style:italic;font-size:36px;color:{VINO};margin-top:8px">máximo 40 oz</div>
</div>
<div class="abs" style="top:1640px;left:640px;width:430px">
  <div class="caps" style="font-size:24px;color:{VINO};letter-spacing:.26em">Por favor</div>
  <div style="font-family:ISerif;font-size:50px;line-height:1.1;color:{ink};margin-top:14px">tráelo limpio y vacío</div>
</div>
<div class="abs c" style="top:1900px;font-family:ISerif;font-style:italic;font-size:46px;color:{ink};opacity:.8">menos vasos, más Navidad</div>"""
    svg += f'<line x1="594" y1="1640" x2="594" y2="1790" stroke="{ink}" stroke-width="1" opacity=".3"/>'
    svg += rule_svg(1860, 420, W - 420, ink, .35, diamond=False)
    return page(CREMA, svg, html, grain=.16)


if __name__ == "__main__":
    for name, fn in (("1-recompensas", recompensas), ("2-malvavisco", malvavisco), ("3-puntos-dobles", dobles), ("4-refill", refill)):
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(fn())
    print("ok")
