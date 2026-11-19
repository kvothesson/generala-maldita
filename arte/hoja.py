"""Arte del prototipo: fondos ya iluminados y la hoja de las 30 estampitas.

Sale de las mismas piezas que maqueta.py. Los dados, la letra y la interfaz se dibujan en vivo en index.html.

    python arte/hoja.py
"""
import json

import numpy as np
from PIL import Image

import maqueta as M
from maqueta import P

SALIDA = M.AQUI.parent

COL = dict(M.COL)
COL.update({"V": P["v1"], "m": P["m3"], "M": P["m1"], "a": P["a0"], "A": P["a1"], "z": P["h0"]})

# nombre: (fondo, filas de 12)
NUEVAS = {
    "difunta": ("m2", [".....cc.....", ".....cc.....", "....cccc....", "...cccccc...", "...cwccCc...", "...cwccCc...",
                       "...cwccCc...", "...cwccCc...", "...cccccc...", "...cccccc...", "....CCCC...."]),
    "cayetano": ("c0", [".....G......", "....GgG.....", ".....G......", "....GgG.....", ".....G......", "....GgG.....",
                        ".....G......", "....GgG.....", ".....g......", ".....g......", ".....g......", ".....g......"]),
    "gilda": ("c1", ["............", "....rr.rr...", "...rrrrrrr..", "...rrRrRrr..", "...rrrRrrr..", "....rrrrr...",
                     ".....rrr....", "......v.....", "....vvv.....", "......v.....", "......vvv...", "......v....."]),
    "ceferino": ("c1", [".....ww.....", ".....ww.....", "..wwwwwwww..", "..wwwwwwww..", ".....ww.....", ".....ww.....",
                        ".....ww.....", ".....ww.....", ".....ww.....", ".....ww....."]),
    "luzmala": ("tinta", ["............", ".....A......", "....AAA.....", "...AAwAA....", "..AAwwwAA...", "..AAwwwAA...",
                          "...AAwAA....", "....AAA.....", ".....A......", "............", "..v..v..v...", ".vvvvvvvvv.."]),
    "lobizon": ("c0", ["............", "....hhhh....", "...hhhhhh...", "..hhhHhhhh..", "..hhhhhhHh..", "..hhHhhhhh..",
                       "...hhhhhh...", "....hhhh....", "............", ".k.......k..", ".kk.....kk..", ".kkk.kkkkk..",
                       ".kkkkkkkkk.."]),
    "pombero": ("v0", ["............", "....aaaa....", "...aaaaaa...", "...aaaaaa...", "...MMMMMM...", ".aaaaaaaaaa.",
                       "aaaaaaaaaaaa", "...kkkkkk...", "...kAkkAk...", "...kkkkkk...", "....kkkk...."]),
    "llorona": ("tinta", ["....wwww....", "...wwwwww...", "...wkwwkw...", "...wwwwww...", "...wwkkww...", "..wwwwwwww..",
                          "..wwwwwwww..", ".wwwwwwwwww.", ".wwwwwwwwww.", ".www.ww.www.", "..c......c..", "..c......c.."]),
    "almamula": ("r0", ["............", "...zzzzzz...", "..zzzzzzzz..", "..zzz..zzz..", "..zz....zz..", "..zz....zz..",
                        "..zz....zz..", "..zz....zz..", "..zzz..zzz..", "............", "..r.r..r.r..", ".rArrrrrArr."]),
    "basilisco": ("tinta", ["............", "............", "...GGGGGG...", "..GGvvvvGG..", ".GGvvkkvvGG.", ".GvvvkkvvvG.",
                            ".GGvvkkvvGG.", "..GGvvvvGG..", "...GGGGGG..."]),
    "ginebra": ("m2", [".....mm.....", ".....vv.....", ".....vv.....", "....vvvv....", "...vvvvvv...", "...vVvvvv...",
                       "...vhhhhv...", "...vhkkhv...", "...vhhhhv...", "...vVvvvv...", "...vvvvvv...", "....VVVV...."]),
    "fiado": ("m1", ["..hhhhhhhh..", "..hhhhhhhh..", "..hkhkhkhh..", "..hkhkhkhh..", "..hkhkhkhh..", "..hhhhhhhh..",
                     "..hrrrrrrh..", "..hhhhhhhh..", "..hkhkhhhh..", "..hkhkhhhh..", "..hhhhhhhh..", "..HHHHHHHH.."]),
    "caja": ("v0", ["............", "..mmmmmmmm..", ".mmmmmmmmmm.", ".mMMMMMMMMm.", ".mmmmGGmmmm.", ".mmmmGGmmmm.",
                    ".mmmmmmmmmm.", ".MMMMMMMMMM.", "............", "..GG..GG....", ".GggG.GgG...", "..GG..GG...."]),
    "naipe": ("v1", ["..hhhhhhhh..", "..hGhhhhhh..", "..hhhhhhhh..", "..hhhGGhhh..", "..hhGggGhh..", "..hGggggGh..",
                     "..hGggggGh..", "..hhGggGhh..", "..hhhGGhhh..", "..hhhhhhhh..", "..hhhhhhGh..", "..hhhhhhhh.."]),
    "facon": ("r1", ["..........h.", ".........hh.", "........hhh.", ".......hhH..", "......hhH...", ".....hhH....",
                     "....hhH.....", "...GhH......", "..GGG.......", "..mGG.......", ".mm.........", "mm.........."]),
    "tero": ("c2", ["............", "......kk....", ".....kkkk...", ".....kwkrr..", "....zzkk....", "...zzzzzz...",
                    "..zzzzwwzz..", ".zzzzwwwwz..", "..zzwwwww...", "....r..r....", "....r..r....", "...rr.rr...."]),
    "mulita": ("v1", ["............", "............", "....mmmmm...", "...mMmMmMm..", "..mmMmMmMmm.", ".smmMmMmMmm.",
                      "ssmmMmMmMmmm", "ksmmmmmmmmm.", ".s.mm..mm...", "...m....m..."]),
    "hornero": ("c1", ["............", "....mmmm....", "...mmmmmm...", "..mmmmmmmm..", "..mmmkkmmm..", "..mmkkkkmm..",
                       "..mmkkkkmm..", "..mmmkkmmm..", "..mmmmmmmm..", ".MMMMMMMMMM.", "MMMMMMMMMMMM"]),
    "nandu": ("a0", ["....zz......", "...zkzr.....", "....zz......", "....zz......", "....zz......", "....zzzzz...",
                     "...zzzzzzz..", "...zzzzzzzz.", "....zzzzzz..", ".....k.k....", ".....k.k....", "....kk.kk..."]),
    "yarara": ("m1", ["............", "...vvvvv....", "..vvkvvvr...", "..vv........", "..vvvvvv....", "...vVvVvv...",
                      ".......vv...", ".......vv...", "..vvvvvvv...", ".vvVvVvv....", ".vv........."]),
    "carancho": ("c1", ["............", "...kkkkk....", "..kkkkkkk...", "..kkwkkAA...", "..kkkkAAAA..", "..hhhhh.A...",
                        "..hhhhhh....", "...hhhhhh...", "...mmmmmm...", "..mmmmmmmm..", "..mmmmmmmm.."]),
    "firma": ("r0", ["..hhhhhhhh..", "..hkkkkkhh..", "..hhhhhhhh..", "..hkkkkhhh..", "..hhhhhhhh..", "..hkkkkkkh..",
                     "..hhhhhhhh..", "..hhhhhhhh..", "..hrhhrhhh..", "..hhrrhhhh..", "..hrhhrhhh..", "..hhhhhhhh.."]),
    "sexto": ("r0", ["............", "..hhhhhhhh..", ".hhhhhhhhhh.", ".hhkhhhhkhh.", ".hhhhhhhhhh.", ".hhkhhhhkhh.",
                     ".hhhhhhhhhh.", ".hhkhhhhkhh.", ".hhhhhhhhhh.", "..HHHHHHHH.."]),
    "salamanca": ("r0", ["............", "...zzzzzz...", "..zzzzzzzz..", ".zzzkkkkzzz.", ".zzkkkkkkzz.", ".zzkkrrkkzz.",
                         ".zzkrAArkzz.", ".zzkrAArkzz.", ".zzkkrrkkzz.", "zzzkkkkkkzzz"]),
    "violin": ("r0", [".........mm.", "........mm..", ".......mm...", "....mm.m....", "...mmmmm....", "..mmMmmm....",
                      "..mmmMmmm...", "...mmmmmm...", "..mmmmMmm...", ".mmmMmmmm...", ".mmmmmmm....", "..mmmmm....."]),
    "azufre": ("r0", [".....A......", "....AA......", "....AAA.....", "...AAAA.A...", "...AwAAAA...", "..AAwwAAA...",
                      "..AwwwwAA...", "..AwwwwAA...", "..AAwwAAA...", "...AAAAA....", "....zzz.....", "...zzzzz...."]),
    "cola": ("tinta", [".........r..", "........rrr.", ".......rrrrr", ".........r..", ".........r..", "........rr..",
                       ".......rr...", "..rrr.rr....", ".rr.rrr.....", ".rr.........", "..rrr.......", "....rr......"]),
}
M.ESTAMPITAS.update(NUEVAS)
M.ESTAMPITAS["sanlamuerte"] = M.ESTAMPITAS["muerte"]
M.COL.update(COL)

