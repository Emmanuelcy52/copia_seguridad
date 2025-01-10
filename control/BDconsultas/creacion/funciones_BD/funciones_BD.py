import sqlite3
import os
from pathlib import Path

def exportar_sql():
    try:
        # Obtener la ruta del escritorio del usuario
        usuario_home = str(Path.home())
        escritorio_es = os.path.join(usuario_home, 'Escritorio')  # En español
        escritorio_en = os.path.join(usuario_home, 'Desktop')    # En inglés
        
        # Asignar la ruta del escritorio correcta dependiendo del sistema
        if os.path.exists(escritorio_es):
            escritorio = escritorio_es
        elif os.path.exists(escritorio_en):
            escritorio = escritorio_en
        else:
            return "No se pudo encontrar la carpeta de escritorio."

        # Crear la carpeta puntoBackup si no existe
        carpeta_backup = os.path.join(escritorio, 'puntoBackup')
        if not os.path.exists(carpeta_backup):
            os.makedirs(carpeta_backup)

        # Ruta del archivo de base de datos
        ruta_db = "./modelo/punto_venta.db"
        
        # Verificar si la base de datos existe
        if not os.path.exists(ruta_db):
            mensaje = f"El archivo de base de datos no existe en la ruta {ruta_db}."
            return mensaje
        
        # Conectar a la base de datos
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Ruta para guardar el archivo exportado
        archivo_exportado = os.path.join(carpeta_backup, "exportado.sql")

        # Generar el script SQL de la base de datos
        with open(archivo_exportado, "w") as archivo_sql:
            for linea in conexion.iterdump():
                archivo_sql.write(f"{linea}\n")
        
        mensaje = f"Base de datos exportada exitosamente a '{archivo_exportado}'."
        return mensaje

    except sqlite3.Error as e:
        # Capturar errores de la base de datos
        mensaje = f"Error al conectar o exportar la base de datos: {e}"
        return mensaje

    except Exception as e:
        # Capturar cualquier otro error
        mensaje = f"Error inesperado: {e}"
        return mensaje

    finally:
        # Asegurarse de cerrar la conexión
        if 'conexion' in locals() and conexion:
            conexion.close()


def insertar_producto_copia(idProvedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras):
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect('./modelo/punto_venta.db')
        cursor = conexion.cursor()

        # Verificar si el producto ya existe en la base de datos
        cursor.execute('''
            SELECT COUNT(*) 
            FROM productos 
            WHERE nombre_producto = ? AND codigo_barras = ?
        ''', (nombre_producto, codigo_barras))
        
        resultado = cursor.fetchone()
        
        if resultado[0] == 0:  # No se encontraron coincidencias
            # Preparar e insertar el nuevo producto
            cursor.execute('''
                INSERT INTO productos (id_proveedor, nombre_producto, precio_publico, precio_compra, precio_mayorista, unidad_medida, cantidad_inventario, cantidad_mayorista, categoria, codigo_barras) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (idProvedor, nombre_producto, precio_publico, precio_compra, precio_mayorista, unidad_medida, cantidad_inventario, cantidad_mayorista, categoria, codigo_barras))
            
            # Confirmar la transacción
            conexion.commit()
            print(f"Producto '{nombre_producto}' con código de barras '{codigo_barras}' insertado exitosamente.")
        else:
            print(f"El producto '{nombre_producto}' con código de barras '{codigo_barras}' ya existe en la base de datos. No se realizó la inserción.")
    
    except sqlite3.Error as e:
        print(f"Error al insertar el producto en la base de datos: {e}")
    
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()