import streamlit as st


def render_recommendation_card(recommendation: dict):
    """
    Muestra la recomendación principal del día.
    """

    with st.container(border=True):

        st.subheader("Recomendación del Día")

        if recommendation is None:

            st.info("No existe ninguna recomendación.")

            return

        title = recommendation.get("titulo", "")

        message = recommendation.get("mensaje", "")

        level = recommendation.get("nivel", "info")

        text = f"### {title}\n\n{message}"

        if level == "success":

            st.success(text)

        elif level == "warning":

            st.warning(text)

        elif level == "error":

            st.error(text)

        else:

            st.info(text)