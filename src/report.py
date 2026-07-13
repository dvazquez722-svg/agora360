"""
report.py
---------

Gestión del informe diario.
"""

from io import BytesIO
from datetime import datetime

import streamlit as st

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


# ==========================================================
# INICIALIZAR
# ==========================================================

def initialize_report():

    if "daily_report" not in st.session_state:

        st.session_state.daily_report = []


# ==========================================================
# AÑADIR COMENTARIO
# ==========================================================

def add_comment(page, comment):

    initialize_report()

    if comment.strip() == "":
        return

    st.session_state.daily_report.append({

        "datetime": datetime.now().strftime("%d/%m/%Y %H:%M"),

        "page": page,

        "user": st.session_state["user"]["username"],

        "comment": comment

    })


# ==========================================================
# LEER
# ==========================================================

def load_comments():

    initialize_report()

    return st.session_state.daily_report


# ==========================================================
# NUEVO INFORME
# ==========================================================

def clear_report():

    st.session_state.daily_report = []


# ==========================================================
# PDF
# ==========================================================

def generate_pdf():

    initialize_report()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]

    title.alignment = TA_CENTER

    story = []

    story.append(

        Paragraph(

            "Ágora 360",

            title

        )

    )

    story.append(

        Paragraph(

            "Informe diario",

            styles["Heading2"]

        )

    )

    story.append(

        Spacer(1,20)

    )

    if len(st.session_state.daily_report) == 0:

        story.append(

            Paragraph(

                "No existen comentarios.",

                styles["BodyText"]

            )

        )

    else:

        for row in st.session_state.daily_report:

            story.append(

                Paragraph(

                    f"<b>{row['datetime']}</b>",

                    styles["BodyText"]

                )

            )

            story.append(

                Paragraph(

                    f"<b>Página:</b> {row['page']}",

                    styles["BodyText"]

                )

            )

            story.append(

                Paragraph(

                    f"<b>Usuario:</b> {row['user']}",

                    styles["BodyText"]

                )

            )

            story.append(

                Paragraph(

                    row["comment"],

                    styles["BodyText"]

                )

            )

            story.append(

                Spacer(1,18)

            )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf