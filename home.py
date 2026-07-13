"""
Home.py
========

Pantalla de acceso de Ágora 360.
"""

import streamlit as st

from src.styles import apply_styles

from src.auth import login

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(

    page_title="Ágora 360",

    page_icon="⚽",

    layout="wide",

    initial_sidebar_state="collapsed"

)

apply_styles()


# =============================================================================
# VARIABLES
# =============================================================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.empty()


# =============================================================================
# CABECERA
# =============================================================================

st.markdown("<br>", unsafe_allow_html=True)

st.title("⚽ Ágora 360")

st.markdown(
    """
### Plataforma inteligente de análisis del rendimiento deportivo
"""
)

st.caption(

    "Monitorización · Comparación · Planificación · Apoyo a la toma de decisiones"

)

st.divider()

# =============================================================================
# ACCESO
# =============================================================================

left, right = st.columns([3, 2], gap="large")

# -------------------------------------------------------------------------
# INFORMACIÓN
# -------------------------------------------------------------------------

with left:

    st.subheader("Una única plataforma para el control del rendimiento")

    st.write(
        """
        Ágora 360 integra toda la información necesaria para el seguimiento
        diario del rendimiento del equipo en un único entorno de trabajo.

        La aplicación permite analizar la carga de entrenamiento, comparar
        jugadores, controlar el riesgo, estudiar el microciclo y apoyar la
        toma de decisiones del cuerpo técnico.
        """
    )

# -------------------------------------------------------------------------
# LOGIN
# -------------------------------------------------------------------------

with right:

    st.subheader("Acceso")

    username = st.text_input(

        "Usuario",

        placeholder="Introduzca su usuario"

    )

    password = st.text_input(

        "Contraseña",

        type="password",

        placeholder="Introduzca su contraseña"

    )

    login_button = st.button(

        "Acceder",

        use_container_width=True

    )

    if login_button:

        if login(username, password):

            st.switch_page("pages/1_Estado General.py")

        else:

            st.error("Usuario o contraseña incorrectos.")

# =============================================================================
# MÓDULOS
# =============================================================================

st.divider()

st.subheader("Módulos de Ágora 360")

st.caption(
    "Seleccione el área de trabajo que desea consultar."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    st.container(border=True)

    st.markdown("## 📊 Estado General")

    st.write(
        "Visualización ejecutiva del estado diario del equipo y apoyo a la toma de decisiones."
    )

    st.container(border=True)

    st.markdown("## 📈 Comparativas")

    st.write(
        "Comparación entre jugadores, posiciones, sesiones y periodos de entrenamiento."
    )

    st.container(border=True)

    st.markdown("## 🚨 Riesgo")

    st.write(
        "Control de la carga, indicadores de riesgo y seguimiento preventivo."
    )

with col2:

    st.container(border=True)

    st.markdown("## 👥 Plantilla")

    st.write(
        "Análisis individual de cada jugador y evolución de su rendimiento."
    )

    st.container(border=True)

    st.markdown("## 📅 Microciclo")

    st.write(
        "Seguimiento de la planificación semanal y análisis de las sesiones."
    )

# =============================================================================
# INFORMACIÓN
# =============================================================================

st.divider()

col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("Ágora 360")

    st.write(
        """
        Ágora 360 es una plataforma diseñada para centralizar el análisis del
        rendimiento deportivo mediante datos GPS, facilitando el seguimiento
        diario del equipo y apoyando la toma de decisiones del cuerpo técnico.

        Toda la información se organiza en módulos especializados para ofrecer
        una visión clara, estructurada y objetiva del rendimiento individual y colectivo.
        """
    )

with col2:

    st.metric(

        "Versión",

        "1.0"

    )

    st.metric(

        "Estado",

        "Operativo"

    )

    st.metric(

        "Idioma",

        "Español"

    )

# =============================================================================
# PIE
# =============================================================================

st.divider()

st.caption(
    "© Ágora 360 · Plataforma de análisis del rendimiento deportivo"
)