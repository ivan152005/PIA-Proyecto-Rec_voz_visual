from pathlib import Path
import cv2
import face_recognition as fr
from almacenamiento import cargar_usuarios

IMAGES_DIR = Path("imagenes")


def capturar_foto():
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print("No se pudo acceder a la cámara.")
        return None

    print("Cámara abierta. Pulsa ENTER para capturar o ESC para cancelar.")

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            continue

        cv2.imshow("Captura de rostro", frame)
        key = cv2.waitKey(1)
        if key == 13:  # ENTER
            break
        elif key == 27:  # ESC
            frame = None
            break

    cam.release()
    cv2.destroyAllWindows()
    return frame


def codificar_rostro(imagen):
    rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    caras = fr.face_locations(rgb)
    if not caras:
        return None
    return fr.face_encodings(rgb, caras)[0]


def identificar_usuario(encoding_actual, usuarios):
    if encoding_actual is None:
        return None

    encodings_registrados = []
    nombres_registrados = []

    for u in usuarios:
        if u.encoding is not None:
            encodings_registrados.append(u.encoding)
            nombres_registrados.append(u.nombre)

    if not encodings_registrados:
        return None

    coincidencias = fr.compare_faces(encodings_registrados, encoding_actual)
    distancias = fr.face_distance(encodings_registrados, encoding_actual)
    mejor_indice = distancias.argmin()

    if coincidencias[mejor_indice]:
        return nombres_registrados[mejor_indice]

    return None


def reconocer_usuario():
    foto = capturar_foto()
    if foto is None:
        return None, None, None

    encoding_actual = codificar_rostro(foto)
    if encoding_actual is None:
        print("No se detectó rostro en la imagen.")
        return None, foto, None

    usuarios = cargar_usuarios()
    usuario_identificado = identificar_usuario(encoding_actual, usuarios)

    return usuario_identificado, foto, encoding_actual