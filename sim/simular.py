"""Simulador de la Generala maldita: juega miles de partidas con un bot para ver qué rompe y qué no sirve.

Sigue las reglas de ../DISENO.md. Lo que el diseño no define todavía lo fija acá (ver SUPUESTOS).

    python games/generala/sim/simular.py 2000 2      # partidas, procesos

Deja el informe en RESULTADOS.md y los números crudos en resultados.json.
"""
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from multiprocessing import Pool
from pathlib import Path

SUPUESTOS = [
    "Plata: empezás con 6 y cobrás 8 por mesa ganada, más lo que den los ítems y el premio por pasarse.",
    "Precios de estampita: común 4, rara 7, legendaria 10. Tienda: 3 estampitas y 2 caras.",
    "Pacto: después de las mesas 2, 4 y 6 el Mandinga ofrece 2 pactos gratis; el bot acepta uno 6 de cada 10 veces.",
    "Los jefes no tienen regla propia todavía: las mesas 4 y 8 son mesas comunes.",
    "Se juegan siempre todas las anotaciones de la mesa, aunque la meta ya esté pasada.",
    "El bot compra al azar lo que le alcanza (así se mide cada ítem sin el gusto del bot) y no vende.",
    "El bot pega las caras en su número favorito: el 1 si tiene San La Muerte o Tero, si no el 6.",
    "El bot decide qué fijar mirando un solo tiro hacia adelante. Un humano bueno juega mejor.",
    "Servida vale solo para escalera, full, póker y generala.",
    "Basilisco: si anotás sin volver a tirar, cuentan todos los dados como fijados.",
]

NUM = {"unos": 1, "doses": 2, "treses": 3, "cuatros": 4, "cincos": 5, "seises": 6}
BASE = {"escalera": (20, 2), "full": (30, 2), "poker": (40, 3), "generala": (50, 5)}
JUGADAS = list(NUM) + list(BASE)
METAS = [80, 220, 600, 2000, 5000, 12000, 30000, 80000]
CARAS = {"hueso": 2, "brasa": 3, "dorada": 3, "cargada": 3, "inquieta": 3, "semilla": 4, "comodin": 5, "maldita": 5,
         "doble": 6, "contagiosa": 6, "hielo": 6, "espejo": 7}
ESTAMPITAS = {
    "gauchito": "SC", "sanlamuerte": "SR", "difunta": "SC", "cayetano": "SC", "gilda": "SR", "ceferino": "SC",
    "luzmala": "AC", "lobizon": "AR", "pombero": "AC", "llorona": "AR", "almamula": "AR", "basilisco": "AL",
    "ginebra": "PC", "taba": "PC", "fiado": "PC", "caja": "PR", "naipe": "PR", "facon": "PR",
    "tero": "MC", "mulita": "MC", "hornero": "MR", "nandu": "MR", "yarara": "MR", "carancho": "MR",
    "firma": "DL", "sexto": "DL", "salamanca": "DL", "violin": "DR", "azufre": "DR", "cola": "DR",
}  # familia (Santos, Aparecidos, Pulpería, paMpa, Diablo) + rareza
PRECIO = {"C": 4, "R": 7, "L": 10}
PESO = {"C": 60, "R": 32, "L": 8}
MULTIPLICAN = ["firma", "basilisco", "lobizon", "carancho", "yarara"]
COPIA_PRIMERO = MULTIPLICAN + ["violin", "gilda", "sanlamuerte", "gauchito", "ginebra"]
MUESTRAS = 6


