import os
import json
import pandas as pd
from pathlib import Path
from control.datos.datos import sesion
from datetime import datetime
from control.BDconsultas.creacion.funciones_BD.funciones_BD import exportar_sql, insertar_producto_copia
from control.BDconsultas.inventario.CRUD import obtener_productos
from control.BDconsultas.ventas.CRUD import obtener_ventas, obtener_ventas_detalles
from control.BDconsultas.cortecaja.CRUD import obtener_corte_caja, obtener_dineroInical
from kivy.clock import Clock

def configurar_ruta_escritorio():
    usuario_home = str(Path.home())
    escritorio_es = os.path.join(usuario_home, 'Escritorio')
    escritorio_en = os.path.join(usuario_home, 'Desktop')

    if os.path.exists(escritorio_es):
        return escritorio_es
    elif os.path.exists(escritorio_en):
        return escritorio_en
    else:
        return None

def configurar_backup():
    escritorio = configurar_ruta_escritorio()
    if escritorio:
        carpeta_backup = os.path.join(escritorio, 'puntoBackup')
        if not os.path.exists(carpeta_backup):
            os.makedirs(carpeta_backup)
        return carpeta_backup
    else:
        return None

def exportar_db():
    respuesta = exportar_sql()  # Supongamos que esta función devuelve un mensaje
    if "exitosamente" in respuesta:  # Verificamos si "exitosamente" está en la respuesta
        return "Exito"
    else:
        return "La exportación falló"

def exportar_productos():
    respuesta = obtener_productos()

    if not respuesta:
        return "No se encontraron productos para exportar."

    columnas = [
        "id", "id_proveedor", "nombre_producto", "precio_publico", 
        "precio_compra", "precio_mayorista", "unidad_medida", 
        "cantidad_inventario", "cantidad_mayorista", "categoria", "codigo_barras"
    ]

    df_productos = pd.DataFrame(respuesta, columns=columnas)

    carpeta_backup = configurar_backup()
    if not carpeta_backup:
        return "No se pudo configurar la carpeta de respaldo."

    archivo_excel = os.path.join(carpeta_backup, 'productos.xlsx')
    archivo_json = os.path.join(carpeta_backup, 'productos_respaldo.json')

    try:
        df_productos.to_excel(archivo_excel, index=False, engine='openpyxl')
        df_productos.to_json(archivo_json, orient='records', indent=4, force_ascii=False)
        return "Exito"
    except Exception as e:
        return f"Error al exportar los productos: {e}"

def exportar_ventas():
    ventas = obtener_ventas()
    ventasDetalles = obtener_ventas_detalles()

    if not ventas:
        return "No se encontraron ventas para exportar."
    if not ventasDetalles:
        return "No se encontraron detalles de ventas para exportar."

    columnas_ventas = [
        "id", "fecha_venta", "total", "dinero_recibido", 
        "cambio_devuelto", "cantidad_productos", "estatus", 
        "id_empleado"
    ]
    columnas_ventasDetalles = [
        "id", "id_venta", "id_producto", "cantidad_total", 
        "unidad_medida", "subtotal"
    ]

    df_ventas = pd.DataFrame(ventas, columns=columnas_ventas)
    df_ventas_detalles = pd.DataFrame(ventasDetalles, columns=columnas_ventasDetalles)

    carpeta_backup = configurar_backup()
    if not carpeta_backup:
        return "No se pudo configurar la carpeta de respaldo."

    archivo_excel = os.path.join(carpeta_backup, 'ventas_respaldo.xlsx')

    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
            df_ventas.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=0)
            start_col = len(columnas_ventas) + 2
            df_ventas_detalles.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=start_col)
        return "Exito"
    except Exception as e:
        return f"Error al exportar las ventas: {e}"

def exportar_cortes():
    corteCaja = obtener_corte_caja()
    DineroEncaja = obtener_dineroInical()

    if not corteCaja:
        return "No se encontraron cortes de caja para exportar."
    if not DineroEncaja:
        return "No se encontraron detalles de dinero inicial para exportar."

    columnas_corteCaja = [
        "id", "id_monto_inicial", "fecha_corte", "monto_inicial", 
        "ingresos", "egresos", "total_corte"
    ]
    columnas_DineroEncaja = [
        "id", "monto_inicial", "fecha_dia", "estado"
    ]

    df_corteCaja = pd.DataFrame(corteCaja, columns=columnas_corteCaja)
    df_DineroEncaja = pd.DataFrame(DineroEncaja, columns=columnas_DineroEncaja)

    carpeta_backup = configurar_backup()
    if not carpeta_backup:
        return "No se pudo configurar la carpeta de respaldo."

    archivo_excel = os.path.join(carpeta_backup, 'cortecaja_respaldo.xlsx')

    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
            df_corteCaja.to_excel(writer, sheet_name="Cortes de Caja", index=False, startrow=0, startcol=0)
            start_col = len(columnas_corteCaja) + 2
            df_DineroEncaja.to_excel(writer, sheet_name="Cortes de Caja", index=False, startrow=0, startcol=start_col)
        return "Exito"
    except Exception as e:
        return f"Error al exportar los cortes: {e}"