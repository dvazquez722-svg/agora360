import pandas as pd

import streamlit as st

from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    JsCode
)


# =============================================================================
# RENDERERS
# =============================================================================

STATUS_RENDERER = JsCode("""
function(params){

    let colors={
        "Óptimo":"#16a34a",
        "Bueno":"#65a30d",
        "Aceptable":"#ca8a04",
        "Comprometido":"#ea580c",
        "Crítico":"#dc2626"
    }

    let color=colors[params.value] || "#475569";

    return `
        <span style="
            background:${color};
            color:white;
            padding:5px 12px;
            border-radius:999px;
            font-size:11px;
            font-weight:700;
        ">
        ${params.value}
        </span>
    `
}
""")



# =============================================================================
# TABLE
# =============================================================================

def squad_table(players):

    df=pd.DataFrame(players)

    df=df[
        [
            "player",
            "status",
            "overall_score",
            "risk",
            "availability",
            "action"
        ]
    ]

    df.columns=[
        "Jugador",
        "Estado",
        "Score",
        "Riesgo",
        "Disponibilidad",
        "Acción"
    ]

    df=df.sort_values(
        "Score"
    )

    gb=GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        sortable=True,
        filter=True,
        floatingFilter=True,
        resizable=True
    )

    gb.configure_selection(
        "single",
        use_checkbox=False
    )

    gb.configure_column(
        "Jugador",
        pinned="left",
        width=240
    )

    gb.configure_column(
        "Estado",
        width=150,
        cellRenderer=STATUS_RENDERER
    )

    gb.configure_column(
        "Score",
        width=90
    )

    gb.configure_column(
        "Riesgo",
        width=120
    )

    gb.configure_column(
        "Disponibilidad",
        width=150
    )

    gb.configure_column(
        "Acción",
        width=170
    )

    gb.configure_grid_options(
        rowHeight=46,
        headerHeight=44,
        animateRows=True
    )

    return AgGrid(

        df,

        gridOptions=gb.build(),

        allow_unsafe_jscode=True,

        theme="dark",

        fit_columns_on_grid_load=True,

        update_on=["selectionChanged"],

        height=760

    )