class Estado:
    def __init__(self):
        self.dados = [[{"v": v, "p": set(), "s": 0, "w": 1} for v in range(1, 7)] for _ in range(6)]
        self.tengo = []
        self.plata = 6
        self.llorona = self.almamula = self.mulita = self.hornero = 0
        self.rehacer()

    def rehacer(self):
        t = [e for e in self.tengo if e != "salamanca"]
        orden = [e for e in t if e not in MULTIPLICAN] + [e for e in t if e in MULTIPLICAN]
        if "salamanca" in self.tengo and t:
            orden.append(next((e for e in COPIA_PRIMERO if e in t), t[0]))
        self.orden = orden
        self.n = Counter(orden)
        fam = Counter(ESTAMPITAS[e][0] for e in self.tengo)
        self.santuario = 2 if fam["S"] >= 3 else 1
        self.crece = 2 if fam["A"] >= 3 else 1
        self.parroquiano = fam["P"] >= 3
        self.baqueano = fam["M"] >= 3
        self.condenado = fam["D"] >= 3
        self.suerte = 2 ** self.n["naipe"]
        self.nd = 6 if "sexto" in self.tengo else 5
        self.fav = 1 if (self.n["sanlamuerte"] or self.n["tero"]) and not self.n["azufre"] else 6


class Ctx:
    __slots__ = ("sobran", "servida", "fijados", "ultima", "numeros", "usadas", "facon")

    def __init__(self, **k):
        for a, b in k.items():
            setattr(self, a, b)


def tirar(dado, rng):
    return rng.choices(dado, weights=[c["w"] for c in dado])[0]


def vista(vals, caras):
    """Resuelve los espejos: devuelve (valores, propiedades, cara que guarda la semilla)."""
    v, p, f = list(vals), [], []
    for i, c in enumerate(caras):
        if "espejo" in c["p"] and i > 0:
            v[i] = v[i - 1]; p.append(p[i - 1]); f.append(f[i - 1])
        else:
            p.append(c["p"]); f.append(c)
    return v, p, f


def patron(vals, jug, nandu):
    cu = Counter(vals)
    if jug == "generala" or jug == "poker":
        hace = 5 if jug == "generala" else 4
        ok = [v for v, c in cu.items() if c >= hace]
        return [i for i, v in enumerate(vals) if v == max(ok)] if ok else None
    if jug == "full":
        tr = [v for v, c in cu.items() if c >= 3]
        for a in sorted(tr, reverse=True):
            pa = [v for v, c in cu.items() if c >= 2 and v != a]
            if pa:
                b = max(pa)
                return [i for i, v in enumerate(vals) if v in (a, b)]
        return None
    largo = 4 if nandu else 5
    for ini in range(6 - largo + 1, 0, -1):
        tramo = set(range(ini, ini + largo))
        if tramo <= set(cu):
            if largo == 4:                                    # con Ñandú, si hay 5 seguidos puntúan los 5
                for ini5 in (2, 1):
                    t5 = set(range(ini5, ini5 + 5))
                    if t5 <= set(cu):
                        tramo = t5
            return [i for i, v in enumerate(vals) if v in tramo]
    return None


