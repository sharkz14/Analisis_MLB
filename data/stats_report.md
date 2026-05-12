# MLB Postmortems — Reporte de recalibración

Dataset: **29 partidos**. Fuente: `data/postmortems.yaml`.

## 1. Resumen de decisiones

**Clasificación jugada** (lo realmente apostado):

| Clasificación | Count | % |
|---|---:|---:|
| ACIERTO_LIMPIO | 9 | 31% |
| PASS_CORRECTO | 7 | 24% |
| PASS_INCORRECTO | 6 | 21% |
| ERROR_DE_LECTURA | 4 | 14% |
| ERROR_DE_MERCADO | 2 | 7% |
| VARIANZA | 1 | 3% |

**Clasificación analítica** (frame del análisis):

| Clasificación | Count | % |
|---|---:|---:|
| ERROR_DE_MERCADO | 15 | 52% |
| ACIERTO_LIMPIO | 8 | 28% |
| ERROR_DE_LECTURA | 6 | 21% |

## 2. Apostar vs pasar

- Apuestas tomadas: **16** (55%)
- Pass: **13** (45%)

- Pass correctos: **7/13** (54%)
- Pass incorrectos: **6/13** (46%)

## 3. Win rate y P&L de apuestas reales

- Total apuestas/piernas: **17**
- Ganadas: **10** (59%)
- Perdidas: 7 (41%)
- Push: 0
  - Piernas de parlay: 7 cobraron / 2 perdieron

- **P&L estimado** (singles, 1u flat): **-3.00u** en 8 apuestas
- **ROI singles**: **-37.5%**

_Nota: P&L de parlay legs no se computa porque depende del resto del parlay, que no se registra._

## 4. Performance por tipo de mercado (apuestas reales)

| Mercado | W | L | Push | P&L singles (u) |
|---|---:|---:|---:|---:|
| F5_doble_oportunidad | 2 | 1 | 0 | — |
| partial_DNB | 1 | 0 | 0 | +0.31 |
| prop_bateador_HRR_RBI | 1 | 0 | 0 | +0.80 |
| ML | 1 | 0 | 0 | — |
| F5_DNB | 2 | 1 | 0 | -0.11 |
| over_under_full | 1 | 0 | 0 | — |
| run_line_underdog_1.5 | 1 | 0 | 0 | — |
| TT_full_game | 0 | 1 | 0 | -1.00 |
| prop_bateador_bases | 1 | 2 | 0 | -2.00 |
| F5_under | 0 | 1 | 0 | — |
| prop_pitcher_Ks | 0 | 1 | 0 | -1.00 |

## 5. Performance por fuente de edge

| Fuente | N | Acierto | Pass✓ | Pass✗ | Err_Lectura | Err_Mercado | Varianza |
|---|---:|---:|---:|---:|---:|---:|---:|
| matchup_mano_repertorio | 15 | 7 | 3 | 1 | 2 | 1 | 1 |
| tipo_vulnerabilidad_pitcher | 4 | 1 | 1 | 2 | 0 | 0 | 0 |
| leash_bullpen | 3 | 0 | 2 | 1 | 0 | 0 | 0 |
| forma_individual | 3 | 0 | 1 | 0 | 2 | 0 | 0 |
| parque_clima | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| bullpen_rival_debil | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| edge_combinado | 1 | 1 | 0 | 0 | 0 | 0 | 0 |

## 6. Performance por tipo de pitcher vulnerable

| Tipo | N | Aciertos | Errores |
|---|---:|---:|---:|
| Tipo A | 6 | 2 | 1 |
| Tipo B | 9 | 4 | 1 |
| Tipo C | 2 | 0 | 0 |

## 7. Frecuencia de patrones v2 aplicados

| Patrón | Apariciones |
|---|---:|
| 10: Props salen del guion, no del menú | 10 |
| 1: Tipología vulnerabilidades pitcher (A/B/C) | 9 |
| 12: Side con ruido → mercado más limpio | 9 |
| 4: K upside no es over Ks si hay tráfico | 7 |
| 11: Factores ambientales (parque/clima/umpire) | 6 |
| 5: Un solo equipo con rutas → su TT | 6 |
| 3: Timing del daño: F5 vs full game | 5 |
| 8: Opener/spot starter no es fade automático | 4 |
| 9: Pitcher élite no bloquea automáticamente | 4 |
| 2: 'Mejor abridor' no es F5 side automático | 3 |
| 6: Favorito sin edge ofensivo colectivo | 2 |
| 7: Underdog +1.5 necesita conversión | 2 |

## 8. Calidad del menú: picks analizadas pero no jugadas

- Total: **247**
- Habrían cobrado: **143** | perdido: 101 | push: 3
- Win rate (sin push): **59%**
- P&L hipotético (1u flat): **+26.68u** en 152 con cuota → ROI **+17.6%**

## 9. Patrones emergentes registrados

Hipótesis candidatas a v3 si reaparecen en partidos futuros:

**1.** `orioles-marlins-050526`

