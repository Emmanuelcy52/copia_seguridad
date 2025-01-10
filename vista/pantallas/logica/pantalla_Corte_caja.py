import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from control.datos.datos import sesion
from kivy.uix.image import Image
from datetime import datetime
from control.BDconsultas.cortecaja.CRUD import obtener_ventas_corte,obtener_pagos,obtener_dinero_inicial,obtener_egreso,registrar_corte_caja,validad_corte
from control.BDconsultas.ventas.CRUD import obtener_detalles_venta_id
from control.BDconsultas.inventario.CRUD import obtener_producto_id
from kivy.uix.popup import Popup
from vista.pantallas.logica.popup.usuarios.pantalla_registro_user import RegistroUserScreen
from vista.pantallas.logica.popup.usuarios.pantalla_editar_usuario import EditarUserScreen
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

kv_path = os.path.join(os.path.dirname(__file__), '..','diseño', 'cortecaja.kv')
Builder.load_file(kv_path)

class CorteCajaScreen(Screen):
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    ruta_imagenes = StringProperty(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diseño', 'imagenes', 'icons'))
    )
    
    def on_enter(self):
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:
            self.ids.usuario.text = datos[1]
            self.id_usuario=datos[0]
        else:
            print("La sesión no está inicializada")
        fecha = datetime.now().strftime('%d/%m/%Y')   
        datos= validad_corte(fecha)
        if datos[0] == 'Iniciado':
            ventasDia = obtener_ventas_corte(fecha)
            if ventasDia:
                self.cargar_ventas()
            else:
                boton_corte = self.ids.boton_corte
                boton_corte.disabled = True
        else:
            boton_corte = self.ids.boton_corte
            boton_corte.disabled = True
            
    def cargar_ventas(self):
        """Crea los widgets dinámicamente para cada proveedor."""
        fecha = datetime.now().strftime('%d/%m/%Y')
        totalVentasDia = 0
        total_egresos = 0
        total_pagos = 0
        ventasDia = obtener_ventas_corte(fecha)
        grid = self.ids.Ventas_grid
        grid.clear_widgets() 
        saldo_dia = obtener_dinero_inicial(fecha)
        self.id_saldo = saldo_dia[0]
        self.ids.saldo_inicial.text = str(saldo_dia[1])
        datoegresos = obtener_egreso(self.id_saldo)
        datosPagos = obtener_pagos(fecha)
        if datoegresos != False:   
            for egresos in datoegresos:
                id,id_saldo_dia,monto_egresado,motivo_egreso,hora_egreso = egresos
                total_egresos +=monto_egresado
            label_totalRetiros = self.ids.total_retiros  
            self.add_mouse_over_event_egresos(label_totalRetiros)
        
        if datosPagos != False:
            for pagos in datosPagos:
                idpagos,id_credito,fecha_pago,monto,metodo_pago = pagos
                total_pagos +=monto
                label_totalpagos = self.ids.total_pagos
                self.add_mouse_over_event_pagos(label_totalpagos)
            
        for venta in ventasDia:
            id_venta,fechaventa,total_venta,dinero_recibido,cambio_devuelto,cantidad_productos,estatus,id_empleado = venta
            
            label_idVenta = Label(
                text=str(id_venta),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_idVenta)
            
            # Widget para el teléfono
            label_TotalVenta = Label(
                text= str(total_venta),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_TotalVenta)
            
            label_DineroRecibido = Label(
                text= str(dinero_recibido),
                color=(0, 0, 0, 1),
                text_size=(None, None),
                size_hint=(1, None),
                shorten=True,
                shorten_from='right'
            )
            grid.add_widget(label_DineroRecibido)

            
            label_cambio = Label(
                text=str(cambio_devuelto),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_cambio)
            
            label_totalProdcutos = Label(
                text=str(cantidad_productos),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            self.add_mouse_over_event(label_totalProdcutos, id_venta)
            grid.add_widget(label_totalProdcutos)
            
            label_estado = Label(
                text=str(estatus),
                color=(0, 0, 0, 1),
                text_size=(None, None),  # Tamaño inicial
                size_hint=(1, None),  # Asegura que el texto no expanda el widget
                shorten=True,  # Truncar texto si es demasiado largo
                shorten_from='right'  # Truncar desde la derecha
            )
            grid.add_widget(label_estado)
            
            totalVentasDia += total_venta
            
        self.ids.total_retiros.text = str(total_egresos)
        self.ids.total_pagos.text = str(total_pagos)
        self.ids.total_ventas.text = str(totalVentasDia)
        calculo_G_P= (saldo_dia[1] + totalVentasDia + total_pagos)- total_egresos

        if calculo_G_P >= saldo_dia[1]:
            self.ids.total_ganacia.color = (0, 0.8, 0, 1)
        else:
            self.ids.total_ganacia.color = (0.8,0, 0, 1)

        self.ids.total_ganacia.text = str(calculo_G_P)
        
    def cerrar_caja(self):
        saldo_dia = float(self.ids.saldo_inicial.text)
        total_venta = float(self.ids.total_ventas.text)
        total_retiros = float(self.ids.total_retiros.text)
        total_corte = float(self.ids.total_ganacia.text)
        fecha = datetime.now().strftime('%d/%m/%Y')
        respuesta = registrar_corte_caja(self.id_saldo,fecha,saldo_dia,total_venta,total_retiros,total_corte)
        if respuesta == 'Exito': 
            self.ids.message.text = "corte de caja cerrado"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 5)
            self.redirect_productos()
            return

    def show_tooltip(self, widget, text):
        """Muestra un popup con el texto completo."""
        id_productos_cantidades = obtener_detalles_venta_id(text)

        # Crear una lista de líneas con nombre y cantidad
        lineas_productos = []
        for id_producto, cantidad,unidad_medida in id_productos_cantidades:
            resultado = obtener_producto_id(id_producto)
            if len(resultado) > 2:  # Asegurarse de que el índice 2 existe
                nombre_producto = resultado[2]
                lineas_productos.append(f"producto: {nombre_producto}\ncantidad vendida: {cantidad} {unidad_medida}\n")  # Formato: nombre X cantidad

        # Unir todas las líneas en un solo texto, separados por saltos de línea
        texto_popup = "\n".join(lineas_productos)

        # Mostrar el popup
        popup = Popup(
            title='Información completa',
            content=Label(text=texto_popup),
            size_hint=(0.4, 0.4),  # Ajustar tamaño para mostrar varios nombres
            auto_dismiss=True
        )
        popup.open()
        
    def show_tooltip_egresos(self, widget):
        text = obtener_egreso(self.id_saldo)
        """Muestra un popup con los detalles del retiro en un ScrollView."""
        # Crear un layout para contener cada línea de texto en un Label
        if self.current_popup:
            self.current_popup.dismiss()
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        
        # Ajustar la altura del layout según el número de elementos que se van a mostrar
        layout.height = len(text) * 120  # Ajustar la altura del layout según el número de líneas

        for egresos in text:
            id, id_saldo_dia, monto_egresado, motivo_egreso, hora_egreso = egresos
            
            # Crear un Label para "Dinero retirado"
            label_monto = Label(
                text=f"Dinero retirado: {monto_egresado}",
                size_hint_y=None, 
                height=40,
                text_size=(500, None),  # Ajusta el texto al ancho del ScrollView
                halign='center',          # Alinea el texto a la izquierda
                valign='middle',        # Centra verticalmente el texto
                padding=(10, 0)  
            )
            layout.add_widget(label_monto)

            # Crear un Label para "Motivo", con ajuste de tamaño dinámico
            label_motivo = Label(
                text=f"Motivo: {motivo_egreso}",
                size_hint_y=None,
                height=40,  # Asignar un valor mínimo de altura
                text_size=(500, None),  # Ajusta el texto al ancho del ScrollView
                halign='center',          # Alinea el texto a la izquierda
                valign='middle',        # Centra verticalmente el texto
                padding=(10, 0)  
            )
            layout.add_widget(label_motivo)

            # Crear un Label para "Hora del retiro"
            label_hora = Label(
                text=f"Hora del retiro: {hora_egreso}", 
                size_hint_y=None, 
                height=40,
                text_size=(500, None),  # Ajusta el texto al ancho del ScrollView
                halign='center',          # Alinea el texto a la izquierda
                valign='middle',        # Centra verticalmente el texto
                padding=(10, 0)  
            )
            layout.add_widget(label_hora)

        # Crear el ScrollView y añadir el layout dentro de él
        scroll_view = ScrollView(size_hint=(None, None), size=(500, 300))
        scroll_view.add_widget(layout)

        # Crear el popup que contiene el ScrollView
        self.current_popup = Popup(title="Detalles de Egresos", content=scroll_view, size_hint=(None, None), size=(500, 400))
        self.current_popup.bind(on_dismiss=self.remove_popup)
        self.current_popup.open()
        
    def show_tooltip_pagos(self, widget):
        """Muestra un popup con los detalles del retiro en un ScrollView."""
        # Obtener la fecha actual y los detalles de los pagos
        fecha = datetime.now().strftime('%d/%m/%Y')
        text = obtener_pagos(fecha)

        # Cerrar cualquier popup abierto previamente
        if self.current_popup:
            self.current_popup.dismiss()

        # Crear un layout vertical para contener las etiquetas
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.height = len(text) * 120  # Ajustar la altura del layout según el número de líneas

        # Añadir detalles de cada pago al layout
        for pagos in text:
            idpagos, id_credito, fecha_pago, monto, metodo_pago = pagos

            # Crear y añadir etiquetas para cada detalle del pago
            label_monto = Label(
                text=f"Dinero pagado: {monto}",
                size_hint_y=None,
                height=40,
                text_size=(500, None),  # Ajusta el texto al ancho del ScrollView
                halign='center',          # Alinea el texto a la izquierda
                valign='middle',        # Centra verticalmente el texto
                padding=(10, 0)         # Opcional: agrega un espaciado interno a la izquierda
            )
            layout.add_widget(label_monto)

            label_fecha = Label(
                text=f"Fecha de pago: {fecha_pago}",
                size_hint_y=None,
                height=40,
                text_size=(500, None),
                halign='center',
                valign='middle',
                padding=(10, 0)
            )
            layout.add_widget(label_fecha)

            label_tipo_pago = Label(
                text=f"Tipo de pago: {metodo_pago}\n",
                size_hint_y=None,
                height=40,
                text_size=(500, None),
                halign='center',
                valign='middle',
                padding=(10, 0)
            )
            layout.add_widget(label_tipo_pago)

        # Crear un ScrollView para envolver el layout
        scroll_view = ScrollView(size_hint=(None, None), size=(500, 300))
        scroll_view.add_widget(layout)

        # Crear y mostrar el popup con el ScrollView como contenido
        self.current_popup = Popup(
            title="Detalles de pagos",
            content=scroll_view,
            size_hint=(None, None),
            size=(500, 400)
        )
        self.current_popup.bind(on_dismiss=self.remove_popup)
        self.current_popup.open()

    def add_mouse_over_event(self, widget, text):
        """Asocia el evento de mostrar el tooltip al pasar el mouse sobre el widget."""
        widget.bind(
            on_touch_down=lambda instance, touch: self.show_tooltip(widget, text)
            if widget.collide_point(*touch.pos) else None
        )
        
    def add_mouse_over_event_egresos(self, widget):
        """Asocia el evento de mostrar el tooltip al pasar el mouse sobre el widget."""
        widget.bind(
            on_touch_down=lambda instance, touch: self.show_tooltip_egresos(widget)
            if widget.collide_point(*touch.pos) else None
        )
        
    def add_mouse_over_event_pagos(self, widget):
        """Asocia el evento de mostrar el tooltip al pasar el mouse sobre el widget."""
        widget.bind(
            on_touch_down=lambda instance, touch: self.show_tooltip_pagos(widget)
            if widget.collide_point(*touch.pos) else None
        )
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Programar actualizaciones cada segundo
        Clock.schedule_interval(self.actualizar_fecha_hora, 1)
        self.current_popup = None
        
        
    def cerrarmensaje(self, *args):
        self.height_message = 0  # Restaura la altura del mensaje
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""   


    def actualizar_fecha_hora(self, *args):
        # Obtener la fecha y hora actual
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        # Actualizar el texto del Label con la fecha y hora
        self.ids.fecha_hora.text = ahora
        
        
    def dismiss_popup(self):
        """Cierra el popup si está abierto."""
        if self.popup:
            self.popup.dismiss()
            self.popup = None
            
    def remove_popup(self, instance):
        """Limpia la referencia del popup sin modificar directamente el contenido."""
        if self.current_popup == instance:
            self.current_popup = None
            
            
    def redirect_productos(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'
        
    def redirect_Inventario(self, *args):
        app = App.get_running_app()
        app.root.current = 'inventario'
        
    def redirect_Empleados(self, *args):
        app = App.get_running_app()
        app.root.current = 'empleados'
        
    def redirect_Proveedores(self, *args):
        app = App.get_running_app()
        app.root.current = 'proveedores'
        
    def redirect_clientes(self, *args):
        app = App.get_running_app()
        app.root.current = 'clientes'