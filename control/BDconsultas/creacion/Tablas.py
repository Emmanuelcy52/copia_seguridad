import sqlite3
import os
import sys

# Función para manejar rutas de recursos
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

def CrearTablas():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        print(f"Conexión establecida con la base de datos en: {ruta_db}")
        cursor = conexion.cursor()
        
        #crear una lista para almacenar todas las tablas y porder hacer mas facil su creacion y identificacion de cada una
        
        tablas = [
            '''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_real TEXT NOT NULL,
                nombre_usuario TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                tipo_usuario TEXT NOT NULL,
                codigo_empleado_recup TEXT NOT NULL
            )''',
            '''CREATE TABLE IF NOT EXISTS proveedores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_empresa TEXT NOT NULL,
                correo_electronico TEXT,
                telefono TEXT,
                direccion TEXT,
                notas TEXT 
            )''',
            '''CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_cliente TEXT NOT NULL,
                nombre_real TEXT NOT NULL,
                clave_lector TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                correo TEXT,
                nombre_refente TEXT NOT NULL,
                telefono_refente TEXT NOT NULL,
                direccion_refente TEXT NOT NULL,
                limite_credito REAL DEFAULT 0
            )''',
            '''CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_proveedor TEXT NOT NULL,
                nombre_producto TEXT NOT NULL,
                precio_publico REAL NOT NULL,
                precio_compra REAL NOT NULL,
                precio_mayorista REAL NOT NULL,
                unidad_medida TEXT NOT NULL,
                cantidad_inventario INTEGER NOT NULL,
                cantidad_mayorista INTEGER NOT NULL,
                categoria TEXT NOT NULL,
                codigo_barras TEXT NOT NULL,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS ventas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_venta TEXT NOT NULL,
                total REAL NOT NULL,
                dinero_recibido REAL NOT NULL,
                cambio_devuelto REAL NOT NULL,
                cantidad_productos NOT NULL,
                estatus TEXT DEFAULT 'completada',
                id_empleado INTEGER,
                FOREIGN KEY (id_empleado) REFERENCES usuarios(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS detalles_ventas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER,
                id_producto INTEGER,
                cantidad_total INTEGER NOT NULL,
                unidad_medida TEXT,
                subtotal REAL NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES ventas(id),
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS creditos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_venta INTEGER NOT NULL,
                monto_total REAL NOT NULL,
                saldo_pendiente REAL NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_vencimiento TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                FOREIGN KEY (id_venta) REFERENCES ventas(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_credito INTEGER NOT NULL,
                fecha_pago TEXT NOT NULL,
                monto REAL NOT NULL,
                metodo_pago TEXT DEFAULT 'efectivo',
                FOREIGN KEY (id_credito) REFERENCES creditos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS garantias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_unico TEXT NOT NULL,
                id_producto INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_vencimiento TEXT NOT NULL,
                tipo_garantia TEXT,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS reembolsos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                id_cliente INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha_solicitud TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                motivo TEXT,
                FOREIGN KEY (id_venta) REFERENCES ventas(id),
                FOREIGN KEY (id_producto) REFERENCES productos(id),
                FOREIGN KEY (id_cliente) REFERENCES clientes(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS detalles_reembolsos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_reembolso INTEGER NOT NULL,
                monto_pagado REAL NOT NULL,
                fecha_pago TEXT NOT NULL,
                metodo_pago TEXT DEFAULT 'efectivo',
                FOREIGN KEY (id_reembolso) REFERENCES reembolsos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                fecha_movimiento TEXT NOT NULL,
                descripcion TEXT,
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS historial_precios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                precio REAL NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS codigos_barras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                codigo REAL NOT NULL,
                ruta_codigo TEXT NOT NULL,
                FOREIGN KEY (id_producto) REFERENCES productos(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS saldo_dia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monto_inicial REAL NOT NULL,
                fecha_dia TEXT NOT NULL,
                estado TEXT DEFAULT 'Iniciado'
            )''',
            '''CREATE TABLE IF NOT EXISTS corte_Caja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_monto_inicial INTEGER NOT NULL,
                fecha_corte TEXT NOT NULL,
                monto_inicial REAL DEFAULT 0.0,
                ingresos REAL DEFAULT 0.0,
                egresos REAL DEFAULT 0.0,
                total_corte REAL NOT NULL,
                FOREIGN KEY (id_monto_inicial) REFERENCES saldo_dia(id)
            )''',
            '''CREATE TABLE IF NOT EXISTS egresos_caja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_saldo_dia INTEGER NOT NULL,
                monto_egresado REAL NOT NULL,
                motivo_egreso TEXT NOT NULL,
                hora_egreso TEXT NOT NULL,
                FOREIGN KEY (id_saldo_dia) REFERENCES saldo_dia(id))''',
                
            '''CREATE TABLE IF NOT EXISTS respaldo_datos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_respaldo TEXT NOT NULL,
                proximo_respaldo TEXT NOT NULL,
                estado_respaldo TEXT NOT NULL
                )'''
            ]
        for tabla in tablas:
             cursor.execute(tabla)
             print("tabla creada o ya existe.")
             
             
        # Confirmar los cambios
        conexion.commit()
        print("Todas la tablas creadas")

        

    except sqlite3.Error as e:
        # Capturar errores de la base de datos
        print(f"Error al conectar o modificar la base de datos: {e}")

    except Exception as e:
        # Capturar cualquier otro error
        print(f"Error inesperado: {e}")

    finally:
        # Asegurarse de cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()
            print("Conexión cerrada.")

# Llama a esta función al inicio del programa para inicializar la base
CrearTablas()