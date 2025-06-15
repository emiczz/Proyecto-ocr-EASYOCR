import cv2
import easyocr
import numpy as np

# 1) Cargar imagen original
ruta_original = './pruebas/imagen_mercadona_prueba.jpg'
imagen = cv2.imread(ruta_original)

#2) Inicializo EASYOCR
reader = easyocr.Reader(['es'],gpu=False)

#3) Leer texto
resultado = reader.readtext(imagen)

#4) Organizar retorno //////// (_ no le da importancia a ese valor)
for coordenadas, texto, confianza in resultado:
    cords_limpias = [[int(x), int(y)] for x,y in coordenadas]
    print(f'Coordenadas: {cords_limpias} - Texto: "{texto}" - Confianza: {confianza:.2f}')
    #Creo los puntos de trackeo (cuadro delimitador que envuelve el texto)
    punto_cero = cords_limpias[0][0]
    punto_uno = coordenadas[0][1]
    punto_dos = coordenadas[0][2]
    punto_tres = coordenadas[0][3]

    cv2.circle(imagen,punto_cero, 2, color=(255,0,0), thickness=2)




cv2.imshow('IMAGEN', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()



