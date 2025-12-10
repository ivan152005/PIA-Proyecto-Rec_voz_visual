import datetime
import time
import pyttsx3
import speech_recognition as sr
import unicodedata
from almacenamiento import (
    consultar_usuario as buscar_usuario,
    exportar_json_a_csv
)

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
for v in voices:
    if "Spanish" in v.name or "es" in v.id:
        engine.setProperty("voice", v.id)
        break


def talk(msg: str):
    print(msg)
    try:
        engine.say(msg)
        engine.runAndWait()
    except:
        pass
    time.sleep(0.2)


def quitar_tildes(texto):
    if not texto:
        return texto
    return ''.join(c for c in unicodedata.normalize('NFKD', texto)
                   if not unicodedata.combining(c))


def limpiar_nombre(nombre):
    nombre = nombre.lower().strip()
    saludos = ["hola", "buenos dias", "buenos días", "buenas tardes", "buenas noches"]
    for s in saludos:
        if nombre.startswith(s):
            nombre = nombre.replace(s, "").strip()
    nombre = quitar_tildes(nombre)
    nombre = nombre.replace(" ", "_")
    return nombre


def limpiar_dni(dni):
    dni = dni.upper().replace(" ", "").replace("-", "")
    dni = "".join(c for c in dni if c.isalnum())
    if len(dni) == 9 and dni[:-1].isdigit() and dni[-1].isalpha():
        return dni
    return None


def audio_to_text():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.7

    with sr.Microphone() as source:
        talk("Escuchando...")

        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            talk("No detecté ninguna voz. Cerrando el programa.")
            exit()

        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"Reconocido: {text}")
            return text

        except sr.UnknownValueError:
            talk("No te entendí, repite por favor")
            return audio_to_text()

        except sr.RequestError:
            talk("Error con el servicio de reconocimiento")
            return None


def saludo():
    hora = datetime.datetime.now().hour
    if hora < 6 or hora > 20:
        momento = "Buenas noches."
    elif hora < 13:
        momento = "Buenos días."
    else:
        momento = "Buenas tardes."
    talk(f"{momento} Vamos a registrar tus datos.")


def registrar_usuario_por_voz():
    saludo()
    talk("¿Cómo te llamas?")
    nombre_raw = audio_to_text()

    if not nombre_raw:
        return None, None

    nombre = limpiar_nombre(nombre_raw)
    talk(f"De acuerdo, {nombre}. ¿Cuál es tu DNI?")

    dni = None
    while dni is None:
        dni_raw = audio_to_text()
        if not dni_raw:
            talk("No te entendí, repite el DNI.")
            continue

        dni = limpiar_dni(dni_raw)
        if dni is None:
            talk("El DNI no es válido. Debe tener 8 números y una letra. Inténtalo de nuevo.")

    talk(f"He entendido: {nombre}, DNI {dni}.")
    return nombre, dni


def consultar_usuario():
    talk("Dime el nombre del usuario que deseas consultar.")
    nombre_raw = audio_to_text()

    if not nombre_raw:
        talk("No pude entender el nombre.")
        return

    nombre = limpiar_nombre(nombre_raw)
    usuario = buscar_usuario(nombre)

    if usuario:
        talk(f"El DNI de {usuario.nombre} es {usuario.dni}.")
    else:
        talk(f"No encontré ningún usuario llamado {nombre}.")


def exportar_datos():
    ruta = exportar_json_a_csv()
    talk(f"Datos exportados correctamente. Archivo generado en {ruta}.")


def modo_asistente():
    talk("Puedes decir consultar usuario, exportar datos o salir.")
    while True:
        request = audio_to_text()
        if not request:
            continue

        r = request.lower()

        if "consultar" in r:
            consultar_usuario()
        elif "exportar" in r or "csv" in r:
            exportar_datos()
        elif "salir" in r:
            talk("Hasta pronto.")
            break
