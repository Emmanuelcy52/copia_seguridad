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

def registro(id_cliente,id_venta,monto_total,saldo_pendiente,fecha_inicio,fecha_vencimiento,estado):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

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
            
def pagar_credito(id_credito, montoRestante, estatus):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Obtener el saldo pendiente y el monto total del crédito
        cursor.execute('''
            SELECT monto_total, saldo_pendiente, id_cliente 
            FROM creditos 
            WHERE id = ?
        ''', (id_credito,))
        credito_info = cursor.fetchone()

        if credito_info:
            monto_total, saldo_pendiente, id_cliente = credito_info

            # Calcular el nuevo saldo pendiente
            nuevo_saldo_pendiente = montoRestante

            # Actualizar la tabla creditos
            cursor.execute('''
                UPDATE creditos 
                SET saldo_pendiente = ?, estado = ? 
                WHERE id = ?
            ''', (nuevo_saldo_pendiente, estatus, id_credito))

            # Verificar si la actualización fue exitosa
            if cursor.rowcount > 0:
                # Obtener el límite de crédito actual
                cursor.execute('SELECT limite_credito FROM clientes WHERE id = ?', (id_cliente,))
                limite_credito_actual = cursor.fetchone()[0]

                # Calcular el nuevo límite de crédito
                nuevo_limite_credito = limite_credito_actual + float(saldo_pendiente) - nuevo_saldo_pendiente

                # Actualizar el límite de crédito en la tabla clientes
                cursor.execute('''
                    UPDATE clientes 
                    SET limite_credito = ? 
                    WHERE id = ?
                ''', (nuevo_limite_credito, id_cliente))

                # Confirmar los cambios
                conexion.commit()

                return 'Exito'
            else:
                return 'Error: No se pudo actualizar el crédito.'
        else:
            return 'Error: Crédito no encontrado.'

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
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))
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