from pathlib import Path
from reconocimiento_facial import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    paths = []
    paths.append(Path('fotos', 'foto1.jpg'))
    paths.append(Path('fotos', 'foto2.jpg'))
    paths.append(Path('fotos', 'foto3.jpeg'))
    fotos_list = cargar_imagenes(paths)
    fotos_list = asignar_perfil_color(fotos_list)
    locations = localizar_cara(fotos_list)
    cod_faces = get_cod_faces(fotos_list)
    draw_rectangles(fotos_list, locations)
    results = compare_all_with_control(cod_faces)
    show_results(fotos_list, results)
    show_imgs(fotos_list)
    cv2.waitKey(0)
