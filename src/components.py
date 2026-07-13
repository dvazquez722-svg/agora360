"""
components.py
-------------
Componentes visuales reutilizables de la aplicación.

Responsabilidades
-----------------
- Header
- Títulos
- Tarjetas
- KPIs
- Alertas
- Recomendaciones
- Decisión del día

No contiene lógica deportiva.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.styles import COLORS

def section_title(
    title: str,
    subtitle: str | None = None
):
    """
    Título de sección.
    """

    st.markdown(f"## {title}")

    if subtitle:
        st.caption(subtitle)

def divider():
    """
    Separador horizontal.
    """

    st.divider()

def spacer(height: int = 1):
    """
    Inserta espacio vertical.
    """

    for _ in range(height):
        st.write("")

def badge(
    text: str,
    color: str = COLORS["primary"]
):
    """
    Badge de información.
    """

    st.markdown(
        f"""
        <span style="
            background:{color};
            color:white;
            padding:4px 10px;
            border-radius:20px;
            font-size:12px;
            font-weight:600;
        ">
            {text}
        </span>
        """,
        unsafe_allow_html=True
    )

def status_dot(
    color: str,
    label: str
):
    """
    Punto de estado.
    """

    st.markdown(
        f"""
        <span style="color:{color};font-size:18px;">●</span>
        <span>{label}</span>
        """,
        unsafe_allow_html=True
    )

def card(
    title: str,
    body: str
):
    """
    Tarjeta genérica.
    """

    st.markdown(
        f"""
        <div class="card">

        <h4>{title}</h4>

        <p>{body}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

def metric_card(
    title: str,
    value: str,
    description: str,
    color: str
):
    """
    Tarjeta KPI.
    """

    st.markdown(
        f"""
<div class="card">

<div style="display:flex;justify-content:space-between;align-items:center;">

<div style="
font-size:12px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
color:#94A3B8;
">

{title}

</div>

<div style="
width:10px;
height:10px;
border-radius:50%;
background:{color};
">

</div>

</div>

<div style="
font-size:46px;
font-weight:800;
color:{color};
margin-top:14px;
line-height:1;
">

{value}

</div>

<hr style="
margin:16px 0;
border:none;
border-top:1px solid #273449;
">

<div style="
font-size:13px;
line-height:1.45;
color:#CBD5E1;
min-height:40px;
">

{description}

</div>

</div>
""",
        unsafe_allow_html=True
    )


def metric_row(metrics: list[dict]):
    """
    Muestra una fila de tarjetas KPI.

    Cada elemento debe contener:
    - title
    - value
    - description
    - color
    """

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            metric_card(
                title=metric["title"],
                value=metric["value"],
                description=metric["description"],
                color=metric["color"]
            )

def two_columns(
    left_ratio: int = 2,
    right_ratio: int = 1
):
    """
    Devuelve dos columnas con proporciones personalizadas.
    """

    return st.columns([left_ratio, right_ratio])

def three_columns():

    """
    Devuelve tres columnas iguales.
    """

    return st.columns(3)

def four_columns():

    """
    Devuelve cuatro columnas iguales.
    """

    return st.columns(4)

def info_box(
    title: str,
    text: str
):

    st.markdown(
        f"""
<div class="card">

### {title}

{text}

</div>
""",
        unsafe_allow_html=True
    )

def colored_box(
    title: str,
    text: str,
    color: str
):
    """
    Caja informativa corporativa.
    """

    st.markdown(
        f"""
<div style="
background:#FFFFFF;
border:1px solid #E5E7EB;
border-left:6px solid {color};
border-radius:16px;
padding:22px;
margin-bottom:18px;
box-shadow:0 1px 3px rgba(15,23,42,.06);
">

<div style="
font-size:18px;
font-weight:700;
color:#111827;
margin-bottom:12px;
">

{title}

</div>

<div style="
font-size:15px;
line-height:1.7;
color:#4B5563;
">

{text}

</div>

</div>
""",
        unsafe_allow_html=True
    )
def alert_card(
    title: str,
    text: str,
    color: str
):
    """
    Tarjeta compacta para alertas.
    """

    st.markdown(
        f"""
<div class="card">

<div style="
display:flex;
align-items:center;
gap:10px;
margin-bottom:8px;
">

<div style="
width:10px;
height:10px;
border-radius:50%;
background:{color};
">
</div>

<div style="
font-size:15px;
font-weight:700;
color:white;
">

{title}

</div>

</div>

<div style="
font-size:12px;
line-height:1.35;
color:#CBD5E1;
">

{text}

</div>

</div>
""",
        unsafe_allow_html=True
    )

def player_card(
    player: str,
    subtitle: str,
    risk: str,
    color: str
):
    """
    Tarjeta compacta de jugador prioritario.
    """

    st.markdown(
        f"""
<div class="card">

<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">

<div style="font-size:18px;font-weight:700;color:white;">

{player}

</div>

<div style="width:10px;height:10px;border-radius:50%;background:{color};"></div>

</div>

<div style="font-size:13px;color:#CBD5E1;line-height:1.35;margin-bottom:10px;">

{subtitle}

</div>

<div>

<span style="
background:{color};
color:white;
padding:4px 10px;
border-radius:20px;
font-size:11px;
font-weight:700;
text-transform:uppercase;
">

{risk.upper()}

</span>

</div>

</div>
""",
        unsafe_allow_html=True
    )

