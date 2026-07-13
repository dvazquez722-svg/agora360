"""
=========================================================

DASHBOARD

Orquesta toda la información necesaria
para las páginas de la aplicación.

=========================================================
"""

import pandas as pd

from services.metrics import get_team_kpis

from services.workload import build_workload_dataframe

from config.risk_weights import build_risk_dataframe

from services.alerts import build_alerts

from services.priorities import get_priority_players

from services.recommendations import generate_recommendation

from services.interpretations import (

    build_interpretations,

    executive_summary,

    interpret_team

)

# ==========================================================
# DASHBOARD
# ==========================================================

def build_dashboard(
    df: pd.DataFrame
) -> dict:

    """
    Construye toda la información que utilizará
    cualquier página del dashboard.
    """

    # ======================================================
    # KPIs
    # ======================================================

    kpis = get_team_kpis(df)

    # ======================================================
    # WORKLOAD
    # ======================================================

    workload = build_workload_dataframe(df)

    # ======================================================
    # RIESGO
    # ======================================================

    risk = build_risk_dataframe(workload)

    print("\nCOLUMNAS DEL DATAFRAME RISK")
    print(risk.columns.tolist())

    # ======================================================
    # ALERTAS
    # ======================================================

    alerts = build_alerts(risk)

    # ======================================================
    # INTERPRETACIONES
    # ======================================================

    interpretations = build_interpretations(alerts)

    # ======================================================
    # ESTADO DEL EQUIPO
    # ======================================================

    team_status = interpret_team(

        interpretations

    )

    # ======================================================
    # RESUMEN EJECUTIVO
    # ======================================================

    summary = executive_summary(

        interpretations

    )

    # ======================================================
    # JUGADORES PRIORITARIOS
    # ======================================================

    priority_players = get_priority_players(risk)

    # ======================================================
    # RECOMENDACIÓN
    # ======================================================

    recommendation = generate_recommendation(df)

    # ======================================================
    # RESULTADO
    # ======================================================

    dashboard = {

        "kpis": kpis,

        "workload": workload,

        "risk": risk,

        "alerts": alerts,

        "interpretations": interpretations,

        "team_status": team_status,

        "executive_summary": summary,

        "priority_players": priority_players,

        "recommendation": recommendation

    }

    return dashboard