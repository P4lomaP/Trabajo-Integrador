import tkinter as tk
from tkinter import messagebox, ttk
import fondos
import json_productos
import subprocess

def ventas(productos, nombre_usuario, master):
    def vender_producto():
        selected_item = treeview_productos.selection()
        if selected_item:
            producto_index = treeview_productos.index(selected_item[0])
            producto = productos[producto_index]
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
        for item in treeview_productos.get_children():
            treeview_productos.delete(item)
        for i, producto in enumerate(productos):
            treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock']))
    
    def filtrar_productos(event):
        filtro = search_var.get().lower()
        for item in treeview_productos.get_children():
            treeview_productos.delete(item)
        for i, producto in enumerate(productos):
            if filtro in producto['nombre'].lower():
                treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock']))

    
    ventas_window = tk.Toplevel(master)
    ventas_window.title("Ventas")
    ventas_window.state('normal')
    ventas_window.attributes('-fullscreen', True)
    fondos.establecer_imagen_de_fondo(ventas_window, "fondoventa.png")

    def volver():
        ventas_window.destroy()
        subprocess.Popen(["python","main.py"])

    ventas_frame = tk.Frame(ventas_window, padx=20, pady=6, bg="#FED89B")
    ventas_frame.pack(expand=True, fill=tk.BOTH)

    ventas_frame.grid_rowconfigure(0, weight=0)
    ventas_frame.grid_rowconfigure(1, weight=1)
    ventas_frame.grid_rowconfigure(2, weight=0)
    ventas_frame.grid_columnconfigure(0, weight=1)
    ventas_frame.grid_columnconfigure(1, weight=1)

    label_productos = tk.Label(ventas_frame, text="Productos Disponibles:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_productos.grid(row=0, column=0, sticky="w")

    search_label = tk.Label(ventas_frame, text="Buscar Producto:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    search_label.grid(row=0, column=1, sticky="e")

    search_var = tk.StringVar()
    search_bar = tk.Entry(ventas_frame, textvariable=search_var, font=("Times new roman", 14))
    search_bar.grid(row=0, column=2, padx=10, pady=10, sticky="e")
    search_bar.bind("<KeyRelease>", filtrar_productos)

    style = ttk.Style()
    style.configure("Treeview", font=("Times new roman", 14))
    style.configure("Treeview.Heading", font=("Times new roman", 14, "bold"))

    treeview_productos = ttk.Treeview(ventas_frame, columns=("nombre", "precio", "stock"), show="headings", height=20)
    treeview_productos.heading("nombre", text="Nombre")
    treeview_productos.heading("precio", text="Precio")
    treeview_productos.heading("stock", text="Stock")
    treeview_productos.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    treeview_productos.tag_configure('treeview', font=("Times new roman", 14))

    label_cantidad = tk.Label(ventas_frame, text="Cantidad:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_cantidad.grid(row=2, column=0, sticky="w")

    entry_cantidad = tk.Entry(ventas_frame, font=("Times new roman", 14))
    entry_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    btn_vender = tk.Button(ventas_frame, text="Vender Producto", command=vender_producto, font=("Times new roman", 14), bg="#8F4B2C", fg="white")
    btn_vender.grid(row=4, columnspan=3, pady=20)

    label_usuario = tk.Label(ventas_frame, text=f"Bienvenido, {nombre_usuario} :)", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_usuario.grid(row=5, column=0, columnspan=3, pady=10)

    actualizar_lista_productos()

    btn_salir = tk.Button(ventas_frame, text="Salir", command=volver, font=("Times new roman", 14), fg="white", bg="#BE7250")
    btn_salir.grid(row=6, column=0, columnspan=3, pady=10)

