import streamlit as st
from textwrap import dedent
from services.loader import load_data
from components.filters import (
    apply_filters,
    get_players,
    get_positions,
    get_sessions,
    get_type_sessions,
    get_match_days,
)


def render_sidebar():
    """
    Renderiza la barra lateral global de la aplicación.

    Devuelve un diccionario con:
        - DataFrame filtrado
        - Valores de todos los filtros
    """

    # ======================================
    # Cargar datos
    # ======================================

    df = load_data()

    # ======================================
    # SIDEBAR
    # ======================================

    st.sidebar.title("⚙️ Filtros")

    # -------------------------
    # Jugador
    # -------------------------

    player = st.sidebar.selectbox(
        "Jugador",
        ["Todos"] + get_players(df)
    )

    # -------------------------
    # Posición
    # -------------------------

    position = st.sidebar.selectbox(
        "Posición",
        ["Todos"] + get_positions(df)
    )

    # -------------------------
    # Tipo de sesión
    # -------------------------

    type_session = st.sidebar.selectbox(
        "Tipo de sesión",
        ["Todos"] + get_type_sessions(df)
    )

    # -------------------------
    # Sesión
    # -------------------------

    session = st.sidebar.selectbox(
        "Sesión",
        ["Todas"] + get_sessions(df)
    )

    # -------------------------
    # Match Day
    # -------------------------

    match_day = st.sidebar.selectbox(
        "Match Day",
        ["Todos"] + get_match_days(df)
    )

    # -------------------------
    # Fechas
    # -------------------------

    date_range = st.sidebar.date_input(
        "Rango de fechas",
        (
            df["date"].min(),
            df["date"].max()
        )
    )

    # ======================================
    # Aplicar filtros
    # ======================================

    df_filtered = apply_filters(
        df,
        player=player,
        position=position,
        session=session,
        type_session=type_session,
        match_day=match_day,
        date_range=date_range
    )

    # ======================================
    # Devolver contexto
    # ======================================

    return {
        "df": df_filtered,
        "player": player,
        "position": position,
        "session": session,
        "type_session": type_session,
        "match_day": match_day,
        "date_range": date_range,
    }