def priority_players_table(players: list):
    """
    Tabla compacta de jugadores prioritarios para la portada.
    """

    section_title(
        "Jugadores prioritarios",
        "Mayor atención requerida hoy"
    )

    if len(players) == 0:

        st.success("No existen jugadores prioritarios.")

        return

    st.markdown(
        """
<div class="card">
""",
        unsafe_allow_html=True
    )

    header = st.columns([0.7, 2.8, 1.2, 2.3])

    header[0].markdown("**●**")
    header[1].markdown("**Jugador**")
    header[2].markdown("**Riesgo**")
    header[3].markdown("**Motivo**")

    st.divider()

    for player in players:

        cols = st.columns([0.7, 2.8, 1.2, 2.3])

        cols[0].markdown(
            f"<span style='color:{player['color']};font-size:18px;'>●</span>",
            unsafe_allow_html=True
        )

        cols[1].write(player["player"])

        cols[2].write(player["risk"])

        cols[3].write(player["reason"])

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

def progress_bar(
    value: float,
    color: str
):
    """
    Barra de progreso personalizada.

    value entre 0 y 100.
    """

    value = max(0, min(100, value))

    st.markdown(
        f"""
<div
style="
background:#243244;
border-radius:20px;
height:12px;
overflow:hidden;
">

<div
style="
width:{value}%;
height:12px;
background:{color};
">

</div>

</div>
""",
        unsafe_allow_html=True
    )

def page_header(
    title: str,
    subtitle: str | None = None,
    badge_text: str | None = None
):
    """
    Cabecera principal de la página.
    """

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown(f"# {title}")

        if subtitle:
            st.caption(subtitle)

    with col2:

        if badge_text:
            badge(badge_text)

    spacer()

def team_state_card(data: dict):
    """
    Estado general del equipo.
    """

    section_title(
        "Estado general",
        "Resumen automático del estado colectivo"
    )

    st.markdown(
        f"""
<div class="card">

<div style="
font-size:13px;
font-weight:700;
text-transform:uppercase;
letter-spacing:1px;
color:#94A3B8;
">

Estado actual

</div>

<div style="
font-size:36px;
font-weight:800;
color:{data["color"]};
margin-top:10px;
line-height:1;
">

{data["label"]}

</div>

<div style="
margin-top:14px;
font-size:14px;
line-height:1.5;
color:#CBD5E1;
">

{data["description"]}

</div>

</div>
""",
        unsafe_allow_html=True
    )

    progress_bar(
        value=data["value"],
        color=data["color"]
    )

    st.caption(
        f"Índice global del equipo: {round(data['value'])}/100"
    )


def priority_players_panel(players: list):
    """
    Lista de jugadores prioritarios.
    """

    section_title(
        "Jugadores prioritarios",
        "Requieren atención del cuerpo técnico"
    )

    if len(players) == 0:

        st.success("No existen jugadores prioritarios.")

        return

    for player in players:

        player_card(

            player=player["player"],

            subtitle=player["reason"],

            risk=player["risk"],

            color=player["color"]

)
def alerts_panel(alerts: list):
    """
    Alertas del equipo.
    """

    section_title(
        "Alertas",
        "Eventos que requieren seguimiento"
    )

    if len(alerts) == 0:

        st.success("No existen alertas relevantes.")

        return

    cols = st.columns(len(alerts))

    for col, alert in zip(cols, alerts):

        with col:

            alert_card(

                title=alert["title"],

                text=alert["description"],

                color=alert["color"]

)

def recommendation_panel(data: dict):
    """
    Recomendación automática.
    """

    section_title(
        "Recomendación automática"
    )

    colored_box(

        title=data["title"],

        text=data["text"],

        color=data["color"]

    )

def decision_panel(data: dict):
    """
    Decisión final del día.
    """

    spacer()

    st.markdown("---")

    colored_box(

        title="Decisión del día",

        text=data["decision"],

        color=data["color"]

    )

def hero_metric(
    title: str,
    value: str,
    subtitle: str
):

    st.markdown(f"""
<div class="card">

<div
style="
font-size:16px;
color:#94A3B8;
">

{title}

</div>

<div
style="
font-size:52px;
font-weight:700;
margin-top:10px;
">

{value}

</div>

<div
style="
margin-top:10px;
">

{subtitle}

</div>

</div>
""", unsafe_allow_html=True)
    
# =============================================================================
# CONTENEDOR PRINCIPAL
# =============================================================================

def page_container():
    """
    Añade separación superior para mantener una estructura uniforme
    en todas las páginas.
    """
    spacer()


# =============================================================================
# ESTADOS GENERALES
# =============================================================================

