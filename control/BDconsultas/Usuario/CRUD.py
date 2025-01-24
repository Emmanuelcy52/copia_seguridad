import sqlite3
import bcrypt
from control.datos.datos import sesion
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

def obtener_empleados(id_excluir):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT id, nombre_real, nombre_usuario, tipo_usuario 
            FROM usuarios 
            WHERE id != ?
        ''', (id_excluir,))
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
            
def obtener_empleado_id(id):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM usuarios WHERE id = ?''',(id,))
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


def login(username,password):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM usuarios LIMIT 1''')
        resultado = cursor.fetchone()
        if resultado is None:
            return 'True'
        else:
            cursor.execute('''SELECT id,nombre_usuario,contrasena,tipo_usuario FROM usuarios WHERE nombre_usuario = ? ''',(username,))
            resultado_login = cursor.fetchone()
            
            if resultado_login:
                stored_hash = resultado_login[2]  # La contraseña encriptada de la base de datos
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    # La contraseña es correcta
                    sesion.iniciar_sesion(resultado_login[0], resultado_login[1], resultado_login[3])
                    return 'Exito'
                else:
                    return 'Error: Credenciales incorrectas'
            else:
                return 'Error: Usuario no encontrado'
            
        
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
            
def registro(nombreReal, nombreUsuario,contrasena,rol,codigoRecu):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        hashed_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute('''INSERT INTO usuarios (nombre_real, nombre_usuario, contrasena, tipo_usuario, codigo_empleado_recup) 
                          VALUES (?, ?, ?, ?, ?)''', 
                       (nombreReal, nombreUsuario, hashed_contrasena, rol, codigoRecu))

        # Confirmar la transacción
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se insertó el registro.'
        
    except sqlite3.Error as e:
        # Capturar errores de la base de datos
        print(f"Error al conectar o modificar la base de datos: {e}")
        conexion.rollback() 
        return (f"Error al conectar o modificar la base de datos: {e}")

    except Exception as e:
        # Capturar cualquier otro error
        print(f"Error inesperado: {e}")

    finally:
        # Asegurarse de cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()
            
            
def editar(nuevo_nombre, nuevo_nombre_usuario, nuevo_tipo, nueva_codigo, nueva_contraseña, id_usuario):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        contrasena_valida = ""
        
        cursor.execute('''SELECT contrasena FROM usuarios WHERE id = ? ''',(id_usuario,))
        resultado = cursor.fetchone()
            
        if resultado:
            stored_hash = resultado[0]  # La contraseña encriptada de la base de datos
            if bcrypt.checkpw(nueva_contraseña.encode('utf-8'), stored_hash):
                contrasena_valida=stored_hash
            else:
                contrasena_valida = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute('''
            UPDATE usuarios
            SET nombre_real = ?, nombre_usuario = ?, tipo_usuario = ?, codigo_empleado_recup = ?, contrasena = ?
            WHERE id = ?
        ''', (nuevo_nombre, nuevo_nombre_usuario, nuevo_tipo, nueva_codigo, contrasena_valida, id_usuario))
        
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
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''
            DELETE FROM usuarios WHERE id = ?
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
            
def crear_o_actualizar_respaldo(fecha_respaldo, fecha_proximo_respaldo, estado):
    try:
        # Ruta a la base de datos
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Intentar actualizar el registro existente
        cursor.execute('''
            UPDATE respaldo_datos
            SET fecha_respaldo = ?, 
                proximo_respaldo = ?, 
                estado_respaldo = ?
            WHERE id = 1
        ''', (fecha_respaldo, fecha_proximo_respaldo, estado))

        # Si no se actualizó ninguna fila, insertar un nuevo registro
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO respaldo_datos (id, fecha_respaldo, proximo_respaldo, estado_respaldo)
                VALUES (1, ?, ?, ?)
            ''', (fecha_respaldo, fecha_proximo_respaldo, estado))

        # Confirmar la transacción
        conexion.commit()

        return 'Exito'

    except sqlite3.Error as e:
        # Manejar errores de la base de datos
        print(f"Error en la base de datos: {e}")
        conexion.rollback()
        return f"Error en la base de datos: {e}"

    finally:
        # Cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()
            
def obtener_respaldo():
    try:
        # Ruta a la base de datos
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Obtener el único registro
        cursor.execute('SELECT * FROM respaldo_datos WHERE id = 1')
        respaldo = cursor.fetchone()

        return respaldo if respaldo else None

    except sqlite3.Error as e:
        # Manejar errores de la base de datos
        print(f"Error en la base de datos: {e}")
        return f"Error en la base de datos: {e}"

    finally:
        # Cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()