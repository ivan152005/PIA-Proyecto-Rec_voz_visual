from pathlib import Path
import cv2
import face_recognition as fr

IMAGES_DIR = Path("imagenes")

# Captura una foto desde la cámara
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


# Obtiene la codificación de una imagen
def codificar_rostro(imagen):
    rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    caras = fr.face_locations(rgb)

    if len(caras) == 0:
        return None

    return fr.face_encodings(rgb, caras)[0]


# Carga todas las imágenes registradas y sus codificaciones
def cargar_usuarios_registrados():
    codificaciones = []
    nombres = []

    for img_path in IMAGES_DIR.glob("*.jpg"):
        imagen = fr.load_image_file(img_path)
        face_locations = fr.face_locations(imagen)

        if len(face_locations) == 0:
            continue

        encoding = fr.face_encodings(imagen, face_locations)[0]

        nombre = img_path.stem.replace("usuario_", "")
        codificaciones.append(encoding)
        nombres.append(nombre)

    return codificaciones, nombres


# Compara un rostro capturado con la base de usuarios
def identificar_usuario(encoding_actual, codificaciones, nombres):
    if encoding_actual is None:
        return None

    coincidencias = fr.compare_faces(codificaciones, encoding_actual)
    distancias = fr.face_distance(codificaciones, encoding_actual)

    if len(distancias) == 0:
        return None

    mejor_indice = distancias.argmin()

    if coincidencias[mejor_indice]:
        return nombres[mejor_indice]

    return None


# FUNCIÓN PRINCIPAL
def reconocer_usuario():
    foto = capturar_foto()
    if foto is None:
        return None, None

    encoding_actual = codificar_rostro(foto)
    if encoding_actual is None:
        print("No se detectó rostro en la imagen.")
        return None, foto

    codificaciones, nombres = cargar_usuarios_registrados()

    usuario = identificar_usuario(encoding_actual, codificaciones, nombres)
    return usuario, foto