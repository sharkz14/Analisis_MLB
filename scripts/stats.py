#!/usr/bin/env python3
"""
stats.py — Reporte de recalibración del dataset MLB postmortems.

Lee data/postmortems.yaml y produce un reporte agregado en markdown con:
- Resumen de decisiones (clasificación jugada vs analítica)
- Win rate y P&L estimado de apuestas reales
- Performance por tipo de mercado y por fuente de edge
- Frecuencia de patrones v2
- Calidad del menú (picks analizadas no jugadas)
- Patrones emergentes registrados
- Divergencias entre jugada y analítica

Uso:
    python3 scripts/stats.py                       # imprime a stdout
    python3 scripts/stats.py --output reporte.md   # escribe a archivo
"""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


PATRON_NAMES = {
    1: "Tipología vulnerabilidades pitcher (A/B/C)",
    2: "'Mejor abridor' no es F5 side automático",
    3: "Timing del daño: F5 vs full game",
    4: "K upside no es over Ks si hay tráfico",
    5: "Un solo equipo con rutas → su TT",
    6: "Favorito sin edge ofensivo colectivo",
    7: "Underdog +1.5 necesita conversión",
    8: "Opener/spot starter no es fade automático",
    9: "Pitcher élite no bloquea automáticamente",
    10: "Props salen del guion, no del menú",
    11: "Factores ambientales (parque/clima/umpire)",
    12: "Side con ruido → mercado más limpio",
}


def get_apuestas(g):
    """Devuelve lista de apuestas, tanto si el partido usa apuesta singular como apuestas lista."""
    if "apuestas" in g:
        return g["apuestas"]
    if "apuesta" in g:
        return [g["apuesta"]]
    return []


def is_pass(g):
    return any(a.get("tipo_mercado") == "pass" for a in get_apuestas(g))


def get_resultado(a):
    """Para un bet object, devuelve el resultado relevante (single o pierna de parlay)."""
    return a.get("resultado") or a.get("resultado_pierna")


def section(title, level=2):
    return f"\n{'#' * level} {title}\n"