ORDEN = ["gauchito", "sanlamuerte", "difunta", "cayetano", "gilda", "ceferino",
         "luzmala", "lobizon", "pombero", "llorona", "almamula", "basilisco",
         "ginebra", "taba", "fiado", "caja", "naipe", "facon",
         "tero", "mulita", "hornero", "nandu", "yarara", "carancho",
         "firma", "sexto", "salamanca", "violin", "azufre", "cola"]


def fondo_mesa(jefe, semilla=3):
    rng = np.random.default_rng(semilla)
    L = M.Lienzo()
    M.madera(L, 0, 34, M.W, 140, rng)
    L.rrect(12, 86, 22, 6, P["m0"], 2)
    M.iluminar(L, 132, 84, 180, 86, 34, P["r1"] if jefe else (26, 14, 34), calido=0.06)
    a = L.arr()
    M.halo(a, 23, 70, 46, P["a0"], 0.5, pasos=5)
    if jefe:
        M.halo(a, 160, 30, 90, P["r2"], 0.45, pasos=5, aplaste=1.6)
    L.desde(a)
    M.a_paleta(L)
    L.rect(0, 0, M.W, 34, P["tinta"])
    if jefe:
        a = L.arr(); M.halo(a, 160, 22, 70, P["r1"], 0.9, pasos=4, aplaste=1.8); L.desde(a); M.a_paleta(L)
    L.rect(0, 33, M.W, 1, P["r2"] if jefe else P["m3"])
    M.rival(L, jefe)
    M.farol(L, 14, 54)
    M.baranda(L, [])
    L.rect(0, 142, 124, 38, P["m1"])                                   # sin huecos: los dibuja el juego
    return L


