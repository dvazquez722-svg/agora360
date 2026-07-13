"""
=========================================================

RECOMMENDATIONS

Generador de recomendaciones automáticas.

=========================================================
"""

import pandas as pd


# ==========================================================
# RECOMENDACIÓN
# ==========================================================

def generate_recommendation(
    df: pd.DataFrame
) -> dict:
    """
    Genera la recomendación principal del día
    a partir de los indicadores del equipo.
    """

    if df.empty:

        return {

            "nivel": "info",

            "titulo": "Sin datos",

            "mensaje": "No existen datos suficientes."

        }

    # ======================================================
    # Variables
    # ======================================================

    wellness = df["wellness_fatigue"].mean()

    rpe = df["rpe_general"].mean()

    player_load = df["player_load"].mean()

    hsr = df["abs_hsr_m"].mean()

    # ======================================================
    # Estado crítico
    # ======================================================

    if (

        pd.notna(wellness)

        and wellness <= 2

    ):

        return {

            "nivel": "error",

            "titulo": "Reducir la carga",

            "mensaje": (

                "El equipo presenta un nivel de fatiga elevado. "

                "Se recomienda disminuir la carga externa y "

                "priorizar estrategias de recuperación."

            )

        }

    # ======================================================
    # RPE elevado
    # ======================================================

    if (

        pd.notna(rpe)

        and rpe >= 8

    ):

        return {

            "nivel": "warning",

            "titulo": "Controlar la intensidad",

            "mensaje": (

                "La carga interna percibida es elevada. "

                "Conviene reducir la intensidad de la "

                "próxima sesión."

            )

        }

    # ======================================================
    # Exposición alta
    # ======================================================

    if (

        pd.notna(hsr)

        and hsr > df["abs_hsr_m"].quantile(0.75)

    ):

        return {

            "nivel": "warning",

            "titulo": "Controlar la exposición",

            "mensaje": (

                "La exposición a alta velocidad se encuentra "

                "por encima de lo habitual. Se recomienda "

                "monitorizar el volumen de HSR."

            )

        }

    # ======================================================
    # Carga elevada
    # ======================================================

    if (

        pd.notna(player_load)

        and player_load > df["player_load"].quantile(0.75)

    ):

        return {

            "nivel": "warning",

            "titulo": "Vigilar la carga",

            "mensaje": (

                "El Player Load del equipo es elevado. "

                "Se aconseja revisar la planificación "

                "de la siguiente sesión."

            )

        }

    # ======================================================
    # Estado normal
    # ======================================================

    return {

        "nivel": "success",

        "titulo": "Mantener planificación",

        "mensaje": (

            "Los indicadores del equipo se encuentran "

            "dentro de los rangos esperados."

        )

    }