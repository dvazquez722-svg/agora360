"""
analytics_compare.py

Motor de análisis comparativo.

Este módulo contiene toda la lógica necesaria para construir
comparaciones entre jugadores, posiciones, plantilla y periodos.

No contiene componentes gráficos ni código de Streamlit.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.compare_config import (
    DATA_COLUMNS,
    METRICS,
    METRIC_CATEGORIES,
    ANALYSIS_TYPES,
    VISUALIZATIONS
)

# =============================================================================
# VALIDACIÓN
# =============================================================================

def _validate_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Valida y prepara el DataFrame.
    """

    required = [
        DATA_COLUMNS["player"],
        DATA_COLUMNS["date"]
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Columnas obligatorias no encontradas: {missing}"
        )

    df = df.copy()

    df[DATA_COLUMNS["date"]] = pd.to_datetime(
        df[DATA_COLUMNS["date"]],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            DATA_COLUMNS["player"],
            DATA_COLUMNS["date"]
        ]
    )

    df = df.sort_values(
        DATA_COLUMNS["date"]
    ).reset_index(
        drop=True
    )

    return df


# =============================================================================
# FILTROS PÚBLICOS
# =============================================================================

def get_players(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Devuelve los jugadores disponibles.
    """

    df = _validate_dataframe(df)

    column = DATA_COLUMNS["player"]

    players = (
        df[[column]]
        .dropna()
        .drop_duplicates()
        .sort_values(column)
        .rename(columns={column: "value"})
    )

    players["label"] = players["value"]

    return players[
        ["label", "value"]
    ].reset_index(drop=True)


def get_positions(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Devuelve las posiciones disponibles.
    """

    column = DATA_COLUMNS["position"]

    if column not in df.columns:
        return pd.DataFrame(
            columns=["label", "value"]
        )

    positions = (
        df[[column]]
        .dropna()
        .drop_duplicates()
        .sort_values(column)
        .rename(columns={column: "value"})
    )

    positions["label"] = positions["value"]

    return positions[
        ["label", "value"]
    ].reset_index(drop=True)


def get_sessions(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Devuelve las sesiones disponibles.
    """

    column = DATA_COLUMNS["session"]

    if column not in df.columns:
        return pd.DataFrame(
            columns=["label", "value"]
        )

    sessions = (
        df[[column]]
        .dropna()
        .drop_duplicates()
        .sort_values(column)
        .rename(columns={column: "value"})
    )

    sessions["label"] = sessions["value"]

    return sessions[
        ["label", "value"]
    ].reset_index(drop=True)


def get_microcycles(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Devuelve los microciclos disponibles.
    """

    column = DATA_COLUMNS["microcycle"]

    if column not in df.columns:
        return pd.DataFrame(
            columns=["label", "value"]
        )

    microcycles = (
        df[[column]]
        .dropna()
        .drop_duplicates()
        .sort_values(column)
        .rename(columns={column: "value"})
    )

    microcycles["label"] = microcycles["value"]

    return microcycles[
        ["label", "value"]
    ].reset_index(drop=True)


def get_weeks(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Devuelve las semanas disponibles.
    """

    column = DATA_COLUMNS["week"]

    if column not in df.columns:
        return pd.DataFrame(
            columns=["label", "value"]
        )

    weeks = (
        df[[column]]
        .dropna()
        .drop_duplicates()
        .sort_values(column)
        .rename(columns={column: "value"})
    )

    weeks["label"] = weeks["value"]

    return weeks[
        ["label", "value"]
    ].reset_index(drop=True)


def get_dates(
    df: pd.DataFrame
) -> dict:
    """
    Devuelve el rango temporal disponible.
    """

    df = _validate_dataframe(df)

    column = DATA_COLUMNS["date"]

    return {

        "min": df[column].min(),

        "max": df[column].max()

    }


def get_metrics() -> pd.DataFrame:
    """
    Devuelve el catálogo completo de métricas.
    """

    rows = []

    for metric, config in METRICS.items():

        rows.append(

            {

                "metric": metric,

                **config

            }

        )

    return (

        pd.DataFrame(rows)

        .sort_values(

            "order"

        )

        .reset_index(

            drop=True

        )

    )

# =============================================================================
# HELPERS · SELECCIÓN
# =============================================================================

def _select_period(
    df: pd.DataFrame,
    start_date=None,
    end_date=None
) -> pd.DataFrame:
    """
    Filtra un DataFrame por rango de fechas.
    """

    result = df.copy()

    column = DATA_COLUMNS["date"]

    if start_date is not None:

        result = result[
            result[column] >= pd.Timestamp(start_date)
        ]

    if end_date is not None:

        result = result[
            result[column] <= pd.Timestamp(end_date)
        ]

    return result.reset_index(drop=True)


def _select_entities(
    df: pd.DataFrame,
    column: str,
    values
) -> pd.DataFrame:
    """
    Filtra una o varias entidades.

    Parameters
    ----------
    column
        Nombre REAL de la columna del DataFrame.
    """

    if column not in df.columns:

        return df.copy()

    if values is None:

        return df.copy()

    if not isinstance(values, (list, tuple, set)):

        values = [values]

    return (

        df[
            df[column].isin(values)
        ]

        .reset_index(drop=True)

    )


def _select_metrics(
    df: pd.DataFrame,
    metrics: list
) -> pd.DataFrame:
    """
    Devuelve únicamente las columnas de identificación
    junto con las métricas seleccionadas.
    """

    keep = []

    for key in DATA_COLUMNS.values():

        if key in df.columns:

            keep.append(key)

    metrics = [

        metric

        for metric in metrics

        if metric in df.columns

    ]

    keep.extend(metrics)

    keep = list(dict.fromkeys(keep))

    return df[keep].copy()


# =============================================================================
# HELPERS · AGRUPACIÓN
# =============================================================================

def _average_metrics(
    df: pd.DataFrame,
    metrics: list
) -> pd.Series:
    """
    Calcula la media de las métricas seleccionadas.
    """

    metrics = [

        metric

        for metric in metrics

        if metric in df.columns

    ]

    if len(metrics) == 0:

        return pd.Series(dtype=float)

    return (

        df[metrics]

        .mean(
            numeric_only=True,
            skipna=True
        )

    )


def _group_metrics(
    df: pd.DataFrame,
    group_by: str,
    metrics: list
) -> pd.DataFrame:
    """
    Agrupa métricas por una columna.
    """

    if group_by not in df.columns:

        return pd.DataFrame()

    metrics = [

        metric

        for metric in metrics

        if metric in df.columns

    ]

    grouped = (

        df

        .groupby(group_by)[metrics]

        .mean()

        .reset_index()

    )

    ordered = sorted(

        metrics,

        key=lambda metric: METRICS[metric]["order"]

    )

    return grouped[
        [group_by] + ordered
    ]


# =============================================================================
# HELPERS · ESTADÍSTICAS
# =============================================================================

def _calculate_statistics(
    reference: pd.Series,
    comparison: pd.Series
) -> pd.DataFrame:
    """
    Construye el DataFrame maestro utilizado por todo
    el módulo de comparativas.
    """

    rows = []

    metrics = [

        metric

        for metric in reference.index

        if metric in comparison.index

    ]

    metrics = sorted(

        metrics,

        key=lambda metric: METRICS[metric]["order"]

    )

    for metric in metrics:

        ref = float(

            np.nan_to_num(

                reference.get(metric, np.nan)

            )

        )

        comp = float(

            np.nan_to_num(

                comparison.get(metric, np.nan)

            )

        )

        difference = ref - comp

        abs_difference = abs(difference)

        if comp == 0:

            difference_pct = np.nan

        else:

            difference_pct = (

                difference / comp

            ) * 100

        if difference > 0:

            direction = "higher"

        elif difference < 0:

            direction = "lower"

        else:

            direction = "equal"

        config = METRICS[metric]
        
        # ------------------------------------------
        # Valores normalizados (0-100)
        # ------------------------------------------

        maximum = max(ref, comp)

        if maximum == 0:

            reference_normalized = 0

            comparison_normalized = 0

        else:

            reference_normalized = (ref / maximum) * 100

            comparison_normalized = (comp / maximum) * 100

        rows.append(

            {

                "metric": metric,

                "label": config["label"],

                "short": config["short"],

                "category": config["category"],

                "unit": config["unit"],

                "format": config["format"],

                "color": config["color"],

                "higher_is_better": config["higher_is_better"],

                "order": config["order"],

                "reference": ref,

                "comparison": comp,

                "reference_normalized": reference_normalized,

                "comparison_normalized": comparison_normalized,

                "difference_pct": difference_pct,

                "abs_difference": abs_difference,

                "direction": direction

            }

        )

    statistics = pd.DataFrame(rows)

    if statistics.empty:

        return statistics

    return (

        statistics

        .sort_values("order")

        .reset_index(drop=True)

    )

# =============================================================================
# PREPARACIÓN · SUMMARY
# =============================================================================

def _prepare_summary(
    statistics: pd.DataFrame
) -> dict:
    """
    Construye el resumen principal del análisis.
    """

    if statistics.empty:

        return {

            "cards": [],

            "groups": {},

            "top_positive": [],

            "top_negative": []

        }

    cards = []

    for _, row in statistics.iterrows():

        cards.append(

            {

                "metric": row["metric"],

                "label": row["label"],

                "short": row["short"],

                "category": row["category"],

                "reference": row["reference"],

                "comparison": row["comparison"],

                "difference": row["difference"],

                "difference_pct": row["difference_pct"],

                "direction": row["direction"],

                "unit": row["unit"],

                "format": row["format"],

                "color": row["color"],

                "higher_is_better": row["higher_is_better"]

            }

        )

    groups = {}

    ordered_categories = sorted(

        METRIC_CATEGORIES,

        key=lambda x: METRIC_CATEGORIES[x]["order"]

    )

    for category in ordered_categories:

        groups[category] = [

            card

            for card in cards

            if card["category"] == category

        ]

    top_positive = sorted(

        cards,

        key=lambda x: x["difference"],

        reverse=True

    )[:3]

    top_negative = sorted(

        cards,

        key=lambda x: x["difference"]

    )[:3]

    return {

        "cards": cards,

        "groups": groups,

        "top_positive": top_positive,

        "top_negative": top_negative

    }


# =============================================================================
# PREPARACIÓN · HEADER
# =============================================================================

def _prepare_header(
    analysis_type: str
) -> dict:
    """
    Construye la cabecera del análisis.
    """

    config = ANALYSIS_TYPES[analysis_type]

    return {

        "title": config["label"],

        "analysis_type": analysis_type

    }


# =============================================================================
# PREPARACIÓN · METADATA
# =============================================================================

def _prepare_metadata(
    reference_df: pd.DataFrame,
    comparison_df: pd.DataFrame
) -> dict:
    """
    Información auxiliar del análisis.
    """

    return {

        "reference_rows": len(reference_df),

        "comparison_rows": len(comparison_df),

        "reference_players": reference_df[
            DATA_COLUMNS["player"]
        ].nunique(),

        "comparison_players": comparison_df[
            DATA_COLUMNS["player"]
        ].nunique(),

        "reference_dates": reference_df[
            DATA_COLUMNS["date"]
        ].nunique(),

        "comparison_dates": comparison_df[
            DATA_COLUMNS["date"]
        ].nunique()

    }


# =============================================================================
# PREPARACIÓN · VISUALIZACIONES
# =============================================================================

def _prepare_visualizations(
    analysis_type: str,
    statistics: pd.DataFrame
) -> list:
    """
    Construye automáticamente las visualizaciones
    definidas en compare_config.py.
    """

    visualizations = []

    layout = ANALYSIS_TYPES[analysis_type]["layout"]

    for section in layout:

        section_type = section["type"]

        if section_type in [

            "summary",

            "insights"

        ]:

            continue

        config = VISUALIZATIONS[section_type]

        visualizations.append(

            {

                "type": section_type,

                "title": config["label"],

                "component": config["component"],

                "data": statistics.copy()

            }

        )

    return visualizations


# =============================================================================
# PREPARACIÓN · INSIGHTS
# =============================================================================

def _prepare_insights(
    statistics: pd.DataFrame,
    analysis_type: str
) -> list:
    """
    Genera automáticamente hallazgos del análisis.

    Esta función crecerá con el tiempo dependiendo
    del tipo de comparación.
    """

    if statistics.empty:

        return []

    insights = []

    biggest = statistics.loc[
        statistics["abs_difference"].idxmax()
    ]

    insights.append(

        {

            "level": "info",

            "title": "Mayor diferencia",

            "metric": biggest["metric"],

            "text": (

                f'{biggest["label"]}: '

                f'{biggest["difference"]:.1f} '

                f'{biggest["unit"]}'

            )

        }

    )

    positive = statistics[
        statistics["difference"] > 0
    ]

    if not positive.empty:

        row = positive.iloc[0]

        insights.append(

            {

                "level": "success",

                "title": "Principal ventaja",

                "metric": row["metric"],

                "text": row["label"]

            }

        )

    negative = statistics[
        statistics["difference"] < 0
    ]

    if not negative.empty:

        row = negative.iloc[0]

        insights.append(

            {

                "level": "warning",

                "title": "Principal diferencia negativa",

                "metric": row["metric"],

                "text": row["label"]

            }

        )

    return insights

# =============================================================================
# BUILDER
# =============================================================================

def _build_comparison(
    analysis_type: str,
    reference_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    metrics: list
) -> dict:
    """
    Construye el objeto completo de comparación.

    Esta función centraliza toda la lógica del motor.
    """

    reference = _average_metrics(

        reference_df,

        metrics

    )

    comparison = _average_metrics(

        comparison_df,

        metrics

    )

    statistics = _calculate_statistics(

        reference,

        comparison

    )

    summary = _prepare_summary(

        statistics

    )

    visualizations = _prepare_visualizations(

        analysis_type,

        statistics

    )

    insights = _prepare_insights(

        statistics,

        analysis_type

    )

    metadata = _prepare_metadata(

        reference_df,

        comparison_df

    )

    header = _prepare_header(

        analysis_type

    )

    return {

        "header": header,

        "metadata": metadata,

        "summary": summary,

        "visualizations": visualizations,

        "insights": insights,

        "statistics": statistics,

        "reference": reference,

        "comparison": comparison

    }


# =============================================================================
# API PÚBLICA
# =============================================================================

def get_available_filters(
    df: pd.DataFrame
) -> dict:
    """
    Devuelve todos los filtros necesarios para construir
    la interfaz de comparativas.
    """

    df = _validate_dataframe(df)

    return {

        "players": get_players(df),

        "positions": get_positions(df),

        "weeks": get_weeks(df),

        "sessions": get_sessions(df),

        "microcycles": get_microcycles(df),

        "metrics": get_metrics(),

        "dates": get_dates(df)

    }


def build_comparison(
    df: pd.DataFrame,
    analysis_type: str,
    reference: dict,
    comparison: dict | None = None,
    metrics: list | None = None,
    start_date=None,
    end_date=None
) -> dict:
    """
    Construye cualquier comparación soportada
    por el motor.
    """

    if analysis_type not in ANALYSIS_TYPES:

        raise ValueError(

            f"Tipo de análisis no válido: {analysis_type}"

        )

    df = _validate_dataframe(df)

    df = _select_period(

        df,

        start_date,

        end_date

    )

    if metrics is None:

        metrics = [

            metric

            for metric, config

            in METRICS.items()

            if config["default"]

        ]

    reference_df = df.copy()

    for column, value in reference.items():

        if column not in DATA_COLUMNS:

            continue

        reference_df = _select_entities(

            reference_df,

            DATA_COLUMNS[column],

            value

        )

    if comparison is None:

        comparison_df = df.copy()

        if "player" in reference:

            comparison_df = comparison_df[

                comparison_df[
                    DATA_COLUMNS["player"]
                ]

                != reference["player"]

            ]

        if "position" in reference:

            comparison_df = comparison_df[

                comparison_df[
                    DATA_COLUMNS["position"]
                ]

                != reference["position"]

            ]

    else:

        comparison_df = df.copy()

        for column, value in comparison.items():

            if column not in DATA_COLUMNS:

                continue

            comparison_df = _select_entities(

                comparison_df,

                DATA_COLUMNS[column],

                value

            )

    reference_df = _select_metrics(

        reference_df,

        metrics

    )

    comparison_df = _select_metrics(

        comparison_df,

        metrics

    )

    return _build_comparison(

        analysis_type=analysis_type,

        reference_df=reference_df,

        comparison_df=comparison_df,

        metrics=metrics

    )

# =============================================================================
# UTILIDADES
# =============================================================================

def get_default_metrics() -> list:
    """
    Devuelve las métricas marcadas como default
    en compare_config.py.
    """

    return [

        metric

        for metric, config

        in METRICS.items()

        if config["default"]

    ]


def get_metric_info(
    metric: str
) -> dict:
    """
    Devuelve la configuración completa de una métrica.
    """

    return METRICS.get(metric, {})


def get_analysis_config(
    analysis_type: str
) -> dict:
    """
    Devuelve la configuración del tipo de análisis.
    """

    if analysis_type not in ANALYSIS_TYPES:

        raise ValueError(

            f"Tipo de análisis no válido: {analysis_type}"

        )

    return ANALYSIS_TYPES[analysis_type]


def get_layout(
    analysis_type: str
) -> list:
    """
    Devuelve el layout definido para un análisis.
    """

    return get_analysis_config(

        analysis_type

    )["layout"]


def get_visualization_config(
    visualization_type: str
) -> dict:
    """
    Devuelve la configuración de una visualización.
    """

    if visualization_type not in VISUALIZATIONS:

        raise ValueError(

            f"Visualización no válida: {visualization_type}"

        )

    return VISUALIZATIONS[visualization_type]


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [

    "build_comparison",

    "get_available_filters",

    "get_default_metrics",

    "get_metric_info",

    "get_analysis_config",

    "get_layout",

    "get_visualization_config"

]