from pathlib import Path
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))
import numpy as np
import pandas as pd

from config.column_mapping import COLUMN_MAPPING

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

INPUT_FOLDER = Path(r"E:\Análisis de datos\FData")

OUTPUT_FOLDER = Path(r"E:\performance_app_v2\data\processed")

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = OUTPUT_FOLDER / "dataset_clean.csv"

# ==========================================================
# BUSCAR DATASET
# ==========================================================

xlsx_files = list(INPUT_FOLDER.glob("*.xlsx"))

if not xlsx_files:

    raise FileNotFoundError(
        f"No se encontró ningún archivo XLSX en:\n{INPUT_FOLDER}"
    )

INPUT_FILE = xlsx_files[0]

print("=" * 60)
print("GENERANDO DATASET")
print("=" * 60)
print(f"Archivo encontrado: {INPUT_FILE.name}")

# ==========================================================
# CARGA
# ==========================================================

df = pd.read_excel(
    INPUT_FILE,
    engine="openpyxl"
)

print(f"\nFilas originales: {len(df)}")
print(f"Columnas originales: {len(df.columns)}")

# ==========================================================
# LIMPIEZA BÁSICA
# ==========================================================

# Eliminar columnas "Unnamed"
df = df.loc[:, ~df.columns.str.contains(r"^Unnamed", regex=True)]

# Eliminar filas completamente vacías
df = df.dropna(how="all")

# Eliminar duplicados
df = df.drop_duplicates()

# Eliminar espacios en los nombres de columnas
df.columns = df.columns.str.strip()

print(f"\nFilas tras limpieza: {len(df)}")
print(f"Columnas tras limpieza: {len(df.columns)}")

# ==========================================================
# RENOMBRAR COLUMNAS
# ==========================================================

df = df.rename(columns=COLUMN_MAPPING)

print("Columnas renombradas correctamente.")

# ==========================================================
# CONVERSIÓN DE FECHA
# ==========================================================

if "date" in df.columns:

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

# ==========================================================
# CONVERSIÓN DE VARIABLES CATEGÓRICAS
# ==========================================================

categorical_columns = [

    "player",
    "wimu_name",
    "team",
    "position",
    "sport",
    "session",
    "type_session",
    "group",
    "task",
    "match_day"

]

for col in categorical_columns:

    if col in df.columns:

        df[col] = (

            df[col]

            .astype(str)

            .str.strip()

        )

# ==========================================================
# CONVERSIÓN AUTOMÁTICA A NUMÉRICO
# ==========================================================

exclude = [

    "player",
    "wimu_name",
    "team",
    "position",
    "sport",
    "date",
    "week_calendar",
    "week_team",
    "week_match_day",
    "start_hour",
    "final_hour",
    "session",
    "type_session",
    "group",
    "task",
    "match_day",
    "signal"

]

numeric_columns = [

    c

    for c in df.columns

    if c not in exclude

]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# ==========================================================
# ORDENAR CRONOLÓGICAMENTE
# ==========================================================

if {"date", "player"}.issubset(df.columns):

    df = (

        df

        .sort_values(
            ["date", "player"]
        )

        .reset_index(drop=True)

    )

# ==========================================================
# FILTRAR ENTRENAMIENTOS (DRILLS)
# ==========================================================

if "task" in df.columns:

    before = len(df)

    df = df[
        df["task"].str.lower() == "drills"
    ].copy()

    print(
        f"\nSesiones Drills: {len(df)} "
        f"(eliminadas {before - len(df)})"
    )

# ==========================================================
# ELIMINAR JUGADORES INVÁLIDOS
# ==========================================================

df = df[
    df["player"].notna()
]

df = df[
    df["player"] != ""
]

df = df.reset_index(drop=True)

# ==========================================================
# CREAR DURACIÓN EN MINUTOS
# ==========================================================

# ==========================================================
# DURACIÓN (EXCEL -> MINUTOS)
# ==========================================================

df["minutes"] = df["drills_duration"] * 24 * 60

df.loc[df["minutes"] <= 0, "minutes"] = np.nan

# ==========================================================
# COMPROBACIÓN RÁPIDA
# ==========================================================

print("\nRESUMEN DEL DATASET")

print(f"Jugadores : {df['player'].nunique()}")

print(f"Sesiones  : {df['session'].nunique()}")

print(f"Equipos   : {df['team'].nunique()}")

print(f"Posiciones: {df['position'].nunique()}")

print(f"Filas     : {len(df)}")

# ==========================================================
# VARIABLES DE VELOCIDAD
# ==========================================================

df["high_speed_distance"] = (
    df["speed_18_21_m"]
    + df["speed_21_24_m"]
    + df["speed_24_50_m"]
)

df["very_high_speed_distance"] = (
    df["speed_21_24_m"]
    + df["speed_24_50_m"]
)

