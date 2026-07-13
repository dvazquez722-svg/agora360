"""
analytics.py
============

Motor de análisis de Performance Monitor.

Este módulo transforma datos GPS en información para la toma
de decisiones deportivas.

No contiene interfaz.
No contiene HTML.
No contiene Streamlit.

Todas las funciones públicas devuelven diccionarios que serán
utilizados por components.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from typing import Dict, List


# =============================================================================
# VARIABLES DEL MOTOR
# =============================================================================

LOAD_METRICS = [
    "player_load",
    "distance_m",
    "high_speed_distance",
    "very_high_speed_distance",
    "hmld_m",
    "mechanical_actions"
]

INTENSITY_METRICS = [
    "player_load_min",
    "distance_min",
    "energy_min",
    "metabolic_power_avg",
    "hsr_ratio",
    "high_speed_ratio",
    "sprint_ratio",
    "hmld_ratio"
]

HIGH_INTENSITY_METRICS = [
    "high_speed_distance",
    "very_high_speed_distance",
    "high_accelerations",
    "high_decelerations",
    "high_mechanical_actions"
]


# =============================================================================
# FUNCIONES PRIVADAS
# =============================================================================

def _latest_date(df: pd.DataFrame):

    return df["date"].max()


def _latest_team_data(df: pd.DataFrame):

    latest = _latest_date(df)

    return df[df["date"] == latest].copy()


def _latest_player_data(df: pd.DataFrame):

    latest = _latest_team_data(df)

    return latest.sort_values("player")


def _safe_mean(series):

    return float(series.mean()) if len(series) else 0.0


def _safe_std(series):

    value = float(series.std())

    if np.isnan(value):

        return 0

    return value


def _normalize(value, minimum, maximum):

    if maximum == minimum:

        return 0

    return (value - minimum) / (maximum - minimum)


def _inverse_normalize(value, minimum, maximum):

    return 1 - _normalize(value, minimum, maximum)


# =============================================================================
# CARGA AGUDA
# =============================================================================

def acute_load(player_df, metric):

    return player_df.tail(7)[metric].sum()


# =============================================================================
# CARGA CRÓNICA
# =============================================================================

def chronic_load(player_df, metric):

    return player_df.tail(28)[metric].sum() / 4


# =============================================================================
# ACWR
# =============================================================================

def acwr(player_df, metric):

    chronic = chronic_load(player_df, metric)

    if chronic == 0:

        return 0

    return acute_load(player_df, metric) / chronic


# =============================================================================
# EWMA
# =============================================================================

def ewma(player_df, metric, span):

    return (
        player_df[metric]
        .ewm(span=span)
        .mean()
        .iloc[-1]
    )


def ewma_ratio(player_df, metric):

    short = ewma(player_df, metric, 7)

    long = ewma(player_df, metric, 28)

    if long == 0:

        return 0

    return short / long


# =============================================================================
# MONOTONÍA
# =============================================================================

def monotony(player_df, metric):

    week = player_df.tail(7)[metric]

    sd = week.std()

    if sd == 0:

        return 0

    return week.mean() / sd


# =============================================================================
# STRAIN
# =============================================================================

def strain(player_df, metric):

    week = player_df.tail(7)[metric]

    return week.sum() * monotony(player_df, metric)


# =============================================================================
# Z SCORE
# =============================================================================

def z_score(player_df, metric):

    value = player_df.iloc[-1][metric]

    mean = player_df[metric].mean()

    std = player_df[metric].std()

    if std == 0:

        return 0

    return (value - mean) / std


# =============================================================================
# PERCENTIL INDIVIDUAL
# =============================================================================

def percentile(player_df, metric):

    value = player_df.iloc[-1][metric]

    return (
        player_df[metric]
        .rank(pct=True)
        .iloc[-1]
    )


# =============================================================================
# SCORE DE MÉTRICAS
# =============================================================================

def metric_summary(player_df, metric):

    return {

        "current": player_df.iloc[-1][metric],

        "mean": player_df[metric].mean(),

        "std": player_df[metric].std(),

        "acwr": acwr(player_df, metric),

        "ewma": ewma_ratio(player_df, metric),

        "monotony": monotony(player_df, metric),

        "strain": strain(player_df, metric),

        "z_score": z_score(player_df, metric),

        "percentile": percentile(player_df, metric)

    }

# =============================================================================
# UMBRALES DEL MOTOR
# =============================================================================

THRESHOLDS = {

    "acwr": {
        "low": 0.80,
        "optimal_low": 0.80,
        "optimal_high": 1.30,
        "high": 1.50
    },

    "ewma": {
        "optimal_low": 0.90,
        "optimal_high": 1.10,
        "high": 1.30
    },

    "z_score": {
        "normal": 1.0,
        "attention": 1.5,
        "risk": 2.0
    },

    "monotony": {
        "attention": 2.0,
        "risk": 2.5
    },

    "strain": {
        "attention": 6000,
        "risk": 8000
    }

}

# =============================================================================
# ACWR STATUS
# =============================================================================

def acwr_status(value):

    if value == 0:
        return "Sin datos"

    if value < THRESHOLDS["acwr"]["low"]:
        return "Carga baja"

    if value <= THRESHOLDS["acwr"]["optimal_high"]:
        return "Óptima"

    if value <= THRESHOLDS["acwr"]["high"]:
        return "Atención"

    return "Riesgo"

# =============================================================================
# EWMA STATUS
# =============================================================================

def ewma_status(value):

    if value == 0:
        return "Sin datos"

    if value < THRESHOLDS["ewma"]["optimal_low"]:
        return "Baja"

    if value <= THRESHOLDS["ewma"]["optimal_high"]:
        return "Normal"

    if value <= THRESHOLDS["ewma"]["high"]:
        return "Alta"

    return "Muy alta"

# =============================================================================
# Z SCORE STATUS
# =============================================================================

def zscore_status(value):

    value = abs(value)

    if value < THRESHOLDS["z_score"]["normal"]:
        return "Normal"

    if value < THRESHOLDS["z_score"]["attention"]:
        return "Atención"

    if value < THRESHOLDS["z_score"]["risk"]:
        return "Alta"

    return "Muy alta"

# =============================================================================
# MONOTONY STATUS
# =============================================================================

def monotony_status(value):

    if value < THRESHOLDS["monotony"]["attention"]:
        return "Normal"

    if value < THRESHOLDS["monotony"]["risk"]:
        return "Atención"

    return "Riesgo"

# =============================================================================
# STRAIN STATUS
# =============================================================================

def strain_status(value):

    if value < THRESHOLDS["strain"]["attention"]:
        return "Normal"

    if value < THRESHOLDS["strain"]["risk"]:
        return "Atención"

    return "Riesgo"

# =============================================================================
# SCORE ACWR
# =============================================================================

def acwr_score(value):

    if value == 0:
        return 0

    if 0.8 <= value <= 1.3:
        return 100

    if 0.7 <= value < 0.8:
        return 85

    if 1.3 < value <= 1.5:
        return 70

    if 0.6 <= value < 0.7:
        return 55

    return 25

# =============================================================================
# SCORE EWMA
# =============================================================================

def ewma_score(value):

    if value == 0:
        return 0

    if 0.9 <= value <= 1.1:
        return 100

    if 0.8 <= value < 0.9:
        return 85

    if 1.1 < value <= 1.2:
        return 75

    if 1.2 < value <= 1.3:
        return 55

    return 25

# =============================================================================
# SCORE Z SCORE
# =============================================================================

def zscore_score(value):

    value = abs(value)

    if value < 1:
        return 100

    if value < 1.5:
        return 80

    if value < 2:
        return 60

    return 25

# =============================================================================
# GLOBAL METRIC SCORE
# =============================================================================

def metric_score(player_df, metric):

    summary = metric_summary(player_df, metric)

    score = np.mean([

        acwr_score(summary["acwr"]),

        ewma_score(summary["ewma"]),

        zscore_score(summary["z_score"])

    ])

    return {

        "metric": metric,

        "score": round(score,1),

        "summary": summary,

        "status": acwr_status(summary["acwr"])

    }

# =============================================================================
# MÉTRICAS ANALIZADAS
# =============================================================================

ANALYSIS_METRICS = [

    "player_load",

    "distance_m",

    "high_speed_distance",

    "very_high_speed_distance",

    "hmld_m",

    "mechanical_actions"

]

# =============================================================================
# PESOS DEL MOTOR
# =============================================================================

METRIC_WEIGHTS = {

    "player_load": 0.25,

    "distance_m": 0.15,

    "high_speed_distance": 0.20,

    "very_high_speed_distance": 0.15,

    "hmld_m": 0.15,

    "mechanical_actions": 0.10

}

# =============================================================================
# NOMBRES DE LAS MÉTRICAS
# =============================================================================

METRIC_LABELS = {

    "player_load": "Player Load",

    "distance_m": "Distancia",

    "high_speed_distance": "HSR",

    "very_high_speed_distance": "VHSR",

    "hmld_m": "HMLD",

    "mechanical_actions": "Acciones Mecánicas"

}

# =============================================================================
# PLAYER EXPLANATION
# =============================================================================

def _explain_player(metrics: dict) -> str:
    """
    Devuelve la principal causa del estado del jugador
    según las métricas analizadas.
    """

    explanations = []

    for metric, result in metrics.items():

        metric_label = METRIC_LABELS.get(metric, metric)

        summary = result["summary"]

        if summary["acwr"] > THRESHOLDS["acwr"]["high"]:

            explanations.append(
                (
                    summary["acwr"],
                    f"{metric_label} elevado (ACWR {summary['acwr']:.2f})"
                )
            )

        elif summary["ewma"] > THRESHOLDS["ewma"]["high"]:

            explanations.append(
                (
                    summary["ewma"],
                    f"{metric_label} en incremento reciente (EWMA {summary['ewma']:.2f})"
                )
            )

        elif abs(summary["z_score"]) > THRESHOLDS["z_score"]["risk"]:

            explanations.append(
                (
                    abs(summary["z_score"]),
                    f"{metric_label} fuera de su patrón habitual (Z {summary['z_score']:.2f})"
                )
            )

    if len(explanations) == 0:

        return "Carga dentro de los rangos esperados."

    explanations.sort(reverse=True)

    return explanations[0][1]

# =============================================================================
# WORKLOAD ENGINE · HISTORY
# =============================================================================

def player_history(
    df: pd.DataFrame,
    player: str
) -> pd.DataFrame:
    """
    Histórico completo del jugador.
    """

    history = (
        df[df["player"] == player]
        .sort_values("date")
        .reset_index(drop=True)
    )

    return history


def team_history(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Histórico completo del equipo.
    """

    return (
        df
        .sort_values("date")
        .reset_index(drop=True)
    )


