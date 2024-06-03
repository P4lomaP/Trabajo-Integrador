import tkinter as tk
from tkinter import messagebox
import fondos
import json_productos
import subprocess

def ventas(productos, nombre_usuario, master):
    def vender_producto():
        selected_index = listbox_productos.curselection()
        if selected_index:
            producto = productos[selected_index[0]]
            cantidad_vendida = entry_cantidad.get()
            if cantidad_vendida:
                try:
                    cantidad_vendida = int(cantidad_vendida)
                    if cantidad_vendida > 0 and cantidad_vendida <= producto["stock"]:
                        producto["stock"] -= cantidad_vendida
                        json_productos.guardar_productos(productos)
                        messagebox.showinfo("Éxito", f"Se vendieron {cantidad_vendida} unidades de {producto['nombre']}.")
                        actualizar_lista_productos()
                    else:
                        messagebox.showerror("Error", "La cantidad ingresada no es válida.")
                except ValueError:
                    messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            else:
                messagebox.showerror("Error", "Por favor ingresa la cantidad a vender.")
        else:
            messagebox.showerror("Error", "Por favor selecciona un producto.")

    def actualizar_lista_productos():
        listbox_productos.delete(0, tk.END)
        for producto in productos:
            info_producto = f"{producto['nombre']} - Precio: {producto['precio']} - Stock: {producto['stock']}"
            listbox_productos.insert(tk.END, info_producto)
    
    ventas_window = tk.Toplevel(master)
    ventas_window.title("Ventas")
    ventas_window.state('normal')
    ventas_window.attributes('-fullscreen', True)
    fondos.establecer_imagen_de_fondo(ventas_window, "fondoventa.png")

    def volver():
        ventas_window.destroy()
        subprocess.Popen(["python","main.py"])

    ventas_frame = tk.Frame(ventas_window, padx=20, pady=6, bg="#FED89B")
    ventas_frame.pack(anchor="center", pady=80)

    label_productos = tk.Label(ventas_frame, text="Productos Disponibles:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_productos.grid(row=0, column=0, sticky="w")

    listbox_productos = tk.Listbox(ventas_frame, width=50, height=10, font=("Times new roman", 12))
    listbox_productos.grid(row=1, column=0, padx=10, pady=10)

    label_cantidad = tk.Label(ventas_frame, text="Cantidad:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_cantidad.grid(row=2, column=0, sticky="w")

    entry_cantidad = tk.Entry(ventas_frame, font=("Times new roman", 14))
    entry_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    btn_vender = tk.Button(ventas_frame, text="Vender Producto", command=vender_producto, font=("Times new roman", 14), bg="#8F4B2C", fg="white")
    btn_vender.grid(row=4, columnspan=2, pady=20)

    label_usuario = tk.Label(ventas_frame, text=f"Bienvenido, {nombre_usuario} :)", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_usuario.grid(row=5, column=0, columnspan=2, pady=10)

    actualizar_lista_productos()

    btn_salir = tk.Button(ventas_frame, text="Salir", command=volver, font=("Times new roman", 14), fg="white", bg="#BE7250")
    btn_salir.grid(row=6, column=0, columnspan=2, pady=10)

