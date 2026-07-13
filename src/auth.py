"""
auth.py
=======

Sistema de autenticación de Ágora 360.
"""

import streamlit as st


# =============================================================================
# COMPROBAR AUTENTICACIÓN
# =============================================================================

def check_authentication() -> None:
    """
    Impide acceder a cualquier página si el usuario
    no ha iniciado sesión.
    """

    if not st.session_state.get("authenticated", False):

        st.switch_page("Home.py")

        st.stop()


# =============================================================================
# INICIAR SESIÓN
# =============================================================================

def login(username: str, password: str) -> bool:
    """
    Valida las credenciales del usuario.
    """

    # Temporal
    if username == "admin" and password == "agora360":

        st.session_state.authenticated = True

        st.session_state.user = {

            "username": username,

            "role": "Administrador"

        }

        return True

    return False


# =============================================================================
# CERRAR SESIÓN
# =============================================================================

def logout() -> None:

    st.session_state.clear()

    st.switch_page("Home.py")