import os
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kivy.clock import Clock
from control.Crear_copia.copia_seguridad import exportar_cortes,exportar_productos,exportar_ventas
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from control.BDconsultas.Usuario.CRUD import login,obtener_respaldo,crear_o_actualizar_respaldo
from vista.pantallas.logica.popup.usuarios.pantalla_registro_user import RegistroUserScreen


# Carga el archivo KV
kv_path = os.path.join(os.path.dirname(__file__), '..', 'diseño', 'login.kv')
Builder.load_file(kv_path)

class LoginScreen(Screen):
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'icons'))
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Captura eventos de teclado
        Window.bind(on_key_down=self._on_key_down)
        respaldo = obtener_respaldo()
        if respaldo:
            fecha_Actual = datetime.now()
            fecha_Actual_formateada = fecha_Actual.strftime('%d/%m/%Y')
            if respaldo[2] <= fecha_Actual_formateada:
                respaldo2 = exportar_productos()
                respaldo3 = exportar_ventas()
                respaldo4 = exportar_cortes()
                if respaldo2 == 'Exito' and respaldo3 == 'Exito' and respaldo4 == 'Exito':
                    # Fecha actual
                    fecha_respaldo = datetime.now()
                    # Sumar un mes a la fecha actual
                    fecha_proximo_respaldo = fecha_respaldo + relativedelta(months=1)

                    # Formatear ambas fechas como cadenas
                    fecha_respaldo_str = fecha_respaldo.strftime('%d/%m/%Y')
                    fecha_proximo_respaldo_str = fecha_proximo_respaldo.strftime('%d/%m/%Y')
                    # Estado
                    estado = 'echo'
                    respuesta = crear_o_actualizar_respaldo(fecha_respaldo_str,fecha_proximo_respaldo_str,estado)
                    print(respuesta)
                    print('respaldo realizado')
        else:
            respaldo2 = exportar_productos()
            respaldo3 = exportar_ventas()
            respaldo4 = exportar_cortes()
            if respaldo2 == 'Exito' and respaldo3 == 'Exito' and respaldo4 == 'Exito':
                # Fecha actual
                fecha_respaldo = datetime.now()
                # Sumar un mes a la fecha actual
                fecha_proximo_respaldo = fecha_respaldo + relativedelta(months=1)

                # Formatear ambas fechas como cadenas
                fecha_respaldo_str = fecha_respaldo.strftime('%d/%m/%Y')
                fecha_proximo_respaldo_str = fecha_proximo_respaldo.strftime('%d/%m/%Y')
                # Estado
                estado = 'echo'
                respuesta = crear_o_actualizar_respaldo(fecha_respaldo_str,fecha_proximo_respaldo_str,estado)
                print(respuesta)
            print("No se encontró ningún respaldo.")

    def verify_credentials(self):
        """Verifica las credenciales y navega a la pantalla principal si son correctas."""
        username = self.ids.username.text.lower()
        password = self.ids.password.text
        mensaje = login(username, password)

        if mensaje == "True":
            self.show_popup()  # Muestra el Popup cuando el mensaje es "tabla vacia"
        else:
            if mensaje == "Exito":
                self.ids.username.text = ''
                self.ids.password.text = ''
                self.manager.current = 'home'
            else:
                self.ids.message.text = mensaje
                self.height_message = 80
                self.size_hint_x_menssage=0.5
                Clock.schedule_once(self.cerrarmensaje, 5)
    
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0  # Restaura el tamaño
        self.ids.message.text = ""

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

    def show_popup(self):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = RegistroUserScreen()
        self.popup = Popup(title="Registro de Usuario",
                           content=popup_content,
                           size_hint=(0.8, 0.8),
                           auto_dismiss=False)
        self.popup.open()

    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None  # Limpiar la referencia al popup
