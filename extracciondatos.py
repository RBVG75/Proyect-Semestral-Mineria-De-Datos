import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
import pandas as pd

hoy = datetime.today()
fecha_inicio = hoy - timedelta(days=7)
todos_sismos = []

for i in range(7):
    fecha = hoy - timedelta(days=i)
    url = f"https://www.sismologia.cl/sismicidad/catalogo/{fecha.year}/{fecha.month:02d}/{fecha.strftime('%Y%m%d')}.html"
    print(f"Extrayendo: {url}")

    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"No se pudo acceder a {url}")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")
    tabla = soup.find("table", class_="sismologia detalle")
    if not tabla:
        print(f"No se encontró tabla para {fecha}")
        continue

    filas = tabla.find_all("tr")[1:] 

    for fila in filas:
        celdas = fila.find_all("td")
        if len(celdas) < 5:
            continue

        fecha_local = celdas[0].get_text(strip=True)
        fecha_utc = celdas[1].get_text(strip=True)
        lat_long_raw = celdas[2].get_text(strip=True)
        lat_long = [x for x in lat_long_raw.replace('\n', ' ').split(' ') if x]
        latitud = lat_long[0] if len(lat_long) > 0 else ""
        longitud = lat_long[1] if len(lat_long) > 1 else ""
        profundidad = celdas[3].get_text(strip=True)
        magnitud = celdas[4].get_text(strip=True)

        todos_sismos.append({
            "fecha_local": fecha_local,
            "fecha_utc": fecha_utc,
            "latitud": latitud,
            "longitud": longitud,
            "profundidad": profundidad,
            "magnitud": magnitud
        })
    time.sleep(1)

df_sismos = pd.DataFrame(todos_sismos)
df_sismos.to_csv("sismos.csv", index=False, encoding="utf-8")
print(f"Guardado en: sismos.csv")
