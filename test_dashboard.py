from services.loader import load_data
from services.dashboard import build_dashboard

print("Cargando datos...")

df = load_data()

print(df.shape)

print("Construyendo dashboard...")

dashboard = build_dashboard(df)

print()

print("Dashboard generado correctamente")

print()

print(dashboard.keys())