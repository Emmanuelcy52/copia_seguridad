import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
from control.datos.datos import sesion
from control.BDconsultas.inventario.CRUD import obtener_productos_bajos
from control.BDconsultas.proveedores.CRUD import obtener_proveedor_id
from kivy.properties import StringProperty

kv_path = os.path.join(os.path.dirname(__file__), '..','..','..','diseño','popup','proveedores','alerta_stock_bajo.kv')
Builder.load_file(kv_path)

class StockBajoScreen(Screen):
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'icons'))
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        self.cargar_productos_bajos()
        
    def on_enter(self):
        """Se llama cuando la pantalla está a punto de mostrarse."""
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:  # Verifica si la sesión está configurada
            self.ids.usuario.text = datos[1]
        else:
            print("La sesión no está inicializada")
        
            
    def cargar_productos_bajos(self):
        """Crea los widgets dinámicamente en forma de tarjetas para cada producto con bajo inventario."""
        productos = obtener_productos_bajos()
        grid = self.ids.productos_grid
        grid.clear_widgets()  # Limpia los widgets existentes

        # Número de columnas que deseas mostrar en el GridLayout

        for producto in productos:
            id_proveedor, nombre_producto, cantidad_inventario = producto
            datos_proveedor = obtener_proveedor_id(id_proveedor)
            id, nombre_empresa, correo_electronico, telefono, direccion, notas = datos_proveedor
            
            # Widget para el nombre del producto
            label_info_proveedor = Label(
                text='[b]Informacion proveedor[/b]',
                markup= True,
                color=(0, 0.15, 0.57, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_info_proveedor)
                
            label_nombre_proveedor = Label(
                text=f'Proveedor: {nombre_empresa}',
                color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_nombre_proveedor)
                
            label_telfono = Label(
                text=f'Contacto: {telefono}',
                color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_telfono)
                
            label_direccion = Label(
                text=f'Direccion: {direccion}',
                color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_direccion)
                
            label_infomacion = Label(
                text='[b]Infomacion del producto[/b]',
                markup= True,
                color=(0.33, 0, 0.57, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_infomacion)
            
            label_nombre = Label(
                text=f'Nombre del producto: {nombre_producto}',
                color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=18,
            )
            grid.add_widget(label_nombre)
            # Widget para la cantidad en inventario
            label_cantidad = Label(
                text=f"Cantidad Disponible: {cantidad_inventario}",
                color=(0, 0, 0, 1),
                size_hint=(1, None),
                height=40,
                shorten=True,
                shorten_from='right',
                font_size=16,
            )
            grid.add_widget(label_cantidad)

