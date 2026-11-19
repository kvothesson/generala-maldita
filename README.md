# Generala maldita

Roguelike de dados en pixel art: jugás a la generala contra el Mandinga en una pulpería de madrugada. Ocho mesas, cada una con una meta de puntos. Entre mesa y mesa comprás estampitas de santos y aparecidos, pegás caras nuevas en tus dados y, si te animás, firmás pactos con el diablo. Las buenas partidas terminan con números ridículos.

Se juega en **https://kvothesson.com/generala-maldita/**. En la compu: `abrir.cmd` (servidor local en el puerto 5441).

## Cómo se juega

- **TIRAR** (o la barra espaciadora) tira los dados. Clic en un dado para fijarlo. Tenés 3 tiros por turno.
- **Clic en una fila de la libreta** para anotar. Cada fila muestra cuánto daría con los dados como están.
- El puntaje es **puntos × multiplicador**. Las estampitas se resuelven de izquierda a derecha: conviene sumar antes de multiplicar.
- **Clic en dos estampitas tuyas** las cambia de lugar. **VER DADOS** muestra los seis lados de cada dado.
- **M** apaga el sonido.
- **F** o el ícono de las esquinas pone pantalla completa.
- **En el celu** se juega de costado; si lo tenés derecho, el juego se gira solo. Para anotar, tocá la jugada una vez para ver cuánto da y otra para confirmar.

## Cómo está hecho

- **`reglas.js`**: las reglas puras, sin pantalla. `node sim/probar_reglas.js` las prueba contra las cuentas del diseño.
- **`index.html`**: la pantalla: el juego vive en 320×180 y el lienzo toma la forma de la pantalla, estirando los bordes del dibujo para que no queden franjas negras. Sin dependencias.
- **`arte/`**: los fondos y las 30 estampitas salen de código (`python arte/hoja.py`), con paleta cerrada y luz en escalones tramados. `arte/maqueta.py` dibuja los tres cuadros con los que se eligió la estética.
- **`DISENO.md`**: reglas, las 12 caras, las 30 estampitas y sus familias.
- **`sim/`**: un simulador en Python que juega miles de partidas para encontrar ítems rotos de más y problemas de plata. Los informes están en `sim/RESULTADOS.md`.
- **`metricas/`**: un Worker de Cloudflare con D1 que recibe eventos anónimos (sin datos personales): hasta qué mesa se llega, qué se compra y qué pactos se firman. En local no se mandan salvo que abras el juego con `?metricas`.

Hecho por [Kvothesson](https://kvothesson.com/).
