import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

# Leer csv
df = pd.read_csv('bdd.csv')

print(df.info())

# Encontrar la latitud máxima y mínima
print("Latitud máxima:", df['latitud'].max())
print("Latitud mínima:", df['latitud'].min())

# Categorizar magnitudes
# Se elige 3.5 como limite entre leve y moderado, y 5.0 entre moderado y fuerte
bins = [-np.inf, 3.5, 5.0, np.inf]
labels = ['Leve', 'Moderado', 'Fuerte']
df['categoria'] = pd.cut(df['magnitud'], bins=bins, labels=labels)

# Conteos totales por categoría
conteos_categoria = df['categoria'].value_counts().reindex(labels, fill_value=0)
print("Conteos totales por categoría:")
print(conteos_categoria.to_string())

# Conteos por región y categoría
conteos = df.groupby(['region', 'categoria']).size().unstack(fill_value=0)
conteos['Total'] = conteos.sum(axis=1)
conteos = conteos.sort_values('Total', ascending=False)
print("Sismos por región y categoría:")
print(conteos.to_string())

# Resumen estadístico de magnitud por región
resumen = df.groupby('region')['magnitud'].agg(['count','mean','std','min','max']).sort_values('count', ascending=False)
print("Resumen estadístico de magnitud por región (top 20 por cantidad):")
print(resumen.head(20).to_string())

# Porcentajes por región
porcentaje = conteos.div(conteos['Total'], axis=0).round(3) * 100
print("\nPorcentaje por categoría dentro de cada región:")
print(porcentaje[['Leve','Moderado','Fuerte']].to_string())
