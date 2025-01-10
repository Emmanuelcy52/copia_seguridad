import re
from control.BDconsultas.inventario.CRUD import obtener_productos

class Venta:
    def __init__(self):
        self.venta_activa=[]

    def agregar_venta(self, datos_producto):
        codigo_barras = datos_producto["codigoBarras"]
        cantidad_a_agregar = float(datos_producto["CantidadVenta"])
        unidad_medida = datos_producto["unidad_medida"]
        stock_disponible = float(re.search(r'\d+(\.\d+)?', datos_producto["Stock"]).group())
        unidad_stock = datos_producto["Stock"].split()[-1]
        
        # Normalización de unidad_stock
        unidad_stock = unidad_stock.strip().lower()
        if unidad_stock in ['kilos', 'kilo', 'peso']:
            unidad_stock = 'kg'
        elif unidad_stock in ['metros', 'metro', 'longitud']:
            unidad_stock = 'm'
        elif unidad_stock.lower() in ['pieza','piezas']:
            unidad_stock = 'pieza'

        # Manejar conversión automática de g a kg y cm a m
        if unidad_medida == "g" and cantidad_a_agregar >= 1000:
            cantidad_a_agregar /= 1000  # Convertir gramos a kilogramos
            unidad_medida = "kg"
        elif unidad_medida == "cm" and cantidad_a_agregar >= 100:
            cantidad_a_agregar /= 100  # Convertir centímetros a metros
            unidad_medida = "m"

        # Si la unidad de medida no coincide con el stock, realizar conversiones necesarias
        if unidad_medida != unidad_stock:
            if unidad_medida == "g" and unidad_stock == "kg":
                cantidad_a_agregar /= 1000  # Convertir gramos a kilogramos
            elif unidad_medida == "kg" and unidad_stock == "g":
                cantidad_a_agregar *= 1000  # Convertir kilogramos a gramos
            elif unidad_medida == "cm" and unidad_stock == "m":
                cantidad_a_agregar /= 100  # Convertir centímetros a metros
            elif unidad_medida == "m" and unidad_stock == "cm":
                cantidad_a_agregar *= 100  
            elif unidad_medida.lower() == "pieza" and unidad_stock == "pieza":
                cantidad_a_agregar *= 1
            else:
                return "No se puede agregar el producto debido a unidades incompatibles."

        # Buscar si el producto ya existe en la lista
        for producto in self.venta_activa:
            if producto["codigoBarras"] == codigo_barras:
                cantidad_actual = float(producto["CantidadVenta"])
                nueva_cantidad = cantidad_actual + cantidad_a_agregar

                # Ajustar la cantidad al máximo permitido según el stock
                if nueva_cantidad > stock_disponible:
                    nueva_cantidad = stock_disponible

                # Actualizar la cantidad y mantener la unidad del stock
                producto["CantidadVenta"] = str(round(nueva_cantidad, 2))
                producto["unidad_medida"] = unidad_stock
                return "Cantidad ajustada correctamente."

        # Si no existe, verificar que la cantidad inicial no exceda el stock
        if cantidad_a_agregar > stock_disponible:
            cantidad_a_agregar = stock_disponible

        # Preparar y agregar el nuevo producto
        datos_producto["CantidadVenta"] = str(round(cantidad_a_agregar, 2))
        datos_producto["unidad_medida"] = unidad_stock
        self.venta_activa.append(datos_producto)
        return "Producto agregado correctamente."


    def aumentar_cantidad(self, codigo_barras):
        for producto in self.venta_activa:
            if producto["codigoBarras"] == codigo_barras:
                cantidad_actual = float(producto["CantidadVenta"])
                unidad_actual = producto["unidad_medida"]
                stock_disponible = float(re.search(r'\d+(\.\d+)?', producto["Stock"]).group())

                # Incrementar la cantidad según la unidad
                if unidad_actual == "cm":
                    incremento = 1 / 100  # 1 cm convertido a m
                elif unidad_actual == "g":
                    incremento = 1 / 1000  # 1 g convertido a kg
                else:
                    incremento = 1  # Para m o kg

                nueva_cantidad = cantidad_actual + incremento

                # Ajustar la cantidad al máximo permitido según el stock
                if nueva_cantidad > stock_disponible:
                    nueva_cantidad = stock_disponible

                producto["CantidadVenta"] = str(round(nueva_cantidad, 2))  # Redondear a 2 decimales
                return round(nueva_cantidad, 2)  # Devolver la nueva cantidad

        return None  # Producto no encontrado


    def restar_cantidad(self, codigo_barras):
        for producto in self.venta_activa:
            if producto["codigoBarras"] == codigo_barras:
                cantidad_actual = float(producto["CantidadVenta"])

                # Decrementar la cantidad si es mayor a 1
                if cantidad_actual > 1:
                    cantidad_actual -= 1
                    producto["CantidadVenta"] = f"{cantidad_actual:.3f}"  # Formatear con 3 decimales
                return cantidad_actual  # Devolver la nueva cantidad, redondeada a 3 decimales

        return None  # Producto no encontrado

    def obtener_venta(self):
        datos=self.venta_activa
        if datos is None:
            datos = []
        return datos
    
    def eliminar_producto(self, codigo_barras):
        self.venta_activa = [producto for producto in self.venta_activa if producto["codigoBarras"] != codigo_barras]

    def limpiar_venta(self):
        self.venta_activa = []
        
    def modo_busqueda(self):
        self.productos = obtener_productos()
        
    def fuera_busqueda(self):
        self.productos = None
        

# Instancia global de la sesión
venta = Venta()