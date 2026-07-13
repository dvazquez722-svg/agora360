"""
1_Inicio.py
============
Página principal de Performance Monitor.

Objetivo:
Responder a la pregunta:

¿Cómo está el equipo hoy?

La página no contiene lógica deportiva.
Toda la información procede de analytics.py.
"""

import streamlit as st

from src.auth import check_authentication

check_authentication()

from src.components import priority_players_table

from src.styles import apply_styles

from src.data_loader import load_data

from src.analytics import build_dashboard_summary

from src.components import (

    page_container,

    page_header,

    metric_row,

    two_columns,

    team_state_card,

    priority_players_table,

    alerts_panel,

    recommendation_panel,

    decision_panel,

    footer

)


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(

    page_title="Inicio",

    page_icon="⚽",

    layout="wide"

)


apply_styles()

page_container()


# =============================================================================
# CARGA DE DATOS
# =============================================================================

data = load_data()

df = data["clean"]

# =============================================================================
# ANÁLISIS
# =============================================================================

summary = build_dashboard_summary(df)


# =============================================================================
# CABECERA
# =============================================================================

page_header(

    title=summary["header"]["title"],

    subtitle=summary["header"]["subtitle"],

    badge_text=summary["header"]["badge_text"]

)


# =============================================================================
# TARJETAS PRINCIPALES
# =============================================================================

metric_row(

    summary["metrics"]

)

# =============================================================================
# ESTADO COLECTIVO + JUGADORES PRIORITARIOS
# =============================================================================

left, right = st.columns(2)

with left:

    team_state_card(
        summary["team_state"]
    )

with right:

    priority_players_table(
    summary["priority_players"]
)


# =============================================================================
# RECOMENDACIÓN + DECISIÓN
# =============================================================================

left, right = st.columns(2)

with left:

    recommendation_panel(
        summary["recommendation"]
    )

with right:

    decision_panel(
        summary["decision"]
    )


# =============================================================================
# ALERTAS
# =============================================================================

alerts_panel(
    summary["alerts"]
)


# =============================================================================
# FOOTER
# =============================================================================

footer()