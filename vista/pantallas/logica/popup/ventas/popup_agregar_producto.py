import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from control.datos.datos_venta import venta
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
import sys

# Función para obtener la ruta correcta según el entorno
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)


kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño','popup','ventas','agregar_producto.kv'))
Builder.load_file(kv_path)

class AgregarProductoScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unidad_seleccionada = None
    
    def guardar_seleccion(self, spinner, texto_seleccionado):
        self.unidad_seleccionada = texto_seleccionado
    
    def cargar_producto(self, producto_datos,codigoBR):
        id,id_proveedor,nombre_producto,precio_publico,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista = producto_datos
        proveedor_id = int(id_proveedor)
        self.id_producto = int(id)
        if cantidad_inventario > 1:
            if unidad_medida == "Pieza":
                unidad_medida = "Piezas"
            elif unidad_medida == "Logitud":
                unidad_medida = "Metros"
            elif unidad_medida == "Peso":
                unidad_medida = "Kilos"
            cantidad_inventario_formateado = f"{cantidad_inventario} {unidad_medida}"
        else:
            if unidad_medida == "Logitud":
                unidad_medida = "Metro"
            elif unidad_medida == "Peso":
                unidad_medida = "Kilo"
            cantidad_inventario_formateado = f"{cantidad_inventario} {unidad_medida}"
        
        # Cambiar opciones del Spinner dinámicamente según la unidad de medida
        if unidad_medida.lower() in ["kilos", "kilo", "peso"]:
            self.ids.unidadMedida.values = ["kg", "g"]  # Opciones para Peso
        elif unidad_medida.lower() in ["metros", "metro", "logitud"]:
            self.ids.unidadMedida.values = ["m", "cm"]  # Opciones para Longitud
        elif unidad_medida.lower() in ["piezas", "pieza"]:
            self.ids.unidadMedida.values = ["Pieza"]  # Opciones para Piezas
        else:
            self.ids.unidadMedida.values = ["Otro"]
            
        self.unidadmedida=unidad_medida
        self.ids.codigoBarras.text = codigoBR
        self.ids.nombreProducto.text = nombre_producto
        self.ids.Stock.text = str(cantidad_inventario_formateado)
        self.ids.precioPublico.text = str(precio_publico)
        self.ids.precioMayorista.text = str(precio_mayorista)
        self.ids.CantidadMayorista.text = str(cantidad_mayorista)
        
    def validarCantidad(self):
    # Convertir las entradas de cantidad a números (por ejemplo, enteros o flotantes)
        try:
            cantidad_inventario = float(self.ids.Stock.text.split()[0])  
            cantidad_venta = float(self.ids.CantidadVenta.text)
        except ValueError:
            # Si no se puede convertir, muestra un error
            self.ids.message.text = "Cantidad inválida en el inventario o cantidad de venta."
            self.height_message = 200
            self.size_hint_x_menssage = .8
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return False
        
        if self.unidad_seleccionada is None:
            mensaje = (f"Selecciona el tipo de unidad de medida porfavor.")
            self.ids.message.text = mensaje
            self.height_message = 200
            self.size_hint_x_menssage = .8
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return False

        # Realizar conversiones según la unidad seleccionada
        if self.unidad_seleccionada:
            if self.unidad_seleccionada in ["g"]:  
                cantidad_inventario *= 1000  
            elif self.unidad_seleccionada in ["cm"]: 
                cantidad_inventario *= 100 

        # Validar si la cantidad de venta es mayor que la de inventario
        if cantidad_venta > cantidad_inventario:
            mensaje = (
                f"La cantidad de venta ({cantidad_venta} {self.unidad_seleccionada}) "
                f"no puede ser mayor a la cantidad del inventario ({cantidad_inventario} {self.unidad_seleccionada})."
            )
            self.ids.message.text = mensaje
            self.height_message = 200
            self.size_hint_x_menssage = .8
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return False
        else:
            return True


    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""
        
    def Agregar_producto(self):
        valido=self.validarCantidad()
        if valido == True: 
                
            datos_producto = {
                "codigoBarras": self.ids.codigoBarras.text,
                "nombreProducto": self.ids.nombreProducto.text,
                "Stock": self.ids.Stock.text,
                "precioPublico": self.ids.precioPublico.text,
                "precioMayorista": self.ids.precioMayorista.text,
                "CantidadMayorista": self.ids.CantidadMayorista.text,
                "CantidadVenta": self.ids.CantidadVenta.text,
                "id_producto": self.id_producto,
                "unidad_medida": self.unidad_seleccionada,
                
            }
            venta.agregar_venta(datos_producto)
            app = App.get_running_app()
            venta_screen = app.root.get_screen('home')
            self.ids.message.text = ""
            venta_screen.dismiss_popup()