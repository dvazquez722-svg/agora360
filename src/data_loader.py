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
# CLUB ACTIVO
# =============================================================================

def get_club_path() -> Path:
    """
    Devuelve la carpeta de datos del club activo.
    """

    if "user" not in st.session_state:

        raise RuntimeError(
            "No existe un usuario autenticado."
        )

    club = st.session_state["user"]["club"]

    return Path("data") / "clubs" / club


# =============================================================================
# FUNCIONES INTERNAS
# =============================================================================

def _read_csv(path: Path) -> pd.DataFrame:
    """
    Lee un CSV comprobando previamente su existencia.
    """

    if not path.exists():

        raise FileNotFoundError(
            f"No se encontró el archivo:\n{path}"
        )

    return pd.read_csv(path)


def _prepare_clean_dataset(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Limpieza básica del dataset principal.
    """

    df = df.copy()

    df.columns = df.columns.str.strip()

    for col in df.columns:

        if "date" in col.lower() or "fecha" in col.lower():

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


def _prepare_session_dataset(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Limpieza básica del dataset de sesiones.
    """

    df = df.copy()

    df.columns = df.columns.str.strip()

    for col in df.columns:

        if "date" in col.lower() or "fecha" in col.lower():

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


# =============================================================================
# CARGA DATASET PRINCIPAL
# =============================================================================

@st.cache_data(show_spinner=False)
def load_clean_data() -> pd.DataFrame:
    """
    Carga el dataset principal.
    """

    data_dir = get_club_path() / "processed"

    clean_data = data_dir / "dataset_clean.csv"

    df = _read_csv(clean_data)

    return _prepare_clean_dataset(df)


# =============================================================================
# CARGA DATASET SESIONES
# =============================================================================

@st.cache_data(show_spinner=False)
def load_session_data() -> pd.DataFrame:
    """
    Carga el dataset de sesiones.
    """

    data_dir = get_club_path() / "processed"

    session_data = data_dir / "dataset_sessions.csv"

    df = _read_csv(session_data)

    return _prepare_session_dataset(df)


# =============================================================================
# CARGA GLOBAL
# =============================================================================

@st.cache_data(show_spinner=False)
def load_data() -> dict:
    """
    Devuelve todos los datasets del club activo.
    """

    return {

        "clean": load_clean_data(),

        "sessions": load_session_data()

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

        "session_columns": len(data["sessions"].columns)

    }