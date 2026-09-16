import random
import math
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

# 1. Generación de matriz 1000x1000 sin librerías matriciales
start_time_manual = time.time()
filas, columnas = 1000, 1000
matriz = [[random.randint(0, 255) for _ in range(columnas)] for _ in range(filas)]

# 2. Cálculo matemático manual de estadísticos
def calcular_estadisticas(mat):
    vector = [val for fila in mat for val in fila]
    N = len(vector)
    mini, maxi, suma = vector[0], vector[0], 0
    
    for v in vector:
        if v < mini: mini = v
        if v > maxi: maxi = v
        suma += v
        
    media = suma / N
    suma_varianza = sum((v - media) ** 2 for v in vector)
    desviacion = math.sqrt(suma_varianza / N)
    return mini, maxi, media, desviacion, vector

mini, maxi, media, desv, vector_aplanado = calcular_estadisticas(matriz)

# 3. Guardar vector aplanado en archivo CSV local[cite: 1]
ruta_archivo = "sensor_noise_sim.csv"
with open(ruta_archivo, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(vector_aplanado)
tiempo_manual = time.time() - start_time_manual

# 4. Lectura desde archivo y cálculo con NumPy[cite: 1]
start_time_numpy = time.time()
vector_np = np.loadtxt(ruta_archivo, delimiter=',')
matriz_np = vector_np.reshape((filas, columnas))

# Estadísticos con NumPy[cite: 1]
mini_np = np.min(matriz_np)
maxi_np = np.max(matriz_np)
media_np = np.mean(matriz_np)
desv_np = np.std(matriz_np)
tiempo_numpy = time.time() - start_time_numpy

# 5. Salida comparativa completa por consola[cite: 1]
print("==================================================")
print("        RETO 1: COMPARACIÓN DE ESTADÍSTICOS       ")
print("==================================================")
print(f"MANUAL -> Mín: {mini:3d} | Máx: {maxi:3d} | Media: {media:6.2f} | Desv: {desv:6.2f} | Tiempo: {tiempo_manual:.4f}s")
print(f"NUMPY  -> Mín: {int(mini_np):3d} | Máx: {int(maxi_np):3d} | Media: {media_np:6.2f} | Desv: {desv_np:6.2f} | Tiempo: {tiempo_numpy:.4f}s")
print("--------------------------------------------------")
print(f"Diferencia de tiempo: {tiempo_manual - tiempo_numpy:.4f}s")

# 6. Visualización del mapa de ruido[cite: 1]
plt.figure(figsize=(7, 6))
plt.imshow(matriz_np, cmap='gray')
plt.title("Mapa de Ruido Sintético (Simulación de Sensor SLAM)")
plt.colorbar(label='Intensidad de Píxel (0-255)')
plt.tight_layout()
plt.show()