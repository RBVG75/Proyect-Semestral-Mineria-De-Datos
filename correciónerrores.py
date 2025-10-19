import csv
import re

entrada = "sismos.csv"
salida = "bdd.csv"

with open(entrada, newline='', encoding="utf-8") as fin, \
     open(salida, "w", newline='', encoding="utf-8") as fout:
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        latlong = row["latitud"]
        match = re.match(r"^\s*([+-]?\d+\.\d+)[\s\-]+([+-]?\d+\.\d+)\s*$", latlong)
        if not row["longitud"] and match:
            row["latitud"] = match.group(1)
            row["longitud"] = match.group(2)
        elif not row["longitud"] and "-" in latlong:
            parts = latlong[1:].split("-", 1)
            if len(parts) == 2:
                row["latitud"] = latlong[0] + parts[0]
                row["longitud"] = "-" + parts[1]
        writer.writerow(row)

print("Archivo corregido guardado como:", salida)

