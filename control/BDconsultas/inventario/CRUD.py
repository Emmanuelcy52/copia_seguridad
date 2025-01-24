import sqlite3
import bcrypt
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
            
def obtener_productos():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM productos''')
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
            
def obtener_producto_id(id):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM productos WHERE id = ?''',(id,))
        resultados = cursor.fetchone()
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
            
def obtener_producto_codigoBR(codigo_barras):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id,id_proveedor,nombre_producto,precio_publico,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista FROM productos WHERE codigo_barras = ?''',(codigo_barras,))
        resultados = cursor.fetchone()
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
            
def registro(id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO productos (id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras) 
                VALUES (?,?,?,?,?,?,?,?,?,?)''',(id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras))
        # Confirmar la transacción
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se registro el producto.'
            
        
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
            
def editar(id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras,id_producto):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''
            UPDATE productos
            SET id_proveedor = ?, nombre_producto = ?, precio_publico = ?, precio_compra = ?, precio_mayorista = ?, unidad_medida = ?, cantidad_inventario = ?, cantidad_mayorista = ?, categoria = ?, codigo_barras = ?
            WHERE id = ?
        ''', (id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras,id_producto))
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se edito el producto.'
    
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
            
def eliminar(id_producto):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''
            DELETE FROM productos WHERE id = ?
        ''', (id_producto,))
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se elimino el proveedor.'
    
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
            
def actualizarcantidad(idventa):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_producto,cantidad_total FROM detalles_ventas WHERE id_venta = ?''',(idventa,))
        resultados = cursor.fetchall()
        errores = []

        if resultados:
            for producto in resultados:
                id_producto, cantidad = producto
                cursor.execute('''SELECT cantidad_inventario FROM productos WHERE id = ?''', (id_producto,))
                result = cursor.fetchone()

                if result is None:
                    errores.append(f"Error: Producto con ID {id_producto} no encontrado.")
                    continue

                cantidad_inv_actual = float(result[0])
                cantidad_rest = float(cantidad)
                cantidad_nueva = cantidad_inv_actual - cantidad_rest

                cursor.execute('''UPDATE productos SET cantidad_inventario = ? WHERE id = ?''', (cantidad_nueva, id_producto))
                conexion.commit()

                if cursor.rowcount == 0:
                    errores.append(f"Error: Producto con ID {id_producto} no se actualizó correctamente.")

            if errores:
                return errores  # Devuelve una lista de errores para más claridad.
            else:
                return 'Exito'
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
            
def obtener_productos_bajos():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id_proveedor,nombre_producto,cantidad_inventario FROM productos WHERE cantidad_inventario <= 5''')
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