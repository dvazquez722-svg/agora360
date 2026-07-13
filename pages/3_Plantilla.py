"""
Plantilla
---------

Estado actual de todos los jugadores del equipo.
"""

import streamlit as st



from src.styles import apply_styles
from src.data_loader import load_clean_data
from src.analytics import build_squad_summary

from src.auth import check_authentication

check_authentication()

from src.components import (
    page_header,
    metric_card,
    squad_table
)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(
    page_title="Plantilla",
    page_icon="👥",
    layout="wide"
)

apply_styles()

# =============================================================================
# DATOS
# =============================================================================

df = load_clean_data()

summary = build_squad_summary(df)


# =============================================================================
# CABECERA
# =============================================================================

page_header(**summary["header"])

# =============================================================================
# KPIs
# =============================================================================

cols = st.columns(4)

for col, metric in zip(cols, summary["metrics"]):

    with col:

        metric_card(
            title=metric["title"],
            value=str(metric["value"]),
            description=metric["description"],
            color=metric["color"]
        )

st.divider()

# =============================================================================
# PLANTILLA
# =============================================================================

squad_table(summary["players"])