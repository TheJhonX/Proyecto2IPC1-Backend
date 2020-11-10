from flask import Flask, jsonify, request
from flask_cors import CORS
from Persona import Personas
from Admins import Administrador
from Canciones import Cancion
from Comentarios import Comentario
import pdfkit
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
CORS(app)

Usuarios = []
Administradores = []
L_canciones = []
L_comentarios = []
My_playlist = []
L_Solicitudes = []
cont_canciones = 0
cont_solicitudes = 0

Administradores.append(Personas("Usuario", "Maestro","admin", "admin"))

@app.route('/', methods=['GET'])
def rutainicial():
    return ("<h1>hola culos</h1>")

#Trae a todos los usuarios
@app.route('/Personas', methods=['GET'])
def rutapersonas():
    global Usuarios
    Datos = []
    for usuario in Usuarios:
        Dato = {
                'nombre': usuario.getNombre(),
                'apellido': usuario.getApellido(),
                'usuario': usuario.getUsuario()
            }
        Datos.append(Dato)
    respuesta = jsonify(Datos)
    return (respuesta)

#Agrega un usuario
@app.route('/Personas', methods=['POST'])
def AgregarUsuario():
    global Usuarios
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    username = request.json['usuario']
    password = request.json['password']
    flag = False
    for user in Usuarios:
        if user.getUsuario() == username:
            flag = True
            break
    if flag:
        return jsonify({
            'message':'failed',
            'reason':'El usuario ya está registrado'
        })
    else:
        nuevo = Personas(nombre, apellido, username, password)
        Usuarios.append(nuevo)
        return jsonify({
            'message':'Success',
            'reason':'Se registró correctamente el usuario'
        })

#Agrega un usuario de tipo administrador
@app.route('/Admins', methods=['POST'])
def AgregarAdmin():
    global Administradores
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    username = request.json['usuario']
    password = request.json['password']
    flag = False
    for adm in Administradores:
        if adm.getUsuario() == username:
            flag = True
            break
    if flag:
        return jsonify({
            'message':'failed',
            'reason':'El usuario administrador ya está registrado'
        })
    else:
        nuevo = Administrador(nombre, apellido, username, password)
        Administradores.append(nuevo)
        return jsonify({
            'message':'Success',
            'reason':'Se registró correctamente'
        })

#Trae a los usuario, es para mostrar el perfil (ya adaptado jsjsjs)
@app.route('/Personas/<string:username>', methods=['GET'])
def ObtenerPersona(username):
    global Usuarios
    global Administradores

    for adm in Administradores:
        if adm.getUsuario() == username:
            Dato = {
                'nombre': adm.getNombre(),
                'apellido': adm.getApellido(),
                'usuario': adm.getUsuario(),
                'password': adm.getPass()
            }
            return jsonify(Dato)

    for usuario in Usuarios:
        if usuario.getUsuario() == username:
            Dato = {
                'nombre': usuario.getNombre(),
                'apellido': usuario.getApellido(),
                'usuario': usuario.getUsuario(),
                'password': usuario.getPass()
            }
            return jsonify(Dato)
    return jsonify({'message': 'No hay ningun usuario'})

#Edita los datos del usuario, el perfil (ya adaptado jsjsjs)
@app.route('/Personas/Editar/<string:username>', methods=['POST'])
def ActualizarDatos(username):
    global Usuarios
    global Administradores
    
    if not(request.json['usuario'] == request.json['message']):
        for adm in Administradores:
            if request.json['usuario'] == adm.getUsuario():
                return jsonify({'message':'Failed'})

    for adm in Administradores:
        if adm.getUsuario() == username:
            adm.setNombre(request.json['nombre'])
            adm.setApellido(request.json['apellido'])
            adm.setUsuario(request.json['usuario'])
            adm.setPass(request.json['password'])
            return jsonify({
                'message':'Se actualizó correctamente',
                'usuario': request.json['usuario']
            })

    if not(request.json['usuario'] == request.json['message']):
        for usuario in Usuarios:
            if request.json['usuario'] == usuario.getUsuario():
                return jsonify({'message':'Failed'})

    for user in Usuarios:
        if user.getUsuario() == username:
            user.setNombre(request.json['nombre'])
            user.setApellido(request.json['apellido'])
            user.setUsuario(request.json['usuario'])
            user.setPass(request.json['password'])
            return jsonify({
                    'message':'Se actualizó correctamente',
                    'usuario': request.json['usuario']
            })
    return jsonify({'message': 'Failed'})

