"""
utils.py
---------
Funciones auxiliares reutilizables para toda la aplicación.

Responsabilidades:
- Fechas
- Formatos
- Colores
- Iconos
- Conversión de valores
- Utilidades generales

No contiene lógica deportiva.
"""

from datetime import datetime

import pandas as pd


# =============================================================================
# FORMATO
# =============================================================================

def format_number(value, decimals=1):
    """
    Formatea un número.
    """

    if pd.isna(value):
        return "-"

    return f"{value:.{decimals}f}"


def format_percentage(value, decimals=0):
    """
    Convierte un decimal en porcentaje.
    """

    if pd.isna(value):
        return "-"

    return f"{value * 100:.{decimals}f}%"


def format_integer(value):
    """
    Formatea enteros.
    """

    if pd.isna(value):
        return "-"

    return f"{int(value):,}"


# =============================================================================
# FECHAS
# =============================================================================

def format_date(date):
    """
    Convierte fechas al formato dd/mm/yyyy.
    """

    if pd.isna(date):
        return "-"

    return pd.to_datetime(date).strftime("%d/%m/%Y")


def today():
    """
    Devuelve la fecha actual.
    """

    return datetime.today()


# =============================================================================
# COLORES
# =============================================================================

def risk_color(level):
    """
    Color asociado a un nivel de riesgo.
    """

    level = str(level).lower()

    mapping = {
        "muy bajo": "#22C55E",
        "bajo": "#84CC16",
        "moderado": "#EAB308",
        "alto": "#F97316",
        "muy alto": "#EF4444"
    }

    return mapping.get(level, "#94A3B8")


def status_color(status):
    """
    Color asociado a un estado.
    """

    status = str(status).lower()

    mapping = {
        "ok": "#22C55E",
        "correcto": "#22C55E",
        "atención": "#EAB308",
        "alerta": "#EF4444"
    }

    return mapping.get(status, "#94A3B8")


# =============================================================================
# ICONOS
# =============================================================================

def status_icon(status):
    """
    Icono asociado a un estado.
    """

    status = str(status).lower()

    mapping = {
        "ok": "🟢",
        "correcto": "🟢",
        "atención": "🟡",
        "riesgo": "🟠",
        "alerta": "🔴"
    }

    return mapping.get(status, "⚪")


# =============================================================================
# DATAFRAME
# =============================================================================

def safe_mean(series):
    """
    Media ignorando valores nulos.
    """

    if len(series) == 0:
        return 0

    return series.dropna().mean()


def safe_sum(series):
    """
    Suma ignorando valores nulos.
    """

    if len(series) == 0:
        return 0

    return series.dropna().sum()


def latest_record(df, date_column):
    """
    Devuelve el registro más reciente.
    """

    if df.empty:
        return df

    return (
        df.sort_values(date_column)
          .iloc[-1]
    )


# =============================================================================
# TEXTO
# =============================================================================

def capitalize(text):
    """
    Capitaliza un texto.
    """

    if pd.isna(text):
        return "-"

    return str(text).strip().capitalize()


def clean_columns(df):
    """
    Limpia los nombres de columnas.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("  ", " ")
    )

    return df