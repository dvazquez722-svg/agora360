from pathlib import Path

import pandas as pd

# ==========================================================
# RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "data" / "processed" / "dataset_clean.csv"

OUTPUT = BASE_DIR / "data" / "processed" / "dataset_sessions.csv"

# ==========================================================
# CARGA
# ==========================================================

df = pd.read_csv(INPUT)

df["date"] = pd.to_datetime(df["date"])

print("=" * 60)
print("GENERANDO DATASET DE SESIONES")
print("=" * 60)

print(f"Filas originales: {len(df)}")

# ==========================================================
# VARIABLES QUE SE SUMAN
# ==========================================================

SUM_COLUMNS = [

    "minutes",

    "distance_m",

    "explosive_distance_m",

    "abs_hsr_m",

    "abs_hsr_count",

    "distance_abs_m",

    "distance_rel_m",

    "sprints_abs_count",

    "sprints_rel_count",

    "accelerations",

    "decelerations",

    "distance_acceleration",

    "distance_deceleration",

    "player_load",

    "player_load_horizontal",

    "player_load_vertical",

    "player_load_anteroposterior",

    "player_load_mediolateral",

    "energy_expenditure",

    "hmld_m",

    "hmld_count",

    "dsl",

    "mechanical_actions",

    "high_mechanical_actions",

    "locomotor_load",

    "high_speed_distance",

    "very_high_speed_distance",

    "high_speed_actions",

    "high_accelerations",

    "very_high_accelerations",

    "high_decelerations",

    "very_high_decelerations"

]

# ==========================================================
# VARIABLES QUE SE PROMEDIAN
# ==========================================================

MEAN_COLUMNS = [

    "avg_speed_kmh",

    "avg_heart_rate",

    "avg_hr_percent",

    "metabolic_power",

    "metabolic_power_avg",

    "player_load_min",

    "distance_min",

    "hsr_min",

    "accelerations_min",

    "decelerations_min",

    "sprints_min",

    "high_speed_distance_min",

    "very_high_speed_distance_min",

    "high_accelerations_min",

    "very_high_accelerations_min",

    "high_decelerations_min",

    "very_high_decelerations_min",

    "energy_min",

    "hmld_min",

    "hsr_ratio",

    "high_speed_ratio",

    "sprint_ratio",

    "hmld_ratio",

    "rpe_general",

    "rpe_peripheral",

    "wellness_fatigue",

    "wellness_sleep",

    "wellness_doms",

    "wellness_stress",

    "wellness_mood"

]

# ==========================================================
# VARIABLES MÁXIMAS
# ==========================================================

MAX_COLUMNS = [

    "max_speed_kmh",

    "max_acceleration",

    "max_deceleration",

    "max_heart_rate"

]

# ==========================================================
# DICCIONARIO DE AGREGACIÓN
# ==========================================================

agg_dict = {}

# Variables que se suman
for col in SUM_COLUMNS:

    if col in df.columns:

        agg_dict[col] = "sum"

# Variables que se promedian
for col in MEAN_COLUMNS:

    if col in df.columns:

        agg_dict[col] = "mean"

# Variables máximas
for col in MAX_COLUMNS:

    if col in df.columns:

        agg_dict[col] = "max"

# ==========================================================
# AGRUPAR POR JUGADOR Y FECHA
# ==========================================================

sessions = (

    df

    .groupby(

        [

            "player",

            "date"

        ],

        as_index=False

    )

    .agg(agg_dict)

)

# ==========================================================
# INFORMACIÓN DESCRIPTIVA
# ==========================================================

info_columns = [

    "team",

    "position",

    "sport",

    "week_calendar",

    "week_team",

    "week_match_day",

    "session",

    "type_session",

    "group",

    "match_day"

]

for col in info_columns:

    if col in df.columns:

        values = (

            df

            .groupby(

                [

                    "player",

                    "date"

                ]

            )[col]

            .first()

            .reset_index()

        )

        sessions = sessions.merge(

            values,

            on=[

                "player",

                "date"

            ],

            how="left"

        )

