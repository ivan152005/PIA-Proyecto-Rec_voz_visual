from reconocimiento_facial import reconocer_usuario
from asistente_voz import talk, registrar_usuario_por_voz, modo_asistente
from almacenamiento import guardar_imagen_usuario, consultar_usuario, guardar_usuario
from usuario import Usuario


def ejecutar_sistema():

    # Intentar reconocer el rostro del usuario
    nombre_reconocido, foto = reconocer_usuario()

    # No se reconoció o no existe en el sistema
    if nombre_reconocido is None:
        talk("No estás registrado. Vamos a realizar el proceso de registro.")

        nombre, dni = registrar_usuario_por_voz()

        if not nombre or not dni:
            talk("No se pudieron registrar tus datos.")
            return

        # Guardamos la foto y obtenemos su ruta
        ruta_imagen = guardar_imagen_usuario(nombre, foto)

        # Crear objeto Usuario y guardarlo
        usuario = Usuario(nombre=nombre, dni=dni, ruta_imagen=str(ruta_imagen))
        guardar_usuario(usuario)

        talk(f"Registro completado. Bienvenido, {usuario.nombre}.")
        modo_asistente()
        return

    # Usuario reconocido por su rostro
    talk(f"Hola {nombre_reconocido}, he reconocido tu rostro.")

    usuario = consultar_usuario(nombre_reconocido)

    if usuario:
        talk(f"Tu DNI es {usuario.dni}.")
    else:
        talk("No encontré tu DNI en la base de datos CSV.")

    talk("¿Necesitas realizar alguna consulta?")
    modo_asistente()


if __name__ == '__main__':
    ejecutar_sistema()