def position_history(
    df: pd.DataFrame,
    position: str
) -> pd.DataFrame:
    """
    Histórico completo de una posición.
    """

    return (
        df[df["position"] == position]
        .sort_values("date")
        .reset_index(drop=True)
    )


def group_history(
    df: pd.DataFrame,
    group: str
) -> pd.DataFrame:
    """
    Histórico completo de un grupo de entrenamiento.
    """

    return (
        df[df["group"] == group]
        .sort_values("date")
        .reset_index(drop=True)
    )

# =============================================================================
# WORKLOAD ENGINE · WINDOWS
# =============================================================================

def last_sessions(
    history: pd.DataFrame,
    sessions: int = 5
) -> pd.DataFrame:
    """
    Últimas N sesiones.
    """

    return history.tail(sessions).copy()


def last_days(
    history: pd.DataFrame,
    days: int = 7
) -> pd.DataFrame:
    """
    Últimos N días naturales.
    """

    if history.empty:
        return history

    last_date = history["date"].max()

    start_date = last_date - pd.Timedelta(days=days)

    return history[
        history["date"] >= start_date
    ].copy()


def full_season(
    history: pd.DataFrame
) -> pd.DataFrame:
    """
    Toda la temporada.
    """

    return history.copy()

# =============================================================================
# WORKLOAD ENGINE · STATISTICS
# =============================================================================

def metric_stats(
    history: pd.DataFrame,
    metric: str
) -> dict:

    values = history[metric].dropna()

    if values.empty:

        return {}

    return {

        "current": float(values.iloc[-1]),

        "mean": float(values.mean()),

        "median": float(values.median()),

        "minimum": float(values.min()),

        "maximum": float(values.max()),

        "std": float(values.std()),

        "count": int(values.count())

    }

