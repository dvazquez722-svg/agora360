import numpy as np
import pandas as pd

# ==========================================================
# VARIABLES DE CARGA
# ==========================================================

LOAD_METRICS = [

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
# HISTÓRICO DEL JUGADOR
# ==========================================================

def player_history(df, player):

    history = (

        df[
            df["player"] == player
        ]

        .sort_values("date")

        .reset_index(drop=True)

    )

    return history

# ==========================================================
# EWMA
# ==========================================================

def calculate_ewma(series: pd.Series, span: int) -> float:
    """
    Exponentially Weighted Moving Average.
    Da mayor peso a las sesiones más recientes.
    """

    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if len(values) == 0:

        return np.nan

    return (

        values

        .ewm(
            span=span,
            adjust=False
        )

        .mean()

        .iloc[-1]

    )

# ==========================================================
# ACUTE LOAD (7 sesiones)
# ==========================================================

def calculate_acute_load(series):

    """
    Carga aguda mediante EWMA de 7 sesiones.
    """

    return calculate_ewma(series, span=7)


# ==========================================================
# CHRONIC LOAD (28 sesiones)
# ==========================================================

def calculate_chronic_load(series):

    """
    Carga crónica mediante EWMA de 28 sesiones.
    """

    return calculate_ewma(series, span=28)
# ==========================================================
# ACWR (EWMA)
# ==========================================================

def calculate_acwr(series: pd.Series) -> float:
    """
    Acute : Chronic Workload Ratio
    mediante EWMA (7 y 28 días).
    """

    acute = calculate_acute_load(series)

    chronic = calculate_chronic_load(series)

    if pd.isna(chronic):

        return np.nan

    if chronic == 0:

        return np.nan

    return acute / chronic


# ==========================================================
# CAMBIO SEMANAL
# ==========================================================

def calculate_weekly_change(series):

    values = (

        pd.to_numeric(

            series,

            errors="coerce"

        )

        .dropna()

    )

    if len(values) < 14:

        return np.nan

    last_week = values.tail(7).mean()

    previous_week = values.iloc[-14:-7].mean()

    if previous_week == 0:

        return np.nan

    return (

        (

            last_week

            -

            previous_week

        )

        /

        previous_week

    ) * 100


# ==========================================================
# Z SCORE
# ==========================================================

def calculate_zscore(series):

    values = (

        pd.to_numeric(

            series,

            errors="coerce"

        )

        .dropna()

    )

    if len(values) < 5:

        return np.nan

    std = values.std()

    if std == 0:

        return 0

    return (

        values.iloc[-1]

        -

        values.mean()

    ) / std


# ==========================================================
# PERCENTIL
# ==========================================================

def calculate_percentile(series):

    values = (

        pd.to_numeric(

            series,

            errors="coerce"

        )

        .dropna()

    )

    if len(values) < 5:

        return np.nan

    return (

        values.rank(pct=True)

        .iloc[-1]

    ) * 100


# ==========================================================
# WORKLOAD DE UN JUGADOR
# ==========================================================

def calculate_player_workload(history: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula todas las métricas de carga para un jugador.
    """

    results = []

    history = history.sort_values("date")

    for metric in LOAD_METRICS:

        if metric not in history.columns:

            continue

        series = history[metric]

        current = pd.to_numeric(
            series,
            errors="coerce"
        ).dropna()

        n_sessions = len(current)

        if len(current) == 0:

            continue

        results.append({

            "player": history["player"].iloc[-1],

            "date": history["date"].iloc[-1],

            "metric": metric,

            "n_sessions": n_sessions,

            "current": current.iloc[-1],

            "acute_load": calculate_acute_load(series),

            "chronic_load": calculate_chronic_load(series),

            "acwr": calculate_acwr(series),

            "monotony": calculate_monotony(series),

            "strain": calculate_strain(series),

            "trend": calculate_trend(series),

            "weekly_change": calculate_weekly_change(series),

            "z_score": calculate_zscore(series),

            "percentile": calculate_percentile(series)

        })

    return pd.DataFrame(results)


# ==========================================================
# MONOTONY
# ==========================================================

def calculate_monotony(series: pd.Series) -> float:
    """
    Calcula el Training Monotony (Foster).

    Monotony = media semanal / desviación típica semanal
    """

    values = (

        pd.to_numeric(
            series,
            errors="coerce"
        )

        .dropna()

    )

    if len(values) < 7:

        return np.nan

    week = values.tail(7)

    std = week.std()

    if std == 0:

        return np.nan

    return week.mean() / std

# ==========================================================
# STRAIN
# ==========================================================

def calculate_strain(series: pd.Series) -> float:
    """
    Calcula el Training Strain (Foster).

    Strain = carga semanal × monotony
    """

    values = (

        pd.to_numeric(
            series,
            errors="coerce"
        )

        .dropna()

    )

    if len(values) < 7:

        return np.nan

    week = values.tail(7)

    monotony = calculate_monotony(series)

    if pd.isna(monotony):

        return np.nan

    return week.sum() * monotony

# ==========================================================
# TENDENCIA
# ==========================================================

def calculate_trend(series: pd.Series) -> str:
    """
    Clasifica la tendencia de la carga
    según el cambio semanal.
    """

    change = calculate_weekly_change(series)

    if pd.isna(change):

        return "Sin datos"

    if change <= -20:

        return "Descendente"

    if change < 10:

        return "Estable"

    if change < 30:

        return "Ascendente"

    return "Muy ascendente"

# ==========================================================
# DATAFRAME DE WORKLOAD
# ==========================================================

def build_workload_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye el DataFrame de carga de todos los jugadores.
    """

    workload = []

    players = sorted(df["player"].dropna().unique())

    for player in players:

        history = player_history(df, player)

        if history.empty:

            continue

        player_df = calculate_player_workload(history)

        workload.append(player_df)

    if len(workload) == 0:

        return pd.DataFrame()

    workload = (

        pd.concat(

            workload,

            ignore_index=True

        )

        .sort_values(

            [

                "player",

                "metric"

            ]

        )

        .reset_index(drop=True)

    )

    workload = pivot_workload(workload)

    workload = validate_workload_dataframe(workload)

    return workload


# ==========================================================
# WORKLOAD DE UN JUGADOR
# ==========================================================

def get_player_workload(

    workload_df: pd.DataFrame,

    player: str

):

    row = workload_df[

        workload_df["player"] == player

    ]

    if row.empty:

        return None

    return row.iloc[0]


# ==========================================================
# PIVOTAR WORKLOAD
# ==========================================================

def pivot_workload(workload_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el DataFrame de formato largo
    a formato ancho.

    Una fila por jugador.
    """

    if workload_df.empty:

        return workload_df

    pivot = (

        workload_df

        .set_index(

            [

                "player",

                "date",

                "metric"

            ]

        )

        .unstack("metric")

    )

    pivot.columns = [

        f"{metric}_{variable}"

        for variable, metric in pivot.columns

    ]

    pivot = (

        pivot

        .reset_index()

    )

    fixed = [

        "player",

        "date"

    ]

    others = sorted(

        [

            c

            for c in pivot.columns

            if c not in fixed

        ]

    )

    pivot = pivot[fixed + others]

    pivot = (

        pivot

        .sort_values("player")

        .reset_index(drop=True)

    )

    return pivot


# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_workload_dataframe(

    workload_df: pd.DataFrame

) -> pd.DataFrame:
    """
    Comprueba que el DataFrame generado
    sea válido antes de utilizarlo
    en el resto de la aplicación.
    """

    if workload_df.empty:

        return workload_df

    required_columns = [

        "player",

        "date"

    ]

    missing = [

        col

        for col in required_columns

        if col not in workload_df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas obligatorias: {missing}"

        )

    duplicated = workload_df["player"].duplicated().sum()

    if duplicated > 0:

        raise ValueError(

            "Existen jugadores duplicados en workload."

        )

    numeric_columns = workload_df.select_dtypes(

        include="number"

    ).columns

    workload_df[numeric_columns] = workload_df[

        numeric_columns

    ].replace(

        [

            np.inf,

            -np.inf

        ],

        np.nan

    )

    return workload_df