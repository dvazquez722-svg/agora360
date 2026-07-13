"""
compare_config.py

Configuración global del módulo de Análisis Comparativo.

Este archivo contiene únicamente constantes y catálogos.
No incluye ninguna función ni lógica de negocio.
"""

# =============================================================================
# COLUMNAS DEL DATASET
# =============================================================================

DATA_COLUMNS = {

    "player": "player",

    "team": "team",

    "position": "position",

    "date": "date",

    "session": "session",

    "microcycle": "microcycle",

    "week": "week"

}

# =============================================================================
# CATEGORÍAS DE MÉTRICAS
# =============================================================================

METRIC_CATEGORIES = {

    "Carga": {

        "order": 1

    },

    "Volumen": {

        "order": 2

    },

    "Alta intensidad": {

        "order": 3

    },

    "Aceleraciones": {

        "order": 4

    },

    "Desaceleraciones": {

        "order": 5

    },

    "Velocidad": {

        "order": 6

    }

}

# =============================================================================
# CATÁLOGO DE MÉTRICAS
# =============================================================================

METRICS = {

    "player_load": {

        "label": "Player Load",

        "short": "PL",

        "unit": "",

        "category": "Carga",

        "default": True,

        "higher_is_better": False,

        "format": ".1f",

        "color": "#2563EB",

        "order": 1

    },

    "distance_m": {

        "label": "Distancia",

        "short": "Distancia",

        "unit": "m",

        "category": "Volumen",

        "default": True,

        "higher_is_better": True,

        "format": ".0f",

        "color": "#16A34A",

        "order": 2

    },

    "high_speed_distance": {

        "label": "HSR",

        "short": "HSR",

        "unit": "m",

        "category": "Alta intensidad",

        "default": True,

        "higher_is_better": True,

        "format": ".0f",

        "color": "#EA580C",

        "order": 3

    },

    "very_high_speed_distance": {

        "label": "VHSR",

        "short": "VHSR",

        "unit": "m",

        "category": "Alta intensidad",

        "default": True,

        "higher_is_better": True,

        "format": ".0f",

        "color": "#DC2626",

        "order": 4

    },

    "hmld_m": {

        "label": "HMLD",

        "short": "HMLD",

        "unit": "m",

        "category": "Alta intensidad",

        "default": True,

        "higher_is_better": True,

        "format": ".0f",

        "color": "#7C3AED",

        "order": 5

    },

    "mechanical_actions": {

        "label": "Acciones Mecánicas",

        "short": "Acc. Mec.",

        "unit": "",

        "category": "Carga",

        "default": True,

        "higher_is_better": False,

        "format": ".0f",

        "color": "#0891B2",

        "order": 6

    }

}

# =============================================================================
# TIPOS DE ANÁLISIS
# =============================================================================

ANALYSIS_TYPES = {

    "player_vs_player": {

        "label": "Jugador vs Jugador",

        "entities": ["player", "player"],

        "layout": [

            {"type": "summary"},
            {"type": "radar"},
            {"type": "bar"},
            {"type": "line"},
            {"type": "insights"}

        ]

    },

    "player_vs_position": {

        "label": "Jugador vs Posición",

        "entities": ["player", "position"],

        "layout": [

            {"type": "summary"},
            {"type": "bar"},
            {"type": "boxplot"},
            {"type": "distribution"},
            {"type": "insights"}

        ]

    },

    "player_vs_team": {

        "label": "Jugador vs Plantilla",

        "entities": ["player"],

        "layout": [

            {"type": "summary"},
            {"type": "distribution"},
            {"type": "boxplot"},
            {"type": "insights"}

        ]

    },

    "position_vs_position": {

        "label": "Posición vs Posición",

        "entities": ["position", "position"],

        "layout": [

            {"type": "summary"},
            {"type": "boxplot"},
            {"type": "bar"},
            {"type": "insights"}

        ]

    },

    "week_vs_week": {

        "label": "Semana vs Semana",

        "entities": ["week", "week"],

        "layout": [

            {"type": "summary"},
            {"type": "line"},
            {"type": "bar"},
            {"type": "insights"}

        ]

    },

    "session_vs_session": {

        "label": "Sesión vs Sesión",

        "entities": ["session", "session"],

        "layout": [

            {"type": "summary"},
            {"type": "bar"},
            {"type": "line"},
            {"type": "insights"}

        ]

    },

    "day_vs_day": {

        "label": "Día vs Día",

        "entities": ["microcycle", "microcycle"],

        "layout": [

            {"type": "summary"},
            {"type": "line"},
            {"type": "bar"},
            {"type": "distribution"},
            {"type": "insights"}

        ]

    }

}

# =============================================================================
# VISUALIZACIONES
# =============================================================================

VISUALIZATIONS = {

    "summary": {

        "label": "Resumen",

        "component": "comparison_summary",

        "order": 1

    },

    "radar": {

        "label": "Radar",

        "component": "comparison_radar",

        "order": 2

    },

    "bar": {

        "label": "Barras",

        "component": "comparison_bar",

        "order": 3

    },

    "line": {

        "label": "Líneas",

        "component": "comparison_line",

        "order": 4

    },

    "boxplot": {

        "label": "Boxplot",

        "component": "comparison_boxplot",

        "order": 5

    },

    "distribution": {

        "label": "Distribución",

        "component": "comparison_distribution",

        "order": 6

    },

    "violin": {

        "label": "Violín",

        "component": "comparison_violin",

        "order": 7

    },

    "insights": {

        "label": "Hallazgos",

        "component": "comparison_insights",

        "order": 8

    }

}