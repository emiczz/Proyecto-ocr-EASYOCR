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
for x in resultado:
    
    print(f' Texto: "{x}')
    #Creo los puntos de trackeo (cuadro delimitador que envuelve el texto)
    punto_cero = x[0][0]
    punto_uno = x[0][1]
    punto_dos = x[0][2]
    punto_tres = x[0][3]

    cv2.circle(imagen,punto_cero, radius=2, color=(255,0,0), thickness=2)
    cv2.circle(imagen,punto_uno, radius=2, color=(0,255,0), thickness=2)
    cv2.circle(imagen,punto_dos,radius=2, color=(0,0,255), thickness=2)
    cv2.circle(imagen,punto_tres,radius=2,color=(0,255,255),thickness=2)





cv2.imshow('IMAGEN', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()



