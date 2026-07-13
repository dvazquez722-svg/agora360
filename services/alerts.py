"""
=========================================================

ALERTS

Generador de alertas de rendimiento.

Convierte el DataFrame de riesgo en
alertas ordenadas por prioridad.

=========================================================
"""

import pandas as pd

# ==========================================================
# NIVELES DE ALERTA
# ==========================================================

ALERT_LEVELS = {

    "critical": 80,

    "high": 60,

    "medium": 40,

    "low": 20

}

# ==========================================================
# ALERTA DE UN JUGADOR
# ==========================================================

def build_player_alert(row: pd.Series) -> dict:
    """
    Genera una alerta para un jugador.
    """

    risk = row["global_risk"]

    if pd.isna(risk):

        return None

    if risk >= ALERT_LEVELS["critical"]:

        level = "Crítica"

        icon = "🚨"

    elif risk >= ALERT_LEVELS["high"]:

        level = "Alta"

        icon = "🔴"

    elif risk >= ALERT_LEVELS["medium"]:

        level = "Media"

        icon = "🟠"

    elif risk >= ALERT_LEVELS["low"]:

        level = "Baja"

        icon = "🟡"

    else:

        return None

    return {

        "player": row["player"],

        "level": level,

        "icon": icon,

        "risk": risk,

        "status": row["status"],

        "reasons": row["risk_reasons"]

    }

# ==========================================================
# RECOMENDACIÓN
# ==========================================================

def generate_recommendation(row: pd.Series) -> str:
    """
    Genera una recomendación automática
    según el riesgo del jugador.
    """

    risk = row["risk"]

    if pd.isna(risk):

        return "Sin datos suficientes."

    if risk >= 80:

        return (
            "Reducir significativamente la carga y "
            "realizar una valoración individual."
        )

    if risk >= 60:

        return (
            "Reducir la carga de entrenamiento y "
            "monitorizar la evolución."
        )

    if risk >= 40:

        return (
            "Mantener seguimiento diario y "
            "evitar incrementos bruscos."
        )

    if risk >= 20:

        return (
            "Continuar con la planificación "
            "prestando atención a la evolución."
        )

    return "Mantener la planificación prevista."

# ==========================================================
# GENERAR ALERTAS
# ==========================================================

def build_alerts(risk_df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera todas las alertas del equipo
    ordenadas por nivel de riesgo.
    """

    alerts = []

    for _, row in risk_df.iterrows():

        alert = build_player_alert(row)

        if alert is not None:

            alerts.append(alert)

    if len(alerts) == 0:

        return pd.DataFrame()

    alerts = pd.DataFrame(alerts)

    alerts["recommendation"] = alerts.apply(

        generate_recommendation,

        axis=1

)
    alerts["n_reasons"] = alerts["reasons"].apply(len)
    
    alerts = (

        alerts

        .sort_values(

            by=["risk",
            "n_reasons"],

            ascending=[False,
                       False]

        )

        .reset_index(drop=True)

    )

    alerts["summary"] = alerts["reasons"].apply(

    lambda x: " · ".join(x)

    if len(x) > 0

    else "Sin incidencias"

)
    alerts = validate_alerts(alerts)

    return alerts


#PLAYER ALERT#


def get_player_alert(

    alerts_df: pd.DataFrame,

    player: str

):

    row = alerts_df[

        alerts_df["player"] == player

    ]

    if row.empty:

        return None

    return row.iloc[0]


# ==========================================================
# FILTRAR ALERTAS
# ==========================================================

def filter_alerts(
    alerts_df: pd.DataFrame,
    level: str = None
) -> pd.DataFrame:
    """
    Filtra las alertas por nivel.
    """

    if alerts_df.empty:

        return alerts_df

    if level is None:

        return alerts_df

    return (

        alerts_df[
            alerts_df["level"] == level
        ]

        .reset_index(drop=True)

    )

# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_alerts(alerts_df: pd.DataFrame) -> pd.DataFrame:

    if alerts_df.empty:

        return alerts_df

    required = [

        "player",

        "risk",

        "level",

        "recommendation"

    ]

    missing = [

        col

        for col in required

        if col not in alerts_df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas: {missing}"

        )

    return alerts_df