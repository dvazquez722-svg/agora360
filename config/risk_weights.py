"""
=========================================================

RISK WEIGHTS

Motor de interpretación del riesgo.

Convierte las métricas de workload en:

• Riesgo por métrica
• Riesgo global
• Estado del jugador

=========================================================
"""

import numpy as np
import pandas as pd

from config.thresholds import *

# ==========================================================
# PESOS DEL MODELO
# ==========================================================

RISK_WEIGHTS = {

    "acwr": 0.30,

    "weekly_change": 0.20,

    "percentile": 0.15,

    "monotony": 0.15,

    "strain": 0.10,

    "trend": 0.10

}

# ==========================================================
# NOMBRES DE LAS MÉTRICAS
# ==========================================================

METRIC_NAMES = {

    "player_load": "Player Load",

    "distance_m": "Distancia",

    "abs_hsr_m": "HSR",

    "high_speed_distance": "Distancia alta velocidad",

    "accelerations": "Aceleraciones",

    "decelerations": "Deceleraciones",

    "sprints_abs_count": "Sprints",

    "mechanical_actions": "Acciones mecánicas",

    "hmld_m": "HMLD"

}

# ==========================================================
# ACWR
# ==========================================================

def interpret_acwr(value: float) -> float:
    """
    Devuelve un score de riesgo (0-100)
    para el ACWR.
    """

    if pd.isna(value):

        return 0

    if value < 0.80:

        return 40

    if value <= 1.30:

        return 0

    if value <= 1.50:

        return 60

    return 100

# ==========================================================
# CAMBIO SEMANAL
# ==========================================================

def interpret_weekly_change(value: float) -> float:
    """
    Riesgo asociado al cambio semanal.
    """

    if pd.isna(value):

        return 0

    change = abs(value)

    if change < 10:

        return 0

    if change < 20:

        return 30

    if change < 30:

        return 60

    return 100

# ==========================================================
# PERCENTIL
# ==========================================================

def interpret_percentile(value: float) -> float:
    """
    Riesgo asociado al percentil histórico.
    """

    if pd.isna(value):

        return 0

    if value < 75:

        return 0

    if value < 90:

        return 40

    if value < 95:

        return 70

    return 100

# ==========================================================
# MONOTONY
# ==========================================================

def interpret_monotony(value: float) -> float:
    """
    Riesgo asociado a la monotonía.
    """

    if pd.isna(value):

        return 0

    if value < 1.0:

        return 0

    if value < 1.5:

        return 25

    if value < 2.0:

        return 60

    return 100

# ==========================================================
# STRAIN
# ==========================================================

def interpret_strain(value: float) -> float:
    """
    Riesgo asociado al Training Strain.

    Los umbrales son provisionales.
    """

    if pd.isna(value):

        return 0

    if value < 2000:

        return 0

    if value < 4000:

        return 40

    if value < 6000:

        return 70

    return 100

# ==========================================================
# TENDENCIA
# ==========================================================

def interpret_trend(value: str) -> float:
    """
    Riesgo asociado a la tendencia.
    """

    if pd.isna(value):

        return 0

    scores = {

        "Sin datos": 0,

        "Descendente": 0,

        "Estable": 0,

        "Ascendente": 40,

        "Muy ascendente": 100

    }

    return scores.get(value, 0)

# ==========================================================
# RIESGO DE UNA MÉTRICA
# ==========================================================

def calculate_metric_risk(
    acwr: float,
    weekly_change: float,
    percentile: float,
    monotony: float,
    strain: float,
    trend: str
) -> float:
    """
    Calcula un score de riesgo (0-100)
    para una métrica concreta.
    """

    score = (

        interpret_acwr(acwr)
        * RISK_WEIGHTS["acwr"]

        +

        interpret_weekly_change(weekly_change)
        * RISK_WEIGHTS["weekly_change"]

        +

        interpret_percentile(percentile)
        * RISK_WEIGHTS["percentile"]

        +

        interpret_monotony(monotony)
        * RISK_WEIGHTS["monotony"]

        +

        interpret_strain(strain)
        * RISK_WEIGHTS["strain"]

        +

        interpret_trend(trend)
        * RISK_WEIGHTS["trend"]

    )

    return round(score, 1)

# ==========================================================
# ESTADO DE RIESGO
# ==========================================================

def classify_risk(score: float) -> tuple[str, str]:
    """
    Clasifica un score de riesgo.
    """

    if pd.isna(score):

        return "Sin datos", "⚪"

    if score < 20:

        return "Normal", "🟢"

    if score < 40:

        return "Bajo", "🟡"

    if score < 60:

        return "Moderado", "🟠"

    if score < 80:

        return "Alto", "🔴"

    return "Muy alto", "🚨"

