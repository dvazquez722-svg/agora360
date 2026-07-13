import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    player=None,
    team=None,
    position=None,
    session=None,
    type_session=None,
    match_day=None,
    week_calendar=None,
    week_team=None,
    date_range=None,
):
    """
    Aplica todos los filtros seleccionados al DataFrame.
    """

    filtered = df.copy()

    # ==========================
    # Jugador
    # ==========================
    if player and player != "Todos":
        filtered = filtered[filtered["player"] == player]

    # ==========================
    # Equipo
    # ==========================
    if team and team != "Todos":
        filtered = filtered[filtered["team"] == team]

    # ==========================
    # Posición
    # ==========================
    if position and position != "Todos":
        filtered = filtered[filtered["position"] == position]

    # ==========================
    # Sesión
    # ==========================
    if session and session != "Todas":
        filtered = filtered[filtered["session"] == session]

    # ==========================
    # Tipo de sesión
    # ==========================
    if type_session and type_session != "Todos":
        filtered = filtered[filtered["type_session"] == type_session]

    # ==========================
    # Match Day
    # ==========================
    if match_day and match_day != "Todos":
        filtered = filtered[filtered["match_day"] == match_day]

    # ==========================
    # Semana calendario
    # ==========================
    if week_calendar and week_calendar != "Todas":
        filtered = filtered[filtered["week_calendar"] == week_calendar]

    # ==========================
    # Semana equipo
    # ==========================
    if week_team and week_team != "Todas":
        filtered = filtered[filtered["week_team"] == week_team]

    # ==========================
    # Rango de fechas
    # ==========================
    if date_range is not None and len(date_range) == 2:

        start_date, end_date = date_range

        filtered = filtered[
            (filtered["date"] >= pd.to_datetime(start_date))
            & (filtered["date"] <= pd.to_datetime(end_date))
        ]

    return filtered


# ============================================================
# Funciones auxiliares para los filtros
# ============================================================

def get_players(df):
    return sorted(df["player"].dropna().unique().tolist())


def get_teams(df):
    return sorted(df["team"].dropna().unique().tolist())


def get_positions(df):
    return sorted(df["position"].dropna().unique().tolist())


def get_sessions(df):
    return sorted(df["session"].dropna().unique().tolist())


def get_type_sessions(df):
    return sorted(df["type_session"].dropna().unique().tolist())


def get_match_days(df):
    return sorted(df["match_day"].dropna().unique().tolist())


def get_week_calendar(df):
    return sorted(df["week_calendar"].dropna().unique().tolist())


def get_week_team(df):
    return sorted(df["week_team"].dropna().unique().tolist())