import plotly.graph_objects as go


def apply_plot_theme(fig: go.Figure) -> go.Figure:
    """
    Aplica el tema gráfico global del software.
    """

    fig.update_layout(

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            family="Inter",
            size=13,
            color="#111827"
        ),

        title=dict(
            x=0,
            xanchor="left",
            font=dict(
                size=20
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        hovermode="x unified",

        showlegend=False,

        height=340

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

        showline=False

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#E5E7EB",

        zeroline=False,

        showline=False

    )

    return fig