# ==========================================================
# DATAFRAME DE RIESGO
# ==========================================================

def build_risk_dataframe(workload_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el riesgo de todas las métricas
    para todos los jugadores.
    """

    df = workload_df.copy()

    metrics = [

        "player_load",

        "distance_m",

        "abs_hsr_m",

        "high_speed_distance",

        "accelerations",

        "decelerations",

        "sprints_abs_count",

        "mechanical_actions",

        "hmld_m"

    ]

    global_scores = []

    for metric in metrics:

        acwr = f"{metric}_acwr"

        weekly = f"{metric}_weekly_change"

        percentile = f"{metric}_percentile"

        monotony = f"{metric}_monotony"

        strain = f"{metric}_strain"

        trend = f"{metric}_trend"

        risk_column = f"{metric}_risk"

        if acwr not in df.columns:

            continue

        df[risk_column] = df.apply(

            lambda row: calculate_metric_risk(

                row.get(acwr, np.nan),

                row.get(weekly, np.nan),

                row.get(percentile, np.nan),

                row.get(monotony, np.nan),

                row.get(strain, np.nan),

                row.get(trend, "Sin datos")

            ),

            axis=1

        )

        global_scores.append(risk_column)

    if len(global_scores) > 0:

        df["global_risk"] = (

            df[global_scores]

            .mean(axis=1)

            .round(1)

        )

    else:

        df["global_risk"] = np.nan

    # ======================================================
    # Estado global
    # ======================================================

    status = df["global_risk"].apply(calculate_player_status)

    df["status"] = status.apply(lambda x: x[0])

    df["status_icon"] = status.apply(lambda x: x[1])

    # ======================================================
    # Razones del riesgo
    # ======================================================

    df["risk_reasons"] = df.apply(

    calculate_risk_reasons,

    axis=1

)
    
    df = validate_risk_dataframe(df)

    return df

# ==========================================================
# ESTADO GLOBAL DEL JUGADOR
# ==========================================================

def calculate_player_status(global_risk: float) -> tuple[str, str]:
    """
    Devuelve el estado global del jugador
    según su riesgo.
    """

    if pd.isna(global_risk):

        return "Sin datos", "⚪"

    if global_risk < 20:

        return "Normal", "🟢"

    if global_risk < 40:

        return "Vigilancia", "🟡"

    if global_risk < 60:

        return "Precaución", "🟠"

    if global_risk < 80:

        return "Riesgo", "🔴"

    return "Riesgo muy alto", "🚨"

# ==========================================================
# RAZONES DEL RIESGO
# ==========================================================

def calculate_risk_reasons(row: pd.Series) -> list:
    """
    Devuelve una lista con los principales
    factores que generan riesgo.
    """

    reasons = []

    metrics = [

        "player_load",

        "distance_m",

        "abs_hsr_m",

        "high_speed_distance",

        "accelerations",

        "decelerations",

        "sprints_abs_count",

        "mechanical_actions",

        "hmld_m"

    ]

    for metric in metrics:

        # ------------------------
        # ACWR
        # ------------------------

        acwr = row.get(f"{metric}_acwr", np.nan)

        if pd.notna(acwr) and acwr > 1.30:

            reasons.append(
                f"{METRIC_NAMES[metric]}: ACWR elevado ({acwr:.2f})"
            )

        # ------------------------
        # Cambio semanal
        # ------------------------

        weekly = row.get(

            f"{metric}_weekly_change",

            np.nan

        )

        if pd.notna(weekly) and abs(weekly) >= 20:

            reasons.append(
                f"{METRIC_NAMES[metric]}: cambio semanal {weekly:.1f}%"
            )

        # ------------------------
        # Percentil
        # ------------------------

        percentile = row.get(

            f"{metric}_percentile",

            np.nan

        )

        if pd.notna(percentile) and percentile >= 90:

            reasons.append(
                f"{METRIC_NAMES[metric]}: percentil {percentile:.0f}"
            )

        # ------------------------
        # Monotonía
        # ------------------------

        monotony = row.get(

            f"{metric}_monotony",

            np.nan

        )

        if pd.notna(monotony) and monotony >= 2:

            reasons.append(
                f"{METRIC_NAMES[metric]}: monotonía elevada"
            )

    return reasons

# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_risk_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprueba que el DataFrame de riesgo
    contiene las columnas necesarias.
    """

    required = [

        "player",

        "global_risk",

        "status",

        "status_icon",

        "risk_reasons"

    ]

    missing = [

        col

        for col in required

        if col not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas obligatorias: {missing}"

        )

    duplicated = df["player"].duplicated().sum()

    if duplicated > 0:

        raise ValueError(

            "Existen jugadores duplicados."

        )

    return df