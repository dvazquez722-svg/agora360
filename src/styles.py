"""
styles.py
----------

Sistema de diseño global de Performance Monitor.

Este archivo centraliza toda la apariencia de la aplicación.

Responsabilidades

- Paleta de colores
- Tipografía
- Espaciados
- Radios
- Sombras
- CSS global
- Tema Plotly

No contiene lógica de negocio.
"""

import streamlit as st


# =============================================================================
# PALETA
# =============================================================================

COLORS = {

    # -------------------------------------------------------------------------
    # Marca
    # -------------------------------------------------------------------------

    "primary": "#2563EB",

    "primary_dark": "#1D4ED8",

    "primary_light": "#DBEAFE",

    # -------------------------------------------------------------------------
    # Estados
    # -------------------------------------------------------------------------

    "success": "#16A34A",

    "warning": "#F59E0B",

    "danger": "#DC2626",

    "info": "#0EA5E9",

    # -------------------------------------------------------------------------
    # Fondos
    # -------------------------------------------------------------------------

    "background": "#F8FAFC",

    "surface": "#FFFFFF",

    "card": "#FFFFFF",

    "card_hover": "#F9FAFB",

    # -------------------------------------------------------------------------
    # Bordes
    # -------------------------------------------------------------------------

    "border": "#E5E7EB",

    "border_light": "#F1F5F9",

    # -------------------------------------------------------------------------
    # Texto
    # -------------------------------------------------------------------------

    "text": "#111827",

    "text_secondary": "#4B5563",

    "text_muted": "#9CA3AF"

}


# =============================================================================
# TIPOGRAFÍA
# =============================================================================

FONT = {

    "hero": "54px",

    "title": "34px",

    "subtitle": "24px",

    "header": "20px",

    "body": "15px",

    "small": "13px",

    "caption": "12px"

}


# =============================================================================
# ESPACIADOS
# =============================================================================

SPACE = {

    "xs": "4px",

    "sm": "8px",

    "md": "16px",

    "lg": "24px",

    "xl": "40px",

    "xxl": "64px"

}


# =============================================================================
# RADIOS
# =============================================================================

RADIUS = {

    "xs": "8px",

    "sm": "12px",

    "md": "16px",

    "lg": "22px",

    "xl": "30px"

}


# =============================================================================
# SOMBRAS
# =============================================================================

SHADOW = {

    "card": "0 1px 3px rgba(15,23,42,.06)",

    "hover": "0 10px 24px rgba(15,23,42,.10)",

    "dropdown": "0 10px 30px rgba(15,23,42,.08)"

}


# =============================================================================
# PLOTLY
# =============================================================================

PLOTLY_THEME = {

    "paper_bgcolor": "rgba(0,0,0,0)",

    "plot_bgcolor": "rgba(0,0,0,0)",

    "font_family": "Inter",

    "font_color": COLORS["text"],

    "colorway": [

        COLORS["primary"],

        COLORS["success"],

        COLORS["warning"],

        COLORS["danger"],

        COLORS["info"]

    ]

}

# =============================================================================
# BASE CSS
# =============================================================================

BASE_CSS = f"""
<style>

/* ==========================================================================
FUENTE
========================================================================== */

html,
body,
[class*="css"] {{

    font-family:
        "Inter",
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    color:{COLORS["text"]};

    background:{COLORS["background"]};

    font-size:{FONT["body"]};

}}


/* ==========================================================================
APP
========================================================================== */

.stApp {{

    background:{COLORS["background"]};

}}


/* ==========================================================================
LAYOUT
========================================================================== */

.block-container {{

    max-width:1700px;

    padding-top:2rem;

    padding-bottom:2rem;

    padding-left:3rem;

    padding-right:3rem;

}}


/* ==========================================================================
SIDEBAR
========================================================================== */

section[data-testid="stSidebar"] {{

    background:{COLORS["surface"]};

    border-right:1px solid {COLORS["border"]};

}}

section[data-testid="stSidebar"] > div {{

    padding-top:1rem;

}}


/* ==========================================================================
HEADERS
========================================================================== */

h1 {{

    font-size:{FONT["title"]};

    font-weight:700;

    color:{COLORS["text"]};

    letter-spacing:-0.03em;

    margin-bottom:.25rem;

}}

h2 {{

    font-size:{FONT["subtitle"]};

    font-weight:700;

    color:{COLORS["text"]};

    margin-top:1.5rem;

    margin-bottom:.75rem;

}}

h3 {{

    font-size:{FONT["header"]};

    font-weight:600;

    color:{COLORS["text"]};

}}

p {{

    color:{COLORS["text_secondary"]};

}}

small {{

    color:{COLORS["text_muted"]};

}}


/* ==========================================================================
SEPARADORES
========================================================================== */

hr {{

    border:none;

    border-top:1px solid {COLORS["border"]};

    margin:1.5rem 0;

}}

</style>
"""