# =============================================================================
# WORKLOAD ENGINE · TREND
# =============================================================================

def metric_trend(
    history: pd.DataFrame,
    metric: str
):

    values = history[metric].dropna()

    if len(values) < 2:

        return {

            "variation": 0,

            "trend": "Estable"

        }

    current = values.iloc[-1]

    previous = values.iloc[:-1].mean()

    if previous == 0:

        variation = 0

    else:

        variation = round(
            (current - previous)
            / previous
            * 100,
            1
        )

    if variation > 5:

        trend = "Subiendo"

    elif variation < -5:

        trend = "Bajando"

    else:

        trend = "Estable"

    return {

        "variation": variation,

        "trend": trend

    }

## =============================================================================
# WORKLOAD SUMMARY
# =============================================================================

def build_workload_summary(
    df: pd.DataFrame,
    player: str,
    metric: str,
    window_type: str = "sessions",
    window_size: int = 5
) -> dict:
    """
    Construye un resumen completo de una métrica de carga.

    Devuelve toda la información necesaria para los paneles
    de evolución y comparación.
    """

    # ---------------------------------------------------------
    # HISTÓRICO
    # ---------------------------------------------------------

    history = player_history(
        df,
        player
    )

    if history.empty:

        return {}

    # ---------------------------------------------------------
    # VENTANA
    # ---------------------------------------------------------

    if window_type == "days":

        window = last_days(
            history,
            window_size
        )

    elif window_type == "season":

        window = full_season(
            history
        )

    else:

        window = last_sessions(
            history,
            window_size
        )

    if window.empty:

        return {}

    # =========================================================
    # FECHAS DE LA VENTANA
    # =========================================================

    window_dates = window["date"].unique()

    # ---------------------------------------------------------
    # ESTADÍSTICOS
    # ---------------------------------------------------------

    stats = metric_stats(
        window,
        metric
    )

    # ---------------------------------------------------------
    # TENDENCIA
    # ---------------------------------------------------------

    trend = metric_trend(
        window,
        metric
    )

    # ---------------------------------------------------------
    # COMPARACIÓN EQUIPO
    # ---------------------------------------------------------

    team = team_comparison(
        df,
        player,
        metric,
        window_size
    )

    # ---------------------------------------------------------
    # COMPARACIÓN POSICIÓN
    # ---------------------------------------------------------

    position = position_comparison(
        df,
        player,
        metric,
        window_size
    )

    # =========================================================
    # SERIES PARA EL GRÁFICO
    # =========================================================

    # Jugador

    player_series = (

        window[["date", metric]]

        .rename(columns={metric: "player"})

    )

    # Posición del jugador

    position_name = history.iloc[-1]["position"]

    # Media del equipo en las mismas fechas

    team_data = (

        df[
            df["date"].isin(window_dates)
        ]

        .groupby("date", as_index=False)[metric]

        .mean()

        .rename(columns={metric: "team"})

    )

    # Media de la posición en las mismas fechas

    position_data = (

        df[
            (df["position"] == position_name)
            &
            (df["date"].isin(window_dates))
        ]

        .groupby("date", as_index=False)[metric]

        .mean()

        .rename(columns={metric: "position"})

    )
    
    # ---------------------------------------------------------
    # RESULTADO
    # ---------------------------------------------------------

    return {

        # Identificación

        "player": player,

        "metric": metric,

        # Ventana

        "window_type": window_type,

        "window_size": window_size,

        # Datos

        "history": history,

        "window": window,

        # Análisis

        "stats": stats,

        "trend": trend,

        # Comparaciones

        "team": team,

        "position": position,
        
        "player_series": player_series,

        "team_series": team_data,

        "position_series": position_data,       

    }

# =============================================================================
# WORKLOAD INTERPRETATION
# =============================================================================

def build_workload_interpretation(
    workload: dict
) -> dict:
    """
    Genera una interpretación automática de una métrica
    de carga de trabajo.
    """

    if not workload:

        return {}

    stats = workload["stats"]

    trend = workload["trend"]

    team = workload["team"]

    position = workload["position"]

    metric = METRIC_LABELS.get(
        workload["metric"],
        workload["metric"]
    )

    # ==========================================================
    # TÍTULO
    # ==========================================================

    title = metric

    # ==========================================================
    # TENDENCIA
    # ==========================================================

    variation = trend["variation"]

    if trend["trend"] == "Subiendo":

        trend_text = (
            f"{metric} ha aumentado un "
            f"{abs(variation):.1f}% durante el periodo analizado."
        )

    elif trend["trend"] == "Bajando":

        trend_text = (
            f"{metric} ha disminuido un "
            f"{abs(variation):.1f}% durante el periodo analizado."
        )

    else:

        trend_text = (
            f"{metric} permanece estable durante el periodo analizado."
        )

    # ==========================================================
    # COMPARACIÓN EQUIPO
    # ==========================================================

    diff = team["difference"]

    if diff > 5:

        comparison = (
            "Se encuentra claramente por encima de la media del equipo."
        )

    elif diff > 1:

        comparison = (
            "Se sitúa ligeramente por encima de la media del equipo."
        )

    elif diff < -5:

        comparison = (
            "Se encuentra claramente por debajo de la media del equipo."
        )

    elif diff < -1:

        comparison = (
            "Se sitúa ligeramente por debajo de la media del equipo."
        )

    else:

        comparison = (
            "Presenta valores muy similares a la media del equipo."
        )

    # ==========================================================
    # PERCENTIL
    # ==========================================================

    percentile = team["percentile"]

    percentile_text = (
        f"Percentil {percentile:.0f} respecto al equipo."
    )

    # ==========================================================
    # POSICIÓN
    # ==========================================================

    position_text = (
        f"Comparado con su posición ({position['position']}), "
        f"se sitúa en el percentil {position['percentile']:.0f}."
    )

    # ==========================================================
    # RECOMENDACIÓN
    # ==========================================================

    if trend["trend"] == "Subiendo" and percentile >= 80:

        recommendation = (
            "Conviene controlar la evolución durante las próximas sesiones."
        )

    elif trend["trend"] == "Subiendo":

        recommendation = (
            "Mantener seguimiento para confirmar la tendencia."
        )

    elif trend["trend"] == "Bajando":

        recommendation = (
            "Valorar si la reducción responde a la planificación prevista."
        )

    else:

        recommendation = (
            "No se requieren modificaciones específicas."
        )

    # ==========================================================
    # RESULTADO
    # ==========================================================

    return {

        "title": title,

        "trend": trend_text,

        "comparison": comparison,

        "percentile": percentile_text,

        "position": position_text,

        "recommendation": recommendation

    }

