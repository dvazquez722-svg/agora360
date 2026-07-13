"""
data_loader.py
--------------
Carga y preparación de los datos de la aplicación.

Responsabilidades:
- Cargar los datasets
- Validar su existencia
- Convertir tipos de datos
- Cachear la información
- Devolver DataFrames listos para usar

No contiene lógica deportiva.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# =============================================================================
# RUTAS
# =============================================================================

DATA_DIR = Path("data") / "processed"

CLEAN_DATA = DATA_DIR / "dataset_clean.csv"
SESSION_DATA = DATA_DIR / "dataset_sessions.csv"


# =============================================================================
# FUNCIONES INTERNAS
# =============================================================================

def _read_csv(path: Path) -> pd.DataFrame:
    """
    Lee un archivo CSV comprobando previamente su existencia.
    """

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    return pd.read_csv(path)


def _prepare_clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza básica del dataset principal.
    """

    df = df.copy()

    # Eliminar espacios en nombres de columnas
    df.columns = df.columns.str.strip()

    # Convertir columnas de fecha
    for col in df.columns:
        if "date" in col.lower() or "fecha" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def _prepare_session_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza básica del dataset de sesiones.
    """

    df = df.copy()

    df.columns = df.columns.str.strip()

    for col in df.columns:
        if "date" in col.lower() or "fecha" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# =============================================================================
# CARGA DE DATOS
# =============================================================================

@st.cache_data(show_spinner=False)
def load_clean_data() -> pd.DataFrame:
    """
    Carga el dataset principal.
    """

    df = _read_csv(CLEAN_DATA)

    return _prepare_clean_dataset(df)


@st.cache_data(show_spinner=False)
def load_session_data() -> pd.DataFrame:
    """
    Carga el dataset de sesiones.
    """

    df = _read_csv(SESSION_DATA)

    return _prepare_session_dataset(df)


# =============================================================================
# CARGA GLOBAL
# =============================================================================

@st.cache_data(show_spinner=False)
def load_data() -> dict:
    """
    Devuelve todos los datasets de la aplicación.
    """

    return {
        "clean": load_clean_data(),
        "sessions": load_session_data(),
    }


# =============================================================================
# INFORMACIÓN
# =============================================================================

def dataset_info() -> dict:
    """
    Información básica de los datasets.
    """

    data = load_data()

    return {
        "clean_rows": len(data["clean"]),
        "clean_columns": len(data["clean"].columns),
        "session_rows": len(data["sessions"]),
        "session_columns": len(data["sessions"].columns),
    }