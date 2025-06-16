import cv2
import easyocr
import numpy as np
from gtts import gTTS


# 1) Cargar imagen original
ruta_original = './pruebas/imagen_mercadona_prueba.jpg'
imagen = cv2.imread(ruta_original)

#2) Inicializo EASYOCR
reader = easyocr.Reader(['es'],gpu=False)

#3) Leer texto
resultado = reader.readtext(imagen)

texto_total = ""

#4) Organizar retorno //////// (_ no le da importancia a ese valor)
for x in resultado:
    
    print(f' Texto: "{x[1]} ---- Confianza {round(x[2], 2)}')
    #Creo los puntos de trackeo (cuadro delimitador que envuelve el texto)
    # Asegurarse de que sean tuplas de enteros
    punto_cero = tuple(map(int, x[0][0]))
    punto_uno = tuple(map(int, x[0][1]))
    punto_dos = tuple(map(int, x[0][2]))
    punto_tres = tuple(map(int, x[0][3]))


    cv2.rectangle(imagen,punto_cero,punto_dos,color=(160, 32, 240),thickness=4)
    
    #Añado el texto leido arriba del rectangulo
    cv2.putText(imagen,x[1],(punto_cero[0],punto_cero[1]), 2, 0.5,color=(255,255,255) )

    cv2.circle(imagen,punto_cero, radius=2, color=(255,0,0), thickness=2)
    cv2.circle(imagen,punto_uno, radius=2, color=(0,255,0), thickness=2)
    cv2.circle(imagen,punto_dos,radius=2, color=(0,0,255), thickness=2)
    cv2.circle(imagen,punto_tres,radius=2,color=(0,255,255),thickness=2)
    texto_total += x[1] + ". "
    
    
tts = gTTS(texto_total,lang='es')
tts.save("audio.mp3")




cv2.imshow('IMAGEN', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()



