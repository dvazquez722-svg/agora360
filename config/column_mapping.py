"""
Mapeo de nombres de columnas del dataset WIMU.

Todos los nombres originales se transforman a
snake_case para facilitar el desarrollo.
"""

COLUMN_MAPPING ={

# ==========================================================
# IDENTIFICACIÓN
# ==========================================================

"Player": "player",
"Wimu Name": "wimu_name",
"Team": "team",
"Position": "position",
"Sport": "sport",

# ==========================================================
# FECHAS
# ==========================================================

"Date": "date",
"Week Calendar": "week_calendar",
"Week Team": "week_team",
"Week Match Day": "week_match_day",

# ==========================================================
# SESIÓN
# ==========================================================

"Start hour": "start_hour",
"Final Hour": "final_hour",
"Num Session/day": "session_number",
"Session": "session",
"Type Session": "type_session",
"Group": "group",
"Match Day": "match_day",
"Num Total Session": "total_session",
"Task": "task",
"Repetition": "repetition",

# ==========================================================
# DURACIÓN
# ==========================================================

"Drills Duration": "drills_duration",
"Positioning Duration": "positioning_duration",

# ==========================================================
# DISTANCIAS
# ==========================================================

"Distance(m)": "distance_m",
"Explosive Distance (m)": "explosive_distance_m",
"HSR Rel (m)": "hsr_rel_m",
"HSR Rel (count)": "hsr_rel_count",
"Abs HSR(m)": "abs_hsr_m",
"Abs HSR (count)": "abs_hsr_count",

# ==========================================================
# SPRINT
# ==========================================================

"Sprint Duration (s)": "sprint_duration",
"Sprints Abs (count)": "sprints_abs_count",
"Sprints Rel (count)": "sprints_rel_count",
"Distance Abs(m)": "distance_abs_m",
"Distance Rel(m)": "distance_rel_m",

# ==========================================================
# VELOCIDAD
# ==========================================================

"Max Speed (km/h)": "max_speed_kmh",
"AVG Speed (km/h)": "avg_speed_kmh",

# ==========================================================
# ACELERACIONES
# ==========================================================

"Accelerations(count)": "accelerations",
"Decelerations(count)": "decelerations",

"Distance Acceleration (m)": "distance_acceleration",
"Distance Deceleration (m)": "distance_deceleration",

"AVG Acceleration (m/s²)": "avg_acceleration",
"AVG Deceleration (m/s²)": "avg_deceleration",

"Max Acceleration (m/s²)": "max_acceleration",
"Max Deceleration (m/s²)": "max_deceleration",

# ==========================================================
# CARDIACO
# ==========================================================

"Max Heart Rate (BPM)": "max_heart_rate",
"AVG Heart Rate (BPM)": "avg_heart_rate",
"AVG HR  (% of player max HR)": "avg_hr_percent",

# ==========================================================
# IMPACTOS
# ==========================================================

"Impacts (count)": "impacts",

# ==========================================================
# PASOS
# ==========================================================

"Steps (count)": "steps",
"Step Balance (%)": "step_balance",

# ==========================================================
# SALTOS
# ==========================================================

"Jumps (count)": "jumps",
"AVG Take Off (G)": "avg_takeoff",
"AVG Landing (G)": "avg_landing",

# ==========================================================
# FRECUENCIA
# ==========================================================

"MAX Freq (Hz)": "max_frequency",
"AVG Freq. (Hz)": "avg_frequency",

# ==========================================================
# PLAYER LOAD
# ==========================================================

"Player Load (a.u.)": "player_load",

"Player Load  Horizontal": "player_load_horizontal",
"Player Load  Vertical": "player_load_vertical",
"Player Load  Anteroposterior": "player_load_anteroposterior",
"Player Load  Medio Lateral": "player_load_mediolateral",

# ==========================================================
# METABÓLICAS
# ==========================================================

"Power Metabolic (W/kg)": "metabolic_power",
"Power Metabolic AVG (W/kg)": "metabolic_power_avg",

"HMLD (m)": "hmld_m",
"HMLD (count)": "hmld_count",

"Energy Expenditure (kcal)": "energy_expenditure",

"DSL (a.u.)": "dsl",

# ==========================================================
# RPE
# ==========================================================

"RPE General": "rpe_general",
"RPE Peripheral": "rpe_peripheral",

# ==========================================================
# WELLNESS
# ==========================================================

"Wellness Fatige": "wellness_fatigue",
"Wellness Sleep": "wellness_sleep",
"Wellness Doms": "wellness_doms",
"Wellness Stress": "wellness_stress",
"Wellness Mood": "wellness_mood",

# ==========================================================
# OTROS
# ==========================================================

"SIGNAL": "signal",

# ==========================================================
# SPEED ZONES (DISTANCIA)
# ==========================================================

"Speed Zones (m) [0, 6] (m)": "speed_0_6_m",
"Speed Zones (m) [6, 12] (m)": "speed_6_12_m",
"Speed Zones (m) [12, 18] (m)": "speed_12_18_m",
"Speed Zones (m) [18, 21] (m)": "speed_18_21_m",
"Speed Zones (m) [21, 24] (m)": "speed_21_24_m",
"Speed Zones (m) [24, 50] (m)": "speed_24_50_m",

# ==========================================================
# SPEED ZONES (ACCIONES)
# ==========================================================

"Speed Zones (m) [0, 6] Cnt": "speed_0_6_count",
"Speed Zones (m) [6, 12] Cnt": "speed_6_12_count",
"Speed Zones (m) [12, 18] Cnt": "speed_12_18_count",
"Speed Zones (m) [18, 21] Cnt": "speed_18_21_count",
"Speed Zones (m) [21, 24] Cnt": "speed_21_24_count",
"Speed Zones (m) [24, 50] Cnt": "speed_24_50_count",

# ==========================================================
# ACCELERATION ZONES
# ==========================================================

"Acceleration Zones (count) [0, 1] Cnt": "acc_0_1",
"Acceleration Zones (count) [1, 2] Cnt": "acc_1_2",
"Acceleration Zones (count) [2, 3] Cnt": "acc_2_3",
"Acceleration Zones (count) [3, 4] Cnt": "acc_3_4",
"Acceleration Zones (count) [4, 5] Cnt": "acc_4_5",
"Acceleration Zones (count) [5, 6] Cnt": "acc_5_6",
"Acceleration Zones (count) [6, 10] Cnt": "acc_6_10",

# ==========================================================
# DECELERATION ZONES
# ==========================================================

"Acceleration Zones (count) [-1, 0] Cnt": "dec_1_0",
"Acceleration Zones (count) [-2, -1] Cnt": "dec_2_1",
"Acceleration Zones (count) [-3, -2] Cnt": "dec_3_2",
"Acceleration Zones (count) [-4, -3] Cnt": "dec_4_3",
"Acceleration Zones (count) [-5, -4] Cnt": "dec_5_4",
"Acceleration Zones (count) [-6, -5] Cnt": "dec_6_5",
"Acceleration Zones (count) [-10, -6] Cnt": "dec_10_6",

# ==========================================================
# IMPACTS
# ==========================================================

"Zones(G) [0, 3] (m)": "impacts_0_3",
"Zones(G) [3, 5] (m)": "impacts_3_5",
"Zones(G) [5, 8] (m)": "impacts_5_8",
"Zones(G) [8, 100] (m)": "impacts_8_plus",

# ==========================================================
# FREQUENCY
# ==========================================================

"FFT Duration (ms)": "fft_duration",

"MAX Freq (Hz)": "max_frequency",

"AVG Freq. (Hz)": "avg_frequency",

}


