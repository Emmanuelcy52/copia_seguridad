import sqlite3
import bcrypt
from control.datos.datos import sesion

def obtener_clientes():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT * FROM clientes
        ''')
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
            
            
def obtener_cliente_id(id):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM clientes WHERE id = ?''',(id,))
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
            
def obtener_deuda(id):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        estado = 'Pago a credito'
        cursor.execute('''SELECT id,monto_total,saldo_pendiente,fecha_inicio,fecha_vencimiento FROM creditos WHERE id_cliente = ? AND estado = ?''',(id,estado))
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
            
def obtener_cliente_datos(dato):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id FROM clientes WHERE codigo_cliente = ? or nombre_real = ? or telefono = ?''',(dato, dato, dato))
        resultados = cursor.fetchone()
        if resultados:
            id_cliente = resultados[0]
            return id_cliente
        else:
            return "Error"
        
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

def validar_credito(id, credito):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Usar el contexto 'with' para manejar la conexión y el cursor
        with sqlite3.connect(ruta_db) as conexion:
            cursor = conexion.cursor()

            # Verificar si el cliente tiene crédito suficiente
            cursor.execute('''SELECT limite_credito FROM clientes WHERE id = ?''', (id,))
            resultado = cursor.fetchone()

            if resultado:
                limite_credito = resultado[0]
                
                # Si el crédito solicitado es menor o igual al límite de crédito
                if credito <= limite_credito:
                    # Calcular el nuevo límite de crédito
                    nuevo_limite = limite_credito - credito
                    
                    # Actualizar el límite de crédito en la base de datos
                    cursor.execute('''UPDATE clientes SET limite_credito = ? WHERE id = ?''', (nuevo_limite, id))
                    conexion.commit()  # Confirmar los cambios en la base de datos

                    return True
                else:
                    print("El crédito solicitado excede el límite de crédito disponible.")
                    return False
            else:
                print("Cliente no encontrado.")
                return False

    except sqlite3.DatabaseError as e:
        print(f"Error al conectar o modificar la base de datos: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
            
def registro(codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO clientes (codigo_cliente, nombre_real, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente, limite_credito) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito))

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
            
            
def editar(codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito, id_cliente):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        contrasena_valida = ""
        
        cursor.execute('''
            UPDATE clientes
            SET codigo_cliente =?, nombre_real =?, clave_lector =?, telefono =?, direccion =?, correo =?, nombre_refente =?, telefono_refente =?, direccion_refente =?, limite_credito =?
            WHERE id = ?
        ''', (codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito, id_cliente))
        
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
            
def eliminar(id_cliente):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Verificar si el cliente tiene deudas
        cursor.execute('''SELECT monto_total FROM creditos WHERE id_cliente = ?''', (id_cliente,))
        resultados = cursor.fetchall()

        if resultados:  # Si hay deudas, devolver el mensaje con los montos
            deudas = [f"Deuda: ${monto[0]}" for monto in resultados]
            mensaje = "No se puede eliminar porque tiene deudas:\n" + "\n".join(deudas)
            return mensaje

        # Si no hay deudas, intentar eliminar el cliente
        cursor.execute('''
            DELETE FROM clientes WHERE id = ?
        ''', (id_cliente,))
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            return 'Exito'
        else:
            return 'Error: No se eliminó el cliente.'

    except sqlite3.Error as e:
        # Capturar errores de la base de datos
        print(f"Error al conectar o modificar la base de datos: {e}")
        return f"Error: {e}"

    except Exception as e:
        # Capturar cualquier otro error
        print(f"Error inesperado: {e}")
        return f"Error inesperado: {e}"

    finally:
        # Asegurarse de cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()