def fondo_tienda(semilla=5):
    L = M.tienda(semilla)                                              # la maqueta entera, y se limpia lo que es del juego
    a = L.arr()
    base = M.Lienzo()
    rng = np.random.default_rng(semilla)
    M.madera(base, 0, 58, M.W, 140, rng)
    base.rect(0, 58, M.W, 2, P["m4"])
    for mx, mw in ((10, 148), (168, 142)):
        base.rrect(mx, 62, mw, 56, P["tinta"], 2); base.rrect(mx + 1, 63, mw - 2, 54, P["v1"], 2)
        for i in range(mx + 4, mx + mw - 4, 3):
            base.px(i, 65, P["v2"]); base.px(i, 114, P["v2"])
    M.iluminar(base, 160, 78, 215, 105, 0, (26, 14, 34), calido=0.05)
    M.a_paleta(base)
    b = base.arr()
    a[58:140] = b[58:140]                                              # mostrador y paños limpios
    a[0:16, 286:320] = a[0:16, 234:268]                                # sin la plata dibujada: se copia un tramo de pared
    L.desde(a)
    M.baranda(L, [])
    L.rect(0, 142, 124, 38, P["m1"])
    return L


if __name__ == "__main__":
    for nombre, L in (("fondo_mesa", fondo_mesa(False)), ("fondo_jefe", fondo_mesa(True)), ("fondo_tienda", fondo_tienda())):
        Image.fromarray(L.arr()).save(SALIDA / f"{nombre}.png")
    hoja = M.Lienzo()
    hoja.im = Image.new("RGB", (20 * len(ORDEN), 28), P["tinta"]); hoja.d = __import__("PIL.ImageDraw").ImageDraw.Draw(hoja.im)
    for i, e in enumerate(ORDEN):
        M.estampita(hoja, i * 20, 0, e)
    hoja.im.save(SALIDA / "estampitas.png")
    letras = {k: v.split() for k, v in M.letra.G.items()}
    (SALIDA / "arte.json").write_text(json.dumps({"estampitas": ORDEN, "letra": letras}, ensure_ascii=False), encoding="utf-8")
    # lámina para revisar a ojo
    lam = Image.new("RGB", (320, 360 + 60), P["tinta"])
    for k, nombre in enumerate(("fondo_mesa", "fondo_tienda")):
        lam.paste(Image.open(SALIDA / f"{nombre}.png"), (0, k * 180))
    est = Image.open(SALIDA / "estampitas.png")
    lam.paste(est.crop((0, 0, 300, 28)), (10, 362)); lam.paste(est.crop((300, 0, 600, 28)), (10, 392))
    print("fondos y", len(ORDEN), "estampitas listos")
