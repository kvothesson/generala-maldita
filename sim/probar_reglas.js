// Prueba que reglas.js dé las mismas cuentas que el diseño y que el simulador de Python.
//   node games/generala/sim/probar_reglas.js
const R = require('../reglas.js');
let fallas = 0;
function igual(nombre, a, b) {
  const ok = Math.abs(a - b) < 1e-6;
  if (!ok) fallas++;
  console.log((ok ? 'ok   ' : 'FALLA') + ' ' + nombre + ': ' + a + (ok ? '' : ' (esperado ' + b + ')'));
}
const ctx = (x) => Object.assign({ sobran: 0, servida: false, fijados: 0, ultima: false, numeros: 0 }, x);
const caras1 = (S) => [0, 1, 2, 3, 4].map((d) => S.dados[d][0]);

let S = R.nuevoEstado();
S.tengo = ['sanlamuerte', 'violin', 'lobizon', 'firma'];
let c = ctx({ fijados: 3, ultima: true });
igual('generala de unos del diseño', R.vistaPrevia(S, [1, 1, 1, 1, 1], caras1(S), c).generala.total, 32400);
for (let d = 0; d < 5; d++) R.pegarCara(S, 'brasa', d, 1);
igual('la misma con brasa', R.vistaPrevia(S, [1, 1, 1, 1, 1], caras1(S), c).generala.total, 61200);

S = R.nuevoEstado(); S.tengo = ['basilisco'];
const lisas = (S, vals) => vals.map((v, d) => S.dados[d][v - 1]);
igual('basilisco con full servido', R.vistaPrevia(S, [3, 3, 3, 2, 2], lisas(S, [3, 3, 3, 2, 2]), ctx({ servida: true, fijados: 5, sobran: 2 })).full.total, Math.round(43 * 7 * Math.pow(1.5, 5)));

S = R.nuevoEstado();
igual('escalera sin ñandú no sale con 4', R.vistaPrevia(S, [1, 2, 3, 4, 6], lisas(S, [1, 2, 3, 4, 6]), ctx()).escalera.total, 0);
S.tengo = ['nandu'];
igual('escalera con ñandú', R.vistaPrevia(S, [1, 2, 3, 4, 6], lisas(S, [1, 2, 3, 4, 6]), ctx()).escalera.total, (20 + 10) * 5);

S = R.nuevoEstado(); S.tengo = ['salamanca', 'firma'];
igual('salamanca copia a la firma', R.vistaPrevia(S, [6, 6, 6, 6, 6], lisas(S, [6, 6, 6, 6, 6]), ctx()).generala.total, 80 * 5 * 16);
S.tengo = ['firma', 'salamanca'];
igual('salamanca al final no copia nada', R.vistaPrevia(S, [6, 6, 6, 6, 6], lisas(S, [6, 6, 6, 6, 6]), ctx()).generala.total, 80 * 5 * 4);

S = R.nuevoEstado(); R.pegarCara(S, 'comodin', 4, 2);
igual('comodín completa la generala', R.vistaPrevia(S, [5, 5, 5, 5, 2], lisas(S, [5, 5, 5, 5, 2]), ctx()).generala.total, 75 * 5);

S = R.nuevoEstado();
igual('jefe: los seises no valen', R.vistaPrevia(S, [6, 6, 6, 2, 2], lisas(S, [6, 6, 6, 2, 2]), ctx({ jefe: 'seises' })).full.total, 34 * 2);

S = R.nuevoEstado(); S.tengo = ['hornero'];
const rng = R.azar(7);
let r = R.anotar(S, [4, 4, 4, 1, 2], lisas(S, [4, 4, 4, 1, 2]), 'cuatros', ctx(), rng);
igual('hornero: primera jugada no suma', r.total, 12);
igual('hornero: guarda 9', S.hornero, 9);
r = R.anotar(S, [4, 4, 4, 1, 2], lisas(S, [4, 4, 4, 1, 2]), 'cuatros', ctx(), rng);
igual('hornero: la segunda suma 9 una vez', r.total, 21);
igual('pasos para animar', r.pasos.length, 5);

// una partida al azar entera, para ver que nada rompa
const g = R.azar(42);
S = R.nuevoEstado();
let mesas = 0;
for (let m = 0; m < 8; m++) {
  let puntos = 0; const usadas = [];
  for (let a = 0; a < R.anotaciones(S); a++) {
    const nd = R.cuantosDados(S);
    const caras = S.dados.slice(0, nd).map((d) => R.tirar(d, g));
    const vals = caras.map((x) => x.v);
    const pv = R.vistaPrevia(S, vals, caras, ctx({ sobran: 2, servida: true, fijados: nd }));
    const j = R.JUGADAS.filter((x) => !usadas.includes(x)).sort((x, y) => pv[y].total - pv[x].total)[0];
    puntos += R.anotar(S, vals, caras, j, ctx({ sobran: 2, servida: true, fijados: nd }), g).total; usadas.push(j);
  }
  if (puntos < R.metaDe(S, m)) break;
  mesas++;
  const of = R.oferta(S, g);
  of.est.forEach((e) => { if (S.tengo.length < 5) S.tengo.push(e); });
  of.caras.forEach((x) => R.pegarCara(S, x, Math.floor(g() * 5), 6));
  R.pactos(S, g);
}
console.log('partida al azar sin errores, mesas ganadas: ' + mesas + ', estampitas: ' + S.tengo.join(' '));
console.log(fallas ? fallas + ' FALLAS' : 'todo ok');
process.exit(fallas ? 1 : 0);
