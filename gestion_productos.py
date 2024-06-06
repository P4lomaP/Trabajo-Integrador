import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import re
from tkcalendar import DateEntry
import fondos
import json_productos

def gestion_productos(productos, nombre_usuario, root):
    def agregar_producto():
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        stock = entry_stock.get()
        unidad = entry_unidad.get()
        fecha_vencimiento = entry_fecha_vencimiento.get_date()

        if nombre and precio and stock and unidad and fecha_vencimiento:
            try:
                precio = float(precio)
                stock = int(stock)
                if precio > 0 and stock >= 0:
                    if re.match("^[a-zA-Z\s]+$", nombre): 
                        nombres_existente = [producto['nombre'].lower() for producto in productos]
                        if nombre.lower() in nombres_existente:
                            messagebox.showerror("Error", "El nombre del producto ya existe.")
                        else:
                            fecha_vencimiento_str = fecha_vencimiento.strftime('%d-%m-%Y')
                            nuevo_producto = {"nombre": nombre, "precio": precio, "stock": stock, "unidad": unidad, "fecha_vencimiento": fecha_vencimiento_str}
                            productos.append(nuevo_producto)
                            json_productos.guardar_productos(productos)
                            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                            actualizar_lista_productos()
                    else:
                        messagebox.showerror("Error", "El nombre del producto solo puede contener letras y espacios.")
                else:
                    messagebox.showerror("Error", "Precio o stock no válidos.")
            except ValueError:
                messagebox.showerror("Error", "Precio o stock no válidos. Deben ser números positivos.")
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos.")

    def actualizar_lista_productos():
        for item in treeview_productos.get_children():
            treeview_productos.delete(item)
        for i, producto in enumerate(productos):
            treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock'], producto['unidad'], producto['fecha_vencimiento']))
    
    def eliminar_producto():
        selected_item = treeview_productos.selection()
        if selected_item:
            producto_index = treeview_productos.index(selected_item[0])
            confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este producto?")
            if confirmacion:
                del productos[producto_index]
                json_productos.guardar_productos(productos)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                actualizar_lista_productos()

    def modificar_producto():
        selected_item = treeview_productos.selection()
        if selected_item:
            producto_index = treeview_productos.index(selected_item[0])
            producto_modificar = productos[producto_index]
            nuevo_nombre = entry_nombre.get()
            nuevo_precio = entry_precio.get()
            nuevo_stock = entry_stock.get()
            nueva_unidad = entry_unidad.get()
            nueva_fecha_vencimiento = entry_fecha_vencimiento.get_date()

            if nuevo_nombre and nuevo_precio and nuevo_stock and nueva_unidad and nueva_fecha_vencimiento:
                try:
                    nuevo_precio = float(nuevo_precio)
                    nuevo_stock = int(nuevo_stock)
                    if nuevo_precio > 0 and nuevo_stock > 0:
                        if re.match("^[a-zA-Z\s]+$", nuevo_nombre):
                            fecha_vencimiento_str = nueva_fecha_vencimiento.strftime('%d-%m-%Y')
                            producto_modificar["nombre"] = nuevo_nombre
                            producto_modificar["precio"] = nuevo_precio
                            producto_modificar["stock"] = nuevo_stock
                            producto_modificar["unidad"] = nueva_unidad
                            producto_modificar["fecha_vencimiento"] = fecha_vencimiento_str
                            json_productos.guardar_productos(productos)
                            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                            actualizar_lista_productos()
                        else:
                            messagebox.showerror("Error", "El nombre del producto solo puede contener letras y espacios.")
                    else:
                        messagebox.showerror("Error", "El precio y la cantidad deben ser números positivos.")
                except ValueError:
                    messagebox.showerror("Error", "El precio y la cantidad deben ser números.")
            else:
                messagebox.showerror("Error", "Por favor completa todos los campos.")
    
    def filtrar_productos(event):
        filtro = search_var.get().lower()
        for item in treeview_productos.get_children():
            treeview_productos.delete(item)
        for i, producto in enumerate(productos):
            if filtro in producto['nombre'].lower():
                treeview_productos.insert('', 'end', iid=i, values=(producto['nombre'], producto['precio'], producto['stock'], producto['unidad'], producto['fecha_vencimiento']))

    def volver():
        gestion_window.destroy()
        subprocess.Popen(["python","main.py"])
    
    productos = json_productos.cargar_productos()

    gestion_window = tk.Toplevel(root)
    gestion_window.title("Gestión de Productos")
    gestion_window.state('normal')
    gestion_window.attributes('-fullscreen', True)

    fondo_path = "fondoge.png"
    fondos.establecer_imagen_de_fondo(gestion_window, fondo_path)

    gestion_frame = tk.Frame(gestion_window, padx=20, pady=6, bg="#FED89B")
    gestion_frame.pack(expand=True, fill=tk.BOTH)

    gestion_frame.grid_rowconfigure(0, weight=0)
    gestion_frame.grid_rowconfigure(1, weight=1)
    gestion_frame.grid_rowconfigure(2, weight=0)
    gestion_frame.grid_columnconfigure(0, weight=1)
    gestion_frame.grid_columnconfigure(1, weight=1)

    label_productos = tk.Label(gestion_frame, text="Gestión de Productos:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_productos.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

    search_label = tk.Label(gestion_frame, text="Buscar Producto:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    search_label.grid(row=0, column=3, sticky="e", padx=(0, 10), pady=(10, 5))

    search_var = tk.StringVar()
    search_bar = tk.Entry(gestion_frame, textvariable=search_var, font=("Times new roman", 14))
    search_bar.grid(row=0, column=4, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
    search_bar.bind("<KeyRelease>", filtrar_productos)

    treeview_frame = tk.Frame(gestion_frame, bg="#FED89B")
    treeview_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 5), sticky="nsew")

    style = ttk.Style()
    style.configure("Treeview", font=("Times new roman", 14))
    style.configure("Treeview.Heading", font=("Times new roman", 14, "bold"))

    treeview_productos = ttk.Treeview(treeview_frame, columns=("nombre", "precio", "stock", "unidad", "fecha_vencimiento"), show="headings", height=10)
    treeview_productos.heading("nombre", text="Nombre")
    treeview_productos.heading("precio", text="Precio")
    treeview_productos.heading("stock", text="Stock")
    treeview_productos.heading("unidad", text="Unidad")
    treeview_productos.heading("fecha_vencimiento", text="Fecha de Vencimiento")
    treeview_productos.pack(fill=tk.BOTH, expand=True)
    
    form_frame = tk.Frame(gestion_frame, padx=20, pady=6, bg="#FED89B")
    form_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=(10, 5), sticky="nsew")

    label_nombre = tk.Label(form_frame, text="Nombre:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_nombre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nombre = tk.Entry(form_frame, font=("Times new roman", 14))
    entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    label_precio = tk.Label(form_frame, text="Precio:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_precio.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_precio = tk.Entry(form_frame, font=("Times new roman", 14))
    entry_precio.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    label_stock = tk.Label(form_frame, text="Stock:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_stock.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_stock = tk.Entry(form_frame, font=("Times new roman", 14))
    entry_stock.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    label_unidad = tk.Label(form_frame, text="Unidad:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_unidad.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    unidades = ["Kilogramos", "Gramos", "Litros", "Mililitros", "Paquetes", "Otro"]

    entry_unidad = ttk.Combobox(form_frame, values=unidades, font=("Times new roman", 14), state="readonly")
    entry_unidad.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    entry_unidad.current(0)

    label_fecha_vencimiento = tk.Label(form_frame, text="Fecha de Vencimiento:", font=("Times new roman", 14, "bold"), bg="#FED89B")
    label_fecha_vencimiento.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    entry_fecha_vencimiento = DateEntry(form_frame, font=("Times new roman", 14), cal_bg="yellow", cal_fg="black", background="blue", foreground="white", borderwidth=2, selectbackground="violet", selectforeground="white", showweeknumbers=False, locale='es_ES', date_pattern='dd-mm-yyyy', state='readonly')
    entry_fecha_vencimiento.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    btn_eliminar = tk.Button(gestion_frame, text="Eliminar Producto", command=eliminar_producto,font=("Times new roman", 14),bg="#BE7250", fg="white")  
    btn_eliminar.grid(row=7, column=0, columnspan=3, pady=10)
    btn_modificar = tk.Button(gestion_frame, text="Modificar Producto", command=modificar_producto, font=("Times new roman", 14), bg="#BE7250", fg="white")  
    btn_modificar.grid(row=8, column=0, columnspan=3, pady=10)

    btn_volver = tk.Button(gestion_frame, text="Volver", command=volver, font=("Times new roman", 14), bg="#BE7250", fg="white")  
    btn_volver.grid(row=9, column=0, columnspan=3, pady=10)
    
    actualizar_lista_productos()

  