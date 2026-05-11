# data/

Versión estructurada de los postmortems MLB. La idea es poder filtrar y contar
patrones de error sin depender de leer prosa.

Fuente prosa: `../MLB_Postmortems_Raw_040526_070526.txt`
Template canónico: `../MLB_Template_Postmortem.txt`
Heurísticas referenciadas: `../MLB_Heuristicas_Mercados_v2_040526_070526.txt`

## Archivos

- `postmortems.yaml` — un entry por partido bajo la clave `partidos:`.

## Schema (por partido)

```yaml
- id: slug-equipos-ddmmaa            # único, kebab-case
  fecha: YYYY-MM-DD
  partido: "Equipo A vs Equipo B"
  marcador: "X - Y" | null

  edge:
    frase: string                    # edge en una frase (parafraseado del raw)
    fuente: <enum fuente>            # ver vocabulario abajo
    pitcher_vulnerable_tipo: A | B | C | null

  apuesta:
    mercado: string                  # mercado literal jugado
    tipo_mercado: <enum tipo_mercado>
    resultado: ganó | perdió | push | null
    notas_apuesta: string            # opcional, si el mercado/resultado se infirió

  contexto_resultado:
    # campos libres relevantes: líneas de abridores, bates clave, factor clave, etc.

  postmortem:
    lectura_correcta: sí | no | parcialmente
    mercado_capturo_edge: sí | no | parcialmente
    clasificacion: <enum clasificación>
    mercado_correcto_retrospectiva: string | null
    tipo_mercado_correcto: <enum tipo_mercado> | null

  patron_v2:
    aplicable: [int, ...]            # números de patrón en heurísticas v2
    emergente: string | null         # patrón nuevo no listado en v2

  leccion: string                    # lección operativa en una frase
```

## Vocabularios controlados

### `edge.fuente`
Tomado de la **Jerarquía de Edges** en heurísticas v2 (de más a menos confiable):

- `parque_clima`
- `matchup_mano_repertorio`
- `leash_bullpen`
- `tipo_vulnerabilidad_pitcher`
- `forma_lineup_vs_mano`
- `umpire`
- `lineup_spot`
- `forma_individual`           — ruidoso
- `momentum`                    — el más ruidoso
- `bullpen_rival_debil`         — atajo común; suele combinarse con otros
- `edge_combinado`              — cuando el raw justifica con 3+ piezas

### `apuesta.tipo_mercado` / `tipo_mercado_correcto`

- `F5_TT` — team total primeras 5
- `F5_side` — lado primeras 5
- `F5_DNB` — lado F5 con empate devuelve
- `F5_under` — total bajo primeras 5
- `TT_full_game` — team total partido completo
- `over_under_full` — total partido completo
- `ML` — moneyline
- `run_line` — handicap -1.5/+1.5 favorito
- `run_line_underdog_1.5` — +1.5 underdog
- `prop_pitcher_Ks`
- `prop_pitcher_outs`
- `prop_pitcher_hits_allowed`
- `prop_pitcher_ER`
- `prop_bateador_bases` — total bases
- `prop_bateador_HRR_RBI` — hit + run + RBI
- `prop_bateador_RBI`
- `combo` — varios mercados jugados juntos

### `postmortem.clasificacion`
Tomado del template original:

- `ACIERTO_LIMPIO` — lectura correcta + mercado correcto + cobró
- `ACIERTO_RUIDOSO` — cobró por motivo distinto al proyectado
- `ERROR_DE_LECTURA` — la tesis era falsa
- `ERROR_DE_MERCADO` — lectura correcta, mercado mal elegido
- `VARIANZA` — lectura y mercado correctos, perdió por variance
- `PASS_CORRECTO` — no se jugó y el guion confirmó
- `PASS_INCORRECTO` — no se jugó y había edge claro

### `patron_v2.aplicable`
Referencia a los 12 patrones numerados en heurísticas v2:

1. Tipología de vulnerabilidades del pitcher (Tipo A/B/C)
2. "Mejor abridor" no es F5 side automático
3. Timing del daño: F5 vs full game
4. K upside no es over Ks si hay tráfico
5. Un solo equipo con rutas de anotación → su TT
6. Favorito sin edge ofensivo colectivo
7. Underdog +1.5 necesita conversión, no solo tráfico
8. Opener / spot starter no es fade automático
9. Pitcher élite no bloquea automáticamente
10. Props salen del guion, no del menú
11. Factores ambientales (parque, clima, umpire)
12. Side con ruido → mercado más limpio

## Cómo filtrar (ejemplos con `yq`)

```bash
# Contar por clasificación
yq '.partidos[].postmortem.clasificacion' data/postmortems.yaml | sort | uniq -c

# Errores de mercado donde el tipo correcto era F5_TT
yq '.partidos[]
  | select(.postmortem.clasificacion == "ERROR_DE_MERCADO"
       and .postmortem.tipo_mercado_correcto == "F5_TT")
  | .id' data/postmortems.yaml

# Qué patrón v2 aparece más veces
yq '.partidos[].patron_v2.aplicable[]' data/postmortems.yaml | sort | uniq -c | sort -rn

# Casos donde la fuente del edge era "bullpen rival débil" → mercado jugado
yq '.partidos[]
  | select(.edge.fuente == "bullpen_rival_debil")
  | {id: .id, mercado: .apuesta.mercado, clasificacion: .postmortem.clasificacion}' \
  data/postmortems.yaml
```

## Caveats

- Los 14 partidos fueron reconstruidos desde prosa escrita antes del template,
  así que **muchos campos están en null o son inferidos**:
  - Cuotas y stake: no aparecen en el raw, todos null.
  - Marcadores exactos: solo cuando el raw los menciona.
  - Mercado jugado: explícito en algunos casos, inferido en otros (marcado en
    `apuesta.notas_apuesta`).
  - Tipo de vulnerabilidad del pitcher: solo asignado cuando v2 da el ejemplo
    explícitamente o cuando el raw lo describe sin ambigüedad.
- Los partidos futuros se deberían escribir directamente con el template y
  agregarse acá ya estructurados, no parafraseando prosa.
- Si una entrada cambia de interpretación al releer el raw, ese es el lugar
  para discutirlo — la fuente sigue siendo el archivo prosa.