> Un favorito con mejor ERA/WHIP pero perfil Tipo C como abridor propio puede ser MÁS frágil para F5 side que el rival con perfil Tipo A — el rival se rompe por tráfico (predecible), el propio puede colapsar por contacto explotado (varianza).

**2.** `padres-cardinals-070526`

> Cuando se cumplen estas 5 condiciones juntas — favorito con edge de abridor, lineup favorito 'parece' bien por mano pero split colectivo flojo vs esa mano, parque pitcher-friendly, parte baja del favorito poco profunda, underdog competente con bullpen funcional — la jerarquía correcta es: F5 protegido / under / underdog +1.5 > ML favorito > props ofensivas del favorito > run line favorito.

**3.** `rangers-yankees-070526`

> Las 4 condiciones para tomar underdog +1.5: (1) bulk plan del favorito débil O incierto, no solo el opener; (2) underdog convierte tráfico, no solo OBP; (3) abridor del underdog limita inning grande en 2ª/3ª vuelta; (4) favorito sin profundidad 6-9. Si falla 2+, pasar. Refinamiento del Patrón 7 v2.

**4.** `guardians-royals-070526`

> Antes de tomar F5 favorito por diferencia de abridores, revisar si el underdog puede romper el F5 por pitch count más que por slugging. Checklist: ¿favorito tiene whiff real o solo command? ¿underdog tiene 4-5 bates pacientes arriba? ¿muchos zurdos/switch contra el abridor? ¿umpire sin zona grande? ¿underdog puede correr? ¿parte baja del underdog puede extender innings? ¿favorito puede dejar corredores y producir tarde? Si varias son sí: bajar F5 side, subir props top bat / TT full game / over protegido.

**5.** `dbacks-pirates-070526`

> Pitcher Tipo B con leash de nombre/ace puede permitir el contacto/daño esperado pero seguir completando innings y acumulando Ks contra lineups con K naturales. Las picks under Ks/outs fallan; F5 TT del rival y hits allowed sí cobran. El diagnóstico de vulnerabilidad sigue siendo correcto, solo el mercado.

**6.** `yankees-rangers-050526`

> Pitcher élite (K% alto) con grietas de contacto fuerte/barrels en parque HR-friendly NO es bloqueador automático del lineup rival. La grieta importa más que la ERA. Mercado correcto: ML/TT/props de poder full game, no F5 (que sigue dependiendo de dominio temprano del ace).

**7.** `nationals-twins-050526`

> Cuando un abridor combina K upside + WHIP alto + BB + rival con OBP funcional, el orden de mercados debería ser: TT rival > F5 TT rival > hits permitidos > outs under > carreras permitidas > over Ks. La sucesión 'pitcher con stuff' → 'over Ks' es un atajo peligroso si el perfil real es de tráfico.

**8.** `orioles-yankees-040526`

> Cuando el favorito tiene ML muy corto (1.47) en un spot de lineup fuerte vs abridor vulnerable, jugarlo como pierna de parlay multi-leg + tomar la prop H+R+RBI/TB de un bate 2º-5º como single separado es buena gestión: el ML corto aporta a cuota acumulada en otro vehículo, y el prop captura el edge del partido con cuota viva propia.

**9.** `cardinals-brewers-040526`

> Cuando ambos abridores son vulnerables, comparar por Tipo: A (comando frágil → no sobrevive innings con tráfico) > B (contacto fuerte permitido → puede sobrevivir con whiff parcial) > C (sin whiff pero command management → suele sobrevivir si no enfrenta paciencia). El Tipo A es el más atacable para TT/F5 TT del rival; el B/C requiere ataques más específicos (hits allowed over) que pueden no convertirse en runs.

**10.** `reds-cubs-040526`

> TT alto del favorito necesita pre-confirmación de clima/viento en ventana <2h del game time. Proyecciones tempranas de viento a 10+ mph que no se confirman in-game son la fuente más común de TT over frágiles. Si el viento no está confirmado, bajar el TT over a opción secundaria y subir ML/under.

**11.** `redsox-tigers-040526`

> Subestimar abridor con K%, SwStr%, CSW% y leash real puede convertir un under Ks en el mercado más peligroso de la sesión. Si las métricas avanzadas del pitcher señalan dominio (Tolle aquí), no flippear a under Ks por paciencia del rival salvo línea muy alta.

**12.** `padres-giants-040526`

> Antes de fadear a un opener/spot starter por leash o comando o malas líneas Triple-A, exigir 2 confirmaciones: (1) que el lineup rival tenga paciencia/bajo chase / OBP funcional; (2) que las muestras MLB previas del pitcher (no Triple-A) también señalen el problema. Sin esas, la fuente queda en la zona ruidosa de la jerarquía v2.

**13.** `phillies-rockies-080526`

> K upside no es run prevention. Una prop de BB sobre 1.5 es estructuralmente frágil: necesita guion limpio, no solo buen BB% de temporada. Si el pitcher entra bajo estrés o tiene salida corta, la línea se rompe rápido. Para pitcher con K alto + perfil de tráfico, mejor outs over / hits allowed que BB under.

