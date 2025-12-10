from pathlib import Path
import csv
import json
import cv2
from usuario import Usuario
from datetime import datetime

DATA_DIR = Path("data")
IMAGES_DIR = Path("imagenes")

USUARIOS_JSON = DATA_DIR / "usuarios.json"
ASISTENCIA_JSON = DATA_DIR / "asistencia.json"
USUARIOS_CSV = DATA_DIR / "usuarios_export.csv"


def asegurar_estructura():
    DATA_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)

    # Crear JSON vacío si no existe
    if not USUARIOS_JSON.is_file():
        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    if not ASISTENCIA_JSON.is_file():
        with open(ASISTENCIA_JSON, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)



def cargar_usuarios():
    asegurar_estructura()

    with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Usuario.from_dict(u) for u in data]


def guardar_usuario(usuario: Usuario):
    asegurar_estructura()

    usuarios = cargar_usuarios()

    # Evitar duplicados por nombre
    usuarios = [u for u in usuarios if u.nombre != usuario.nombre]

    usuarios.append(usuario)

    with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4, ensure_ascii=False)


def guardar_imagen_usuario(nombre, foto):
    asegurar_estructura()

    ruta = IMAGES_DIR / f"usuario_{nombre.lower()}.jpg"
    cv2.imwrite(str(ruta), foto)
    return str(ruta)


#  CONSULTAR USUARIO POR NOMBRE
def consultar_usuario(nombre: str):
    nombre = nombre.lower()
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u.nombre == nombre:
            return u

    return None


#  REGISTRAR ASISTENCIA
def registrar_asistencia(nombre: str, dni: str):
    # Registra un evento de asistencia con fecha y hora
    asegurar_estructura()

    with open(ASISTENCIA_JSON, "r", encoding="utf-8") as f:
        registros = json.load(f)

    nuevo = {
        "nombre": nombre,
        "dni": dni,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S")
    }

    registros.append(nuevo)

    with open(ASISTENCIA_JSON, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)


#  EXPORTACIÓN: JSON a CSV
def exportar_json_a_csv():
    asegurar_estructura()

    usuarios = cargar_usuarios()

    with open(USUARIOS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Cabeceras
        writer.writerow(["nombre", "dni", "ruta_imagen", "encoding"])

        for u in usuarios:
            # encoding convertido a JSON para que sea legible en CSV
            encoding_str = json.dumps(u.encoding, ensure_ascii=False)

            writer.writerow([
                u.nombre,
                u.dni,
                u.ruta_imagen,
                encoding_str
            ])

    return USUARIOS_CSV
