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
    Aplica todos los filtros globales de la aplicación.
    Devuelve un nuevo DataFrame filtrado.
    """

    filtered = df.copy()

    # -------------------------
    # Jugador
    # -------------------------
    if player and player != "Todos":
        filtered = filtered[filtered["player"] == player]

    # -------------------------
    # Equipo
    # -------------------------
    if team and team != "Todos":
        filtered = filtered[filtered["team"] == team]

    # -------------------------
    # Posición
    # -------------------------
    if position and position != "Todos":
        filtered = filtered[filtered["position"] == position]

    # -------------------------
    # Sesión
    # -------------------------
    if session and session != "Todas":
        filtered = filtered[filtered["session"] == session]

    # -------------------------
    # Tipo de sesión
    # -------------------------
    if type_session and type_session != "Todos":
        filtered = filtered[
            filtered["type_session"] == type_session
        ]

    # -------------------------
    # Match Day
    # -------------------------
    if match_day and match_day != "Todos":
        filtered = filtered[
            filtered["match_day"] == match_day
        ]

    # -------------------------
    # Semana calendario
    # -------------------------
    if week_calendar and week_calendar != "Todas":
        filtered = filtered[
            filtered["week_calendar"] == week_calendar
        ]

    # -------------------------
    # Semana equipo
    # -------------------------
    if week_team and week_team != "Todas":
        filtered = filtered[
            filtered["week_team"] == week_team
        ]

    # -------------------------
    # Rango de fechas
    # -------------------------
    if date_range is not None:

        start_date, end_date = date_range

        filtered = filtered[
            (filtered["date"] >= pd.to_datetime(start_date))
            &
            (filtered["date"] <= pd.to_datetime(end_date))
        ]

    return filtered