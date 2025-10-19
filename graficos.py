import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Leer datos
df = pd.read_csv('bdd.csv')

plt.figure(figsize=(8, 6))
bins = [-np.inf, 3.5, 5.0, np.inf]
labels = ['Leve', 'Moderado', 'Fuerte']
df['categoria'] = pd.cut(df['magnitud'], bins=bins, labels=labels)
conteos = df['categoria'].value_counts().reindex(labels)
conteos.plot(kind='bar')
plt.title('Distribución de Sismos por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Cantidad de Sismos')
plt.show()


# 2. Top 10 regiones por cantidad de sismos
plt.figure(figsize=(12, 6))
top_10_regiones = df['region'].value_counts().head(10)
sns.barplot(x=top_10_regiones.values, y=top_10_regiones.index)
plt.title('Top 10 Regiones con Mayor Cantidad de Sismos')
plt.xlabel('Cantidad de Sismos')
plt.show()


# 3. Distribución de magnitudes (histograma)
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='magnitud', bins=30, kde=True)
plt.title('Distribución de Magnitudes Sísmicas')
plt.xlabel('Magnitud')
plt.ylabel('Frecuencia')
plt.show()


# 4. Mapa de calor de sismos por región y categoría
plt.figure(figsize=(12, 8))
pivot_table = pd.crosstab(df['region'], df['categoria'])
sns.heatmap(pivot_table, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Mapa de Calor: Sismos por Región y Categoría')
plt.ylabel('Región')
plt.xlabel('Categoría')
plt.show()

# 5. Gráfico de dispersión de magnitud vs profundidad
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='magnitud', y='rango_profundidad', hue='rango_profundidad', alpha=0.6, legend=False)
plt.title('Magnitud vs Rango de Profundidad')
plt.xlabel('Magnitud')
plt.ylabel('Rango de Profundidad')
plt.show()

# 6. Box plot de magnitudes por región
plt.figure(figsize=(15, 6))
sns.boxplot(data=df, x='region', y='magnitud')
plt.title('Distribución de Magnitudes por Región')
plt.show()

print("Gráficos generados y guardados como archivos PNG")