class Sesion:
    def __init__(self):
        self.usuario_id = None
        self.nombre_usuario = None
        self.rol = None

    def iniciar_sesion(self, id_usuario,nombre_usuario,rol):
        self.usuario_id = id_usuario
        self.nombre_usuario = nombre_usuario
        self.rol=rol

    def obtener_usuario_id(self):
        datos=[self.usuario_id,self.nombre_usuario,self.rol]
        return datos

    def cerrar_sesion(self):
        self.usuario_id = None
        self.nombre_usuario = None
        self.rol = None

# Instancia global de la sesión
sesion = Sesion()
