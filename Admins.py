class Administrador:
    def __init__(self, nombre, apellido, usuario, password):
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.password = password

    def getNombre(self):
        return self.nombre

    def getApellido(self):
        return self.apellido

    def getUsuario(self):
        return self.usuario

    def getPass(self):
        return self.password

    def setNombre(self, nombre):
        self.nombre = nombre

    def setApellido(self, apellido):
        self.apellido = apellido
    
    def setUsuario(self, usuario):
        self.usuario = usuario

    def setPass(self, password):
        self.password = password