import streamlit as st
from datetime import datetime


def render_header(
    title: str,
    subtitle: str,
):
    """
    Cabecera principal de la página.
    """

    fecha = datetime.now().strftime("%d/%m/%Y")

    col1, col2 = st.columns([5, 1])

    with col1:

        st.caption("PERFORMANCE MONITOR")

        st.title(title)

        st.caption(subtitle)

    with col2:

        st.caption("Última actualización")

        st.markdown(f"### {fecha}")

    st.divider()