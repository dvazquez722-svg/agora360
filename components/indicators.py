import streamlit as st

from textwrap import dedent

from styles.theme import (
    SUCCESS,
    WARNING,
    ERROR,
    INFO,
    TEXT,
    TEXT_SECONDARY,
    CARD,
    BORDER,
    RADIUS,
)

def status_badge(status: str):
    """
    Indicador de estado.
    """

    colors = {
        "Óptimo": SUCCESS,
        "Bueno": SUCCESS,
        "Atención": WARNING,
        "Alto": WARNING,
        "Crítico": ERROR,
        "Bajo": ERROR
    }

    color = colors.get(status, INFO)

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:{color};
            color:white;
            padding:6px 16px;
            border-radius:20px;
            font-size:13px;
            font-weight:600;
        ">
            {status}
        </div>
        """,
        unsafe_allow_html=True
    )

def delta_badge(delta):

    if delta > 0:
        color = SUCCESS
        symbol = "▲"

    elif delta < 0:
        color = ERROR
        symbol = "▼"

    else:
        color = INFO
        symbol = "■"

    st.markdown(
        f"""
        <span style="
            color:{color};
            font-weight:700;
            font-size:15px;
        ">
            {symbol} {delta:.1f} %
        </span>
        """,
        unsafe_allow_html=True
    )

def progress_bar(value, maximum):

    pct = min(value / maximum * 100, 100)

    if pct < 60:
        color = SUCCESS

    elif pct < 85:
        color = WARNING

    else:
        color = ERROR

    st.markdown(
        f"""
        <div style="
            width:100%;
            height:10px;
            background:#374151;
            border-radius:10px;
            overflow:hidden;
        ">

            <div style="
                width:{pct:.1f}%;
                height:100%;
                background:{color};
            ">

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

def score_indicator(score, maximum=10):

    progress_bar(score, maximum)

    st.markdown(
        f"""
        <p style="
            color:{TEXT_SECONDARY};
            margin-top:8px;
            margin-bottom:0;
        ">
            {score:.1f} / {maximum}
        </p>
        """,
        unsafe_allow_html=True
    )

def mini_metric(title, value):

    st.markdown(
        dedent(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:{RADIUS};
            padding:15px;
        ">

            <div style="
                color:{TEXT_SECONDARY};
                font-size:13px;
            ">
                {title}
            </div>

            <div style="
                color:{TEXT};
                font-size:24px;
                font-weight:700;
                margin-top:5px;
            ">
                {value}
            </div>

        </div>
        """),
        unsafe_allow_html=True
    )