from reconocimiento_facial import *
from asistente_voz import *
from almacenamiento import *


def ejecutar_sistema():

    usuario, foto = reconocer_usuario()

    # No se pudo capturar foto o no se detectó rostro
    if usuario is None:
        talk("No estás registrado. Vamos a realizar el proceso de registro.")
        nombre, dni = registrar_usuario_por_voz()

        if not nombre or not dni:
            talk("No se pudieron registrar tus datos.")
            return

        guardar_imagen_usuario(nombre, foto)

        talk(f"Registro completado. Bienvenido, {nombre}.")
        modo_asistente()
        return

    # Usuario reconocido por su rostro
    talk(f"Hola {usuario}, he reconocido tu rostro.")

    dni = consultar_usuario(usuario)
    if dni:
        talk(f"Tu DNI es {dni}.")
    else:
        talk("No encontré tu DNI en la base de datos CSV.")

    talk("¿Necesitas realizar alguna consulta?")
    modo_asistente()


if __name__ == '__main__':
    ejecutar_sistema()