df["high_speed_actions"] = (
    df["speed_18_21_count"]
    + df["speed_21_24_count"]
    + df["speed_24_50_count"]
)

# ==========================================================
# VARIABLES DE ACELERACIÓN
# ==========================================================

df["total_accelerations"] = df["accelerations"]

df["high_accelerations"] = (
    df["acc_3_4"]
    + df["acc_4_5"]
    + df["acc_5_6"]
    + df["acc_6_10"]
)

df["very_high_accelerations"] = (
    df["acc_5_6"]
    + df["acc_6_10"]
)

# ==========================================================
# VARIABLES DE DECELERACIÓN
# ==========================================================

df["total_decelerations"] = df["decelerations"]

df["high_decelerations"] = (
    df["dec_3_2"]
    + df["dec_4_3"]
    + df["dec_5_4"]
    + df["dec_6_5"]
    + df["dec_10_6"]
)

df["very_high_decelerations"] = (
    df["dec_5_4"]
    + df["dec_6_5"]
    + df["dec_10_6"]
)

# ==========================================================
# VARIABLES RELATIVAS (POR MINUTO)
# ==========================================================

relative_metrics = {

    "distance_m": "distance_min",

    "player_load": "player_load_min",

    "abs_hsr_m": "hsr_min",

    "accelerations": "accelerations_min",

    "decelerations": "decelerations_min",

    "sprints_abs_count": "sprints_min",

    "high_speed_distance": "high_speed_distance_min",

    "very_high_speed_distance": "very_high_speed_distance_min",

    "high_accelerations": "high_accelerations_min",

    "very_high_accelerations": "very_high_accelerations_min",

    "high_decelerations": "high_decelerations_min",

    "very_high_decelerations": "very_high_decelerations_min",

    "energy_expenditure": "energy_min",

    "hmld_m": "hmld_min"

}

for original, new in relative_metrics.items():

    if original in df.columns:

        df[new] = df[original] / df["minutes"]

# ==========================================================
# RATIOS
# ==========================================================

df["hsr_ratio"] = (
    df["abs_hsr_m"] /
    df["distance_m"]
) * 100

df["high_speed_ratio"] = (
    df["high_speed_distance"] /
    df["distance_m"]
) * 100

df["sprint_ratio"] = (
    df["distance_abs_m"] /
    df["distance_m"]
) * 100

df["hmld_ratio"] = (
    df["hmld_m"] /
    df["distance_m"]
) * 100

# ==========================================================
# CARGA MECÁNICA
# ==========================================================

df["mechanical_actions"] = (

    df["accelerations"]

    +

    df["decelerations"]

    +

    df["sprints_abs_count"]

)

df["high_mechanical_actions"] = (

    df["high_accelerations"]

    +

    df["high_decelerations"]

)

# ==========================================================
# CARGA LOCOMOTORA
# ==========================================================

df["locomotor_load"] = (

    df["distance_m"]

    +

    df["abs_hsr_m"]

    +

    df["distance_abs_m"]

)

# ==========================================================
# ELIMINAR COLUMNAS REDUNDANTES
# ==========================================================

patterns = [

    # Zonas de velocidad
    "Speed Zones",

    # Zonas de aceleración
    "Acceleration Zones",

    # Impactos
    "Zones(G)",

    "H. Impacts Zones",

    # Saltos
    "Zones (Landing)",

    "Jump Take off zones",

    # Frecuencia
    "Frequency Zones",

    # Accel T
    "Accel. T Zones"

]

drop_columns = []

for col in df.columns:

    for pattern in patterns:

        if pattern in col:

            drop_columns.append(col)

            break

df.drop(
    columns=drop_columns,
    inplace=True,
    errors="ignore"
)

print(f"\nColumnas eliminadas: {len(drop_columns)}")

# ==========================================================
# LIMPIEZA DE INFINITOS
# ==========================================================

df.replace(

    [np.inf, -np.inf],

    np.nan,

    inplace=True

)

# ==========================================================
# REORDENAR COLUMNAS
# ==========================================================

priority = [

    # Identificación

    "player",

    "team",

    "position",

    "date",

    "session",

    "type_session",

    "task",

    # Tiempo

    "minutes",

    # Carga externa

    "distance_m",

    "player_load",

    "abs_hsr_m",

    "sprints_abs_count",

    "accelerations",

    "decelerations",

    # Variables derivadas

    "distance_min",

    "player_load_min",

    "hsr_min",

    "high_speed_distance",

    "high_accelerations",

    "high_decelerations"

]

existing = [

    c

    for c in priority

    if c in df.columns

]

remaining = [

    c

    for c in df.columns

    if c not in existing

]

df = df[
    existing + remaining
]

# ==========================================================
# INFORMACIÓN
# ==========================================================

print("\n====================================")

print("DATASET PREPARADO")

print("====================================")

