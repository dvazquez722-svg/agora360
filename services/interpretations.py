"""
=========================================================

INTERPRETATIONS

Generación automática de interpretaciones
en lenguaje natural.

=========================================================
"""

import pandas as pd


# ==========================================================
# INTERPRETACIÓN DE UN JUGADOR
# ==========================================================

def interpret_player(row: pd.Series) -> str:
    """
    Genera una interpretación automática
    del estado del jugador.
    """

    if pd.isna(row["risk"]):

        return "No existen datos suficientes para realizar una valoración."

    text = (

        f"{row['player']} presenta un "

        f"riesgo {row['status'].lower()} "

        f"(score {row['risk']:.1f})."

    )

    if len(row["risk_reasons"]) > 0:

        text += " "

        text += "Factores principales: "

        text += "; ".join(row["risk_reasons"])

        text += "."

    if "recommendation" in row:

        text += " "

        text += row["recommendation"]

    return text


# ==========================================================
# INTERPRETACIÓN DE UNA MÉTRICA
# ==========================================================

def interpret_metric(
    metric: str,
    risk: float
) -> str:

    if pd.isna(risk):

        return f"{metric}: sin datos."

    if risk >= 80:

        return f"{metric}: riesgo muy alto."

    if risk >= 60:

        return f"{metric}: riesgo alto."

    if risk >= 40:

        return f"{metric}: riesgo moderado."

    if risk >= 20:

        return f"{metric}: vigilancia."

    return f"{metric}: situación normal."


# ==========================================================
# RESUMEN DE UN JUGADOR
# ==========================================================

def build_player_report(row: pd.Series) -> dict:

    return {

        "player": row["player"],

        "risk": row["risk"],

        "status": row["status"],

        "interpretation": interpret_player(row)

    }


# ==========================================================
# DATAFRAME DE INTERPRETACIONES
# ==========================================================

def build_interpretations(
    alerts_df: pd.DataFrame
) -> pd.DataFrame:

    reports = []

    for _, row in alerts_df.iterrows():

        reports.append(

            build_player_report(row)

        )

    return pd.DataFrame(reports)

# ==========================================================
# RESUMEN DEL EQUIPO
# ==========================================================

def interpret_team(
    interpretations_df: pd.DataFrame
) -> str:

    if interpretations_df.empty:

        return "No existen jugadores con alertas."

    total = len(interpretations_df)

    critical = (

        interpretations_df["risk"] >= 80

    ).sum()

    high = (

        (interpretations_df["risk"] >= 60)

        &

        (interpretations_df["risk"] < 80)

    ).sum()

    medium = (

        (interpretations_df["risk"] >= 40)

        &

        (interpretations_df["risk"] < 60)

    ).sum()

    return (

        f"Se han detectado {total} jugadores con alertas. "

        f"{critical} presentan riesgo muy alto, "

        f"{high} riesgo alto y "

        f"{medium} riesgo moderado."

    )


# ==========================================================
# RESUMEN EJECUTIVO
# ==========================================================

def executive_summary(
    interpretations_df: pd.DataFrame
) -> str:

    if interpretations_df.empty:

        return "No existen incidencias relevantes."

    players = ", ".join(

        interpretations_df["player"]

    )

    summary = interpret_team(

        interpretations_df

    )

    summary += " "

    summary += (

        "Jugadores prioritarios: "

        f"{players}."

    )

    return summary

def interpret_player(row: pd.Series) -> str:
    """
    Genera una interpretación automática
    del estado del jugador.
    """

    risk = row["risk"]

    if pd.isna(risk):

        return "No existen datos suficientes para realizar una valoración."

    text = (

        f"{row['player']} presenta un "

        f"riesgo {row['status'].lower()} "

        f"(score {risk:.1f})."

    )

    if "reasons" in row and len(row["reasons"]) > 0:

        text += " "

        text += "Factores principales: "

        text += "; ".join(row["reasons"])

        text += "."

    if "recommendation" in row:

        text += " "

        text += row["recommendation"]

    return text

# ==========================================================
#
# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_interpretations(
    interpretations_df: pd.DataFrame
) -> pd.DataFrame:

    if interpretations_df.empty:

        return interpretations_df

    required = [

        "player",

        "risk",

        "status",

        "interpretation"

    ]

    missing = [

        col

        for col in required

        if col not in interpretations_df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas: {missing}"

        )

    if interpretations_df["player"].duplicated().any():

        raise ValueError(

            "Hay jugadores duplicados."

        )

    return interpretations_df