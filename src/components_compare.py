"""
components_compare.py

Componentes visuales del módulo de comparativas.

Todos los componentes reciben objetos preparados por
analytics_compare.py.

Nunca realizan cálculos.
"""

from __future__ import annotations

import streamlit as st

from src.compare_config import (

    ANALYSIS_TYPES,

    VISUALIZATIONS

)


# =============================================================================
# CABECERA
# =============================================================================

def comparison_header(
    header: dict
) -> None:
    """
    Cabecera de la página.
    """

    st.title(header["title"])

    st.caption(

        "Comparativa avanzada de rendimiento"

    )

    st.divider()


# =============================================================================
# SELECTOR DE ANÁLISIS
# =============================================================================

def comparison_selector() -> str:
    """
    Selector del tipo de comparación.
    """

    options = list(

        ANALYSIS_TYPES.keys()

    )

    labels = {

        key: value["label"]

        for key, value

        in ANALYSIS_TYPES.items()

    }

    selected = st.selectbox(

        "Tipo de comparación",

        options,

        format_func=lambda x: labels[x]

    )

    return selected


# =============================================================================
# FILTROS
# =============================================================================

# =============================================================================
# FILTROS
# =============================================================================

def comparison_filters(
    filters: dict,
    analysis_type: str
) -> dict:
    """
    Construye automáticamente los filtros necesarios
    para cualquier tipo de comparación.
    """

    config = ANALYSIS_TYPES[analysis_type]

    entities = config["entities"]

    result = {}

    # ==========================================================
    # COMPARACIÓN
    # ==========================================================

    st.subheader("Comparación")

    cols = st.columns(len(entities))

    entity_labels = {

        "player": "Jugador",

        "position": "Posición",

        "week": "Semana",

        "microcycle": "Microciclo",

        "session": "Sesión",

        "team": "Equipo"

    }

    entity_sources = {

        "player": "players",

        "position": "positions",

        "week": "weeks",

        "microcycle": "microcycles",

        "session": "sessions",

        "team": "teams"

    }

    selections = []

    for i, entity in enumerate(entities):

        source = entity_sources.get(entity)

        values = filters.get(source, [])

        label = entity_labels.get(entity, entity.capitalize())

        with cols[i]:

            selection = st.selectbox(

                f"{label} {i+1}" if len(entities) > 1 else label,

                values,

                key=f"{analysis_type}_{entity}_{i}"

            )

        selections.append(

            {

                entity: selection

            }

        )

    result["reference"] = selections[0]

    if len(selections) > 1:

        result["comparison"] = selections[1]

    else:

        result["comparison"] = None

    st.divider()

    # ==========================================================
    # FILTROS GLOBALES
    # ==========================================================

    st.subheader("Filtros")

    col1, col2 = st.columns(2)

    with col1:

        result["start_date"] = st.date_input(

            "Desde",

            value=filters["dates"]["min"],

            key="compare_start"

        )

    with col2:

        result["end_date"] = st.date_input(

            "Hasta",

            value=filters["dates"]["max"],

            key="compare_end"

        )

    col1, col2, col3 = st.columns(3)

    with col1:

        weeks = [

            "Todas"

        ] + filters["weeks"]

        result["week"] = st.selectbox(

            "Semana",

            weeks,

            key="compare_week"

        )

    with col2:

        microcycles = [

            "Todos"

        ] + filters["microcycles"]

        result["microcycle"] = st.selectbox(

            "Microciclo",

            microcycles,

            key="compare_micro"

        )

    with col3:

        sessions = [

            "Todas"

        ] + filters["sessions"]

        result["session"] = st.selectbox(

            "Sesión",

            sessions,

            key="compare_session"

        )

    st.divider()

        # ==========================================================
    # FILTROS CONTEXTUALES
    # ==========================================================

    contextual_cols = []

    if "positions" in filters and filters["positions"]:

        contextual_cols.append(

            (

                "position_filter",

                "Posición",

                ["Todas"] + filters["positions"]

            )

        )

    if "teams" in filters and filters["teams"]:

        contextual_cols.append(

            (

                "team_filter",

                "Equipo",

                ["Todos"] + filters["teams"]

            )

        )

    if contextual_cols:

        st.subheader("Filtros adicionales")

        cols = st.columns(len(contextual_cols))

        for col, (key, label, values) in zip(cols, contextual_cols):

            with col:

                result[key] = st.selectbox(

                    label,

                    values,

                    key=f"compare_{key}"

                )

        st.divider()

    # ==========================================================
    # MÉTRICAS
    # ==========================================================

    st.subheader("Métricas")

    metrics_df = filters["metrics"]

    default_metrics = metrics_df.loc[

        metrics_df["default"],

        "metric"

    ].tolist()

    metric_labels = {

        row.metric: row.label

        for row in metrics_df.itertuples()

    }

    result["metrics"] = st.multiselect(

        "",

        options=metrics_df["metric"].tolist(),

        default=default_metrics,

        format_func=lambda x: metric_labels[x],

        key="compare_metrics"

    )

    # ==========================================================
    # LIMPIEZA
    # ==========================================================

    if result["week"] == "Todas":

        result["week"] = None

    if result["microcycle"] == "Todos":

        result["microcycle"] = None

    if result["session"] == "Todas":

        result["session"] = None

    if "position_filter" in result:

        if result["position_filter"] == "Todas":

            result["position_filter"] = None

    if "team_filter" in result:

        if result["team_filter"] == "Todos":

            result["team_filter"] = None

    if len(result["metrics"]) == 0:

        result["metrics"] = default_metrics

    return result

    # --------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------

    metrics = filters["metrics"]

    defaults = metrics.loc[

        metrics["default"],

        "metric"

    ].tolist()

    result["metrics"] = st.multiselect(

        "Métricas",

        metrics["metric"],

        default=defaults,

        format_func=lambda x: metrics.loc[
            metrics.metric == x,
            "label"
        ].iloc[0]

    )

    return result

