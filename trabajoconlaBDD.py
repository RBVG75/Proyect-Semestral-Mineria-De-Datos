import numpy as np
import pandas as pd

# Leer csv
df = pd.read_csv('bdd.csv')
df.dropna(inplace=True)

# Convertir magnitud
df['magnitud'] = (
    df['magnitud']
    .astype(str)
    .str.extract(r'([\d,.]+)')
    .replace(',', '.', regex=True)
    .astype(float)
)
# Corregir longitud
df['longitud'] = -df['longitud'].abs()

promedio_magnitud = df['magnitud'].mean()
print(f"Magnitud promedio: {promedio_magnitud:.2f}")

rangos_regiones = [
    (-19.000, -17.300, "Arica y Parinacota"),
    (-21.300, -19.000, "Tarapacá"),
    (-25.300, -21.300, "Antofagasta"),
    (-29.300, -25.300, "Atacama"),
    (-32.000, -29.300, "Coquimbo"),
    (-32.950, -32.000, "Valparaíso"),
    (-34.150, -32.950, "Región Metropolitana de Santiago"),
    (-35.000, -34.150, "Libertador B. O'Higgins"),
    (-36.250, -35.000, "Maule"),
    (-36.850, -36.250, "Ñuble"),
    (-37.900, -36.850, "Biobío"),
    (-40.500, -37.900, "La Araucanía"),
    (-40.580, -39.500, "Los Ríos"),
    (-43.600, -40.580, "Los Lagos"),
    (-48.000, -43.600, "Aysén del General Carlos Ibáñez del Campo"),
    (-52.810, -48.000, "Magallanes y de la Antártica Chilena")
]

df['region'] = df['latitud'].apply(
    lambda lat: next((region for lat_min, lat_max, region in rangos_regiones if lat_min <= lat <= lat_max), "Fuera de Chile")
)
# Limpiar Datos Fuera de Chile
df = df[df['region'] != "Fuera de Chile"]
print(df[['latitud', 'longitud', 'region']])

# Links a maps
df['maps_link'] = df.apply(
    lambda row: f"https://www.google.com/maps?q={row['latitud']},{row['longitud']}",
    axis=1
)

# Limpiar y convertir profundidad a número
df['profundidad'] = (df['profundidad'].astype(str).str.extract(r'([\d.]+)').astype(float))

bins = [0, 10, 30, 60, 100, 200, 500, np.inf]
labels = ['<10 km', '10–30 km', '30–60 km', '60–100 km', '100–200 km', '200–500 km', '>500 km']
df['rango_profundidad'] = pd.cut(df['profundidad'], bins=bins, labels=labels)

# Guardar CSV limpio
df.to_csv('bdd.csv', index=False)

