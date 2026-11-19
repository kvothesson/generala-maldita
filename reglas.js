// Generala maldita: reglas puras, sin pantalla. Las usa index.html y se prueban con node (sim/probar_reglas.js).
// Siguen DISENO.md. El simulador de Python (sim/simular.py) tiene las mismas cuentas.
(function (raiz) {
  'use strict';

  const NUM = { unos: 1, doses: 2, treses: 3, cuatros: 4, cincos: 5, seises: 6 };
  const BASE = { escalera: [20, 2], full: [30, 2], poker: [40, 3], generala: [50, 5] };
  const JUGADAS = ['unos', 'doses', 'treses', 'cuatros', 'cincos', 'seises', 'escalera', 'full', 'poker', 'generala'];
  const METAS = [80, 220, 600, 2000, 5000, 12000, 30000, 80000];
  const JEFES = { 3: { id: 'seises', nombre: 'EL FAMILIAR', regla: 'LOS SEISES NO VALEN' }, 7: { id: 'tiro', nombre: 'EL MANDINGA', regla: 'UN TIRO MENOS' } };

  const CARAS = {
    hueso: { nombre: 'HUESO VIEJO', precio: 2, desc: '+15 PUNTOS AL PUNTUAR' },
    brasa: { nombre: 'BRASA', precio: 3, desc: '+4 MULT AL PUNTUAR' },
    dorada: { nombre: 'DORADA', precio: 3, desc: '+1 DE PLATA AL PUNTUAR' },
    cargada: { nombre: 'CARGADA', precio: 3, desc: 'ESE LADO SALE EL DOBLE DE VECES' },
    inquieta: { nombre: 'INQUIETA', precio: 3, desc: 'UNA VEZ POR TURNO SE TIRA DE NUEVO GRATIS' },
    semilla: { nombre: 'SEMILLA', precio: 4, desc: 'GANA +2 PUNTOS PARA SIEMPRE AL PUNTUAR' },
    comodin: { nombre: 'COMODÍN', precio: 5, desc: 'VALE EL NÚMERO QUE MÁS TE CONVENGA' },
    maldita: { nombre: 'MALDITA', precio: 5, desc: '×1,5 MULT. FUERA DE LA JUGADA, -10 PUNTOS' },
    doble: { nombre: 'DOBLE', precio: 6, desc: 'PUNTÚA DOS VECES' },
    contagiosa: { nombre: 'CONTAGIOSA', precio: 6, desc: 'AL FIJARLA, EL DADO DE LA DERECHA LA COPIA' },
    hielo: { nombre: 'DE HIELO', precio: 6, desc: '×2 MULT. 1 EN 4 DE ROMPERSE' },
    espejo: { nombre: 'ESPEJO', precio: 7, desc: 'COPIA AL DADO DE SU IZQUIERDA' },
  };

  // fam: S santos, A aparecidos, P pulpería, M pampa, D pactos. r: C común, R rara, L legendaria.
  const ESTAMPITAS = {
    gauchito: { nombre: 'GAUCHITO GIL', fam: 'S', r: 'C', desc: '+4 MULT. +4 MÁS POR CADA MALDITA QUE PUNTÚE' },
    sanlamuerte: { nombre: 'SAN LA MUERTE', fam: 'S', r: 'R', desc: 'CADA 1 QUE PUNTÚA DA +4 MULT' },
    difunta: { nombre: 'DIFUNTA CORREA', fam: 'S', r: 'C', desc: 'EL PRIMER TURNO DE CADA MESA TIENE +2 TIROS' },
    cayetano: { nombre: 'SAN CAYETANO', fam: 'S', r: 'C', desc: 'AL CERRAR LA MESA, +1 PLATA POR TIRO SIN USAR' },
    gilda: { nombre: 'GILDA', fam: 'S', r: 'R', desc: 'EL PRIMER Y EL ÚLTIMO DADO PUNTÚAN DE NUEVO' },
    ceferino: { nombre: 'CEFERINO', fam: 'S', r: 'C', desc: '+20 PUNTOS POR CADA NÚMERO YA ANOTADO' },
    luzmala: { nombre: 'LUZ MALA', fam: 'A', r: 'C', desc: '+3 MULT POR CADA TIRO QUE TE SOBRE' },
    lobizon: { nombre: 'LOBIZÓN', fam: 'A', r: 'R', desc: '×3 MULT EN LA ÚLTIMA ANOTACIÓN DE LA MESA' },
    pombero: { nombre: 'POMBERO', fam: 'A', r: 'C', desc: 'UNA VEZ POR TURNO DAS VUELTA UN DADO' },
    llorona: { nombre: 'LLORONA', fam: 'A', r: 'R', desc: 'GANA +2 MULT CADA VEZ QUE TACHÁS CON 0' },
    almamula: { nombre: 'ALMAMULA', fam: 'A', r: 'R', desc: 'GANA +2 MULT AL TIRAR TODOS LOS DADOS DE NUEVO' },
    basilisco: { nombre: 'BASILISCO', fam: 'A', r: 'L', desc: '×1,5 MULT POR DADO FIJADO EN EL PRIMER TIRO' },
    ginebra: { nombre: 'GINEBRA', fam: 'P', r: 'C', desc: '+1 TIRO POR TURNO' },
    taba: { nombre: 'LA TABA', fam: 'P', r: 'C', desc: 'AL ANOTAR, 1 EN 2 DE SUMAR +10 MULT' },
    fiado: { nombre: 'EL FIADO', fam: 'P', r: 'C', desc: 'PODÉS QUEDAR DEBIENDO HASTA 10 DE PLATA' },
    caja: { nombre: 'CAJA DEL PULPERO', fam: 'P', r: 'R', desc: '+1 MULT POR CADA 2 DE PLATA QUE TENGAS' },
    naipe: { nombre: 'NAIPE MARCADO', fam: 'P', r: 'R', desc: 'SUERTE DOBLE. AL ANOTAR, 1 EN 3 DE +1 PLATA' },
    facon: { nombre: 'FACÓN', fam: 'P', r: 'R', desc: 'UNA VEZ POR MESA REPETÍS UNA JUGADA ANOTADA' },
    tero: { nombre: 'TERO', fam: 'M', r: 'C', desc: 'LOS 1 Y LOS 2 VALEN 10 PUNTOS CADA UNO' },
    mulita: { nombre: 'MULITA', fam: 'M', r: 'C', desc: 'GANA +5 PUNTOS CADA VEZ QUE ANOTÁS UN NÚMERO' },
    hornero: { nombre: 'HORNERO', fam: 'M', r: 'R', desc: 'GANA +3 PUNTOS POR CADA DADO QUE PUNTÚA' },
    nandu: { nombre: 'ÑANDÚ', fam: 'M', r: 'R', desc: 'ESCALERA CON 4 DADOS Y +3 MULT' },
    yarara: { nombre: 'YARARÁ', fam: 'M', r: 'R', desc: '×2 MULT SI TODO LO QUE PUNTÚA ES PAR' },
    carancho: { nombre: 'CARANCHO', fam: 'M', r: 'R', desc: '×1,5 MULT POR CADA DADO FUERA DE LA JUGADA' },
    firma: { nombre: 'LA FIRMA', fam: 'D', r: 'L', desc: '×4 MULT', cobra: 'UNA ANOTACIÓN MENOS POR MESA' },
    sexto: { nombre: 'EL SEXTO', fam: 'D', r: 'L', desc: 'TIRÁS 6 DADOS Y PUNTÚAN LOS 6', cobra: 'UN TIRO MENOS POR TURNO' },
    salamanca: { nombre: 'SALAMANCA', fam: 'D', r: 'L', desc: 'COPIA A LA ESTAMPITA DE SU DERECHA', cobra: '1 DE PLATA POR MESA' },
    violin: { nombre: 'VIOLÍN DEL DIABLO', fam: 'D', r: 'R', desc: 'TODOS LOS DADOS PUNTÚAN OTRA VEZ', cobra: 'LAS METAS SUBEN 25%' },
    azufre: { nombre: 'AZUFRE', fam: 'D', r: 'R', desc: 'TUS 6 CUENTAN COMO MALDITOS', cobra: 'LOS 1 NO PUNTÚAN' },
    cola: { nombre: 'COLA DEL DIABLO', fam: 'D', r: 'R', desc: 'SIN TIROS: GIRÁS DADOS DE A +1, 6 GIROS', cobra: 'NO HAY SERVIDA' },
  };
  const PRECIO = { C: 4, R: 7, L: 10 };
  const PESO = { C: 60, R: 32, L: 8 };
  const FAMILIAS = {
    S: { nombre: 'SANTUARIO', desc: 'TUS +MULT DE ESTAMPITA VALEN EL DOBLE' },
    A: { nombre: 'NOCHE CERRADA', desc: 'LO QUE CRECE PARA SIEMPRE CRECE EL DOBLE' },
    P: { nombre: 'PARROQUIANO', desc: 'UN PRODUCTO MÁS EN LA TIENDA' },
    M: { nombre: 'BAQUEANO', desc: 'UNA ANOTACIÓN MÁS POR MESA' },
    D: { nombre: 'CONDENADO', desc: '×2 MULT AL FINAL' },
  };

  function nuevoEstado() {
    const dados = [];
    for (let d = 0; d < 6; d++) {
      const lados = [];
      for (let v = 1; v <= 6; v++) lados.push({ v, p: [], s: 0, w: 1 });
      dados.push(lados);
    }
    return { dados, tengo: [], plata: 6, llorona: 0, almamula: 0, mulita: 0, hornero: 0 };
  }

  // Lo que de verdad cuenta al puntuar: la Salamanca se vuelve la estampita de su derecha.
  function efectivas(S) {
    const out = [];
    S.tengo.forEach((e, k) => {
      if (e !== 'salamanca') out.push({ id: e, k });
      else if (S.tengo[k + 1] && S.tengo[k + 1] !== 'salamanca') out.push({ id: S.tengo[k + 1], k });
    });
    return out;
  }
  function cuenta(S) {
    const n = {};
    for (const id in ESTAMPITAS) n[id] = 0;
    efectivas(S).forEach((e) => { n[e.id]++; });
    return n;
  }
  function familias(S) {
    const f = { S: 0, A: 0, P: 0, M: 0, D: 0 };
    S.tengo.forEach((e) => { f[ESTAMPITAS[e].fam]++; });
    const out = {};
    for (const k in f) out[k] = f[k] >= 3;
    return out;
  }
  const tiene = (S, id) => S.tengo.includes(id);
  const cuantosDados = (S) => (tiene(S, 'sexto') ? 6 : 5);
  const suerte = (S) => Math.pow(2, cuenta(S).naipe);
  function tirosDelTurno(S, primerTurno, jefe) {
    const n = cuenta(S);
    if (n.cola) return 1;
    return Math.max(1, 3 + n.ginebra - (tiene(S, 'sexto') ? 1 : 0) + (primerTurno ? 2 * n.difunta : 0) - (jefe === 'tiro' ? 1 : 0));
  }
  const anotaciones = (S) => Math.max(1, 4 - (tiene(S, 'firma') ? 1 : 0) + (familias(S).M ? 1 : 0));
  const metaDe = (S, mesa) => Math.round(METAS[mesa] * (tiene(S, 'violin') ? 1.25 : 1));

  function tirar(dado, rng) {
    let tot = 0;
    dado.forEach((c) => { tot += c.w; });
    let r = rng() * tot;
    for (const c of dado) { r -= c.w; if (r < 0) return c; }
    return dado[dado.length - 1];
  }

  // Resuelve los espejos: valores, propiedades y la cara que guarda la semilla.
  function vista(vals, caras) {
    const v = vals.slice(), p = [], f = [];
    caras.forEach((c, i) => {
      if (c.p.includes('espejo') && i > 0) { v[i] = v[i - 1]; p.push(p[i - 1]); f.push(f[i - 1]); }
      else { p.push(c.p); f.push(c); }
    });
    return { v, p, f };
  }

  function patron(vals, jug, nandu) {
    const cu = {};
    vals.forEach((v) => { cu[v] = (cu[v] || 0) + 1; });
    const valores = Object.keys(cu).map(Number);
    const idx = (ok) => vals.map((v, i) => (ok(v) ? i : -1)).filter((i) => i >= 0);
    if (jug === 'generala' || jug === 'poker') {
      const hace = jug === 'generala' ? 5 : 4;
      const ok = valores.filter((v) => cu[v] >= hace);
      if (!ok.length) return null;
      const m = Math.max(...ok);
      return idx((v) => v === m);
    }
    if (jug === 'full') {
      const tr = valores.filter((v) => cu[v] >= 3).sort((a, b) => b - a);
      for (const a of tr) {
        const pa = valores.filter((v) => cu[v] >= 2 && v !== a);
        if (pa.length) { const b = Math.max(...pa); return idx((v) => v === a || v === b); }
      }
      return null;
    }
    const largo = nandu ? 4 : 5;
    for (let ini = 6 - largo + 1; ini >= 1; ini--) {
      let ok = true;
      for (let k = ini; k < ini + largo; k++) if (!cu[k]) ok = false;
      if (!ok) continue;
      let a = ini, b = ini + largo - 1;
      if (largo === 4) for (const i5 of [2, 1]) { let t = true; for (let k = i5; k < i5 + 5; k++) if (!cu[k]) t = false; if (t) { a = i5; b = i5 + 4; break; } }
      return idx((v) => v >= a && v <= b);
    }
    return null;
  }

  // c: { sobran, servida, fijados, ultima, numeros, jefe }. o: { real, rng, pasos }.
  // Devuelve { total, pts, mult, en } y, si o.pasos es una lista, le agrega cada paso para animarlo.
  function puntuar(S, vals, props, caras, jug, c, o) {
    o = o || {};
    const n = o.n || cuenta(S), fam = o.fam || familias(S), real = !!o.real, rng = o.rng || Math.random, pasos = o.pasos;
    const ef = o.ef || efectivas(S);
    let sc, pts, mult;
    if (NUM[jug]) { sc = vals.map((v, i) => (v === NUM[jug] ? i : -1)).filter((i) => i >= 0); pts = 0; mult = 1; }
    else {
      sc = patron(vals, jug, n.nandu > 0);
      if (!sc) return { total: 0, pts: 0, mult: 0, en: [] };
      pts = BASE[jug][0]; mult = BASE[jug][1];
      if (c.servida && !n.cola) mult += 5;
    }
    if (!sc.length) return { total: 0, pts: 0, mult: 0, en: [] };
    if (pasos) pasos.push({ t: 'base', pts, mult, txt: c.servida && !NUM[jug] && !n.cola ? 'SERVIDA' : '' });
    const dob = fam.S ? 2 : 1, crece = fam.A ? 2 : 1, su = Math.pow(2, n.naipe);
    const slots = (id) => ef.filter((e) => e.id === id).map((e) => e.k);
    let malditas = 0, plata = 0, hornero = S.hornero;
    const rotos = [];
    const prim = sc[0], ult = sc[sc.length - 1];
    for (const i of sc) {
      const v = vals[i], p = props[i];
      if ((v === 1 && n.azufre) || (v === 6 && c.jefe === 'seises')) { if (pasos) pasos.push({ t: 'nulo', i, pts, mult }); continue; }
      const veces = 1 + n.violin + (p.includes('doble') ? 1 : 0) + (i === prim || i === ult ? n.gilda : 0);
      for (let k = 0; k < veces; k++) {
        const luce = [];
        let fx = 1, mas = 0;
        pts += v <= 2 && n.tero ? 10 : v;
        if (v <= 2 && n.tero) luce.push(...slots('tero'));
        if (p.includes('hueso')) pts += 15;
        if (p.includes('brasa')) { mult += 4; mas += 4; }
        if (p.includes('dorada')) plata += 1;
        if (p.includes('semilla')) { pts += caras[i].s; if (real) caras[i].s += 2 * crece; }
        if (p.includes('hielo')) { mult *= 2; fx *= 2; if (real && rng() < Math.min(1, 0.25 * su)) rotos.push(caras[i]); }
        if (p.includes('maldita') || (v === 6 && n.azufre)) { mult *= 1.5; fx *= 1.5; malditas++; }
        if (v === 1 && n.sanlamuerte) { mult += 4 * dob * n.sanlamuerte; mas += 4 * dob * n.sanlamuerte; luce.push(...slots('sanlamuerte')); }
        if (n.hornero) { hornero += 3 * crece * n.hornero; luce.push(...slots('hornero')); }
        if (pasos) pasos.push({ t: 'dado', i, pts, mult, rep: k > 0, luce, fx, mas });
      }
    }
    let menos = 0;
    props.forEach((p, i) => { if (!sc.includes(i) && p.includes('maldita')) menos += 10; });
    if (menos) { pts -= menos; if (pasos) pasos.push({ t: 'base', pts, mult, txt: 'MALDITA AFUERA' }); }
    for (const e of ef) {
      const p0 = pts, m0 = mult;
      let txt = '';
      switch (e.id) {
        case 'gauchito': mult += (4 + 4 * malditas) * dob; break;
        case 'ceferino': pts += 20 * c.numeros; break;
        case 'luzmala': mult += 3 * c.sobran * dob; break;
        case 'taba': {
          const pr = Math.min(1, 0.5 * su);
          if (real) { if (rng() < pr) { mult += 10 * dob; txt = 'SUERTE'; } else txt = 'CULO'; } else mult += 10 * dob * pr;
          break;
        }
        case 'caja': mult += Math.max(0, Math.floor((S.plata + plata) / 2)) * dob; break;
        case 'nandu': if (jug === 'escalera') mult += 3 * dob; break;
        case 'llorona': mult += S.llorona * dob; break;
        case 'almamula': mult += S.almamula * dob; break;
        case 'mulita': pts += S.mulita; break;
        case 'hornero': pts += S.hornero; break;
        case 'lobizon': if (c.ultima) mult *= 3; break;
        case 'basilisco': mult *= Math.pow(1.5, c.fijados); break;
        case 'yarara': if (sc.every((i) => vals[i] % 2 === 0)) mult *= 2; break;
        case 'carancho': mult *= Math.pow(1.5, vals.length - sc.length); break;
        case 'firma': mult *= 4; break;
        default: break;
      }
      if (pasos && (pts !== p0 || mult !== m0 || txt)) pasos.push({ t: 'est', k: e.k, pts, mult, txt, veces: mult !== m0 && m0 > 0 && ['lobizon', 'basilisco', 'yarara', 'carancho', 'firma'].includes(e.id) });
    }
    if (fam.D) { mult *= 2; if (pasos) pasos.push({ t: 'base', pts, mult, txt: 'CONDENADO' }); }
    if (real) {
      S.plata += plata;
      S.hornero = hornero;
      if (NUM[jug]) S.mulita += 5 * crece * n.mulita;
      rotos.forEach((cara) => { cara.p = cara.p.filter((x) => x !== 'hielo'); });
    }
    pts = Math.max(0, pts);
    return { total: Math.round(pts * mult), pts, mult, en: sc, plata, rotos: rotos.length };
  }

  function variantes(v, props) {
    const com = [];
    props.forEach((p, i) => { if (p.includes('comodin')) com.push(i); });
    if (!com.length) return [v];
    const out = [];
    if (com.length <= 2) {
      const rec = (k, w) => { if (k === com.length) { out.push(w.slice()); return; } for (let x = 1; x <= 6; x++) { w[com[k]] = x; rec(k + 1, w); } };
      rec(0, v.slice());
    } else for (let x = 1; x <= 6; x++) { const w = v.slice(); com.forEach((i) => { w[i] = x; }); out.push(w); }
    return out;
  }

  // Puntaje de cada jugada con los dados como están (los comodines toman el mejor número para cada una).
  function vistaPrevia(S, vals, caras, c) {
    const { v, p, f } = vista(vals, caras);
    const o = { n: cuenta(S), fam: familias(S), ef: efectivas(S) };
    const vs = variantes(v, p), out = {};
    for (const j of JUGADAS) {
      let top = null;
      for (const w of vs) { const r = puntuar(S, w, p, f, j, c, o); if (!top || r.total > top.total) { top = r; top.vals = w; } }
      out[j] = top;
    }
    return out;
  }

  // Anota de verdad: aplica crecimientos y devuelve los pasos para animar.
  function anotar(S, vals, caras, jug, c, rng) {
    const { v, p, f } = vista(vals, caras);
    const previa = vistaPrevia(S, vals, caras, c)[jug];
    const pasos = [];
    const n = cuenta(S), crece = familias(S).A ? 2 : 1;
    const r = previa.total > 0 ? puntuar(S, previa.vals, p, f, jug, c, { real: true, rng, pasos }) : { total: 0, pts: 0, mult: 0, en: [] };
    if (r.total === 0) S.llorona += 2 * crece * n.llorona;
    for (let k = 0; k < n.naipe; k++) if (rng() < Math.min(1, Math.pow(2, n.naipe) / 3)) { S.plata += 1; r.naipe = (r.naipe || 0) + 1; }
    r.pasos = pasos;
    r.vals = previa.vals || v;
    return r;
  }

  function elegir(pozo, pesos, rng) {
    let tot = 0;
    pesos.forEach((w) => { tot += w; });
    let r = rng() * tot;
    for (let i = 0; i < pozo.length; i++) { r -= pesos[i]; if (r < 0) return i; }
    return pozo.length - 1;
  }
  function oferta(S, rng) {
    const pozo = Object.keys(ESTAMPITAS).filter((e) => ESTAMPITAS[e].fam !== 'D' && !tiene(S, e));
    const est = [];
    const cuantas = familias(S).P ? 4 : 3;
    for (let k = 0; k < cuantas && pozo.length; k++) {
      const i = elegir(pozo, pozo.map((e) => PESO[ESTAMPITAS[e].r]), rng);
      est.push(pozo.splice(i, 1)[0]);
    }
    const ids = Object.keys(CARAS), caras = [];
    while (caras.length < 2) { const c = ids[Math.floor(rng() * ids.length)]; if (!caras.includes(c)) caras.push(c); }
    return { est, caras };
  }
  function pactos(S, rng) {
    const pozo = Object.keys(ESTAMPITAS).filter((e) => ESTAMPITAS[e].fam === 'D' && !tiene(S, e));
    const out = [];
    while (out.length < 2 && pozo.length) out.push(pozo.splice(Math.floor(rng() * pozo.length), 1)[0]);
    return out;
  }
  const precioDe = (id) => (ESTAMPITAS[id] ? PRECIO[ESTAMPITAS[id].r] : CARAS[id].precio);
  function pegarCara(S, id, dado, valor) {
    const cara = S.dados[dado][valor - 1];
    if (!cara.p.includes(id)) cara.p.push(id);
    if (id === 'cargada') cara.w = 2;
  }
  // Plata al ganar una mesa: 8, más San Cayetano, más 3 por cada vez que la meta se multiplicó por 10.
  function premio(S, puntos, meta, sobrantes) {
    const n = cuenta(S);
    const pasada = puntos >= meta ? Math.floor(Math.log10(puntos / meta) + 1e-9) : 0;
    return { base: 8, cayetano: n.cayetano * sobrantes, pasada: 3 * pasada, salamanca: tiene(S, 'salamanca') ? -1 : 0 };
  }
  function azar(semilla) {
    let a = semilla >>> 0;
    return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }

  const R = { NUM, BASE, JUGADAS, METAS, JEFES, CARAS, ESTAMPITAS, PRECIO, FAMILIAS, nuevoEstado, efectivas, cuenta, familias, tiene,
    cuantosDados, suerte, tirosDelTurno, anotaciones, metaDe, tirar, vista, patron, puntuar, vistaPrevia, anotar, oferta, pactos,
    precioDe, pegarCara, premio, azar };
  if (typeof module !== 'undefined' && module.exports) module.exports = R;
  else raiz.Reglas = R;
})(typeof window !== 'undefined' ? window : globalThis);
