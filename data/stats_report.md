# MLB Postmortems — Reporte de recalibración

Dataset: **52 partidos**. Fuente: `data/postmortems.yaml`.

## 1. Resumen de decisiones

**Clasificación jugada** (lo realmente apostado):

| Clasificación | Count | % |
|---|---:|---:|
| ACIERTO_LIMPIO | 14 | 27% |
| PASS_CORRECTO | 13 | 25% |
| PASS_INCORRECTO | 13 | 25% |
| ERROR_DE_LECTURA | 5 | 10% |
| ERROR_DE_MERCADO | 4 | 8% |
| NO_JUGADA | 2 | 4% |
| VARIANZA | 1 | 2% |

**Clasificación analítica** (frame del análisis):

| Clasificación | Count | % |
|---|---:|---:|
| ERROR_DE_MERCADO | 19 | 37% |
| ACIERTO_LIMPIO | 18 | 35% |
| ERROR_DE_LECTURA | 13 | 25% |
| PASS_INCORRECTO | 1 | 2% |
| ACIERTO_RUIDOSO | 1 | 2% |

## 2. Apostar vs pasar

- Apuestas tomadas: **24** (46%)
- Pass: **28** (54%)

- Pass correctos: **13/28** (46%)
- Pass incorrectos: **13/28** (46%)

## 3. Win rate y P&L de apuestas reales

- Total apuestas/piernas: **25**
- Ganadas: **15** (60%)
- Perdidas: 10 (40%)
- Push: 0
  - Piernas de parlay: 7 cobraron / 2 perdieron

- **P&L estimado** (singles, 1u flat): **-0.99u** en 16 apuestas
- **ROI singles**: **-6.2%**

_Nota: P&L de parlay legs no se computa porque depende del resto del parlay, que no se registra._

## 4. Performance por tipo de mercado (apuestas reales)

| Mercado | W | L | Push | P&L singles (u) |
|---|---:|---:|---:|---:|
| prop_bateador_HRR_RBI | 2 | 0 | 0 | +1.46 |
| F5_doble_oportunidad | 2 | 1 | 0 | — |
| partial_DNB | 1 | 0 | 0 | +0.31 |
| ML | 1 | 0 | 0 | — |
| F5_DNB | 2 | 1 | 0 | -0.11 |
| over_under_full | 1 | 0 | 0 | — |
| run_line_underdog_1.5 | 1 | 0 | 0 | — |
| prop_equipo | 1 | 0 | 0 | +1.08 |
| prop_pitcher_ER | 1 | 0 | 0 | +1.62 |
| TT_full_game | 2 | 3 | 0 | -1.35 |
| prop_bateador_bases | 1 | 2 | 0 | -2.00 |
| F5_under | 0 | 1 | 0 | — |
| prop_pitcher_Ks | 0 | 1 | 0 | -1.00 |
| prop_bateador_BB | 0 | 1 | 0 | -1.00 |

## 5. Performance por fuente de edge

| Fuente | N | Acierto | Pass✓ | Pass✗ | Err_Lectura | Err_Mercado | Varianza |
|---|---:|---:|---:|---:|---:|---:|---:|
| matchup_mano_repertorio | 20 | 8 | 4 | 2 | 3 | 1 | 1 |
| edge_combinado | 15 | 5 | 5 | 3 | 0 | 2 | 0 |
| leash_bullpen | 4 | 0 | 2 | 2 | 0 | 0 | 0 |
| tipo_vulnerabilidad_pitcher | 4 | 1 | 1 | 2 | 0 | 0 | 0 |
| forma_individual | 4 | 0 | 1 | 1 | 2 | 0 | 0 |
| parque_clima | 3 | 0 | 0 | 2 | 0 | 0 | 0 |
| bullpen_rival_debil | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| momentum | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

## 6. Performance por tipo de pitcher vulnerable

