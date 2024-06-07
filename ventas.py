import tkinter as tk
from tkinter import messagebox, ttk
import fondos
import json_productos
import subprocess

def ventas(productos, nombre_usuario, master):
    carrito = []

    def vender_producto():
        selected_item = treeview_productos.selection()
        if selected_item:
            producto_index = treeview_productos.index(selected_item[0])
            producto = productos[producto_index]
            cantidad_vendida = entry_cantidad.get()
            if cantidad_vendida:
                try:
                    cantidad_vendida = int(cantidad_vendida)
                    if 0 < cantidad_vendida <= producto["stock"]:
                        producto_vendido = producto.copy()
                        producto_vendido["cantidad_vendida"] = cantidad_vendida
                        producto_vendido["total"] = producto_vendido["precio"] * cantidad_vendida
                        carrito.append(producto_vendido)
                        producto["stock"] -= cantidad_vendida
                        json_productos.guardar_productos(productos)
                        messagebox.showinfo("Éxito", f"Se añadieron {cantidad_vendida} unidades de {producto['nombre']} al carrito.")
                        actualizar_lista_productos()
                        actualizar_carrito()
                    else:
                        messagebox.showerror("Error", "La cantidad ingresada no es válida.")
                except ValueError:
                    messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            else:
                messagebox.showerror("Error", "Por favor ingresa la cantidad a vender.")
        else:
            messagebox.showerror("Error", "Por favor selecciona un producto.")

    def actualizar_lista_productos():
        treeview_productos.delete(*treeview_productos.get_children())
        for i, producto in enumerate(productos):
            treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock'], producto['unidad'], producto['fecha_vencimiento']))

    def actualizar_carrito():
        listbox_carrito.delete(0, 'end')
        for producto in carrito:
            listbox_carrito.insert('end', f"{producto['nombre']} - Cantidad: {producto['cantidad_vendida']} - Total: {producto['total']}")
    
    def filtrar_productos(event):
        filtro = search_var.get().lower()
        for item in treeview_productos.get_children():
            treeview_productos.delete(item)
        for i, producto in enumerate(productos):
            if filtro in producto['nombre'].lower():
                treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock'], producto['unidad'], producto['fecha_vencimiento']))
    
    def comprar():
        if carrito:
            total_compra = sum(item['total'] for item in carrito)
            detalles_compra = "\n".join([f"{item['nombre']} - Cantidad: {item['cantidad_vendida']} - Total: {item['total']}" for item in carrito])
            messagebox.showinfo("Detalles de la Compra", f"Nombre del Cliente: {nombre_usuario}\n\nDetalles de la Compra:\n{detalles_compra}\n\nTotal de la Compra: {total_compra}")
            carrito.clear()
            actualizar_carrito()
        else:
            messagebox.showwarning("Carrito Vacío", "El carrito de compras está vacío.")

    def eliminar_del_carrito():
        selected_item = listbox_carrito.curselection()
        if selected_item:
            index = selected_item[0]
            producto_eliminado = carrito.pop(index)
            producto_nombre = producto_eliminado['nombre']
            for producto in productos:
                if producto['nombre'] == producto_nombre:
                    producto['stock'] += producto_eliminado['cantidad_vendida']
                    break
            json_productos.guardar_productos(productos)
            messagebox.showinfo("Éxito", f"Se eliminó {producto_nombre} del carrito.")
            actualizar_carrito()
            actualizar_lista_productos()
        else:
            messagebox.showerror("Error", "Por favor selecciona un producto del carrito para eliminar.")

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
    label_productos.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

    search_label = tk.Label(ventas_frame, text="Buscar Producto:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    search_label.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=(10, 5))

    search_var = tk.StringVar()
    search_bar = tk.Entry(ventas_frame, textvariable=search_var, font=("Times new roman", 14))
    search_bar.grid(row=0, column=4, columnspan=2, padx=(0, 10), pady=(10, 5), sticky="ew")
    search_bar.bind("<KeyRelease>", filtrar_productos)

    treeview_frame = tk.Frame(ventas_frame, bg="#FED89B")
    treeview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="nsew")

    style = ttk.Style()
    style.configure("Treeview", font=("Times new roman", 14))
    style.configure("Treeview.Heading", font=("Times new roman", 14, "bold"))

    vsb = ttk.Scrollbar(treeview_frame, orient="vertical")
    vsb.pack(side='right', fill='y')
    hsb = ttk.Scrollbar(treeview_frame, orient="horizontal")
    hsb.pack(side='bottom', fill='x')

    treeview_productos = ttk.Treeview(treeview_frame, columns=("nombre", "precio", "stock", "unidad", "fecha_vencimiento"), show="headings", height=10, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=treeview_productos.yview)
    hsb.config(command=treeview_productos.xview)

    treeview_productos.heading("nombre", text="Nombre")
    treeview_productos.heading("precio", text="Precio")
    treeview_productos.heading("stock", text="Stock")
    treeview_productos.heading("unidad", text="Unidad")
    treeview_productos.heading("fecha_vencimiento", text="Fecha de Vencimiento")
    treeview_productos.pack(fill=tk.BOTH, expand=True)

    carrito_frame = tk.Frame(ventas_frame, padx=20, pady=6, bg="#FED89B")
    carrito_frame.grid(row=1, column=2, columnspan=4, rowspan=2, padx=10, pady=(0, 5), sticky="nsew")

    label_cartel = tk.Label(carrito_frame, text="Carrito de Compras:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_cartel.pack(side="top", fill="both", expand=True)

    listbox_carrito = tk.Listbox(carrito_frame, font=("Times new roman", 14), width=40, height=10)
    listbox_carrito.pack(fill="both", expand=True)

    btn_comprar = tk.Button(carrito_frame, text="Comprar", command=comprar, font=("Times new roman", 14), fg="white", bg="#8F4B2C")
    btn_comprar.pack(side="bottom", padx=10, pady=(0, 10))

    btn_eliminar = tk.Button(carrito_frame, text="Eliminar del Carrito", command=eliminar_del_carrito, font=("Times new roman", 14), bg="#8F4B2C", fg="white")
    btn_eliminar.pack(side="bottom", padx=10, pady=(5, 0))

    entry_frame = tk.Frame(ventas_frame, bg="#FED89B")
    entry_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

    label_cantidad = tk.Label(entry_frame, text="Cantidad:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_cantidad.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_cantidad = tk.Entry(entry_frame, font=("Times new roman", 14))
    entry_cantidad.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    btn_vender = tk.Button(entry_frame, text="Añadir al Carrito", command=vender_producto, font=("Times new roman", 14), bg="#8F4B2C", fg="white")
    btn_vender.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    btn_salir = tk.Button(entry_frame, text="Salir", command=volver, font=("Times new roman", 14), fg="white", bg="#BE7250")
    btn_salir.grid(row=0, column=4, padx=10, pady=10, sticky="e")

    entry_frame = tk.Frame(ventas_frame, bg="#FED89B")
    entry_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

    label_cantidad = tk.Label(entry_frame, text="Cantidad:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_cantidad.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_cantidad = tk.Entry(entry_frame, font=("Times new roman", 14))
    entry_cantidad.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    btn_vender = tk.Button(entry_frame, text="Añadir al Carrito", command=vender_producto, font=("Times new roman", 14), bg="#8F4B2C", fg="white")
    btn_vender.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    btn_salir = tk.Button(entry_frame, text="Volver", command=volver, font=("Times new roman", 14), fg="white", bg="#BE7250")
    btn_salir.grid(row=0, column=4, padx=10, pady=10, sticky="e")

    actualizar_lista_productos()