from reconocimiento_facial import reconocer_usuario
from asistente_voz import talk, registrar_usuario_por_voz, modo_asistente
from almacenamiento import guardar_imagen_usuario, guardar_usuario, registrar_asistencia, consultar_usuario
from usuario import Usuario


def ejecutar_sistema():
    nombre_reconocido, foto, encoding = reconocer_usuario()

    if nombre_reconocido is None:
        talk("No estás registrado. Vamos a realizar el proceso de registro.")

        nombre, dni = registrar_usuario_por_voz()
        if not nombre or not dni:
            talk("No se pudieron registrar tus datos.")
            return

        ruta_imagen = guardar_imagen_usuario(nombre, foto)

        nuevo_usuario = Usuario(
            nombre=nombre,
            dni=dni,
            ruta_imagen=ruta_imagen,
            encoding=encoding.tolist()
        )

        guardar_usuario(nuevo_usuario)
        talk(f"Registro completado. Bienvenido, {nuevo_usuario.nombre}.")
        return modo_asistente()

    talk(f"Hola {nombre_reconocido}, he reconocido tu rostro.")

    usuario = consultar_usuario(nombre_reconocido)

    if usuario:
        talk(f"Tu DNI es {usuario.dni}.")
        registrar_asistencia(usuario.nombre, usuario.dni)
        talk("Tu asistencia ha sido registrada.")
    else:
        talk("No encontré tus datos en el registro.")

    talk("¿Necesitas realizar alguna consulta?")
    modo_asistente()
