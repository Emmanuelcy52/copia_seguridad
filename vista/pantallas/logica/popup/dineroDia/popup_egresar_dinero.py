import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from datetime import datetime,timedelta
from control.BDconsultas.cortecaja.CRUD import obtener_dinero_inicial,registrar_egreso_dinero
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

# Obtén la ruta absoluta del archivo KV
kv_path = os.path.join(os.path.dirname(__file__), '..','..','..','diseño','popup','dinerodia','egresar_dinero.kv')
Builder.load_file(kv_path)

class egresardineroScreen(Screen):
    
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'diseño', 'imagenes', 'icons'))
    )
    
    def Registar_egreso(self):
        """Verifica las credenciales y navega a la pantalla principal si son correctas."""
        dineroRetirar = self.ids.dineroRetirar.text
        motivoRetiro = self.ids.motivoRetiro.text.lower()
        fecha = datetime.now().strftime('%d/%m/%Y') 
        hora = datetime.now().strftime('%H:%M')
        datosDineroInicial= obtener_dinero_inicial(fecha)
        id_dinero_dia = datosDineroInicial[0]
        # Validar que todos los campos estén llenos
        if not dineroRetirar:
            self.ids.message.text = "ingresa una cantidad de dinero"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        elif not motivoRetiro:
            self.ids.message.text = "ingresa el motivo del retiro"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage=.5
            self.size_hint_y_menssage=0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        
        dineroRetirar = float(dineroRetirar)
        mensaje = registrar_egreso_dinero(id_dinero_dia, dineroRetirar,motivoRetiro,hora)
        
        if mensaje == "Exito":
            # Mostrar mensaje de éxito
            self.ids.message.text = "Tu retiro fue registrado"
            self.ids.message.color = get_color_from_hex("#000000")  # Color verde
            self.height_message = 10
            self.size_hint_x_menssage=.5
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
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None
                    
    def redirect(self, *args):
        app = App.get_running_app()
        productos_screen = app.root.get_screen('home')
        self.ids.message.text = ""
        productos_screen.dismiss_popup()
    
    def __init__(self,origen=None, **kwargs):
        super().__init__(**kwargs)
        # Captura eventos de teclado
        self.origen = origen 
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