"""
Perfil del Jugador
------------------

Análisis individual del estado actual del jugador.
"""

import streamlit as st

from src.styles import apply_styles
from src.data_loader import load_clean_data

from src.analytics import (
    player_summary
)

from src.auth import check_authentication

check_authentication()

from src.components import (
    page_header,
    player_header,
    player_report_card,
    player_kpis)
# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(

    page_title="Perfil del Jugador",
    page_icon="👤",
    layout="wide"
)

apply_styles()

# =============================================================================
# DATOS
# =============================================================================

df = load_clean_data()

players = sorted(df["player"].unique())


# =============================================================================
# SELECCIÓN DEL JUGADOR
# =============================================================================

default_player = st.session_state.get(
    "selected_player",
    players[0]
)

player_name = st.selectbox(
    "Jugador",
    players,
    index=players.index(default_player)
    if default_player in players
    else 0
)

summary = player_summary(
    df,
    player_name
)

# =============================================================================
# CABECERA
# =============================================================================

page_header(
    title="Perfil del Jugador",
    subtitle="Análisis individual del estado actual",
    badge_text="Análisis"
)

# =============================================================================
# RESUMEN DEL JUGADOR
# =============================================================================

player_header(summary)

st.write("")

player_report_card(
    summary["report"],
    summary
)

st.write("")

player_kpis(summary)

st.divider()