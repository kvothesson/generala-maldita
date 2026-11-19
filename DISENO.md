# Generala maldita: diseño

Roguelike de dados. Jugás a la generala contra el Mandinga en una pulpería. Primera tanda: reglas de puntaje, 12 caras y 30 estampitas. Los números son de partida y se ajustan jugando.

## Lo que manda: sentirse roto

Una buena partida tiene que terminar con números ridículos. Para eso:

1. **Nada tiene tope.** Ni el multiplicador, ni los tiros, ni las repeticiones.
2. **Los × se multiplican entre sí.** Dos estampitas de ×3 dan ×9, no ×6.
3. **Las repeticiones repiten todo.** Si un dado vuelve a puntuar, vuelve a disparar su cara y cada estampita que lo mira.
4. **Pasarse paga.** Cada vez que el puntaje de la mesa multiplica por 10 la meta, +3 de plata. Estar roto te hace más roto.
5. **Se ve.** El multiplicador sube número por número en pantalla, la luz del farol crece con él y, si pasás la meta ×10, la mesa se prende fuego.
6. **Las metas crecen más rápido que una partida normal.** Sin combo no se llega a la mesa 5. Con combo, la mesa 8 se pasa de un tiro.

## Reglas

- 5 dados, 3 tiros por turno. Entre tiros fijás los que quieras.
- Cada mesa tiene **4 anotaciones**. Cada jugada se anota una sola vez por mesa. La libreta se limpia al cambiar de mesa.
- 8 mesas. La 4 y la 8 son jefes con una regla tramposa.
- Entre mesas, tienda. Cada tanto, un pacto con el Mandinga o un altar.

### Puntaje

`puntaje = puntos × multiplicador`

| Jugada | Puntos base | Mult base |
|---|---|---|
| Unos a seises | suma de esos dados | 1 |
| Escalera | 20 | 2 |
| Full | 30 | 2 |
| Póker | 40 | 3 |
| Generala | 50 | 5 |

Servida (sale en el primer tiro): +5 al mult.

### Orden en que se resuelve

1. Cada dado que puntúa, de izquierda a derecha: suma su número a los puntos y dispara su cara.
2. Cada estampita, de izquierda a derecha.

El orden importa: conviene sumar mult antes de multiplicarlo. Ordenar las estampitas es parte de jugar bien.

### Perillas

Todo ítem toca alguna de estas seis: **puntos, mult, tiros, anotaciones, plata, suerte**. La suerte multiplica toda probabilidad escrita en un ítem.

### Metas

| Mesa | 1 | 2 | 3 | 4 (jefe) | 5 | 6 | 7 | 8 (jefe) |
|---|---|---|---|---|---|---|---|---|
| Meta | 80 | 220 | 600 | 2.000 | 5.000 | 12.000 | 30.000 | 80.000 |

Sin ítems una mesa buena da unos 250 puntos.

### Plata

Empezás con 6 y cobrás 8 por cada mesa ganada, más lo que den los ítems y el premio por pasarse.

## Las 12 caras

Cada cara comprada se pega en ese número en dos dados que elijas. Las propiedades se suman: una cara puede tener más de una si le pegás otra encima con un altar.

| # | Cara | Qué hace | Precio |
|---|---|---|---|
| 1 | Hueso viejo | +15 puntos al puntuar | 2 |
| 2 | Brasa | +4 mult al puntuar | 3 |
| 3 | Dorada | +1 de plata al puntuar | 3 |
| 4 | Cargada | Ese lado sale el doble de veces | 3 |
| 5 | Inquieta | Una vez por turno la volvés a tirar sin gastar tiro | 3 |
| 6 | Semilla | Gana +2 puntos para siempre cada vez que puntúa | 4 |
| 7 | Comodín | Vale el número que más te convenga | 5 |
| 8 | Maldita | ×1,5 mult al puntuar. Si queda fuera de la jugada, −10 puntos | 5 |
| 9 | Doble | Puntúa dos veces | 6 |
| 10 | Contagiosa | Al fijarla, el dado de su derecha toma su número | 6 |
| 11 | De hielo | ×2 mult al puntuar. 1 en 4 de romperse y volver a ser común | 6 |
| 12 | Espejo | Copia el número y las propiedades del dado de su izquierda | 7 |

## Las 30 estampitas

Cinco familias de seis. Llevás hasta 5 a la vez. Rareza: C común, R rara, L legendaria.

### Santos (seguros: mult parejo y red de contención)

| # | Estampita | R | Qué hace |
|---|---|---|---|
| 1 | Gauchito Gil | C | +4 mult. +4 más por cada cara maldita que puntúe |
| 2 | San La Muerte | R | Cada 1 que puntúa da +4 mult |
| 3 | Difunta Correa | C | El primer turno de cada mesa tiene +2 tiros |
| 4 | San Cayetano | C | Al cerrar la mesa, +1 de plata por cada tiro que no usaste |
| 5 | Gilda | R | El primer y el último dado de la jugada vuelven a puntuar |
| 6 | Ceferino | C | +20 puntos por cada jugada de número (unos a seises) ya anotada en la mesa |

### Aparecidos (riesgo y crecimiento)

| # | Estampita | R | Qué hace |
|---|---|---|---|
| 7 | Luz Mala | C | +3 mult por cada tiro que te sobre al anotar |
| 8 | Lobizón | R | ×3 mult en la última anotación de cada mesa |
| 9 | Pombero | C | Una vez por turno das vuelta un dado (el 1 pasa a 6, el 2 a 5, el 3 a 4) |
| 10 | Llorona | R | Gana +2 mult para siempre cada vez que tachás una jugada con 0 |
| 11 | Almamula | R | Gana +2 mult para siempre cada vez que volvés a tirar los 5 dados juntos |
| 12 | Basilisco | L | ×1,5 mult por cada dado que fijaste en el primer tiro |

