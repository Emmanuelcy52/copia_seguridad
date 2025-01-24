import os
import sys
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from vista.pantallas.logica.pantalla_login import LoginScreen
from vista.pantallas.logica.principal import HomeScreen
from vista.pantallas.logica.Pantalla_inventario import InventrioScreen
from vista.pantallas.logica.proveedores import ProveedoresScreen
from vista.pantallas.logica.pantalla_empleados import EmpleadosScreen
from vista.pantallas.logica.pantalla_clientes import ClientesScreen
from vista.pantallas.logica.pantalla_Corte_caja import CorteCajaScreen
from vista.pantallas.logica.pantalla_estadisticas import EstadisticasScreen
import locale

# Función para rutas de recursos
def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller y desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable, busca en la carpeta temporal
        return os.path.join(sys._MEIPASS, relative_path)
    # Si se ejecuta como script, busca en el sistema de archivos normal
    return os.path.join(os.path.abspath("."), relative_path)

# Establece el locale a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class MyApp(MDApp):
    def build(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        Window.maximize()
        # Configura el tema de la aplicación
        self.theme_cls.theme_style = "Light"  # Opciones: 'Light' o 'Dark'
        self.theme_cls.primary_palette = "Blue"  # Cambia el color principal si lo deseas

        # Crear el gestor de pantallas
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(InventrioScreen(name='inventario'))
        sm.add_widget(ProveedoresScreen(name='proveedores'))
        sm.add_widget(ClientesScreen(name='clientes'))
        sm.add_widget(EmpleadosScreen(name='empleados'))
        sm.add_widget(CorteCajaScreen(name='corte_caja'))
        sm.add_widget(EstadisticasScreen(name='Estadisticas'))
        return sm

if __name__ == '__main__':
    MyApp().run()
