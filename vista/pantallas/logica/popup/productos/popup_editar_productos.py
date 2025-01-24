import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import random
from control.BDconsultas.proveedores.CRUD import obtener_proveedor_productos
from control.BDconsultas.inventario.CRUD import editar
from kivy.clock import Clock
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

# Obtén la ruta absoluta del archivo KV
kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño','popup','productos','editar_productos.kv'))
Builder.load_file(kv_path)

class EditarProductosScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    
    def __init__(self,origen=None, **kwargs):
        super().__init__(**kwargs)
        # Captura eventos de teclado
        self.proveedores = obtener_proveedor_productos()
        self.ids.proveedores.values = [proveedor[1] for proveedor in self.proveedores]
        self.origen = origen 
        Window.bind(on_key_down=self._on_key_down)
    
    def filtrar_proveedores(self, texto):
        # Filtra los proveedores según el texto ingresado
        texto = texto.lower()
        resultados_filtrados = [
            proveedor for proveedor in self.proveedores if texto in proveedor[1].lower()
        ]
        
        # Si no hay resultados, muestra un mensaje
        if not resultados_filtrados:
            resultados_filtrados = []
        
        # Actualiza el Spinner con los resultados filtrados
        self.ids.proveedores.values = [proveedor[1] for proveedor in resultados_filtrados]
        
    def calcular_ganacia(self, *args):
        try:
            # Obtener valores de los TextInput
            precio_venta = float(self.ids.precioPublico.text or 0)
            precio_compra = float(self.ids.precioCompra.text or 0)
            
            # Calcular ganancia
            ganancia = precio_venta - precio_compra

            # Actualizar el campo ganancia
            self.ids.ganancia.text = f"$ {ganancia:.2f}"
        except ValueError:
            # Manejar errores si no se ingresan números válidos
            self.ids.ganancia.text = "Error"
            
    def obtener_id_proveedor(self, nombre_seleccionado):
        for proveedor_id, proveedor_nombre in self.proveedores:
            if proveedor_nombre == nombre_seleccionado:
                return proveedor_id
        return None
    
    def obtener_nombre_proveedor(self,id_proveedor):
        for proveedor in self.proveedores:
            if proveedor[0] == id_proveedor:  
                return proveedor[1] 
        return f"No se encontró un proveedor con ID {id_proveedor}"
    
    def cargar_campos(self, productos_datos):
        id_producto,id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras = productos_datos
        proveedor_id = int(id_proveedor)
        nombre_proveedor = self.obtener_nombre_proveedor(proveedor_id)
        self.id_producto = id_producto
        self.ids.nombreProducto.text = nombre_producto
        self.ids.Stock.text = str(cantidad_inventario)
        self.ids.categoria.text = categoria
        self.ids.codigoBarras.text = codigo_barras
        self.ids.precioPublico.text = str(precio_publico)
        self.ids.precioCompra.text = str(precio_compra)
        self.ids.precioMayorista.text = str(precio_mayorista)
        self.ids.CantidadMayorista.text = str(cantidad_mayorista)
        self.ids.unidadMedida.text = unidad_medida
        self.ids.proveedores.text = nombre_proveedor
        
    def generar_codigo(self):
        numero = '0' + ''.join(str(random.randint(0, 9)) for _ in range(12))
        self.ids.codigoBarras.text = str(numero)
    
    def editar_producto(self):
        """Verifica las credenciales y navega a la pantalla principal si son correctas."""
        nombreProducto = self.ids.nombreProducto.text.lower()
        cantidad = self.ids.Stock.text
        categoria = self.ids.categoria.text.lower()
        codigoBarras = self.ids.codigoBarras.text
        precioPublico = self.ids.precioPublico.text
        precioCompra = self.ids.precioCompra.text
        precioMayorista = self.ids.precioMayorista.text
        CantidadMayorista = self.ids.CantidadMayorista.text
        unidadMedida = self.ids.unidadMedida.text
        proveedores = self.ids.proveedores.text 
        
        proveedor_id = self.obtener_id_proveedor(proveedores)
        
        # Validar que todos los campos estén llenos
        if not nombreProducto or not cantidad or not categoria or not codigoBarras or not precioPublico or not precioCompra or not precioMayorista or not CantidadMayorista:
            self.ids.message.text = "Llena todos los campos para continuar"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = 0.5
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return

        # Validar selección de unidad de medida o proveedor
        if unidadMedida == "Seleciona el Tipo de Medida" or proveedor_id is None:
            self.ids.message.text = "Tienes una selección inválida en unidad de medida o proveedor"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = 0.5
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return

        # Registrar producto con el ID del proveedor
        mensaje = editar(proveedor_id,nombreProducto, precioPublico, precioCompra, precioMayorista, unidadMedida, cantidad, CantidadMayorista, categoria, codigoBarras,self.id_producto)
        
        if mensaje == "Exito":
            # Mostrar mensaje de éxito
            self.ids.message.text = "¡Actualizacion completa! Redirigiendo..."
            self.ids.message.color = get_color_from_hex("#000000")
            self.height_message = 10
            self.size_hint_x_menssage=.6
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            # Retrasar 5 segundos antes de cambiar de pantalla
            Clock.schedule_once(self.redirect, 3)
        else:
        # Mostrar mensaje de error
            self.ids.message.text = mensaje
            self.height_message = 200
            self.size_hint_x_menssage=0.5
            self.size_hint_y_menssage=0.5
            Clock.schedule_once(self.cerrarmensaje, 3)
    
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""   
                    
    def redirect(self, *args):
        app = App.get_running_app()
        login_screen = app.root.get_screen('inventario')
        self.ids.message.text = ""
        login_screen.dismiss_popup()

    def _find_focusable_inputs(self, widget):
        """Recorre recursivamente para encontrar todos los TextInput."""
        focusable_widgets = []
        if isinstance(widget, TextInput):
            focusable_widgets.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                focusable_widgets.extend(self._find_focusable_inputs(child))
        return focusable_widgets

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 9:  # Código de la tecla Tab
            focusable_widgets = self._find_focusable_inputs(self)
            current_focus = next((widget for widget in focusable_widgets if widget.focus), None)
            if current_focus:
                # Buscar el siguiente input para enfocar
                current_index = focusable_widgets.index(current_focus)
                next_index = (current_index + 1) % len(focusable_widgets)  # Cicla al primero
                focusable_widgets[next_index].focus = True
            return True  # Consumir el evento
        return False