import plotly.express as px
import plotly.graph_objects as go


# =============================================================================
# SUMMARY
# =============================================================================

def comparison_summary(
    summary: dict
) -> None:
    """
    Tarjetas resumen de la comparación.
    """

    cards = summary["cards"]

    if not cards:

        st.info(

            "No hay métricas disponibles."

        )

        return

    CARDS_PER_ROW = 4

    for start in range(0, len(cards), CARDS_PER_ROW):

        cols = st.columns(CARDS_PER_ROW)

        row_cards = cards[start:start + CARDS_PER_ROW]

        for col, card in zip(cols, row_cards):

            diff = card["difference"]

            if diff > 0:

                delta_color = "normal"

                delta = f"+{diff:{card['format']}} {card['unit']}"

            elif diff < 0:

                delta_color = "inverse"

                delta = f"{diff:{card['format']}} {card['unit']}"

            else:

                delta_color = "off"

                delta = "0"

            with col:

                st.metric(

                    label=card["short"],

                    value=f'{card["reference"]:{card["format"]}} {card["unit"]}',

                    delta=delta,

                    delta_color=delta_color

                )


# =============================================================================
# RADAR
# =============================================================================

def comparison_radar(
    statistics
) -> None:
    """
    Radar comparativo.
    """

    if statistics.empty:

        return

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=statistics["reference_normalized"],

            theta=statistics["short"],

            fill="toself",

            name="Referencia"

        )

    )

    fig.add_trace(

        go.Scatterpolar(

            r=statistics["comparison_normalized"],

            theta=statistics["short"],

            fill="toself",

            name="Comparación"

        )

    )

    fig.update_layout(

        height=550,

        polar=dict(

            radialaxis=dict(

                visible=True

            )

        ),

        margin=dict(

            l=40,

            r=40,

            t=40,

            b=40

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# =============================================================================
# BARRAS
# =============================================================================

def comparison_bar(
    statistics
) -> None:
    """
    Diferencia entre ambas entidades.
    """

    if statistics.empty:

        return

    fig = px.bar(

        statistics,

        x="short",

        y="difference",

        color="difference",

        text="difference"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}",

        textposition="outside"

    )

    fig.update_layout(

        height=500,

        xaxis_title="",

        yaxis_title="Diferencia",

        showlegend=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# =============================================================================
# EVOLUCIÓN
# =============================================================================

def comparison_line(
    history
) -> None:
    """
    Evolución temporal.
    """

    if history.empty:

        return

    fig = px.line(

        history,

        x="date",

        y="value",

        color="group"

    )

    fig.update_layout(

        height=500,

        xaxis_title="",

        yaxis_title=""

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =============================================================================
# BOXPLOT
# =============================================================================

def comparison_boxplot(
    distribution,
    reference_name: str,
    comparison_name: str
) -> None:
    """
    Posición de ambas entidades respecto
    a la distribución.
    """

    if distribution.empty:

        return

    fig = px.box(

        distribution,

        x="metric",

        y="value",

        color="metric",

        points=False

    )

    reference = distribution[
        distribution["group"] == "reference"
    ]

    comparison = distribution[
        distribution["group"] == "comparison"
    ]

    fig.add_scatter(

        x=reference["metric"],

        y=reference["value"],

        mode="markers",

        marker=dict(

            size=12,

            symbol="diamond"

        ),

        name=reference_name

    )

    fig.add_scatter(

        x=comparison["metric"],

        y=comparison["value"],

        mode="markers",

        marker=dict(

            size=12,

            symbol="x"

        ),

        name=comparison_name

    )

    fig.update_layout(

        height=550,

        showlegend=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# =============================================================================
# DISTRIBUCIÓN
# =============================================================================

def comparison_distribution(
    distribution,
    metric: str
) -> None:
    """
    Distribución de una métrica.
    """

    if distribution.empty:

        return

    data = distribution[

        distribution["metric"] == metric

    ]

    if data.empty:

        st.info(

            "No hay datos disponibles para esta métrica."

        )

        return

    fig = px.histogram(

        data,

        x="value",

        color="group",

        nbins=20,

        barmode="overlay",

        opacity=0.75

    )

    fig.update_layout(

        height=450,

        xaxis_title="",

        yaxis_title="Frecuencia",

        legend_title=""

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# =============================================================================
# TABLA
# =============================================================================

# =============================================================================
# TABLA COMPARATIVA
# =============================================================================

def comparison_table(
    statistics
) -> str | None:
    """
    Tabla comparativa de métricas.

    Devuelve el ID interno de la métrica seleccionada
    (player_load, distance_m, etc.) para que el resto
    de componentes utilicen siempre el mismo identificador.
    """

    if statistics.empty:

        st.info(

            "No hay datos disponibles."

        )

        return None

    # --------------------------------------------------
    # CATEGORÍAS
    # --------------------------------------------------

    categories = [

        "Todas"

    ] + sorted(

        statistics["category"].unique()

    )

    selected_category = st.segmented_control(

        label="",

        options=categories,

        default="Todas",

        key="comparison_table_category"

    )

    table = statistics.copy()

    if selected_category != "Todas":

        table = table[

            table["category"] == selected_category

        ].reset_index(drop=True)

    # --------------------------------------------------
    # Guardamos los IDs reales
    # --------------------------------------------------

    metric_ids = table["metric"].tolist()

    # --------------------------------------------------
    # TABLA
    # --------------------------------------------------

    display = table[

        [

            "label",

            "reference",

            "comparison",

            "difference",

            "difference_pct"

        ]

    ].copy()

    display.columns = [

        "Métrica",

        "Referencia",

        "Comparación",

        "Diferencia",

        "%"

    ]

    event = st.dataframe(

        display,

        hide_index=True,

        use_container_width=True,

        height=420,

        on_select="rerun",

        selection_mode="single-row",

        column_config={

            "Métrica": st.column_config.TextColumn(

                width="medium"

            ),

            "Referencia": st.column_config.NumberColumn(

                format="%.1f"

            ),

            "Comparación": st.column_config.NumberColumn(

                format="%.1f"

            ),

            "Diferencia": st.column_config.NumberColumn(

                format="%+.1f"

            ),

            "%": st.column_config.NumberColumn(

                format="%+.1f %%"

            )

        }

    )

    # --------------------------------------------------
    # FILA SELECCIONADA
    # --------------------------------------------------

    if len(event.selection.rows):

        row = event.selection.rows[0]

        return metric_ids[row]

    # --------------------------------------------------
    # POR DEFECTO
    # --------------------------------------------------

    return metric_ids[0]

# =============================================================================
# INSIGHTS
# =============================================================================

def comparison_insights(
    insights: list
) -> None:
    """
    Muestra los hallazgos automáticos del análisis.
    """

    if not insights:

        return

    st.subheader("Hallazgos")

    for insight in insights:

        if insight["level"] == "success":

            st.success(

                insight["text"]

            )

        elif insight["level"] == "warning":

            st.warning(

                insight["text"]

            )

        else:

            st.info(

                insight["text"]

            )


# =============================================================================
# RENDER VISUALIZACIONES
# =============================================================================

def render_visualizations(
    comparison: dict
) -> None:
    """
    Renderiza automáticamente todas las visualizaciones
    definidas en compare_config.py.
    """

    statistics = comparison["statistics"]

    selected_metric = comparison_table(

        statistics

    )

    if selected_metric is None:

        selected_metric = statistics.iloc[0]["metric"]

    for visualization in comparison["visualizations"]:

        viz_type = visualization["type"]

        if viz_type == "radar":

            comparison_radar(statistics)

        elif viz_type == "bar":

            comparison_bar(statistics)

        elif viz_type == "line":

            pass

        elif viz_type == "distribution":

            comparison_distribution(

                comparison["distribution"],

                selected_metric

            )

        elif viz_type == "boxplot":

            comparison_boxplot(

                comparison["distribution"],

                comparison["header"]["reference_name"],

                comparison["header"]["comparison_name"]

            )

# =============================================================================
# COMPONENTE PRINCIPAL
# =============================================================================

def render_comparison(
    comparison: dict
) -> None:
    """
    Renderiza un análisis completo.
    """

    comparison_header(

        comparison["header"]

    )

    comparison_summary(

        comparison["summary"]

    )

    render_visualizations(

        comparison

    )

    comparison_insights(

        comparison["insights"]

    )