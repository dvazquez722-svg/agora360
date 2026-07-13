"""
auth.py
=======

Sistema de autenticación de Ágora 360.

Responsabilidades
-----------------
- Inicio de sesión
- Cierre de sesión
- Comprobación de autenticación
- Gestión del usuario activo

Preparado para múltiples clubes y usuarios.
"""

from __future__ import annotations

import streamlit as st


# =============================================================================
# USUARIOS (TEMPORAL)
# =============================================================================

USERS = {

    "admin": {

        "password": "agora360",

        "name": "Administrador",

        "club": "ud_las_palmas",

        "role": "Administrador",

        "active": True

    }

}


# =============================================================================
# OBTENER USUARIO
# =============================================================================

def get_user(username: str) -> dict | None:
    """
    Devuelve la información del usuario.

    En el futuro esta función leerá una base de datos.
    """

    return USERS.get(username)


# =============================================================================
# LOGIN
# =============================================================================

def login(
    username: str,
    password: str
) -> bool:
    """
    Valida las credenciales del usuario.
    """

    user = get_user(username)

    if user is None:

        return False

    if not user["active"]:

        return False

    if password != user["password"]:

        return False

    st.session_state.authenticated = True

    st.session_state.user = {

        "username": username,

        "name": user["name"],

        "club": user["club"],

        "role": user["role"]

    }

    return True


# =============================================================================
# LOGOUT
# =============================================================================

def logout():
    """
    Cierra la sesión actual.
    """

    st.session_state.clear()

    st.switch_page("Home.py")


# =============================================================================
# COMPROBAR AUTENTICACIÓN
# =============================================================================

def check_authentication() -> None:
    """
    Impide acceder a cualquier página si no existe
    una sesión válida.
    """

    if (
        not st.session_state.get("authenticated", False)
        or "user" not in st.session_state
    ):

        st.session_state.clear()

        st.switch_page("Home.py")

        st.stop()


# =============================================================================
# INFORMACIÓN DEL USUARIO
# =============================================================================

def current_user() -> dict:
    """
    Devuelve el usuario autenticado.
    """

    return st.session_state.get("user", {})


def current_club() -> str:
    """
    Devuelve el club activo.
    """

    return current_user().get("club", "")


def current_role() -> str:
    """
    Devuelve el rol del usuario.
    """

    return current_user().get("role", "")


def current_username() -> str:
    """
    Devuelve el nombre de usuario.
    """

    return current_user().get("username", "")


# =============================================================================
# PERMISOS
# =============================================================================

def has_role(role: str) -> bool:
    """
    Comprueba si el usuario tiene un rol.
    """

    return current_role() == role


def is_admin() -> bool:
    """
    Comprueba si el usuario es administrador.
    """

    return has_role("Administrador")