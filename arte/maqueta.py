"""Generala maldita: 3 cuadros de maqueta para decidir la estética (pulpería de madrugada + estampitas).

Lienzo 320x180, paleta cerrada, luz en escalones tramados, agrandado entero x4.
Letra 5x7 en letra.py; la luz en escalones tramados con Bayer está acá abajo.

    python arte/maqueta.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import letra

AQUI = Path(__file__).resolve().parent
BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def bayer(h, w):
    return BAYER4[np.arange(h)[:, None] % 4, np.arange(w)[None, :] % 4]


def agrandar(im, k):
    return np.repeat(np.repeat(im, k, axis=0), k, axis=1)


def halo(im, cx, cy, radio, color, fuerza, pasos=6, aplaste=1.0):
    """Luz falsa sumada en escalones tramados (nunca degradé suave)."""
    h, w = im.shape[:2]
    x0, x1 = int(max(cx - radio - 1, 0)), int(min(cx + radio + 2, w))
    y0, y1 = int(max(cy - radio / aplaste - 1, 0)), int(min(cy + radio / aplaste + 2, h))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((xx - cx) ** 2 + ((yy - cy) * aplaste) ** 2)
    k = np.floor(np.clip(1 - d / radio, 0, 1) * pasos + BAYER4[yy % 4, xx % 4]) / pasos
    z = im[y0:y1, x0:x1].astype(float) + (np.asarray(color, float) * fuerza)[None, None, :] * k[..., None]
    im[y0:y1, x0:x1] = np.clip(z, 0, 255).astype(np.uint8)


W, H = 320, 180


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


P = {k: hx(v) for k, v in {
    "tinta": "0d0a0c",
    "m0": "1c1210", "m1": "2e1c14", "m2": "472b1a", "m3": "6b4424", "m4": "8f6233", "m5": "b88748",   # madera
    "a0": "e8a33a", "a1": "ffd27a", "a2": "fff1c4",                                                    # luz del farol
    "v0": "0f2a22", "v1": "1c4a38", "v2": "2f7a55",                                                    # verde botella
    "h0": "6b5a47", "h1": "a08c6a", "h2": "d4c39c", "h3": "f2e8cf",                                    # hueso
    "r0": "2a0c10", "r1": "5a1218", "r2": "9c1f22", "r3": "d93a2e",                                    # rojo
    "o0": "8a6420", "o1": "c9962b", "o2": "f4cf5a",                                                    # dorado
    "c0": "1d4257", "c1": "2e6f8a", "c2": "6fb7c9",                                                    # celeste
}.items()}
PALETA = np.array(list(P.values()), dtype=float)
MAD = [P[f"m{i}"] for i in range(6)]


class Lienzo:
    def __init__(self):
        self.im = Image.new("RGB", (W, H), P["tinta"])
        self.d = ImageDraw.Draw(self.im)

    def rect(self, x, y, w, h, c):
        if w > 0 and h > 0:
            self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

    def rrect(self, x, y, w, h, c, r=1):
        """Rectángulo con esquinas comidas (r = 1 o 2)."""
        self.rect(x + r, y, w - 2 * r, h, c)
        self.rect(x, y + r, w, h - 2 * r, c)
        if r == 2:
            for px_, py_ in ((x + 1, y + 1), (x + w - 2, y + 1), (x + 1, y + h - 2), (x + w - 2, y + h - 2)):
                self.d.point((px_, py_), fill=c)

    def px(self, x, y, c):
        self.d.point((x, y), fill=c)

    def poli(self, pts, c):
        self.d.polygon(pts, fill=c)

    def elipse(self, x0, y0, x1, y1, c):
        self.d.ellipse([x0, y0, x1, y1], fill=c)

    def texto(self, x, y, s, c, escala=1, sombra=None, borde=None):
        s = s.upper()
        if borde is not None:
            for dx in range(-1, escala + 1):
                for dy in range(-1, escala + 1):
                    if dx or dy:
                        self._texto(x + dx, y + dy, s, borde, escala)
        if sombra is not None:
            self._texto(x, y + escala, s, sombra, escala)
        self._texto(x, y, s, c, escala)

    def _texto(self, x, y, s, c, e):
        cx = x
        for ch in s:
            base = letra.ACC.get(ch, ch)
            for j, fila in enumerate(letra.G.get(base, letra.G["?"]).split()):
                for i, b in enumerate(fila):
                    if b == "1":
                        self.rect(cx + i * e, y + j * e, e, e, c)
            if ch in letra.ACC:
                marcas = ((1, -2), (2, -3), (3, -2), (4, -3)) if ch == "Ñ" else ((2, -2), (3, -3))
                for i, j in marcas:
                    self.rect(cx + i * e, y + j * e, e, e, c)
            cx += 6 * e

    def sprite(self, x, y, filas, colores):
        for j, fila in enumerate(filas):
            for i, ch in enumerate(fila):
                if ch != ".":
                    self.px(x + i, y + j, colores[ch])

    def arr(self):
        return np.array(self.im)

    def desde(self, a):
        self.im = Image.fromarray(a.astype(np.uint8), "RGB")
        self.d = ImageDraw.Draw(self.im)


def ancho(s, escala=1):
    return (len(s) * 6 - 1) * escala


# ---------------- mesa ----------------
def madera(L, x0, y0, x1, y1, rng, alto=19):
    y = y0
    k = 0
    while y < y1:
        h = min(alto + int(rng.integers(-2, 3)), y1 - y)
        L.rect(x0, y, x1 - x0, h, MAD[2])
        for _ in range(int((x1 - x0) * h / 55)):                      # veta
            lx = int(rng.integers(x0, x1)); ly = y + int(rng.integers(1, max(h - 1, 2)))
            lar = int(rng.integers(6, 42)); tono = MAD[1] if rng.random() < 0.6 else MAD[3]
            L.rect(lx, ly, min(lar, x1 - lx), 1, tono)
        if rng.random() < 0.7:                                        # nudo
            nx = int(rng.integers(x0 + 10, x1 - 10)); ny = y + h // 2
            L.elipse(nx - 4, ny - 2, nx + 4, ny + 2, MAD[1]); L.elipse(nx - 2, ny - 1, nx + 2, ny + 1, MAD[3])
            L.px(nx, ny, MAD[1])
        jx = int(rng.integers(x0 + 30, x1 - 30))                      # junta de tablas y clavos
        L.rect(jx, y, 1, h, MAD[0]); L.rect(jx + 1, y + 1, 1, h - 2, MAD[3])
        for cx in (jx - 3, jx + 4):
            L.px(cx, y + 3, MAD[0]); L.px(cx, y + h - 4, MAD[0])
        L.rect(x0, y, x1 - x0, 1, MAD[3])                             # canto iluminado y ranura
        L.rect(x0, y + h - 1, x1 - x0, 1, MAD[0])
        y += h; k += 1


def iluminar(L, cx, cy, rx, ry, y_desde, tinte, pasos=(0.2, 0.34, 0.5, 0.7, 0.88, 1.0), calido=0.0):
    """Luz del farol en escalones tramados: multiplica, tiñe la sombra y deja el centro a pleno."""
    a = L.arr().astype(float)
    yy, xx = np.mgrid[0:H, 0:W]
    dist = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    luz = np.clip(1 - dist, 0, 1) ** 0.75
    n = len(pasos) - 1
    k = np.clip(np.floor(luz * n + bayer(H, W)), 0, n).astype(int)
    m = np.asarray(pasos)[k][..., None]
    out = a * m + np.asarray(tinte, float) * (1 - m) * 0.3 + np.asarray(P["a0"], float) * calido * (m > 0.95)
    zona = (yy >= y_desde)[..., None]
    L.desde(np.where(zona, np.clip(out, 0, 255), a))


def a_paleta(L):
    a = L.arr().astype(float)
    peso = np.array([0.6, 1.0, 0.5])
    d = (((a[:, :, None, :] - PALETA[None, None]) * peso) ** 2).sum(-1)
    L.desde(PALETA[d.argmin(-1)])


def farol(L, x, y):
    """Farol de kerosén de 18x34 visto de tres cuartos."""
    L.rrect(x + 5, y, 8, 3, P["tinta"]); L.rect(x + 6, y + 1, 6, 1, P["v2"])                 # aro del asa
    L.rect(x + 8, y - 4, 2, 4, P["tinta"])
    L.rrect(x + 3, y + 3, 12, 6, P["tinta"]); L.rect(x + 4, y + 4, 10, 4, P["v1"])            # tapa
    L.rect(x + 4, y + 4, 10, 1, P["v2"]); L.rect(x + 5, y + 6, 1, 1, P["a1"]); L.rect(x + 9, y + 6, 1, 1, P["a1"])
    L.rrect(x + 2, y + 9, 14, 16, P["tinta"], 2)                                               # tubo de vidrio
    L.rrect(x + 3, y + 10, 12, 14, P["a0"], 2); L.rrect(x + 4, y + 11, 10, 12, P["a1"], 2)
    L.rrect(x + 6, y + 13, 6, 9, P["a2"], 2)
    L.rect(x + 8, y + 15, 2, 6, (255, 255, 255)); L.rect(x + 8, y + 21, 2, 2, P["r3"])        # llama y mecha
    L.rect(x + 2, y + 10, 1, 14, P["tinta"]); L.rect(x + 15, y + 10, 1, 14, P["tinta"])       # varillas
    L.rrect(x, y + 25, 18, 9, P["tinta"], 2); L.rrect(x + 1, y + 26, 16, 7, P["v1"], 2)       # tanque
    L.rect(x + 3, y + 26, 12, 1, P["v2"]); L.rect(x + 3, y + 28, 4, 1, P["a1"]); L.rect(x + 2, y + 31, 14, 1, P["v0"])


PIPS = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}
TIPOS = {  # cara, luz, canto, canto oscuro, punto, brillo bajo el punto
    "hueso": ("h3", "a2", "h2", "h1", "m1", "a2"),
    "maldito": ("r2", "r3", "r1", "r0", "h3", "r1"),
    "dorado": ("o2", "a2", "o1", "o0", "m1", "a2"),
}


def sombra_dado(L, x, y, alto=0):
    L.rrect(x + 2 + alto, y + 28 + alto, 28, 8, P["m0"], 2)
    L.rrect(x + 4 + alto, y + 30 + alto, 26, 7, P["tinta"], 2)


def dado(L, x, y, valor, tipo="hueso", guardado=False, anulado=False, canto=True):
    """Dado de 28x33 (cara de 26 + canto de 5). guardado: contorno dorado. anulado: apagado y tachado."""
    cara, luz, c1, c2, punto, brillo = (P[k] for k in TIPOS[tipo])
    if anulado:
        cara, luz, c1, c2, punto, brillo = P["h1"], P["h1"], P["h0"], P["m1"], P["m2"], P["h1"]
    borde = P["o2"] if guardado else P["tinta"]
    alto = 33 if canto else 28
    L.rrect(x, y, 28, alto, borde, 2)
    if guardado:
        L.rrect(x - 1, y - 1, 30, alto + 2, P["o1"], 3); L.rrect(x, y, 28, alto, borde, 2)
    if canto:
        L.rrect(x + 1, y + 20, 26, 12, c1, 2); L.rect(x + 2, y + 30, 24, 1, c2); L.rect(x + 3, y + 31, 22, 1, c2)
    L.rrect(x + 1, y + 1, 26, 26, cara, 2)
    L.rect(x + 3, y + 1, 22, 1, luz); L.rect(x + 1, y + 3, 1, 22, luz)                         # filo de luz
    L.rect(x + 3, y + 26, 22, 1, c1)
    if tipo == "hueso" and not anulado:                                                        # marcas del hueso
        L.rect(x + 19, y + 4, 4, 1, P["h2"]); L.rect(x + 5, y + 22, 3, 1, P["h2"]); L.px(x + 22, y + 15, P["h2"])
    for i, j in PIPS[valor]:
        px0, py0 = x + 5 + i * 7, y + 5 + j * 7
        L.rect(px0 + 1, py0 + 4, 3, 1, brillo); L.rect(px0 + 4, py0 + 1, 1, 3, brillo)        # canto tallado
        L.rrect(px0, py0, 4, 4, punto, 1)
    if anulado:
        for k in range(22):
            L.rect(x + 3 + k, y + 3 + k, 2, 1, P["r3"])


# ---------------- estampitas ----------------
COL = {"k": P["tinta"], "h": P["h3"], "H": P["h1"], "r": P["r3"], "R": P["r1"], "g": P["o1"], "G": P["o2"],
       "c": P["c2"], "C": P["c1"], "s": P["m5"], "w": P["a2"], "v": P["v2"]}
ESTAMPITAS = {
    "muerte": ("tinta", [
        "............", "....hhhh....", "...hhhhhh...", "..hhhhhhhh..", "..hkkhhkkh..", "..hkkhhkkh..",
        "..hhhkkhhh..", "...hhhhhh...", "...hkhkhk...", "....hhhh....", "............", "..H......H..",
        "...HH..HH...", ".....HH.....", "...HH..HH...", "..H......H.."]),
    "corazon": ("c0", [
        ".....G......", "....GgG.....", "...g.G.g....", ".....g......", "..rr...rr...", ".rrrr.rrrr..",
        "rrwrrrrrrrr.", "rrwrrrrrrrr.", "rrrrrrrrrrr.", ".rrrrrrrrr..", "..rrRrrrr...", "...rrRrr....",
        "....rrr.....", ".....r......", "............", "............"]),
    "gauchito": ("r1", [
        ".....GG.....", ".....GG.....", "..GGGGGGGG..", ".....GG.....", "....kkkk....", "...kkkkkk...",
        "....ssss....", "....ssss....", "...rrrrrr...", "..ccrrrrcc..", "..cccrrccc..", "..cccccccc..",
        "..cc.cc.cc..", "..ss.cc.ss..", "....cccc....", "....kkkk...."]),
    "virgen": ("v0", [
        "....GGGG....", "...G....G...", "...G.ss.G...", "....cssc....", "...cccccc...", "...ccwwcc...",
        "..cccwwccc..", "..cccwwccc..", "..ccwwwwcc..", ".cccwwwwccc.", ".cccwwwwccc.", ".ccwwwwwwcc.",
        "cccwwwwwwccc", "cccccccccccc", "............", "............"]),
    "sol": ("c1", [
        ".....g......", ".g...g...g..", "..g.....g...", "....GGGG....", "...GGGGGG...", "..GGkGGkGG..",
        "ggGGGGGGGGgg", "..GGGGGGGG..", "..GGkGGkGG..", "...GGkkGG...", "....GGGG....", "..g.....g...",
        ".g...g...g..", ".....g......", "............", "............"]),
    "taba": ("r0", [
        "............", "............", "..hh....hh..", ".hhhh..hhhh.", ".hhhhhhhhhh.", "..hhhhhhhh..",
        "...hHHHHh...", "...hHHHHh...", "..hhhhhhhh..", ".hhhhhhhhhh.", ".hhhh..hhhh.", "..hh....hh..",
        "............", "............", "............", "............"]),
}


def estampita(L, x, y, cual, elegida=False):
    """Estampita de 20x28 con marco dorado."""
    fondo, filas = ESTAMPITAS[cual]
    if elegida:
        L.rrect(x - 2, y - 2, 24, 32, P["a2"], 2)
    L.rrect(x, y, 20, 28, P["tinta"], 1)
    L.rect(x + 1, y + 1, 18, 26, P["o1"])
    L.rect(x + 1, y + 1, 18, 1, P["o2"]); L.rect(x + 1, y + 1, 1, 26, P["o2"])                 # marco con luz arriba
    L.rect(x + 2, y + 26, 17, 1, P["o0"]); L.rect(x + 18, y + 2, 1, 25, P["o0"])
    L.rect(x + 3, y + 3, 14, 22, P[fondo])
    L.sprite(x + 4, y + 4, filas, COL)
    L.rect(x + 3, y + 21, 14, 4, P["o1"]); L.rect(x + 3, y + 21, 14, 1, P["o2"])               # cinta de abajo
    for i in (5, 9, 13):
        L.rect(x + i, y + 23, 2, 1, P["r2"])
    for px_, py_ in ((x + 1, y + 1), (x + 18, y + 1), (x + 1, y + 26), (x + 18, y + 26)):       # remaches
        L.px(px_, py_, P["a2"])


def hueco(L, x, y):
    for i in range(0, 20, 3):
        L.rect(x + i, y, 2, 1, P["m3"]); L.rect(x + i, y + 27, 2, 1, P["m3"])
    for j in range(0, 28, 3):
        L.rect(x, y + j, 1, 2, P["m3"]); L.rect(x + 19, y + j, 1, 2, P["m3"])


# ---------------- piezas de pantalla ----------------
def boton(L, x, y, w, h, s, base, luz, sombra, tinta="tinta"):
    L.rrect(x, y, w, h, P["tinta"], 2)
    L.rrect(x + 1, y + 1, w - 2, h - 2, P[sombra], 2)
    L.rrect(x + 1, y + 1, w - 2, h - 4, P[base], 2)
    L.rect(x + 3, y + 1, w - 6, 1, P[luz])
    L.texto(x + (w - ancho(s)) // 2 + 1, y + (h - 3 - 7) // 2 + 1, s, P[tinta])


def moneda(L, x, y):
    L.rrect(x, y, 7, 7, P["tinta"], 2); L.rrect(x + 1, y + 1, 5, 5, P["o1"], 1)
    L.rect(x + 2, y + 1, 2, 1, P["a2"]); L.rect(x + 3, y + 2, 1, 3, P["o0"])


def baranda(L, amuletos):
    """Borde de la mesa de este lado: amuletos, puntaje y botones."""
    L.rect(0, 139, W, 41, P["tinta"])
    L.rect(0, 140, W, 40, P["m1"]); L.rect(0, 140, W, 1, P["m4"]); L.rect(0, 141, W, 1, P["m2"])
    for x in range(0, W, 4):
        L.px(x + (x // 4) % 2, 143 + (x * 7) % 31, P["m0"])
    for i in range(5):
        x = 6 + i * 23
        if i < len(amuletos):
            estampita(L, x, 147, amuletos[i])
        else:
            hueco(L, x, 147)


def barra_meta(L, mesa, puntos, meta, plata, jefe=None):
    if jefe:
        L.texto(4, 4, jefe, P["r3"], borde=P["tinta"])
    else:
        L.texto(4, 4, mesa, P["h2"])
    L.rrect(4, 14, 84, 7, P["tinta"], 1); L.rect(5, 15, 82, 5, P["m1"])
    lleno = min(82, int(82 * puntos / meta))
    L.rect(5, 15, lleno, 5, P["a0"]); L.rect(5, 15, lleno, 1, P["a1"])
    if puntos >= meta:
        L.rect(5, 15, 82, 5, P["o2"]); L.rect(5, 15, 82, 1, P["a2"])
    L.texto(4, 24, f"{puntos}/{meta}", P["a1"] if puntos < meta else P["o2"])
    s = str(plata)
    moneda(L, W - 6 - ancho(s) - 10, 4); L.texto(W - 5 - ancho(s), 4, s, P["o2"])


def planilla(L, x, y, filas, sugerida=None):
    """Libreta de jugadas. filas: (nombre, valor, anotado o None)."""
    w, h = 74, len(filas) * 9 + 7
    L.rect(x + 2, y + 2, w, h, P["tinta"])
    L.rect(x, y, w, h, P["h1"]); L.rect(x + 1, y + 1, w - 2, h - 2, P["h2"])
    L.rect(x + 1, y + 1, w - 2, 1, P["h3"])
    for i, (nombre, valor, anotado) in enumerate(filas):
        fy = y + 4 + i * 9
        if nombre == sugerida:
            L.rect(x + 1, fy - 1, w - 2, 9, P["a0"]); L.rect(x + 1, fy - 1, w - 2, 1, P["a1"])
        if i and nombre != sugerida:
            L.rect(x + 3, fy - 1, w - 6, 1, P["h1"])
        tinta = P["h1"] if anotado is not None else P["tinta"]
        L.texto(x + 4, fy, nombre, tinta)
        s = str(valor if anotado is None else anotado)
        L.texto(x + w - 4 - ancho(s), fy, s, P["r2"] if anotado is not None else P["tinta"])


def rival(L, jefe=False):
    """El que juega enfrente, del otro lado de la mesa."""
    if not jefe:
        c, rim = P["m0"], P["m2"]
        L.poli([(108, 34), (124, 21), (196, 21), (212, 34)], c)
        L.elipse(149, 9, 171, 27, c)
        L.elipse(128, 9, 192, 17, c); L.rect(147, 1, 26, 11, c); L.rect(147, 9, 26, 1, P["m1"])
        L.px(155, 19, P["a0"]); L.px(165, 19, P["a0"])
        for hx_ in (124, 178):
            L.rrect(hx_, 31, 18, 9, c, 2); L.rect(hx_ + 2, 39, 14, 1, rim)
        return
    c, rim = P["r1"], P["r2"]
    L.poli([(96, 34), (116, 17), (204, 17), (224, 34)], c)
    L.poli([(116, 17), (204, 17), (200, 19), (120, 19)], rim)
    L.elipse(146, 5, 174, 29, c)
    for s in (1, -1):                                                                          # cuernos
        cx = 160 - s * 12
        L.poli([(cx, 12), (cx - s * 8, 7), (cx - s * 11, -1), (cx - s * 5, 4), (cx + s * 3, 8)], c)
        L.poli([(cx - s * 11, -1), (cx - s * 9, 3), (cx - s * 7, 4)], P["h2"])
    for ex in (152, 163):                                                                      # ojos
        L.rect(ex, 15, 5, 3, P["tinta"]); L.rect(ex + 1, 15, 3, 2, P["o2"]); L.px(ex + 2, 16, P["a2"])
    L.rect(153, 23, 14, 3, P["tinta"])                                                         # sonrisa
    for i in range(0, 14, 2):
        L.px(153 + i, 23, P["h3"]); L.px(154 + i, 25, P["h3"])
    for hx_ in (112, 184):                                                                     # garras sobre la mesa
        L.rrect(hx_, 29, 24, 12, P["tinta"], 2); L.rrect(hx_ + 1, 30, 22, 10, c, 2); L.rect(hx_ + 3, 30, 18, 1, rim)
        for i in range(4):
            L.rect(hx_ + 3 + i * 5, 40, 3, 3, P["tinta"]); L.rect(hx_ + 4 + i * 5, 40, 1, 3, P["h3"])


def chispas(L, rng, x0, y0, x1, y1, n):
    for _ in range(n):
        x, y = int(rng.integers(x0, x1)), int(rng.integers(y0, y1))
        c = (P["o2"], P["a2"], P["a1"])[int(rng.integers(0, 3))]
        if rng.random() < 0.3:
            L.rect(x - 1, y, 3, 1, c); L.rect(x, y - 1, 1, 3, c); L.px(x, y, (255, 255, 255))
        else:
            L.px(x, y, c)


# ---------------- cuadros ----------------
JUGADAS = ["UNOS", "DOSES", "TRESES", "CUATROS", "CINCOS", "SEISES", "ESCALERA", "FULL", "POKER", "GENERALA"]
VALORES = [1, 2, 3, 4, 5, 6, 20, 30, 40, 50]


def mesa(dados, anotadas, sugerida, mesa_txt, puntos, meta, plata, amuletos, cuenta, jefe=None, regla=None, tiros=1,
         festejo=None, semilla=3):
    rng = np.random.default_rng(semilla)
    L = Lienzo()
    madera(L, 0, 34, W, 140, rng)
    xs = [52, 88, 124, 160, 196]
    ys = [66, 70, 64, 69, 66]
    for (v, tipo, guardado, anulado), x, y in zip(dados, xs, ys):
        sombra_dado(L, x, y - (3 if guardado else 0), 2 if guardado else 0)
    L.rrect(12, 86, 22, 6, P["m0"], 2)                                                         # sombra del farol
    tinte = P["r1"] if jefe else (26, 14, 34)
    iluminar(L, 132, 84, 205 if festejo else 180, 100 if festejo else 86, 34, tinte, calido=0.06)
    a = L.arr()
    halo(a, 23, 70, 46, P["a0"], 0.5, pasos=5)
    if jefe:
        halo(a, 160, 30, 90, P["r2"], 0.45, pasos=5, aplaste=1.6)
    L.desde(a)
    a_paleta(L)
    L.rect(0, 0, W, 34, P["tinta"])
    if jefe:
        a = L.arr(); halo(a, 160, 22, 70, P["r1"], 0.9, pasos=4, aplaste=1.8); L.desde(a); a_paleta(L)
    L.rect(0, 33, W, 1, P["m3"] if not jefe else P["r2"])
    rival(L, bool(jefe))
    farol(L, 14, 54)
    for (v, tipo, guardado, anulado), x, y in zip(dados, xs, ys):          # los dados van limpios, sin trama
        dado(L, x, y - (3 if guardado else 0), v, tipo, guardado, anulado)
    if regla:
        w = ancho(regla) + 14
        x = (236 - w) // 2 + 4
        L.rrect(x, 45, w, 13, P["tinta"], 2); L.rrect(x + 1, 46, w - 2, 11, P["r2"], 2); L.rect(x + 3, 46, w - 6, 1, P["r3"])
        L.texto(x + 7, 49, regla, P["a2"], sombra=P["r0"])
    filas = [(n, v, anotadas.get(n)) for n, v in zip(JUGADAS, VALORES)]
    planilla(L, 240, 38, filas, sugerida)
    if festejo:
        chispas(L, rng, 44, 46, 232, 134, 46)
        L.texto((236 - ancho(festejo, 2)) // 2 + 4, 112, festejo, P["o2"], escala=2, sombra=P["o0"], borde=P["tinta"])
    else:
        for (v, tipo, guardado, anulado), x, y in zip(dados, xs, ys):
            if guardado:
                L.texto(x + 14 - ancho("FIJO") // 2, y + 36, "FIJO", P["o2"], borde=P["tinta"])
    baranda(L, amuletos)
    barra_meta(L, mesa_txt, puntos, meta, plata, jefe)
    nombre, base, mult = cuenta
    L.texto(128, 146, nombre, P["a1"])
    s = f"{base}×{mult}"
    L.texto(128, 157, s, P["a2"], escala=2, sombra=P["m0"])
    L.rect(128, 174, 100, 1, P["m3"])
    if tiros:
        boton(L, 240, 145, 74, 17, "TIRAR   ", "a0", "a1", "o0")
    else:
        boton(L, 240, 145, 74, 17, "TIRAR   ", "m3", "m4", "m2", tinta="m1")
    for i in range(3):
        L.rrect(289 + i * 6, 151, 4, 4, P["tinta"] if i < tiros else (P["o0"] if tiros else P["m2"]), 1)
    boton(L, 240, 163, 74, 15, "ANOTAR", "v2", "c2", "v1", tinta="a2")
    return L


def tienda(semilla=5):
    rng = np.random.default_rng(semilla)
    L = Lienzo()
    L.rect(0, 0, W, 58, P["m0"])
    for x in range(0, W, 26):                                                                  # pared de tablas
        L.rect(x, 0, 1, 58, P["tinta"])
    for ey in (24, 50):                                                                        # estantes con botellas
        x = 6
        while x < W - 8:
            bw = int(rng.integers(5, 9)); bh = int(rng.integers(10, 18))
            if not (130 < x < 186 and ey == 24):
                tono = [("v1", "v2"), ("v0", "v1"), ("m3", "a0"), ("r1", "r2"), ("c0", "c1")][int(rng.integers(0, 5))]
                L.rrect(x, ey - bh, bw, bh, P[tono[0]], 1)
                L.rect(x + bw // 2 - 1, ey - bh - 4, 2, 4, P[tono[0]]); L.rect(x + bw // 2 - 1, ey - bh - 5, 2, 1, P["h1"])
                L.rect(x + 1, ey - bh + 2, 1, bh - 4, P[tono[1]])
                if bw > 6:
                    L.rect(x + 2, ey - bh // 2 - 2, bw - 3, 4, P["h2"])
            x += bw + int(rng.integers(2, 7))
        L.rect(0, ey, W, 3, P["m3"]); L.rect(0, ey, W, 1, P["m4"]); L.rect(0, ey + 3, W, 1, P["tinta"])
    madera(L, 0, 58, W, 140, rng)
    L.rect(0, 58, W, 2, P["m4"])
    for mx, mw, titulo in ((10, 148, "ESTAMPITAS"), (168, 142, "DADOS Y CARAS")):              # paños
        L.rrect(mx, 62, mw, 56, P["tinta"], 2); L.rrect(mx + 1, 63, mw - 2, 54, P["v1"], 2)
        for i in range(mx + 4, mx + mw - 4, 3):
            L.px(i, 65, P["v2"]); L.px(i, 114, P["v2"])
    venta = [("gauchito", 5), ("muerte", 7), ("corazon", 4), ("sol", 6)]
    for i, (cual, precio) in enumerate(venta):
        x = 22 + i * 34
        L.rrect(x + 2, 78, 20, 28, P["v0"], 1)
    caras = [(6, "dorado", 6), (1, "maldito", 5), (3, "hueso", 3)]
    for i, (v, tipo, precio) in enumerate(caras):
        L.rrect(180 + i * 42 + 2, 79, 28, 28, P["v0"], 2)
    iluminar(L, 160, 78, 215, 105, 0, (26, 14, 34), calido=0.05)
    a = L.arr(); halo(a, 160, 22, 60, P["a0"], 0.55, pasos=5); L.desde(a)
    a_paleta(L)
    L.rect(159, 0, 2, 6, P["m4"])                                                              # farol colgado
    farol(L, 151, 6)
    L.rrect(8, 5, 78, 15, P["tinta"], 2); L.rrect(9, 6, 76, 13, P["m3"], 2); L.rect(11, 6, 72, 1, P["m5"])   # cartel
    L.rect(20, 0, 1, 5, P["m4"]); L.rect(73, 0, 1, 5, P["m4"])
    L.texto(47 - ancho("PULPERÍA") // 2, 9, "PULPERÍA", P["a2"], sombra=P["m0"])
    moneda(L, W - 6 - ancho("12") - 10, 6); L.texto(W - 5 - ancho("12"), 6, "12", P["o2"], borde=P["tinta"])
    for i, (cual, precio) in enumerate(venta):
        x = 22 + i * 34
        estampita(L, x, 76, cual, elegida=(i == 1))
        etiqueta(L, x + 10, 107, precio, caro=precio > 12)
    for i, (v, tipo, precio) in enumerate(caras):
        x = 180 + i * 42
        dado(L, x, 76, v, tipo, canto=False)
        etiqueta(L, x + 14, 107, precio)
    L.texto(16, 67, "ESTAMPITAS", P["c2"], sombra=P["v0"]); L.texto(174, 67, "DADOS Y CARAS", P["c2"], sombra=P["v0"])
    # cartel del elegido
    L.rrect(10, 119, 300, 20, P["tinta"], 2); L.rrect(11, 120, 298, 18, P["o1"], 2); L.rrect(12, 121, 296, 16, P["m0"], 1)
    L.texto(17, 122, "SAN LA MUERTE", P["o2"]); L.texto(17 + ancho("SAN LA MUERTE") + 8, 122, "ESTAMPITA RARA", P["r3"])
    L.texto(17, 130, "CADA DADO CON UN 1 SUMA +4 AL MULTIPLICADOR", P["h2"])
    baranda(L, ["taba", "virgen", "corazon"])
    L.texto(128, 146, "TU PLATA", P["a1"])
    moneda(L, 128, 160); moneda(L, 131, 158)
    L.texto(142, 157, "12", P["o2"], escala=2, sombra=P["o0"])
    L.rect(128, 174, 100, 1, P["m3"])
    boton(L, 240, 145, 74, 17, "COMPRAR 7", "a0", "a1", "o0")
    boton(L, 240, 163, 74, 15, "OTRA MESA", "v2", "c2", "v1", tinta="a2")
    return L


def etiqueta(L, cx, y, precio, caro=False):
    s = str(precio)
    w = ancho(s) + 14
    x = cx - w // 2
    L.rrect(x, y - 1, w, 11, P["tinta"], 2); L.rrect(x + 1, y, w - 2, 9, P["h2"], 1); L.rect(x + 2, y, w - 4, 1, P["h3"])
    L.rect(x + 3, y + 3, 4, 4, P["o1"]); L.px(x + 4, y + 4, P["a2"])
    L.texto(x + 10, y + 1, s, P["r2"] if caro else P["tinta"])


def guardar(L, nombre, escala=4):
    a = L.arr()
    Image.fromarray(a).save(AQUI / f"{nombre}_1x.png")
    Image.fromarray(agrandar(a, escala)).save(AQUI / f"{nombre}.png")
    colores = len(np.unique(a.reshape(-1, 3), axis=0))
    print(f"{nombre}.png  {a.shape[1] * escala}x{a.shape[0] * escala}  {colores} colores")


if __name__ == "__main__":
    guardar(mesa(
        dados=[(5, "hueso", True, False), (2, "hueso", False, False), (5, "hueso", True, False),
               (5, "maldito", True, False), (2, "hueso", False, False)],
        anotadas={"UNOS": 3, "TRESES": 9, "ESCALERA": 20}, sugerida="FULL",
        mesa_txt="MESA 3 DE 8", puntos=184, meta=300, plata=12,
        amuletos=["taba", "virgen", "corazon"], cuenta=("FULL", 30, 3), tiros=1), "cuadro_1_mesa")
    guardar(tienda(), "cuadro_2_tienda")
    guardar(mesa(
        dados=[(4, "hueso", True, False), (4, "dorado", True, False), (4, "hueso", True, False),
               (4, "maldito", True, False), (4, "hueso", True, False)],
        anotadas={"UNOS": 3, "DOSES": 8, "TRESES": 9, "CINCOS": 15, "SEISES": 0, "ESCALERA": 20, "FULL": 30},
        sugerida="GENERALA", mesa_txt="", puntos=612, meta=500, plata=19,
        amuletos=["taba", "virgen", "corazon", "muerte", "sol"], cuenta=("GENERALA", 50, 12), tiros=0,
        jefe="EL MANDINGA", regla="LOS SEISES NO VALEN", festejo="¡GENERALA!", semilla=3), "cuadro_3_jefe")
