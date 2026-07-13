import streamlit as st


def render_kpi_card(
    title: str,
    value,
    description: str = "",
):
    """
    Tarjeta KPI estándar.
    """

    with st.container(border=True):

        st.metric(
            label=title,
            value=value,
        )

        if description:
            st.caption(description)