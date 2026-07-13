"""
=========================================================

METRICS

Funciones para calcular KPIs y métricas
utilizadas por el dashboard.

=========================================================
"""

import numpy as np
import pandas as pd


# ==========================================================
# MÉTRICAS PRINCIPALES
# ==========================================================

MAIN_METRICS = [

    "player_load",

    "distance_m",

    "abs_hsr_m",

    "high_speed_distance",

    "accelerations",

    "decelerations",

    "sprints_abs_count",

    "mechanical_actions",

    "hmld_m"

]


# ==========================================================
# KPIs DEL EQUIPO
# ==========================================================

def get_team_kpis(df: pd.DataFrame) -> dict:

    if df.empty:

        return {}

    return {

        "players": df["player"].nunique(),

        "sessions": df["date"].nunique(),

        "avg_player_load": round(df["player_load"].mean(), 1),

        "avg_distance": round(df["distance_m"].mean(), 1),

        "avg_hsr": round(df["abs_hsr_m"].mean(), 1),

        "avg_sprints": round(df["sprints_abs_count"].mean(), 1),

        "avg_accelerations": round(df["accelerations"].mean(), 1),

        "avg_decelerations": round(df["decelerations"].mean(), 1),

        "avg_energy": round(df["energy_expenditure"].mean(), 1)

    }


# ==========================================================
# KPIs DE UN JUGADOR
# ==========================================================

def get_player_kpis(

    df: pd.DataFrame,

    player: str

) -> dict:

    player_df = df[

        df["player"] == player

    ]

    if player_df.empty:

        return {}

    return {

        "sessions": len(player_df),

        "minutes": round(player_df["minutes"].sum(), 1),

        "player_load": round(player_df["player_load"].mean(), 1),

        "distance": round(player_df["distance_m"].mean(), 1),

        "hsr": round(player_df["abs_hsr_m"].mean(), 1),

        "sprints": round(player_df["sprints_abs_count"].mean(), 1),

        "accelerations": round(player_df["accelerations"].mean(), 1),

        "decelerations": round(player_df["decelerations"].mean(), 1),

        "energy": round(player_df["energy_expenditure"].mean(), 1)

    }


# ==========================================================
# RESUMEN DEL EQUIPO
# ==========================================================

def get_team_summary(df: pd.DataFrame) -> pd.DataFrame:

    summary = (

        df

        .groupby("player")

        [

            MAIN_METRICS

        ]

        .mean()

        .round(2)

        .reset_index()

    )

    return summary


# ==========================================================
# RESUMEN POR POSICIÓN
# ==========================================================

def get_position_summary(df: pd.DataFrame) -> pd.DataFrame:

    summary = (

        df

        .groupby("position")

        [

            MAIN_METRICS

        ]

        .mean()

        .round(2)

        .reset_index()

    )

    return summary


# ==========================================================
# TOP JUGADORES
# ==========================================================

def top_players(

    df: pd.DataFrame,

    metric: str,

    n: int = 5

) -> pd.DataFrame:

    return (

        df

        .groupby("player")[metric]

        .mean()

        .sort_values(

            ascending=False

        )

        .head(n)

        .reset_index()

    )


# ==========================================================
# ÚLTIMOS JUGADORES
# ==========================================================

def bottom_players(

    df: pd.DataFrame,

    metric: str,

    n: int = 5

) -> pd.DataFrame:

    return (

        df

        .groupby("player")[metric]

        .mean()

        .sort_values()

        .head(n)

        .reset_index()

    )


# ==========================================================
# RANKING
# ==========================================================

def calculate_rankings(

    df: pd.DataFrame,

    metric: str

) -> pd.DataFrame:

    ranking = (

        df

        .groupby("player")[metric]

        .mean()

        .sort_values(

            ascending=False

        )

        .reset_index()

    )

    ranking["rank"] = (

        np.arange(

            1,

            len(ranking) + 1

        )

    )

    return ranking


# ==========================================================
# PERCENTILES
# ==========================================================

def calculate_percentiles(

    df: pd.DataFrame,

    metric: str

) -> pd.DataFrame:

    table = (

        df

        .groupby("player")[metric]

        .mean()

        .reset_index()

    )

    table["percentile"] = (

        table[metric]

        .rank(

            pct=True

        )

        * 100

    ).round(1)

    return table


# ==========================================================
# CARGA DEL EQUIPO
# ==========================================================

def calculate_team_load(df: pd.DataFrame) -> pd.DataFrame:

    load = (

        df

        .groupby("date")

        [

            MAIN_METRICS

        ]

        .sum()

        .reset_index()

    )

    return load


# ==========================================================
# CARGA POR SESIÓN
# ==========================================================

def calculate_session_load(df: pd.DataFrame) -> pd.DataFrame:

    load = (

        df

        .groupby(

            [

                "date",

                "type_session"

            ]

        )

        [

            MAIN_METRICS

        ]

        .mean()

        .reset_index()

    )

    return load


# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_metrics(

    df: pd.DataFrame

) -> pd.DataFrame:

    required = [

        "player",

        "date"

    ]

    missing = [

        c

        for c in required

        if c not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas: {missing}"

        )

    return df