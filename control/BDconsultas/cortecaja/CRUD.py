import sqlite3

def obtener_corte_caja():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM corte_Caja''')
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
            
def obtener_dineroInical():
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        
        cursor.execute('''SELECT * FROM saldo_dia''')
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

def registrar_corte_caja(id_monto_inicial,fecha_corte,monto_inicial,ingresos,egresos,total_corte):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO corte_Caja (id_monto_inicial, fecha_corte, monto_inicial, ingresos, egresos, total_corte) VALUES (?,?,?,?,?,?)''', (id_monto_inicial,fecha_corte,monto_inicial,ingresos,egresos,total_corte))
        conexion.commit()

        # Verificar si se insertó al menos un registro
        if cursor.rowcount > 0:
            estado = 'corte ralizado'
            cursor.execute('''
            UPDATE saldo_dia
            SET estado = ? WHERE id = ?''', (estado,id_monto_inicial))
        
            conexion.commit()
            
            if cursor.rowcount > 0:
                return 'Exito'
            else:
                return 'Error: No se edito el proveedor.'
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

def obtener_ventas_corte(fecha):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM ventas WHERE fecha_venta = ?''',(fecha,))
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

def obtener_dinero_inicial(fecha):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT id,monto_inicial FROM saldo_dia WHERE fecha_dia = ?''',(fecha,))
        resultados = cursor.fetchone()
        if resultados:
            return resultados
        else:
            return False
        
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
            
def validad_corte(fecha):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT estado FROM saldo_dia WHERE fecha_dia = ?''',(fecha,))
        resultados = cursor.fetchone()
        if resultados:
            return resultados
        else:
            return False
        
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

def registrar_dinero_inicial(monto_inicial,fecha):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO saldo_dia (monto_inicial, fecha_dia) VALUES (?, ?)''', (monto_inicial, fecha))
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
            
def registrar_egreso_dinero(id_saldo_dia,monto_egresado,motivo_egreso,hora_egreso):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO egresos_caja (id_saldo_dia, monto_egresado, motivo_egreso, hora_egreso) VALUES (?, ?, ?, ?)''', (id_saldo_dia,monto_egresado,motivo_egreso,hora_egreso))
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
            
def obtener_egreso(id_saldo_dia):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM egresos_caja WHERE id_saldo_dia = ?''',(id_saldo_dia,))
        resultados = cursor.fetchall()
        if resultados:
            return resultados
        else:
            return False
        
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
            
def obtener_pagos(fecha):
    try:
        # Validar si la ruta del archivo existe
        ruta_db = "./modelo/punto_venta.db"

        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''SELECT * FROM pagos WHERE fecha_pago = ?''',(fecha,))
        resultados = cursor.fetchall()
        if resultados:
            return resultados
        else:
            return False
        
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