| Tipo | N | Aciertos | Errores |
|---|---:|---:|---:|
| Tipo A | 11 | 2 | 2 |
| Tipo B | 24 | 8 | 2 |
| Tipo C | 5 | 1 | 1 |

## 7. Frecuencia de patrones v2 aplicados

| Patrón | Apariciones |
|---|---:|
| 1: Tipología vulnerabilidades pitcher (A/B/C) | 29 |
| 12: Side con ruido → mercado más limpio | 22 |
| 11: Factores ambientales (parque/clima/umpire) | 20 |
| 5: Un solo equipo con rutas → su TT | 19 |
| 10: Props salen del guion, no del menú | 17 |
| 3: Timing del daño: F5 vs full game | 13 |
| 4: K upside no es over Ks si hay tráfico | 13 |
| 9: Pitcher élite no bloquea automáticamente | 10 |
| 6: Favorito sin edge ofensivo colectivo | 9 |
| 8: Opener/spot starter no es fade automático | 9 |
| 2: 'Mejor abridor' no es F5 side automático | 6 |
| 7: Underdog +1.5 necesita conversión | 3 |
| 13: Señal específica con mecanismo > agregado de temporada | 2 |

## 8. Calidad del menú: picks analizadas pero no jugadas

- Total: **363**
- Habrían cobrado: **215** | perdido: 145 | push: 3
- Win rate (sin push): **60%**
- P&L hipotético (1u flat): **+50.52u** en 234 con cuota → ROI **+21.6%**

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

**22.** `giants-athletics-150526`

> Validación de Patrón 5 cuando el rival visitante es bottom-tier ofensivo: el TT del fuerte cobra cómodo aunque el marcador full game sea moderado (5-2). La sublección del Patrón 6 sobre RL puede tener excepciones cuando el rival no convierte tráfico (SF 10 hits / 2 R).

**23.** `marlins-rays-160526`

> En partidos con dos Tipo C en parque suppressor, el riesgo principal del Under NO es la regulación sino EXTRAS con bullpen débil identificable. Antes de tomar Under en este perfil, chequear si hay un brazo con ERA >5 que sería long-relief en extras; si sí, bajar stake del Under y subir picks independientes del run environment (SB, hits específicos, props matchup-driven).

**24.** `ath-laa-190526`

> Candidato Patrón 13 (matchup-específico vs métrica-promedio): cuando un abridor tuvo blow-up vs UN equipo específico en la temporada actual, el riesgo de repetición es mayor que lo que sugieren sus métricas de temporada. Detmers vs ATH ya había estallado el 8/4 y hoy se repitió. Las métricas avanzadas son promedio vs liga; no neutralizan la asimetría head-to-head reciente. También: 'lineup debilitado' (ATH sin sus 2 mejores zurdos) ≠ 'lineup monoruta' — ATH anotó 14 con multiruta.

**25.** `nationals-reds-130526`

> Refinamiento Patrón 3: cuando AMBOS abridores son Tipo B con leash atenuado por contexto (regreso IL, parque hostil + ofensiva en racha), salen en 3-4 IP y el Over F5 alto puede ser MÁS limpio que el Over full game. Distinguir 'Tipo B clásico con leash sólido' de 'Tipo B con leash atenuado por contexto' — el segundo se comporta más cerca del Tipo A.

**26.** `cardinals-athletics-130526`

> Cuando la tesis identifica vulnerabilidad Tipo A en lineup robusto + parque favorable, los mercados de EVENTO COLECTIVO (TT over, hits/ER/BB allowed del pitcher, ML) capturan el edge con menos varianza que las props INDIVIDUALES de bateadores. La cuota individual más larga no compensa la varianza de depender de un solo AB. Suma al cluster Ohtani outs / Cavalli outs / Pittsburgh +1 F5.

**27.** `mariners-astros-130526`