# =============================================================================
# TEAM COMPARISON
# =============================================================================

def team_comparison(
    df: pd.DataFrame,
    player: str,
    metric: str,
    window_size: int = 5
) -> dict:
    """
    Compara un jugador con la media del equipo utilizando
    las últimas N sesiones de cada jugador.
    """

    players = sorted(df["player"].unique())

    values = []

    player_value = None

    for p in players:

        history = player_history(df, p)

        history = last_sessions(history, window_size)

        if history.empty:
            continue

        value = history[metric].mean()

        values.append(value)

        if p == player:
            player_value = value

    if player_value is None or len(values) == 0:

        return {}

    values = pd.Series(values)

    percentile = round(
        values.rank(pct=True)[values == player_value].max() * 100,
        1
    )

    return {

        "player_mean": round(player_value, 1),

        "team_mean": round(values.mean(), 1),

        "difference": round(player_value - values.mean(), 1),

        "percentile": percentile

    }

# =============================================================================
# POSITION COMPARISON
# =============================================================================

def position_comparison(
    df: pd.DataFrame,
    player: str,
    metric: str,
    window_size: int = 5
) -> dict:
    """
    Compara un jugador con los jugadores de su posición.
    """

    player_info = df[df["player"] == player]

    if player_info.empty:
        return {}

    position = player_info.iloc[-1]["position"]

    position_players = sorted(

        df[df["position"] == position]["player"].unique()

    )

    values = []

    player_value = None

    for p in position_players:

        history = player_history(df, p)

        history = last_sessions(history, window_size)

        if history.empty:
            continue

        value = history[metric].mean()

        values.append(value)

        if p == player:
            player_value = value

    if player_value is None or len(values) == 0:

        return {}

    values = pd.Series(values)

    percentile = round(

        values.rank(pct=True)[values == player_value].max()

        * 100,

        1

    )

    return {

        "position": position,

        "position_mean": round(values.mean(), 1),

        "player_mean": round(player_value, 1),

        "difference": round(player_value - values.mean(), 1),

        "percentile": percentile

    }


# =============================================================================
# PLAYER SUMMARY
# =============================================================================

def player_summary(df: pd.DataFrame, player: str) -> dict:
    """
    Genera el resumen completo de un jugador.

    Devuelve:
    - Score global
    - Estado
    - Riesgo
    - Prioridad
    - Todas las métricas analizadas
    """

    player_df = (
        df[df["player"] == player]
        .sort_values("date")
        .reset_index(drop=True)
    )

    if player_df.empty:
        return {}

    # ==========================================================
    # MÉTRICAS
    # ==========================================================

    metrics = {}

    weighted_score = 0

    risk_flags = 0

    for metric, weight in METRIC_WEIGHTS.items():

        result = metric_score(player_df, metric)

        metrics[metric] = result

        weighted_score += result["score"] * weight

        if result["summary"]["acwr"] > THRESHOLDS["acwr"]["high"]:
            risk_flags += 1

        if result["summary"]["ewma"] > THRESHOLDS["ewma"]["high"]:
            risk_flags += 1

        if abs(result["summary"]["z_score"]) > THRESHOLDS["z_score"]["risk"]:
            risk_flags += 1

    # ==========================================================
    # SCORE GLOBAL
    # ==========================================================

    overall_score = round(weighted_score, 1)

    status = player_status(overall_score)

    # ==========================================================
    # RIESGO
    # ==========================================================

    if risk_flags <= 2:

        risk = "Bajo"

    elif risk_flags <= 5:

        risk = "Moderado"

    elif risk_flags <= 8:

        risk = "Alto"

    else:

        risk = "Muy Alto"

    risk_level = {

        "Bajo": 1,

        "Moderado": 2,

        "Alto": 3,

        "Muy Alto": 4

    }[risk]

    # ==========================================================
    # DECISIÓN
    # ==========================================================

    decision = player_decision(

        overall_score,

        risk

    )

    # ==========================================================
    # INFORMACIÓN ACTUAL
    # ==========================================================

    latest = player_df.iloc[-1]

    reason = _explain_player(metrics)

    # ==========================================================
    # RESUMEN
    # ==========================================================

    summary = {

        "player": player,

        "team": latest["team"],

        "position": latest["position"],

        "date": latest["date"],

        "overall_score": overall_score,

        "status": status["label"],

        "color": status["color"],

        "risk": risk,

        "risk_level": risk_level,

        "risk_flags": risk_flags,

        "max_risk_flags": len(METRIC_WEIGHTS) * 3,

        "reason": reason,

        "metrics": metrics,

        "decision": decision

    }

    # ==========================================================
    # INFORME IA
    # ==========================================================

    summary["report"] = generate_player_report(summary)

    return summary

# =============================================================================
# PLAYER REPORT
# =============================================================================

def generate_player_report(player: dict) -> dict:
    """
    Genera un informe estructurado del jugador.
    """

    if player["risk"] == "Muy Alto":

        title = "Estado crítico"
        priority = "Alta"
        color = "#DC2626"

    elif player["risk"] == "Alto":

        title = "Atención"
        priority = "Alta"
        color = "#EA580C"

    elif player["risk"] == "Moderado":

        title = "Seguimiento"
        priority = "Media"
        color = "#CA8A04"

    else:

        title = "Estado óptimo"
        priority = "Normal"
        color = "#16A34A"

    summary = " ".join([

        build_intro(player),

        build_analysis(player),

        build_explanation(player)

    ])

    recommendation = build_recommendation(player)

    return {

        "title": title,

        "summary": summary,

        "recommendation": recommendation,

        "priority": priority,

        "color": color

    }

