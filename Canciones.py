class Cancion:
    def __init__(self, id, nombre, artista, album, imagen, fecha, l_spotify, l_youtube):
        self.id = id
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.fecha = fecha
        self.l_spotify = l_spotify
        self.l_youtube = l_youtube
    
    def getID(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getArtista(self):
        return self.artista
    
    def getAlbum(self):
        return self.album

    def getImagen(self):
        return self.imagen

    def getFecha(self):
        return self.fecha

    def getSpotify(self):
        return self.l_spotify
    
    def getYoutube(self):
        return self.l_youtube

    def setID(self, id):
        self.id = id

    def setNombre(self, nombre):
        self.nombre = nombre

    def setArtista(self, artista):
        self.artista = artista
    
    def setAlbum(self, album):
        self.album = album

    def setImagen(self, imagen):
        self.imagen = imagen

    def setFecha(self, fecha):
        self.fecha = fecha

    def setSpotify(self, spotify):
        self.l_spotify = spotify
    
    def setYoutube(self, youtube):
        self.l_youtube = youtube