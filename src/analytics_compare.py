"""
analytics_compare.py

Motor de análisis comparativo.

Toda la lógica de negocio del módulo de comparativas
está centralizada en este archivo.

No contiene componentes gráficos.
No contiene código de Streamlit.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.compare_config import (

    DATA_COLUMNS,

    METRICS,

    METRIC_CATEGORIES,

    ANALYSIS_TYPES

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

            f"Columnas obligatorias ausentes: {missing}"

        )

    result = df.copy()

    result[DATA_COLUMNS["date"]] = pd.to_datetime(

        result[DATA_COLUMNS["date"]],

        errors="coerce"

    )

    result = result.dropna(

        subset=[

            DATA_COLUMNS["player"],

            DATA_COLUMNS["date"]

        ]

    )

    result = result.sort_values(

        DATA_COLUMNS["date"]

    ).reset_index(

        drop=True

    )

    return result


# =============================================================================
# FILTROS DISPONIBLES
# =============================================================================

def get_available_filters(
    df: pd.DataFrame
) -> dict:
    """
    Devuelve todos los filtros necesarios
    para construir la interfaz.
    """

    df = _validate_dataframe(df)

    filters = {}

    # ---------------------------------------------------------
    # Jugadores
    # ---------------------------------------------------------

    filters["players"] = sorted(

        df[

            DATA_COLUMNS["player"]

        ]

        .dropna()

        .unique()

        .tolist()

    )

    # ---------------------------------------------------------
    # Posiciones
    # ---------------------------------------------------------

    if DATA_COLUMNS["position"] in df.columns:

        filters["positions"] = sorted(

            df[

                DATA_COLUMNS["position"]

            ]

            .dropna()

            .unique()

            .tolist()

        )

    else:

        filters["positions"] = []

    # ---------------------------------------------------------
    # Semanas
    # ---------------------------------------------------------

    if DATA_COLUMNS["week"] in df.columns:

        filters["weeks"] = sorted(

            df[

                DATA_COLUMNS["week"]

            ]

            .dropna()

            .unique()

            .tolist()

        )

    else:

        filters["weeks"] = []

    # ---------------------------------------------------------
    # Microciclos
    # ---------------------------------------------------------

    if DATA_COLUMNS["microcycle"] in df.columns:

        filters["microcycles"] = sorted(

            df[

                DATA_COLUMNS["microcycle"]

            ]

            .dropna()

            .unique()

            .tolist()

        )

    else:

        filters["microcycles"] = []

    # ---------------------------------------------------------
    # Sesiones
    # ---------------------------------------------------------

    if DATA_COLUMNS["session"] in df.columns:

        filters["sessions"] = sorted(

            df[

                DATA_COLUMNS["session"]

            ]

            .dropna()

            .unique()

            .tolist()

        )

    else:

        filters["sessions"] = []

    # ---------------------------------------------------------
    # Métricas
    # ---------------------------------------------------------

    filters["metrics"] = pd.DataFrame(

        [

            {

                "metric": metric,

                **config

            }

            for metric, config

            in METRICS.items()

        ]

    ).sort_values(

        "order"

    ).reset_index(

        drop=True

    )

    # ---------------------------------------------------------
    # Fechas
    # ---------------------------------------------------------

    filters["dates"] = {

        "min": df[

            DATA_COLUMNS["date"]

        ].min(),

        "max": df[

            DATA_COLUMNS["date"]

        ].max()

    }

    return filters

# =============================================================================
# HELPERS · FILTROS
# =============================================================================

def _filter_period(
    df: pd.DataFrame,
    start_date=None,
    end_date=None
) -> pd.DataFrame:
    """
    Filtra el DataFrame por un rango de fechas.
    """

    result = df.copy()

    date_col = DATA_COLUMNS["date"]

    if start_date is not None:

        result = result[

            result[date_col] >= pd.Timestamp(start_date)

        ]

    if end_date is not None:

        result = result[

            result[date_col] <= pd.Timestamp(end_date)

        ]

    return result.reset_index(drop=True)


def _filter_entities(
    df: pd.DataFrame,
    filters: dict | None
) -> pd.DataFrame:
    """
    Aplica cualquier filtro definido en un diccionario.

    Ejemplo

    {

        "player":"Kirian",

        "position":"MC"

    }

    """

    if filters is None:

        return df.copy()

    result = df.copy()

    for key, value in filters.items():

        if key not in DATA_COLUMNS:

            continue

        column = DATA_COLUMNS[key]

        if column not in result.columns:

            continue

        if value is None:

            continue

        if isinstance(

            value,

            (list, tuple, set)

        ):

            result = result[

                result[column].isin(value)

            ]

        else:

            result = result[

                result[column] == value

            ]

    return result.reset_index(drop=True)


def _remove_reference_from_comparison(
    comparison_df: pd.DataFrame,
    reference_filters: dict | None
) -> pd.DataFrame:
    """
    Evita comparar un jugador consigo mismo
    o una posición consigo misma cuando la
    comparación es contra la plantilla.
    """

    if reference_filters is None:

        return comparison_df

    result = comparison_df.copy()

    for key, value in reference_filters.items():

        if key not in DATA_COLUMNS:

            continue

        column = DATA_COLUMNS[key]

        if column not in result.columns:

            continue

        result = result[

            result[column] != value

        ]

    return result.reset_index(drop=True)


# =============================================================================
# HELPERS · MÉTRICAS
# =============================================================================

def _get_valid_metrics(
    df: pd.DataFrame,
    metrics: list | None
) -> list:
    """
    Devuelve únicamente las métricas válidas
    existentes en el DataFrame.
    """

    if metrics is None:

        metrics = [

            metric

            for metric, config

            in METRICS.items()

            if config["default"]

        ]

    return [

        metric

        for metric in metrics

        if metric in df.columns

    ]


def _calculate_means(
    df: pd.DataFrame,
    metrics: list
) -> pd.Series:
    """
    Calcula la media de cada métrica.
    """

    if len(metrics) == 0:

        return pd.Series(dtype=float)

    return (

        df[metrics]

        .mean(

            numeric_only=True,

            skipna=True

        )

    )


# =============================================================================
# PREPARACIÓN
# =============================================================================

# =============================================================================
# PREPARACIÓN
# =============================================================================

def _prepare_dataframes(
    df: pd.DataFrame,
    reference_filters: dict,
    comparison_filters: dict | None,
    metrics: list,
    start_date=None,
    end_date=None,
    week=None,
    microcycle=None,
    session=None,
    position_filter=None
):
    """
    Prepara los DataFrames de referencia y comparación.
    """

    # ---------------------------------------------------------
    # PERIODO
    # ---------------------------------------------------------

    df = _filter_period(

        df,

        start_date,

        end_date

    )

    # ---------------------------------------------------------
    # FILTROS GLOBALES
    # ---------------------------------------------------------

    if week is not None:

        df = df[

            df[

                DATA_COLUMNS["week"]

            ] == week

        ]

    if microcycle is not None:

        df = df[

            df[

                DATA_COLUMNS["microcycle"]

            ] == microcycle

        ]

    if session is not None:

        df = df[

            df[

                DATA_COLUMNS["session"]

            ] == session

        ]

    if position_filter is not None:

        df = df[

            df[

                DATA_COLUMNS["position"]

            ] == position_filter

        ]

    df = df.reset_index(

        drop=True

    )

    # ---------------------------------------------------------
    # REFERENCIA
    # ---------------------------------------------------------

    reference_df = _filter_entities(

        df,

        reference_filters

    )

    # ---------------------------------------------------------
    # COMPARACIÓN
    # ---------------------------------------------------------

    if comparison_filters is None:

        comparison_df = _remove_reference_from_comparison(

            df,

            reference_filters

        )

    else:

        comparison_df = _filter_entities(

            df,

            comparison_filters

        )

    # ---------------------------------------------------------
    # MÉTRICAS
    # ---------------------------------------------------------

    metrics = _get_valid_metrics(

        df,

        metrics

    )

    return (

        reference_df,

        comparison_df,

        metrics

    )

# =============================================================================
# CONSTRUCCIÓN DE ESTADÍSTICAS
# =============================================================================

def _build_statistics(
    reference_means: pd.Series,
    comparison_means: pd.Series
) -> pd.DataFrame:
    """
    Construye el DataFrame maestro del análisis.

    Cada fila representa una métrica.
    """

    rows = []

    metrics = sorted(

        reference_means.index,

        key=lambda metric: METRICS[metric]["order"]

    )

    for metric in metrics:

        config = METRICS[metric]

        ref = float(

            np.nan_to_num(

                reference_means.get(metric, np.nan)

            )

        )

        comp = float(

            np.nan_to_num(

                comparison_means.get(metric, np.nan)

            )

        )

        difference = ref - comp

        if comp == 0:

            difference_pct = np.nan

        else:

            difference_pct = (

                difference / comp

            ) * 100

        maximum = max(ref, comp)

        if maximum == 0:

            ref_norm = 0

            comp_norm = 0

        else:

            ref_norm = (

                ref / maximum

            ) * 100

            comp_norm = (

                comp / maximum

            ) * 100

        rows.append(

            {

                # Identificación

                "metric": metric,

                "category": config["category"],

                "label": config["label"],

                "short": config["short"],

                "unit": config["unit"],

                "format": config["format"],

                "color": config["color"],

                "higher_is_better": config["higher_is_better"],

                "order": config["order"],

                # Valores

                "reference": ref,

                "comparison": comp,

                "difference": difference,

                "difference_pct": difference_pct,

                # Radar

                "reference_normalized": ref_norm,

                "comparison_normalized": comp_norm

            }

        )

    statistics = pd.DataFrame(

        rows

    )

    if statistics.empty:

        return statistics

    return (

        statistics

        .sort_values(

            "order"

        )

        .reset_index(

            drop=True

        )

    )


# =============================================================================
# DISTRIBUCIÓN
# =============================================================================

def _build_distribution(
    reference_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    metrics: list
) -> pd.DataFrame:
    """
    Construye el DataFrame utilizado por:

    - Boxplot
    - Histograma
    - Distribuciones
    """

    rows = []

    for metric in metrics:

        # Referencia

        if metric in reference_df.columns:

            for value in reference_df[metric].dropna():

                rows.append(

                    {

                        "metric": metric,

                        "group": "reference",

                        "value": float(value)

                    }

                )

        # Comparación

        if metric in comparison_df.columns:

            for value in comparison_df[metric].dropna():

                rows.append(

                    {

                        "metric": metric,

                        "group": "comparison",

                        "value": float(value)

                    }

                )

    return pd.DataFrame(rows)


# =============================================================================
# METADATA
# =============================================================================

def _build_metadata(
    reference_df: pd.DataFrame,
    comparison_df: pd.DataFrame
) -> dict:
    """
    Información auxiliar.
    """

    return {

        "reference_rows": len(

            reference_df

        ),

        "comparison_rows": len(

            comparison_df

        ),

        "reference_players": reference_df[

            DATA_COLUMNS["player"]

        ].nunique(),

        "comparison_players": comparison_df[

            DATA_COLUMNS["player"]

        ].nunique(),

        "reference_sessions": reference_df[

            DATA_COLUMNS["date"]

        ].nunique(),

        "comparison_sessions": comparison_df[

            DATA_COLUMNS["date"]

        ].nunique()

    }

# =============================================================================
# SUMMARY
# =============================================================================

def _build_summary(
    statistics: pd.DataFrame
) -> dict:
    """
    Construye el resumen utilizado por los componentes.
    """

    if statistics.empty:

        return {

            "cards": [],

            "groups": {}

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

                "reference_normalized": row["reference_normalized"],

                "comparison_normalized": row["comparison_normalized"],

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

    return {

        "cards": cards,

        "groups": groups

    }


# =============================================================================
# INSIGHTS
# =============================================================================

def _build_insights(
    statistics: pd.DataFrame
) -> list:
    """
    Genera automáticamente los hallazgos principales.
    """

    if statistics.empty:

        return []

    insights = []

    biggest = statistics.loc[

        statistics["difference"].abs().idxmax()

    ]

    insights.append(

        {

            "level": "info",

            "title": "Mayor diferencia",

            "metric": biggest["metric"],

            "text": (

                f'{biggest["label"]}: '

                f'{biggest["difference"]:+.1f} '

                f'{biggest["unit"]}'

            )

        }

    )

    positives = statistics[

        statistics["difference"] > 0

    ]

    if not positives.empty:

        best = positives.iloc[0]

        insights.append(

            {

                "level": "success",

                "title": "Punto fuerte",

                "metric": best["metric"],

                "text": (

                    f'{best["label"]} '

                    f'(+{best["difference"]:.1f} {best["unit"]})'

                )

            }

        )

    negatives = statistics[

        statistics["difference"] < 0

    ]

    if not negatives.empty:

        worst = negatives.iloc[0]

        insights.append(

            {

                "level": "warning",

                "title": "Principal diferencia",

                "metric": worst["metric"],

                "text": (

                    f'{worst["label"]} '

                    f'({worst["difference"]:.1f} {worst["unit"]})'

                )

            }

        )

    return insights


# =============================================================================
# HEADER
# =============================================================================

def _build_header(
    analysis_type: str,
    reference_filters: dict,
    comparison_filters: dict | None
) -> dict:
    """
    Construye la información de cabecera.
    """

    config = ANALYSIS_TYPES[analysis_type]

    reference_name = list(

        reference_filters.values()

    )[0]

    if comparison_filters is None:

        comparison_name = "Plantilla"

    else:

        comparison_name = list(

            comparison_filters.values()

        )[0]

    return {

        "title": config["label"],

        "analysis_type": analysis_type,

        "reference_name": reference_name,

        "comparison_name": comparison_name

    }


# =============================================================================
# VISUALIZACIONES
# =============================================================================

def _build_visualizations(
    analysis_type: str
) -> list:
    """
    Devuelve el layout definido en compare_config.
    """

    return ANALYSIS_TYPES[

        analysis_type

    ]["layout"]

# =============================================================================
# BUILDER
# =============================================================================

def _build_comparison(
    analysis_type: str,
    reference_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    metrics: list,
    reference_filters: dict,
    comparison_filters: dict | None
) -> dict:
    """
    Construye el objeto completo de comparación.
    """

    # ---------------------------------------------------------
    # MEDIAS
    # ---------------------------------------------------------

    reference_means = _calculate_means(

        reference_df,

        metrics

    )

    comparison_means = _calculate_means(

        comparison_df,

        metrics

    )

    # ---------------------------------------------------------
    # ESTADÍSTICAS
    # ---------------------------------------------------------

    statistics = _build_statistics(

        reference_means,

        comparison_means

    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary = _build_summary(

        statistics

    )

    # ---------------------------------------------------------
    # DISTRIBUCIÓN
    # ---------------------------------------------------------

    distribution = _build_distribution(

        reference_df,

        comparison_df,

        metrics

    )

    # ---------------------------------------------------------
    # INSIGHTS
    # ---------------------------------------------------------

    insights = _build_insights(

        statistics

    )

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    header = _build_header(

        analysis_type,

        reference_filters,

        comparison_filters

    )

    # ---------------------------------------------------------
    # METADATA
    # ---------------------------------------------------------

    metadata = _build_metadata(

        reference_df,

        comparison_df

    )

    # ---------------------------------------------------------
    # VISUALIZACIONES
    # ---------------------------------------------------------

    visualizations = _build_visualizations(

        analysis_type

    )

    return {

        "header": header,

        "metadata": metadata,

        "summary": summary,

        "statistics": statistics,

        "distribution": distribution,

        "visualizations": visualizations,

        "insights": insights

    }

# =============================================================================
# API PÚBLICA
# =============================================================================

def build_comparison(

    df: pd.DataFrame,

    analysis_type: str,

    reference: dict,

    comparison: dict | None = None,

    metrics: list | None = None,

    start_date=None,

    end_date=None,

    week=None,

    microcycle=None,

    session=None,

    position_filter=None

) -> dict:
    """
    Punto de entrada del motor de comparativas.
    """

    # ---------------------------------------------------------
    # VALIDACIÓN
    # ---------------------------------------------------------

    if analysis_type not in ANALYSIS_TYPES:

        raise ValueError(

            f"Tipo de análisis no válido: {analysis_type}"

        )

    df = _validate_dataframe(df)

    reference_df, comparison_df, metrics = _prepare_dataframes(

        df=df,

        reference_filters=reference,

        comparison_filters=comparison,

        metrics=metrics,

        start_date=start_date,

        end_date=end_date,

        week=week,

        microcycle=microcycle,

        session=session,

        position_filter=position_filter

    )
    # ---------------------------------------------------------
    # BUILDER
    # ---------------------------------------------------------

    return _build_comparison(

        analysis_type=analysis_type,

        reference_df=reference_df,

        comparison_df=comparison_df,

        metrics=metrics,

        reference_filters=reference,

        comparison_filters=comparison

    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [

    "build_comparison",

    "get_available_filters"

]