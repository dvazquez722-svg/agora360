"""
Riesgo de Lesión
----------------

Evaluación automática del riesgo de lesión.
"""

import streamlit as st

from src.styles import apply_styles
from src.data_loader import load_clean_data

from src.analytics import (
    build_risk_summary,
    build_player_risk_history
)

from src.auth import check_authentication

check_authentication()

from src.components import (

    page_header,

    risk_kpis,

    risk_gauge,

    risk_scatter,

    risk_factor_bars,

    coach_decision_card

)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(

    page_title="Riesgo de Lesión",

    page_icon="🚨",

    layout="wide"

)

apply_styles()

# =============================================================================
# DATOS
# =============================================================================

df = load_clean_data()

summary = build_risk_summary(df)

# =============================================================================
# CABECERA
# =============================================================================

page_header(

    title=summary["header"]["title"],

    subtitle=summary["header"]["subtitle"],

    badge_text=summary["header"]["badge_text"]

)

# =============================================================================
# KPIs
# =============================================================================

risk_kpis(summary)

# =============================================================================
# SELECCIÓN DEL JUGADOR
# =============================================================================

players = summary["players"]

selected_player = st.selectbox(

    "Selecciona un jugador",

    [p["player"] for p in players]

)

player = next(

    p for p in players

    if p["player"] == selected_player

)

# =============================================================================
# RESUMEN SUPERIOR
# =============================================================================

left, right = st.columns([1.15, 0.85])

with left:

    risk_gauge(player)

with right:

    coach_decision_card(player)

st.divider()

# =============================================================================
# MAPA DE DECISIÓN
# =============================================================================

risk_scatter(

    summary,

    selected_player

)

st.divider()

# =============================================================================
# FACTORES DE RIESGO
# =============================================================================

risk_factor_bars(player)