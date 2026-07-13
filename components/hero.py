import streamlit as st


def render_hero(
    status: str,
    icon: str,
    message: str,
):
    """
    Tarjeta principal del estado general.
    """

    if icon == "🟢":
        st.success(f"### {icon} {status}")

    elif icon == "🟡":
        st.warning(f"### {icon} {status}")

    else:
        st.error(f"### {icon} {status}")

    st.write(message)

    st.divider()