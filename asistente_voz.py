import datetime
import pyttsx3
import speech_recognition as sr
import unicodedata
from almacenamiento import (
    guardar_en_csv,
    consultar_usuario as buscar_dni,
    exportar_csv_a_json
)


# Motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

# Selección de voz en español
voices = engine.getProperty('voices')
for v in voices:
    if "Spanish" in v.name or "es" in v.id:
        engine.setProperty('voice', v.id)
        break

# Redefinir print para que también hable
import builtins
print_original = print
def print(*args, **kwargs):
    texto = " ".join(str(a) for a in args)
    engine.say(texto)
    engine.runAndWait()
    print_original(*args, **kwargs)

# Quitar tildes
def quitar_tildes(texto):
    if not texto:
        return texto
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

# Limpiar nombre
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
    dni = dni.upper()
    dni = dni.replace(" ", "")
    dni = dni.replace("-", "")
    dni = "".join(c for c in dni if c.isalnum())  # eliminar símbolos

    # Validación: 8 números + 1 letra al final
    if len(dni) == 9 and dni[:-1].isdigit() and dni[-1].isalpha():
        return dni

    return None


# Hablar
def talk(msg: str):
    print(msg)  # Hablar y mostrar por consola

# Voz a texto
def audio_to_text():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.7
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Reconocido: {text}")
            return text
        except sr.UnknownValueError:
            talk("No te entendí, repite por favor.")
            return audio_to_text()
        except sr.RequestError:
            talk("Error con el reconocimiento.")
            return None

# Saludo según hora
def saludo():
    hour = datetime.datetime.now().hour
    if hour < 6 or hour > 20:
        momento = "Buenas noches."
    elif hour < 13:
        momento = "Buenos días."
    else:
        momento = "Buenas tardes."
    talk(f"{momento} Vamos a registrar tus datos.")

# Registrar usuario
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
            talk("El DNI no es válido. Debe tener 8 números y una letra al final. Inténtalo de nuevo.")

    talk(f"He entendido: {nombre}, DNI {dni}.")
    guardar_en_csv(nombre, dni)
    talk("Tus datos han sido guardados correctamente.")
    return nombre, dni

# Consultar usuario
def consultar_usuario():
    talk("Dime el nombre del usuario que deseas consultar.")
    nombre_raw = audio_to_text()
    if not nombre_raw:
        talk("No pude entender el nombre.")
        return
    nombre = limpiar_nombre(nombre_raw)
    dni = buscar_dni(nombre)
    if dni:
        talk(f"El DNI de {nombre} es {dni}.")
    else:
        talk(f"No encontré ningún usuario llamado {nombre}.")

# Exportar CSV a JSON
def exportar_datos():
    ruta = exportar_csv_a_json()
    talk(f"Datos exportados correctamente. Archivo generado en {ruta}.")

# Modo asistente
def modo_asistente():
    talk("Puedes decir consultar usuario, exportar datos o salir.")
    while True:
        request = audio_to_text()
        if not request:
            continue
        r = request.lower()
        if "consultar" in r:
            consultar_usuario()
        elif "exportar" in r or "exportar datos" in r:
            exportar_datos()
        elif "salir" in r:
            talk("Hasta pronto.")
            break