# =============================================================================
# TEAM SUMMARY
# =============================================================================

def team_summary(df: pd.DataFrame) -> list:
    """
    Devuelve el resumen de todos los jugadores del equipo.
    """

    players = sorted(df["player"].unique())

    summary = []

    for player in players:

        summary.append(
            player_summary(df, player)
        )

    return summary

# =============================================================================
# TEAM STATUS
# =============================================================================

def get_team_status(df: pd.DataFrame) -> dict:
    """
    Estado general del equipo.
    """

    players = team_summary(df)

    scores = [p["overall_score"] for p in players]

    team_score = round(np.mean(scores), 1)

    if team_score >= 85:

        label = "Excelente"
        color = "#22C55E"

    elif team_score >= 75:

        label = "Bueno"
        color = "#84CC16"

    elif team_score >= 65:

        label = "Aceptable"
        color = "#FACC15"

    elif team_score >= 55:

        label = "Comprometido"
        color = "#F97316"

    else:

        label = "Crítico"
        color = "#EF4444"

    return {

        "value": team_score,

        "label": label,

        "color": color,

        "description": (
            f"El estado general del equipo es {label.lower()}."
        )

    }

# =============================================================================
# TEAM AVAILABILITY
# =============================================================================

def get_team_availability(df: pd.DataFrame):

    players = team_summary(df)

    available = [

        p for p in players

        if p["overall_score"] >= 70

    ]

    percentage = round(

        len(available) / len(players) * 100

    )

    return {

        "title":"Disponibilidad",

        "value":f"{percentage}%",

        "description":f"{len(available)} de {len(players)} jugadores disponibles",

        "color":"#22C55E"

    }

# =============================================================================
# TEAM RISK
# =============================================================================

def get_team_risk(df):

    players = team_summary(df)

    risk = sum(

        p["risk"] in ["Alto","Muy Alto"]

        for p in players

    )

    if risk == 0:

        label="Muy bajo"

        color="#22C55E"

    elif risk <=2:

        label="Bajo"

        color="#84CC16"

    elif risk <=4:

        label="Moderado"

        color="#FACC15"

    elif risk <=6:

        label="Alto"

        color="#F97316"

    else:

        label="Muy alto"

        color="#EF4444"

    return{

        "title":"Riesgo",

        "value":label,

        "description":f"{risk} jugadores con riesgo elevado.",

        "color":color

    }

# =============================================================================
# TEAM FATIGUE
# =============================================================================

def get_team_fatigue(df):

    players = team_summary(df)

    fatigue = np.mean(

        [

            100-p["overall_score"]

            for p in players

        ]

    )

    fatigue = round(fatigue,1)

    if fatigue <20:

        label="Muy baja"

        color="#22C55E"

    elif fatigue<30:

        label="Baja"

        color="#84CC16"

    elif fatigue<40:

        label="Moderada"

        color="#FACC15"

    elif fatigue<50:

        label="Alta"

        color="#F97316"

    else:

        label="Muy alta"

        color="#EF4444"

    return{

        "title":"Fatiga",

        "value":label,

        "description":"Estimación basada en indicadores GPS.",

        "color":color

    }

# =============================================================================
# PLAYER STATUS
# =============================================================================

def player_status(score):

    if score >= 85:

        return {

            "label":"Óptimo",

            "color":"#22C55E"

        }

    if score >= 70:

        return {

            "label":"Bueno",

            "color":"#84CC16"

        }

    if score >= 55:

        return {

            "label":"Atención",

            "color":"#FACC15"

        }

    if score >= 40:

        return {

            "label":"Riesgo",

            "color":"#F97316"

        }

    return {

        "label":"Crítico",

        "color":"#EF4444"

    }

# =============================================================================
# PLAYER DECISION
# =============================================================================

def player_decision(
    overall_score: float,
    risk: str
) -> dict:
    """
    Determina la decisión deportiva del jugador.
    """

    decision = {

        "availability": "Disponible",

        "action": "Mantener",

        "priority": False,

        "monitoring": False,

        "restriction": None,

        "decision_level": "Normal"

    }

    # ---------------------------------------------------------
    # Riesgo muy alto
    # ---------------------------------------------------------

    if risk == "Muy Alto":

        decision.update({

            "availability": "No disponible",

            "action": "Recuperación",

            "priority": True,

            "monitoring": True,

            "restriction": "Sin tareas de alta intensidad",

            "decision_level": "Crítico"

        })

        return decision

    # ---------------------------------------------------------
    # Riesgo alto
    # ---------------------------------------------------------

    if risk == "Alto":

        decision.update({

            "availability": "Adaptado",

            "action": "Reducir",

            "priority": True,

            "monitoring": True,

            "restriction": "Reducir volumen e intensidad",

            "decision_level": "Alto"

        })

        return decision

    # ---------------------------------------------------------
    # Score bajo
    # ---------------------------------------------------------

    if overall_score < 70:

        decision.update({

            "availability": "Control",

            "action": "Control",

            "priority": True,

            "monitoring": True,

            "restriction": "Control individual",

            "decision_level": "Moderado"

        })

        return decision

    # ---------------------------------------------------------
    # Score medio
    # ---------------------------------------------------------

    if overall_score < 85:

        decision.update({

            "availability": "Disponible",

            "action": "Mantener",

            "priority": False,

            "monitoring": False,

            "restriction": None,

            "decision_level": "Normal"

        })

        return decision

    # ---------------------------------------------------------
    # Score excelente
    # ---------------------------------------------------------

    decision.update({

        "availability": "Disponible",

        "action": "Aumentar",

        "priority": False,

        "monitoring": False,

        "restriction": None,

        "decision_level": "Óptimo"

    })

    return decision


# =============================================================================
# PLAYER REPORT
# =============================================================================

def build_intro(player: dict) -> str:

    name = player["player"]

    if player["status"] == "Óptimo":

        return (
            f"{name} presenta un estado físico óptimo y puede afrontar la sesión prevista sin limitaciones."
        )

    if player["status"] == "Bueno":

        return (
            f"{name} mantiene un buen estado físico y está preparado para completar la planificación prevista."
        )

    if player["status"] == "Aceptable":

        return (
            f"{name} presenta un estado físico aceptable, aunque conviene controlar su respuesta durante la sesión."
        )

    if player["status"] == "Comprometido":

        return (
            f"{name} muestra signos de fatiga y requiere una planificación más conservadora."
        )

    return (
        f"{name} presenta un estado físico comprometido y requiere una gestión muy prudente de la carga."
    )

