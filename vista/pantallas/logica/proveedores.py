import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from control.datos.datos import sesion
from kivy.uix.image import Image
from datetime import datetime
from control.BDconsultas.proveedores.CRUD import obtener_proveedores,obtener_proveedor_id,eliminar
from kivy.uix.popup import Popup
from vista.pantallas.logica.popup.proveedores.pantalla_registro_proveedor import RegistroProveedorScreen
from vista.pantallas.logica.popup.proveedores.pantalla_editar_proveedor import EditarProveedoresScreen
from kivy.clock import Clock
from kivy.properties import StringProperty

kv_path = os.path.join(os.path.dirname(__file__), '..','diseño', 'proveedores.kv')
Builder.load_file(kv_path)

class ProveedoresScreen(Screen):
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'icons'))
    )
    
    def on_enter(self):
        self.cargar_proveedores()
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:
            if datos[2] != 'administrador':
              self.ids.corteCajaRedig.disabled = True
              self.ids.empleadosRedig.disabled = True 
            else:
                self.ids.corteCajaRedig.disabled = False
                self.ids.empleadosRedig.disabled = False
            self.ids.usuario.text = datos[1]
        else:
            print("La sesión no está inicializada")
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)
        
        
    def cargar_proveedores(self):
        """Crea los widgets dinámicamente para cada proveedor."""
        proveedores = obtener_proveedores()
        grid = self.ids.proveedores_grid
        grid.clear_widgets()  # Limpia la cuadrícula antes de añadir nuevos widgets

        for proveedor in proveedores:
            id_proveedor, nombre, correo, telefono, direccion, notas = proveedor

            # Widget para el nombre
            texto_truncado = nombre[:20] + "..." if len(nombre) > 20 else nombre
            label_nombre = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            self.add_mouse_over_event(label_nombre, nombre)
            grid.add_widget(label_nombre)

            # Widget para el correo
            texto_truncado = correo[:35] + "..." if len(correo) > 35 else correo
            label_correo = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_correo, correo)
            grid.add_widget(label_correo)

            # Widget para el teléfono
            label_telefono = Label(
                text=telefono,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_telefono)

            # Widget para la dirección
            texto_truncado = direccion[:35] + "..." if len(direccion) > 35 else direccion
            label_direccion = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_direccion, direccion)
            grid.add_widget(label_direccion)

            # Widget para las notas con funcionalidad de tooltip
            texto_truncado = notas[:20] + "..." if len(notas) > 20 else notas
            label_notas = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Limita el ancho según el tamaño disponible
                size_hint=(1, None),
                shorten=True,
                shorten_from='right',
                max_lines=.5  # Limita a una sola línea
            )
            self.add_mouse_over_event(label_notas, notas)
            grid.add_widget(label_notas)

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
                on_release=lambda x, id=id_proveedor: self.editar_proveedor(id)
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
                on_release=lambda x,name=nombre, id=id_proveedor: self.eliminar_proveedor(id,name)
            )
            acciones.add_widget(btn_editar)
            acciones.add_widget(btn_eliminar)
            grid.add_widget(acciones)

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


    def editar_proveedor(self, id_proveedor):
        """Abre el modal para editar un proveedor."""
        proveedor = obtener_proveedor_id(id_proveedor)  # Obtén los datos del proveedor por ID
        if proveedor:
            self.show_popup_editar(proveedor)  # Pasar los datos al popup
        else:
            print(f"No se encontró el proveedor con ID: {id_proveedor}")

    def eliminar_proveedor(self, id_proveedor,name):
        """Muestra un Popup de confirmación para eliminar el proveedor."""
        # Crear el contenido del Popup de confirmación
        box_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(
            text=f"¿Estás seguro de que deseas eliminar al proveedor llamado?",
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
        btn_confirmar.bind(on_release=lambda *args: self.confirmar_eliminacion(id_proveedor, popup_confirmacion))
        btn_cancelar.bind(on_release=popup_confirmacion.dismiss)

        # Mostrar el Popup
        popup_confirmacion.open()

    def confirmar_eliminacion(self, id_proveedor, popup):
        """Realiza la eliminación del proveedor y muestra el resultado."""
        popup.dismiss()  # Cerrar el Popup de confirmación

        # Llamar a la función eliminar
        resultado = eliminar(id_proveedor)  # Aquí debes implementar la función eliminar

        # Mostrar un Popup con el resultado
        mensaje = "Proveedor eliminado con éxito" if resultado == "Exito" else "Error al eliminar el proveedor"
        layout = BoxLayout(spacing=10, padding=10)
        
        gif1 = Image(
            source= self.ruta_imagenes + "/success.png",  # Reemplaza con la ruta de tu GIF
            size_hint_x= 0.3,
            size_hint_y= 0.3,
            pos_hint= {'center_y': 0.5}
        )
        # Etiqueta para el mensaje
        etiqueta = Label(
            text=mensaje,
            font_size= self.width * 0.02,
            color=(0, 0, 0, 1),
            halign='center'
        )

        # Imagen GIF (asegúrate de que el archivo .gif esté en tu directorio de trabajo)
        gif = Image(
            source= self.ruta_imagenes + "/success.png",  # Reemplaza con la ruta de tu GIF
            size_hint_x= 0.3,
            size_hint_y= 0.3,
            pos_hint= {'center_y': 0.5}
        )

        # Agregar widgets al layout
        layout.add_widget(gif1)
        layout.add_widget(etiqueta)
        layout.add_widget(gif)

        # Crear el Popup con el layout
        popup = Popup(
            title='Mensaje',
            title_align= 'center',
            title_color= (0, 0, 0, 1),
            content=layout,
            size_hint=(0.5, 0.5),  # Ajusta el tamaño según sea necesario
            background='',
            background_color=(1, 1, 1, 0.9),
            auto_dismiss=True
        )

        # Actualizar los proveedores y mostrar el Popup
        self.cargar_proveedores()
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
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = RegistroProveedorScreen()
        self.popup = Popup(title="Registro de proveedores",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None
            self.cargar_proveedores()
            
    def show_popup_editar(self,datos_proveedor):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = EditarProveedoresScreen()
        popup_content.cargar_campos(datos_proveedor)
        self.popup = Popup(title="Editar proveedores",
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
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_clientes(self, *args):
        app = App.get_running_app()
        app.root.current = 'clientes'
        
    def redirect_corte_caja(self, *args):
        app = App.get_running_app()
        app.root.current = 'corte_caja'