def puntuar(S, vals, props, caras, jug, c, real=False, rng=None):
    """Puntaje de una jugada. Con real=True aplica lo que queda para siempre (plata, crecimientos, hielo roto)."""
    n = S.n
    if jug in NUM:
        sc = [i for i, v in enumerate(vals) if v == NUM[jug]]
        pts, mult = 0, 1
    else:
        sc = patron(vals, jug, n["nandu"])
        if sc is None:
            return 0
        pts, mult = BASE[jug]
        if c.servida and not n["cola"]:
            mult += 5
    if not sc:
        return 0
    dob = S.santuario
    malditas = plata = 0
    hornero = S.hornero
    rotos = []
    prim, ult = sc[0], sc[-1]
    for i in sc:
        v, p = vals[i], props[i]
        if v == 1 and n["azufre"]:
            continue
        veces = 1 + n["violin"] + ("doble" in p) + (n["gilda"] if i == prim or i == ult else 0)
        for _ in range(veces):
            pts += 10 if (v <= 2 and n["tero"]) else v
            if p:
                if "hueso" in p: pts += 15
                if "brasa" in p: mult += 4
                if "dorada" in p: plata += 1
                if "semilla" in p:
                    pts += caras[i]["s"]
                    if real: caras[i]["s"] += 2 * S.crece
                if "hielo" in p:
                    mult *= 2
                    if real and rng.random() < min(1, 0.25 * S.suerte): rotos.append(caras[i])
            if (p and "maldita" in p) or (v == 6 and n["azufre"]):
                mult *= 1.5; malditas += 1
            if v == 1 and n["sanlamuerte"]:
                mult += 4 * dob * n["sanlamuerte"]
            if n["hornero"]:
                hornero += 3 * S.crece * n["hornero"]
    en = set(sc)
    for i, p in enumerate(props):
        if i not in en and "maldita" in p:
            pts -= 10
    for e in S.orden:
        if e == "gauchito": mult += (4 + 4 * malditas) * dob
        elif e == "ceferino": pts += 20 * c.numeros
        elif e == "luzmala": mult += 3 * c.sobran * dob
        elif e == "taba":
            pr = min(1, 0.5 * S.suerte)
            mult += (10 * dob if rng.random() < pr else 0) if real else 10 * dob * pr
        elif e == "caja": mult += max(0, (S.plata + plata) // 2) * dob
        elif e == "nandu" and jug == "escalera": mult += 3 * dob
        elif e == "llorona": mult += S.llorona * dob
        elif e == "almamula": mult += S.almamula * dob
        elif e == "mulita": pts += S.mulita
        elif e == "hornero": pts += S.hornero                      # lo guardado suma una vez por jugada
        elif e == "lobizon" and c.ultima: mult *= 3
        elif e == "basilisco": mult *= 1.5 ** c.fijados
        elif e == "yarara" and all(vals[i] % 2 == 0 for i in sc): mult *= 2
        elif e == "carancho": mult *= 1.5 ** (len(vals) - len(sc))
        elif e == "firma": mult *= 4
    if S.condenado:
        mult *= 2
    if real:
        S.plata += plata
        S.hornero = hornero
        if jug in NUM: S.mulita += 5 * S.crece * n["mulita"]
        for cara in rotos: cara["p"].discard("hielo")
    return max(0, pts) * mult


def mejor(S, vals0, caras, c, pombero=False):
    """Mejor jugada disponible: (puntaje, jugada, valores finales). Prueba comodines y la vuelta del Pombero."""
    vals, props, cf = vista(vals0, caras)
    com = [i for i, p in enumerate(props) if "comodin" in p]
    if not com: variantes = [vals]
    elif len(com) <= 2: variantes = [_con(vals, com, o) for o in product(range(1, 7), repeat=len(com))]
    else: variantes = [_con(vals, com, (v,) * len(com)) for v in range(1, 7)]
    if pombero:
        variantes = variantes + [_con(w, [i], (7 - w[i],)) for w in variantes[:6] for i in range(len(w))]
    libres = [j for j in JUGADAS if j not in c.usadas] if not c.facon else JUGADAS
    top = (-1, None, vals)
    for w in variantes:
        presentes = set(w)
        for j in libres:
            if j in NUM and NUM[j] not in presentes:
                continue
            s = puntuar(S, w, props, cf, j, c)
            if s > top[0]:
                top = (s, j, w)
    if top[1] is None:
        top = (0, libres[0], vals)
    return top


def _con(vals, idx, nuevos):
    w = list(vals)
    for i, v in zip(idx, nuevos):
        w[i] = v
    return w


def candidatos(vals, props):
    fijos = {i for i, p in enumerate(props) if "comodin" in p}
    out = [set(fijos)]
    for v in set(vals):
        out.append(fijos | {i for i, x in enumerate(vals) if x == v})
    mejor_tramo = set()
    for ini in (1, 2, 3):                                           # el tramo de escalera más largo
        tramo, visto = set(), set()
        for i, x in enumerate(vals):
            if ini <= x < ini + 5 and x not in visto:
                visto.add(x); tramo.add(i)
        if len(tramo) > len(mejor_tramo):
            mejor_tramo = tramo
    out.append(fijos | mejor_tramo)
    unicos = []
    for h in out:
        if h not in unicos and len(h) < len(vals):
            unicos.append(h)
    return unicos


def cola(S, vals, caras, c):
    """Cola del diablo: sin tiros, hasta 6 giros de +1 (el 6 vuelve al 1)."""
    top = mejor(S, vals, caras, c)
    pruebas = []
    for v in range(1, 7):
        w, resto = list(vals), 6
        for costo, i in sorted(((v - x) % 6, i) for i, x in enumerate(vals)):
            if costo <= resto:
                w[i] = v; resto -= costo
        pruebas.append(w)
    if len(vals) == 5:
        for ini in (1, 2):
            mc, mw = 99, None
            for perm in permutations(range(ini, ini + 5)):
                costo = sum((t - x) % 6 for t, x in zip(perm, vals))
                if costo < mc:
                    mc, mw = costo, list(perm)
            if mc <= 6:
                pruebas.append(mw)
    for w in pruebas:
        t = mejor(S, w, caras, c)
        if t[0] > top[0]:
            top = t
    return top


def turno(S, rng, usadas, facon, numeros, ultima, primer_turno, ganada):
    nd = S.nd
    tiros = max(1, 3 + S.n["ginebra"] - (1 if "sexto" in S.tengo else 0) + (2 * S.n["difunta"] if primer_turno else 0))
    dados = S.dados[:nd]
    caras = [tirar(d, rng) for d in dados]
    vals = [c["v"] for c in caras]
    usados, fijados = 1, None
    granja = ganada and S.n["almamula"]

    def ctx(sobran, servida, fij):
        return Ctx(sobran=sobran, servida=servida, fijados=fij, ultima=ultima, numeros=numeros, usadas=usadas, facon=facon)

    if S.n["cola"]:
        s, jug, w = cola(S, vals, caras, ctx(0, False, nd))
        return s, jug, w, caras, ctx(0, False, nd), 0
    while usados < tiros:
        ahora = mejor(S, vals, caras, ctx(tiros - usados, usados == 1, nd if fijados is None else fijados))[0]
        _, props, _ = vista(vals, caras)
        elegido, valor = None, ahora
        if granja:
            elegido = set()
        else:
            for h in candidatos(vals, props):
                c2 = ctx(tiros - usados - 1, False, len(h) if fijados is None else fijados)
                tot = 0
                for _ in range(MUESTRAS):
                    cs = [caras[i] if i in h else tirar(dados[i], rng) for i in range(nd)]
                    tot += mejor(S, [vals[i] if i in h else cs[i]["v"] for i in range(nd)], cs, c2)[0]
                if tot / MUESTRAS > valor:
                    elegido, valor = h, tot / MUESTRAS
        if elegido is None:
            break
        for i in sorted(elegido):                                   # la contagiosa pasa su número al de la derecha
            if "contagiosa" in caras[i]["p"] and i + 1 < nd:
                vals[i + 1] = vals[i]; elegido = elegido | {i + 1}
        if fijados is None:
            fijados = len(elegido)
        if not elegido:
            S.almamula += 2 * S.crece * S.n["almamula"]
        for i in range(nd):
            if i not in elegido:
                caras[i] = tirar(dados[i], rng); vals[i] = caras[i]["v"]
        usados += 1
    c = ctx(tiros - usados, usados == 1, nd if fijados is None else fijados)
    s, jug, w = mejor(S, vals, caras, c, pombero=bool(S.n["pombero"]))
    for i in range(nd):                                             # cara inquieta: un tiro gratis si no ayudó
        if "inquieta" in caras[i]["p"]:
            en = patron(w, jug, S.n["nandu"]) if jug in BASE else [k for k, v in enumerate(w) if v == NUM[jug]]
            if not en or i not in en:
                caras[i] = tirar(dados[i], rng); vals[i] = caras[i]["v"]
                s, jug, w = mejor(S, vals, caras, c, pombero=bool(S.n["pombero"]))
            break
    return s, jug, w, caras, c, tiros - usados


def pegar_cara(S, nombre, rng):
    idx = list(range(S.nd))
    if nombre == "espejo": idx = idx[1:]
    if nombre == "contagiosa": idx = idx[:-1]
    rng.shuffle(idx)
    for prueba in (S.fav, None):
        for i in idx:
            libres = [c for c in S.dados[i] if not c["p"] and (prueba is None or c["v"] == prueba)]
            if libres:
                cara = rng.choice(libres)
                cara["p"].add(nombre)
                if nombre == "cargada": cara["w"] = 2
                return
    S.dados[idx[0]][S.fav - 1]["p"].add(nombre)


def partida(semilla):
    rng = random.Random(semilla)
    S = Estado()
    compras, pico, llamas, mesas = [], 0.0, 0, 0
    for m, meta in enumerate(METAS):
        if S.n["violin"]: meta *= 1.25
        puntos, usadas, numeros, sobrantes = 0, set(), 0, 0
        facon = S.n["facon"]
        anot = max(1, 4 - (1 if "firma" in S.tengo else 0) + (1 if S.baqueano else 0))
        for a in range(anot):
            ganada = puntos >= meta
            s, jug, w, caras, c, sobran = turno(S, rng, usadas, facon, numeros, a == anot - 1, a == 0, ganada)
            if ganada and S.n["llorona"]:                           # con la mesa ganada, tacha para alimentar a la Llorona
                libres = [j for j in JUGADAS if j not in usadas]
                tachar = [j for j in libres if j in BASE and patron(w, j, S.n["nandu"]) is None]
                if tachar:
                    jug, s = tachar[0], 0
            if s > 0:
                _, props, cf = vista([cc["v"] for cc in caras], caras)
                s = puntuar(S, w, props, cf, jug, c, real=True, rng=rng)
            if s == 0:
                S.llorona += 2 * S.crece * S.n["llorona"]
            if jug in usadas: facon -= 1
            usadas.add(jug)
            numeros += jug in NUM
            puntos += s
            sobrantes += sobran
            for _ in range(S.n["naipe"]):                           # el naipe paga 1 de plata, 1 de cada 3 veces
                S.plata += rng.random() < min(1, S.suerte / 3)
        pico = max(pico, puntos / meta)
        if puntos < meta:
            break
        mesas = m + 1
        llamas += puntos >= 10 * meta
        S.plata += 8 + S.n["cayetano"] * sobrantes + 3 * int(math.log10(puntos / meta)) - ("salamanca" in S.tengo)
        if m == len(METAS) - 1:
            break
        piso = -10 if S.n["fiado"] else 0
        pozo = [e for e, fr in ESTAMPITAS.items() if fr[0] != "D" and e not in S.tengo]
        oferta = []
        for _ in range(4 if S.parroquiano else 3):
            if pozo:
                e = rng.choices(pozo, weights=[PESO[ESTAMPITAS[x][1]] for x in pozo])[0]
                pozo.remove(e); oferta.append(("E", e, PRECIO[ESTAMPITAS[e][1]]))
        oferta += [("C", x, CARAS[x]) for x in rng.sample(list(CARAS), 2)]
        rng.shuffle(oferta)
        for tipo, nombre, precio in oferta:
            if S.plata - precio < piso or (tipo == "E" and len(S.tengo) >= 5):
                continue
            S.plata -= precio
            compras.append((nombre, m))
            if tipo == "E":
                S.tengo.append(nombre); S.rehacer()
            else:                                                   # cada cara comprada se pega en dos dados
                pegar_cara(S, nombre, rng); pegar_cara(S, nombre, rng)
        if m in (1, 3, 5) and len(S.tengo) < 5 and rng.random() < 0.6:
            pactos = [e for e, fr in ESTAMPITAS.items() if fr[0] == "D" and e not in S.tengo]
            e = rng.choice(rng.sample(pactos, min(2, len(pactos))))
            S.tengo.append(e); S.rehacer(); compras.append((e, m))
    return {"mesas": mesas, "compras": compras, "pico": pico, "llamas": llamas, "tengo": list(S.tengo)}


# ---------------- informe ----------------
def informe(res, seg):
    N = len(res)
    dist = Counter(r["mesas"] for r in res)
    base = {}
    for m in range(8):
        llegan = [r["mesas"] for r in res if r["mesas"] > m]
        base[m] = sum(llegan) / len(llegan) if llegan else 0
    por = defaultdict(list)
    for r in res:
        for nombre, m in r["compras"]:
            por[nombre].append(r["mesas"] - base[m])
    pares = defaultdict(list)
    for r in res:
        cuando = {}
        for nombre, m in r["compras"]:
            if nombre in ESTAMPITAS: cuando[nombre] = m
        for a, b in combinations(sorted(cuando), 2):
            pares[(a, b)].append(r["mesas"] - base[max(cuando[a], cuando[b])])

    def fila(nombre, d):
        n = len(d); med = sum(d) / n
        se = (sum((x - med) ** 2 for x in d) / max(n - 1, 1)) ** 0.5 / n ** 0.5
        return nombre, n, med, se

    est = sorted((fila(k, d) for k, d in por.items() if k in ESTAMPITAS), key=lambda f: -f[2])
    car = sorted((fila(k, d) for k, d in por.items() if k in CARAS), key=lambda f: -f[2])
    par = sorted((fila(" + ".join(k), d) for k, d in pares.items() if len(d) >= 25), key=lambda f: -f[2])
    picos = sorted(r["pico"] for r in res)
    L = ["# Generala maldita: resultados del simulador", "",
         f"{N} partidas en {seg:.0f} segundos. Bot que compra al azar y mira un tiro hacia adelante.", "",
         "## Hasta dónde llega", "", "| Mesas ganadas | Partidas | % |", "|---|---|---|"]
    for m in range(9):
        L.append(f"| {m}{' (ganó)' if m == 8 else ''} | {dist[m]} | {100 * dist[m] / N:.1f} |")
    conllamas = sum(1 for r in res if r["llamas"])
    L += ["", f"- Partidas con al menos una mesa pasada por 10 veces la meta: {conllamas} ({100 * conllamas / N:.1f} %)",
          f"- Mejor mesa de cada partida, puntaje sobre meta: mediana {picos[N // 2]:.1f}, el 10 % de arriba pasa {picos[int(N * 0.9)]:.1f}, máximo {picos[-1]:,.0f}",
          "", "## Estampitas", "",
          "Ventaja = mesas ganadas de más frente a las partidas que llegaron a esa misma tienda. El ± es el error estándar.", "",
          "| Estampita | Compras | Ventaja | ± |", "|---|---|---|---|"]
    L += [f"| {a} | {n} | {m:+.2f} | {s:.2f} |" for a, n, m, s in est]
    L += ["", "## Caras", "", "| Cara | Compras | Ventaja | ± |", "|---|---|---|---|"]
    L += [f"| {a} | {n} | {m:+.2f} | {s:.2f} |" for a, n, m, s in car]
    L += ["", "## Pares de estampitas (25 partidas o más)", "", "| Par | Partidas | Ventaja | ± |", "|---|---|---|---|"]
    L += [f"| {a} | {n} | {m:+.2f} | {s:.2f} |" for a, n, m, s in par[:12]]
    L += ["", "Los peores:", "", "| Par | Partidas | Ventaja | ± |", "|---|---|---|---|"]
    L += [f"| {a} | {n} | {m:+.2f} | {s:.2f} |" for a, n, m, s in par[-6:]]
    L += ["", "## Supuestos", ""] + [f"- {s}" for s in SUPUESTOS]
    return "\n".join(L) + "\n", {"dist": dict(dist), "estampitas": est, "caras": car, "pares": par}


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    t0 = time.time()
    if procs > 1:
        with Pool(procs) as pool:
            res = pool.map(partida, range(N), chunksize=20)
    else:
        res = [partida(i) for i in range(N)]
    seg = time.time() - t0
    texto, crudo = informe(res, seg)
    aqui = Path(__file__).resolve().parent
    sufijo = "" if N >= 1000 else "_prueba"
    (aqui / f"RESULTADOS{sufijo}.md").write_text(texto, encoding="utf-8")
    (aqui / f"resultados{sufijo}.json").write_text(json.dumps(crudo, ensure_ascii=False), encoding="utf-8")
    print(texto)
