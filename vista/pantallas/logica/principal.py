import os
import sys
from kivy.app import App
from kivy.lang import Builder
import re
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from control.datos.datos import sesion
from control.datos.datos_venta import venta
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from control.BDconsultas.inventario.CRUD import obtener_producto_codigoBR,obtener_productos_bajos
from control.BDconsultas.cortecaja.CRUD import obtener_ventas_corte,obtener_dinero_inicial,validad_corte
from vista.pantallas.logica.popup.ventas.popup_agregar_producto import AgregarProductoScreen
from vista.pantallas.logica.popup.ventas.popup_pago_productos import ProcesarPagoScreen
from vista.pantallas.logica.popup.dineroDia.popup_dineroDia import dinerodiaScreen
from vista.pantallas.logica.popup.dineroDia.popup_egresar_dinero import egresardineroScreen
from vista.pantallas.logica.popup.proveedores.pantalla_alerta_stock_bajo import StockBajoScreen

# Función para obtener la ruta correcta según el entorno
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

# Obtén la ruta absoluta del archivo KV
kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño', 'principal.kv'))
Builder.load_file(kv_path)

class HomeScreen(Screen):
    
    dinerocaja = False
    button_enabled = BooleanProperty(False)
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
            
        self.corte_realizado = False
        fecha = datetime.now().strftime('%d/%m/%Y')   
        productos_bajos = obtener_productos_bajos()
        datos= validad_corte(fecha)
        if productos_bajos:
            self.show_popup_productos_bajos()
        if datos == False:
            self.validar_saldo_dia()
        elif datos[0] != 'Iniciado':
            self.corte_realizado = True
                
        
            
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)
        
        
    def validar_saldo_dia(self):
        fecha = datetime.now().strftime('%d/%m/%Y')
        valido = obtener_dinero_inicial(fecha)
        if valido == False:
            self.dinerocaja = True
            self.show_popup_registrarDinero()
            
        
    def cargar_productos(self):
        """Crea los widgets dinámicamente para cada proveedor."""
        self.ids.total_pagar.text ="$ 0.0"
        self.ids.total_productos.text = "0"
        datos=venta.obtener_venta()
        grid = self.ids.productos_grid
        grid.clear_widgets() 
        self.ids.buscar_producto.text=''
        totalproductos=len(datos)
        total_compra=0
        descuento_total=0
        
        if self.corte_realizado != True:
            self.button_enabled = len(datos) > 0

        for producto in datos:
            codigoBR = producto['codigoBarras']
            nombre_producto = producto['nombreProducto']
            cantidad_inventario = producto['Stock']
            precio_publico = float(producto['precioPublico'])
            precio_mayorista = float(producto['precioMayorista'])
            cantidad_venta = float(producto['CantidadVenta'])
            unidad_medida = str(producto['unidad_medida'])
            cantidad_mayorista = float(producto['CantidadMayorista'])
            
            if cantidad_venta >= cantidad_mayorista:
                precio_total = precio_mayorista * cantidad_venta
                descuento_producto = precio_publico - precio_mayorista
                descuento_producto *= cantidad_venta
            else:
                precio_total = precio_publico * cantidad_venta  
                descuento_producto = 0  
            
            
            texto_truncado = nombre_producto[:20] + "..." if len(nombre_producto) > 20 else nombre_producto
            # Widget para el teléfono
            label_nombre = Label(
                text= texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            self.add_mouse_over_event(label_nombre, nombre_producto)
            grid.add_widget(label_nombre)
            
            label_cantidad = Label(
                text=str(cantidad_inventario),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad)

            
            label_precio = Label(
                text=str(precio_publico),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio)
            
            label_cantidad_mayorista = Label(
                text=str(cantidad_mayorista),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad_mayorista)
            
            label_precio_Mayorista = Label(
                text=str(precio_mayorista),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio_Mayorista)
            
            cantida_formateada= f"{cantidad_venta} {unidad_medida}"
            label_Cantida_Venta = Label(
                text=str(cantida_formateada),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_Cantida_Venta)
            
            label_Total = Label(
                text=str(precio_total),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_Total)


            acciones_contenedor = BoxLayout(orientation='vertical', spacing=5,pos_hint = {'center_y': 0.5 })

            acciones_superior = BoxLayout(orientation='horizontal', spacing=5)
            btn_aumentar = Button(
                text='[b]+[/b]',
                markup = True,
                size_hint=(1, .8),
                background_normal='',
                background_color=(0.1, 0.7, 0.1, 1),
                pos_hint = {'center_y': 0.5 },
                on_release=lambda x, codigo=codigoBR: self.aumentar_cantidad(codigo)
            )
            btn_restar = Button(
                text='[b]-[/b]',
                markup = True,
                size_hint=(1, .8),
                background_normal='',
                background_color=(0.86, 0.01, 0.01, 1),
                pos_hint = {'center_y': 0.5 },
                on_release=lambda x, codigo=codigoBR: self.restar_cantidad(codigo)
            )
            acciones_superior.add_widget(btn_aumentar)
            acciones_superior.add_widget(btn_restar)

            # Botón de eliminar (fila inferior)
            btn_eliminar = Button(
                text='[b]Eliminar[/b]',
                markup=True,
                color=(1, 1, 1, 1),
                background_normal='',
                pos_hint = {'center_y': 0.5 },
                background_color=(0.86, 0.01, 0.01, 1),
                size_hint=(1, .9),  # Ocupa todo el ancho del contenedor
                on_release=lambda x, codigo=codigoBR: self.eliminar_producto(codigo)
            )

            # Añadir las filas al contenedor principal
            acciones_contenedor.add_widget(acciones_superior)  # Fila superior con aumentar y restar
            acciones_contenedor.add_widget(btn_eliminar)       # Fila inferior con eliminar

            # Agregar el contenedor de acciones al grid
            grid.add_widget(acciones_contenedor)
            total_compra +=precio_total
            descuento_total += descuento_producto
            total_formateado = f"$ {total_compra}"
            descuento_formateado = f"$ {descuento_total}"
            self.ids.descuento.text =descuento_formateado
            self.ids.total_pagar.text =total_formateado
            self.ids.total_productos.text =str(totalproductos)
            
    def comprobar_texto(self, instance, focus):
        venta.modo_busqueda()
        grid = self.ids.productos_grid
        header_labels = self.ids.header_labels
        header_labels.clear_widgets() 
        grid.cols = 6
        
        label_nombre = Label(
            text="Nombre Producto",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_nombre)

        label_stock = Label(
            text="Stock",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_stock)

        label_precio_unidad = Label(
            text="Precio x Unidad",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_precio_unidad)

        label_cantidad_mayorista = Label(
            text="Cantidad Mayorista",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_cantidad_mayorista)

        label_precio_mayorista = Label(
            text="Precio Mayorista",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_precio_mayorista)

        label_accion = Label(
            text="Acción",
            bold=True,
            color=(0, 0, 0, 1),
            font_size=self.width * 0.01
        )
        header_labels.add_widget(label_accion)
        
        
        if not focus:  
            venta.fuera_busqueda()
            grid = self.ids.productos_grid
            header_labels = self.ids.header_labels 
            header_labels.clear_widgets()
            grid.cols = 8
            
            label_nombre = Label(
                text="Nombre Producto",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_nombre)

            label_stock = Label(
                text="Stock",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_stock)

            label_precio_unidad = Label(
                text="Precio x Unidad",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_precio_unidad)

            label_cantidad_mayorista = Label(
                text="Cantidad Mayorista",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_cantidad_mayorista)

            label_precio_mayorista = Label(
                text="Precio Mayorista",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_precio_mayorista)

            label_cantidad = Label(
                text="Cantidad",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_cantidad)

            label_precio_total = Label(
                text="Precio Total",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_precio_total)

            label_accion = Label(
                text="Acción",
                bold=True,
                color=(0, 0, 0, 1),
                font_size=self.width * 0.01
            )
            header_labels.add_widget(label_accion)
            
    def filtrar_productos(self, texto):
        productos = venta.productos if venta.productos else []
        texto = texto.strip().lower()
        grid = self.ids.productos_grid
        grid.clear_widgets()
            
    
        # Ajustar las columnas del grid

            # Filtrar productos que coincidan con el texto ingresado
        productos_filtrados = [
            producto for producto in productos
            if texto in producto[2].lower() or texto in producto[10].lower()
        ]
            

        # Cargar los productos filtrados
        for producto in productos_filtrados:
            id_producto,id_proveedor,nombre_producto,precio_publico,precio_compra,precio_mayorista,unidad_medida,cantidad_inventario,cantidad_mayorista,categoria,codigo_barras = producto
                
                
            texto_truncado = nombre_producto[:20] + "..." if len(nombre_producto) > 20 else nombre_producto
            label_nombre = Label(
                text= texto_truncado,
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
                )
            self.add_mouse_over_event(label_nombre, nombre_producto)
            grid.add_widget(label_nombre)
                
            label_cantidad_stok = Label(
                text=str(cantidad_inventario),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad_stok)
                
            label_precio = Label(
                text=str(precio_publico),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio)
                            
            label_cantidad_mayorista = Label(
                text=str(cantidad_mayorista),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cantidad_mayorista)
                
            label_precio_mayorista = Label(
                text=str(precio_mayorista),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_precio_mayorista)

            # Acciones: Editar y Eliminar
            acciones = BoxLayout(orientation='horizontal', spacing=5)
            btn_agregar = Button(
                text='[b]Agregar ala Venta[/b]',
                markup= True,
                color=(1, 1, 1, 1),
                background_normal= '',
                background_color = (0.02, 0.81, 0, 1),
                size_hint_x=0.5,
                size_hint_y=0.5,
                pos_hint= {'center_y': 0.5},
                on_release=lambda x, codigoBR=codigo_barras: self.agregar_busqueda(codigoBR)
            )
            acciones.add_widget(btn_agregar)
            grid.add_widget(acciones)
        


    def aumentar_cantidad(self, codigo):
        
        venta.aumentar_cantidad(codigo)
        self.cargar_productos()
            
    def restar_cantidad(self, codigo):
        
        venta.restar_cantidad(codigo)
        self.cargar_productos()
            
    def eliminar_producto(self, codigo_barras):
        # Eliminar el producto de la lista de ventas
        venta.eliminar_producto(codigo_barras)
        self.ids.total_pagar.text ="$ 0.0"
        # Actualizar la cuadrícula para reflejar los cambios
        self.cargar_productos()
        
        
    def validar_producto(self):
        codigoBarras = self.ids.buscar_producto.text
        datos_producto=obtener_producto_codigoBR(codigoBarras)
        if not datos_producto: 
            self.ids.buscar_producto.text = ''
        else:
            self.show_popup_agregar(datos_producto, codigoBarras)
            
    def agregar_busqueda(self,codigoBarras):
        datos_producto=obtener_producto_codigoBR(codigoBarras)
        if not datos_producto: 
            self.ids.buscar_producto.text = ''
        else:
            self.show_popup_agregar(datos_producto, codigoBarras)
    
        
    def show_popup_agregar(self,datos_producto, codigoBR):
        """Muestra el Popup con la pantalla del RegistroUserScreen."""
        # Crea la pantalla del registro
        popup_content = AgregarProductoScreen()
        popup_content.cargar_producto(datos_producto,codigoBR)
        
        self.popup = Popup(title="Validar Producto",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    def show_popup_pago(self):
        # Crea la pantalla del registro
        totalPago = self.ids.total_pagar.text
        popup_content = ProcesarPagoScreen(totalPago)
        self.popup = Popup(title="Procesar Pago",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    def show_popup_productos_bajos(self):
        # Crea la pantalla del registro
        popup_content = StockBajoScreen()
        self.popup = Popup(title="productos bajos solicitar al proveedor",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           pos_hint={'center_x': 0.5 })
        self.popup.open()
        
    def show_popup_registrarDinero(self):
        # Crea la pantalla del registro
        popup_content = dinerodiaScreen()
        self.popup = Popup(title="Registrar Dinero en caja",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.cargar_productos()
            self.popup = None
            
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

    def actualizar_fecha_hora(self, *args):
        # Obtener la fecha y hora actual
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        # Actualizar el texto del Label con la fecha y hora
        self.ids.fecha_hora.text = ahora
        
    def redirect_Inventario(self, *args):
        app = App.get_running_app()
        app.root.current = 'inventario'
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_clientes(self, *args):
        app = App.get_running_app()
        app.root.current = 'clientes'
        
    def redirect_Proveedores(self, *args):
        app = App.get_running_app()
        app.root.current = 'proveedores'
    
    def redirect_Corte_Caja(self, *args):
        app = App.get_running_app()
        app.root.current = 'corte_caja'
        
    def redirect_Estadisticas(self, *args):
        app = App.get_running_app()
        app.root.current = 'inventario'
        
    def redirect_Estadisticas(self, *args):
        app = App.get_running_app()
        app.root.current = 'Estadisticas'
        
    def redirect_Retirar_dinero(self, *args):
        popup_content = egresardineroScreen()
        self.popup = Popup(title="Dinero retirar de la caja",
                           content=popup_content,
                           size_hint=(0.6, 0.8),
                           auto_dismiss=False)
        self.popup.open()