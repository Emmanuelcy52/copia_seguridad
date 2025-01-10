import sqlite3

def registar_garantia(codigo,id_producto,fecha_ini,fecha_final,tipo_garantia):
    try:
        estado = "Activa"
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

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