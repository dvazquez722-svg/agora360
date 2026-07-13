import streamlit as st


def render_evidence(
    title: str,
    description: str,
    figure,
):
    """
    Panel de evidencia reutilizable.
    """

    with st.container(border=True):

        st.subheader(title)

        st.caption(description)

        st.plotly_chart(
            figure,
            use_container_width=True
        )