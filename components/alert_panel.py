import streamlit as st


def render_alerts_panel(alerts: list):
    """
    Muestra las alertas activas del equipo.
    """

    with st.container(border=True):

        st.subheader("Alertas Activas")

        if not alerts:

            st.success("No existen alertas activas.")

            return

        for alert in alerts:

            level = alert.get("level", "warning")

            title = alert.get("title", "")

            player = alert.get("player", "")

            message = alert.get("message", "")

            text = f"**{player}** · **{title}**\n\n{message}"

            if level == "success":

                st.success(text)

            elif level == "error":

                st.error(text)

            elif level == "info":

                st.info(text)

            else:

                st.warning(text)