import pandas as pd
import re

# Leer CSV
df = pd.read_csv("sismos.csv", encoding="utf-8")

df[['latitud', 'longitud']] = df.apply(lambda row: ((row['latitud'], row['longitud']) if row['longitud'] not in [None, ""] else(float(m.group(1)), float(m.group(2))) if (m := re.match(r"^\s*([+-]?\d+\.\d+)[\s\-]+([+-]?\d+\.\d+)\s*$", row['latitud'])) else(float(row['latitud'][0] + row['latitud'][1:].split("-",1)[0]),-float(row['latitud'][1:].split("-",1)[1])) if "-" in row['latitud'][1:] else(row['latitud'], row['longitud'])),axis=1,result_type='expand')

# Guardar CSV limpio
df.to_csv("bdd.csv", index=False, encoding="utf-8")

print("Archivo corregido guardado como: bdd.csv")
