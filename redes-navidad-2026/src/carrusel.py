"""Carruseles 4:5 (1080x1350) – estilo "Nochebuena de Cacao". Uso: python3 -I carrusel.py -> html/carrusel_*.html"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import A, FONTS, PINO, PINO2, VINO, VINO2, CREMA, ORO_A, ORO_B, ORO_C, copo_svg, tam

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1350


def img(src, cx, cy, h, rot=0, sombra=True):
    iw, ih = tam(src)
    w = h * iw / ih
    sh = "filter:drop-shadow(0 26px 30px rgba(0,0,0,.55));" if sombra else ""
    return (f'<img src="file://{A}/{src}" style="position:absolute;left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;width:{w:.0f}px;'
            f'height:{h}px;transform:rotate({rot}deg);{sh}">')


def txt(html, top, size, font="g", color=CREMA, w=920, cx=540, align="center", rot=0, style=""):
    fam = {"g": "font-family:Gloock;line-height:1.02", "i": "font-family:ISerif;font-style:italic;line-height:1.12",
           "c": "font-family:ISans;font-weight:700;letter-spacing:.28em;text-transform:uppercase;line-height:1.25",
           "s": "font-family:ISans;font-weight:700;line-height:1.15", "r": "font-family:ISans;line-height:1.3"}[font]
    cls = ' class="oro"' if color == "oro" else ""
    col = "" if color == "oro" else f"color:{color};"
    left = cx - w / 2 if align == "center" else cx
    return (f'<div{cls} style="position:absolute;left:{left:.0f}px;top:{top}px;width:{w}px;text-align:{align};font-size:{size}px;'
            f'{fam};{col}transform:rotate({rot}deg);{style}">{html}</div>')


def sello(html, cx, cy, D, size, rot=0, sub=""):
    s = f'<div class="cap" style="font-size:{int(D * .075)}px;color:{VINO};margin-top:4px">{sub}</div>' if sub else ""
    return (f'<div class="sello" style="position:absolute;left:{cx - D / 2}px;top:{cy - D / 2}px;width:{D}px;height:{D}px;transform:rotate({rot}deg)">'
            f'<div class="anillo"></div><div style="font-family:Gloock;font-size:{size}px;color:{VINO};line-height:1">{html}</div>{s}</div>')


def pastilla(html, cx, cy, w, h, size, rot=0, font="c"):
    fam = "font-family:ISans;font-weight:700;letter-spacing:.2em;text-transform:uppercase" if font == "c" else "font-family:Gloock"
    return (f'<div class="pastilla" style="position:absolute;left:{cx - w / 2}px;top:{cy - h / 2}px;width:{w}px;height:{h}px;'
            f'transform:rotate({rot}deg);{fam};font-size:{size}px;color:{VINO}">{html}</div>')


def copo(cx, cy, r, op=.2):
    return f'<div style="position:absolute;left:{cx - r - 10}px;top:{cy - r - 10}px;opacity:{op}">{copo_svg(r)}</div>'


def circulo(src, cx, cy, D):
    return (f'<div style="position:absolute;left:{cx - D / 2}px;top:{cy - D / 2}px;width:{D}px;height:{D}px;border-radius:50%;overflow:hidden;'
            f'box-shadow:0 0 0 6px {ORO_B},0 0 0 14px rgba(244,221,160,.18),0 30px 50px rgba(0,0,0,.5)">'
            f'<img src="file://{A}/{src}" style="width:118%;height:118%;margin:-9%;object-fit:cover"></div>')


def lamina(fondo, cuerpo, n, total, flecha=True):
    claro = PINO2 if fondo == PINO else VINO2
    puntos = "".join(f'<span style="display:inline-block;width:{22 if k == n else 10}px;height:10px;border-radius:5px;margin:0 5px;'
                     f'background:{ORO_B if k == n else "rgba(243,234,216,.35)"}"></span>' for k in range(total))
    fl = (f'<div class="cap" style="position:absolute;right:70px;bottom:70px;font-size:22px;color:{ORO_B}">desliza →</div>') if flecha else ""
    return f"""<section style="background:radial-gradient(ellipse 85% 65% at 50% 42%,{claro} 0%,{fondo} 62%,#050403 135%)">