def empty_state(
    title: str,
    message: str
):
    """
    Muestra un estado vacío.
    """

    st.markdown(
        f"""
        <div class="card" style="text-align:center;padding:40px;">

            <h3>{title}</h3>

            <p>{message}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


def loading(text: str = "Cargando..."):
    """
    Spinner de carga.
    """

    with st.spinner(text):
        st.write("")


def success_box(text: str):
    """
    Caja de éxito.
    """

    colored_box(
        title="Correcto",
        text=text,
        color=COLORS["success"]
    )


def warning_box(text: str):
    """
    Caja de advertencia.
    """

    colored_box(
        title="Atención",
        text=text,
        color=COLORS["warning"]
    )


def error_box(text: str):
    """
    Caja de error.
    """

    colored_box(
        title="Alerta",
        text=text,
        color=COLORS["danger"]
    )


# =============================================================================
# GRID DE KPIs
# =============================================================================

def kpi_grid(metrics: list[dict]):
    """
    Dibuja automáticamente una cuadrícula de KPIs.

    Cada elemento debe contener:

    title
    value
    description
    color
    """

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            metric_card(

                title=metric["title"],

                value=metric["value"],

                description=metric["description"],

                color=metric["color"]

            )


# =============================================================================
# LISTA DE JUGADORES
# =============================================================================

def player_list(players: list):
    """
    Lista completa de jugadores.
    """

    if len(players) == 0:

        empty_state(
            "Sin jugadores",
            "No existen jugadores para mostrar."
        )

        return

    for player in players:

        player_card(

            player=player["player"],

            subtitle=player["subtitle"],

            risk=player["risk"],

            color=player["color"]

)


# =============================================================================
# FOOTER
# =============================================================================

def footer():

    spacer(2)

    st.markdown("---")

    st.caption(
        "Performance Monitor · Versión 1.0"
    )

# =============================================================================
# BADGE
# =============================================================================

def colored_badge(
    text: str,
    color: str
):
    """
    Badge reutilizable.
    """

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:{color};
            color:white;
            padding:4px 12px;
            border-radius:999px;
            font-size:12px;
            font-weight:700;
            text-align:center;
            min-width:95px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# SCORE BAR
# =============================================================================

def score_bar(score: float):

    score = max(0, min(100, score))

    st.progress(score / 100)

    st.caption(f"Score: {score:.1f}/100")


# =============================================================================
# PLAYER ROW
# =============================================================================

def player_row(player: dict):
    """
    Fila horizontal de un jugador.
    """

    status_colors = {
        "Óptimo": "#22C55E",
        "Bueno": "#84CC16",
        "Aceptable": "#EAB308",
        "Comprometido": "#F97316",
        "Crítico": "#EF4444"
    }

    risk_colors = {
        "Bajo": "#22C55E",
        "Moderado": "#EAB308",
        "Alto": "#F97316",
        "Muy Alto": "#EF4444"
    }

    availability_colors = {
        "Disponible": "#22C55E",
        "Control": "#EAB308",
        "Adaptado": "#F97316",
        "No disponible": "#EF4444"
    }

    action_colors = {
        "Aumentar": "#22C55E",
        "Mantener": "#3B82F6",
        "Control": "#EAB308",
        "Reducir": "#F97316",
        "Recuperación": "#EF4444"
    }

    st.markdown(
        """
        <div class="card" style="padding:18px;">
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:

        st.markdown(
            f"### {player['player']}"
        )

        score_bar(player["overall_score"])

    with col2:

        st.caption("Estado")

        colored_badge(
            player["status"],
            status_colors.get(
                player["status"],
                "#475569"
            )
        )

        st.write("")

        st.caption("Riesgo")

        colored_badge(
            player["risk"],
            risk_colors.get(
                player["risk"],
                "#475569"
            )
        )

    with col3:

        st.caption("Disponibilidad")

        colored_badge(
            player["decision"]["availability"],
            availability_colors.get(
                player["decision"]["availability"],
                "#475569"
            )
        )

        st.write("")

        st.caption("Acción")

        colored_badge(
            player["action"],
            action_colors.get(
                player["action"],
                "#475569"
            )
        )

    st.write("")

    _, _, right = st.columns([5, 1, 2])

    with right:

        if st.button(
            "👤 Ver perfil",
            key=f"profile_{player['player']}",
            use_container_width=True
        ):
            st.session_state["selected_player"] = player["player"]
            st.switch_page("pages/4_Perfil_Individual.py")

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =============================================================================
# SQUAD TABLE
# =============================================================================

def squad_table(
    players: list,
    title: str = "Plantilla"
):

    st.subheader(title)

    st.write("")

    if len(players) == 0:
        st.info("No existen jugadores.")
        return

    # ==========================================================
    # FILTROS
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        search = st.text_input(
            "Buscar jugador",
            placeholder="Nombre..."
        )

    with c2:

        estado = st.selectbox(
            "Estado",
            ["Todos"] + sorted(
                list(
                    {
                        p["status"]
                        for p in players
                    }
                )
            )
        )

    with c3:

        riesgo = st.selectbox(
            "Riesgo",
            ["Todos"] + sorted(
                list(
                    {
                        p["risk"]
                        for p in players
                    }
                )
            )
        )

    with c4:

        disponibilidad = st.selectbox(
            "Disponibilidad",
            ["Todos"] + sorted(
                list(
                    {
                        p["decision"]["availability"]
                        for p in players
                    }
                )
            )
        )

    st.write("")

    # ==========================================================
    # FILTRADO
    # ==========================================================

    filtered = players.copy()

    if search:

        filtered = [

            p

            for p in filtered

            if search.lower() in p["player"].lower()

        ]

    if estado != "Todos":

        filtered = [

            p

            for p in filtered

            if p["status"] == estado

        ]

    if riesgo != "Todos":

        filtered = [

            p

            for p in filtered

            if p["risk"] == riesgo

        ]

    if disponibilidad != "Todos":

        filtered = [

            p

            for p in filtered

            if p["availability"] == disponibilidad

        ]

    # ==========================================================
    # RESUMEN
    # ==========================================================

    st.caption(
        f"Mostrando {len(filtered)} de {len(players)} jugadores"
    )

    st.write("")

    # ==========================================================
    # JUGADORES
    # ==========================================================

    for player in filtered:

        player_row(player)

        st.write("")

# =============================================================================
# PLAYER HEADER
# =============================================================================

def player_header(player: dict):
    """
    Cabecera principal del perfil del jugador.
    """

    st.markdown(f"# {player['player']}")

    st.caption(player["position"])

    score_bar(player["overall_score"])

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    status_colors = {
        "Óptimo": "#22C55E",
        "Bueno": "#84CC16",
        "Aceptable": "#EAB308",
        "Comprometido": "#F97316",
        "Crítico": "#EF4444"
    }

    risk_colors = {
        "Bajo": "#22C55E",
        "Moderado": "#EAB308",
        "Alto": "#F97316",
        "Muy Alto": "#EF4444"
    }

    availability_colors = {
        "Disponible": "#22C55E",
        "Control": "#EAB308",
        "Adaptado": "#F97316",
        "No disponible": "#EF4444"
    }

    action_colors = {
        "Aumentar": "#22C55E",
        "Mantener": "#3B82F6",
        "Control": "#EAB308",
        "Reducir": "#F97316",
        "Recuperación": "#EF4444"
    }

    with c1:
        st.caption("Estado")
        colored_badge(
            player["status"],
            status_colors.get(player["status"], "#475569")
        )

    with c2:
        st.caption("Riesgo")
        colored_badge(
            player["risk"],
            risk_colors.get(player["risk"], "#475569")
        )

    with c3:
        st.caption("Disponibilidad")
        colored_badge(
            player["decision"]["availability"],
            availability_colors.get(player["decision"]["availability"], "#475569")
        )

    with c4:
        st.caption("Acción")
        colored_badge(
            player["decision"]["action"],
            action_colors.get(player["decision"]["action"], "#475569")
        )

# =============================================================================
# PLAYER REPORT
# =============================================================================

def player_report(player: dict):
    """
    Informe automático del jugador.
    """

    st.subheader("Resumen automático")

    st.info(player["report"])


# =============================================================================
# PLAYER REPORT CARD
# =============================================================================

def player_report_card(report: dict, player: dict):
    """
    Tarjeta principal del informe del jugador.
    """

    priority_colors = {
        "Normal": "#16A34A",
        "Media": "#CA8A04",
        "Alta": "#EA580C"
    }

    priority_icons = {
        "Normal": "🟢",
        "Media": "🟡",
        "Alta": "🔴"
    }

    color = priority_colors.get(report["priority"], "#3B82F6")
    icon = priority_icons.get(report["priority"], "🔵")

    progress = {
        "Normal": 30,
        "Media": 65,
        "Alta": 100
    }

    with st.container(border=True):

        # =====================================================
        # CABECERA
        # =====================================================

        c1, c2 = st.columns([5,1])

        with c1:

            st.markdown(
                f"""
                <h2 style="margin-bottom:0;color:{color};">
                {icon} {report["title"]}
                </h2>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.metric(
                "Prioridad",
                report["priority"]
            )

        st.divider()

        # =====================================================
        # RESUMEN
        # =====================================================

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Estado",
                player["status"]
            )

        with c2:
            st.metric(
                "Riesgo",
                player["risk"]
            )

        with c3:
            st.metric(
                "Disponibilidad",
                player["decision"]["availability"]
            )

        st.divider()

        # =====================================================
        # INFORME
        # =====================================================

        st.markdown("#### 📋 Informe automático")

        st.write(report["summary"])

        st.divider()

        # =====================================================
        # PRINCIPAL INDICADOR
        # =====================================================

        st.markdown("#### 🎯 Principal indicador")

        st.info(player["reason"])

        st.divider()

        # =====================================================
        # RECOMENDACIÓN
        # =====================================================

        st.markdown("#### 💡 Decisión recomendada")

        st.success(report["recommendation"])

        st.divider()

        # =====================================================
        # NIVEL DE ATENCIÓN
        # =====================================================

        st.markdown("#### ⚠ Nivel de atención")

        st.progress(progress[report["priority"]] / 100)

        st.caption(
            f"Prioridad actual: {report['priority']}"
        )


# =============================================================================
# METRIC DETAIL CARD
# =============================================================================

def metric_detail_card(title: str, metric: dict):

    colors = {
        "Óptimo": "🟢",
        "Bueno": "🟢",
        "Aceptable": "🟡",
        "Riesgo": "🟠",
        "Crítico": "🔴"
    }

    with st.container(border=True):

        st.markdown(f"### {title}")

        st.metric(
            "Score",
            f"{metric['score']:.1f}"
        )

        st.markdown(
            f"**Estado:** {colors.get(metric['status'], '⚪')} **{metric['status']}**"
        )       

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**ACWR**")
            st.write(f"{metric['summary']['acwr']:.2f}")

        with c2:
            st.markdown("**EWMA**")
            st.write(f"{metric['summary']['ewma']:.2f}")

        with c3:
            st.markdown("**Z-Score**")
            st.write(f"{metric['summary']['z_score']:.2f}")


def player_kpis(player: dict):

    st.subheader("📊 Estado de las métricas")

    names = {

        "player_load":"Player Load",
        "distance_m":"Distancia",
        "high_speed_distance":"HSR",
        "very_high_speed_distance":"VHSR",
        "hmld_m":"HMLD",
        "mechanical_actions":"Acciones Mec."

    }

    metrics = player["metrics"]

    keys = list(metrics.keys())

    for i in range(0, len(keys), 2):

        c1, c2 = st.columns(2)

        with c1:

            metric_detail_card(
                names[keys[i]],
                metrics[keys[i]]
            )

        if i + 1 < len(keys):

            with c2:

                metric_detail_card(
                    names[keys[i+1]],
                    metrics[keys[i+1]]
                )

# =============================================================================
# METRIC ANALYSIS PANEL
# =============================================================================

def metric_analysis_panel(
    workload: dict,
    interpretation: dict
):
    """
    Panel completo de análisis de una métrica.
    """

    if not workload:
        return

    stats = workload["stats"]
    trend = workload["trend"]
    team = workload["team"]
    position = workload["position"]

    with st.container(border=True):

        st.subheader(f"📈 {interpretation['title']}")

        # =====================================================
        # KPIs
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Actual",
            f"{stats['current']:.1f}"
        )

        c2.metric(
            "Media",
            f"{stats['mean']:.1f}"
        )

        c3.metric(
            "Máximo",
            f"{stats['maximum']:.1f}"
        )

        c4.metric(
            "Percentil",
            f"{team.get('percentile', 0):.0f}"
        )

        st.divider()

        # =====================================================
        # COMPARACIÓN
        # =====================================================

        st.markdown("#### Comparación")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Jugador",
            f"{team.get('player_mean', 0):.1f}"
        )

        c2.metric(
            "Equipo",
            f"{team.get('team_mean', 0):.1f}"
        )

        c3.metric(
            "Posición",
            f"{position.get('position_mean', 0):.1f}"
        )

        st.divider()

        # =====================================================
        # TENDENCIA
        # =====================================================

        c1, c2 = st.columns([1, 4])

        c1.metric(
            "Cambio",
            f"{trend['variation']:.1f}%"
        )

        c2.write(
            interpretation["trend"]
        )

        st.divider()

        # =====================================================
        # INTERPRETACIÓN
        # =====================================================

        st.markdown("#### Interpretación")

        st.info(
            interpretation["comparison"]
        )

        st.write(
            interpretation["position"]
        )

        st.write(
            interpretation["percentile"]
        )

        st.divider()

        # =====================================================
        # RECOMENDACIÓN
        # =====================================================

        st.success(
            interpretation["recommendation"]
        )

        st.divider()

        # ==========================================================
        # EVOLUCIÓN
        # ==========================================================

        st.markdown("#### 📈 Evolución")

        chart = (

            workload["player_series"]

            .merge(

                workload["team_series"],

                on="date",

                how="left"

            )

            .merge(

                workload["position_series"],

                on="date",

                how="left"

            )

            .sort_values("date")

            .set_index("date")

        )

        chart.columns = [

            "Jugador",

            "Media equipo",

            "Media posición"

        ]

        st.line_chart(
            chart,
            height=350
        )       

# =============================================================================
# RISK TABLE
# =============================================================================

def risk_table(players):

    st.subheader("🚨 Prioridad de intervención")

    rows = []

    for p in players:

        rows.append({

            "Jugador": p["player"],

            "Posición": p["position"],

            "Score": round(p["overall_score"], 1),

            "Riesgo": p["risk"],

            "Prioridad": "Sí" if p["decision"]["priority"] else "No",

            "Acción": p["decision"]["action"]

        })

    st.dataframe(

        rows,

        use_container_width=True,

        hide_index=True

    )

# =============================================================================
# RISK KPIs
# =============================================================================

def risk_kpis(summary: dict):
    """
    Resumen global del estado de riesgo de la plantilla.
    """

    players = summary["players"]

    if len(players) == 0:

        st.warning("No hay jugadores disponibles.")

        return

    very_high = sum(p["risk"] == "Muy Alto" for p in players)
    high = sum(p["risk"] == "Alto" for p in players)
    moderate = sum(p["risk"] == "Moderado" for p in players)
    low = sum(p["risk"] == "Bajo" for p in players)

    mean_score = round(
        sum(p["overall_score"] for p in players) / len(players),
        1
    )

    risk_players = very_high + high

    risk_percent = round(
        risk_players / len(players) * 100,
        1
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "🔴 Muy Alto",
        very_high
    )

    c2.metric(
        "🟠 Alto",
        high
    )

    c3.metric(
        "🟡 Moderado",
        moderate
    )

    c4.metric(
        "🟢 Bajo",
        low
    )

    c5.metric(
        "⚠ En riesgo",
        f"{risk_percent:.0f}%"
    )

    c6.metric(
        "📊 Score medio",
        f"{mean_score:.1f}"
    )

    st.divider()

# =============================================================================
# RISK SCATTER
# =============================================================================

import pandas as pd
import plotly.graph_objects as go


def risk_scatter(summary, selected_player=None):
    """
    Mapa de decisión Riesgo vs Estado.
    """

    players = summary["players"]

    risk_map = {
        "Bajo": 1,
        "Moderado": 2,
        "Alto": 3,
        "Muy Alto": 4
    }

    plot_df = pd.DataFrame({

        "Jugador": [p["player"] for p in players],

        "Score": [p["overall_score"] for p in players],

        "Riesgo": [risk_map[p["risk"]] for p in players],

        "Estado": [p["status"] for p in players],

        "Acción": [p["decision"]["action"] for p in players]

    })

    fig = go.Figure()

    # ==========================================================
    # CUADRANTES
    # ==========================================================

    fig.add_vrect(
        x0=0,
        x1=70,
        fillcolor="rgba(239,68,68,0.08)",
        line_width=0
    )

    fig.add_vrect(
        x0=70,
        x1=100,
        fillcolor="rgba(34,197,94,0.05)",
        line_width=0
    )

    fig.add_hrect(
        y0=2.5,
        y1=4.5,
        fillcolor="rgba(239,68,68,0.08)",
        line_width=0
    )

    # ==========================================================
    # JUGADORES
    # ==========================================================

    fig.add_trace(

        go.Scatter(

            x=plot_df["Score"],

            y=plot_df["Riesgo"],

            mode="markers",

            marker=dict(

                size=16,

                color=plot_df["Score"],

                colorscale="RdYlGn",

                reversescale=False,

                cmin=0,

                cmax=100,

                line=dict(
                    color="white",
                    width=1
                )

            ),

            customdata=plot_df[

                ["Jugador", "Estado", "Acción"]

            ],

            hovertemplate=

            "<b>%{customdata[0]}</b><br>" +

            "Estado: %{customdata[1]}<br>" +

            "Acción: %{customdata[2]}<br>" +

            "Score: %{x:.1f}<extra></extra>"

        )

    )

    # ==========================================================
    # JUGADOR SELECCIONADO
    # ==========================================================

    if selected_player is not None:

        selected = plot_df[
            plot_df["Jugador"] == selected_player
        ]

        if not selected.empty:

            fig.add_trace(

                go.Scatter(

                    x=selected["Score"],

                    y=selected["Riesgo"],

                    mode="markers+text",

                    text=["⬇"],

                    textposition="top center",

                    marker=dict(

                        size=28,

                        color="white",

                        line=dict(

                            color="#EF4444",

                            width=4

                        )

                    ),

                    hoverinfo="skip",

                    showlegend=False

                )

            )

    # ==========================================================
    # LÍNEAS
    # ==========================================================

    fig.add_vline(
        x=70,
        line_dash="dash"
    )

    fig.add_hline(
        y=2.5,
        line_dash="dash"
    )

    # ==========================================================
    # CUADRANTES
    # ==========================================================

    fig.add_annotation(
        x=35,
        y=4.25,
        text="🔴 Riesgo alto",
        showarrow=False
    )

    fig.add_annotation(
        x=85,
        y=4.25,
        text="🟠 Buena forma<br>pero riesgo",
        showarrow=False
    )

    fig.add_annotation(
        x=35,
        y=1,
        text="🟡 Baja forma",
        showarrow=False
    )

    fig.add_annotation(
        x=85,
        y=1,
        text="🟢 Estado óptimo",
        showarrow=False
    )

    # ==========================================================
    # LAYOUT
    # ==========================================================

    fig.update_layout(

        title="Mapa de decisión",

        height=600,

        showlegend=False,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis=dict(

            title="Estado físico",

            range=[0, 100]

        ),

        yaxis=dict(

            title="Nivel de riesgo",

            range=[0.5, 4.5],

            tickvals=[1, 2, 3, 4],

            ticktext=[
                "Bajo",
                "Moderado",
                "Alto",
                "Muy Alto"
            ]

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()
# =============================================================================
# RISK FACTOR BARS
# =============================================================================

import pandas as pd
import plotly.express as px
import streamlit as st


def risk_factor_bars(player):
    """
    Factores que más influyen en el riesgo del jugador.
    """

    metrics = player["metrics"]

    names = {

        "player_load": "Player Load",

        "distance_m": "Distancia",

        "high_speed_distance": "HSR",

        "very_high_speed_distance": "VHSR",

        "hmld_m": "HMLD",

        "mechanical_actions": "Acc. Mecánicas"

    }

    rows = []

    for metric, values in metrics.items():

        score = values["score"]

        if score >= 80:

            level = "Crítico"

            color = "#E53935"

        elif score >= 65:

            level = "Alto"

            color = "#FB8C00"

        elif score >= 45:

            level = "Moderado"

            color = "#FBC02D"

        else:

            level = "Bajo"

            color = "#43A047"

        rows.append({

            "Factor": names.get(metric, metric),

            "Score": score,

            "Nivel": level,

            "Color": color

        })

    plot_df = (

        pd.DataFrame(rows)

        .sort_values(

            "Score",

            ascending=False

        )

    )

    fig = px.bar(

        plot_df,

        x="Score",

        y="Factor",

        orientation="h",

        color="Nivel",

        color_discrete_map={

            "Crítico": "#E53935",

            "Alto": "#FB8C00",

            "Moderado": "#FBC02D",

            "Bajo": "#43A047"

        },

        text="Score",

        height=380

    )

    fig.update_traces(

        texttemplate="%{text:.0f}",

        textposition="outside"

    )

    fig.update_layout(

        title="Factores que generan el riesgo",

        showlegend=True,

        legend_title="Nivel",

        margin=dict(

            l=10,

            r=10,

            t=60,

            b=10

        ),

        xaxis=dict(

            title="Score",

            range=[0,100]

        ),

        yaxis=dict(

            title=""

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # PRINCIPAL FACTOR
    # ==========================================================

    top = plot_df.iloc[0]

    icon = {

        "Crítico": "🔴",

        "Alto": "🟠",

        "Moderado": "🟡",

        "Bajo": "🟢"

    }

    st.info(

        f"""

### Principal factor de riesgo

{icon[top['Nivel']]} **{top['Factor']}**

Score: **{top['Score']:.1f}**

Nivel: **{top['Nivel']}**

"""

    )

    st.divider()

# =============================================================================
# RISK GAUGE
# =============================================================================

import plotly.graph_objects as go
import streamlit as st


def risk_gauge(player):
    """
    Indicador principal del estado del jugador.
    """

    score = player["overall_score"]
    risk = player["risk"]

    decision = player["decision"]

    availability = decision["availability"]
    action = decision["action"]

    colors = {

        "Bajo": "#43A047",
        "Moderado": "#FBC02D",
        "Alto": "#FB8C00",
        "Muy Alto": "#E53935"

    }

    color = colors.get(risk, "#1976D2")

    # ==========================================================
    # CABECERA
    # ==========================================================

    st.subheader(f"👤 {player['player']}")

    c1, c2 = st.columns([1.2, 1])

    # ==========================================================
    # GAUGE
    # ==========================================================

    with c1:

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=score,

                number=dict(
                    font=dict(size=42)
                ),

                gauge=dict(

                    axis=dict(
                        range=[0, 100],
                        tickwidth=1
                    ),

                    bar=dict(
                        color=color,
                        thickness=0.32
                    ),

                    steps=[

                        dict(
                            range=[0,40],
                            color="rgba(67,160,71,0.25)"
                        ),

                        dict(
                            range=[40,70],
                            color="rgba(251,192,45,0.25)"
                        ),

                        dict(
                            range=[70,100],
                            color="rgba(229,57,53,0.25)"
                        )

                    ],

                    threshold=dict(

                        value=score,

                        line=dict(
                            color="white",
                            width=5
                        ),

                        thickness=0.9

                    )

                )

            )

        )

        fig.update_layout(

            height=320,

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=10
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ==========================================================
    # RESUMEN
    # ==========================================================

    with c2:

        st.metric(

            "Nivel de riesgo",

            risk

        )

        st.metric(

            "Disponibilidad",

            availability

        )

        st.metric(

            "Acción recomendada",

            action

        )

        st.info(

            player["reason"]

        )

    st.divider()

# =============================================================================
# RISK HISTORY CHART
# =============================================================================

import plotly.graph_objects as go
import streamlit as st


def risk_history_chart(history):
    """
    Evolución del estado del jugador.
    """

    if history.empty:

        st.info("No hay histórico suficiente.")

        return

    # ==========================================================
    # ÚLTIMAS SESIONES
    # ==========================================================

    history = history.tail(10).copy()

    # ==========================================================
    # TENDENCIA
    # ==========================================================

    variation = (

        history.iloc[-1]["overall_score"]

        -

        history.iloc[0]["overall_score"]

    )

    if variation >= 5:

        st.success(

            f"📈 Tendencia positiva (+{variation:.1f} puntos)"

        )

    elif variation <= -5:

        st.error(

            f"📉 Tendencia negativa ({variation:.1f} puntos)"

        )

    else:

        st.info(

            "➖ Estado estable"

        )

    # ==========================================================
    # MEDIA
    # ==========================================================

    mean_score = history["overall_score"].mean()

    # ==========================================================
    # FIGURA
    # ==========================================================

    fig = go.Figure()

    # ==========================================================
    # ZONAS
    # ==========================================================

    fig.add_hrect(

        y0=0,

        y1=40,

        fillcolor="rgba(67,160,71,0.10)",

        line_width=0

    )

    fig.add_hrect(

        y0=40,

        y1=60,

        fillcolor="rgba(255,235,59,0.10)",

        line_width=0

    )

    fig.add_hrect(

        y0=60,

        y1=75,

        fillcolor="rgba(251,140,0,0.10)",

        line_width=0

    )

    fig.add_hrect(

        y0=75,

        y1=100,

        fillcolor="rgba(229,57,53,0.10)",

        line_width=0

    )

    # ==========================================================
    # MEDIA
    # ==========================================================

    fig.add_hline(

        y=mean_score,

        line_dash="dot",

        line_color="white",

        annotation_text="Media",

        annotation_position="top left"

    )

    # ==========================================================
    # EVOLUCIÓN
    # ==========================================================

    fig.add_trace(

        go.Scatter(

            x=history["date"],

            y=history["overall_score"],

            mode="lines+markers",

            line=dict(

                color="#4F8EF7",

                width=4

            ),

            marker=dict(

                size=8,

                color="#4F8EF7"

            ),

            hovertemplate=

            "<b>%{x|%d/%m/%Y}</b><br>" +

            "Score: %{y:.1f}<extra></extra>"

        )

    )

    # ==========================================================
    # ÚLTIMO VALOR
    # ==========================================================

    last = history.iloc[-1]

    fig.add_trace(

        go.Scatter(

            x=[last["date"]],

            y=[last["overall_score"]],

            mode="markers",

            marker=dict(

                size=22,

                color="#E53935",

                line=dict(

                    color="white",

                    width=3

                )

            ),

            showlegend=False,

            hovertemplate=

            "<b>Última sesión</b><br>" +

            "Score: %{y:.1f}<extra></extra>"

        )

    )

    # ==========================================================
    # LAYOUT
    # ==========================================================

    fig.update_layout(

        title="Evolución del estado (últimas 10 sesiones)",

        height=460,

        showlegend=False,

        hovermode="x unified",

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        xaxis=dict(

            title="",

            showgrid=False

        ),

        yaxis=dict(

            title="Score",

            range=[0,100],

            gridcolor="rgba(255,255,255,0.08)"

        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

# =============================================================================
# COACH DECISION CARD
# =============================================================================

import streamlit as st


def coach_decision_card(player):
    """
    Tarjeta ejecutiva para el entrenador.
    """

    decision = player["decision"]
    report = player["report"]

    availability = decision["availability"]
    action = decision["action"]
    restriction = decision["restriction"]

    risk = player["risk"]
    score = player["overall_score"]

    # ==========================================================
    # COLOR DEL ESTADO
    # ==========================================================

    if risk == "Bajo":

        icon = "🟢"
        title = "Disponible"

    elif risk == "Moderado":

        icon = "🟡"
        title = "Disponible con control"

    elif risk == "Alto":

        icon = "🟠"
        title = "Reducir carga"

    else:

        icon = "🔴"
        title = "No recomendado"

    # ==========================================================
    # TÍTULO
    # ==========================================================

    st.subheader("🧠 Decisión del cuerpo técnico")

    st.success(

        f"""
## {icon} {title}

**Score global:** {score:.1f}

**Nivel de riesgo:** {risk}
"""
    )

    # ==========================================================
    # PLAN DEL DÍA
    # ==========================================================

    st.markdown("### 📋 Plan para hoy")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Entrenamiento",

            action

        )

    with c2:

        st.metric(

            "Disponibilidad",

            availability

        )

    with c3:

        st.metric(

            "Restricción",

            restriction

        )

    st.divider()

    # ==========================================================
    # MOTIVO
    # ==========================================================

    st.markdown("### 📌 Motivo principal")

    st.info(player["reason"])

    # ==========================================================
    # RECOMENDACIÓN
    # ==========================================================

    recommendation = ""

    if isinstance(report, dict):

        recommendation = report.get(

            "recommendation",

            ""

        )

    if recommendation != "":

        st.markdown("### 🎯 Recomendación")

        st.success(recommendation)


import plotly.graph_objects as go


def player_evolution_chart(
    df,
    player_name
):
    """
    Evolución temporal del jugador frente a la media del equipo.
    """

    st.subheader("📈 Evolución temporal")

    # ==========================================
    # MÉTRICAS DISPONIBLES
    # ==========================================

    metrics = [

        c

        for c in df.select_dtypes(include="number").columns

        if c not in [

            "season",
            "week"

        ]

    ]

    metric = st.selectbox(

        "Métrica",

        metrics

    )

    # ==========================================
    # FECHAS
    # ==========================================

    min_date = df["date"].min()

    max_date = df["date"].max()

    start_date, end_date = st.date_input(

        "Rango de fechas",

        value=(

            min_date,

            max_date

        )

    )

    # ==========================================
    # FILTRO
    # ==========================================

    data = df[

        (df["date"] >= pd.to_datetime(start_date))

        &

        (df["date"] <= pd.to_datetime(end_date))

    ]

    # ==========================================
    # SERIES
    # ==========================================

    player = (

        data[data["player"] == player_name]

        .groupby("date")[metric]

        .mean()

        .reset_index()

    )

    team = (

        data

        .groupby("date")[metric]

        .mean()

        .reset_index()

    )

    # ==========================================
    # FIGURA
    # ==========================================

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=team["date"],

            y=team[metric],

            mode="lines",

            name="Media equipo",

            line=dict(

                width=3,

                dash="dot"

            )

        )

    )

    fig.add_trace(

        go.Scatter(

            x=player["date"],

            y=player[metric],

            mode="lines+markers",

            name=player_name,

            line=dict(

                width=4

            )

        )

    )

    fig.update_layout(

        height=450,

        hovermode="x unified",

        xaxis_title="",

        yaxis_title=metric,

        legend_title="",

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )