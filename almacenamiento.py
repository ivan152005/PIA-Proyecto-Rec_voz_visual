from pathlib import Path
import csv
import json
import cv2

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


def guardar_en_csv(nombre, dni):
    asegurar_estructura()
    existe = CSV_PATH.is_file()

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["nombre", "dni"])

        writer.writerow([nombre.lower(), dni])


def consultar_usuario(nombre):
    nombre = nombre.lower()

    if not CSV_PATH.is_file():
        return None

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["nombre"].lower() == nombre:
                return row["dni"]

    return None


def cargar_todos_los_usuarios():
    if not CSV_PATH.is_file():
        return []

    usuarios = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            usuarios.append({"nombre": row["nombre"], "dni": row["dni"]})

    return usuarios


def exportar_csv_a_json():
    asegurar_estructura()
    usuarios = cargar_todos_los_usuarios()

    with open(JSON_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

    return JSON_EXPORT_PATH