#Recupera la contraseña de un usuario (ya adaptado jsjsjs)
@app.route('/Personas/Recuperar/<string:user>', methods=['GET'])
def RecuperarPassword(user):
    global Usuarios
    global Administradores

    for adm in Administradores:
        if user == adm.getUsuario():
            Dato = {
                'message': 'Success',
                'password': adm.getPass()
            }
            return jsonify(Dato)

    for usuario in Usuarios:
        if user == usuario.getUsuario():
            Dato = {
                'message': 'Success',
                'password': usuario.getPass()
            }
            return jsonify(Dato)
    
    return jsonify({
        'message': 'failed',
        'reason': 'No se encontró al usuario ingresado'
    })

#Elimina un usuario
@app.route('/Personas/Eliminar/<string:user>', methods=['DELETE'])
def Eliminar_Usuario(user):
    global Usuarios
    for i in range(len(Usuarios)):
        if user == Usuarios[i].getUsuario():
            del Usuarios[i]
            break
    return jsonify({'message': 'El usuario se eliminó correctamente'})

#Traer todas las canciones
@app.route('/Canciones', methods=['GET'])
def ObtenerCanciones():
    global L_canciones
    temazos = []
    for song in L_canciones:
        temazo = {
            'id': song.getID(),
            'nombre': song.getNombre(),
            'artista': song.getArtista(),
            'album': song.getAlbum(),
            'imagen': song.getImagen(),
            'fecha': song.getFecha(),
            'spotify': song.getSpotify(),
            'youtube': song.getYoutube()
        }
        temazos.append(temazo)
    return jsonify(temazos)

#Crea una cancion
@app.route('/Canciones/Nueva', methods=['POST'])
def NuevaCancion():
    global L_canciones
    global cont_canciones
    nombre = request.json['nombre']
    artista = request.json['artista']
    album = request.json['album']
    imagen = request.json['imagen']
    fecha = request.json['fecha']
    spotify = request.json['spotify']
    youtube = request.json['youtube']
    nuevo = Cancion(cont_canciones,nombre,artista,album,imagen,fecha,spotify,youtube)
    L_canciones.append(nuevo)
    cont_canciones+=1
    return jsonify({'message': 'Succes'})

#Traer datos de una cancion
@app.route('/Canciones/<string:ids>',methods=['GET'])
def editar_cancion(ids):
    global L_canciones
    encontrado = False
    for song in L_canciones:
        if int(ids) == song.getID():
            Dato = {
                'message': 'Success',
                'nombre': song.getNombre(),
                'artista': song.getArtista(),
                'album': song.getAlbum(),
                'imagen': song.getImagen(),
                'fecha': song.getFecha(),
                'spotify': song.getSpotify(),
                'youtube': song.getYoutube()
            }
            encontrado = True
            break
    if (not encontrado):
        Dato = {
            'message': 'Failed'
        }

    return jsonify(Dato)

#Editar una cancion
@app.route('/Canciones/Editar/<string:ids>', methods=['POST'])
def Actualizar_Cancion(ids):
    global L_canciones
    for song in L_canciones:
        if int(ids) == song.getID():
            song.setNombre(request.json['nombre'])
            song.setArtista(request.json['artista'])
            song.setAlbum(request.json['album'])
            song.setImagen(request.json['imagen'])
            song.setFecha(request.json['fecha'])
            song.setSpotify(request.json['spotify'])
            song.setYoutube(request.json['youtube'])
            break
    return jsonify({'message': 'Se actualizó correctamente'})

#Eliminar una Cancion
@app.route('/Canciones/Eliminar/<string:ids>',methods=['DELETE'])
def Eliminar_Cancion(ids):
    global L_canciones
    for i in range(len(L_canciones)):
        if int(ids) == L_canciones[i].getID():
            del L_canciones[i]
            break
    return jsonify({'message': 'Se eliminó la cancion correctamente'})

#Comentarios de una cancion
@app.route('/Canciones/Comentario/<string:ids>', methods=['GET'])
def Comentarios(ids):
    global L_comentarios
    global L_canciones
    comentar = []
    for comments in L_comentarios:
        if int(ids) == comments.getID():
            for song in L_canciones:
                if song.getID() == comments.getID():
                    Dato = {
                        'usuario': comments.getUsuario(),
                        'comentario': comments.getComentario(),
                        'imagen': song.getImagen(),
                        'nombre': song.getNombre()
                    }
                    comentar.append(Dato)
                    
    if (len(comentar) == 0):
        for song in L_canciones:
            if song.getID() == int(ids):
                return jsonify({
                    'message': 'Failed',
                    'imagen': song.getImagen(),
                    'nombre': song.getNombre()
                    })
    else:
        return jsonify(comentar)

