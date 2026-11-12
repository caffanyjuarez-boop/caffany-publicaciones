"""Motor de los videos verticales (1080x1920) de Navidad 2026 – estilo "Nochebuena de Cacao".

Cada video es una página HTML con elementos que tienen tiempo de entrada/salida (data-in/data-out) y una función
seek(t) que deja la página exactamente como debe verse en el segundo t. render.js la recorre cuadro por cuadro.
Uso: python3 -I motor.py  (genera html/<video>.html)
"""
import json, math, os, re
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(BASE, "assets")
FONTS = "/root/.claude/skills/synced/00b5ca32-0a36-4555-a7f0-e18e9ec26a25_b827725b-720c-4425-ac5d-3ede28ac4c94/canvas-design/canvas-fonts"
W, H, CX = 1080, 1920, 490          # CX: centro de la zona segura (x 60–920)

PINO, PINO2 = "#0E2A1F", "#1A4433"
VINO, VINO2 = "#4A0C14", "#7A1823"
CREMA, ORO_A, ORO_B, ORO_C = "#F3EAD8", "#A87A2E", "#F4DDA0", "#C9993F"

ARREGLOS = {"visión": "edición", "Caffé": "Caffany", "Cafeny": "Caffany", "Cafany,": "Caffany,", "Cafany": "Caffany"}
QUITAR = {"Bene", "Ne"}

_size = {}


def tam(src):
    if src not in _size:
        _size[src] = Image.open(os.path.join(A, src)).size
    return _size[src]


def attrs(tin, tout=None, a="up", d=.45, loop="", rot=0, extra=""):
    s = f'data-in="{tin:.3f}" data-a="{a}" data-d="{d}"'
    if tout is not None:
        s += f' data-out="{tout:.3f}"'
    if loop:
        s += f' data-loop="{loop}"'
    if rot:
        s += f' data-rot="{rot}"'
    return s + " " + extra


def T(html, top, size, tin, tout=None, a="up", font="g", color=CREMA, w=860, cx=CX, align="center", d=.45,
      loop="", rot=0, extra="", style=""):
    """Texto. font: g=Gloock, i=Instrument Serif itálica, c=versalitas Instrument Sans, s=Instrument Sans negrita."""
    fam = {"g": "font-family:Gloock;line-height:1.02",
           "i": "font-family:ISerif;font-style:italic;line-height:1.1",
           "c": "font-family:ISans;font-weight:700;letter-spacing:.28em;text-transform:uppercase;line-height:1.2",
           "s": "font-family:ISans;font-weight:700;line-height:1.1"}[font]
    left = cx - w / 2 if align == "center" else cx
    cls = "oro" if color == "oro" else ""
    col = "" if color == "oro" else f"color:{color};"
    return (f'<div class="el {cls}" {attrs(tin, tout, a, d, loop, rot, extra)} style="left:{left:.0f}px;top:{top}px;'
            f'width:{w}px;text-align:{align};font-size:{size}px;{fam};{col}{style}">{html}</div>')


def I(src, cx, cy, h, tin, tout=None, a="pop", loop="float", d=.5, rot=0, shadow=True, extra="", style=""):
    iw, ih = tam(src)
    w = h * iw / ih
    sh = "filter:drop-shadow(0 28px 34px rgba(0,0,0,.55));" if shadow else ""
    return (f'<div class="el" {attrs(tin, tout, a, d, loop, rot, extra)} style="left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;'
            f'width:{w:.0f}px;height:{h}px;{style}"><img src="file://{A}/{src}" style="width:100%;height:100%;{sh}"></div>')


def B(inner, cx, cy, w, h, tin, tout=None, a="pop", loop="", d=.45, rot=0, extra="", style=""):
    """Caja libre centrada en (cx, cy)."""
    return (f'<div class="el" {attrs(tin, tout, a, d, loop, rot, extra)} style="left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;'
            f'width:{w}px;height:{h}px;{style}">{inner}</div>')


def sello(txt, cx, cy, D, tin, tout=None, a="stamp", size=None, loop="", rot=0, extra="", sub=""):
    size = size or int(D * .34)
    sub_html = f'<div class="cap" style="font-size:{int(D * .07)}px;color:{VINO};margin-top:6px">{sub}</div>' if sub else ""
    inner = (f'<div class="sello" style="width:{D}px;height:{D}px"><div class="anillo"></div>'
             f'<div style="font-family:Gloock;font-size:{size}px;color:{VINO};line-height:1">{txt}</div>{sub_html}</div>')
    return B(inner, cx, cy, D, D, tin, tout, a, loop, .5, rot, extra)


def pastilla(txt, cx, cy, w, h, tin, tout=None, a="stamp", size=56, rot=0, font="c", extra=""):
    fam = "font-family:ISans;font-weight:700;letter-spacing:.2em;text-transform:uppercase" if font == "c" else "font-family:Gloock"
    inner = (f'<div class="pastilla" style="width:{w}px;height:{h}px;{fam};font-size:{size}px;color:{VINO}">{txt}</div>')
    return B(inner, cx, cy, w, h, tin, tout, a, "", .45, rot, extra)


