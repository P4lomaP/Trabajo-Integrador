import json
import uuid
from datetime import datetime

archivo_ventas = 'detalles_venta.json'

def cargar_registro():
    try:
        with open(archivo_ventas, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_registro(registro):
    with open(archivo_ventas, 'w') as file:
        json.dump(registro, file, indent=4)

def agregar_venta(nombre_usuario, carrito):
    registro = cargar_registro()
    venta = {
        'id': str(uuid.uuid4()),  
        'vendedor': nombre_usuario, 
        'detalles': [
            {
                'nombre': producto['nombre'],
                'cantidad_vendida': producto['cantidad_vendida'],
                'total': producto['total']
            } for producto in carrito
        ],
        'total_venta': sum(producto['total'] for producto in carrito),
        'fecha': datetime.now().strftime('%d-%m-%Y') 
    }
    
    registro.append(venta)
    guardar_registro(registro)
