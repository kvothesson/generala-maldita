CREATE TABLE IF NOT EXISTS eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT DEFAULT (datetime('now')),
  ev TEXT NOT NULL,          -- inicio, mesa, gano, perdio, compra, pacto, llamas, pulso, salida
  jugador TEXT NOT NULL,     -- número al azar guardado en el navegador, sin datos personales
  seg INTEGER,               -- segundos jugados en esa partida
  mesa INTEGER,              -- mesa en la que estaba (1 a 8)
  puntos INTEGER,            -- mejor jugada de la partida
  movil INTEGER,             -- 1 si es celular
  extra TEXT,                -- estampitas que llevaba, lo que compró, el pacto o el número de partida
  pais TEXT                  -- país según Cloudflare
);
CREATE INDEX IF NOT EXISTS ev_idx ON eventos(ev);
CREATE INDEX IF NOT EXISTS jug_idx ON eventos(jugador);
