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

def registar_garantia(codigo,id_producto,fecha_ini,fecha_final,tipo_garantia):
    try:
        estado = "Activa"
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO garantias (codigo_unico,id_producto,fecha_inicio,fecha_vencimiento,tipo_garantia,estado) 
                       VALUES (?,?,?,?,?,?)''',(codigo,id_producto,fecha_ini,fecha_final,tipo_garantia,estado))
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se insertó el registro.'
        
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