def build_report(games):
    out = []
    out.append("# MLB Postmortems — Reporte de recalibración")
    out.append("")
    out.append(f"Dataset: **{len(games)} partidos**. Fuente: `data/postmortems.yaml`.")

    # 1. Resumen de clasificaciones
    out.append(section("1. Resumen de decisiones"))

    c_jugada = Counter(g["postmortem"].get("clasificacion_jugada") for g in games)
    c_analitica = Counter(g["postmortem"].get("clasificacion_analitica") for g in games)

    out.append("**Clasificación jugada** (lo realmente apostado):")
    out.append("")
    out.append("| Clasificación | Count | % |")
    out.append("|---|---:|---:|")
    for k, v in c_jugada.most_common():
        out.append(f"| {k or '—'} | {v} | {100 * v / len(games):.0f}% |")

    out.append("")
    out.append("**Clasificación analítica** (frame del análisis):")
    out.append("")
    out.append("| Clasificación | Count | % |")
    out.append("|---|---:|---:|")
    for k, v in c_analitica.most_common():
        out.append(f"| {k or '—'} | {v} | {100 * v / len(games):.0f}% |")

    # 2. Apostar vs pasar
    out.append(section("2. Apostar vs pasar"))

    n_pass = sum(1 for g in games if is_pass(g))
    n_bet = len(games) - n_pass

    out.append(f"- Apuestas tomadas: **{n_bet}** ({100 * n_bet / len(games):.0f}%)")
    out.append(f"- Pass: **{n_pass}** ({100 * n_pass / len(games):.0f}%)")
    out.append("")

    pc = c_jugada.get("PASS_CORRECTO", 0)
    pi = c_jugada.get("PASS_INCORRECTO", 0)
    if n_pass:
        out.append(f"- Pass correctos: **{pc}/{n_pass}** ({100 * pc / n_pass:.0f}%)")
        out.append(f"- Pass incorrectos: **{pi}/{n_pass}** ({100 * pi / n_pass:.0f}%)")

    # 3. Win rate y P&L de apuestas reales
    out.append(section("3. Win rate y P&L de apuestas reales"))

    wins = losses = pushes = 0
    pnl_total = 0.0
    n_with_cuota = 0
    legs_won = legs_lost = 0

    for g in games:
        for a in get_apuestas(g):
            tm = a.get("tipo_mercado")
            if tm == "pass":
                continue
            res = get_resultado(a)
            cuota = a.get("cuota")
            formato = a.get("formato", "single")

            if res == "ganó":
                wins += 1
                if formato == "parlay_leg":
                    legs_won += 1
                if cuota and formato == "single":
                    pnl_total += cuota - 1
                    n_with_cuota += 1
            elif res == "perdió":
                losses += 1
                if formato == "parlay_leg":
                    legs_lost += 1
                if cuota and formato == "single":
                    pnl_total -= 1
                    n_with_cuota += 1
            elif res == "push":
                pushes += 1

    total = wins + losses + pushes
    if total:
        out.append(f"- Total apuestas/piernas: **{total}**")
        out.append(f"- Ganadas: **{wins}** ({100 * wins / total:.0f}%)")
        out.append(f"- Perdidas: {losses} ({100 * losses / total:.0f}%)")
        out.append(f"- Push: {pushes}")
        out.append(f"  - Piernas de parlay: {legs_won} cobraron / {legs_lost} perdieron")
        out.append("")
        if n_with_cuota:
            roi = 100 * pnl_total / n_with_cuota
            out.append(
                f"- **P&L estimado** (singles, 1u flat): **{pnl_total:+.2f}u** en {n_with_cuota} apuestas"
            )
            out.append(f"- **ROI singles**: **{roi:+.1f}%**")
            out.append("")
            out.append(
                "_Nota: P&L de parlay legs no se computa porque depende del resto del parlay, que no se registra._"
            )

    # 4. Performance por tipo de mercado
    out.append(section("4. Performance por tipo de mercado (apuestas reales)"))

    by_market = defaultdict(lambda: {"w": 0, "l": 0, "p": 0, "pnl": 0.0, "n_cuota": 0})
    for g in games:
        for a in get_apuestas(g):
            tm = a.get("tipo_mercado")
            if tm in (None, "pass"):
                continue
            res = get_resultado(a)
            cuota = a.get("cuota")
            formato = a.get("formato", "single")
            entry = by_market[tm]
            if res == "ganó":
                entry["w"] += 1
                if cuota and formato == "single":
                    entry["pnl"] += cuota - 1
                    entry["n_cuota"] += 1
            elif res == "perdió":
                entry["l"] += 1
                if cuota and formato == "single":
                    entry["pnl"] -= 1
                    entry["n_cuota"] += 1
            elif res == "push":
                entry["p"] += 1

    out.append("| Mercado | W | L | Push | P&L singles (u) |")
    out.append("|---|---:|---:|---:|---:|")
    for tm, s in sorted(by_market.items(), key=lambda x: -(x[1]["w"] - x[1]["l"])):
        pnl_str = f"{s['pnl']:+.2f}" if s["n_cuota"] else "—"
        out.append(f"| {tm} | {s['w']} | {s['l']} | {s['p']} | {pnl_str} |")

    # 5. Performance por fuente de edge
    out.append(section("5. Performance por fuente de edge"))

    by_source = defaultdict(
        lambda: dict(total=0, limpio=0, pass_ok=0, pass_bad=0, err_l=0, err_m=0, var=0)
    )
    for g in games:
        src = g["edge"].get("fuente") or "desconocida"
        clas = g["postmortem"].get("clasificacion_jugada")
        e = by_source[src]
        e["total"] += 1
        if clas == "ACIERTO_LIMPIO":
            e["limpio"] += 1
        elif clas == "PASS_CORRECTO":
            e["pass_ok"] += 1
        elif clas == "PASS_INCORRECTO":
            e["pass_bad"] += 1
        elif clas == "ERROR_DE_LECTURA":
            e["err_l"] += 1
        elif clas == "ERROR_DE_MERCADO":
            e["err_m"] += 1
        elif clas == "VARIANZA":
            e["var"] += 1

    out.append("| Fuente | N | Acierto | Pass✓ | Pass✗ | Err_Lectura | Err_Mercado | Varianza |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for src, s in sorted(by_source.items(), key=lambda x: -x[1]["total"]):
        out.append(
            f"| {src} | {s['total']} | {s['limpio']} | {s['pass_ok']} | "
            f"{s['pass_bad']} | {s['err_l']} | {s['err_m']} | {s['var']} |"
        )

    # 6. Performance por tipo de pitcher vulnerable
    out.append(section("6. Performance por tipo de pitcher vulnerable"))

    by_tipo = defaultdict(lambda: dict(total=0, limpio=0, err=0))
    for g in games:
        t = g["edge"].get("pitcher_vulnerable_tipo")
        if not t:
            continue
        clas = g["postmortem"].get("clasificacion_jugada")
        e = by_tipo[t]
        e["total"] += 1
        if clas == "ACIERTO_LIMPIO":
            e["limpio"] += 1
        if clas in ("ERROR_DE_LECTURA", "ERROR_DE_MERCADO"):
            e["err"] += 1

    if by_tipo:
        out.append("| Tipo | N | Aciertos | Errores |")
        out.append("|---|---:|---:|---:|")
        for t in sorted(by_tipo.keys()):
            s = by_tipo[t]
            out.append(f"| Tipo {t} | {s['total']} | {s['limpio']} | {s['err']} |")
    else:
        out.append("_Sin datos suficientes (campo `pitcher_vulnerable_tipo` casi siempre null)._")

    # 7. Frecuencia de patrones v2
    out.append(section("7. Frecuencia de patrones v2 aplicados"))

    pat_counter = Counter()
    for g in games:
        for p in g["patron_v2"].get("aplicable") or []:
            pat_counter[p] += 1

    out.append("| Patrón | Apariciones |")
    out.append("|---|---:|")
    for p, count in pat_counter.most_common():
        nombre = PATRON_NAMES.get(p, "?")
        out.append(f"| {p}: {nombre} | {count} |")

    # 8. Calidad del menú
    out.append(section("8. Calidad del menú: picks analizadas pero no jugadas"))

    panj = dict(total=0, ganó=0, perdió=0, push=0, pnl=0.0, n_cuota=0)
    by_panj_market = defaultdict(lambda: dict(w=0, l=0))

    for g in games:
        for p in g.get("picks_analizadas_no_jugadas") or []:
            panj["total"] += 1
            res = p.get("resultado_hipotetico")
            cuota = p.get("cuota")
            if res == "ganó":
                panj["ganó"] += 1
                if cuota:
                    panj["pnl"] += cuota - 1
                    panj["n_cuota"] += 1
            elif res == "perdió":
                panj["perdió"] += 1
                if cuota:
                    panj["pnl"] -= 1
                    panj["n_cuota"] += 1
            elif res == "push":
                panj["push"] += 1

    if panj["total"]:
        wr = 100 * panj["ganó"] / (panj["ganó"] + panj["perdió"]) if (panj["ganó"] + panj["perdió"]) else 0
        out.append(f"- Total: **{panj['total']}**")
        out.append(f"- Habrían cobrado: **{panj['ganó']}** | perdido: {panj['perdió']} | push: {panj['push']}")
        out.append(f"- Win rate (sin push): **{wr:.0f}%**")
        if panj["n_cuota"]:
            roi = 100 * panj["pnl"] / panj["n_cuota"]
            out.append(
                f"- P&L hipotético (1u flat): **{panj['pnl']:+.2f}u** en {panj['n_cuota']} con cuota → ROI **{roi:+.1f}%**"
            )

    # 9. Patrones emergentes
    out.append(section("9. Patrones emergentes registrados"))
    out.append("Hipótesis candidatas a v3 si reaparecen en partidos futuros:")
    out.append("")

    emerg = [(g["id"], g["patron_v2"]["emergente"]) for g in games if g["patron_v2"].get("emergente")]
    for i, (gid, em) in enumerate(emerg, 1):
        out.append(f"**{i}.** `{gid}`")
        out.append("")
        out.append(f"> {em}")
        out.append("")

    # 10. Divergencias jugada vs analítica
    out.append(section("10. Divergencias jugada ≠ analítica"))
    out.append("Partidos donde lo realmente apostado y el frame del análisis tienen clasificación distinta:")
    out.append("")
    out.append("| Partido | Jugada | Analítica |")
    out.append("|---|---|---|")
    diverg_count = 0
    for g in games:
        cj = g["postmortem"].get("clasificacion_jugada")
        ca = g["postmortem"].get("clasificacion_analitica")
        if cj and ca and cj != ca:
            out.append(f"| {g['id']} | {cj} | {ca} |")
            diverg_count += 1
    out.append("")
    out.append(f"_{diverg_count} partidos con divergencia (de {len(games)})._")

    # 11. Sumario operativo
    out.append(section("11. Insights operativos"))

    insights = []

    # Insight 1: pass quality
    if n_pass:
        pc_ratio = pc / n_pass
        if pc_ratio >= 0.6:
            insights.append(
                f"**Decisión de pasar es buena**: {pc}/{n_pass} pass correctos ({100 * pc_ratio:.0f}%). "
                "El instinto de no apostar correlaciona con análisis débiles."
            )
        elif pc_ratio <= 0.4:
            insights.append(
                f"**Cuidado con pasar**: solo {pc}/{n_pass} pass correctos ({100 * pc_ratio:.0f}%). "
                "Más pass perdiendo edge que evitando pérdidas."
            )

    # Insight 2: bet performance
    if n_with_cuota and total:
        roi = 100 * pnl_total / n_with_cuota if n_with_cuota else 0
        if roi > 5:
            insights.append(
                f"**Apuestas con ROI positivo**: {roi:+.1f}% en {n_with_cuota} singles con cuota."
            )
        elif roi < -5:
            insights.append(
                f"**Apuestas con ROI negativo**: {roi:+.1f}% en {n_with_cuota} singles con cuota."
            )

    # Insight 3: menu quality vs picked
    if panj["n_cuota"] and n_with_cuota:
        roi_panj = 100 * panj["pnl"] / panj["n_cuota"]
        roi_real = 100 * pnl_total / n_with_cuota
        if roi_panj > roi_real + 5:
            insights.append(
                f"**El menú considerado supera al jugado**: ROI menú {roi_panj:+.1f}% vs jugado {roi_real:+.1f}%. "
                "Sugiere que se descartan picks correctas por cuota/heurística de selección."
            )

    # Insight 4: most error-prone source
    err_by_source = {
        s: e["err_l"] + e["err_m"]
        for s, e in by_source.items()
        if e["total"] >= 3
    }
    if err_by_source:
        worst = max(err_by_source.items(), key=lambda x: x[1])
        if worst[1] >= 2:
            insights.append(
                f"**Fuente de edge más propensa a error**: `{worst[0]}` con {worst[1]} errores. Revisar antes de apostar."
            )

    # Insight 5: most successful market
    by_mkt_wr = [
        (tm, s["w"], s["l"], s["w"] / (s["w"] + s["l"]) if (s["w"] + s["l"]) else 0)
        for tm, s in by_market.items()
        if (s["w"] + s["l"]) >= 2
    ]
    if by_mkt_wr:
        best = max(by_mkt_wr, key=lambda x: x[3])
        if best[3] >= 0.6 and best[1] >= 2:
            insights.append(
                f"**Mejor mercado por win rate**: `{best[0]}` con {best[1]}-{best[2]} ({100 * best[3]:.0f}% wr)."
            )

    if not insights:
        insights.append("_Sin insights destacados todavía. Agregar más partidos para tendencias más confiables._")

    for ins in insights:
        out.append(f"- {ins}")

    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", default="data/postmortems.yaml", help="Ruta al YAML de postmortems")
    parser.add_argument("--output", default="-", help="Archivo de salida (- para stdout)")
    args = parser.parse_args()

    data = yaml.safe_load(Path(args.data).read_text())
    games = data["partidos"]
    report = build_report(games)

    if args.output == "-":
        sys.stdout.write(report)
    else:
        Path(args.output).write_text(report)
        print(f"Reporte escrito en {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
