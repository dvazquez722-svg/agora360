"""
5_Comparativas.py

Página de Análisis Comparativo.
"""

import streamlit as st

from src.styles import apply_styles
from src.data_loader import load_clean_data

from src.auth import check_authentication

check_authentication()

from src.analytics_compare import (
    get_available_filters,
    build_comparison
)

from src.components_compare import (
    comparison_selector,
    comparison_filters,
    render_comparison
)

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(

    page_title="Análisis Comparativo",

    page_icon="📊",

    layout="wide"

)

apply_styles()

# =============================================================================
# DATOS
# =============================================================================

df = load_clean_data()

filters = get_available_filters(df)

# =============================================================================
# TÍTULO
# =============================================================================

st.title("Análisis Comparativo")

st.caption(
    "Explora y compara el rendimiento entre jugadores, posiciones y periodos."
)

st.divider()

# =============================================================================
# TIPO DE ANÁLISIS
# =============================================================================

analysis_type = comparison_selector()

st.divider()

# =============================================================================
# FILTROS
# =============================================================================

selected = comparison_filters(

    filters,

    analysis_type

)

# =============================================================================
# COMPARACIÓN
# =============================================================================

comparison = build_comparison(

    df=df,

    analysis_type=analysis_type,

    reference=selected["reference"],

    comparison=selected["comparison"],

    metrics=selected["metrics"],

    start_date=selected["start_date"],

    end_date=selected["end_date"],

    week=selected["week"],

    microcycle=selected["microcycle"],

    session=selected["session"],

    position_filter=selected.get(

        "position_filter",

        None

    )

)

# =============================================================================
# RESULTADOS
# =============================================================================

st.divider()

render_comparison(

    comparison

)