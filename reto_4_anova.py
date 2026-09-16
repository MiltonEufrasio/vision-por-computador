import cv2
import numpy as np
import random
import time
from skimage.metrics import structural_similarity as ssim
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 1. Cargar e inyectar ruido Salt & Pepper (4%)
img_full = cv2.imread('entorno_slam.jpg', cv2.IMREAD_GRAYSCALE)
if img_full is None:
    print("Error: No se encontró la imagen 'entorno_slam.jpg'.")
    exit()

# Trabajamos sobre una ROI de 300x300 px para optimizar el bucle manual
img_original = img_full[400:700, 600:900]
alto, ancho = img_original.shape

def agregar_ruido_sp(imagen, prob=0.04):
    img_ruido = np.copy(imagen)
    for i in range(alto):
        for j in range(ancho):
            rnd = random.random()
            if rnd < prob / 2: img_ruido[i, j] = 0
            elif rnd > 1 - (prob / 2): img_ruido[i, j] = 255
    return img_ruido

# 2. Implementación de los 3 filtros MANUALES (sin OpenCV)
def aplicar_filtro_manual(imagen, tipo):
    img_f = np.copy(imagen)
    for i in range(1, alto - 1):
        for j in range(1, ancho - 1):
            vecindad = imagen[i-1:i+2, j-1:j+2].flatten()
            if tipo == 'media':
                img_f[i, j] = np.mean(vecindad)
            elif tipo == 'moda':
                valores, conteos = np.unique(vecindad, return_counts=True)
                img_f[i, j] = valores[np.argmax(conteos)]
            elif tipo == 'mediana':
                img_f[i, j] = np.median(vecindad)
    return img_f

# ==========================================
# ETAPA 1: ANÁLISIS ESTADÍSTICO (FILTROS MANUALES)
# ==========================================
replicas = 10
filtros_manuales = ['media', 'moda', 'mediana']
ssim_resultados = {f: [] for f in filtros_manuales}

print(f"Ejecutando Etapa 1: Evaluación Algorítmica ({replicas} réplicas por filtro)...")
for r in range(replicas):
    print("\n" "ensayo", r+1, "de", replicas)
    img_ruidosa = agregar_ruido_sp(img_original)
    for f in filtros_manuales:
        img_filtrada = aplicar_filtro_manual(img_ruidosa, f)
        val_ssim = ssim(img_original, img_filtrada, data_range=255)
        ssim_resultados[f].append(val_ssim)

# ANOVA Unidireccional entre los 3 filtros manuales
f_stat, p_val = stats.f_oneway(
    ssim_resultados['media'],
    ssim_resultados['moda'],
    ssim_resultados['mediana']
)

print("\n" + "="*55)
print("  ETAPA 1: ANÁLISIS DE VARIANZA (ANOVA) - FILTROS MANUALES")
print("="*55)
for f in filtros_manuales:
    m_ssim = np.mean(ssim_resultados[f])
    v_ssim = np.var(ssim_resultados[f])
    print(f"Filtro {f.upper():<8} -> Media SSIM: {m_ssim:.4f} | Varianza: {v_ssim:.6f}")

print("-" * 55)
print(f"Estadístico F: {f_stat:.4f}")
print(f"Valor p:       {p_val:.2e}")

# Prueba Post-Hoc de Tukey HSD
datos_ssim = []
grupos = []
for f in filtros_manuales:
    datos_ssim.extend(ssim_resultados[f])
    grupos.extend([f] * replicas)

tukey = pairwise_tukeyhsd(endog=datos_ssim, groups=grupos, alpha=0.05)

print("\n" + "="*55)
print("  PRUEBA POST-HOC DE TUKEY (Diferencia entre Filtros)")
print("="*55)
print(tukey)

# ==========================================
# ETAPA 2: COMPARACIÓN DE TIEMPOS DE EJECUCIÓN
# (Mediana Manual vs. Mediana OpenCV)
# ==========================================
print("\n" + "="*55)
print("  ETAPA 2: RENDIMIENTO COMPUTACIONAL (MEDIANA MANUAL vs OPENCV)")
print("="*55)

img_test = agregar_ruido_sp(img_original)

# Mediana Manual
t0 = time.time()
img_med_man = aplicar_filtro_manual(img_test, 'mediana')
t_manual = time.time() - t0

# Mediana OpenCV
t0 = time.time()
img_med_cv2 = cv2.medianBlur(img_test, 3)
t_cv2 = time.time() - t0

print(f"Tiempo Mediana Manual: {t_manual:.4f} s")
print(f"Tiempo Mediana OpenCV: {t_cv2:.4f} s")
print(f"Factor de Aceleración: {t_manual / t_cv2:.2f}x más rápido con OpenCV")