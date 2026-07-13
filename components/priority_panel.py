import streamlit as st
import pandas as pd


# ==========================================================
# JUGADORES PRIORITARIOS
# ==========================================================

def render_priority_panel(priority_df: pd.DataFrame):
    """
    Muestra los jugadores que requieren
    mayor atención por parte del cuerpo técnico.
    """

    st.subheader("🎯 Jugadores prioritarios")

    if priority_df.empty:

        st.success("No existen jugadores prioritarios.")

        return

    priority_df = priority_df.rename(

        columns={

            "icon": "",

            "player": "Jugador",

            "priority": "Prioridad",

            "risk": "Riesgo",

            "reason": "Motivo principal",

            "action": "Acción recomendada"

        }

    )

    st.dataframe(

        priority_df,

        use_container_width=True,

        hide_index=True

    )