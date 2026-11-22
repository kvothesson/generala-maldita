// Métricas de Generala maldita: recibe eventos anónimos del juego y los guarda en D1.
// Eventos: inicio {n° de partida}, mesa {estampitas}, gano {estampitas}, perdio {estampitas}, compra {id}, pacto {id o rechazo},
// llamas {puntos}, pulso (cada minuto jugado), salida.
// GET /resumen?clave=  → JSON con los totales.  El tablero se arma en la PC (taller: tablero/).
// Las fechas se muestran en hora argentina (UTC-3); D1 guarda en UTC.
const EVENTOS = ['inicio', 'mesa', 'gano', 'perdio', 'compra', 'pacto', 'llamas', 'pulso', 'salida'];

export default {
  async fetch(req, env) {
    const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'content-type' };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    const url = new URL(req.url);
    if (req.method === 'POST' && url.pathname === '/evento') {
      let d;
      try { d = JSON.parse(await req.text()); } catch { return new Response('mal', { status: 400, headers: cors }); }
      if (!EVENTOS.includes(d.ev) || typeof d.id !== 'string' || d.id.length > 40) return new Response('mal', { status: 400, headers: cors });
      await env.DB.prepare('INSERT INTO eventos (ev, jugador, seg, mesa, puntos, movil, extra, pais) VALUES (?,?,?,?,?,?,?,?)')
        .bind(d.ev, d.id, Math.min(d.seg | 0, 864000), Math.min(Math.max(d.mesa | 0, 0), 8), Math.min(Math.max(Number(d.puntos) || 0, 0), 9e15),
          d.movil ? 1 : 0, String(d.extra ?? '').slice(0, 80), req.cf?.country || '')
        .run();
      return new Response('ok', { headers: cors });
    }
    const conClave = env.CLAVE && url.searchParams.get('clave') === env.CLAVE;
    if (url.pathname === '/resumen' && conClave) {
      return new Response(JSON.stringify(await resumen(env), null, 2), { headers: { 'content-type': 'application/json; charset=utf-8' } });
    }
    return new Response('Generala maldita · métricas', { headers: cors });
  },
};

const AR = "'-3 hours'";
async function resumen(env) {
  const q = s => env.DB.prepare(s).all().then(r => r.results);
  return {
    jugadores: await q("SELECT COUNT(DISTINCT jugador) n FROM eventos WHERE ev='inicio'"),
    partidas: await q("SELECT COUNT(*) n FROM eventos WHERE ev='inicio'"),
    por_dia: await q(`SELECT date(ts, ${AR}) dia, COUNT(DISTINCT jugador) jugadores, COUNT(CASE WHEN ev='inicio' THEN 1 END) partidas, COUNT(DISTINCT CASE WHEN ev='gano' THEN jugador END) ganaron FROM eventos GROUP BY dia ORDER BY dia DESC LIMIT 30`),
    por_hora: await q(`SELECT strftime('%Y-%m-%d %H', ts, ${AR}) hora, COUNT(DISTINCT jugador) jugadores, COUNT(DISTINCT CASE WHEN movil=1 THEN jugador END) celu FROM eventos WHERE ts >= datetime('now','-48 hours') GROUP BY hora ORDER BY hora`),
    // un pulso por minuto jugado: minutos por persona = pulsos de esa persona
    minutos: await q("SELECT ROUND(AVG(m),1) promedio, MAX(m) maximo FROM (SELECT jugador, COUNT(CASE WHEN ev='pulso' THEN 1 END) m FROM eventos GROUP BY jugador)"),
    partidas_por_jugador: await q("SELECT ROUND(AVG(n),1) promedio, MAX(n) maximo FROM (SELECT jugador, COUNT(*) n FROM eventos WHERE ev='inicio' GROUP BY jugador)"),
    // cada mesa ganada manda un evento 'mesa' (la 8 manda 'gano'): sirve aunque cierren la pestaña a mitad
    mesas_ganadas: await q("SELECT mesa, COUNT(*) n FROM eventos WHERE ev='mesa' GROUP BY mesa"),
    victorias: await q("SELECT COUNT(*) n FROM eventos WHERE ev='gano'"),
    perdidas: await q("SELECT mesa, COUNT(*) n FROM eventos WHERE ev='perdio' GROUP BY mesa ORDER BY mesa"),
    mejor_jugada: await q("SELECT MAX(puntos) maximo FROM eventos"),
    llamas: await q("SELECT COUNT(*) veces, COUNT(DISTINCT jugador) jugadores FROM eventos WHERE ev='llamas'"),
    compras: await q("SELECT extra id, COUNT(*) veces FROM eventos WHERE ev='compra' GROUP BY extra ORDER BY veces DESC"),
    pactos: await q("SELECT extra id, COUNT(*) veces FROM eventos WHERE ev='pacto' GROUP BY extra ORDER BY veces DESC"),
    ganadoras: await q("SELECT extra FROM eventos WHERE ev='gano' ORDER BY id DESC LIMIT 200"),
    celular: await q("SELECT movil, COUNT(DISTINCT jugador) jugadores FROM eventos GROUP BY movil"),
    paises: await q("SELECT pais, COUNT(DISTINCT jugador) jugadores FROM eventos GROUP BY pais ORDER BY jugadores DESC LIMIT 10"),
    ultimo: await q(`SELECT datetime(MAX(ts), ${AR}) ts FROM eventos`),
  };
}
