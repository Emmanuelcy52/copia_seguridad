import sqlite3
from pathlib import Path
import os
import sys

# Función para manejar rutas de recursos
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def exportar_sql():
    try:
        usuario_home = str(Path.home())
        escritorio_es = os.path.join(usuario_home, 'Escritorio')
        escritorio_en = os.path.join(usuario_home, 'Desktop')
        escritorio = escritorio_es if os.path.exists(escritorio_es) else escritorio_en
        if not escritorio:
            return "No se pudo encontrar la carpeta de escritorio."

        carpeta_backup = os.path.join(escritorio, 'puntoBackup')
        if not os.path.exists(carpeta_backup):
            os.makedirs(carpeta_backup)
            print(f"Carpeta creada en: {carpeta_backup}")

        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))
        if not os.path.exists(ruta_db):
            return f"El archivo de base de datos no existe en la ruta {ruta_db}."

        conexion = sqlite3.connect(ruta_db)
        archivo_exportado = os.path.join(carpeta_backup, "exportado.sql")
        with open(archivo_exportado, "w", encoding="utf-8") as archivo_sql:
            for linea in conexion.iterdump():
                archivo_sql.write(f"{linea}\n")
        return f"Base de datos exportada exitosamente a '{archivo_exportado}'."

    except sqlite3.Error as e:
        return f"Error al conectar o exportar la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

def insertar_producto_copia(idProvedor, nombre_producto, precio_publico, precio_compra, precio_mayorista, unidad_medida, cantidad_inventario, cantidad_mayorista, categoria, codigo_barras):
    try:
        ruta_db = resource_path(os.path.join("modelo", "punto_venta.db"))
        if not os.path.exists(ruta_db):
            return f"Base de datos no encontrada en {ruta_db}. Verifica la ruta."

        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        cursor.execute('''
            SELECT COUNT(*) 
            FROM productos 
            WHERE nombre_producto = ? AND codigo_barras = ?
        ''', (nombre_producto, codigo_barras))
        
        resultado = cursor.fetchone()
        if resultado[0] == 0:
            cursor.execute('''
                INSERT INTO productos (id_proveedor, nombre_producto, precio_publico, precio_compra, precio_mayorista, unidad_medida, cantidad_inventario, cantidad_mayorista, categoria, codigo_barras) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (idProvedor, nombre_producto, precio_publico, precio_compra, precio_mayorista, unidad_medida, cantidad_inventario, cantidad_mayorista, categoria, codigo_barras))
            conexion.commit()
            return f"Producto '{nombre_producto}' insertado exitosamente."
        else:
            return f"El producto '{nombre_producto}' ya existe. No se realizó la inserción."
    except sqlite3.Error as e:
        return f"Error al insertar el producto: {e}"
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