def tachar(txt_html, top, size, tin, tout, st, color=CREMA, font="g", w=860, cx=CX):
    inner = f'<span class="tach">{txt_html}<i class="line"></i></span>'
    return T(inner, top, size, tin, tout, "up", font, color, w, cx, extra=f'data-st="{st:.3f}"')


def contar(pre, a0, a1, suf, top, size, tin, tout, cd=.8, color="oro", w=860, cx=CX, a="pop", font="g"):
    html = f'{pre}<span class="num">{a0}</span>{suf}'
    return T(html, top, size, tin, tout, a, font, color, w, cx, extra=f'data-count="{a0},{a1}" data-cd="{cd}"')


def copo_svg(r=200, color=ORO_B, sw=5):
    parts = []
    c = r + 10
    for k in range(6):
        ang = math.radians(k * 60 - 90)
        x2, y2 = c + r * math.cos(ang), c + r * math.sin(ang)
        parts.append(f'<line x1="{c}" y1="{c}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        for f, L in ((.45, .3), (.72, .2)):
            bx, by = c + r * f * math.cos(ang), c + r * f * math.sin(ang)
            for s in (-1, 1):
                b = ang + s * math.radians(42)
                parts.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + r * L * math.cos(b):.1f}" y2="{by + r * L * math.sin(b):.1f}"/>')
    return (f'<svg width="{2 * c}" height="{2 * c}" viewBox="0 0 {2 * c} {2 * c}"><g stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" fill="none">{"".join(parts)}</g></svg>')


def copo(cx, cy, r, tin, tout=None, op=.25, a="pop"):
    return B(f'<div style="opacity:{op}">{copo_svg(r)}</div>', cx, cy, 2 * r + 20, 2 * r + 20, tin, tout, a, "spin", .6)


def foto_circulo(src, cx, cy, D, tin, tout=None, a="pop"):
    inner = (f'<div style="width:{D}px;height:{D}px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 6px {ORO_B},'
             f'0 0 0 14px rgba(244,221,160,.18),0 30px 50px rgba(0,0,0,.5)"><img src="file://{A}/{src}" '
             f'style="width:118%;height:118%;margin:-9%;object-fit:cover"></div>')
    return B(inner, cx, cy, D, D, tin, tout, a, "float", .5)


ICONOS = {
    "guardar": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M24 10h52a4 4 0 0 1 4 4v78L50 72 20 92V14a4 4 0 0 1 4-4z" fill="url(#g)" stroke="{ORO_A}" stroke-width="2"/>'
               f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORO_A}"/><stop offset=".45" stop-color="{ORO_B}"/><stop offset="1" stop-color="{ORO_C}"/></linearGradient></defs></svg>',
    "enviar": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><defs><linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORO_A}"/><stop offset=".45" stop-color="{ORO_B}"/><stop offset="1" stop-color="{ORO_C}"/></linearGradient></defs>'
              f'<path d="M8 46 92 10 70 90 48 62z" fill="url(#g2)"/><path d="M48 62 92 10 34 54z" fill="{ORO_A}" opacity=".7"/><path d="M48 62 42 84 34 54z" fill="{ORO_A}"/></svg>',
    "comentario": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M12 14h76a6 6 0 0 1 6 6v46a6 6 0 0 1-6 6H40L20 90V72h-8a6 6 0 0 1-6-6V20a6 6 0 0 1 6-6z" fill="{CREMA}"/>'
                  f'<circle cx="32" cy="43" r="6" fill="{VINO2}"/><circle cx="50" cy="43" r="6" fill="{VINO2}"/><circle cx="68" cy="43" r="6" fill="{VINO2}"/></svg>',
    "check": f'<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M18 52 40 74 84 26" fill="none" stroke="{VINO}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def final(t0, dur):
    """Tarjeta de cierre: logo + Síguenos."""
    logo = (f'<div style="width:520px;height:520px;border-radius:50%;background:{CREMA};box-shadow:0 0 0 8px {ORO_B},0 0 0 20px rgba(244,221,160,.2),'
            f'0 40px 70px rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;overflow:hidden">'
            f'<img src="file://{A}/logo.png" style="width:470px;mix-blend-mode:multiply;margin-top:18px"></div>')
    s = [B(logo, CX, 700, 520, 520, t0, None, "pop", "float", .6),
         copo(150, 470, 70, t0 + .2, None, .35), copo(840, 980, 56, t0 + .3, None, .3),
         T("Síguenos", 1010, 150, t0 + .25, None, "up", "g", "oro"),
         T("para no perderte lo nuevo", 1180, 56, t0 + .45, None, "up", "i", CREMA),
         T("Plaza Alameda Iglesias · Cd. Juárez", 1268, 26, t0 + .6, None, "fade", "c", ORO_B)]
    return "".join(s)


