import os
import json
import pandas as pd
from kivy.app import App
from kivy.lang import Builder
from pathlib import Path
from kivy.uix.screenmanager import Screen
from control.datos.datos import sesion
from datetime import datetime
from control.BDconsultas.creacion.funciones_BD.funciones_BD import exportar_sql,insertar_producto_copia
from control.BDconsultas.inventario.CRUD import obtener_productos
from control.BDconsultas.ventas.CRUD import obtener_ventas,obtener_ventas_detalles
from control.BDconsultas.cortecaja.CRUD import obtener_corte_caja,obtener_dineroInical
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
import sys

# Función para obtener la ruta correcta según el entorno
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño', 'estadisticas.kv'))
Builder.load_file(kv_path)

class EstadisticasScreen(Screen):
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Verificar la ruta del escritorio según el sistema operativo
        self.configurar_ruta_escritorio()
        
        # Crear la carpeta puntoBackup si no existe
        self.carpeta_backup = os.path.join(self.escritorio, 'puntoBackup')
        if not os.path.exists(self.carpeta_backup):
            os.makedirs(self.carpeta_backup)
        
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)
        self.current_popup = None

    def configurar_ruta_escritorio(self):
        usuario_home = str(Path.home())
        # Verificar si el escritorio está en español o inglés
        escritorio_es = os.path.join(usuario_home, 'Escritorio')  # En español
        escritorio_en = os.path.join(usuario_home, 'Desktop')    # En inglés

        # Asignar la ruta del escritorio correcta dependiendo del sistema
        if os.path.exists(escritorio_es):
            self.escritorio = escritorio_es
        elif os.path.exists(escritorio_en):
            self.escritorio = escritorio_en
        else:
            print("No se pudo encontrar la carpeta de escritorio.")
            self.escritorio = None

    def on_enter(self):
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:
            if datos[2] != 'administrador':
                self.ids.empleadosRedig.disabled = True 
            else:
                self.ids.empleadosRedig.disabled = False
            self.ids.usuario.text = datos[1]
            self.id_usuario = datos[0]
        else:
            print("La sesión no está inicializada")

    def exportar_db(self):
        respuesta = exportar_sql()
        self.ids.message.text = f"{respuesta}."
        self.ids.message.color = (0, 1, 0, 1)  
        self.height_message = 10
        self.size_hint_x_menssage = 1
        self.size_hint_y_menssage = 0.4
        Clock.schedule_once(self.cerrarmensaje, 3)

    def exportar_productos(self):
        # Obtener los productos desde tu función obtener_productos()
        respuesta = obtener_productos()

        # Verificar si la respuesta tiene productos
        if not respuesta:
            print("No se encontraron productos para exportar.")
            return

        # Definir los nombres de las columnas
        columnas = [
            "id", "id_proveedor", "nombre_producto", "precio_publico", 
            "precio_compra", "precio_mayorista", "unidad_medida", 
            "cantidad_inventario", "cantidad_mayorista", "categoria", "codigo_barras"
        ]

        # Convertir la respuesta (lista de tuplas) en un DataFrame
        df_productos = pd.DataFrame(respuesta, columns=columnas)

        # Definir las rutas de los archivos en la carpeta de respaldo
        archivo_excel = os.path.join(self.carpeta_backup, 'productos.xlsx')
        archivo_json = os.path.join(self.carpeta_backup, 'productos_respaldo.json')

        # Exportar el DataFrame a un archivo Excel
        try:
            # Exportar a Excel
            df_productos.to_excel(archivo_excel, index=False, engine='openpyxl')
            print(f"Productos exportados exitosamente a {archivo_excel}.")

            # Exportar a JSON con formato de lista estándar
            df_productos.to_json(archivo_json, orient='records', indent=4, force_ascii=False)
            print(f"Respaldo de productos guardado exitosamente en {archivo_json}.")
            self.ids.message.text = f"Respaldo de productos en: {archivo_excel}."
            self.ids.message.color = (0, 1, 0, 1)  
            self.height_message = 10
            self.size_hint_x_menssage = 1
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)

        except Exception as e:
            print(f"Error al exportar los productos: {e}")
            
    def recuperar_productos(self):
        # Definir la ruta al archivo JSON
        archivo_json = os.path.join(self.carpeta_backup, 'productos_respaldo.json')
        print(archivo_json)
        
        try:
            # Intentar abrir y leer el archivo JSON
            with open(archivo_json, 'r') as file:
                productos = json.load(file)
                print(f"Productos leídos desde {archivo_json}.")

                # Insertar los productos en la base de datos
                for producto in productos:
                    idProducto = producto['id']
                    idProvedor = producto['id_proveedor']
                    nombre_producto = producto['nombre_producto']
                    precio_publico = producto['precio_publico']
                    precio_compra = producto['precio_compra']
                    precio_mayorista = producto['precio_mayorista']
                    unidad_medida = producto['unidad_medida']
                    cantidad_inventario = producto['cantidad_inventario']
                    cantidad_mayorista = producto['cantidad_mayorista']
                    categoria = producto['categoria']
                    codigo_barras = producto['codigo_barras']
                    insertar_producto_copia(idProvedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras)
                self.ids.message.text = "PRODUCTOS RESTAURADOS"
                self.ids.message.color = (0, 1, 0, 1)  
                self.height_message = 10
                self.size_hint_x_menssage = 0.5
                self.size_hint_y_menssage = 0.4
                Clock.schedule_once(self.cerrarmensaje, 3)
        
        except FileNotFoundError:
            print(f"El archivo {archivo_json} no se encuentra.")
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON. Asegúrate de que el formato sea correcto.")
        except Exception as e:
            print(f"Error al recuperar los productos: {e}")
            
    def exportar_ventas(self):
        # Obtener los datos de ventas y detalles de ventas
        ventas = obtener_ventas()
        ventasDetalles = obtener_ventas_detalles()

        # Verificar si los datos existen
        if not ventas:
            print("No se encontraron ventas para exportar.")
            return
        if not ventasDetalles:
            print("No se encontraron detalles de ventas para exportar.")
            return

        # Definir los nombres de las columnas
        columnas_ventas = [
            "id", "fecha_venta", "total", "dinero_recibido", 
            "cambio_devuelto", "cantidad_productos", "estatus", 
            "id_empleado"
        ]
        columnas_ventasDetalles = [
            "id", "id_venta", "id_producto", "cantidad_total", 
            "unidad_medida", "subtotal"
        ]

        # Convertir los datos a DataFrames
        df_ventas = pd.DataFrame(ventas, columns=columnas_ventas)
        df_ventas_detalles = pd.DataFrame(ventasDetalles, columns=columnas_ventasDetalles)

        # Definir la ruta del archivo de respaldo
        archivo_excel = os.path.join(self.carpeta_backup, 'ventas_respaldo.xlsx')

        # Exportar ambos DataFrames al mismo archivo Excel en la misma hoja
        try:
            with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                # Escribir "Ventas" a partir de la columna A
                df_ventas.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=0)
                
                # Escribir "Detalles de Ventas" a partir de la columna después de "Ventas"
                start_col = len(columnas_ventas) + 2  # Espacio de 2 columnas entre ambas tablas
                df_ventas_detalles.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=start_col)

            self.ids.message.text = f"Ventas y detalles exportados exitosamente a {archivo_excel}."
            self.ids.message.color = (0, 1, 0, 1)  
            self.height_message = 10
            self.size_hint_x_menssage = 1
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
        
        except Exception as e:
            print(f"Error al exportar las ventas: {e}")
            
    def exportar_cortes(self):
        # Obtener los datos de ventas y detalles de ventas
        corteCaja = obtener_corte_caja()
        DineroEncaja = obtener_dineroInical()

        # Verificar si los datos existen
        if not corteCaja:
            print("No se encontraron ventas para exportar.")
            return
        if not DineroEncaja:
            print("No se encontraron detalles de ventas para exportar.")
            return

        # Definir los nombres de las columnas
        columnas_corteCaja = [
            "id", "id_monto_inicial", "fecha_corte", "monto_inicial", 
            "ingresos", "egresos", "total_corte"
        ]
        columnas_DineroEncaja = [
            "id", "monto_inicial", "fecha_dia", "estado"
        ]

        # Convertir los datos a DataFrames
        df_ventas = pd.DataFrame(corteCaja, columns=columnas_corteCaja)
        df_ventas_detalles = pd.DataFrame(DineroEncaja, columns=columnas_DineroEncaja)

        # Definir la ruta del archivo de respaldo
        archivo_excel = os.path.join(self.carpeta_backup, 'cortecaja_respaldo.xlsx')

        # Exportar ambos DataFrames al mismo archivo Excel en la misma hoja
        try:
            with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                # Escribir "Ventas" a partir de la columna A
                df_ventas.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=0)
                
                # Escribir "Detalles de Ventas" a partir de la columna después de "Ventas"
                start_col = len(columnas_corteCaja) + 2  # Espacio de 2 columnas entre ambas tablas
                df_ventas_detalles.to_excel(writer, sheet_name="Ventas y Detalles", index=False, startrow=0, startcol=start_col)

            self.ids.message.text = f"corte de caja exportados exitosamente a {archivo_excel}."
            self.ids.message.color = (0, 1, 0, 1)  
            self.height_message = 10
            self.size_hint_x_menssage = 1
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
        
        except Exception as e:
            print(f"Error al exportar las ventas: {e}")
            
    def cerrar_sesion(self):
        sesion.cerrar_sesion()
        app = App.get_running_app()
        app.root.current = 'login'
        
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""   

    def actualizar_fecha_hora(self, *args):
        # Obtener la fecha y hora actual
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        # Actualizar el texto del Label con la fecha y hora
        self.ids.fecha_hora.text = ahora
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None

    def remove_popup(self, instance):
        """Limpia la referencia del popup sin modificar directamente el contenido."""
        if self.current_popup == instance:
            self.current_popup = None

    def redirect_productos(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'
        
    def redirect_Inventario(self, *args):
        app = App.get_running_app()
        app.root.current = 'inventario'
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_Proveedores(self, *args):
        app = App.get_running_app()
        app.root.current = 'proveedores'
        
    def redirect_clientes(self, *args):
        app = App.get_running_app()
        app.root.current = 'clientes'
