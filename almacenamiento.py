from pathlib import Path
import csv
import json
import cv2
from usuario import Usuario

DATA_DIR = Path("data")
IMAGES_DIR = Path("imagenes")

CSV_PATH = DATA_DIR / "usuarios.csv"
JSON_EXPORT_PATH = DATA_DIR / "usuarios_export.json"


def asegurar_estructura():
    DATA_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)


def guardar_imagen_usuario(nombre, foto):
    asegurar_estructura()
    ruta = IMAGES_DIR / f"usuario_{nombre.lower()}.jpg"
    cv2.imwrite(str(ruta), foto)
    return ruta


def guardar_usuario(usuario: Usuario):
    asegurar_estructura()
    existe = CSV_PATH.is_file()

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["nombre", "dni", "ruta_imagen"])

        writer.writerow([usuario.nombre, usuario.dni, usuario.ruta_imagen])


def consultar_usuario(nombre: str):
    nombre = nombre.lower()
    if not CSV_PATH.is_file():
        return None

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["nombre"].lower() == nombre:
                return Usuario(
                    nombre=row["nombre"],
                    dni=row["dni"],
                    ruta_imagen=row.get("ruta_imagen")
                )
    return None


def cargar_todos_los_usuarios():
    if not CSV_PATH.is_file():
        return []

    usuarios = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            usuarios.append(
                Usuario(
                    nombre=row["nombre"],
                    dni=row["dni"],
                    ruta_imagen=row.get("ruta_imagen")
                )
            )
    return usuarios


def exportar_csv_a_json():
    asegurar_estructura()
    usuarios = cargar_todos_los_usuarios()

    lista_dicts = [u.to_dict() for u in usuarios]

    with open(JSON_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

    return JSON_EXPORT_PATH
