import json
import os

archivo_usuarios = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(archivo_usuarios):
        with open(archivo_usuarios, "r") as archivo:
            return json.load(archivo)
    return []

def guardar_usuarios(usuarios):
    with open(archivo_usuarios, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

