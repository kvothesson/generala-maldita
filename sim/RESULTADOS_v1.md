# Generala maldita: resultados del simulador

8000 partidas en 268 segundos. Bot que compra al azar y mira un tiro hacia adelante.

## Hasta dónde llega

| Mesas ganadas | Partidas | % |
|---|---|---|
| 0 | 1177 | 14.7 |
| 1 | 2857 | 35.7 |
| 2 | 2043 | 25.5 |
| 3 | 982 | 12.3 |
| 4 | 312 | 3.9 |
| 5 | 147 | 1.8 |
| 6 | 172 | 2.1 |
| 7 | 175 | 2.2 |
| 8 (ganó) | 135 | 1.7 |

- Partidas con al menos una mesa pasada por 10 veces la meta: 162 (2.0 %)
- Mejor mesa de cada partida, puntaje sobre meta: mediana 2.7, el 10 % de arriba pasa 5.9, máximo 113

## Estampitas

Ventaja = mesas ganadas de más frente a las partidas que llegaron a esa misma tienda. El ± es el error estándar.

| Estampita | Compras | Ventaja | ± |
|---|---|---|---|
| hornero | 707 | +2.85 | 0.09 |
| basilisco | 6 | +1.73 | 0.69 |
| gauchito | 756 | +0.93 | 0.06 |
| firma | 428 | +0.75 | 0.08 |
| taba | 769 | +0.64 | 0.06 |
| cola | 398 | +0.36 | 0.09 |
| violin | 473 | +0.20 | 0.09 |
| luzmala | 755 | +0.17 | 0.06 |
| ceferino | 838 | +0.16 | 0.05 |
| pombero | 781 | +0.13 | 0.06 |
| sexto | 432 | +0.11 | 0.08 |
| azufre | 471 | +0.10 | 0.07 |
| carancho | 216 | +0.05 | 0.10 |
| nandu | 219 | +0.00 | 0.09 |
| salamanca | 435 | -0.01 | 0.07 |
| almamula | 205 | -0.03 | 0.13 |
| tero | 798 | -0.04 | 0.05 |
| mulita | 781 | -0.07 | 0.05 |
| yarara | 194 | -0.10 | 0.11 |
| fiado | 796 | -0.10 | 0.06 |
| ginebra | 794 | -0.10 | 0.05 |
| sanlamuerte | 196 | -0.18 | 0.10 |
| difunta | 807 | -0.20 | 0.05 |
| cayetano | 796 | -0.22 | 0.05 |
| gilda | 226 | -0.22 | 0.09 |
| lobizon | 209 | -0.25 | 0.09 |
| llorona | 204 | -0.37 | 0.11 |
| facon | 217 | -0.53 | 0.07 |
| naipe | 236 | -0.53 | 0.07 |
| caja | 199 | -0.55 | 0.07 |

## Caras

| Cara | Compras | Ventaja | ± |
|---|---|---|---|
| brasa | 1266 | +0.15 | 0.04 |
| comodin | 920 | +0.04 | 0.05 |
| hueso | 1747 | -0.02 | 0.04 |
| maldita | 916 | -0.02 | 0.05 |
| cargada | 1262 | -0.07 | 0.04 |
| inquieta | 1236 | -0.09 | 0.04 |
| dorada | 1248 | -0.10 | 0.04 |
| semilla | 1008 | -0.19 | 0.04 |
| hielo | 605 | -0.28 | 0.05 |
| contagiosa | 603 | -0.30 | 0.05 |
| espejo | 464 | -0.39 | 0.05 |
| doble | 588 | -0.39 | 0.05 |

## Pares de estampitas (25 partidas o más)

| Par | Partidas | Ventaja | ± |
|---|---|---|---|
| hornero + violin | 110 | +2.95 | 0.18 |
| gauchito + hornero | 150 | +2.71 | 0.15 |
| cola + hornero | 102 | +2.69 | 0.16 |
| hornero + luzmala | 107 | +2.52 | 0.17 |
| hornero + taba | 145 | +2.40 | 0.17 |
| firma + hornero | 96 | +2.27 | 0.20 |
| carancho + hornero | 27 | +2.25 | 0.24 |
| gilda + hornero | 32 | +2.22 | 0.28 |
| hornero + yarara | 26 | +2.15 | 0.38 |
| hornero + sexto | 113 | +2.10 | 0.17 |
| hornero + pombero | 140 | +2.06 | 0.16 |
| fiado + hornero | 147 | +1.94 | 0.16 |

Los peores:

| Par | Partidas | Ventaja | ± |
|---|---|---|---|
| ceferino + difunta | 109 | -0.44 | 0.11 |
| difunta + ginebra | 93 | -0.46 | 0.10 |
| salamanca + tero | 69 | -0.47 | 0.12 |
| cayetano + salamanca | 63 | -0.50 | 0.14 |
| cayetano + tero | 78 | -0.56 | 0.12 |
| ginebra + mulita | 95 | -0.58 | 0.09 |

## Supuestos

- Plata: empezás con 4 y cobrás 5 por mesa ganada, más lo que den los ítems y el premio por pasarse.
- Precios de estampita: común 4, rara 7, legendaria 10. Tienda: 3 estampitas y 2 caras.
- Pacto: después de las mesas 2, 4 y 6 el Mandinga ofrece 2 pactos gratis; el bot acepta uno 6 de cada 10 veces.
- Los jefes no tienen regla propia todavía: las mesas 4 y 8 son mesas comunes.
- Se juegan siempre todas las anotaciones de la mesa, aunque la meta ya esté pasada.
- El bot compra al azar lo que le alcanza (así se mide cada ítem sin el gusto del bot) y no vende.
- El bot pega las caras en su número favorito: el 1 si tiene San La Muerte o Tero, si no el 6.
- El bot decide qué fijar mirando un solo tiro hacia adelante. Un humano bueno juega mejor.
- Servida vale solo para escalera, full, póker y generala.
- Basilisco: si anotás sin volver a tirar, cuentan todos los dados como fijados.
