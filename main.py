import tkinter as tk
from tkinter import messagebox
import re
import lista_empleados
import lista_productos
import gestion_productos
import fondos
import gestion_ventas
import subprocess

def volver_gestion():
    subprocess.Popen(["python","gestion_productos.py"])

def volver_ventas():
    subprocess.Popen(["python","ventas.py"])

def iniciar_sesion():
    nombre_usuario = entry_usuario.get()
    contraseña = entry_password.get()
    if not re.match("^[a-zA-Z\s]+$", nombre_usuario):
        messagebox.showerror("Error", "El nombre de usuario solo puede contener letras y espacios.")
        return
    if nombre_usuario and contraseña:
        categoria = seleccion_categoria.get()
        if categoria:
            usuarios = lista_empleados.cargar_empleados()
            usuario_encontrado = False
            for usuario in usuarios:
                if usuario["usuario"] == nombre_usuario:
                    usuario_encontrado = True
                    if usuario["categoria"] != categoria:
                        messagebox.showerror("Error", f"El usuario '{nombre_usuario}' ya está categorizado como '{usuario['categoria']}'.")
                        return
                    if usuario.get("contrasena") == contraseña:
                        root.withdraw()
                        if categoria == "Ventas":
                            productos = lista_productos.cargar_productos()
                            gestion_ventas.gestion_ventas(productos, nombre_usuario, root)
                        else:
                            productos = lista_productos.cargar_productos()
                            gestion_productos.gestion_productos(productos, nombre_usuario, root)
                        return
            if not usuario_encontrado and guardar_usuario_var.get():
                verificar_usuario(nombre_usuario, categoria, contraseña)
                messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
                root.withdraw()
                if categoria == "Ventas":
                    productos = lista_productos.cargar_productos()
                    gestion_ventas.gestion_ventas(productos, nombre_usuario, root)
                else:
                    productos = lista_productos.cargar_productos()
                    gestion_productos.gestion_productos(productos, nombre_usuario, root)
                return
            elif not usuario_encontrado:
                messagebox.showerror("Error", "El usuario no está registrado.")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "Por favor selecciona una categoría.")
    else:
        messagebox.showerror("Error", "Por favor ingresa tu nombre de usuario y contraseña.")

def verificar_usuario(usuario, categoria, contraseña):
    usuarios = lista_empleados.cargar_empleados()
    usuario_existente = False

    for u in usuarios:
        if u["usuario"] == usuario:
            usuario_existente = True
            break

    if not usuario_existente:
        usuarios.append({"usuario": usuario, "categoria": categoria, "contrasena": contraseña})
        lista_empleados.guardar_empleados(usuarios)

def salir():
    root.destroy()

root = tk.Tk()
root.title("Inicio de Sesión")
root.state('normal')
root.attributes('-fullscreen', True)

frame_login = tk.Frame(root, padx=5, pady=5)
frame_login.pack()
fondos.establecer_imagen_de_fondo(root, "fondofinal.png")
productos = lista_productos.cargar_productos()

login_frame = tk.LabelFrame(root, text="Inicio de Sesión", font=("Times new roman", 12, "bold"), padx=20, pady=20, bg="#FFCD98")
login_frame.pack(padx=20, pady=200)

label_usuario = tk.Label(login_frame, text="Nombre de Usuario:", font=("Times new roman", 14), bg="#FFCD98")
label_usuario.grid(row=0, column=0, sticky="e")
entry_usuario = tk.Entry(login_frame, font=("Times new roman", 14))
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(login_frame, text="Contraseña:", font=("Times new roman", 14), bg="#FFCD98")
label_password.grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(login_frame, show="*", font=("Times new roman", 14))
entry_password.grid(row=1, column=1, padx=10, pady=5)

label_info = tk.Label(login_frame, text="Por favor elija una categoría para continuar:", font=("Times new roman", 14), bg="#FFCD98")
label_info.grid(row=2, column=0, columnspan=2, pady=5)

seleccion_categoria = tk.StringVar()

radiobutton_gestion = tk.Radiobutton(login_frame, text="Gestión de Productos", variable=seleccion_categoria, value="Gestion", font=("Times new roman", 14), bg="#FFCD98")
radiobutton_gestion.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

radiobutton_ventas = tk.Radiobutton(login_frame, text="Ventas", variable=seleccion_categoria, value="Ventas", font=("Times new roman", 14), bg="#FFCD98")
radiobutton_ventas.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

guardar_usuario_var = tk.BooleanVar()
check_guardar_usuario = tk.Checkbutton(login_frame, text="Guardar Usuario", variable=guardar_usuario_var, font=("Times new roman", 14), bg="#FFCD98")
check_guardar_usuario.grid(row=5, column=0, columnspan=2, pady=5)

btn_continuar = tk.Button(login_frame, text="Continuar", command=iniciar_sesion, font=("Times new roman", 14), fg="white", bg="#BE7250")
btn_continuar.grid(row=6, column=0, columnspan=2, pady=10)

btn_salir = tk.Button(login_frame, text="Salir", command=salir, font=("Times new roman", 14), fg="white", bg="#BE7250")
btn_salir.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
