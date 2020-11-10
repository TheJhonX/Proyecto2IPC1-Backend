class Comentario:
    def __init__(self, id, usuario, coment):
        self.id = id
        self.usuario = usuario
        self.coment = coment
    
    def getID(self):
        return self.id
    
    def getUsuario(self):
        return self.usuario

    def getComentario(self):
        return self.coment

    def setID(self, id):
        self.id = id
    
    def setUsuario(self, usuario):
        self.usuario = usuario

    def setComentario(self, comment):
        self.coment = comment
