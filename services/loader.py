"""
=========================================================

LOADER

Carga centralizada de los datasets de la
aplicación.

=========================================================
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

DATASET_SESSIONS = PROCESSED_DIR / "dataset_sessions.csv"

DATASET_CLEAN = PROCESSED_DIR / "dataset_clean.csv"


# ==========================================================
# DATASET DE SESIONES
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Dataset principal de la aplicación.
    """

    df = pd.read_csv(

        DATASET_SESSIONS,

        low_memory=False

    )

    if "date" in df.columns:

        df["date"] = pd.to_datetime(

            df["date"],

            errors="coerce"

        )

        df = (

            df

            .sort_values("date")

            .reset_index(drop=True)

        )

    return df


# ==========================================================
# DATASET CLEAN
# ==========================================================

@st.cache_data(show_spinner=False)
def load_clean_dataset() -> pd.DataFrame:
    """
    Dataset limpio original.
    """

    df = pd.read_csv(

        DATASET_CLEAN,

        low_memory=False

    )

    if "date" in df.columns:

        df["date"] = pd.to_datetime(

            df["date"],

            errors="coerce"

        )

    return df


# ==========================================================
# ÚLTIMA FECHA
# ==========================================================

def get_last_date(df: pd.DataFrame):

    if df.empty:

        return None

    return df["date"].max()


# ==========================================================
# ÚLTIMA SESIÓN
# ==========================================================

def get_last_session(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:

        return df

    last_date = get_last_date(df)

    return (

        df

        [

            df["date"] == last_date

        ]

        .copy()

    )


# ==========================================================
# JUGADORES
# ==========================================================

def get_players(df: pd.DataFrame):

    return sorted(

        df["player"]

        .dropna()

        .unique()

    )


# ==========================================================
# POSICIONES
# ==========================================================

def get_positions(df: pd.DataFrame):

    return sorted(

        df["position"]

        .dropna()

        .unique()

    )


# ==========================================================
# SESIONES
# ==========================================================

def get_sessions(df: pd.DataFrame):

    return sorted(

        df["date"]

        .dropna()

        .unique()

    )


# ==========================================================
# VALIDACIÓN
# ==========================================================

def validate_dataset(df: pd.DataFrame):

    required = [

        "player",

        "date"

    ]

    missing = [

        col

        for col in required

        if col not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Faltan columnas obligatorias: {missing}"

        )

    return df