print(f"Filas: {len(df)}")

print(f"Columnas: {len(df.columns)}")

print(f"Jugadores: {df['player'].nunique()}")

print(f"Sesiones: {df['session'].nunique()}")

# ==========================================================
# COLUMNAS A CONSERVAR
# ==========================================================

keep_columns = [

    # ======================================================
    # IDENTIFICACIÓN
    # ======================================================

    "player",
    "wimu_name",
    "team",
    "position",
    "sport",

    # ======================================================
    # FECHA
    # ======================================================

    "date",
    "week_calendar",
    "week_team",
    "week_match_day",

    # ======================================================
    # SESIÓN
    # ======================================================

    "session",
    "type_session",
    "group",
    "task",
    "match_day",

    # ======================================================
    # TIEMPO
    # ======================================================

    "drills_duration",
    "minutes",

    # ======================================================
    # DISTANCIAS
    # ======================================================

    "distance_m",
    "explosive_distance_m",
    "abs_hsr_m",
    "abs_hsr_count",

    # ======================================================
    # VELOCIDAD
    # ======================================================

    "max_speed_kmh",
    "avg_speed_kmh",

    # ======================================================
    # SPRINT
    # ======================================================

    "distance_abs_m",
    "distance_rel_m",
    "sprint_duration",
    "sprints_abs_count",
    "sprints_rel_count",

    # ======================================================
    # ACELERACIONES
    # ======================================================

    "accelerations",
    "decelerations",

    "distance_acceleration",
    "distance_deceleration",

    "max_acceleration",
    "max_deceleration",

    "avg_acceleration",
    "avg_deceleration",

    # ======================================================
    # CARDIACO
    # ======================================================

    "avg_heart_rate",
    "max_heart_rate",
    "avg_hr_percent",

    # ======================================================
    # PLAYER LOAD
    # ======================================================

    "player_load",
    "player_load_horizontal",
    "player_load_vertical",
    "player_load_anteroposterior",
    "player_load_mediolateral",

    # ======================================================
    # METABÓLICAS
    # ======================================================

    "metabolic_power",
    "metabolic_power_avg",

    "hmld_m",
    "hmld_count",

    "energy_expenditure",

    "dsl",

    # ======================================================
    # IMPACTOS
    # ======================================================

    "impacts",

    # ======================================================
    # PASOS
    # ======================================================

    "steps",
    "step_balance",

    # ======================================================
    # SALTOS
    # ======================================================

    "jumps",
    "avg_takeoff",
    "avg_landing",

    # ======================================================
    # RPE
    # ======================================================

    "rpe_general",
    "rpe_peripheral",

    # ======================================================
    # WELLNESS
    # ======================================================

    "wellness_fatigue",
    "wellness_sleep",
    "wellness_doms",
    "wellness_stress",
    "wellness_mood",

    # ======================================================
    # VARIABLES DERIVADAS
    # ======================================================

    "high_speed_distance",
    "very_high_speed_distance",
    "high_speed_actions",

    "total_accelerations",
    "high_accelerations",
    "very_high_accelerations",

    "total_decelerations",
    "high_decelerations",
    "very_high_decelerations",

    "distance_min",
    "player_load_min",
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

    "mechanical_actions",
    "high_mechanical_actions",

    "locomotor_load"

]

keep_columns = [

    c

    for c in keep_columns

    if c in df.columns

]

df = df[keep_columns].copy()

# ==========================================================
# VALIDACIÓN
# ==========================================================

required = [

    "player",

    "date",

    "distance_m",

    "player_load",

    "abs_hsr_m"

]

missing = [

    c

    for c in required

    if c not in df.columns

]

if missing:

    raise ValueError(

        f"Faltan columnas obligatorias: {missing}"

    )

# ==========================================================
# NORMALIZAR NOMBRES DE EQUIPO
# ==========================================================

df["team"] = df["team"].replace({

    "TEAM": "UD Las Palmas",

    "Udlp 2022-2023": "UD Las Palmas",

    "UD LAS PALMAS 23-24": "UD Las Palmas"

})

print(df["date"].nunique())

print(df.groupby("date").size().head(20))

# ==========================================================
# ELIMINAR FILA RESUMEN DEL EQUIPO
# ==========================================================

df = df[df["position"] != "TEAM"].copy()
# ==========================================================
# GUARDAR DATASET
# ==========================================================

df.to_csv(

    OUTPUT_FILE,

    index=False,

    encoding="utf-8-sig"

)

print("\n========================================")

print("DATASET GENERADO CORRECTAMENTE")

print("========================================")

print(f"Filas: {len(df)}")

print(f"Columnas: {len(df.columns)}")

print(f"Jugadores: {df['player'].nunique()}")

print(f"Sesiones: {df['session'].nunique()}")

print(f"\nArchivo guardado en:")

print(OUTPUT_FILE)