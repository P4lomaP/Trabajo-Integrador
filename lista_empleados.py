import json
import os

archivo_empleados = "empleados.json"

def cargar_empleados():
    if os.path.exists(archivo_empleados):
        with open(archivo_empleados, "r") as archivo:
            return json.load(archivo)
    return []

def guardar_empleados(usuarios):
    with open(archivo_empleados, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

