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


## DECISIONES POR CLUSTER

### A1 — FILTRO DE SELECCIÓN → REGLA DE EJECUCIÓN (PROMOVER)

Estado v2.1: "check de selección" = gatillo duro defensivo (exige razón para
descartar). Evidencia v2.2: 10 casos de picks ganadoras descartadas/relegadas/
sub-priorizadas + 6 PASS_INCORRECTO. Es el leak dominante del run.

Decisión: PROMOVER de gatillo a regla primaria con DEFAULT INVERTIDO.

Texto propuesto para v2.2:

----------------------------------------------------------------------
REGLA DE EJECUCIÓN Y SELECCIÓN DE MERCADO (v2.2)

Contexto empírico (24 partidos, 11/05-07/06): el error más caro NO fue
analítico sino de ejecución. Se apostó en 8 de 24; de esos 8, 6 fueron
aciertos limpios (75% por proceso). Pero de los 16 pass, 6 dejaron EV claro.
El sistema de análisis funciona; el cuello de botella es ejecutar.

DEFAULT INVERTIDO:
Cuando el análisis identifica una pick que (a) captura el edge top, (b) tiene
cuota >1.80, y (c) no tiene razón de descarte de tier 1-4 → la acción por
defecto es EJECUTAR A STAKE MÍNIMO, no pasar. Pasar requiere justificación
activa, igual que apostar.
[ ] Caveat de sobre-apuesta: la regla aplica solo a la pick que captura el
    edge TOP (no a todo el menú) y a STAKE MÍNIMO. No es licencia para
    apostar todo el board; es para no dejar morir el edge mejor identificado.

JERARQUÍA DE SELECCIÓN (timing > precio):
[ ] El análisis de TIMING del daño (F5 / full game / tardío) elige el
    mercado. El precio NO invierte esa elección.
[ ] Si el análisis dice "daño tardío / full game", NO elevar el F5 TT por
    estar "menos tasado" (brewers-rockies 06/06: F5 TT elevado contra el
    propio análisis de daño tardío → perdió; el full-game TT degradado por
    "cobrado" → ganó).
[ ] Una pick degradada por análisis de timing/dependencia documentado SÍ
    puede descartarse (rangers-cardinals 02/06: Under 6.5 degradado por
    riesgo de daño tardío vs bullpen → descarte válido). Timing degrada;
    precio no.

RAZONES INVÁLIDAS para descartar una pick que captura el edge top a cuota
>1.80 (ninguna, sola, justifica el descarte):
[ ] "Cuota corta / poco valor."
[ ] "Forma reciente individual del pitcher" sin soporte Statcast en la misma
    dirección (mariners-astros 14/05: SEA ML descartado por reframe de forma
    reciente → habría ganado).
[ ] "Demasiado obvio / el mercado ya lo precia."
[ ] "Solo live" (relegar a en-vivo un edge legible pre-partido —
    royals-twins 04/06: Over relegado a 'solo live' → cobró).
[ ] "Prefiero el bate top RHH" cuando hay LHH viable con mejor platoon
    (athletics-angels 21/05).

RAZONES VÁLIDAS para descartar (tier 1-4):
[ ] Lineup no confirmado.
[ ] Bullpen contradice el guion.
[ ] Parque/clima hostil confirmado <90 min.
[ ] Timing del daño no calza con el mercado.
[ ] Dependencia adicional no contemplada en el edge.

CASOS DE REFERENCIA (10): Ohtani outs (Astros/Dodgers 05/05), Cavalli outs
(Nationals/Twins 05/05), PIT +1 F5 (D-backs/Pirates 07/05), Over 9.5
(Nationals/Reds 13/05), mercados colectivos (Cardinals/Athletics 13/05),
SEA ML (Mariners/Astros 14/05), picks recomendadas (Athletics/Angels 21/05),
Over (Royals/Twins 04/06), full-game TT (Brewers/Rockies 06/06), 2-de-3
principales (White Sox/Phillies 07/06).
----------------------------------------------------------------------

