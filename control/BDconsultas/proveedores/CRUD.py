import sqlite3
import bcrypt

def obtener_proveedor_productos():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM proveedores LIMIT 1''')
        resultado = cursor.fetchone()
        if resultado is None:
            Provedor='Sin proveedor'
            datos='sin datos'
            cursor.execute('''INSERT INTO proveedores (nombre_empresa,correo_electronico,telefono,direccion,notas) 
                           VALUES (?,?,?,?,?)''',(Provedor,datos,datos,datos,datos))
            # Confirmar la transacción
            conexion.commit()

            cursor.execute('''SELECT id, nombre_empresa FROM proveedores''')
            resultados = cursor.fetchall()

            return resultados if resultados else []
        
        else:
            cursor.execute('''SELECT id, nombre_empresa FROM proveedores''')
            resultados = cursor.fetchall()

            return resultados if resultados else []
            
        
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
            
def obtener_proveedores():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id, nombre_empresa, correo_electronico, telefono, direccion, notas FROM proveedores''')
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
            
def obtener_proveedor_id(id):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM proveedores WHERE id = ?''',(id,))
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
            
def registro(nombreproveedor, correoElectronico, Telefono, direccion, notasReferentes):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO proveedores (nombre_empresa,correo_electronico,telefono,direccion,notas) 
                VALUES (?,?,?,?,?)''',(nombreproveedor, correoElectronico, Telefono, direccion, notasReferentes))
        # Confirmar la transacción
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se registro el proveedor.'
            
        
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
            
def editar(id_proveedor,nuevo_nombre, nuevo_correo, nuevo_telefono, nueva_direccion, nuevas_notas):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''
            UPDATE proveedores
            SET nombre_empresa = ?, correo_electronico = ?, telefono = ?, direccion = ?, notas = ?
            WHERE id = ?
        ''', (nuevo_nombre, nuevo_correo, nuevo_telefono, nueva_direccion, nuevas_notas, id_proveedor))
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se edito el proveedor.'
    
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
            
def eliminar(id_proveedor):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''
            DELETE FROM proveedores WHERE id = ?
        ''', (id_proveedor,))
        
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