import tkinter as tk
from tkinter import messagebox
import fondos
import json_productos
import os
import re
import subprocess

def gestion_productos(productos, nombre_usuario, root):
    def agregar_producto():
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        stock = entry_stock.get()
        if nombre and precio and stock:
            try:
                precio = float(precio)
                stock = int(stock)
                if precio > 0 and stock >= 0:
                    nuevo_producto = {"nombre": nombre, "precio": precio, "stock": stock}
                    productos.append(nuevo_producto)
                    json_productos.guardar_productos(productos)
                    messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                    actualizar_lista_productos()
                else:
                    messagebox.showerror("Error", "Precio o stock no válidos.")
            except ValueError:
                messagebox.showerror("Error", "Precio o stock no válidos.")
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos.")

    def actualizar_lista_productos():
        listbox_productos.delete(0, tk.END)
        for producto in productos:
            info_producto = f"{producto['nombre']} - Precio: {producto['precio']} - Stock: {producto['stock']}"
            listbox_productos.insert(tk.END, info_producto)

    def eliminar_producto():
        selected_index = listbox_productos.curselection()
        if selected_index:
            confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este producto?")
            if confirmacion:
                producto_eliminado = productos[selected_index[0]]
                del productos[selected_index[0]]
                json_productos.guardar_productos(productos)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                actualizar_lista_productos()

    def modificar_producto():
        selected_index = listbox_productos.curselection()
        if selected_index:
            producto_modificar = productos[selected_index[0]]
            nuevo_nombre = entry_nombre.get()
            nuevo_precio = entry_precio.get()
            nuevo_stock = entry_stock.get()
            if nuevo_nombre and nuevo_precio and nuevo_stock:
                try:
                    nuevo_precio = float(nuevo_precio)
                    nuevo_stock = int(nuevo_stock)
                    if nuevo_precio > 0 and nuevo_stock > 0:
                        if re.match("^[a-zA-Z\s]+$", nuevo_nombre):
                            producto_modificar["nombre"] = nuevo_nombre
                            producto_modificar["precio"] = nuevo_precio
                            producto_modificar["stock"] = nuevo_stock
                            json_productos.guardar_productos(productos)
                            messagebox.showinfo("Éxito", "Producto modificado correctamente")
                            actualizar_lista_productos()
                        else:
                            messagebox.showerror("Error", "El nombre del producto solo puede contener letras y espacios")
                    else:
                        messagebox.showerror("Error", "El precio y la cantidad deben ser números positivos")
                except ValueError:
                    messagebox.showerror("Error", "El precio y la cantidad deben ser números")
            else:
                messagebox.showerror("Error", "Por favor completa todos los campos")

    productos = json_productos.cargar_productos()

    gestion_window = tk.Toplevel(root)
    gestion_window.title("Gestión de Productos")
    gestion_window.state('normal')
    gestion_window.attributes('-fullscreen', True)

    def volver():
        gestion_window.destroy()
        subprocess.Popen(["python","main.py"])

    # Verificar la existencia del archivo antes de establecer la imagen de fondo
    fondo_path = "fondoge.png"
    fondos.establecer_imagen_de_fondo(gestion_window, fondo_path)

    gestion_frame = tk.Frame(gestion_window, padx=40, pady=20, bg="#FED89B")  # Aumento del padding para hacer los elementos más grandes
    gestion_frame.pack()

    global entry_nombre
    global entry_precio
    global entry_stock
    global listbox_productos

    label_nombre = tk.Label(gestion_frame, text="Nombre:", font=("Times new roman", 14), bg="#FED89B")  # Aumentar el tamaño de la fuente
    label_nombre.grid(row=0, column=0)
    entry_nombre = tk.Entry(gestion_frame, font=("Times new roman", 14))  # Aumentar el tamaño de la fuente
    entry_nombre.grid(row=0, column=1)

    label_precio = tk.Label(gestion_frame, text="Precio:", font=("Times new roman", 14), bg="#FED89B")  # Aumentar el tamaño de la fuente
    label_precio.grid(row=1, column=0)
    entry_precio = tk.Entry(gestion_frame, font=("Times new roman", 14))  # Aumentar el tamaño de la fuente
    entry_precio.grid(row=1, column=1)

    label_stock = tk.Label(gestion_frame, text="Stock:", font=("Times new roman", 14), bg="#FED89B")  # Aumentar el tamaño de la fuente
    label_stock.grid(row=2, column=0)
    entry_stock = tk.Entry(gestion_frame, font=("Times new roman", 14))  # Aumentar el tamaño de la fuente
    entry_stock.grid(row=2, column=1)

    btn_agregar = tk.Button(gestion_frame, text="Agregar Producto", command=agregar_producto, font=("Times new roman", 14), bg="#BE7250", fg="white")  # Aumentar el tamaño de la fuente
    btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

    # ListBox para mostrar los productos existentes
    listbox_productos = tk.Listbox(gestion_frame, width=50, height=10, font=("Times new roman", 12))  # Aumentar el tamaño de la fuente
    listbox_productos.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Label para mostrar la categoría (en este caso, "Gestión")
    label_categoria = tk.Label(gestion_frame, text="Categoría: Gestión", font=("Times new roman", 14), bg="#FED89B")  # Aumentar el tamaño de la fuente
    label_categoria.grid(row=5, column=0, columnspan=2)

    btn_eliminar = tk.Button(gestion_frame, text="Eliminar Producto", command=eliminar_producto,font=("Times new roman", 14),bg="#BE7250", fg="white")  # Aumentar el tamaño de la fuente
    btn_eliminar.grid(row=7, column=0, columnspan=3, pady=10)
    btn_modificar = tk.Button(gestion_frame, text="Modificar Producto", command=modificar_producto, font=("Times new roman", 14), bg="#BE7250", fg="white")  # Aumentar el tamaño de la fuente
    btn_modificar.grid(row=8, column=0, columnspan=3, pady=10)

    btn_volver = tk.Button(gestion_frame, text="Volver", command=volver, font=("Times new roman", 14), bg="#BE7250", fg="white")  # Aumentar el tamaño de la fuente
    btn_volver.grid(row=9, column=0, columnspan=3, pady=10)
    
    # Actualizar la lista de productos
    actualizar_lista_productos()

  