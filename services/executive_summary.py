from services.metrics import executive_metrics
from services.interpretations import (
    interpret_team_status,
    interpret_external_load,
    interpret_internal_load,
    interpret_recovery,
)


def generate_summary(df):
    """
    Genera un resumen ejecutivo del estado del equipo.
    """

    metrics = executive_metrics(df)

    estado, _, _ = interpret_team_status(df)
    carga, _, = interpret_external_load(df)
    carga_interna, _ = interpret_internal_load(df)
    recuperacion, _ = interpret_recovery(df)

    texto = f"""
La plantilla presenta actualmente un estado general **{estado.lower()}**.

Se han analizado **{metrics['players']} jugadores** y **{metrics['sessions']} sesiones**, observándose un Player Load acumulado de **{metrics['player_load']:.0f} AU**, una distancia total de **{metrics['distance']:.0f} metros** y una exposición a alta velocidad de **{metrics['hsr']:.0f} metros**.

La carga externa se clasifica como **{carga.lower()}**, mientras que la carga interna muestra un comportamiento **{carga_interna.lower()}** con un RPE medio de **{metrics['rpe']:.1f}**.

El bienestar colectivo presenta un valor medio de **{metrics['wellness']:.2f}**, situando el nivel de recuperación en un estado **{recuperacion.lower()}**.

En conjunto, los indicadores disponibles permiten obtener una visión global del estado actual del equipo y constituyen la base para la planificación de la siguiente sesión de entrenamiento.
"""

    return texto