<svg style="position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay" width="{W}" height="{H}"><filter id="n{n}"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/></filter><rect width="100%" height="100%" filter="url(#n{n})"/></svg>
<svg style="position:absolute;inset:0" width="{W}" height="{H}"><rect x="28" y="28" width="{W - 56}" height="{H - 56}" fill="none" stroke="url(#oro)" stroke-width="3" opacity=".85"/>
<rect x="40" y="40" width="{W - 80}" height="{H - 80}" fill="none" stroke="{CREMA}" stroke-width="1.2" opacity=".3"/></svg>
<div class="cap" style="position:absolute;left:0;right:0;top:78px;text-align:center;font-size:22px;letter-spacing:.42em;color:{ORO_B}">CAFFANY · NAVIDAD 2026</div>
{cuerpo}
<div style="position:absolute;left:0;right:0;bottom:78px;text-align:center">{puntos}</div>{fl}
</section>"""


def documento(laminas):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Gloock;src:url(file://{FONTS}/Gloock-Regular.ttf)}}
@font-face{{font-family:ISerif;font-style:italic;src:url(file://{FONTS}/InstrumentSerif-Italic.ttf)}}
@font-face{{font-family:ISans;src:url(file://{FONTS}/InstrumentSans-Regular.ttf)}}
@font-face{{font-family:ISans;font-weight:700;src:url(file://{FONTS}/InstrumentSans-Bold.ttf)}}
html,body{{margin:0;padding:0;background:#000}}
section{{width:{W}px;height:{H}px;position:relative;overflow:hidden}}
.oro{{background:linear-gradient(115deg,{ORO_A} 0%,{ORO_B} 38%,{ORO_C} 62%,{ORO_B} 82%,{ORO_A} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.cap{{font-family:ISans;font-weight:700;letter-spacing:.28em;text-transform:uppercase}}
.sello{{border-radius:50%;background:radial-gradient(circle at 35% 30%,{ORO_B},{ORO_C} 55%,{ORO_A});display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.5)}}
.anillo{{position:absolute;inset:14px;border-radius:50%;border:3px dashed {VINO};opacity:.55}}
.pastilla{{border-radius:999px;background:linear-gradient(115deg,{ORO_A},{ORO_B} 40%,{ORO_C} 70%,{ORO_B});display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(0,0,0,.45)}}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="oro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORO_A}"/><stop offset=".4" stop-color="{ORO_B}"/><stop offset=".65" stop-color="{ORO_C}"/><stop offset=".85" stop-color="{ORO_B}"/><stop offset="1" stop-color="{ORO_A}"/></linearGradient></defs></svg>
{"".join(laminas)}</body></html>"""


def cierre(fondo, n, total, frase, sub):
    logo = (f'<div style="position:absolute;left:{540 - 230}px;top:300px;width:460px;height:460px;border-radius:50%;background:{CREMA};'
            f'box-shadow:0 0 0 8px {ORO_B},0 0 0 20px rgba(244,221,160,.2),0 40px 70px rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;overflow:hidden">'
            f'<img src="file://{A}/logo.png" style="width:420px;mix-blend-mode:multiply;margin-top:16px"></div>')
    c = (copo(170, 330, 70, .3) + copo(900, 760, 56, .28) + logo + txt(frase, 830, 84, "g", "oro") +
         txt(sub, 960, 50, "i") + txt("Plaza Alameda Iglesias · Cd. Juárez", 1100, 24, "c", ORO_B))
    return lamina(fondo, c, n, total, False)


# ---------------------------------------------------------------- Carrusel 1: Edición de invierno
def malvavisco():
    N = 6
    L = []
    c = (copo(150, 250, 60, .25) + copo(930, 300, 48, .22) +
         txt("Edición de invierno", 150, 34, "c", ORO_B) +
         txt("¿Ya probaste el", 205, 72, "i") +
         txt("malvavisco tostado?", 285, 108, "g", "oro") +
         img("cafe_frio.png", 270, 800, 620, -5) + img("matcha_frio.png", 810, 800, 620, 5) + img("frappe_frio.png", 540, 840, 700) +
         pastilla("$99 · 16 oz", 540, 1185, 380, 92, 32, -3))
    L.append(lamina(VINO, c, 0, N))
    fichas = [("01", "Café frío", "con leche y jarabe de <span class='oro'>malvavisco tostado</span>", "cafe_frio.png"),
              ("02", "Frappé", "cremoso, <span class='oro'>helado</span> y con su muñequito de nieve", "frappe_frio.png"),
              ("03", "Matcha", "con ese toque <span class='oro'>dulce</span> que le cae perfecto", "matcha_frio.png")]
    for k, (num, nom, det, im) in enumerate(fichas):
        izq = k % 2 == 0
        col = 300 if izq else 780
        c = (img(im, 760 if izq else 320, 720, 940, 4 if izq else -4) +
             txt(num, 220, 200, "g", "oro", 460, col) +
             txt(nom, 450, 110, "g", CREMA, 460, col) +
             txt("Malvavisco Tostado", 580, 26, "c", ORO_B, 460, col) +
             txt(det, 660, 54, "i", CREMA, 420, col) +
             sello("$99", col, 1000, 230, 92, -6, "16 oz"))
        L.append(lamina(VINO, c, k + 1, N))
    c = (txt("¿Hace frío?", 170, 130, "g", "oro") +
         txt("El café y el matcha también vienen", 330, 58, "i") +
         txt("calientes", 400, 40, "c", ORO_B) +
         img("cafe_caliente.png", 330, 820, 720, -3) + img("matcha_caliente.png", 750, 820, 720, 3))
    L.append(lamina(VINO, c, 4, N))
    L.append(cierre(VINO, 5, N, "¿Cuál pides primero?", "Solo por temporada · coméntanos 1, 2 o 3"))
    return documento(L), N