# =============================================================================
# COMPONENT CSS
# =============================================================================

COMPONENT_CSS = f"""
<style>

/* ==========================================================================
TARJETAS
========================================================================== */

.card {{

    background:{COLORS["card"]};

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["lg"]};

    padding:24px;

    margin-bottom:20px;

    box-shadow:{SHADOW["card"]};

    transition:all .20s ease;

}}

.card:hover {{

    transform:translateY(-2px);

    border-color:{COLORS["primary_light"]};

    box-shadow:{SHADOW["hover"]};

}}


/* ==========================================================================
KPIs
========================================================================== */

div[data-testid="metric-container"] {{

    background:{COLORS["surface"]};

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["md"]};

    padding:18px;

    box-shadow:{SHADOW["card"]};

}}

div[data-testid="metric-container"]:hover {{

    border-color:{COLORS["primary"]};

    box-shadow:{SHADOW["hover"]};

}}


/* Título */

div[data-testid="metric-container"] label {{

    color:{COLORS["text_secondary"]};

    font-size:13px;

    font-weight:600;

}}


/* Valor */

div[data-testid="metric-container"] [data-testid="stMetricValue"] {{

    color:{COLORS["text"]};

    font-size:30px;

    font-weight:700;

}}


/* Delta */

div[data-testid="metric-container"] [data-testid="stMetricDelta"] {{

    font-weight:600;

}}


/* ==========================================================================
NOTIFICACIONES
========================================================================== */

div[data-baseweb="notification"] {{

    border-radius:{RADIUS["md"]};

    border:1px solid {COLORS["border"]};

    box-shadow:{SHADOW["card"]};

}}


/* ==========================================================================
EXPANDERS
========================================================================== */

details {{

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["md"]};

    background:{COLORS["surface"]};

    overflow:hidden;

}}

summary {{

    padding:16px 18px;

    font-weight:600;

    color:{COLORS["text"]};

}}

details > div {{

    padding:18px;

}}


/* ==========================================================================
CONTAINERS
========================================================================== */

[data-testid="stVerticalBlock"] > div:has(> div[data-testid="metric-container"]) {{

    gap:16px;

}}

</style>
"""

# =============================================================================
# INPUT CSS
# =============================================================================

INPUT_CSS = f"""
<style>

/* ==========================================================================
BOTONES
========================================================================== */

.stButton > button {{

    width:100%;

    height:44px;

    border:none;

    border-radius:{RADIUS["sm"]};

    background:{COLORS["primary"]};

    color:white;

    font-weight:600;

    font-size:14px;

    box-shadow:{SHADOW["card"]};

    transition:all .18s ease;

}}

.stButton > button:hover {{

    background:{COLORS["primary_dark"]};

    transform:translateY(-1px);

    box-shadow:{SHADOW["hover"]};

}}


/* ==========================================================================
SELECTBOX
========================================================================== */

.stSelectbox div[data-baseweb="select"] > div {{

    background:{COLORS["surface"]};

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["sm"]};

    min-height:44px;

}}

.stSelectbox div[data-baseweb="select"] > div:hover {{

    border-color:{COLORS["primary"]};

}}


/* ==========================================================================
MULTISELECT
========================================================================== */

.stMultiSelect div[data-baseweb="select"] > div {{

    background:{COLORS["surface"]};

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["sm"]};

}}

.stMultiSelect div[data-baseweb="select"] > div:hover {{

    border-color:{COLORS["primary"]};

}}


/* ==========================================================================
DATE INPUT
========================================================================== */

.stDateInput > div > div {{

    border-radius:{RADIUS["sm"]};

}}

.stDateInput input {{

    background:{COLORS["surface"]};

}}


/* ==========================================================================
TEXT INPUT
========================================================================== */

.stTextInput input {{

    border-radius:{RADIUS["sm"]};

    border:1px solid {COLORS["border"]};

}}

.stTextInput input:focus {{

    border-color:{COLORS["primary"]};

}}


/* ==========================================================================
NUMBER INPUT
========================================================================== */

.stNumberInput input {{

    border-radius:{RADIUS["sm"]};

    border:1px solid {COLORS["border"]};

}}


/* ==========================================================================
CHECKBOX
========================================================================== */

.stCheckbox {{

    padding-top:6px;

}}


/* ==========================================================================
RADIO
========================================================================== */

.stRadio {{

    padding-top:4px;

}}

</style>
"""