**14.** `yankees-brewers-080526`

> F5 under con dos abridores 'buenos en papel' es frágil si uno de los dos lineups tiene perfil de manufactura (contacto + velocidad + paciencia + parte baja funcional). El ace estable puede romperse sin HR. Para edges de K de un abridor específico, dejar la apuesta en prop del pitcher, no trasladar a F5 under.

**15.** `braves-rockies-030526`

> En Coors, parte baja del lineup no necesita ser élite para aportar al TT (Heim 5 RBI, Mateo/White produciendo). Para TT en parques ofensivos, no mirar solo 1-5; revisar si 6-9 evita outs automáticos. // K upside puede dar volumen pese a leash corto si pitcher tiene whiff pitch elite y rival tiene K natural.

**16.** `phillies-marlins-040526`

> Lineup con platoon favorable en papel necesita 2 confirmaciones para traducirse en TT/ML: (1) capacidad de tomar BB para tráfico extra; (2) ejecución con RISP. Sin esas, los hits quedan aislados y el ace rival se estabiliza. Roof closed + viento 0 + ambos abridores con CSW/curva → under es default.

**17.** `bluejays-twins-020526`

> Cuando el favorito tiene mejor abridor Y el bullpen rival es el verdadero punto débil, el mejor mercado no es F5: es prop del abridor (Cease Ks) + TT/over full game del favorito. El daño puede llegar contra bullpen tarde.

**18.** `royals-mariners-020526`

> Cuando un pitcher llega con K-BB% mejorado y nuevo pitch funcional, no basta con 'el rival no tiene K% altísimo'. El salto de arsenal puede superar la disciplina del lineup, especialmente si trae bates jóvenes/volátiles. T-Mobile además limita overs/HR.

**19.** `tigers-braves-300426`

> Pitcher 'vulnerable por forma reciente' no equivale a 'pitcher con pocos Ks'. Separar: under Ks necesita whiff bajo en arsenal real, no solo K% reciente bajo; under outs necesita tráfico+pitch count; team total necesita conversión RISP. Si arsenal está intacto, el pitcher puede seguir acumulando Ks pese a permitir hits.

**20.** `rockies-reds-300426`

> Patrón recurrente en abril: under Ks de pitcher con forma reciente mala pero arsenal MLB intacto falla más de lo esperado. Si el pitcher tiene leash y stuff, los Ks llegan aunque el rival no tenga K% alto. Para ese edge, mejor team total / hits allowed / outs under con línea generosa.

**21.** `rangers-dbacks-110526`

> En bullpen games del favorito con bullpen elite por ERA, el lado del underdog y/o el under del partido son más limpios que el TT del underdog. La paciencia del lineup underdog requiere que el opener pierda comando para traducirse en tráfico; si el opener mete strikes, la paciencia no genera tráfico y la conversión RISP no aparece. Para edge ofensivo del underdog en bullpen game, exigir además bullpen rival mediocre — si el bullpen es elite, expresar el edge en ML/Under, no en TT.


## 10. Divergencias jugada ≠ analítica

Partidos donde lo realmente apostado y el frame del análisis tienen clasificación distinta:

| Partido | Jugada | Analítica |
|---|---|---|
| rangers-yankees-070526 | PASS_CORRECTO | ERROR_DE_LECTURA |
| guardians-royals-070526 | PASS_CORRECTO | ERROR_DE_MERCADO |
| dbacks-pirates-070526 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| phillies-athletics-050526 | ACIERTO_LIMPIO | ERROR_DE_MERCADO |
| yankees-rangers-050526 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| nationals-twins-050526 | PASS_CORRECTO | ERROR_DE_MERCADO |
| cardinals-brewers-040526 | PASS_CORRECTO | ERROR_DE_LECTURA |
| reds-cubs-040526 | PASS_CORRECTO | ERROR_DE_MERCADO |
| redsox-tigers-040526 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| phillies-rockies-080526 | PASS_INCORRECTO | ERROR_DE_LECTURA |
| yankees-brewers-080526 | ERROR_DE_LECTURA | ERROR_DE_MERCADO |
| braves-rockies-030526 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| phillies-marlins-040526 | PASS_CORRECTO | ERROR_DE_LECTURA |
| royals-mariners-020526 | VARIANZA | ERROR_DE_MERCADO |
| tigers-braves-300426 | ERROR_DE_LECTURA | ERROR_DE_MERCADO |
| rockies-reds-300426 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| rangers-dbacks-110526 | PASS_CORRECTO | ERROR_DE_MERCADO |

_17 partidos con divergencia (de 29)._

## 11. Insights operativos

- **Apuestas con ROI negativo**: -37.5% en 8 singles con cuota.
- **El menú considerado supera al jugado**: ROI menú +17.6% vs jugado -37.5%. Sugiere que se descartan picks correctas por cuota/heurística de selección.
- **Fuente de edge más propensa a error**: `matchup_mano_repertorio` con 3 errores. Revisar antes de apostar.
- **Mejor mercado por win rate**: `F5_doble_oportunidad` con 2-1 (67% wr).
