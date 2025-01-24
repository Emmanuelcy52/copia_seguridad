import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from control.BDconsultas.proveedores.CRUD import registro,editar
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

kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño','popup','proveedores','editar_proveedor.kv'))
Builder.load_file(kv_path)

class EditarProveedoresScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    
    def cargar_campos(self, datos_proveedor):
        id_proveedor, nombre, correo, telefono, direccion, notas = datos_proveedor
        self.id_proveedor = id_proveedor
        self.ids.nombreProveedor.text = nombre
        self.ids.correoElectronico.text = correo
        self.ids.Telefono.text = telefono
        self.ids.direccion.text = direccion
        self.ids.notasReferentes.text = notas
    
    def Editar_proveedor(self):
        """Verifica las credenciales y navega a la pantalla principal si son correctas."""
        nombreproveedor = self.ids.nombreProveedor.text.lower()
        correoElectronico = self.ids.correoElectronico.text.lower()
        Telefono= self.ids.Telefono.text
        direccion= self.ids.direccion.text
        notasReferentes = self.ids.notasReferentes.text.lower()
        # Validar que todos los campos estén llenos
        if not nombreproveedor or not correoElectronico or not Telefono or not direccion or not notasReferentes:
            self.ids.message.text = "Llena todos los campos para continuar"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        
        mensaje = editar(self.id_proveedor,nombreproveedor, correoElectronico, Telefono, direccion, notasReferentes)
        
        if mensaje == "Exito":
            # Mostrar mensaje de éxito
            self.ids.message.text = "¡Datos Guardados! SALIENDO..."
            self.ids.message.color = get_color_from_hex("#000000")  # Color verde
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            # Retrasar 5 segundos antes de cambiar de pantalla
            Clock.schedule_once(self.redirect_to_proveedores, 3)
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
                    
    def redirect_to_proveedores(self, *args):
        app = App.get_running_app()  # Obtén la instancia de la app
        proveedor_screen = app.root.get_screen('proveedores')  # Obtén la pantalla de login
        self.ids.message.text = ""  # Limpia el mensaje
        proveedor_screen.dismiss_popup()  # Cierra el popup si existe esta función
        
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Captura eventos de teclado
        Window.bind(on_key_down=self._on_key_down)

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