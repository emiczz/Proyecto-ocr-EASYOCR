import cv2
import easyocr
import os

# ------------------------------------------
# 1) Cargar imagen original
# ------------------------------------------
ruta_original = ''
imagen = cv2.imread(ruta_original)
if imagen is None:
    print(f"❌ No se pudo cargar la imagen.\n   Revisa la ruta: {os.path.abspath(ruta_original)}")
    exit(1)
else:
    print(f"✅ Imagen original cargada: {ruta_original}")

# ------------------------------------------------------
# 2) Preprocesamiento: escala de grises, suavizado, CLAHE
# ------------------------------------------------------
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
contraste = clahe.apply(suavizado)

# ------------------------------------------------------
# 3) Inicializar EasyOCR
# ------------------------------------------------------
reader = easyocr.Reader(['es'])

# ------------------------------------------------------
# 4) Probar solo combinaciones útiles
# ------------------------------------------------------
parametros = [(11, 2), (31, 10), (51, 15)]
mejores_resultados = []
# OCR sin binarizar (sólo contraste)
sin_binarizar = reader.readtext(contraste)
conf_sin_bin = sum([c for _, _, c in sin_binarizar])
mejores_resultados.append(("sin binarizar", "-", conf_sin_bin, sin_binarizar))


print("\n🔍 Probando 3 combinaciones de binarización...")

for block_size, C in parametros:
    binaria = cv2.adaptiveThreshold(
        contraste, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size, C
    )
    # OCR directamente sobre el array (sin guardar en disco)
    resultados = reader.readtext(binaria)
    total_confianza = sum([c for _, _, c in resultados])
    mejores_resultados.append((block_size, C, total_confianza, resultados))

# ------------------------------------------------------
# 5) Elegir la mejor combinación
# ------------------------------------------------------
mejores_resultados.sort(key=lambda x: x[2], reverse=True)
mejor_block, mejor_C, _, textos = mejores_resultados[0]

print(f"\n🏆 Mejor combinación:")
print(f"   ➤ block_size = {mejor_block}")
print(f"   ➤ C = {mejor_C}")

print("\n📜 Textos extraídos:")
for _, texto, confianza in textos:
    print(f"   ➤ \"{texto}\" (confianza: {confianza:.2f})")

# ------------------------------------------------------
# 6) Mostrar imagen binarizada (opcional)
# ------------------------------------------------------
if mejor_block == "sin binarizar":
    print("✅ La mejor opción fue usar la imagen con contraste, sin binarizar.")
    binaria_final = contraste
else:
    print(f"✅ La mejor opción fue binarizar con block_size = {mejor_block}, C = {mejor_C}")
    binaria_final = cv2.adaptiveThreshold(
        contraste, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        mejor_block, mejor_C
    )

cv2.imshow("Imagen Binarizada (Mejor)", binaria_final)
cv2.waitKey()
cv2.destroyAllWindows()

