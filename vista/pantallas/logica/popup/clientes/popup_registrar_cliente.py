import os
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from control.BDconsultas.clientes.CRUD import registro
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

# Obtén la ruta absoluta del archivo KV
kv_path = os.path.join(os.path.dirname(__file__), '..','..','..','diseño','popup','clientes','registrar_clientes.kv')
Builder.load_file(kv_path)

class RegistroCientesScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'diseño', 'imagenes', 'icons'))
    )
    
    def Registar_cliente(self):
        """Verifica las credenciales y navega a la pantalla principal si son correctas."""
        codigoCliente = self.ids.codigoCliente.text.lower()
        nombreReal = self.ids.nombreReal.text.lower()
        clave_lector = self.ids.clave_lector.text.lower()
        telefono= self.ids.telefono.text.lower()
        direccion= self.ids.direccion.text.lower()
        correo = self.ids.correo.text.lower()
        nombre_refente = self.ids.nombre_refente.text.lower()
        telefono_refente= self.ids.telefono_refente.text.lower()
        direccion_refente= self.ids.direccion_refente.text.lower()
        credito_aprovado = self.ids.credito_aprovado.text
        # Validar que todos los campos estén llenos
        if not nombreReal or not clave_lector or not telefono or not direccion or not credito_aprovado or not nombre_refente or not telefono_refente or not direccion_refente:
            self.ids.message.text = "Llena todos los campos para continuar"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        
        mensaje = registro(codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,credito_aprovado)
        
        if mensaje == "Exito":
            # Mostrar mensaje de éxito
            self.ids.message.text = "¡Registro exitoso! Redirigiendo..."
            self.ids.message.color = get_color_from_hex("#000000")  # Color verde
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            # Retrasar 5 segundos antes de cambiar de pantalla
            Clock.schedule_once(self.redirect_to_clientes, 3)
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
                    
    def redirect_to_clientes(self, *args):
        app = App.get_running_app()
        clientes_screen = app.root.get_screen('clientes')
        self.ids.message.text = ""
        clientes_screen.dismiss_popup()
        

    
    def __init__(self,origen=None, **kwargs):
        super().__init__(**kwargs)
        # Captura eventos de teclado
        self.generar_codigo()
        self.origen = origen 
        Window.bind(on_key_down=self._on_key_down)
        
    def generar_codigo(self):
        # Generar un número aleatorio de 13 dígitos
        numero = '0' + ''.join(str(random.randint(0, 9)) for _ in range(10))
        self.ids.codigoCliente.text = str(numero)

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