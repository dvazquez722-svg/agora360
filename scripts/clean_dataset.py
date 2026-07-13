from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "data" / "processed" / "Temporada 2022-2023 Las Palmas_CLEAN.csv"
OUTPUT = BASE_DIR / "data" / "processed" / "dataset_clean.csv"

df = pd.read_csv(INPUT)

# Eliminar columnas unnamed
df = df.loc[:, ~df.columns.str.startswith("unnamed")]

# Convertir fecha
df["date"] = pd.to_datetime(df["date"])

# Eliminar duplicados
df = df.drop_duplicates()

# Eliminar filas completamente vacías
df = df.dropna(how="all")

# Guardar
df.to_csv(OUTPUT, index=False)

print("Dataset limpio guardado correctamente.")
print(f"Filas: {len(df)}")
print(f"Columnas: {len(df.columns)}")