def build_analysis(player: dict) -> str:

    if player["risk"] == "Muy Alto":

        return (
            "Los indicadores de carga reflejan una situación de riesgo muy elevada que aconseja limitar la exposición al entrenamiento."
        )

    if player["risk"] == "Alto":

        return (
            "La carga reciente aconseja reducir la exigencia prevista para minimizar el riesgo."
        )

    if player["risk"] == "Moderado":

        return (
            "Existe un riesgo moderado y resulta recomendable mantener un seguimiento específico durante las próximas sesiones."
        )

    return (
        "La carga reciente permanece dentro de los valores habituales del jugador."
    )

def build_explanation(player: dict) -> str:

    if player["reason"] == "Carga dentro de los rangos esperados.":

        return (
            "No se detectan desviaciones relevantes respecto a su comportamiento habitual."
        )

    return (
        f"El principal indicador observado es {player['reason'].lower()}."
    )

def build_recommendation(player: dict) -> str:

    recommendations = {

        "Aumentar":
            "Puede incrementarse la carga si los objetivos de la sesión lo requieren.",

        "Mantener":
            "Se recomienda mantener la planificación prevista.",

        "Control":
            "Se aconseja un seguimiento individual durante la sesión.",

        "Reducir":
            "Conviene reducir la carga prevista y controlar especialmente las tareas de alta intensidad.",

        "Recuperación":
            "La prioridad debe centrarse en la recuperación antes de incrementar nuevamente la carga."

    }

    return recommendations[player["decision"]["action"]]

# =============================================================================
# PLAYER ANALYSIS
# =============================================================================

def analyse_player(df, player):

    summary = player_summary(df, player)

    status = player_status(summary["overall_score"])

    summary["status"] = status["label"]

    summary["color"] = status["color"]

    return summary

# =============================================================================
# TEAM ANALYSIS
# =============================================================================

def analyse_team(df):

    players = sorted(df["player"].unique())

    results = []

    for player in players:

        results.append(

            analyse_player(df, player)

        )

    return results

# =============================================================================
# TEAM RANKING
# =============================================================================

def team_ranking(df):

    ranking = analyse_team(df)

    ranking = sorted(

        ranking,

        key=lambda x: x["overall_score"],

        reverse=False

    )

    return ranking

# =============================================================================
# PRIORITY PLAYERS
# =============================================================================

def priority_players(df, n=5):

    ranking = team_ranking(df)

    return ranking[:n]

# =============================================================================
# AVAILABILITY
# =============================================================================

def availability(df):

    ranking = analyse_team(df)

    available = [

        p for p in ranking

        if p["overall_score"] >= 70

    ]

    percentage = len(available) / len(ranking)

    return {

        "value": round(percentage*100),

        "players": len(available),

        "total": len(ranking)

    }

# =============================================================================
# PRIORITY PLAYERS
# =============================================================================

def get_priority_players(
    df: pd.DataFrame,
    top_n: int = 5
) -> list:
    """
    Devuelve los jugadores que requieren mayor atención.

    Prioridad de orden:
    1. Riesgo
    2. Prioridad
    3. Score global
    """

    players = team_summary(df)

    risk_order = {
        "Muy Alto": 4,
        "Alto": 3,
        "Moderado": 2,
        "Bajo": 1
    }

    players = sorted(

        players,

        key=lambda x: (

            risk_order.get(x["risk"], 0),

            x["decision"]["priority"],

            -x["overall_score"]

        ),

        reverse=True

    )

    priority = []

    for player in players:

        if not player["decision"]["priority"]:
            continue

        priority.append({

            "player": player["player"],

            "position": player["position"],

            "score": player["overall_score"],

            "risk": player["risk"],

            "reason": player["reason"],

            "color": player["color"]

        })

        if len(priority) >= top_n:
            break

    return priority

# =============================================================================
# ALERTS
# =============================================================================

def get_alerts(df: pd.DataFrame) -> list:
    """
    Genera las alertas colectivas del equipo.
    """

    players = team_summary(df)

    alerts = []

    # ----------------------------------------------------------
    # Riesgo alto
    # ----------------------------------------------------------

    high_risk = [

        p for p in players

        if p["risk"] in ["Alto", "Muy Alto"]

    ]

    if high_risk:

        alerts.append({

            "title": "Jugadores con riesgo elevado",

            "description": (
                f"{len(high_risk)} jugadores presentan un riesgo alto "
                "según los indicadores de carga."
            ),

            "color": "#EF4444"

        })

    # ----------------------------------------------------------
    # ACWR elevado
    # ----------------------------------------------------------

    acwr_players = 0

    for player in players:

        for metric in player["metrics"].values():

            if metric["summary"]["acwr"] > THRESHOLDS["acwr"]["high"]:

                acwr_players += 1

                break

    if acwr_players:

        alerts.append({

            "title": "ACWR elevado",

            "description": (
                f"{acwr_players} jugadores superan el umbral de ACWR."
            ),

            "color": "#F97316"

        })

    # ----------------------------------------------------------
    # EWMA elevada
    # ----------------------------------------------------------

    ewma_players = 0

    for player in players:

        for metric in player["metrics"].values():

            if metric["summary"]["ewma"] > THRESHOLDS["ewma"]["high"]:

                ewma_players += 1

                break

    if ewma_players:

        alerts.append({

            "title": "Incremento reciente de carga",

            "description": (
                f"{ewma_players} jugadores muestran un incremento "
                "rápido de la carga (EWMA)."
            ),

            "color": "#FACC15"

        })

    # ----------------------------------------------------------
    # Monotonía
    # ----------------------------------------------------------

    monotony_players = 0

    for player in players:

        for metric in player["metrics"].values():

            if metric["summary"]["monotony"] > THRESHOLDS["monotony"]["risk"]:

                monotony_players += 1

                break

    if monotony_players:

        alerts.append({

            "title": "Monotonía elevada",

            "description": (
                f"{monotony_players} jugadores presentan una "
                "monotonía semanal elevada."
            ),

            "color": "#FACC15"

        })

    # ----------------------------------------------------------
    # Strain
    # ----------------------------------------------------------

    strain_players = 0

    for player in players:

        for metric in player["metrics"].values():

            if metric["summary"]["strain"] > THRESHOLDS["strain"]["risk"]:

                strain_players += 1

                break

    if strain_players:

        alerts.append({

            "title": "Strain elevado",

            "description": (
                f"{strain_players} jugadores presentan una carga "
                "semanal acumulada elevada."
            ),

            "color": "#F97316"

        })

    # ----------------------------------------------------------
    # Sin alertas
    # ----------------------------------------------------------

    if len(alerts) == 0:

        alerts.append({

            "title": "Sin alertas",

            "description": (
                "No se han detectado situaciones relevantes "
                "en el equipo."
            ),

            "color": "#22C55E"

        })

    return alerts

