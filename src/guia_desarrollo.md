# Ágora 360
## Guía de desarrollo

---

# Flujo de trabajo con Git

## Ver cambios

```bash
git status
```

## Añadir cambios

```bash
git add .
```

## Crear commit

```bash
git commit -m "Descripción del cambio"
```

## Subir a GitHub

```bash
git push
```

---

# Estructura del proyecto

src/

    analytics/
    components/
    data/
    styles.py
    auth.py

pages/

    Estado General
    Plantilla
    Comparativas
    Microciclo
    Riesgo

---

# Arquitectura

Cada página debe seguir esta estructura:

1. Configuración
2. Autenticación
3. Carga de datos
4. Analytics
5. Componentes
6. Visualización

Nunca mezclar lógica con visualización.

---

# Reglas

✅ Una función = una responsabilidad.

✅ Nunca escribir HTML directamente en las páginas.

✅ Los estilos solo en styles.py.

✅ La lógica solo en analytics.

✅ Las visualizaciones solo en components.

✅ No acceder directamente al dataset desde un componente.

---

# Autenticación

Todas las páginas deben comenzar con:

```python
from src.auth import check_authentication

check_authentication()
```

---

# Estilos

Siempre:

```python
from src.styles import apply_styles

apply_styles()
```

---

# Flujo para añadir una nueva página

1. Crear analytics_x.py
2. Crear components_x.py
3. Crear page_x.py
4. Añadir autenticación
5. Aplicar estilos
6. Subir a GitHub

---

# Antes de hacer un commit

Comprobar:

□ No hay errores.

□ No hay imports sin usar.

□ La aplicación inicia.

□ Los gráficos funcionan.

□ Git status limpio.

---

# Próximos desarrollos

□ Rediseño definitivo del Home.

□ Calendar Builder.

□ Login real.

□ Usuarios y roles.

□ Exportación PDF.

□ Exportación Excel.

□ Informes automáticos.

□ Configuración.

□ Optimización del rendimiento.

---

# Convención de commits

feat: nueva funcionalidad

fix: corrección de errores

refactor: mejora interna

style: cambios visuales

docs: documentación

perf: optimización

---

# Filosofía del proyecto

Ágora 360 no es un dashboard.

Es un software de apoyo a la toma de decisiones para cuerpos técnicos profesionales.