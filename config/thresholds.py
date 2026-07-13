"""
Umbrales globales del sistema de monitorización.

Todos los módulos deben utilizar estos valores.
No deben existir números "quemados" en el código.
"""

# ==========================================================
# ACWR
# ==========================================================

ACWR_LOW = 0.80
ACWR_OPTIMAL_MAX = 1.30
ACWR_WARNING = 1.50
ACWR_HIGH = 1.80


# ==========================================================
# CAMBIO SEMANAL (%)
# ==========================================================

LOAD_CHANGE_WARNING = 15
LOAD_CHANGE_HIGH = 25


# ==========================================================
# EWMA (%)
# ==========================================================

EWMA_STABLE = 10
EWMA_WARNING = 20
EWMA_HIGH = 30


# ==========================================================
# PERCENTILES
# ==========================================================

PLAYERLOAD_PERCENTILE_WARNING = 85
PLAYERLOAD_PERCENTILE_HIGH = 95

DISTANCE_PERCENTILE_WARNING = 85
DISTANCE_PERCENTILE_HIGH = 95

HSR_PERCENTILE_WARNING = 85
HSR_PERCENTILE_HIGH = 95

SPRINT_PERCENTILE_WARNING = 85
SPRINT_PERCENTILE_HIGH = 95


# ==========================================================
# Z SCORE
# ==========================================================

ZSCORE_WARNING = 1.5
ZSCORE_HIGH = 2.0


# ==========================================================
# CARGA INTERNA (solo si existen datos válidos)
# ==========================================================

RPE_WARNING = 7
RPE_HIGH = 8

WELLNESS_WARNING = 3
WELLNESS_HIGH = 2


# ==========================================================
# DISPONIBILIDAD
# ==========================================================

AVAILABILITY_WARNING = 90
AVAILABILITY_HIGH = 80