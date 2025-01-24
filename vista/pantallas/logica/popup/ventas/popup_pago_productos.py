import os
import re
import random
import win32print
import win32ui
from kivymd.uix.pickers import MDModalDatePicker
from datetime import datetime,timedelta
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from control.datos.datos_venta import venta
from control.datos.datos import sesion
from control.BDconsultas.grantia.CRUD import registar_garantia
from control.BDconsultas.inventario.CRUD import actualizarcantidad
from control.BDconsultas.creditos.CRUD import registro
from control.BDconsultas.clientes.CRUD import obtener_cliente_datos,validar_credito
from control.BDconsultas.ventas.CRUD import registrar_venta_efectivo,registrar_venta_credito,registrar_detalles_venta
import sys

# Función para obtener la ruta correcta según el entorno
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

kv_path = resource_path(os.path.join('vista', 'pantallas', 'diseño','popup','ventas','pago_productos.kv'))
Builder.load_file(kv_path)

class ProcesarPagoScreen(Screen):
    ruta_imagenes = StringProperty(
        resource_path(os.path.join('vista', 'pantallas', 'diseño', 'imagenes', 'icons'))
    )
    
    input_fecha_inicio = ObjectProperty(None)
    input_fecha_fin = ObjectProperty(None)
    height_message = NumericProperty(0) 
    size_hint_x_menssage = NumericProperty(0)
    size_hint_y_menssage = NumericProperty(0)
    total_pago_formateado = 0
    cambio = 0
    dinero_fromateado = 0
    tipo_venta = ''
    
    def __init__(self, totalPago,**kwargs):
        super().__init__(**kwargs)
        datos = sesion.obtener_usuario_id()
        if datos[0] is not None:  # Verifica si la sesión está configurada
            self.id_user = datos[0]
        else:
            print("La sesión no está inicializada")
        self.ids.label_total.text = f"Total a pagar: {totalPago}"
        self.total_pagar=self.ids.label_total.text
        self.ventaseleccion = False
        self.impreso = False
        self.grantiaActiva = False
        self.garantias=[]
        
    def on_spinner_tipo_pago_change(self, selected_value):
        if selected_value == "Efectivo":
            self.ids.input_dinero.disabled = False
            self.total_pago_formateado = int(re.search(r'\d+',self.total_pagar ).group())
            self.cambio = -self.total_pago_formateado
            self.ids.label_total.text = f"Total a pagar: ${self.total_pago_formateado}"
            self.ids.label_cambio.text = f"Cambio a Dar: ${self.cambio}"
            self.manejar_pago_efectivo()
        elif selected_value == "Credito":
            self.ids.input_dinero.disabled = False
            self.total_pago_formateado = int(re.search(r'\d+',self.total_pagar ).group())
            self.total_pago_formateado += self.total_pago_formateado * 0.10
            self.cambio = -self.total_pago_formateado
            self.ids.label_total.text = f"Total a pagar: ${self.total_pago_formateado}"
            self.ids.label_cambio.text = f"Cambio a Dar: ${self.cambio}"
            self.manejar_pago_credito()
            
    def manejar_pago_efectivo(self):
        self.cerrarmensaje()
        self.tipo_venta = self.ids.spinner_tipo_pago.text
        # Lógica para manejar el pago en efectivo

    def manejar_pago_credito(self):
        self.tipo_venta = self.ids.spinner_tipo_pago.text
        self.ventaseleccion = True
        # Mostrar mensaje con un Input para capturar datos del cliente
        self.ids.message.text = "Ingresa el número de teléfono o el nombre del cliente o el código de cliente:"
        self.ids.message.color = (0, 0, 1, 1)  # Color azul
        self.height_message = 10
        self.size_hint_x_menssage = .9
        self.size_hint_y_menssage = 0.3
                
        self.cliente_input = TextInput(
            multiline=False,
            size_hint=(1, None),
            height=40,  # Altura fija
            hint_text="Teléfono o Nombre"
        )
                
        self.ids.input_container.add_widget(self.cliente_input)
        # Lógica para manejar el pago a crédito
        
    def on_touch_imagen(self, args,imagen_id):
        # Verificar si el toque ocurrió dentro de la imagen
        touch = args[1]
        
        # Usar la imagen correcta según el identificador
        if imagen_id == "inicio":
            img = self.ids.img_calendario_inicio
        elif imagen_id == "fin":
            img = self.ids.img_calendario_fin
        else:
            return  # Si no es ninguna de las imágenes que esperamos, no hacer nada
        
        # Verifica si el toque está dentro de la imagen
        if img.collide_point(*touch.pos):
            if imagen_id == "inicio":
                self.mostrar_calendario_inicio()
            elif imagen_id == "fin":
                self.mostrar_calendario_fin()
        
        
    def devolver_cambio(self, texto):
        if texto == '':
            texto = "0.0"
        dinero_recivido = texto.strip().lower()
        self.dinero_fromateado = float(dinero_recivido)
        self.cambio = self.dinero_fromateado - self.total_pago_formateado
        self.ids.label_cambio.text = f"Cambio a Dar: ${self.cambio}"
        
    def validar_compra(self):
        print("dentro de validar")
        fecha = datetime.now().strftime('%d/%m/%Y')
        datos_venta = venta.obtener_venta()
        totalproductos = len(datos_venta)
        if self.ventaseleccion == False:
            print("dentro de if de ventaseleccion")
            if self.tipo_venta == "Seleccionar Tipo":
                self.ids.message.text = "Selecciona un tipo de pago"
                self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                self.height_message = 10
                self.size_hint_x_menssage = .9
                self.size_hint_y_menssage = 0.4
                Clock.schedule_once(self.cerrarmensaje, 3)
                return
            elif self.tipo_venta == "Efectivo":
                status = "Pago Completado"
                self.ventaseleccion = True
                if self.ids.input_dinero.text == "":
                    self.ids.input_dinero.text = "0.0"
                if float(self.ids.input_dinero.text) < self.total_pago_formateado:
                    print("dentro del mensaje")
                    self.ids.message.text = "El dinero recibido en compras en efectivo no puede ser menor al total"
                    self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                    self.height_message = 10
                    self.size_hint_x_menssage = .9
                    self.size_hint_y_menssage = 0.4
                    Clock.schedule_once(self.cerrarmensaje, 3)
                    self.ventaseleccion = False
                    return
                estado, id_venta = registrar_venta_efectivo(fecha, self.total_pago_formateado, self.dinero_fromateado, self.cambio, totalproductos, status,self.id_user)
                if estado == 'Exito':
                    for producto in datos_venta:
                        id_producto = int(producto['id_producto'])
                        unidad_medida = str(producto['unidad_medida'])
                        precio_publico = float(producto['precioPublico'])
                        precio_mayorista = float(producto['precioMayorista'])
                        cantidad = float(producto['CantidadVenta'])
                        cantidad_mayorista = int(producto['CantidadMayorista'])
                        
                        if  cantidad >= cantidad_mayorista:
                            subtotal = precio_mayorista * cantidad
                        else:
                            subtotal = precio_publico * cantidad
                            
                        respuesta = registrar_detalles_venta(id_venta,id_producto,cantidad,unidad_medida,subtotal)
                    if respuesta == 'Exito':
                            rest = actualizarcantidad(id_venta)
                            if rest == 'Exito':
                                self.impreso = self.imprimirtiket(datos_venta,self.total_pago_formateado,self.dinero_fromateado,self.cambio)
                                if self.impreso is True:
                                    venta.limpiar_venta()
                                    self.cerrarpopup()
                            else:
                                print('tienes errores: ',rest)
                else:
                    print(f"Error al registrar la venta: {estado}")    
        else:
            if self.tipo_venta == "Credito":
                status = "Pago a credito"
                if not self.cliente_input.text.strip():
                    self.ids.message.text = "Se necesita un dato del cliente para realizar la compra"
                    self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                    self.height_message = 10
                    self.size_hint_x_menssage = .9
                    self.size_hint_y_menssage = 0.4
                    Clock.schedule_once(self.cerrarmensaje, 3)
                    self.ventaseleccion = False
                    return
                else:
                    datoscliente = self.cliente_input.text.strip()
                    id_cliente = obtener_cliente_datos(datoscliente)
                    if id_cliente == "Error":
                        self.ids.message.text = "no existe cliente con esos datos"
                        self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                        self.height_message = 10
                        self.size_hint_x_menssage = .9
                        self.size_hint_y_menssage = 0.4
                        Clock.schedule_once(self.cerrarmensaje, 3)
                        self.ventaseleccion = False
                        return
                    cambiopositivo = abs(self.cambio)
                    if cambiopositivo == 0:
                        self.ids.message.text = "en compras a credito el cambio no puede ser $0.0\n     Cambia la forma de pago a !Efectivo!"
                        self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                        self.height_message = 10
                        self.size_hint_x_menssage = .9
                        self.size_hint_y_menssage = 0.4
                        Clock.schedule_once(self.cerrarmensaje, 5)
                        self.ventaseleccion = False
                        return
                    else:
                        valido = validar_credito(id_cliente,cambiopositivo)
                    
                    if valido == True:
                        estado, id_venta = registrar_venta_credito(fecha, self.total_pago_formateado, self.dinero_fromateado, self.cambio, totalproductos, status,self.id_user)
                        saldo_pendiente = self.total_pago_formateado - self.dinero_fromateado
                        
                        fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')

                        # Calcular fecha de inicio y fecha de fin
                        fecha_inicio = fecha_obj + timedelta(days=5)
                        fecha_fin = fecha_inicio + timedelta(days=30)

                        fecha_inicio_str = fecha_inicio.strftime('%d/%m/%Y')
                        fecha_fin_str = fecha_fin.strftime('%d/%m/%Y')
                        estatus_venta="Pago a credito"
                        
                        if estado == 'Exito':
                            for producto in datos_venta:
                                id_producto = int(producto['id_producto'])
                                unidad_medida = str(producto['unidad_medida'])
                                precio_publico = float(producto['precioPublico'])
                                precio_mayorista = float(producto['precioMayorista'])
                                cantidad = float(producto['CantidadVenta'])
                                cantidad_mayorista = int(producto['CantidadMayorista'])
                                
                                if  cantidad >= cantidad_mayorista:
                                    subtotal = precio_mayorista * cantidad
                                else:
                                    subtotal = precio_publico * cantidad
                                    
                                registrar_detalles_venta(id_venta,id_producto,cantidad,unidad_medida,subtotal)
                            respuesta = registro(id_cliente,id_venta,self.total_pago_formateado,saldo_pendiente,fecha_inicio_str,fecha_fin_str,estatus_venta)
                            if respuesta == 'Exito':
                                rest = actualizarcantidad(id_venta)
                                if rest == 'Exito':
                                    impreso = self.imprimirtiket(datos_venta,self.total_pago_formateado,self.dinero_fromateado,self.cambio)
                                    if impreso is True:
                                        venta.limpiar_venta()
                                        self.cerrarpopup()
                                else:
                                    print('tienes errores: ',rest)
                        else:
                            print(f"Error al registrar la venta: {estado}")
                    if valido == False:
                        self.ids.message.text = "El cliente ya no cuenta con credito disponible"
                        self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                        self.height_message = 10
                        self.size_hint_x_menssage = .9
                        self.size_hint_y_menssage = 0.4
                        Clock.schedule_once(self.cerrarmensaje, 3)
                        return
                    fecha = datetime.now().strftime('%d/%m/%Y')
                    datos_venta = venta.obtener_venta()
                    totalproductos = len(datos_venta)
                    
                    self.cerrarmensaje()
            else:
                # Continuar con lo que sigue si no es necesario agregar el Input
                fecha = datetime.now().strftime('%d/%m/%Y')
                datos_venta = venta.obtener_venta()
                totalproductos = len(datos_venta)
                
    def imprimirtiket(self, productos, total_compra, pago_con, cambio_devuelto):
        # Configuración del encabezado
        fecha_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        ticket_text = f"Tlapalería AguiYon\n"
        ticket_text += "Ubicacion:\n"
        ticket_text += '''Leandro Valle 5, Miraflores
        56647 San Mateo Tezoquipan 
        Miraflores, Méx.\n'''
        ticket_text += f"Fecha: {fecha_hora}\n"
        ticket_text += "TICKET DE COMPRA\n"
        ticket_text += "\n"

            # Recorrer productos y agregar al ticket
        for producto in productos:
            nombre = producto['nombreProducto']
            cantidad = float(producto['CantidadVenta'])
            cantidad_mayorista = float(producto['CantidadMayorista'])
            unidad_medida = producto['unidad_medida']
            if unidad_medida == 'pieza':
                unidad_medida = 'pz'
                cantidad = float(producto['CantidadVenta'])
                cantidad = int(cantidad)
            if cantidad >= cantidad_mayorista:
                precio = producto['precioMayorista']
            else:
                precio = producto['precioPublico']
            ticket_text += f"{nombre:<10} x {cantidad} {unidad_medida} ${float(precio):<5}\n"

        # Agregar totales y otros datos
        ticket_text += "\n"
        ticket_text += f"TOTAL:       ${total_compra:<5}\n"
        ticket_text += f"PAGO CON: ${pago_con:<5}\n"
        ticket_text += f"CAMBIO:   ${cambio_devuelto:<5}\n\n"
        ticket_text += "grantias activadas\n"
        if self.garantias:
            for garantia in self.garantias:
                ticket_text += f"Código de la garantía: \n"
                ticket_text += f"{garantia}\n"
            ticket_text += "Nota: no pierda este ticket\n"
            ticket_text += "Garantía no válida sin el ticket"
            ticket_text += "\n"
            ticket_text += "muchas gracias por su compra"
            ticket_text += "\n"
            ticket_text += "--------------------------------------\n\n"
        else:
            ticket_text += '''Nota: Este ticket 
            no incluye garantía\n'''
            ticket_text += "muchas gracias por su compra\n"
            ticket_text += "--------------------------------------\n\n"
        # Obtener la impresora predeterminada
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)

        # Crear el dispositivo de impresión
        printer_device = win32ui.CreateDC()
        printer_device.CreatePrinterDC(printer_name)

        try:
             # Iniciar el trabajo de impresión
            printer_device.StartDoc("Ticket de Compra")
            printer_device.StartPage()
            font=win32ui.CreateFont({
                "name": "Arial",
                "height": 30,
            })
            printer_device.SelectObject(font)

            # Configurar posición inicial en la hoja
            x, y = 10, 10
            line_spacing = 50  # Espaciado entre líneas

            # Escribir línea por línea del ticket
            for line in ticket_text.split("\n"):
                printer_device.TextOut(x, y, line.strip())  # Eliminar espacios innecesarios
                y += line_spacing

            # Finalizar el trabajo de impresión
            printer_device.EndPage()
            printer_device.EndDoc()
                

        except Exception as e:
            print(f"Error durante la impresión: {e}")
            # Cancelar el trabajo de impresión en caso de error
            win32print.AbortPrinter(hprinter)

        finally:
            printer_device.DeleteDC() 
            win32print.ClosePrinter(hprinter)
            return True

        

        
    def habilitar_garantia(self, is_active):
        numero = '0' + ''.join(str(random.randint(0, 9)) for _ in range(12))
        self.grantiaActiva = True
        
        # Obtener los campos de garantía por ID
        garantia_widgets = [
            self.ids.input_codigo_garantia,
            self.ids.input_fecha_inicio,
            self.ids.input_fecha_fin,
            self.ids.spinner_tipo_garantia
        ]

        # Cambiar el estado de los widgets
        for widget in garantia_widgets:
            widget.disabled = not is_active

        # Si se habilita, asignar el número generado al input_codigo_garantia
        if is_active:
            self.ids.input_codigo_garantia.text = numero
        else:
            self.ids.input_codigo_garantia.text = ''
            
    def agregargarantia(self):
        numero = '0' + ''.join(str(random.randint(0, 9)) for _ in range(12))
        datos_venta = venta.obtener_venta()
        producto_encontrado = False
        codigo = self.ids.input_codigo_garantia.text
        codigo_producto = self.ids.input_codigo_producto.text.strip()
        fecha_ini = self.ids.input_fecha_inicio.text
        fecha_final = self.ids.input_fecha_fin.text
        tipo_garantia = self.ids.spinner_tipo_garantia.text
        if tipo_garantia == 'Seleccionar Tipo':
            self.ids.message.text = "selecciona un tipo de garantia porfavor"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.2
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        elif fecha_ini == '':
            self.ids.message.text = "selecciona una fecha de inicio porfavor"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.2
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        elif fecha_final == '':
            self.ids.message.text = "selecciona una fecha de fin porfavor"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.2
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        elif codigo_producto == '':
            self.ids.message.text = "Ingresa el codigo de barras del producto porfavor"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        for producto in datos_venta:
            codigo_product = int(producto['codigoBarras'].strip())
            codigo_producto = int(codigo_producto.strip())
            if codigo_product == codigo_producto:
                id_producto = int(producto['id_producto'])
                nombre_producto = str(producto['nombreProducto'])
                respuesta = registar_garantia(codigo,id_producto,fecha_ini,fecha_final,tipo_garantia)
                producto_encontrado = True
                if respuesta == 'Exito':
                    self.ids.message.text = f"garantia aplicada al producto: {nombre_producto}"
                    self.ids.message.color = (0, 1, 0, 1)  # Color verde
                    self.height_message = 10
                    self.size_hint_x_menssage = .9
                    self.size_hint_y_menssage = 0.4
                    Clock.schedule_once(self.cerrarmensaje, 3)
                    self.garantias.append(codigo)
                    self.ids.input_codigo_garantia.text = numero
                    self.ids.input_codigo_producto.text = ''
                    self.ids.input_fecha_inicio.text = ''
                    self.ids.input_fecha_fin.text = ''
                    self.ids.spinner_tipo_garantia.text = 'Seleccionar Tipo'
                else:
                    self.ids.message.text = "error interno llama a soporte"
                    self.ids.message.color = (1, 0, 0, 1)  # Color rojo
                    self.height_message = 10
                    self.size_hint_x_menssage = .9
                    self.size_hint_y_menssage = 0.4
                    Clock.schedule_once(self.cerrarmensaje, 5)
                    return
                break
        if not producto_encontrado:    
            self.ids.message.text = "el producto ingresado no existe en la compra"
            self.ids.message.color = (1, 0, 0, 1)  # Color rojo
            self.height_message = 10
            self.size_hint_x_menssage = .9
            self.size_hint_y_menssage = 0.4
            Clock.schedule_once(self.cerrarmensaje, 3)
            return
        
    def cerrarpopup(self):
        app = App.get_running_app()
        venta_screen = app.root.get_screen('home')
        self.ids.message.text = ""
        venta_screen.dismiss_popup()
            
    
    def cerrarmensaje(self, *args):
        grid = self.ids.input_container
        grid.clear_widgets()
        self.height_message = 0
        self.size_hint_x_menssage = 0
        self.size_hint_y_menssage = 0
        self.ids.message.text = ""   
            
    def mostrar_calendario_inicio(self,*args):
        date_picker = MDModalDatePicker()
        date_picker.bind(on_ok=self.on_ok_inicio)
        # Conectar el evento de 'on_dismiss' al método 'cancelar_fecha'
        date_picker.bind(on_cancel=self.on_cancel)
        # Abrir el modal
        date_picker.open()
        
    def on_ok_inicio(self, instance_date_picker):
        value = instance_date_picker.get_date()[0]
        self.ids.input_fecha_inicio.text = value.strftime("%d/%m/%Y")
        instance_date_picker.dismiss()
        
    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()

    def mostrar_calendario_fin(self):
        date_picker = MDModalDatePicker()
        date_picker.bind(on_ok=self.on_ok_fin)
        date_picker.bind(on_cancel=self.on_cancel)
        date_picker.open()

    def on_ok_fin(self, instance_date_picker):
        value = instance_date_picker.get_date()[0]
        self.ids.input_fecha_fin.text = value.strftime("%d/%m/%Y")
        instance_date_picker.dismiss()
