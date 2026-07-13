import streamlit as st


def render_executive_summary(summary: str):
    """
    Muestra el resumen ejecutivo de la sesión.
    """

    with st.container(border=True):

        st.subheader("Resumen Ejecutivo")

        if not summary:

            st.info("No hay información disponible.")

            return

        st.markdown(summary)