> (1) Road OPS del lineup como modificador de primer orden para TT over visitante: con favorito road OPS bottom-10 MLB, el TT over exige confirmación adicional aunque matchup + bullpen agregado sugieran edge (Seattle 1-13 RISP). (2) ERA agregado de bullpen sobreestima fragilidad cuando un brazo extremo (Hader IL, Abreu 8.56) infla el promedio — chequear los 3-4 brazos que cubrirían 6ª-9ª. Gemelo del caso Baltimore 10H/1R/0-7 RISP (Patrón 5).

**28.** `mariners-astros-140526`

> Patrón META multi-turn — 'sobrecorrección por forma reciente individual en segundo análisis': cuando un segundo turno cambia la pick top basándose en muestra chica de forma reciente del pitcher (<20 IP) que contradice el perfil de temporada, suele degradar el primer análisis. Forma reciente individual (P8) no debe anular matchup mano/repertorio (P2). Trigger: regresar al primer análisis salvo soporte Statcast en la misma dirección.

**29.** `bluejays-tigers-150526`

> (1) Bullpen game improvisado NO es plan fijo (candidato P13/P8): con incertidumbre de rotación, analizar el bullpen game como SISTEMA, no anclar en un reliever específico (proyecté Madden bulk; fue Anderson). (2) Patrón 6 en tier máximo (4-5 condiciones) → evitar TODOS los mercados ofensivos del favorito. (3) Patrón 11 viento pronóstico ≠ real (caso confirmado).

**30.** `athletics-angels-210526`

> (1) Tipo B se comporta como Tipo C cuando el lineup rival es K-heavy colectivo: la clasificación A/B/C debe leerse SIEMPRE en contexto del lineup rival, no en aislamiento (refinamiento Patrón 1). (2) Selección de bate-prop: priorizar LHH del top-5 con platoon sobre RHH 'bate top' cuando hay RHP HR-prone — el calor reciente del bate top no sustituye la asimetría platoon.

**31.** `tigers-rays-010626`

> Candidato Patrón 13: 'ofensiva con peor AVG/wRC+ del slate ≠ ofensiva inofensiva'. En parque HR-friendly + abridor rival con recta bateable, un lineup 'muerto' con poder zurdo latente puede explotar por HR SIN convertir tráfico. Antes de declarar 'una sola ofensiva tiene ruta' (Patrón 5), agregar el filtro '¿el equipo sin ruta tiene perfil de poder + parque HR + recta bateable enfrente?'. Si sí, el over del juego deja de ser pass automático.

**32.** `astros-cubs-240526`

> 'LHP élite con perfil de barrels post-blow-up vs all-RHB con poder distribuido': cuando un LHP cumple (1) blow-up <14 días, (2) Barrel% ≥9%, (3) degradación post-mediados-temporada previa, (4) viento no confirmado, la ventaja teórica de mano puede invertirse si el lineup rival tiene poder en 3+ spots. Refuerza 'matchup-specific blowup overrides metric-average' (Detmers, ahora Imanaga ×2 = patrón del PITCHER en degradación). Props pitcher Ks/outs sobreviven (Patrón 4 alerta espejada positiva).

**33.** `rangers-cardinals-020626`

> (1) Refinamiento Patrón 11: parque + clima confirmado es el edge más fiable para POWER/HR, NO para el total de carreras. Check obligatorio antes de colgar un under del parque: ¿la ruta de carreras es poder o tráfico? (2) Refinamiento filtro de selección: timing > regla de cuota. (3) Promoción Patrón 13 'manufactura sin HR' (May+Eovaldi Tipo B): el mecanismo común es 'contacto + bullpen frágil decide el partido sin HR'.

**34.** `royals-twins-040626`

> (1) META-REGLA sobre Jerarquía de Edges: no permitir que momentum/forma reciente (tier 7-9) invierta parque/matchup/leash (tiers 1-4) cuando los tiers altos apuntan claro. Paralelo a mariners-astros-140526. (2) Refinamiento 'ofensiva muerta explota por HR': tercer caso del mecanismo 'Tipo C + viento out confirmado + parque pro-run = colapso por slugging' (junto a Tigers/Rays 01/06, Astros/Cubs 24/05).