# =============================================================================
# RECOMMENDATION
# =============================================================================

def generate_recommendation(df: pd.DataFrame) -> dict:
    """
    Genera una recomendación automática para la sesión del día.
    """

    status = get_team_status(df)

    risk = get_team_risk(df)

    priority = get_priority_players(df)

    recommendation = []

    # ----------------------------------------------------------
    # Estado colectivo
    # ----------------------------------------------------------

    if status["value"] >= 85:

        recommendation.append(
            "El estado general del equipo es excelente."
        )

    elif status["value"] >= 75:

        recommendation.append(
            "El equipo presenta un buen nivel de preparación."
        )

    elif status["value"] >= 65:

        recommendation.append(
            "El estado del equipo es aceptable, aunque conviene monitorizar la sesión."
        )

    else:

        recommendation.append(
            "El estado colectivo aconseja reducir la carga global."
        )

    # ----------------------------------------------------------
    # Riesgo colectivo
    # ----------------------------------------------------------

    if risk["value"] in ["Alto", "Muy alto"]:

        recommendation.append(
            "Existen varios jugadores con riesgo elevado que requieren seguimiento individual."
        )

    # ----------------------------------------------------------
    # Jugadores prioritarios
    # ----------------------------------------------------------

    if len(priority):

        names = ", ".join(

            p["player"]

            for p in priority[:3]

        )

        recommendation.append(

            f"Se recomienda controlar especialmente a {names}."

        )

    # ----------------------------------------------------------
    # Texto final
    # ----------------------------------------------------------

    text = " ".join(recommendation)

    return {

        "title": "Recomendación automática",

        "text": text,

        "color": status["color"]

    }

# =============================================================================
# DAILY DECISION
# =============================================================================

def generate_daily_decision(df: pd.DataFrame) -> dict:
    """
    Genera la decisión operativa del día para el cuerpo técnico.
    """

    status = get_team_status(df)

    risk = get_team_risk(df)

    priority = get_priority_players(df)

    availability = get_team_availability(df)

    score = status["value"]

    high_risk = sum(
        p["risk"] in ["Alto", "Muy Alto"]
        for p in team_summary(df)
    )

    # ----------------------------------------------------------
    # CASO 1
    # Excelente
    # ----------------------------------------------------------

    if score >= 85 and high_risk == 0:

        decision = (
            "Mantener la planificación prevista. "
            "No se detectan jugadores que requieran una modificación "
            "individual de la carga."
        )

        color = "#22C55E"

    # ----------------------------------------------------------
    # CASO 2
    # Bueno
    # ----------------------------------------------------------

    elif score >= 75 and high_risk <= 2:

        names = ", ".join(
            p["player"]
            for p in priority[:2]
        )

        decision = (
            "Mantener la planificación colectiva. "
            f"Controlar de forma individual a {names} "
            "durante las tareas de mayor exigencia."
        )

        color = "#84CC16"

    # ----------------------------------------------------------
    # CASO 3
    # Intermedio
    # ----------------------------------------------------------

    elif score >= 65:

        names = ", ".join(
            p["player"]
            for p in priority[:3]
        )

        decision = (
            "Reducir ligeramente la carga de los jugadores prioritarios. "
            f"Especial atención a {names}. "
            "Monitorizar la respuesta durante la sesión."
        )

        color = "#FACC15"

    # ----------------------------------------------------------
    # CASO 4
    # Riesgo elevado
    # ----------------------------------------------------------

    elif score >= 55:

        names = ", ".join(
            p["player"]
            for p in priority[:4]
        )

        decision = (
            "Modificar parcialmente la planificación prevista. "
            "Reducir volumen e intensidad en los jugadores "
            f"{names}. "
            "Evitar una exposición elevada a esfuerzos de alta intensidad."
        )

        color = "#F97316"

    # ----------------------------------------------------------
    # CASO 5
    # Estado crítico
    # ----------------------------------------------------------

    else:

        decision = (
            "No se recomienda realizar la sesión planificada. "
            "Reducir significativamente la carga colectiva "
            "y priorizar tareas regenerativas o de recuperación."
        )

        color = "#EF4444"

    return {

        "title": "Decisión del día",

        "decision": decision,

        "color": color,

        "team_score": score,

        "availability": availability["value"],

        "high_risk_players": high_risk

    }

# =============================================================================
# DASHBOARD SUMMARY
# =============================================================================

def build_dashboard_summary(df: pd.DataFrame) -> dict:
    """
    Genera toda la información necesaria para la página Inicio.

    Esta debe ser la única función utilizada por la interfaz.
    """

    return {

        # ==========================================================
        # CABECERA
        # ==========================================================

        "header": {

            "title": "Estado General",

            "subtitle": "Resumen automático del estado del equipo",

            "badge_text": str(df["date"].max().date())

        },

        # ==========================================================
        # TARJETAS SUPERIORES
        # ==========================================================

        "metrics": [

            get_team_availability(df),

            get_team_fatigue(df),

            get_team_risk(df),

            {

                "title": "Estado",

                "value": get_team_status(df)["label"],

                "description": get_team_status(df)["description"],

                "color": get_team_status(df)["color"]

            }

        ],

        # ==========================================================
        # ESTADO COLECTIVO
        # ==========================================================

        "team_state": get_team_status(df),

        # ==========================================================
        # JUGADORES PRIORITARIOS
        # ==========================================================

        "priority_players": get_priority_players(df),

        # ==========================================================
        # ALERTAS
        # ==========================================================

        "alerts": get_alerts(df),

        # ==========================================================
        # RECOMENDACIÓN
        # ==========================================================

        "recommendation": generate_recommendation(df),

        # ==========================================================
        # DECISIÓN
        # ==========================================================

        "decision": generate_daily_decision(df)

    }