#Agrega un comentario
@app.route('/Canciones/Comentario/Agregar', methods=['POST'])
def AgregarComentario():
    global L_comentarios
    ids = int(request.json['id'])
    usuario = request.json['usuario']
    comment = request.json['comentario']
    nuevo = Comentario(ids,usuario,comment)
    L_comentarios.append(nuevo)
    return jsonify({'message': 'Success'})

#Agrega una cancion a la playlist
@app.route('/Canciones/playlist', methods=['POST'])
def AgregaraPlaylist():
    global My_playlist
    flag = False
    ids = request.json['id']
    if (len(My_playlist) != 0):
        for temazo in My_playlist:
            if int(temazo) == int(ids):
                flag = True
                break
    if (not flag):
        My_playlist.append(ids)

    return jsonify({'message': 'Se agregó a la playlist'})

#trae toda mi playlist
@app.route('/Canciones/playlist/c', methods=['GET'])
def MostrarPlaylist():
    global My_playlist
    global L_canciones
    temazos = []

    for ids in My_playlist:
        for song in L_canciones:
            if (song.getID() == int(ids)):
                temazo = {
                    'message': 'Success',
                    'nombre': song.getNombre(),
                    'artista': song.getArtista(),
                    'album': song.getAlbum(),
                    'imagen': song.getImagen(),
                    'fecha': song.getFecha(),
                    'spotify': song.getSpotify(),
                    'youtube': song.getYoutube(),
                    'id': song.getID()
                }
                temazos.append(temazo)
                break
    return jsonify(temazos)

#borra una cancion de mi playlist
@app.route('/Canciones/playlist/Borrar/<string:ids>', methods=['DELETE'])
def borrarDeMilista(ids):
    global My_playlist
    for i in range(len(My_playlist)):
        if int(ids) == int(My_playlist[i]):
            del My_playlist[i]
            return jsonify({'message': 'Se eliminó correctamente de tu playlist'})
    return jsonify({'message': 'Ocurrio un error'})

#agregar una solicitud
@app.route('/Canciones/Solicitud', methods=['POST'])
def AgregarSolicitud():
    global L_Solicitudes
    global cont_solicitudes
    nombre = request.json['nombre']
    artista = request.json['artista']
    album = request.json['album']
    imagen = request.json['imagen']
    fecha = request.json['fecha']
    spotify = request.json['spotify']
    youtube = request.json['youtube']
    nuevo = Cancion(cont_solicitudes,nombre,artista,album,imagen,fecha,spotify,youtube)
    L_Solicitudes.append(nuevo)
    cont_solicitudes+=1
    return jsonify({'message': 'Success'})

#trae todas las solicitudes
@app.route('/Canciones/Solicitudes', methods=['GET'])
def getSolicitudes():
    global L_Solicitudes
    a_solicitudes = []
    for soli in L_Solicitudes:
        req = {
            'message': 'Success',
            'nombre': soli.getNombre(),
            'artista': soli.getArtista(),
            'album': soli.getAlbum(),
            'imagen': soli.getImagen(),
            'fecha': soli.getFecha(),
            'spotify': soli.getSpotify(),
            'youtube': soli.getYoutube(),
            'id': soli.getID()
        }
        a_solicitudes.append(req)
    return jsonify(a_solicitudes)

#borra una solicitud
@app.route('/Canciones/Solicitud/Borrar/<string:ids>', methods=['DELETE'])
def borrarSolicitud(ids):
    global L_Solicitudes
    for i in range(len(L_Solicitudes)):
        if int(ids) == L_Solicitudes[i].getID():
            del L_Solicitudes[i]
            break
    return jsonify({'message': 'Se eliminó la solicitud correctamente'})

#Login
@app.route('/Login', methods=['POST'])
def Login():
    global Usuarios
    global Administradores
    username = request.json['usuario']
    password = request.json['password']

    for adm in Administradores:
        if adm.getUsuario() == username and adm.getPass() == password:
            return jsonify({
                'message': 'Success',
                'usuario': adm.getUsuario(),
                'tipo': 'administrador'
            })

    for usuario in Usuarios:
        if usuario.getUsuario() == username and usuario.getPass() == password:
            return jsonify({
                'message': 'Success',
                'usuario': usuario.getUsuario(),
                'tipo': 'cliente'
            })
    
    return jsonify({
        'message': 'failed',
        'usuario': ''
    })


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)

