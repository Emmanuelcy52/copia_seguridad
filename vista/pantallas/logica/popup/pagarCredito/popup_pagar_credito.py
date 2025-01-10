import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from control.datos.datos import sesion
from control.BDconsultas.creditos.CRUD import pagar_credito,registrar_pago
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

kv_path = os.path.join(os.path.dirname(__file__), '..','..','..','diseño','popup','pagarCredito','pagar_credito.kv')
Builder.load_file(kv_path)

class PagarCreditoScreen(Screen):
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    # Define la ruta a las imágenes como una propiedad
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'diseño', 'imagenes', 'icons'))
    )
    
    def __init__(self,deuda, **kwargs,):
        super().__init__(**kwargs)
        self.deuda = deuda
        self.cargarDeuda(self.deuda)
        
    def cargarDeuda(self,deuda):
        id,monto_total, saldo_pendiente, fecha_inicio, fecha_vencimiento = deuda
        self.ids.montoRestante.text = f"Total a pagar: ${saldo_pendiente}"
        
    def confirmar_pago(self):
        """Lógica para confirmar el pago."""
        try:
            fecha_pago = datetime.now().strftime('%d/%m/%Y')
            monto = self.ids.monto_pago.text
            id,monto_total, saldo_pendiente, fecha_inicio, fecha_vencimiento = self.deuda
            if monto == '':
                self.ids.message.text = "El monto no debe estar vacio."
                self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                self.height_message = 10
                self.size_hint_x_menssage = .9
                self.size_hint_y_menssage = 0.4
                Clock.schedule_once(self.cerrarmensaje, 3)
                return
            else:
                monto = float(monto)
                print(monto)
            if monto <= 0:
                self.ids.message.text = "El monto debe ser mayor a cero."
                self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                self.height_message = 10
                self.size_hint_x_menssage = .9
                self.size_hint_y_menssage = 0.4
                Clock.schedule_once(self.cerrarmensaje, 3)
                return
            if monto > saldo_pendiente:
                print(monto , saldo_pendiente)
                self.ids.message.text = "El monto no puede ser mayor al saldo pendiente."
                self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                self.height_message = 10
                self.size_hint_x_menssage = .9
                self.size_hint_y_menssage = 0.4
                Clock.schedule_once(self.cerrarmensaje, 3)
                return
            
            nuevo_saldo = saldo_pendiente - monto
            
            if nuevo_saldo <= 0:
                estatus = 'Pagado'
                nuevo_saldo = 0 
            else:
                estatus = 'Pago a credito'
                
            respuesta = registrar_pago(id,fecha_pago,monto)
            if respuesta == 'Exito':
                respuesta = pagar_credito(id,nuevo_saldo,estatus)
                if respuesta == 'Exito':
                    self.ids.message.text = "Pago Registrado"
                    self.ids.message.color = (0, 1, 0, 1)  # Color rojo
                    self.height_message = 10
                    self.size_hint_x_menssage = .9
                    self.size_hint_y_menssage = 0.4
                    Clock.schedule_once(self.cerrarmensaje, 3)
                    Clock.schedule_once(self.cerrarpopup, 3)

        except ValueError as e:
            print(f"Error en el pago: {e}")
            
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""  
            
    def cerrarpopup(self,*args):
        app = App.get_running_app()
        venta_screen = app.root.get_screen('clientes')
        self.ids.message.text = ""
        venta_screen.dismiss_popup_pago()
        
            
    

