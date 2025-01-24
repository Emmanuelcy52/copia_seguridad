import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from control.datos.datos import sesion
from kivy.uix.image import Image
from datetime import datetime
from control.BDconsultas.clientes.CRUD import obtener_clientes,obtener_cliente_id,eliminar,obtener_deuda
from control.BDconsultas.creditos.CRUD import pagar_credito,registrar_pago
from kivy.uix.popup import Popup
from vista.pantallas.logica.popup.pagarCredito.popup_pagar_credito import PagarCreditoScreen
from vista.pantallas.logica.popup.clientes.popup_registrar_cliente import RegistroCientesScreen
from vista.pantallas.logica.popup.clientes.popup_editar_cliente import EditarCientesScreen
from kivy.clock import Clock
from kivy.properties import StringProperty
import sys

# Función para obtener la ruta correcta según el entorno
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño', 'clientes.kv'))
Builder.load_file(kv_path)

class ClientesScreen(Screen):
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    
    def on_enter(self):
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:
            if datos[2] != 'administrador':
              self.ids.corteCajaRedig.disabled = True
              self.ids.empleadosRedig.disabled = True 
            else:
                self.ids.corteCajaRedig.disabled = False
                self.ids.empleadosRedig.disabled = False
            self.ids.usuario.text = datos[1]
            self.id_usuario=datos[0]
        else:
            print("La sesión no está inicializada")
            
        self.cargar_clientes()
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)
        
        
    def cargar_clientes(self):
        """Crea los widgets dinámicamente para cada proveedor."""
        clientes = obtener_clientes()
        grid = self.ids.clientes_grid
        grid.clear_widgets()  # Limpia la cuadrícula antes de añadir nuevos widgets

        for cliente in clientes:
            id_cliente, codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito = cliente
            deuda = obtener_deuda(id_cliente)
            
            if deuda:
                deudasTotales = len(deuda)
            else:
                deudasTotales = 0
            # Widget para el teléfono
            label_codigo_cliente = Label(
                text=str(codigoCliente),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_codigo_cliente)

            # Widget para el nombre
            texto_truncado = nombreReal[:20] + "..." if len(nombreReal) > 20 else nombreReal
            label_nombre = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            self.add_mouse_over_event(label_nombre, nombreReal)
            grid.add_widget(label_nombre)

            label_Telefono = Label(
                text=telefono,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_Telefono)

            # Widget para el teléfono
            texto_truncado = direccion[:20] + "..." if len(direccion) > 20 else direccion
            label_Direccion = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_Direccion, direccion)
            grid.add_widget(label_Direccion)
            
            label_credito = Label(
                text=str(limite_credito),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_credito)
            
            label_Deuda = Label(
                text=str(deudasTotales),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event_deudas(label_Deuda, id_cliente)
            grid.add_widget(label_Deuda)

            # Acciones: Editar y Eliminar
            acciones = BoxLayout(orientation='horizontal', spacing=5)
            btn_editar = Button(
                text='[b]Editar[/b]',
                markup= True,
                color=(1, 1, 1, 1),
                background_normal= '',
                background_color = (0.02, 0.81, 0, 1),
                size_hint_x=0.5,
                size_hint_y=0.5,
                pos_hint= {'center_y': 0.5},
                on_release=lambda x, id=id_cliente: self.editar_cliente(id)
            )
            btn_eliminar = Button(
                text='[b]Eliminar[/b]',
                markup= True,
                color=(1, 1, 1, 1),
                background_normal= '',
                background_color = (0.86, 0.01, 0.01, 1),
                size_hint_x=0.5,
                size_hint_y=0.5,
                pos_hint= {'center_y': 0.5},
                on_release=lambda x,name=nombreReal, id=id_cliente: self.eliminar_cliente(id,name)
            )
            if deuda:
                btn_eliminar.disabled = True  
            else:
                btn_eliminar.disabled = False
                
            acciones.add_widget(btn_editar)
            acciones.add_widget(btn_eliminar)
            grid.add_widget(acciones)
            
    def filtrar_clientes(self, texto):
        """Filtra la lista de clientes basada en el texto ingresado."""
        texto = texto.strip().lower()  # Asegúrate de que el texto sea consistente
        clientes = obtener_clientes()  # Obtener todos los clientes
        grid = self.ids.clientes_grid
        grid.clear_widgets()  # Limpia la cuadrícula antes de añadir nuevos widgets

        # Filtrar clientes que coincidan con el texto ingresado
        clientes_filtrados = [
            cliente for cliente in clientes
            if texto in cliente[1].lower() or texto in cliente[2].lower()
        ]

        # Cargar los clientes filtrados
        for cliente in clientes_filtrados:
            id_cliente, codigoCliente,nombreReal, clave_lector, telefono, direccion, correo, nombre_refente, telefono_refente, direccion_refente,limite_credito = cliente
            
            deuda = obtener_deuda(id_cliente)
            
            if deuda:
                deudasTotales = len(deuda)
            else:
                deudasTotales = 0
            # Widget para el teléfono
            label_codigo_cliente = Label(
                text=str(codigoCliente),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_codigo_cliente)

            # Widget para el nombre
            texto_truncado = nombreReal[:20] + "..." if len(nombreReal) > 20 else nombreReal
            label_nombre = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            self.add_mouse_over_event(label_nombre, nombreReal)
            grid.add_widget(label_nombre)

            label_Telefono = Label(
                text=telefono,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_Telefono)

            # Widget para el teléfono
            texto_truncado = direccion[:20] + "..." if len(direccion) > 20 else direccion
            label_Direccion = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_Direccion, direccion)
            grid.add_widget(label_Direccion)
            
            label_credito = Label(
                text=str(limite_credito),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_credito)
            
            label_Deuda = Label(
                text=str(deudasTotales),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event_deudas(label_Deuda, id_cliente)
            grid.add_widget(label_Deuda)

            # Acciones: Editar y Eliminar
            acciones = BoxLayout(orientation='horizontal', spacing=5)
            btn_editar = Button(
                text='[b]Editar[/b]',
                markup= True,
                color=(1, 1, 1, 1),
                background_normal= '',
                background_color = (0.02, 0.81, 0, 1),
                size_hint_x=0.5,
                size_hint_y=0.5,
                pos_hint= {'center_y': 0.5},
                on_release=lambda x, id=id_cliente: self.editar_cliente(id)
            )
            
            acciones.add_widget(btn_editar)
            # Botón de Eliminar
            btn_eliminar = Button(
                text='[b]Eliminar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.86, 0.01, 0.01, 1),
                size_hint_x=0.5,
                size_hint_y=0.5,
                pos_hint={'center_y': 0.5},
                on_release=lambda x, name=nombreReal, id=id_cliente: self.eliminar_cliente(id, name)
            )
            
            if deuda:
                btn_eliminar.disabled = True  
            else:
                btn_eliminar.disabled = False
            
            acciones.add_widget(btn_eliminar)
            grid.add_widget(acciones)
            


    def show_tooltip_deudas(self, widget, text):
        """Muestra un popup con el texto completo."""
        deudas = obtener_deuda(text)

        # Crear un BoxLayout para contener todas las deudas
        layout_deudas = BoxLayout(orientation="vertical", size_hint_y=None)
        layout_deudas.bind(minimum_height=layout_deudas.setter('height'))  # Ajustar altura dinámica

        for deuda in deudas:
            id,monto_total, saldo_pendiente, fecha_inicio, fecha_vencimiento = deuda

            # Crear un BoxLayout para cada deuda
            deuda_layout = BoxLayout(orientation="vertical", padding=-20, spacing=5, size_hint_y=None)
            deuda_layout.height = 150  # Altura fija para cada sección de deuda

            # Crear un Label para mostrar la información de la deuda
            label_info = Label(
                text=(
                    f"Monto inicial: {monto_total}\n"
                    f"Monto restante: {saldo_pendiente}\n"
                    f"Fecha de compra: {fecha_inicio}\n"
                    f"Fecha de vencimiento: {fecha_vencimiento}"
                ),
                valign="middle",
                halign="center",
                size_hint_y=None,
                color= (0, 0, 0, 1),
                height=100,
            )
            label_info.bind(size=lambda s, w: s.setter('text_size')(s, w))

            # Crear un botón para procesar el pago de esta deuda
            boton_pago = Button(
                text="Pagar esta deuda",
                size_hint_y=None,
                height=40,
                background_color=(0, 1, 0, 1),  # Verde
                on_press=lambda x, deuda=deuda: self.mostrar_popup_pago(deuda)
            )

            # Agregar Label y botón al layout de la deuda
            deuda_layout.add_widget(label_info)
            deuda_layout.add_widget(boton_pago)

            # Agregar el layout de la deuda al layout principal
            layout_deudas.add_widget(deuda_layout)

        # Crear un ScrollView para contener el layout principal
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout_deudas)

        # Mostrar el popup
        self.popupInicial = Popup(
            title="Información completa de la deuda del cliente",
            title_color=(0,0,0,1),
            title_size = 50,
            title_align='center',
            content=scroll_view,
            background='none', 
            background_color=(1,1,1,1),
            size_hint=(0.7, 0.7),
            auto_dismiss=True
        )
        self.popupInicial.open()


    def mostrar_popup_pago(self, deuda):
        self.popupInicial.dismiss()
        # Crear y mostrar el popup
        popup_content = PagarCreditoScreen(deuda)
        self.popup_pago = Popup(
            title="Realizar Pago",
            content=popup_content,
            size_hint=(0.5, 0.8),
            auto_dismiss=False
        )
        self.popup_pago.open()
        

    def show_tooltip(self, widget, text):
        """Muestra un popup con el texto completo."""
        popup = Popup(
            title='Información completa',
            content=Label(text=text),
            size_hint=(0.4, 0.2),
            auto_dismiss=True
        )
        popup.open()

    def add_mouse_over_event(self, widget, text):
        """Asocia el evento de mostrar el tooltip al pasar el mouse sobre el widget."""
        widget.bind(
            on_touch_down=lambda instance, touch: self.show_tooltip(widget, text)
            if widget.collide_point(*touch.pos) else None
        )
        
    def add_mouse_over_event_deudas(self, widget, text):
        widget.bind(
            on_touch_down=lambda instance, touch: self.show_tooltip_deudas(widget, text)
            if widget.collide_point(*touch.pos) else None
        )


    def editar_cliente(self, id_cliente):
        """Abre el modal para editar un proveedor."""
        cliente = obtener_cliente_id(id_cliente)  # Obtén los datos del proveedor por ID
        if cliente:
            self.show_popup_editar(cliente)  # Pasar los datos al popup
        else:
            print(f"No se encontró el empleado con ID: {id_cliente}")

    def eliminar_cliente(self, id_cliente,name):
        # Crear el contenido del Popup de confirmación
        box_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(
            text=f"¿Estás seguro de que deseas eliminar al cliente llamado?",
            color=(0, 0, 0, 1),  
            size_hint_x=1,
            size_hint_y=1,
            pos_hint= {'center_y': 0.5},
            halign='center',
            valign='middle',
            font_size= self.width * 0.01,
        )
        label_name = Label(
            text=f"{name}",
            color=(0, 0, 0, 1),  
            size_hint_x=1,
            size_hint_y=1,
            pos_hint= {'center_y': 0.5},
            halign='center',
            valign='middle',
            font_size= self.width * 0.02,
        )
        
        box_layout.add_widget(label)
        box_layout.add_widget(label_name)

        # Crear los botones de confirmación y cancelación
        btn_confirmar = Button(text="Sí", size_hint=(1, None), height=40,background_normal= '', background_color= (0.02, 0.81, 0, 1))
        btn_cancelar = Button(text="No", size_hint=(1, None), height=40,background_normal= '',background_color = (0.86, 0.01, 0.01, 1))

        # Agregar los botones al layout
        box_buttons = BoxLayout(orientation='horizontal', spacing=10)
        box_buttons.add_widget(btn_confirmar)
        box_buttons.add_widget(btn_cancelar)
        box_layout.add_widget(box_buttons)

        # Crear el Popup de confirmación
        popup_confirmacion = Popup(
            title="Confirmación",
            title_align= 'center',
            title_color= (0, 0, 0, 1),
            content=box_layout,
            size_hint=(0.3, 0.3),
            background= '',
            background_color= (1, 1, 1, 0.9),
            auto_dismiss=False,
        )

        # Conectar los botones con sus funciones
        btn_confirmar.bind(on_release=lambda *args: self.confirmar_eliminacion(id_cliente, popup_confirmacion))
        btn_cancelar.bind(on_release=popup_confirmacion.dismiss)

        # Mostrar el Popup
        popup_confirmacion.open()

    def confirmar_eliminacion(self, id_cliente, popup):
        popup.dismiss()  # Cerrar el Popup de confirmación

        # Llamar a la función eliminar
        resultado = eliminar(id_cliente)

        # Determinar el mensaje a mostrar
        if resultado == "Exito":
            mensaje = "Cliente eliminado con éxito"
            icono = "success.png"
        elif "No se puede eliminar" in resultado:
            mensaje = resultado  # Mostrar el mensaje con las deudas
            icono = "error.png"  # Cambiar el ícono para indicar error
        else:
            mensaje = resultado  # Mostrar cualquier otro error
            icono = "error.png"

        # Crear el layout del Popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Imagen para el estado
        imagen_estado = Image(
            source=self.ruta_imagenes + f"/{icono}",
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.5}
        )

        # Etiqueta para el mensaje
        etiqueta = Label(
            text=mensaje,
            font_size=self.width * 0.02,
            color=(0, 0, 0, 1),
            halign='center'
        )

        # Agregar widgets al layout
        layout.add_widget(imagen_estado)
        layout.add_widget(etiqueta)

        # Crear el Popup con el layout
        popup = Popup(
            title='Resultado',
            title_align='center',
            title_color=(0, 0, 0, 1),
            content=layout,
            size_hint=(0.6, 0.6),
            background='',
            background_color=(1, 1, 1, 0.9),
            auto_dismiss=True
        )

        # Actualizar la lista de clientes y mostrar el Popup
        self.cargar_clientes()
        popup.open()

        # Cerrar el Popup automáticamente después de 3 segundos
        Clock.schedule_once(lambda dt: popup.dismiss(), 3)


    def actualizar_fecha_hora(self, *args):
        # Obtener la fecha y hora actual
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        # Actualizar el texto del Label con la fecha y hora
        self.ids.fecha_hora.text = ahora
        
    #lanzar popup de registro de productos
    def show_popup(self):
        # Crea la pantalla del registro
        popup_content = RegistroCientesScreen(origen=self)
        self.popup = Popup(
            title="Registro de clientes",
            content=popup_content,
            size_hint=(0.6, 0.8),
            auto_dismiss=False
        )
        self.popup.open()
        
        
    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None
            self.cargar_clientes()
            
    def dismiss_popup_pago(self):
        self.popup_pago.dismiss()
        self.cargar_clientes()
            
    def show_popup_editar(self,cliente):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = EditarCientesScreen()
        popup_content.cargar_campos(cliente)
        self.popup = Popup(title="Editar Cliente",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
            
            
    #apartado de redirecciones
            
    def redirect_productos(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'
        
    def redirect_Inventario(self, *args):
        app = App.get_running_app()
        app.root.current = 'inventario'
        
    def redirect_Proveedores(self, *args):
        app = App.get_running_app()
        app.root.current = 'proveedores'
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_Corte_caja(self, *args):
        app = App.get_running_app()
        app.root.current = 'corte_caja'
    
    def redirect_Estadisticas(self, *args):
        app = App.get_running_app()
        app.root.current = 'Estadisticas'