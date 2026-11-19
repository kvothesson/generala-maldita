# Generala maldita: resultados del simulador

8000 partidas en 576 segundos. Bot que compra al azar y mira un tiro hacia adelante.

## Hasta dónde llega

| Mesas ganadas | Partidas | % |
|---|---|---|
| 0 | 992 | 12.4 |
| 1 | 1310 | 16.4 |
| 2 | 1184 | 14.8 |
| 3 | 2095 | 26.2 |
| 4 | 1428 | 17.9 |
| 5 | 586 | 7.3 |
| 6 | 273 | 3.4 |
| 7 | 102 | 1.3 |
| 8 (ganó) | 30 | 0.4 |

- Partidas con al menos una mesa pasada por 10 veces la meta: 372 (4.7 %)
- Mejor mesa de cada partida, puntaje sobre meta: mediana 3.9, el 10 % de arriba pasa 7.9, máximo 89

## Estampitas

Ventaja = mesas ganadas de más frente a las partidas que llegaron a esa misma tienda. El ± es el error estándar.

| Estampita | Compras | Ventaja | ± |
|---|---|---|---|
| basilisco | 86 | +1.59 | 0.19 |
| firma | 543 | +1.21 | 0.06 |
| hornero | 566 | +0.87 | 0.08 |
| almamula | 537 | +0.73 | 0.09 |
| gauchito | 1423 | +0.55 | 0.03 |
| carancho | 566 | +0.49 | 0.06 |
| taba | 1467 | +0.48 | 0.03 |
| ceferino | 1456 | +0.20 | 0.03 |
| sanlamuerte | 557 | +0.17 | 0.05 |
| salamanca | 540 | +0.11 | 0.06 |
| mulita | 1488 | +0.08 | 0.04 |
| luzmala | 1389 | +0.07 | 0.03 |
| cola | 602 | +0.05 | 0.03 |
| violin | 589 | +0.04 | 0.05 |
| pombero | 1468 | +0.01 | 0.03 |
| tero | 1427 | -0.00 | 0.03 |
| azufre | 602 | -0.01 | 0.05 |
| yarara | 573 | -0.01 | 0.06 |
| ginebra | 1427 | -0.07 | 0.03 |
| sexto | 569 | -0.09 | 0.04 |
| gilda | 583 | -0.10 | 0.05 |
| nandu | 591 | -0.11 | 0.04 |
| llorona | 555 | -0.11 | 0.06 |
| lobizon | 549 | -0.16 | 0.05 |
| difunta | 1472 | -0.18 | 0.03 |
| fiado | 1444 | -0.21 | 0.03 |
| cayetano | 1425 | -0.24 | 0.03 |
| facon | 598 | -0.34 | 0.04 |
| naipe | 597 | -0.40 | 0.05 |
| caja | 590 | -0.42 | 0.05 |

## Caras

| Cara | Compras | Ventaja | ± |
|---|---|---|---|
| brasa | 2497 | +0.22 | 0.02 |
| hueso | 2805 | +0.11 | 0.02 |
| comodin | 1846 | +0.10 | 0.03 |
| maldita | 1850 | -0.06 | 0.03 |
| cargada | 2488 | -0.07 | 0.02 |
| hielo | 1656 | -0.08 | 0.03 |
| dorada | 2552 | -0.10 | 0.02 |
| inquieta | 2477 | -0.12 | 0.02 |
| semilla | 2019 | -0.17 | 0.02 |
| contagiosa | 1649 | -0.20 | 0.03 |
| doble | 1635 | -0.21 | 0.03 |
| espejo | 1463 | -0.22 | 0.03 |

## Pares de estampitas (25 partidas o más)

| Par | Partidas | Ventaja | ± |
|---|---|---|---|
| almamula + firma | 59 | +2.28 | 0.18 |
| firma + hornero | 66 | +2.22 | 0.17 |
| almamula + hornero | 37 | +2.10 | 0.35 |
| carancho + hornero | 46 | +2.08 | 0.20 |
| almamula + salamanca | 38 | +1.68 | 0.33 |
| almamula + carancho | 33 | +1.63 | 0.37 |
| gauchito + hornero | 126 | +1.54 | 0.12 |
| firma + gauchito | 123 | +1.44 | 0.10 |
| hornero + taba | 111 | +1.43 | 0.14 |
| firma + taba | 151 | +1.41 | 0.10 |
| gilda + hornero | 33 | +1.34 | 0.29 |
| hornero + salamanca | 39 | +1.31 | 0.30 |

Los peores:

| Par | Partidas | Ventaja | ± |
|---|---|---|---|
| cayetano + naipe | 96 | -0.56 | 0.09 |
| caja + cayetano | 82 | -0.57 | 0.10 |
| facon + nandu | 37 | -0.62 | 0.12 |
| caja + difunta | 95 | -0.64 | 0.10 |
| facon + lobizon | 28 | -0.68 | 0.13 |
| gilda + naipe | 34 | -0.70 | 0.11 |

## Supuestos

- Plata: empezás con 6 y cobrás 8 por mesa ganada, más lo que den los ítems y el premio por pasarse.
- Precios de estampita: común 4, rara 7, legendaria 10. Tienda: 3 estampitas y 2 caras.
- Pacto: después de las mesas 2, 4 y 6 el Mandinga ofrece 2 pactos gratis; el bot acepta uno 6 de cada 10 veces.
- Los jefes no tienen regla propia todavía: las mesas 4 y 8 son mesas comunes.
- Se juegan siempre todas las anotaciones de la mesa, aunque la meta ya esté pasada.
- El bot compra al azar lo que le alcanza (así se mide cada ítem sin el gusto del bot) y no vende.
- El bot pega las caras en su número favorito: el 1 si tiene San La Muerte o Tero, si no el 6.
- El bot decide qué fijar mirando un solo tiro hacia adelante. Un humano bueno juega mejor.
- Servida vale solo para escalera, full, póker y generala.
- Basilisco: si anotás sin volver a tirar, cuentan todos los dados como fijados.