# ---------------------------------------------------------------- Carrusel 2: 3 formas de ahorrar
def ahorro():
    N = 6
    L = []
    c = (copo(160, 260, 64, .22) + copo(920, 1040, 54, .2) +
         txt("Esta Navidad", 160, 34, "c", ORO_B) +
         txt("3 formas de que tu café", 220, 70, "i") +
         txt("te salga más barato", 300, 106, "g", "oro") +
         img("termo.png", 360, 830, 700, -4) + img("cafe_frio.png", 760, 860, 620, 5) +
         pastilla("guárdalo", 540, 1190, 300, 84, 30, -3))
    L.append(lamina(PINO, c, 0, N))
    # 1 termo
    c = (txt("1", 170, 150, "g", "oro") + txt("Trae tu termo", 330, 104, "g") +
         img("termo.png", 300, 830, 700, -3) +
         sello("−$10", 760, 640, 300, 108, -6) +
         txt("en cualquier bebida,<br>fría o caliente", 830, 50, "i", CREMA, 420, 760) +
         txt("16 · 22 · 32 oz", 990, 28, "c", ORO_B, 420, 760) +
         pastilla("termo de 40 oz: Jumbo + $10", 540, 1180, 640, 86, 26, -2))
    L.append(lamina(PINO, c, 1, N))
    # 2 puntos dobles
    dias = ""
    for k, d in enumerate("LMMJVSD"):
        x = 540 - 3 * 118 + k * 118
        if k < 4:
            dias += f'<div class="sello" style="position:absolute;left:{x - 50}px;top:520px;width:100px;height:100px;font-family:Gloock;font-size:52px;color:{VINO}">{d}</div>'
        else:
            dias += (f'<div style="position:absolute;left:{x - 50}px;top:520px;width:100px;height:100px;border-radius:50%;border:2px solid rgba(243,234,216,.3);'
                     f'display:flex;align-items:center;justify-content:center;font-family:Gloock;font-size:52px;color:rgba(243,234,216,.35)">{d}</div>')
    c = (txt("2", 170, 150, "g", "oro") + txt("Puntos dobles", 330, 104, "g") +
         txt("de lunes a jueves", 450, 34, "c", ORO_B) + dias +
         txt("Normal", 700, 30, "c", CREMA, 400, 290) + txt("Lun – jue", 700, 30, "c", ORO_B, 400, 790) +
         txt("20", 750, 190, "g", "rgba(243,234,216,.5)", 400, 290) + txt("40", 740, 220, "g", "oro", 400, 790) +
         txt("→", 790, 110, "s", ORO_B, 160, 540) +
         txt("puntos por cada $100", 980, 50, "i"))
    L.append(lamina(PINO, c, 2, N))
    # 3 canjea
    filas = [("60", "Galleta de avena"), ("100", "$50 de descuento"), ("150", "Bebida de 16 oz"), ("200", "Bebida Jumbo"),
             ("300", "Poke de pollo o ensalada"), ("450", "Comida completa (hasta $300)")]
    c = txt("3", 150, 130, "g", "oro") + txt("Canjea tus puntos", 290, 92, "g")
    for k, (n, t) in enumerate(filas):
        y = 450 + k * 118
        c += (f'<div style="position:absolute;left:110px;right:110px;top:{y + 100}px;height:1px;background:rgba(244,221,160,.22)"></div>' +
              txt(n, y, 92, "g", "oro", 240, 120, "left") + txt(t, y + 22, 56, "i", CREMA, 640, 360, "left"))
    c += txt("1 punto por cada $5 · pide que te registren", 1172, 22, "c", ORO_B)
    L.append(lamina(PINO, c, 3, N))
    # haz cuentas
    c = (txt("Haz cuentas", 160, 110, "g", "oro") +
         txt("Bebida de 16 oz gratis = 150 puntos", 300, 52, "i") +
         img("matcha_frio.png", 820, 800, 560, 5) +
         txt("Cualquier día", 440, 30, "c", CREMA, 560, 120, "left") +
         txt("$750", 480, 170, "g", "rgba(243,234,216,.5)", 560, 120, "left",
             style="text-decoration:line-through;text-decoration-color:" + ORO_B + ";text-decoration-thickness:8px") +
         txt("Lunes a jueves", 720, 30, "c", ORO_B, 560, 120, "left") +
         txt("$375", 760, 210, "g", "oro", 560, 120, "left") +
         pastilla("la mitad", 300, 1100, 300, 86, 30, -3))
    L.append(lamina(PINO, c, 4, N))
    L.append(cierre(PINO, 5, N, "Mándaselo", "a tu compa del café de la tarde"))
    return documento(L), N


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "html"), exist_ok=True)
    for nombre, f in (("carrusel_malvavisco", malvavisco), ("carrusel_ahorro", ahorro)):
        html, n = f()
        open(os.path.join(BASE, "html", nombre + ".html"), "w").write(html)
        print(nombre, n)
