import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Leer imagen a color en OpenCV
img_path = 'entorno_slam.jpg'
img = cv2.imread(img_path)

if img is None:
    print("Error: No se pudo cargar la imagen. Verifica que 'entorno_slam.jpg' esté en la misma carpeta.")
    exit()

# 2. Imprimir forma (shape) de la imagen
print(f"Dimensiones de la imagen original (Shape): {img.shape}")
alto, ancho, canales = img.shape

def obtener_coords_por_pixel(x, y, size):
    """
    Calcula los límites (y1, y2, x1, x2) alrededor de un punto central (x, y) en píxeles.
    """
    y1 = max(0, y - size // 2)
    y2 = min(alto, y + size // 2)
    x1 = max(0, x - size // 2)
    x2 = min(ancho, x + size // 2)
    return (y1, y2, x1, x2)

# 3. Definir las 6 regiones de interés (5 homogéneas, 1 heterogénea)
rois = {
    "R1_Azul (Homogenea)": obtener_coords_por_pixel(1800, 700, 80),    # Cuadro azul en el checkerboard derecho
    "R2_Verde (Homogenea)": obtener_coords_por_pixel(900, 600, 80),   # Cuadro verde en el checkerboard derecho
    "R3_Rojo (Homogenea)": obtener_coords_por_pixel(200, 800, 80),    # Cuadro rojo en el checkerboard central
    "R4_pared (Homogenea)": obtener_coords_por_pixel(1900, 250, 80),  # Cajonera de madera
    "R5_Piso (Homogenea)": obtener_coords_por_pixel(900, 1200, 80),# Piso liso (Baja textura)
    "R6_panel + caja (Heterogenea)": obtener_coords_por_pixel(1870, 490, 80) # Patrones complejos de calibración
}

img_dibujada = img.copy()

print("\n--- ANÁLISIS ESTADÍSTICO DE CANALES (BGR) ---")
for nombre, (y1, y2, x1, x2) in rois.items():
    region = img[y1:y2, x1:x2]
    
    # 4. Obtener la media y desviación estándar de cada uno de los 3 canales[cite: 1]
    media_bgr = np.mean(region, axis=(0, 1))
    desv_bgr = np.std(region, axis=(0, 1))
    
    print(f"\n[{nombre}]")
    print(f"  Media (B, G, R): {media_bgr.round(2)}")
    print(f"  Desviación Estándar (B, G, R): {desv_bgr.round(2)}")
    
    # 5. Mostrar las regiones con un recuadro dibujado[cite: 1]
    color_caja = (0, 255, 0) if "Heterogenea" in nombre else (0, 0, 0)
    grosor = 4 if "Heterogenea" in nombre else 2
    cv2.rectangle(img_dibujada, (x1, y1), (x2, y2), color_caja, grosor)
    
    # Etiqueta visual corta
    etiqueta = nombre.split('_')[0]
    cv2.putText(img_dibujada, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_caja, 2)

# 6. Visualización final con Matplotlib
img_rgb = cv2.cvtColor(img_dibujada, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(12, 8))
plt.imshow(img_rgb)
plt.title("Extracción de ROIs: Homogéneas (Negro) vs Heterogéneas (verde)")
plt.axis('off')
plt.tight_layout()
plt.show()