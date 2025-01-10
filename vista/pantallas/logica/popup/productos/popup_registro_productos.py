import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from control.BDconsultas.proveedores.CRUD import obtener_proveedor_productos
from control.BDconsultas.inventario.CRUD import registro
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
import random
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty
from kivy.clock import Clock

kv_path = os.path.join(os.path.dirname(__file__), '..','..','..','diseño','popup','productos','registro_productos.kv')
Builder.load_file(kv_path)


class RegistroProductosScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'diseño', 'imagenes', 'icons'))
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proveedores = obtener_proveedor_productos()
        self.ids.proveedores.values = [proveedor[1] for proveedor in self.proveedores]
        
        # Captura eventos de teclado
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
            
    def generar_codigo(self):
        # Generar un número aleatorio de 13 dígitos
        numero = '0' + ''.join(str(random.randint(0, 9)) for _ in range(12))
        self.ids.codigoBarras.text = str(numero)
            
    def obtener_id_proveedor(self, nombre_seleccionado):
        for proveedor_id, proveedor_nombre in self.proveedores:
            if proveedor_nombre == nombre_seleccionado:
                return proveedor_id
        return None
            
    def Registar_producto(self):
        # Obtener datos de los campos
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

        # Obtener el ID del proveedor seleccionado
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
        mensaje = registro(proveedor_id,nombreProducto, precioPublico, precioCompra, precioMayorista, unidadMedida, cantidad, CantidadMayorista, categoria, codigoBarras)

        if mensaje == "Exito":
            self.ids.message.text = "¡Registro exitoso! Redirigiendo..."
            self.ids.message.color = (0, 1, 0, 1)  # Color verde
            self.height_message = 10
            self.size_hint_x_menssage = 0.5
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            Clock.schedule_once(self.redirect_to_inventario, 3)
        else:
            self.ids.message.text = mensaje
            self.height_message = 200
            self.size_hint_x_menssage = 0.5
            self.size_hint_y_menssage = 0.5
            Clock.schedule_once(self.cerrarmensaje, 3)
    
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""   
                    
    def redirect_to_inventario(self, *args):
        app = App.get_running_app()
        inventario_screen = app.root.get_screen('inventario')
        self.ids.message.text = ""
        inventario_screen.dismiss_popup()
        

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