# ==========================================================
# RECALCULAR VARIABLES RELATIVAS
# ==========================================================

sessions["distance_min"] = (

    sessions["distance_m"]

    /

    sessions["minutes"]

)

sessions["player_load_min"] = (

    sessions["player_load"]

    /

    sessions["minutes"]

)

sessions["hsr_min"] = (

    sessions["abs_hsr_m"]

    /

    sessions["minutes"]

)

sessions["accelerations_min"] = (

    sessions["accelerations"]

    /

    sessions["minutes"]

)

sessions["decelerations_min"] = (

    sessions["decelerations"]

    /

    sessions["minutes"]

)

sessions["sprints_min"] = (

    sessions["sprints_abs_count"]

    /

    sessions["minutes"]

)

sessions["high_speed_distance_min"] = (

    sessions["high_speed_distance"]

    /

    sessions["minutes"]

)

sessions["very_high_speed_distance_min"] = (

    sessions["very_high_speed_distance"]

    /

    sessions["minutes"]

)

sessions["high_accelerations_min"] = (

    sessions["high_accelerations"]

    /

    sessions["minutes"]

)

sessions["very_high_accelerations_min"] = (

    sessions["very_high_accelerations"]

    /

    sessions["minutes"]

)

sessions["high_decelerations_min"] = (

    sessions["high_decelerations"]

    /

    sessions["minutes"]

)

sessions["very_high_decelerations_min"] = (

    sessions["very_high_decelerations"]

    /

    sessions["minutes"]

)

sessions["energy_min"] = (

    sessions["energy_expenditure"]

    /

    sessions["minutes"]

)

sessions["hmld_min"] = (

    sessions["hmld_m"]

    /

    sessions["minutes"]

)

# ==========================================================
# RECALCULAR RATIOS
# ==========================================================

sessions["hsr_ratio"] = (

    sessions["abs_hsr_m"]

    /

    sessions["distance_m"]

) * 100

sessions["high_speed_ratio"] = (

    sessions["high_speed_distance"]

    /

    sessions["distance_m"]

) * 100

sessions["sprint_ratio"] = (

    sessions["distance_abs_m"]

    /

    sessions["distance_m"]

) * 100

sessions["hmld_ratio"] = (

    sessions["hmld_m"]

    /

    sessions["distance_m"]

) * 100

# ==========================================================
# ORDENAR DATASET
# ==========================================================

sessions = (

    sessions

    .sort_values(

        [

            "date",

            "player"

        ]

    )

    .reset_index(drop=True)

)

# ==========================================================
# LIMPIAR INFINITOS
# ==========================================================

sessions.replace(

    [float("inf"), float("-inf")],

    pd.NA,

    inplace=True

)

# ==========================================================
# VALIDACIÓN
# ==========================================================

required_columns = [

    "player",

    "date",

    "minutes",

    "distance_m",

    "player_load",

    "abs_hsr_m",

    "accelerations",

    "decelerations"

]

missing = [

    c

    for c in required_columns

    if c not in sessions.columns

]

if missing:

    raise ValueError(

        f"Faltan columnas obligatorias: {missing}"

    )

# ==========================================================
# GUARDAR
# ==========================================================

sessions.to_csv(

    OUTPUT,

    index=False,

    encoding="utf-8-sig"

)

# ==========================================================
# RESUMEN
# ==========================================================

print()

print("=" * 60)

print("DATASET DE SESIONES GENERADO")

print("=" * 60)

print(f"Filas: {len(sessions)}")

print(f"Columnas: {len(sessions.columns)}")

print(f"Jugadores: {sessions['player'].nunique()}")

print(f"Días registrados: {sessions['date'].nunique()}")

print(f"Periodo: {sessions['date'].min().date()} -> {sessions['date'].max().date()}")

print()

print(f"Archivo guardado en:\n{OUTPUT}")

print(sessions.head())

print()

print(sessions.info())

print()

print(sessions.describe())

print()

print(sessions.isna().mean().sort_values(ascending=False).head(20))