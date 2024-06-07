import json
import os

archivo_productos = "productos.json"

def cargar_productos():
    if os.path.exists(archivo_productos):
        with open(archivo_productos, "r") as archivo:
            return json.load(archivo)
    return []

def guardar_productos(productos):
    with open(archivo_productos, "w") as archivo:
        json.dump(productos, archivo, indent=4)