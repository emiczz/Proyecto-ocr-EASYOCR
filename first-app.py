import cv2
import easyocr
import os

# ------------------------------------------
# 1) Cargar imagen original (verificar ruta)
# ------------------------------------------
ruta_original = 'imagen5.jpg'
imagen = cv2.imread(ruta_original)
if imagen is None:
    print(f"❌ No se pudo cargar la imagen original.\n   Revisa que '{ruta_original}' exista en el directorio actual:\n   {os.getcwd()}")
    exit(1)
else:
    print(f"✅ Imagen original cargada correctamente: {ruta_original}")

# ------------------------------------------------------
# 2) Procesamiento con OpenCV: grises, contraste, etc.
# ------------------------------------------------------
# 2.1 Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# 2.2 Suavizar para reducir ruido
suavizado = cv2.GaussianBlur(gris, (5, 5), 0)

# 2.3 Aumentar contraste con CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
contraste = clahe.apply(suavizado)

# ------------------------------------------------------------
# 3) Inicializar EasyOCR y buscar mejores parámetros binarios
# ------------------------------------------------------------
reader = easyocr.Reader(['es'])

mejores_resultados = []
print("\n🔍 Probando combinaciones de umbral adaptativo...")

for block_size in range(11, 202, 20):  # Tamaños de bloque impares
    for C in range(5, 50, 5):          # Constantes a restar
        binaria = cv2.adaptiveThreshold(
            contraste, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size, C
        )
        tmp_path = "tmp_binaria.jpg"
        cv2.imwrite(tmp_path, binaria)
        img_tmp = cv2.imread(tmp_path)
        resultados = reader.readtext(img_tmp)
        total_confianza = sum([c for _, _, c in resultados])
        mejores_resultados.append((block_size, C, total_confianza, resultados))

# Ordenar y seleccionar la mejor combinación
mejores_resultados.sort(key=lambda x: x[2], reverse=True)
mejor_block, mejor_C, _, textos = mejores_resultados[0]

print(f"\n🏆 Mejor combinación encontrada:")
print(f"   ➤ block_size = {mejor_block}")
print(f"   ➤ C = {mejor_C}")

# Aplicar la mejor configuración
binaria_final = cv2.adaptiveThreshold(
    contraste, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    mejor_block, mejor_C
)

# ------------------------------------------
# 4) Extraer texto usando la mejor binaria
# ------------------------------------------
tmp_final = "mejor_binaria.jpg"
cv2.imwrite(tmp_final, binaria_final)
img_final = cv2.imread(tmp_final)

# Realizar OCR final con mejor imagen binarizada
textos_finales = reader.readtext(img_final)

print("\n📜 Textos extraídos con la mejor configuración:")
for bbox, texto, confianza in textos_finales:
    print(f"   ➤ \"{texto}\" (confianza: {confianza:.2f})")

# Opcional: mostrar imagen final binarizada
cv2.imshow("Mejor imagen binarizada", binaria_final)
cv2.waitKey(0)
cv2.destroyAllWindows()
