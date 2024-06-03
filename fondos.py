import tkinter as tk
from PIL import Image, ImageTk
import os

def establecer_imagen_de_fondo(ventana, ruta_imagen):
    if os.path.exists(ruta_imagen):
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()), Image.BILINEAR)
        fondo = ImageTk.PhotoImage(imagen)
        label_fondo = tk.Label(ventana, image=fondo)
        label_fondo.image = fondo
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    else:
        print(f"Archivo de fondo no encontrado: {ruta_imagen}")
