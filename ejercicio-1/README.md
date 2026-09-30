# Ejercicio 1 — Visión por computador clásica

Solución de los cuatro retos de la Guía 1: representación matricial, convoluciones,
segmentación por color y filtrado de ruido.

## Contenido

| Archivo | Descripción |
|---|---|
| `main.tex`, `referencias.bib` | Artículo (compilar con pdfLaTeX + BibTeX) |
| `main.pdf` | Artículo compilado |
| `figuras/` | Figuras del artículo |
| `codigo/reto_1.py` | Reto 1: matriz 1000×1000 a imagen; estadísticas manuales frente a NumPy |
| `codigo/convolucion.xlsx` | Reto 2: convoluciones (Sobel y gaussiano) en Excel |
| `codigo/reto_3.py` | Reto 3: segmentación por color y regiones de interés |
| `codigo/reto_4.py` | Reto 4: filtros de ruido (media, mediana, moda, gaussiano) |
| `codigo/reto_4_anova.py` | Reto 4: comparación de filtros con SSIM, ANOVA y prueba de Tukey |
| `codigo/entorno_slam.jpg` | Imagen de entrada de los retos 3 y 4 |

**Sobre `entorno_slam.jpg`:** es una imagen sintética generada con IA (Google Gemini) que
emula un entorno de pruebas de SLAM; no es una fotografía real.

## Cómo ejecutar

Requiere Python 3 con `numpy`, `matplotlib`, `opencv-python`, `scikit-image`, `scipy` y
`statsmodels`. Ejecute los scripts desde la carpeta `codigo/`, porque leen la imagen de su
misma carpeta:

```bash
cd codigo
python reto_1.py
python reto_3.py
python reto_4.py
python reto_4_anova.py
```