**35.** `dodgers-dbacks-040626`

> Refinamiento del usuario: 'sin Tipo A en el partido, B atacable es relativo no absoluto; con freno de fuente alta → under/pass > TT del favorito'. Cuando NO hay Tipo A en el matchup, la atacabilidad del Tipo B depende de frenos de fuente alta (lineup propio en slump, BvP desfavorable); si esos frenos existen y vienen de tier 1-4, el under/pass debe LIDERAR la recomendación. Contraste con dodgers-dbacks-030626 (allí NO había freno → TT LAD cobró).

**36.** `rockies-angels-010626`

> (1) 'TT under del visitante débil es FRÁGIL cuando el abridor propio tiene riesgo de comando alto: los boletos fabrican la ofensiva que el bate no fabrica' (Soriano 7 BB → COL 9 R). Check pre-partido: BB% del abridor propio reciente. (2) Corolario de la Regla Madre: un prop directo del pitcher rival cobra aunque side/total/TT fallen — la pieza de hierro aislada gana al guion completo (2 casos con Tigers/Rays 01/06).

**37.** `brewers-rockies-060626`

> (1) 'Eje bullpen detrás / daño tardío debe primar sobre la preferencia F5 menos tasado → full-game TT > F5 TT'. El precio NO debe invertir el análisis de timing (conecta con rangers-cardinals-020626). (2) 'Equipo bajo-HR en Coors + viento out puede anotar vía HR solitario, no tráfico; no degradar props HR' — cuarto caso del meta-mecanismo 'el daño llega por aire con viento out confirmado' (con Tigers/Rays 01/06, Astros/Cubs 24/05, Royals/Twins 04/06).

**38.** `pirates-braves-050626`

> Candidato Patrón 13: 'Tipo B + dominio histórico inverso documentado (rival específico lo castiga, ej. Keller 7.31 ERA vs ATL) = upgrade de convicción en hits/ER over y TT del rival'. Espejo POSITIVO de 'matchup-specific blowup overrides metric-average' (Detmers/Imanaga). Mismo principio: el head-to-head específico tiene señal por encima del perfil promedio, en ambas direcciones. Patrón 4 alerta espejada validada en negativo (Pérez 5 K, under Ks habría perdido).

**39.** `white-sox-phillies-070626`

> Refinamiento Patrón 11: 'over de CARRERAS y over de HR son tesis distintas'. Viento out confirmado + parque de HR + ofensivas con poder NO garantiza match-HR over — un partido de anotación colectiva puede ir over de carreras vía tráfico/extra-base SIN 3+ HR (CWS, 3º en HR MLB, anotó 5 R con 0 HR). El viento out garantiza el RUN environment, no el camino del daño. Regla: tomar TT/over de carreras (capturan ambos caminos), no match-HR (captura solo un camino).

**40.** `giants-cubs-070626`

> Escudo de brazo bulk (n=1): cuando el edge combina 'atacar abridor vulnerable' + 'bullpen rival gastado', un brazo bulk/swing fresco (bajada reciente, long man, spot en turno) puede anular AMBOS edges a la vez: el abridor sale temprano Y el bulk absorbe 5-6 IP en blanco. Caso: Taillon 1 IP → Assad 6.1 IP shutout. Inverso del Patrón 8. Implicación: si el edge depende de castigar a UN abridor específico, verificar disponibilidad de brazo bulk fresco del rival antes de fijar convicción.

**41.** `phillies-bluejays-080626`