# =============================================================================
# TABLE CSS
# =============================================================================

TABLE_CSS = f"""
<style>

/* ==========================================================================
DATAFRAME
========================================================================== */

div[data-testid="stDataFrame"] {{

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["md"]};

    overflow:hidden;

    box-shadow:{SHADOW["card"]};

}}

div[data-testid="stDataFrame"] table {{

    border-collapse:collapse;

}}

div[data-testid="stDataFrame"] thead tr {{

    background:{COLORS["background"]};

}}

div[data-testid="stDataFrame"] th {{

    font-weight:600;

    color:{COLORS["text"]};

    border-bottom:1px solid {COLORS["border"]};

}}

div[data-testid="stDataFrame"] td {{

    border-bottom:1px solid {COLORS["border_light"]};

}}

div[data-testid="stDataFrame"] tbody tr:hover {{

    background:{COLORS["card_hover"]};

}}


/* ==========================================================================
TABS
========================================================================== */

.stTabs [data-baseweb="tab-list"] {{

    gap:8px;

}}

.stTabs [data-baseweb="tab"] {{

    background:{COLORS["surface"]};

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["sm"]};

    padding:10px 18px;

    font-weight:600;

}}

.stTabs [aria-selected="true"] {{

    background:{COLORS["primary"]};

    color:white;

    border-color:{COLORS["primary"]};

}}


/* ==========================================================================
SCROLLBAR
========================================================================== */

::-webkit-scrollbar {{

    width:8px;

    height:8px;

}}

::-webkit-scrollbar-track {{

    background:{COLORS["background"]};

}}

::-webkit-scrollbar-thumb {{

    background:#CBD5E1;

    border-radius:20px;

}}

::-webkit-scrollbar-thumb:hover {{

    background:#94A3B8;

}}


/* ==========================================================================
PLOTLY
========================================================================== */

.js-plotly-plot {{

    border:1px solid {COLORS["border"]};

    border-radius:{RADIUS["md"]};

    background:{COLORS["surface"]};

    padding:10px;

    box-shadow:{SHADOW["card"]};

}}

</style>
"""

# =============================================================================
# CSS GLOBAL
# =============================================================================

GLOBAL_CSS = (

    BASE_CSS

    + COMPONENT_CSS

    + INPUT_CSS

    + TABLE_CSS

)

# =============================================================================
# PLOTLY
# =============================================================================

def apply_plotly_theme(fig):
    """
    Aplica el tema visual corporativo a una figura Plotly.
    """

    fig.update_layout(

        paper_bgcolor=PLOTLY_THEME["paper_bgcolor"],

        plot_bgcolor=PLOTLY_THEME["plot_bgcolor"],

        font=dict(

            family=PLOTLY_THEME["font_family"],

            color=PLOTLY_THEME["font_color"]

        ),

        colorway=PLOTLY_THEME["colorway"],

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20

        ),

        legend=dict(

            bgcolor="rgba(0,0,0,0)",

            borderwidth=0,

            orientation="h",

            y=1.05,

            x=1,

            xanchor="right"

        ),

        hoverlabel=dict(

            bgcolor=COLORS["surface"],

            bordercolor=COLORS["border"],

            font=dict(

                color=COLORS["text"]

            )

        )

    )

    fig.update_xaxes(

        showgrid=True,

        gridcolor=COLORS["border_light"],

        zeroline=False,

        linecolor=COLORS["border"]

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor=COLORS["border_light"],

        zeroline=False,

        linecolor=COLORS["border"]

    )

    return fig


# =============================================================================
# APLICAR ESTILOS
# =============================================================================

def apply_styles():
    """
    Aplica el sistema de diseño global.
    """

    st.markdown(

        GLOBAL_CSS,

        unsafe_allow_html=True

    )