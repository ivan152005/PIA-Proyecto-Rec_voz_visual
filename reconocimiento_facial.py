from pathlib import Path
import cv2
import face_recognition as fr


# Cargar imagenes
def cargar_imagenes(path_list):
    # La primera será una foto de control, el resto de pruebas
    fotos = []
    for path in path_list:
        fotos.append(fr.load_image_file(path))
    return fotos


def asignar_perfil_color(fotos_list):
    for i in range(len(fotos_list)):
        fotos_list[i] = cv2.cvtColor(fotos_list[i], cv2.COLOR_BGR2RGB)
    return fotos_list


# top, right, botton, left
def localizar_cara(fotos_list):
    locations = []
    for i in fotos_list:
        locations.append(fr.face_locations(i)[0]) #puede detectar más caras... nos quedamos con la primera
    return locations


def get_cod_faces(fotos_list):
    cod_faces = []
    for i in fotos_list:
        cod_faces.append(fr.face_encodings(i)[0])
    return cod_faces

# (left, top), (right, bottom)
def draw_rectangles(fotos_list, locations):
    for (f, l) in zip(fotos_list, locations):
        cv2.rectangle(f,
                      (l[3], l[0]),
                      (l[1], l[2]),
                      (0, 255, 0), 2)


def show_imgs(fotos_list):
    for index, f in enumerate(fotos_list):
        cv2.imshow(f'Foto {index}', f)

# Por defecto, el valor de la distancia para determinar si es true o false es 0.6
def compare_all_with_control(cara_cod_list):
    results = []
    for i,fc in enumerate(cara_cod_list):
        if i > 0:
            # Con fr.compare_faces([control_cod], cara_cod_comparar, 0.3) podemos modificar el límite por el que determinaría si es true
            diferencias = {'misma_cara': fr.compare_faces([cara_cod_list[0]], fc),
                           'distancia': fr.face_distance([cara_cod_list[0]], fc)}
        elif i == 0:
            diferencias = { 'misma_cara': 'control',
                            'distancia': '0'}
        results.append(diferencias)

    return results

def show_results(fotos_list, results):
    for d,f in zip(results, fotos_list):
        resultado = d['misma_cara']
        distancia = d['distancia'][0]
        cv2.putText(f, f'{resultado} :::: {distancia}',
                    (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
