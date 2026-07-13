from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================================
# RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = BASE_DIR / "data" / "processed" / "dataset_clean.csv"

OUTPUT = BASE_DIR / "data" / "processed" / "dataset_audit.xlsx"

# ==========================================================
# CARGA
# ==========================================================

df = pd.read_csv(DATASET, low_memory=False)

print(f"\nDataset cargado correctamente")
print(f"Filas: {len(df)}")
print(f"Columnas: {len(df.columns)}")

# ==========================================================
# AUDITORÍA
# ==========================================================

results = []

for col in df.columns:

    s = df[col]

    non_null = s.notna().sum()

    missing = s.isna().sum()

    pct_non_null = round(non_null / len(df) * 100, 2)

    dtype = str(s.dtype)

    unique = s.nunique(dropna=True)

    # Estadísticos solo para columnas numéricas
    if pd.api.types.is_numeric_dtype(s):

        minimum = s.min()

        maximum = s.max()

        mean = s.mean()

        median = s.median()

        std = s.std()

    else:

        minimum = None

        maximum = None

        mean = None

        median = None

        std = None

    # Clasificación

    if pct_non_null >= 95:

        quality = "Excelente"

    elif pct_non_null >= 80:

        quality = "Buena"

    elif pct_non_null >= 50:

        quality = "Aceptable"

    else:

        quality = "Pobre"

    results.append({

        "column": col,

        "dtype": dtype,

        "non_null": non_null,

        "missing": missing,

        "coverage_%": pct_non_null,

        "unique_values": unique,

        "min": minimum,

        "max": maximum,

        "mean": mean,

        "median": median,

        "std": std,

        "quality": quality

    })

audit = pd.DataFrame(results)

audit = audit.sort_values(

    by=["quality", "coverage_%"],

    ascending=[True, False]

)

# ==========================================================
# GUARDAR
# ==========================================================

audit.to_excel(

    OUTPUT,

    index=False

)

print("\n====================================")
print("AUDITORÍA FINALIZADA")
print("====================================")

print(f"\nArchivo generado:")

print(OUTPUT)

print("\nResumen")

print(audit["quality"].value_counts())

print("\nCobertura media:")

print(round(audit["coverage_%"].mean(), 2), "%")