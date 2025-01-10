import os
import PIL.Image
import PIL.ImageWin
import win32print
import win32ui
from barcode import Code128
from barcode.writer import ImageWriter
from kivy.lang import Builder
import PIL
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from control.datos.datos import sesion
from datetime import datetime
from kivy.clock import Clock
from kivy.uix.popup import Popup
from control.BDconsultas.inventario.CRUD import obtener_productos,obtener_producto_id,eliminar
from vista.pantallas.logica.popup.productos.popup_registro_productos import RegistroProductosScreen
from vista.pantallas.logica.popup.productos.popup_editar_productos import EditarProductosScreen
from kivy.properties import StringProperty

kv_path = os.path.join(os.path.dirname(__file__), '..','diseño', 'inventario.kv')
Builder.load_file(kv_path)

class InventrioScreen(Screen):
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'icons'))
    )
    ruta_barcode = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'codebar'))
    )
    def on_enter(self):
        """Se llama cuando la pantalla está a punto de mostrarse."""
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
        
        self.cargar_productos()
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)

    def actualizar_fecha_hora(self, *args):
        # Obtener la fecha y hora actual
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        # Actualizar el texto del Label con la fecha y hora
        self.ids.fecha_hora.text = ahora
        
        
    #apartado de las funciones principales
    
    def cargar_productos(self):
        """Crea los widgets dinámicamente para cada proveedor."""
        productos = obtener_productos()
        grid = self.ids.productos_grid
        grid.clear_widgets() 

        for producto in productos:
            id_producto,id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras = producto
            
            label_codigo = Label(
                text=str(codigo_barras),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_codigo)
            
            texto_truncado = nombre_producto[:20] + "..." if len(nombre_producto) > 20 else nombre_producto
            # Widget para el teléfono
            label_nombre = Label(
                text= nombre_producto,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_nombre, nombre_producto)
            grid.add_widget(label_nombre)

            
            label_precio = Label(
                text=str(precio_publico),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio)
            
            label_precio_compra = Label(
                text=str(precio_compra),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio_compra)
            
            label_cantidad = Label(
                text=str(cantidad_inventario),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad)

            # Widget para el correo
            texto_truncado = categoria[:35] + "..." if len(categoria) > 35 else categoria
            label_categoria = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_categoria, categoria)
            grid.add_widget(label_categoria)


            # Acciones: Editar y Eliminar
            acciones = BoxLayout(orientation='vertical', spacing=5)
            acciones1 = BoxLayout(orientation='horizontal', spacing=5)

            # Botón Editar
            btn_editar = Button(
                text='[b]Editar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.02, 0.81, 0, 1),
                size_hint=(0.5, 0.5),
                pos_hint={'center_y': 0.5},
                on_release=lambda x, id=id_producto: self.editar_producto(id)
            )

            # Botón Eliminar
            btn_eliminar = Button(
                text='[b]Eliminar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.86, 0.01, 0.01, 1),
                size_hint=(0.5, 0.5),
                pos_hint={'center_y': 0.5},
                on_release=lambda x, name=nombre_producto, id=id_producto: self.eliminar_producto(id, name)
            )

            # Añadir Editar y Eliminar al BoxLayout Horizontal
            acciones1.add_widget(btn_editar)
            acciones1.add_widget(btn_eliminar)

            # Botón Código de Barras
            btn_codigobarras = Button(
                text='[b]Imprimir Código de Barras[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.019, 0.72, 0.70, 1),
                size_hint=(1, 0.5),
                pos_hint={'center_x': 0.5},
                on_release=lambda x, name=nombre_producto,codigoBarras=codigo_barras: self.imprimirCodigo(codigoBarras,name)
            )

            # Añadir el Box Horizontal y el botón Código de Barras al Box Vertical
            acciones.add_widget(acciones1)
            acciones.add_widget(btn_codigobarras)

            # Añadir las acciones al grid
            grid.add_widget(acciones)
                        
    def filtrar_productos(self, texto):
        """Filtra la lista de productos basada en el texto ingresado."""
        texto = texto.strip().lower()  # Asegúrate de que el texto sea consistente
        productos = obtener_productos()  # Obtener todos los productos
        grid = self.ids.productos_grid
        grid.clear_widgets()  # Limpia la cuadrícula antes de añadir nuevos widgets

        # Filtrar productos que coincidan con el texto ingresado
        productos_filtrados = [
            producto for producto in productos
            if texto in producto[2].lower() or texto in producto[10].lower()
        ]
        

        # Cargar los productos filtrados
        for producto in productos_filtrados:
            id_producto,id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras = producto
            
            label_codigo = Label(
                text=str(codigo_barras),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_codigo)
            
            texto_truncado = nombre_producto[:20] + "..." if len(nombre_producto) > 20 else nombre_producto
            # Widget para el teléfono
            label_nombre = Label(
                text= nombre_producto,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_nombre, nombre_producto)
            grid.add_widget(label_nombre)

            
            label_precio = Label(
                text=str(precio_publico),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio)
            
            label_precio_compra = Label(
                text=str(precio_compra),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio_compra)
            
            label_cantidad = Label(
                text=str(cantidad_inventario),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad)

            # Widget para el correo
            texto_truncado = categoria[:35] + "..." if len(categoria) > 35 else categoria
            label_categoria = Label(
                text=texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_categoria, categoria)
            grid.add_widget(label_categoria)


            # Acciones: Editar y Eliminar
            acciones = BoxLayout(orientation='vertical', spacing=5)
            acciones1 = BoxLayout(orientation='horizontal', spacing=5)

            # Botón Editar
            btn_editar = Button(
                text='[b]Editar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.02, 0.81, 0, 1),
                size_hint=(0.5, 0.5),
                pos_hint={'center_y': 0.5},
                on_release=lambda x, id=id_producto: self.editar_producto(id)
            )

            # Botón Eliminar
            btn_eliminar = Button(
                text='[b]Eliminar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.86, 0.01, 0.01, 1),
                size_hint=(0.5, 0.5),
                pos_hint={'center_y': 0.5},
                on_release=lambda x, name=nombre_producto, id=id_producto: self.eliminar_producto(id, name)
            )

            # Añadir Editar y Eliminar al BoxLayout Horizontal
            acciones1.add_widget(btn_editar)
            acciones1.add_widget(btn_eliminar)

            # Botón Código de Barras
            btn_codigobarras = Button(
                text='[b]Imprimir Código de Barras[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                background_color=(0.019, 0.72, 0.70, 1),
                size_hint=(1, 0.5),
                pos_hint={'center_x': 0.5},
                on_release=lambda x, name=nombre_producto,codigoBarras=codigo_barras: self.imprimirCodigo(codigoBarras,name)
            )

            # Añadir el Box Horizontal y el botón Código de Barras al Box Vertical
            acciones.add_widget(acciones1)
            acciones.add_widget(btn_codigobarras)

            # Añadir las acciones al grid
            grid.add_widget(acciones)
            
    def editar_producto(self, id_producto):
        """Abre el modal para editar un proveedor."""
        producto = obtener_producto_id(id_producto)  # Obtén los datos del proveedor por ID
        if producto:
            self.show_popup_editar(producto)  # Pasar los datos al popup
        else:
            print(f"No se encontró el empleado con ID: {id_producto}")

    def eliminar_producto(self, id_producto,name):
        # Crear el contenido del Popup de confirmación
        box_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(
            text=f"¿Estás seguro de que deseas eliminar al empleado llamado?",
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
        btn_confirmar.bind(on_release=lambda *args: self.confirmar_eliminacion(id_producto, popup_confirmacion))
        btn_cancelar.bind(on_release=popup_confirmacion.dismiss)

        # Mostrar el Popup
        popup_confirmacion.open()

    def confirmar_eliminacion(self, id_empleado, popup):
        popup.dismiss()  # Cerrar el Popup de confirmación

        # Llamar a la función eliminar
        resultado = eliminar(id_empleado)  # Aquí debes implementar la función eliminar

        # Mostrar un Popup con el resultado
        mensaje = "Empleado eliminado con éxito" if resultado == "Exito" else "Error al eliminar el empleado"
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
        self.cargar_empleados()
        popup.open()

        # Cerrar el Popup automáticamente después de 3 segundos
        Clock.schedule_once(lambda dt: popup.dismiss(), 3)
        

    def imprimirCodigo(self, codigoBarras, name):
        # Configuración del encabezado
        fecha_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        ticket_text = ""
        ticket_text += "           PRODUCTO\n"
        ticket_text += "----------------------------\n"
        ticket_text += f"       {name:<5}\n"
        ticket_text += "----------------------------\n"
        
        # Obtener la impresora predeterminada
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)

        # Crear el dispositivo de impresión
        printer_device = win32ui.CreateDC()
        printer_device.CreatePrinterDC(printer_name)

        try:
            # Generar el código de barras como imagen
            barcode_path = self.generarCodigoBarras(codigoBarras)
            
            if not barcode_path.endswith('.png'):
                barcode_path = f'{barcode_path}.png'

            # Cargar la imagen del código de barras
            barcode_image = PIL.Image.open(barcode_path)

            # Convertir la imagen a modo RGB (necesario para la impresión)
            barcode_image = barcode_image.convert('RGB')

            # Iniciar el trabajo de impresión
            printer_device.StartDoc("Ticket de Compra")
            printer_device.StartPage()

            # Configurar posición inicial en la hoja
            x, y = 10, 100
            line_spacing = 30  # Espaciado entre líneas

            # Escribir línea por línea del ticket
            for line in ticket_text.split("\n"):
                printer_device.TextOut(x, y, line.strip())  # Eliminar espacios innecesarios
                y += line_spacing

            # Dibujar la imagen del código de barras en el ticket
            # Convertir la imagen en formato compatible con `win32ui`
            dib = PIL.ImageWin.Dib(barcode_image)

            # Configurar posición y tamaño de la imagen
            image_x, image_y = x, y  # Posición inicial de la imagen
            image_width, image_height = barcode_image.size
            # Estirar la imagen un 20% más ancha en el eje X
            stretched_width = image_width  
            stretched_height = image_height 

            # Dibujar la imagen estirada solo en el eje X
            dib.draw(printer_device.GetHandleOutput(), (image_x, image_y, image_x + stretched_width, image_y + stretched_height))

            # Finalizar el trabajo de impresión
            printer_device.EndPage()
            printer_device.EndDoc()

        except Exception as e:
            print(f"Error durante la impresión: {e}")
            # Cancelar el trabajo de impresión en caso de error
            win32print.AbortPrinter(hprinter)

        finally:
            # Liberar recursos
            printer_device.DeleteDC()
            win32print.ClosePrinter(hprinter)

        return True

    def generarCodigoBarras(self, codigoBarras):
        from barcode import Code128
        from barcode.writer import ImageWriter

        # Generar código de barras como imagen
        barcode_class = Code128
        writer = ImageWriter()
        barcode = barcode_class(codigoBarras, writer=writer)

        # Construir la ruta completa para guardar el archivo
        barcode_path = os.path.join(self.ruta_barcode, f'{codigoBarras}')

        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(barcode_path), exist_ok=True)

        # Guardar el código de barras como imagen
        barcode.save(barcode_path)
        return barcode_path

    
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
        
    #lanza el popup de editar productos
    
    def show_popup_editar(self,datos_producto):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = EditarProductosScreen()
        popup_content.cargar_campos(datos_producto)
        self.popup = Popup(title="Editar proveedores",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    #lanzar popup de registro de productos
    def show_popup(self):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = RegistroProductosScreen()
        self.popup = Popup(title="Registro de productos",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.cargar_productos()
            self.popup = None  # Limpiar la referencia al popup
            
    def redirect_productos(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_clientes(self, *args):
        app = App.get_running_app()
        app.root.current = 'clientes'
        
    def redirect_Proveedores(self, *args):
        app = App.get_running_app()
        app.root.current = 'proveedores'
    
    def redirect_corte_caja(self, *args):
        app = App.get_running_app()
        app.root.current = 'corte_caja'