### Pulpería (plata y manejo de los dados)

| # | Estampita | R | Qué hace |
|---|---|---|---|
| 13 | Ginebra | C | +1 tiro por turno |
| 14 | La Taba | C | Al anotar tirás la taba: 1 en 2 de sumar +10 mult |
| 15 | El Fiado | C | Podés quedar debiendo hasta 10 de plata |
| 16 | Caja del pulpero | R | +1 mult por cada 2 de plata que tengas |
| 17 | Naipe marcado | R | Tu suerte se duplica. Además, al anotar, 1 en 3 de pagar 1 de plata |
| 18 | Facón | R | Una vez por mesa podés anotar una jugada que ya anotaste |

### Pampa (puntos y jugadas chicas)

| # | Estampita | R | Qué hace |
|---|---|---|---|
| 19 | Tero | C | Los 1 y los 2 valen 10 puntos cada uno |
| 20 | Mulita | C | Gana +5 puntos para siempre cada vez que anotás una jugada de número |
| 21 | Hornero | R | Gana +3 puntos para siempre por cada dado que puntúa. Lo guardado suma una vez por jugada |
| 22 | Ñandú | R | La escalera se arma con 4 dados y da +3 mult |
| 23 | Yarará | R | ×2 mult si todos los dados que puntúan son pares |
| 24 | Carancho | R | ×1,5 mult por cada dado que queda fuera de la jugada |

### Pactos (solo del Mandinga: rompen las reglas y cobran)

| # | Estampita | R | Qué hace | Qué cobra |
|---|---|---|---|---|
| 25 | La Firma | L | ×4 mult | Una anotación menos por mesa |
| 26 | El Sexto | L | Tirás 6 dados y puntúan los 6 | Un tiro menos por turno |
| 27 | Salamanca | L | Copia a la estampita de su derecha | 1 de plata por mesa |
| 28 | Violín del diablo | R | Todos los dados vuelven a puntuar una vez | Las metas suben un 25% |
| 29 | Azufre | R | Todos tus 6 cuentan como malditos | Los 1 no puntúan |
| 30 | Cola del diablo | R | No hay tiros: tirás una vez y después girás dados de a +1, hasta 6 giros por turno | No hay servida |

### Juntar tres de una familia

| Familia | Transformación | Premio |
|---|---|---|
| Santos | Santuario | Tus +mult de estampita valen el doble |
| Aparecidos | Noche cerrada | Todo lo que crece para siempre crece el doble |
| Pulpería | Parroquiano | Un producto más en la tienda y cambiar la oferta es gratis |
| Pampa | Baqueano | Una anotación más por mesa |
| Pactos | Condenado | ×2 mult al final. No podés vender estampitas |

## Cómo se reparte la tanda

| Qué toca | Cuántas | Cuáles |
|---|---|---|
| + puntos | 4 | Ceferino, Tero, Mulita, Hornero |
| + mult | 8 | Gauchito, San La Muerte, Luz Mala, Taba, Caja, Ñandú, Llorona, Almamula |
| × mult | 6 | Lobizón, Basilisco, Yarará, Carancho, La Firma, Azufre |
| Repetir y copiar | 3 | Gilda, Violín, Salamanca |
| Tiros y manejo | 5 | Difunta, Ginebra, Pombero, Facón, Naipe marcado |
| Plata | 2 | San Cayetano, El Fiado |
| Cambio de regla | 2 | El Sexto, Cola del diablo |

## Cuentas de una partida rota

Mesa 5, meta 5.000. Estampitas en orden: San La Muerte, Violín del diablo, Lobizón, La Firma. Última anotación: generala de unos.

| Paso | Puntos | Mult |
|---|---|---|
| Generala base | 50 | 5 |
| 5 unos puntúan, cada uno +1 punto y +4 mult por San La Muerte | 55 | 25 |
| Violín: los 5 vuelven a puntuar | 60 | 45 |
| Lobizón ×3 | 60 | 135 |
| La Firma ×4 | 60 | 540 |

**60 × 540 = 32.400**, más de cinco veces la meta de 6.250 (5.000 más el 25% del Violín). Si a esos unos les pegás cara Brasa, cada uno suma +8 mult por pasada en vez de +4 y la misma jugada da 60 × 1.020 = 61.200, casi diez veces la meta.

## Combos que deberían aparecer solos

- **Unos del diablo:** San La Muerte + Tero + cara Cargada en los unos. Choca con Azufre, que es la gracia: hay que elegir.
- **Piedra:** Basilisco + Ginebra + Contagiosa. Fijás los 5 de entrada y multiplicás ×7,6.
- **Carroñero:** Carancho + jugadas de número. Puntúa un solo dado y los otros cuatro dan ×5.
- **Banquero:** Caja del pulpero + San Cayetano + caras Doradas. La plata se vuelve mult.
- **Timbero:** La Taba + Naipe marcado + caras De hielo. Con suerte doble la taba siempre cae bien.
- **Seis de seis:** El Sexto + Violín + Gilda. Doce o más puntuaciones por jugada.

## Ajustes tras simular

Primera tanda de 8.000 partidas (`sim/RESULTADOS_v1.md`): Hornero roto de más, la mitad de las partidas moría antes de la segunda tienda, la plata no alcanzaba para raras y las caras caras no rendían. De ahí salen las metas iniciales más bajas, la plata, las caras en dos dados y los cambios a Hornero, Caja y Naipe.

## Falta

- Reglas de los jefes y lista de pactos y altares.
- Segunda tanda hasta 60 estampitas.
- Probarlo: un simulador que juegue miles de partidas para ver qué combos rompen de más y cuáles no se usan.
