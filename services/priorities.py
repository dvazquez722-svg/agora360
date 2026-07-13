"""
=========================================================

PRIORITIES

Genera el listado de jugadores prioritarios
para el cuerpo técnico.

=========================================================
"""

import pandas as pd


# ==========================================================
# PRIORIDAD
# ==========================================================

def calculate_priority(row: pd.Series):

    """
    Calcula la prioridad del jugador
    en función del riesgo.
    """

    risk = row["global_risk"]

    if pd.isna(risk):

        return (

            "Sin datos",

            "⚪"

        )

    if risk >= 80:

        return (

            "Muy alta",

            "🚨"

        )

    if risk >= 60:

        return (

            "Alta",

            "🔴"

        )

    if risk >= 40:

        return (

            "Media",

            "🟠"

        )

    if risk >= 20:

        return (

            "Baja",

            "🟡"

        )

    return (

        "Normal",

        "🟢"

    )


# ==========================================================
# MOTIVO
# ==========================================================

def build_reason(row: pd.Series) -> str:

    """
    Resume el motivo principal
    del riesgo.
    """

    reasons = row.get("reasons", [])

    if isinstance(reasons, list):

        if len(reasons):

            return reasons[0]

    return "Sin incidencias"


# ==========================================================
# ACCIÓN
# ==========================================================

def build_action(row: pd.Series) -> str:

    """
    Acción propuesta.
    """

    recommendation = row.get(

        "recommendation",

        None

    )

    if recommendation:

        return recommendation

    risk = row["global_risk"]

    if risk >= 80:

        return "Reducir carga"

    if risk >= 60:

        return "Control diario"

    if risk >= 40:

        return "Seguimiento"

    return "Planificación normal"


# ==========================================================
# JUGADORES PRIORITARIOS
# ==========================================================

def get_priority_players(

    risk_df: pd.DataFrame,

    top: int = 8

) -> pd.DataFrame:

    """
    Devuelve los jugadores que
    requieren mayor atención.
    """

    if risk_df.empty:

        return pd.DataFrame()

    priority = risk_df.copy()

    priority[

        [

            "priority",

            "icon"

        ]

    ] = priority.apply(

        lambda row: pd.Series(

            calculate_priority(row)

        ),

        axis=1

    )

    priority["reason"] = priority.apply(

        build_reason,

        axis=1

    )

    priority["n_reasons"] = priority["risk_reasons"].apply(

    lambda x: len(x)

    if isinstance(x, list)

    else 0

)

    priority = (

        priority

        .sort_values(

            "global_risk",

            ascending=False

        )

        .head(top)

        [

            [

                "icon",

                "player",

                "priority",

                "global_risk",

                "reason",

                "action"

            ]

        ]

        .reset_index(

            drop=True

        )

    )

    priority = priority.rename(

    columns={

        "global_risk": "risk",

        "risk_reasons": "reasons",

        "status_icon": "icon"

    }

)

    return priority