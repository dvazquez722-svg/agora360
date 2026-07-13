import pandas as pd
import plotly.graph_objects as go

from components.plot_theme import apply_plot_theme


# ==========================================================
# GRÁFICO BASE
# ==========================================================

def trend_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    y_label: str,
    color: str = "#2563EB",
):
    """
    Gráfico estándar de evolución.
    """

    data = data.sort_values(x)

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=data[x],

            y=data[y],

            mode="lines+markers",

            line=dict(
                width=3,
                color=color
            ),

            marker=dict(
                size=7
            ),

            hovertemplate="%{y:.2f}<extra></extra>"
        )

    )

    fig.update_layout(

        title=title,

        yaxis_title=y_label

    )

    return apply_plot_theme(fig)


# ==========================================================
# PLAYER LOAD
# ==========================================================

def player_load_chart(df):

    data = (

        df.groupby("date", as_index=False)

        ["player_load_a_u"]

        .mean()

    )

    return trend_chart(

        data=data,

        x="date",

        y="player_load_a_u",

        title="Player Load",

        y_label="AU",

        color="#2563EB"

    )


# ==========================================================
# WELLNESS
# ==========================================================

def wellness_chart(df):

    cols = [

        "wellness_fatige",

        "wellness_sleep",

        "wellness_doms",

        "wellness_stress",

        "wellness_mood"

    ]

    data = (

        df.groupby("date", as_index=False)[cols]

        .mean()

    )

    data["wellness"] = data[cols].mean(axis=1)

    return trend_chart(

        data=data,

        x="date",

        y="wellness",

        title="Wellness",

        y_label="Puntuación",

        color="#10B981"

    )


# ==========================================================
# RPE
# ==========================================================

def rpe_chart(df):

    data = (

        df.groupby("date", as_index=False)

        ["rpe_general"]

        .mean()

    )

    return trend_chart(

        data=data,

        x="date",

        y="rpe_general",

        title="RPE",

        y_label="Escala",

        color="#F59E0B"

    )