def palabras(nombre):
    ws = json.load(open(os.path.join(BASE, "src", "palabras", nombre + ".json")))["words"]
    out = []
    for w in ws:
        if w.get("type") != "word":
            continue
        t = w["text"]
        if t in QUITAR:
            continue
        t = ARREGLOS.get(t, t)
        out.append({"text": t, "start": w["start"], "end": w["end"]})
    return out


def pagina(nombre, fondo, cuerpo, dur, fin_subs, extra_css=""):
    words = palabras(nombre)
    claro = PINO2 if fondo == PINO else VINO2
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Gloock;src:url(file://{FONTS}/Gloock-Regular.ttf)}}
@font-face{{font-family:ISerif;font-style:italic;src:url(file://{FONTS}/InstrumentSerif-Italic.ttf)}}
@font-face{{font-family:ISerif;src:url(file://{FONTS}/InstrumentSerif-Regular.ttf)}}
@font-face{{font-family:ISans;src:url(file://{FONTS}/InstrumentSans-Regular.ttf)}}
@font-face{{font-family:ISans;font-weight:700;src:url(file://{FONTS}/InstrumentSans-Bold.ttf)}}
html,body{{margin:0;padding:0}}
body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:radial-gradient(ellipse 85% 60% at 50% 42%,{claro} 0%,{fondo} 62%,#050403 130%);font-family:ISans}}
.el{{position:absolute;visibility:hidden;transform-origin:50% 50%;will-change:transform,opacity}}
.oro{{background:linear-gradient(115deg,{ORO_A} 0%,{ORO_B} 38%,{ORO_C} 62%,{ORO_B} 82%,{ORO_A} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.cap{{font-family:ISans;font-weight:700;letter-spacing:.28em;text-transform:uppercase}}
.sello{{border-radius:50%;background:radial-gradient(circle at 35% 30%,{ORO_B},{ORO_C} 55%,{ORO_A});display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;box-shadow:0 30px 60px rgba(0,0,0,.5)}}
.anillo{{position:absolute;inset:14px;border-radius:50%;border:3px dashed {VINO};opacity:.55}}
.pastilla{{border-radius:999px;background:linear-gradient(115deg,{ORO_A},{ORO_B} 40%,{ORO_C} 70%,{ORO_B});display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(0,0,0,.45)}}
.tach{{position:relative;display:inline-block}}
.tach .line{{position:absolute;left:-4%;top:52%;height:.09em;width:0;background:{ORO_B};box-shadow:0 0 12px rgba(0,0,0,.5);transform:rotate(-6deg)}}
.dia{{border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Gloock}}
#snow{{position:absolute;inset:0}}
#marco{{position:absolute;inset:0;pointer-events:none}}
#grano{{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay}}
#bar{{position:absolute;left:0;top:0;height:10px;width:0;background:linear-gradient(90deg,{ORO_A},{ORO_B},{ORO_C})}}
#subs{{position:absolute;left:60px;width:860px;top:1345px;text-align:center;font-family:ISans;font-weight:700;font-size:62px;line-height:1.15;color:{CREMA};
  text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 24px rgba(0,0,0,.7);transform-origin:50% 50%}}
#subs span{{opacity:.55}} #subs span.on{{opacity:1;color:{ORO_B}}}
#tag{{position:absolute;left:60px;width:860px;top:262px;text-align:center;font-family:ISans;font-weight:700;font-size:24px;letter-spacing:.42em;color:{ORO_B};opacity:.9}}
{extra_css}
</style></head><body>
<canvas id="snow" width="{W}" height="{H}"></canvas>
<svg id="grano" width="{W}" height="{H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
<svg id="marco" width="{W}" height="{H}"><defs><linearGradient id="oro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORO_A}"/><stop offset=".4" stop-color="{ORO_B}"/><stop offset=".65" stop-color="{ORO_C}"/><stop offset=".85" stop-color="{ORO_B}"/><stop offset="1" stop-color="{ORO_A}"/></linearGradient></defs>
<rect x="28" y="28" width="{W - 56}" height="{H - 56}" fill="none" stroke="url(#oro)" stroke-width="3" opacity=".8"/>
<rect x="40" y="40" width="{W - 80}" height="{H - 80}" fill="none" stroke="{CREMA}" stroke-width="1.2" opacity=".3"/></svg>
<div id="tag">CAFFANY · NAVIDAD 2026</div>
{cuerpo}
<div id="subs"></div>
<div id="bar"></div>
<script>
window.DUR={dur:.3f}; window.FIN_SUBS={fin_subs:.3f};
window.WORDS={json.dumps(words, ensure_ascii=False)};
</script>
<script src="file://{BASE}/src/motor.js"></script>
</body></html>"""


# ---------------------------------------------------------------- video 1: Malvavisco Tostado
def malvavisco():
    s = []
    # A 0–1.7 gancho
    s += [I("cafe_frio.png", CX, 905, 760, 0, 1.7, "zoomin", "drift"),
          T("Esto no es un", 330, 74, 0, 1.7, "up", "i"),
          T("café normal", 405, 128, .62, 1.7, "stamp", "g", "oro")]
    # B 1.7–4.6 acercamiento al muñequito
    s += [I("cafe_frio.png", 356, 470, 1700, 1.7, 4.6, "zoomin", "drift", shadow=False),
          B(f'<div style="width:100%;height:100%;border-radius:50%;border:5px dashed {ORO_B};box-shadow:0 0 30px rgba(244,221,160,.5)"></div>',
            CX, 790, 520, 520, 2.12, 4.6, "pop", "spin"),
          T("¿Ves ese <span class='oro'>muñequito</span> de nieve?", 330, 70, 1.76, 3.24, "up", "i",
            style="text-shadow:0 4px 20px rgba(0,0,0,.8)"),
          B(f'<div style="background:rgba(60,8,16,.9);border:2px solid {ORO_B};border-radius:28px;padding:22px 10px;text-align:center">'
            f'<div style="font-family:Gloock;font-size:104px;line-height:1" class="oro">Malvavisco</div>'
            f'<div class="cap" style="font-size:40px;color:{CREMA};margin-top:10px">tostado</div></div>', CX, 1180, 700, 220, 3.24, 4.6, "stamp", rot=-3)]
    # C 4.6–7.5 edición de invierno, son tres
    s += [T("Llegó la", 330, 70, 4.9, 7.5, "up", "i"),
          T("Edición de invierno", 405, 84, 5.1, 7.5, "up", "g", "oro", w=900),
          T("y son tres", 525, 34, 6.6, 7.5, "fade", "c", CREMA),
          I("cafe_frio.png", 205, 945, 560, 5.25, 7.5, "pop"),
          I("frappe_frio.png", CX, 945, 600, 5.75, 7.5, "pop"),
          I("matcha_frio.png", 775, 945, 560, 6.25, 7.5, "pop")]
    # D/E/F 01-02-03

    def ficha(num, img, nombre, det, t0, t1, lado, tdet, extra=()):
        out = []
        img_cx, col_cx = (650, 280) if lado == "der" else (330, 700)
        out.append(I(img, img_cx, 880, 800, t0 + .05, t1, "right" if lado == "der" else "left", "float"))
        out.append(T(num, 400, 210, t0, t1, "stamp", "g", "oro", w=420, cx=col_cx))
        out.append(T(nombre, 640, 110, t0 + .25, t1, "up", "g", CREMA, w=420, cx=col_cx))
        out.append(T(det, 900, 54, tdet, t1, "up", "i", CREMA, w=400, cx=col_cx))
        out.extend(extra)
        return out
    s += ficha("01", "cafe_frio.png", "Café<br>frío", "con leche y jarabe de <span class='oro'>malvavisco tostado</span>", 7.55, 11.1, "der", 8.94)
    s += ficha("02", "frappe_frio.png", "Frappé", "cremoso y <span class='oro'>helado</span>", 11.15, 15.95, "izq", 12.56,
               [pastilla("hielo en diciembre: sí", 700, 1130, 400, 96, 14.42, 15.95, size=24, rot=-4)])
    s += ficha("03", "matcha_frio.png", "Matcha", "con ese toque <span class='oro'>dulce</span> que le cae perfecto", 15.95, 19.45, "der", 17.56)
    # G 19.45–22.45 calientes
    s += [B(f'<div style="width:100%;height:100%;background:radial-gradient(ellipse at 50% 60%,rgba(201,153,63,.35),rgba(0,0,0,0) 70%)"></div>',
            540, 960, 1080, 1920, 19.45, 22.45, "fade", d=.8),
          T("¿Hace frío?", 330, 130, 19.54, 22.45, "stamp", "g", "oro"),
          T("también calientes", 500, 34, 21.16, 22.45, "fade", "c", CREMA),
          I("cafe_caliente.png", 300, 920, 700, 20.45, 22.45, "left"),
          I("matcha_caliente.png", 690, 920, 700, 20.85, 22.45, "right")]
    # H 22.45–25.5 precio
    s += [T("cada uno", 340, 36, 22.54, 25.5, "fade", "c", CREMA),
          sello('$<span class="num">0</span>', CX, 760, 560, 22.9, 25.5, "pop", 210,
                extra='data-count="0,99" data-cd=".7"'),
          T("en <span class='oro'>16 oz</span>", 1090, 84, 24.3, 25.5, "up", "i"),
          copo(160, 520, 60, 22.6, 25.5, .3), copo(850, 1040, 50, 22.7, 25.5, .3)]
    # I 25.5–26.95 temporada
    s += [copo(CX, 820, 300, 25.5, 26.95, .1),
          T("Solo por<br>temporada", 640, 140, 25.8, 26.95, "stamp", "g", "oro", rot=-4)]
    # J 26.95–29.3 ¿cuál pides primero?
    s += [T("¿Cuál pides<br><span class='oro'>primero?</span>", 330, 112, 26.98, 29.3, "up", "g"),
          I("cafe_frio.png", 205, 960, 470, 27.1, 29.3, "pop"),
          I("frappe_frio.png", CX, 960, 500, 27.25, 29.3, "pop"),
          I("matcha_frio.png", 775, 960, 470, 27.4, 29.3, "pop"),
          B(ICONOS["comentario"], 790, 640, 190, 190, 28.08, 29.3, "pop", "pulse", rot=6),
          T("te leo en comentarios", 1225, 30, 28.2, 29.3, "fade", "c", ORO_B)]
    dur = 33.4
    s.append(final(29.3, dur))
    return pagina("malvavisco", VINO, "".join(s), dur, 29.3), dur, [0, 1.7, 4.6, 7.55, 11.15, 15.95, 19.45, 22.45, 25.5, 26.95, 29.3]


# ---------------------------------------------------------------- video 2: Trae tu termo
def termo():
    s = []
    s += [I("termo.png", CX, 940, 760, 0, 1.95, "zoomin", "float"),
          T("¿Tienes un", 330, 74, 0, 1.95, "up", "i"),
          T("termo guardado?", 410, 96, .5, 1.95, "stamp", "g", "oro")]
    # B 1.95–4.1
    s += [T("¡Sácalo!", 330, 170, 2.06, 4.1, "stamp", "g", "oro"),
          T("te ahorra dinero", 540, 36, 3.42, 4.1, "fade", "c", CREMA),
          I("termo.png", CX, 960, 700, 2.1, 4.1, "up", "float", d=.6)]
    # C 4.1–6.5 cualquier bebida
    s += [T("te lo llenamos con", 330, 66, 4.24, 6.5, "up", "i"),
          T("cualquier bebida", 400, 104, 5.3, 6.5, "up", "g", "oro"),
          I("termo.png", CX, 960, 640, 4.15, 6.5, "fade", "float"),
          I("cafe_frio.png", 170, 760, 330, 5.3, 6.5, "pop"),
          I("matcha_frio.png", 810, 760, 330, 5.45, 6.5, "pop"),
          I("frappe_frio.png", 170, 1130, 330, 5.6, 6.5, "pop"),
          I("cafe_caliente.png", 810, 1130, 310, 5.75, 6.5, "pop")]
    # C2 6.5–8.3 −$10
    s += [T("y te cobramos", 340, 70, 6.54, 8.3, "up", "i"),
          I("termo.png", 300, 920, 720, 6.5, 8.3, "left", "float"),
          sello("−$10", 700, 790, 400, 7.34, 8.3, "stamp", 150, rot=-6),
          T("menos", 1040, 40, 7.84, 8.3, "fade", "c", CREMA, w=420, cx=700)]
    # D 8.3–10.25 fría o caliente
    s += [T("¿Fría o caliente?", 330, 104, 8.52, 10.25, "up", "g"),
          B(f'<div style="width:100%;height:100%;border-radius:36px;background:linear-gradient(180deg,rgba(150,200,230,.22),rgba(150,200,230,.04));border:2px solid rgba(190,225,245,.5)"></div>',
            270, 900, 390, 760, 8.5, 10.25, "left"),
          B(f'<div style="width:100%;height:100%;border-radius:36px;background:linear-gradient(180deg,rgba(230,140,60,.28),rgba(230,140,60,.05));border:2px solid rgba(244,190,120,.55)"></div>',
            710, 900, 390, 760, 8.8, 10.25, "right"),
          I("cafe_frio.png", 270, 880, 560, 8.55, 10.25, "pop"),
          I("cafe_caliente.png", 710, 880, 520, 8.85, 10.25, "pop"),
          T("fría", 1180, 34, 8.6, 10.25, "fade", "c", "#CFE8F6", w=380, cx=270),
          T("caliente", 1180, 34, 8.9, 10.25, "fade", "c", "#F6CFA0", w=380, cx=710),
          pastilla("las dos", CX, 560, 340, 100, 9.66, 10.25, size=40, rot=-3)]
    # E 10.25–14.65 tamaños
    s += [T("¿16, 22 o 32 onzas?", 360, 76, 10.42, 12.9, "up", "i"),
          T("Del tamaño<br><span class='oro'>de tu termo</span>", 330, 100, 12.96, 14.65, "up", "g"),
          I("termo.png", 760, 920, 600, 11.84, 14.65, "pop", ""),
          I("termo.png", 450, 980, 480, 11.16, 14.65, "pop", ""),
          I("termo.png", 170, 1040, 360, 10.52, 14.65, "pop", ""),
          T("16 oz", 1240, 40, 10.6, 14.65, "up", "c", ORO_B, w=260, cx=170),
          T("22 oz", 1240, 40, 11.24, 14.65, "up", "c", ORO_B, w=260, cx=450),
          T("32 oz", 1240, 40, 11.92, 14.65, "up", "c", ORO_B, w=260, cx=760)]
    # F 14.65–19.15 gigante
    s += [T("¿Y si tu termo es", 330, 70, 14.78, 19.15, "up", "i"),
          T("gigante?", 400, 150, 15.42, 19.15, "stamp", "g", "oro"),
          I("termo.png", 420, 960, 560, 14.8, 19.15, "pop", "", extra='data-sc="16.1,16.9,1.3"'),
          sello('<span class="num">0</span><span style="font-size:.45em"> oz</span>', 760, 720, 320, 16.14, 19.15, "pop", 120,
                extra='data-count="0,40" data-cd=".7"', sub="hasta"),
          pastilla("+$10 sobre la Jumbo", CX, 1250, 640, 100, 17.38, 19.15, size=34, rot=-2)]
    # G 19.15–21.25 guardar
    s += [B(ICONOS["guardar"], CX, 700, 300, 300, 19.26, 21.25, "pop", "pulse"),
          T("Guárdalo", 920, 130, 19.3, 21.25, "up", "g", "oro"),
          T("para tu próxima visita", 1080, 62, 19.6, 21.25, "up", "i")]
    # H 21.25–23.0 menos vasos, más Navidad
    s += [copo(CX, 820, 320, 21.25, 23.0, .07),
          tachar("Menos vasos", 560, 120, 21.36, 23.0, 21.95),
          T("más Navidad", 760, 120, 22.16, 23.0, "stamp", "g", "oro", rot=-3)]
    dur = 27.6
    s.append(final(23.0, dur))
    return pagina("termo", PINO, "".join(s), dur, 23.0), dur, [0, 1.95, 4.1, 6.5, 8.3, 10.25, 14.65, 19.15, 21.25, 23.0]


# ---------------------------------------------------------------- video 3: Puntos dobles
def dobles():
    s = []
    dias = [("L", .24), ("M", .40), ("M", .52), ("J", .64), ("V", None), ("S", None), ("D", None)]
    x0, paso = 86 + 50, 118
    s.append(T("De lunes a jueves", 340, 80, .1, 2.95, "up", "i"))
    for k, (d, t) in enumerate(dias):
        cx = x0 + k * paso
        if t is None:
            inner = f'<div class="dia" style="width:100px;height:100px;border:2px solid rgba(243,234,216,.3);color:rgba(243,234,216,.35);font-size:52px">{d}</div>'
            s.append(B(inner, cx, 560, 100, 100, .1, 2.95, "fade"))
        else:
            inner = f'<div class="dia sello" style="width:100px;height:100px;color:{VINO};font-size:52px;box-shadow:0 10px 24px rgba(0,0,0,.4)">{d}</div>'
            s.append(B(inner, cx, 560, 100, 100, t, 2.95, "pop"))
    s += [T("×2", 680, 330, 2.26, 2.95, "stamp", "g", "oro", rot=-4),
          T("tus puntos valen doble", 1080, 34, 2.4, 2.95, "fade", "c", CREMA)]
    # B 2.95–4.2
    s += [T("¿Cómo<br>funciona?", 560, 150, 3.06, 4.2, "stamp", "g", "oro")]
    # C 4.2–7.25 normal
    s += [T("normalmente", 360, 36, 4.34, 7.25, "fade", "c", CREMA),
          B(f'<div style="width:100%;height:100%;border:4px solid {ORO_B};border-radius:22px;display:flex;align-items:center;justify-content:center;'
            f'font-family:Gloock;font-size:120px;color:{CREMA};background:rgba(0,0,0,.18)">$100</div>', 250, 760, 360, 220, 5.36, 7.25, "pop"),
          T("=", 690, 110, 5.9, 7.25, "pop", "s", ORO_B, w=120, cx=480),
          contar("", 0, 20, "", 640, 190, 6.28, 7.25, .5, "oro", w=360, cx=730),
          T("puntos", 850, 34, 6.4, 7.25, "fade", "c", CREMA, w=360, cx=730),
          T("1 punto por cada $5", 1020, 60, 6.6, 7.25, "up", "i")]
    # D 7.25–9.2 cuarenta
    s += [T("lunes a jueves", 360, 38, 7.38, 9.2, "fade", "c", ORO_B),
          tachar("20", 470, 230, 7.3, 9.2, 8.25, CREMA),
          T("40", 760, 380, 8.62, 9.2, "stamp", "g", "oro", rot=-3),
          T("puntos por cada $100", 1200, 34, 8.75, 9.2, "fade", "c", CREMA)]
    # E 9.2–13.95 haz cuentas
    s += [T("Haz cuentas", 330, 120, 9.34, 13.95, "up", "g"),
          I("cafe_frio.png", 290, 900, 720, 11.6, 13.95, "left"),
          contar("", 0, 150, "", 560, 200, 10.3, 13.95, .7, "oro", w=440, cx=710),
          T("puntos", 790, 34, 10.5, 13.95, "fade", "c", CREMA, w=440, cx=710),
          T("bebida de 16 oz", 870, 54, 11.7, 13.95, "up", "i", CREMA, w=440, cx=710),
          pastilla("gratis", 710, 1060, 340, 110, 13.34, 13.95, size=44, rot=-6)]
    # F 13.95–16.95 antes
    s += [T("Antes tenías que gastar", 380, 70, 14.36, 16.95, "up", "i"),
          contar("$", 0, 750, "", 600, 280, 15.36, 16.95, .8, CREMA)]
    # G 16.95–20.0 ahora
    s += [tachar("$750", 360, 140, 16.95, 20.0, 17.2, "rgba(243,234,216,.55)"),
          T("ahora", 590, 40, 17.14, 20.0, "fade", "c", ORO_B),
          contar("$", 750, 375, "", 660, 290, 17.82, 20.0, 1.0, "oro", a="up"),
          T("y ya la tienes", 1010, 70, 19.18, 20.0, "up", "i"),
          pastilla("la mitad", 760, 600, 270, 84, 18.9, 20.0, size=30, rot=6)]
    # H 20.0–23.8 tarjeta
    pts = "".join(f'<div class="ptc" style="width:58px;height:58px;border-radius:50%;border:3px solid {ORO_B};opacity:.6"></div>' for _ in range(10))
    tarjeta = (f'<div style="width:100%;height:100%;border-radius:34px;background:linear-gradient(135deg,#3a0910,{VINO2} 60%,#2a060b);'
               f'border:3px solid {ORO_B};box-shadow:0 40px 70px rgba(0,0,0,.6);position:relative">'
               f'<div class="cap" style="position:absolute;left:44px;top:40px;font-size:30px;color:{ORO_B}">Caffany</div>'
               f'<div style="position:absolute;left:44px;top:84px;font-family:Gloock;font-size:76px;color:{CREMA}">Puntos</div>'
               f'<div style="position:absolute;left:44px;right:44px;bottom:48px;display:grid;grid-template-columns:repeat(5,58px);justify-content:space-between;row-gap:22px">{pts}</div></div>')
    s += [T("¿Todavía no<br>juntas puntos?", 330, 100, 20.08, 23.8, "up", "g"),
          B(tarjeta, CX, 830, 700, 420, 20.5, 23.8, "pop", "float")]
    for k in range(10):
        cxk = CX - 350 + 44 + 29 + (k % 5) * ((700 - 88 - 58) / 4)
        cyk = 830 - 210 + (420 - 48 - 58 - 80 - 58) + (k // 5) * 80 + 29
        s.append(B(f'<div class="sello" style="width:58px;height:58px"></div>', cxk, cyk, 58, 58, 21.6 + k * .17, 23.8, "pop", d=.3))
    s += [T("pide en caja que te registren", 1110, 32, 21.54, 23.8, "fade", "c", ORO_B)]
    # I 23.8–25.9 mándaselo
    s += [B(ICONOS["enviar"], CX, 690, 300, 300, 23.96, 25.9, "pop", "float", rot=-8),
          T("Mándaselo", 900, 130, 24.0, 25.9, "up", "g", "oro"),
          T("a tu compa del café de la tarde", 1060, 60, 24.4, 25.9, "up", "i")]
    dur = 30.8
    s.append(final(25.9, dur))
    return pagina("dobles", VINO, "".join(s), dur, 25.9), dur, [0, 2.95, 4.2, 7.25, 9.2, 13.95, 16.95, 20.0, 23.8, 25.9]


# ---------------------------------------------------------------- video 4: Recompensas
def recompensas():
    s = []
    s += [I("cafe_caliente.png", CX, 900, 760, 0, 2.25, "zoomin", "drift"),
          T("¿Sabías que tu café te puede salir", 330, 62, 0, 2.25, "up", "i", w=820),
          pastilla("gratis", CX, 1180, 420, 140, 1.6, 2.25, size=64, rot=-5)]
    # B 2.25–6.85
    s += [T("en Caffany", 340, 38, 2.46, 6.85, "fade", "c", ORO_B),
          T("$5", 470, 200, 3.46, 6.85, "pop", "g", CREMA, w=320, cx=230),
          T("=", 530, 110, 3.9, 6.85, "pop", "s", ORO_B, w=120, cx=385),
          T("1 punto", 500, 130, 4.26, 6.85, "pop", "g", "oro", w=520, cx=690),
          T("y los premios están", 840, 74, 4.96, 6.85, "up", "i"),
          T("mejores que nunca", 940, 88, 5.92, 6.85, "stamp", "g", "oro", rot=-2)]
    # escalera
    niveles = [(60, 6.85, 8.95, 7.08), (100, 8.95, 11.45, 9.24), (150, 11.45, 14.35, 11.76), (200, 14.35, 16.05, 14.6),
               (300, 16.05, 19.2, 16.34), (450, 19.2, 24.25, 19.6)]
    xs = [140 + k * (840 - 140) / 5 for k in range(6)]
    linea = f'<div style="width:100%;height:4px;background:rgba(244,221,160,.3);margin-top:28px"></div>'
    s.append(B(linea, CX, 345, 700, 60, 6.85, 24.25, "fade"))
    for k, x in enumerate(xs):
        s.append(B(f'<div class="dia" style="width:44px;height:44px;border:3px solid rgba(244,221,160,.45);background:{PINO}"></div>', x, 345, 44, 44, 6.85, 24.25, "fade"))
        s.append(B(f'<div class="dia sello" style="width:44px;height:44px"></div>', x, 345, 44, 44, niveles[k][3], 24.25, "pop", d=.35))
    prev = 0
    for k, (v, t0, t1, tn) in enumerate(niveles):
        cd = 1.2 if v == 450 else .5
        s.append(contar("", prev, v, "", 390, 220, t0, t1, cd, "oro", a="up"))
        s.append(T("puntos", 620, 34, t0 + .1, t1, "fade", "c", CREMA))
        prev = v
    s += [I("galleta.png", CX, 900, 400, 7.98, 8.95, "pop"),
          T("Galleta de avena", 1140, 80, 8.08, 8.95, "up", "g"),
          B(f'<div class="pastilla" style="width:100%;height:100%;border-radius:26px;flex-direction:column">'
            f'<div style="font-family:Gloock;font-size:170px;color:{VINO};line-height:1">$50</div>'
            f'<div class="cap" style="font-size:26px;color:{VINO}">de descuento</div></div>', CX, 900, 520, 300, 9.72, 11.45, "stamp", rot=-4),
          T("en tu cuenta", 1140, 80, 10.2, 11.45, "up", "g"),
          I("matcha_frio.png", CX, 900, 420, 12.7, 14.35, "pop"),
          T("Bebida de 16 oz", 1140, 80, 12.8, 14.35, "up", "g"),
          I("frappe_frio.png", CX, 890, 460, 15.36, 16.05, "pop"),
          T("Bebida Jumbo", 1140, 80, 15.4, 16.05, "up", "g"),
          foto_circulo("odoo_197.png", 330, 900, 330, 17.42, 19.2),
          foto_circulo("odoo_200.png", 650, 900, 330, 18.36, 19.2),
          T("Poke de pollo o ensalada", 1140, 72, 17.5, 19.2, "up", "g"),
          I("gorro.png", CX, 900, 380, 19.5, 21.0, "pop", "float", rot=-8),
          copo(CX, 900, 280, 19.3, 21.0, .1),
          T("Tu comida<br>completa", 720, 112, 21.04, 24.25, "up", "g"),
          pastilla("gratis", CX, 1040, 460, 140, 22.22, 24.25, size=66, rot=-5),
          T("hasta $300", 1170, 70, 23.0, 24.25, "up", "i")]
    # I 24.25–26.85 resumen
    s.append(T("¿Cuántos llevas <span class='oro'>tú?</span>", 335, 84, 24.34, 26.85, "up", "g"))
    filas = [("60", "Galleta de avena"), ("100", "$50 de descuento"), ("150", "Bebida 16 oz"), ("200", "Bebida Jumbo"),
             ("300", "Poke o ensalada"), ("450", "Comida completa")]
    for k, (n, txt) in enumerate(filas):
        y = 500 + k * 112
        s.append(T(n, y, 76, 24.45 + k * .12, 26.85, "left", "g", "oro", w=200, cx=110, align="left"))
        s.append(T(txt, y + 10, 62, 24.5 + k * .12, 26.85, "left", "i", CREMA, w=560, cx=330, align="left"))
    s.append(T("pregúntalo en caja", 1220, 32, 25.8, 26.85, "fade", "c", ORO_B))
    dur = 30.6
    s.append(final(26.85, dur))
    return pagina("recompensas", PINO, "".join(s), dur, 26.85), dur, [0, 2.25, 6.85, 8.95, 11.45, 14.35, 16.05, 19.2, 24.25, 26.85]


VIDEOS = {"malvavisco": malvavisco, "termo": termo, "dobles": dobles, "recompensas": recompensas}

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "html"), exist_ok=True)
    meta = {}
    for n, f in VIDEOS.items():
        html, dur, cortes = f()
        open(os.path.join(BASE, "html", n + ".html"), "w").write(html)
        meta[n] = {"dur": dur, "cortes": cortes}
    json.dump(meta, open(os.path.join(BASE, "html", "meta.json"), "w"), indent=1)
    print(json.dumps(meta))
