import sqlite3

def registro(id_cliente,id_venta,monto_total,saldo_pendiente,fecha_inicio,fecha_vencimiento,estado):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO creditos (id_cliente,id_venta,monto_total,saldo_pendiente,fecha_inicio,fecha_vencimiento,estado) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (id_cliente,id_venta,monto_total,saldo_pendiente,fecha_inicio,fecha_vencimiento,estado))

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
            
def pagar_credito(id_credito,montoRestante,estatus):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        
        cursor.execute('''
            UPDATE creditos
            SET saldo_pendiente =?, estado =? WHERE id = ?
        ''', (montoRestante,estatus, id_credito))
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se edito el cliente.'
    
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
            
def registrar_pago(id_credito,fecha_pago,monto):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"
        metodo = 'Efectivo'

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO pagos (id_credito,fecha_pago,monto,metodo_pago) 
                          VALUES (?, ?, ?, ?)''', 
                       (id_credito,fecha_pago,monto,metodo))

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