Qué NO cubre esta regla (importante): los casos donde el ANÁLISIS COMPLETO
estaba equivocado y el pass por instinto salvó (astros-cubs 24/05,
dodgers-dbacks 04/06). Ahí no hay filtro que ayude — el pass fue correcto
porque la lectura era falsa. La regla de ejecución aplica solo cuando el
análisis identificó bien el edge; no fuerza ejecutar análisis dudosos.


### A2 — ALERTA ESPEJADA P4 → REGLA DEL UNDER Ks (PROMOVER + AFILAR)

Estado v2.1: alerta embebida en el Patrón 4 ("forma reciente mala ≠ pocos
Ks si arsenal intacto"), con 4 casos. Evidencia v2.2: 9 casos, y al verlos
juntos emerge un insight más afilado — el predictor real NO es el K%
reciente sino las IP ESPERADAS. Esto reconcilia las dos direcciones del
patrón (que el under gane o pierda depende de IP, no de K rate).

Decisión: PROMOVER de alerta a regla operativa propia, reformulada en
términos de IP.

Texto propuesto para v2.2:

----------------------------------------------------------------------
REGLA DEL UNDER Ks (v2.2)

El predictor del under Ks es las IP ESPERADAS, no el K% reciente.

Confirmado en 9 casos, dos direcciones:

Dirección A — arsenal intacto + pitcher llega a 5-6 IP → los Ks llegan,
under PIERDE pese a forma reciente mala o pese a permitir daño:
[ ] Valdez (30/04): bajo K% reciente, 8 K en 6 IP.
[ ] Abbott (30/04): 18% BB temporada, 5 K.
[ ] Hancock (02/05): nuevo arsenal, 14 K en 7 IP.
[ ] Detmers (19/05): 8 K pese a blow-up de 8 ER.
[ ] Wrobleski (04/06): 4 K en 6 IP, under habría perdido.

Dirección B — salida corta por tráfico/bombardeo → under GANA, pero por
POCAS IP, no por bajo K rate:
[ ] Cavalli (05/05): 2 K, salida corta.
[ ] Lugo (04/06): 4 K, salida corta (under descartado correctamente).
[ ] Keller (05/06): 4 K, sacado a 4.2 IP vía bombardeo.
[ ] Nola (07/06): 4 K, sacado a 4.1 IP vía bombardeo.

Regla operativa:
[ ] Para TOMAR under Ks, no basta "forma reciente mala". Exigir riesgo real
    de SALIDA CORTA (<4.2 IP): leash corto confirmado (límite de pitcheo,
    regreso de IL, bullpen game) O Tipo A claro (comando frágil que se
    rompe por tráfico temprano).
[ ] Si el arsenal está intacto y el pitcher proyecta 5+ IP, los Ks llegan
    aunque la forma sea catastrófica → NO tomar under Ks.
[ ] Espejo positivo: el OVER Ks (o outs) vale incluso cuando el pitcher
    permite daño, si el arsenal está intacto. Las props pitcher Ks/outs
    sobreviven al colapso del side (Imanaga 6 K pese a 7 ER, astros-cubs
    24/05; props Eovaldi/May en rangers-cardinals 02/06).
----------------------------------------------------------------------

Nota de conexión: refuerza el principio "forma reciente individual = tier 8
ruidoso" de la Jerarquía de Edges. El K% de las últimas 4-5 salidas es ruido;
la IP esperada (leash + tipo de vulnerabilidad) es la señal.


### A3 — META-REGLA: CONFLICTO DE TIERS (NUEVA, extiende la Jerarquía)

Estado v2.1: la Jerarquía de Edges rankea fuentes pero solo dice "si el edge
viene de posiciones 7-9, bajar stake o confirmar en fuente más alta". NO
cubre el caso de CONFLICTO — qué hacer cuando dos señales de tiers distintos
apuntan a direcciones opuestas. 3 casos del run exponen este hueco.

Decisión: AGREGAR una regla de conflicto a la sección Jerarquía de Edges.

Texto propuesto para v2.2:

----------------------------------------------------------------------
REGLA DE CONFLICTO DE TIERS (v2.2 — extensión de la Jerarquía de Edges)

La Jerarquía rankea fuentes, pero no dice qué hacer cuando dos señales
apuntan a direcciones distintas. Regla:

[ ] Cuando dos señales chocan, la de tier MÁS ALTO manda la DIRECCIÓN.
[ ] Una señal de tier 7-9 (momentum, forma reciente individual, narrativa)
    puede justificar BAJAR STAKE, pero NUNCA invertir la dirección de una
    señal de tier 1-4 (parque/clima confirmado, matchup, leash/bullpen).
[ ] Un FRENO que viene de tier 1-4 (BvP histórico desfavorable, split
    colectivo flojo confirmado) no se releva a "nota al pie" debajo de una
    tesis: debe LIDERAR la recomendación o gatillar pass.

Casos:
[ ] mariners-astros 14/05: el reframe del 2º turno usó forma reciente
    (tier 8) para invertir el matchup de temporada (tier 2: SEA ML). SEA
    ganó 8-3, Burrows se reventó como decía su perfil. Tier 8 invirtió
    tier 2 → error.
[ ] royals-twins 04/06: "ambas ofensivas frías" (tier 9 momentum) invirtió
    parque pro-run + viento out + 2 abridores vulnerables (tiers 1-4) que
    apuntaban al over. Over cobró (14 R). Tier 9 invirtió tiers 1-4 → error.
[ ] dodgers-dbacks 04/06 (dirección inversa): el FRENO de tier alto (Nelson
    histórico vs LAD + top-3 en slump) se subponderó debajo de la tesis "LA
    castiga a Nelson Tipo B". LA top-3 fue 0-12. El freno debió liderar →
    pass o under.

Operativo: antes de fijar la dirección de la apuesta, preguntar "¿hay una
señal de tier más alto que contradice mi tesis o que frena el lado que
elijo?". Si sí, esa señal manda — no se releva a nota al pie ni se invierte
con momentum.
----------------------------------------------------------------------

Esto cierra el CLUSTER A (promociones de regla operativa). Las 3 promociones
atacan el hallazgo central del conteo: el problema migró a LECTURA y
EJECUCIÓN, no a traducción de mercado.


### B4 — PATRÓN 11: "AMBIENTE GOBIERNA RUN ENVIRONMENT, NO EL CAMINO DEL DAÑO" (REFINAR)

Estado v2.1: Patrón 11 tiene la regla del viento (<90 min) ya incorporada,
más parque/clima como filtro previo. Evidencia v2.2: 6 casos que afilan el
patrón en tres sub-hallazgos con un principio unificador — el ambiente
gobierna CUÁNTAS carreras esperar, NO CÓMO se anotan (HR vs tráfico).

Decisión: REFINAR el Patrón 11 con la sección unificada.

Texto propuesto para v2.2:

----------------------------------------------------------------------
PATRÓN 11 — REFINAMIENTO v2.2: el ambiente gobierna el run environment,
no el camino del daño.

(i) Confirmación de viento (regla v2.1, 3 confirmaciones nuevas):
El pronóstico matinal NO cuenta como confirmación; solo anemómetro/
observación <90 min del primer pitch. La dirección se invierte seguido
entre pronóstico y realidad.
[ ] Reds/Cubs 04/05: proyectado out, real 4 mph → TT over perdió por margen.
[ ] BlueJays/Tigers 15/05: proyectado SSW a LF, real IN desde RF.
[ ] Astros/Cubs 24/05: proyectado 7 mph IN RF, real 3 mph IN LF.

(ii) El factor ambiental gobierna CUÁNTAS carreras (run environment), NO
CÓMO se anotan (camino del daño: HR vs tráfico/contacto):
[ ] Parque suppressor de HR + viento in NO implica under de carreras si
    ambos lineups tienen contacto y bullpens flojos — el daño llega por
    tráfico (rangers-cardinals 02/06: 1 HR en 22 hits, pero 11 R por
    tráfico/contacto + colapso de bullpen).
[ ] Viento out confirmado + parque HR NO garantiza match-HR over — el daño
    puede llegar por tráfico (white-sox-phillies 07/06: CWS 3º en HR MLB,
    0 HR, 5 R por sencillos/dobles).
[ ] Sub-regla contraintuitiva: una ofensiva "fría", "sin top bats" o
    "bajo-HR" NO está protegida del slugging cuando hay viento out confirmado
    + abridor que permite contacto. El daño aparece por aire (Tigers/Rays
    01/06 DET 5 HR "ofensiva muerta"; Astros/Cubs 24/05 HOU sin Alvarez/
    Altuve 3 HR; Royals/Twins 04/06 MIN 4 HR; Brewers/Rockies 06/06 MIL
    5 HR solitarios).

Traducción a mercado:
[ ] Para capturar un edge ambiental, usar TT / over / under de CARRERAS
    (capturan ambos caminos del daño), NO match-HR ni props HR específicas
    (capturan solo un camino).
[ ] Viento out confirmado <90 min DEBE pesar como tier 1 en la selección de
    mercado (subir TT/over de carreras como principal), no relegarse a
    "solo live" (ver Regla de Ejecución, A1).
----------------------------------------------------------------------

Nota: este refinamiento absorbe dos candidatos previos del watchlist
("daño por aire pese a ofensiva fría" y "supresión de poder ≠ supresión de
carreras") como sub-reglas del Patrón 11, en vez de promoverlos a patrón
nuevo. Ambos son la misma idea: el ambiente fija el nivel de carreras, no
el mecanismo.


### B5 — PATRÓN 1: "LA CLASIFICACIÓN A/B/C ES CONTEXTUAL" (REFINAR)

Estado v2.1: Patrón 1 trata A/B/C como propiedad del pitcher (perfil de
temporada). Evidencia v2.2: 4 sub-refinamientos que comparten un meta-tema —
el tipo de vulnerabilidad es función del MATCHUP del día (pitcher × lineup ×
parque × leash × estado físico), no del perfil de temporada en aislamiento.

Decisión: REFINAR el Patrón 1 con la sección de contextualidad.

Texto propuesto para v2.2:

----------------------------------------------------------------------
PATRÓN 1 — REFINAMIENTO v2.2: la clasificación A/B/C es CONTEXTUAL, no una
propiedad fija del pitcher.

(a) Clasificación del MATCHUP, no del pitcher solo:
[ ] Un Tipo B (contacto fuerte) vs un lineup con K% colectivo alto (>25%)
    que no extiende at-bats opera como Tipo C (K alto + control). Severino
    HH 41.4% / Barrel 9.8% (Tipo B clásico) terminó 10 K / 0 BB porque LAA
    no extendió turnos (athletics-angels 21/05).
[ ] Antes de fijar el tipo, preguntar: ¿el lineup rival explota ESTE tipo o
    lo neutraliza?

(b) El leash del DÍA atenúa el tipo:
[ ] Un Tipo B con leash atenuado por contexto (regreso de IL, parque hostil +
    ofensiva rival en racha, comando frágil reciente) sale en 3-4 IP como un
    Tipo A, no 5-6 IP → el mercado se desplaza de "full-game over" hacia
    "F5 over alto" (nationals-reds 13/05: Lodolo post-IL + Irvin en parque
    hostil, ambos sub-5 IP, 73% del daño en F5).

(c) Post-IL: usar las últimas 2 salidas como overlay:
[ ] Para un pitcher recién regresado de IL, el xwOBA/Barrel%/K% de temporada
    agregada NO es predictor confiable; las últimas 2 salidas post-IL pesan
    más (phillies-redsox 13/05: Gray season xwOBA .369 vs forma post-IL
    dominante → 6 IP / 1 ER / 6 K).

(d) Operacionalizar el tipo en el PITCHER, no en el bateador:
[ ] La traducción de un tipo a mercado (ej. Tipo A → "BB allowed over") debe
    quedar en el pitcher (Liberatore BB allowed), no migrar a prop individual
    del bateador (Rooker BB @2.54 → perdió, ATH solo 2 BB equipo). La varianza
    individual mata la tesis colectiva (cardinals-athletics 13/05).

Conexión con la Regla de Conflicto de Tiers (A3): cuando NO hay Tipo A en el
partido, la atacabilidad del Tipo B es relativa a los frenos de tier alto
(BvP histórico, split colectivo flojo). Si esos frenos existen, el under/pass
debe liderar (dodgers-dbacks 04/06).
----------------------------------------------------------------------


### B6 — PATRÓN 3: GRANULARIDAD DE BULLPEN (REFINAR)

Estado v2.1: Patrón 3 usa "bullpen rival vulnerable/expuesto" como señal de
timing tardío sin especificar cómo evaluar el bullpen. Evidencia v2.2: 4
casos donde el AGREGADO del bullpen engañó (por rol, por composición, por
lag). (El componente "timing > precio" de este patrón ya quedó en A1.)

Decisión: REFINAR el Patrón 3 con la regla de granularidad de bullpen.

Texto propuesto para v2.2:

----------------------------------------------------------------------
PATRÓN 3 — REFINAMIENTO v2.2: no confiar en el AGREGADO del bullpen.

El ERA de equipo, el ranking ("30/30 MLB"), el rótulo "pen cansado" y el ERA
acumulado son señales agregadas que engañan. Antes de apoyar un edge en
"bullpen rival vulnerable/expuesto", desagregar:

(a) Granularidad por ROL — el agregado no distingue qué brazos cubren qué
innings:
[ ] "Bullpen cansado" requiere saber QUIÉN se usó ayer y QUIÉN no. Bulk/middle
    agotado ≠ setup/closer agotado; los high-leverage (8ª-9ª) rara vez
    participan del bullpen game previo (phillies-redsox 13/05: Whitlock +
    Chapman cerraron limpios porque no se usaron en el bulk previo).

(b) Composición — un brazo extremo infla/desinfla el agregado:
[ ] El ERA de equipo del pen sobreestima fragilidad cuando un brazo extremo
    (en IL, blow-up reciente) infla el promedio. Chequear el ERA de los 3-4
    brazos que REALMENTE cubrirían 6ª-9ª (mariners-astros 13/05: pen "6.05 ERA
    peor MLB" pero Okert 3.79 / King 3.57 / De Los Santos 4.15 cerraron
    dominante).

(c) Lagging vs leading — el ERA acumulado es lagging:
[ ] Un pen con buen ERA acumulado puede estar regresando; uno con mal ERA
    puede haber estabilizado. Pesar peripherals recientes (xFIP, K%, strand
    rate, uso) por encima del ERA acumulado (rangers-dbacks 11/05: pen elite
    por ERA contuvo; astros-cubs 24/05: HOU "30/30 MLB" había estabilizado y
    sostuvo — el análisis lo citó pero lo descartó).

Regla: antes de tomar TT over / over total / +1.5 apoyado en "bullpen rival
débil", nombrar los 2-3 brazos específicos que cubrirían los innings del edge,
su ERA/peripherals recientes y su carga de uso. Si no se puede, bajar
convicción.
----------------------------------------------------------------------

Esto cierra el CLUSTER B (refinamientos a patrones existentes). Las 3
refinaciones (B4 Patrón 11, B5 Patrón 1, B6 Patrón 3) profundizan patrones
sin agregar slots nuevos, y absorben 3 candidatos del watchlist como
sub-reglas.
