import cv2
import numpy as np
import matplotlib.pyplot as plt
import random


# 1. Cargar imagen original (Limpia - Ground Truth)
img_full = cv2.imread('entorno_slam.jpg', cv2.IMREAD_GRAYSCALE)
if img_full is None:
    print("Error: No se encontró la imagen.")
    exit()

# Recorte de 300x300 px
img_original = img_full[400:700, 600:900]
alto, ancho = img_original.shape

# 2. Agregar ruido Salt & Pepper (4%)
def agregar_ruido_sp(imagen, prob=0.04):
    img_ruido = np.copy(imagen)
    for i in range(alto):
        for j in range(ancho):
            rnd = random.random()
            if rnd < prob / 2:
                img_ruido[i, j] = 0
            elif rnd > 1 - (prob / 2):
                img_ruido[i, j] = 255
    return img_ruido

img_ruidosa = agregar_ruido_sp(img_original)

# 3. Función unificada de Filtros Manuales SIN OpenCV (3x3)[cite: 1]
def filtro_manual(imagen, tipo='mediana'):
    img_filtrada = np.copy(imagen)
    borde = 1
    
    for i in range(borde, alto - borde):
        for j in range(borde, ancho - borde):
            vecindad = imagen[i-borde:i+borde+1, j-borde:j+borde+1].flatten()
            
            if tipo == 'mediana':
                img_filtrada[i, j] = np.median(vecindad)
            elif tipo == 'media':
                img_filtrada[i, j] = np.mean(vecindad)
            elif tipo == 'moda':
                valores, conteos = np.unique(vecindad, return_counts=True)
                img_filtrada[i, j] = valores[np.argmax(conteos)]
                
    return img_filtrada

# --- APLICACIÓN DE FILTROS

img_media = filtro_manual(img_ruidosa, tipo='media')
img_moda = filtro_manual(img_ruidosa, tipo='moda')
img_mediana_man = filtro_manual(img_ruidosa, tipo='mediana')
img_mediana_cv2 = cv2.medianBlur(img_ruidosa, 3)

# --- VISUALIZACIÓN ---
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
fig.canvas.manager.set_window_title('Evaluación Cuantitativa de Filtrado')

imagenes = [
    ("1. Original", img_original),
    ("2. Con Ruido", img_ruidosa),
    ("3. Media Manual", img_media),
    ("4. Moda Manual", img_moda),
    ("5. Mediana Manual", img_mediana_man),
    ("6. Mediana OpenCV", img_mediana_cv2)
]

for ax, (titulo, imagen) in zip(axs.flat, imagenes):
    ax.imshow(imagen, cmap='gray')
    ax.set_title(titulo)
    ax.axis('off')

plt.tight_layout()
plt.show()