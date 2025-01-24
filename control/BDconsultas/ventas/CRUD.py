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

def obtener_ventas():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM ventas''')
        resultados = cursor.fetchall()
        
        if resultados:
            return resultados
        else:
            return []
        
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
            
def obtener_ventas_detalles():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM detalles_ventas''')
        resultados = cursor.fetchall()
        
        if resultados:
            return resultados
        else:
            return []
        
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

def registrar_venta_efectivo(fecha_venta,total_compra,dinero_recibido,cambio_devuelto,productos_distintos,status,id_empleado):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO ventas (fecha_venta, total, dinero_recibido, cambio_devuelto, cantidad_productos, estatus, id_empleado) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (fecha_venta,total_compra, dinero_recibido, cambio_devuelto,productos_distintos,status,id_empleado))
        # Confirmar la transacción
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            # Obtener el ID de la fila recién insertada
            id_insertado = cursor.lastrowid
            return 'Exito', id_insertado
        else:
            return 'Error: No se insertó la venta.', None
        
    except sqlite3.Error as e:
        # Capturar errores de la base de datos
        print(f"Error al conectar o modificar la base de datos: {e}")
        return 'Error: Problema con la base de datos.', None

    except Exception as e:
        # Capturar cualquier otro error
        print(f"Error inesperado: {e}")
        return 'Error inesperado.', None

    finally:
        # Asegurarse de cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()

            
def registrar_venta_credito(fecha_venta,total_compra,dinero_recibido,cambio_devuelto,productos_distintos,status,id_empleado):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO ventas (fecha_venta, total, dinero_recibido, cambio_devuelto, cantidad_productos, estatus, id_empleado) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (fecha_venta,total_compra, dinero_recibido, cambio_devuelto,productos_distintos,status,id_empleado))
        # Confirmar la transacción
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            # Obtener el ID de la fila recién insertada
            id_insertado = cursor.lastrowid
            return 'Exito', id_insertado
        else:
            return 'Error: No se insertó la venta.', None
        
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
            
def registrar_detalles_venta(id_venta,id_producto,cantidad,unidad_medida,subtotal):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO detalles_ventas (id_venta, id_producto, cantidad_total, unidad_medida, subtotal) 
                          VALUES (?, ?, ?, ?, ?)''', 
                       (id_venta,id_producto,cantidad,unidad_medida,subtotal))
        # Confirmar la transacción
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se insertó la venta.'
        
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
            
def obtener_detalles_venta_id(id_venta):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT id_producto,cantidad_total,unidad_medida FROM detalles_ventas WHERE id_venta = ?''',(id_venta,))
        resultados = cursor.fetchall()
        
        if resultados:
            return resultados
        else:
            return []
        
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
            
def obtener_productos(id_venta):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT id_producto FROM detalles_ventas''')
        resultados = cursor.fetchall()
        
        if resultados:
            return resultados
        else:
            return []
        
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