# =============================================================================
# AVAILABILITY
# =============================================================================

def _get_availability(player: dict) -> str:

    score = player["overall_score"]
    risk = player["risk"]

    if score >= 85 and risk == "Bajo":
        return "Disponible"

    if score >= 70 and risk in ["Bajo", "Moderado"]:
        return "Control"

    if score >= 55:
        return "Adaptado"

    return "No disponible"


# =============================================================================
# ACTION
# =============================================================================

def _get_action(player: dict) -> str:

    score = player["overall_score"]
    risk = player["risk"]

    if score >= 85 and risk == "Bajo":
        return "Aumentar"

    if score >= 70 and risk in ["Bajo", "Moderado"]:
        return "Mantener"

    if risk == "Moderado":
        return "Control"

    if risk == "Alto":
        return "Reducir"

    return "Recuperación"


# =============================================================================
# SORT PLAYERS
# =============================================================================

def _sort_players(players: list) -> list:

    risk_order = {

        "Muy Alto": 4,
        "Alto": 3,
        "Moderado": 2,
        "Bajo": 1

    }

    return sorted(

        players,

        key=lambda x: (

            x["decision"]["priority"],
            risk_order.get(x["risk"], 0),
            -x["overall_score"]

        ),

        reverse=True

    )

# =============================================================================
# SQUAD SUMMARY
# =============================================================================

def squad_summary(df: pd.DataFrame) -> dict:
    """
    Resumen completo de la plantilla.

    Devuelve:
    - KPIs de plantilla
    - Tabla de jugadores
    """

    players = team_summary(df)

    squad = []

    for player in players:

        row = player.copy()

        row["availability"] = _get_availability(player)

        row["action"] = _get_action(player)

        squad.append(row)

    squad = _sort_players(squad)

    metrics = {

        "average_score": round(
            np.mean([p["overall_score"] for p in squad]), 1
        ),

        "available": sum(
            p["availability"] == "Disponible"
            for p in squad
        ),

        "monitoring": sum(
            p["availability"] == "Control"
            for p in squad
        ),

        "priority": sum(
            p["decision"]["priority"]
            for p in squad
        )

    }

    return {

        "metrics": metrics,

        "players": squad

    }

# =============================================================================
# SQUAD PAGE SUMMARY
# =============================================================================

def build_squad_summary(df: pd.DataFrame) -> dict:
    """
    Genera toda la información necesaria para la página Plantilla.
    """

    squad = squad_summary(df)

    return {

        # ==========================================================
        # CABECERA
        # ==========================================================

        "header": {

            "title": "Plantilla",

            "subtitle": "Estado actual de todos los jugadores",

            "badge_text": str(df["date"].max().date())

        },

        # ==========================================================
        # KPIs
        # ==========================================================

        "metrics": [

            {
                "title": "Estado medio",
                "value": squad["metrics"]["average_score"],
                "description": "Score medio de la plantilla.",
                "color": "#3B82F6"
            },

            {
                "title": "Disponibles",
                "value": squad["metrics"]["available"],
                "description": "Jugadores disponibles.",
                "color": "#22C55E"
            },

            {
                "title": "Control",
                "value": squad["metrics"]["monitoring"],
                "description": "Jugadores en seguimiento.",
                "color": "#FACC15"
            },

            {
                "title": "Prioritarios",
                "value": squad["metrics"]["priority"],
                "description": "Requieren atención.",
                "color": "#EF4444"
            }

        ],

        # ==========================================================
        # TABLA
        # ==========================================================

        "players": squad["players"]

    }

# =============================================================================
# TEAM SERIES
# =============================================================================

def team_series(
    df: pd.DataFrame,
    metric: str
) -> pd.DataFrame:
    """
    Serie temporal de la media del equipo.
    """

    return (

        df

        .groupby("date", as_index=False)[metric]

        .mean()

        .rename(columns={metric: "team"})

    )

# =============================================================================
# POSITION SERIES
# =============================================================================

def position_series(
    df: pd.DataFrame,
    position: str,
    metric: str
) -> pd.DataFrame:
    """
    Serie temporal de la media de la posición.
    """

    return (

        df[df["position"] == position]

        .groupby("date", as_index=False)[metric]

        .mean()

        .rename(columns={metric: "position"})

    )

# =============================================================================
# RISK SUMMARY
# =============================================================================

def build_risk_summary(df: pd.DataFrame) -> dict:
    """
    Construye toda la información de la página Riesgo.
    """

    players = []

    for player in sorted(df["player"].unique()):

        summary = player_summary(df, player)

        players.append(summary)

    players = sorted(

        players,

        key=lambda x: x["overall_score"]

    )

    return {

        "header": {

            "title": "Riesgo de Lesión",

            "subtitle": "Evaluación automática del estado de riesgo",

            "badge_text": str(df["date"].max().date())

        },

        "players": players

    }

# =============================================================================
# PLAYER RISK HISTORY
# =============================================================================

def build_player_risk_history(
    df: pd.DataFrame,
    player: str
) -> pd.DataFrame:
    """
    Calcula el riesgo global del jugador en cada sesión.

    Devuelve un DataFrame con:

    - date
    - overall_score
    - risk
    - risk_level
    """

    player_df = (

        df[df["player"] == player]

        .sort_values("date")

        .reset_index(drop=True)

    )

    rows = []

    for i in range(len(player_df)):

        partial = player_df.iloc[: i + 1]

        summary = player_summary(

            partial,

            player

        )

        if not summary:

            continue

        rows.append({

            "date": summary["date"],

            "overall_score": summary["overall_score"],

            "risk": summary["risk"],

            "risk_level": summary["risk_level"]

        })

    return pd.DataFrame(rows)

