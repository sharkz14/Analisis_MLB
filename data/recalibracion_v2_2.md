# Recalibración v2.2 — conteo periódico

Ventana: 11/05/26 → 07/06/26 (24 partidos nuevos desde el cierre de v2.1).
Disparador: ~25 partidos / Protocolo Operativo Parte 3.
Fuente: bloques en MLB_Postmortems_Raw + 4 entradas fuera del raw.

NOTA METODOLÓGICA: a diferencia de la ventana original del raw (14 partidos
escritos con sesgo a errores), esta ventana se construyó con análisis
pre-partido reales y postmortems disciplinados. El sesgo de selección es
mucho menor, por lo que los conteos son más confiables.


## 1. CONTEO AGREGADO

### Clasificación JUGADA (lo realmente apostado / decidido)

| Clasificación      | Count | %    |
|--------------------|------:|-----:|
| PASS_CORRECTO      |     8 | 33%  |
| ACIERTO_LIMPIO     |     6 | 25%  |
| PASS_INCORRECTO    |     6 | 25%  |
| ERROR_DE_MERCADO   |     2 |  8%  |
| NO_JUGADA          |     2 |  8%  |
| ERROR_DE_LECTURA   |     0 |  0%  |
| ACIERTO_RUIDOSO    |     0 |  0%  |
| VARIANZA           |     0 |  0%  |
| **Total**          | **24**|      |

Desglose de "apostó vs no apostó":
- Apuestas tomadas: 8 (33%) — 6 ACIERTO_LIMPIO + 2 ERROR_DE_MERCADO
- Pass / no jugado: 16 (67%) — 8 PASS_CORRECTO + 6 PASS_INCORRECTO + 2 NO_JUGADA

Cuando SÍ se apostó: 6 de 8 fueron ACIERTO_LIMPIO (75% por proceso). 0 errores
de lectura ejecutados. Las apuestas tomadas son de muy alta calidad.

Cuando se pasó: 8 correctos / 6 incorrectos / 2 sin EV claro = 50% de los pass
con EV dejado en la mesa.


### Clasificación ANALÍTICA (frame del análisis, separado del resultado)

| Clasificación      | Count | %    |
|--------------------|------:|-----:|
| ACIERTO_LIMPIO     |     9 | 38%  |
| ERROR_DE_LECTURA   |     8 | 33%  |
| ERROR_DE_MERCADO   |     5 | 21%  |
| PASS_INCORRECTO    |     1 |  4%  |
| ACIERTO_RUIDOSO    |     1 |  4%  |
| **Total**          | **24**|      |

(2 partidos con dimensión analítica mixta —tigers-rays-010626 y
brewers-rockies-060626— contados por su componente dominante ERROR_DE_LECTURA.)


## 2. LECTURA DEL CONTEO (reglas del template)

### Hallazgo 1 — El problema se DESPLAZÓ de traducción a lectura

- Ventana raw original (14p): ERROR_DE_MERCADO 9 > ERROR_DE_LECTURA 4.
  → problema de TRADUCCIÓN. (motivó v2.1, que refinó mercados.)
- Ventana nueva (24p): ERROR_DE_LECTURA 8 > ERROR_DE_MERCADO 5.
  → problema de ANÁLISIS PRE-PARTIDO.

Implicación per la regla del template: v2.2 no debe enfocarse en refinar
mercados (eso ya lo hizo v2.1) sino en mejorar el proceso de lectura
pre-partido. Tiene sentido: v2.1 cerró la mayoría de los huecos de traducción,
así que el error residual migró a la fuente.

### Hallazgo 2 — El leak dominante es de EJECUCIÓN, no de análisis

6 PASS_INCORRECTO de 24 (25%). En todos, el análisis identificó el edge o el
menú tenía picks ganadoras claras, pero no se apostó. Sumado al cluster del
filtro de selección (10 casos donde una pick de cuota >1.80 que capturaba el
edge top se descartó o no se ejecutó), este es el agujero más caro y más
consistente del run.

Contraste revelador:
- Apuestas tomadas: ROI por proceso altísimo (6/8 limpias).
- Pass: 6 de 16 dejaron EV claro.
→ El problema NO es que se apueste mal; es que se apuesta POCO y se descartan
  picks correctas. El sistema de análisis funciona; el cuello de botella es
  la decisión de ejecutar.

### Hallazgo 3 — Las apuestas tomadas validan el framework

Los 6 ACIERTO_LIMPIO jugados comparten perfil:
- 4 son TT del equipo fuerte / over de carreras (giants-ath, giants-dbacks,
  dodgers-dbacks 03/06, white-sox-phillies hipotético).
- 2 son props de bate top / pitcher en spot aislado (marlins-rays SB,
  rockies-angels Freeland ER, pirates-braves Olson H+R+RBI).
Ninguno es ML caro, run line agresiva, ni under apoyado solo en clima.
→ La regla operativa emergente: cuando el edge es ofensivo unilateral → TT
  del fuerte; cuando es defensivo/matchup → prop aislada del pitcher/bate.


## 3. ORDEN PROPUESTO PARA EL TRABAJO CLUSTER-POR-CLUSTER

A) Promociones de regla operativa (alta evidencia, listas):
   1. Filtro de selección → de "gatillo duro" a regla primaria (10 casos)
   2. Alerta espejada Patrón 4 → de alerta a regla primaria (8 casos)
   3. Meta-regla "tier alto > tier bajo en inversiones" (3 casos)

B) Refinamientos a patrones existentes (evidencia media-alta):
   4. Patrón 11 — "run environment ≠ camino del daño" (6 casos)
   5. Patrón 1 — sub-tipos (Tipo B atenuado, post-IL, matchup-relativo, etc.)
   6. Patrón 3 — granularidad de bullpen + "timing > precio"

C) Candidatos a patrón NUEVO (decidir promoción / fusión):
   7. "Señal head-to-head específica > perfil promedio" (4 casos)
   8. "Manufactura sin HR" + "slugging por aire" (3+3, ¿fusión?)
   9. "Planes de pitcheo no estándar" (bullpen games + escudo de bulk, 3 casos)
  10. Resto n=1-2 → mantener en watchlist


## (pendiente) Decisiones por cluster — se completa en la siguiente fase