> Timing-inversión por H2H fuerte (n=1): un Tipo B con H2H documentado de comando frágil + contacto duro vs un rival específico (Patrón 13 fuerte) puede invertir la lectura de leash — el blow-up llega en F5, no en 3ª vuelta. Corbin, con leash nominal 'funcional', explotó en 3 IP y todo el daño de PHI fue F5. Notas secundarias: (a) cuando el rival anota por HR solitario, preferir TT full a línea alta (2.5) sobre F5 TT a línea ajustada (1.5); (b) arsenal de whiff élite anula la tendencia bajo-K del lineup — no fadear Ks over por 'lineup de contacto'.

**42.** `mariners-orioles-090626`

> (1) TT-UNDER expuesto a viento-out no confirmado en parque HR → tratar el viento no confirmado como señal de PASS específica para ese under, NO neutral. n≥2 ahora (junto con cluster Tigers/Rays 01/06, Royals/Twins 04/06, Brewers/Rockies 06/06 del meta-mecanismo 'daño por aire con viento out'). El espejo: NO tomar TT-UNDER cuando el viento out es plausible-no-confirmado en parque HR + abridor Tipo B. (2) Micro-lección: no abandonar 'outs over' por línea alta cuando la racha de IP la sostiene (Gilbert Outs Over 17.5 ganó, descartado por pivote a Ks que perdió).

**43.** `twins-tigers-100626`

> VIOLACIÓN del Patrón 5 (caveat al revés): se declaró 'solo DET tiene ruta' ignorando poder latente de MIN (Buxton/Lewis HR) + ambiente caliente — 'lineup debilitado ≠ ofensiva inofensiva', MIN anotó 6 > DET 4. Candidatos n=1: (1) ambos abridores vulnerables + parque caliente → over del juego ≥ TT individual (menos dependencias, no exige adivinar qué ofensiva convierte); (2) lineup alto-K vs pen malo-pero-con-whiff → descontar TT-over pese al ERA agregado del pen (DET 14 K / 3-10 RISP; pen MIN tiró 10 K). Nota de proceso: demora por tormenta invalida el anemómetro previo — re-confirmar viento DESPUÉS de cualquier demora (conecta con el gate de viento de mariners-orioles 09/06).


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
| ath-laa-190526 | PASS_CORRECTO | ERROR_DE_LECTURA |
| nationals-reds-130526 | PASS_INCORRECTO | ACIERTO_LIMPIO |
| mariners-astros-130526 | PASS_CORRECTO | ERROR_DE_MERCADO |
| mariners-astros-140526 | PASS_INCORRECTO | ERROR_DE_MERCADO |
| bluejays-tigers-150526 | PASS_CORRECTO | ACIERTO_LIMPIO |
| tigers-rays-010626 | PASS_INCORRECTO | ACIERTO_LIMPIO |
| astros-cubs-240526 | PASS_CORRECTO | ERROR_DE_LECTURA |
| rangers-cardinals-020626 | NO_JUGADA | ERROR_DE_LECTURA |
| royals-twins-040626 | PASS_INCORRECTO | ERROR_DE_LECTURA |
| dodgers-dbacks-040626 | PASS_CORRECTO | ERROR_DE_LECTURA |
| brewers-rockies-060626 | PASS_CORRECTO | ERROR_DE_LECTURA |
| white-sox-phillies-070626 | PASS_INCORRECTO | ACIERTO_LIMPIO |
| giants-cubs-070626 | NO_JUGADA | ACIERTO_RUIDOSO |
| phillies-bluejays-080626 | PASS_INCORRECTO | ACIERTO_LIMPIO |

_31 partidos con divergencia (de 52)._

## 11. Insights operativos

- **Apuestas con ROI negativo**: -6.2% en 16 singles con cuota.
- **El menú considerado supera al jugado**: ROI menú +21.6% vs jugado -6.2%. Sugiere que se descartan picks correctas por cuota/heurística de selección.
- **Fuente de edge más propensa a error**: `matchup_mano_repertorio` con 4 errores. Revisar antes de apostar.
- **Mejor mercado por win rate**: `prop_bateador_HRR_RBI` con 2-0 (100% wr).
