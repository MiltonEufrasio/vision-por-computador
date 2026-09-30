# Ejercicio 2 — Aprendizaje automático y profundo

Solución de los tres retos de la Guía Práctica 2:

1. **Cats&Dogs:** clasificación gato/perro. Descriptores clásicos (HOG, LBP, HSV) con SVM,
   gradient boosting y ensambles; CNN desde cero, MobileNetV2 y autoencoder; diseño
   factorial 3×3×3 sobre HOG y SVM con modelo de superficie de respuesta.
2. **3Scenes:** clasificación de escenas (costa, bosque, autopista). Réplica de las líneas
   base de clase, CNN propia, MobileNetV2 congelada y con ajuste fino, Grad-CAM y análisis
   del error según la textura de la imagen.
3. **VisDrone:** detección de objetos en imágenes de dron con YOLOv8. Diseño factorial 2²
   (tamaño de modelo × resolución de entrada), efectos, interacción y función de
   deseabilidad de Derringer–Suich.

## Contenido

| Carpeta / archivo | Descripción |
|---|---|
| `articulo_guia1.tex`, `articulo_guia1.pdf` | Artículo (plantilla IEEEtran; compilar dos veces con pdfLaTeX) |
| `notebooks/Etapa1_CatsDogs.ipynb` | Reto 1 |
| `notebooks/Etapa2_3Scenes.ipynb` | Reto 2 |
| `notebooks/Etapa3_VisDrone_DoE.ipynb` | Reto 3 |
| `resultados/etapa1/` | Tablas (CSV) y figuras del reto 1, incluidas las 27 corridas del diseño factorial (`doe_etapa1.csv`) |
| `resultados/etapa2/` | Tablas y figuras del reto 2 |
| `resultados/etapa3/` | Tablas, figuras y pesos entrenados de los cuatro modelos YOLO (`weights/`) |

El artículo lee las figuras directamente de `resultados/`, por lo que debe compilarse
desde esta carpeta.

## Cómo ejecutar

Los notebooks están pensados para Google Colab con GPU y descargan los datos
automáticamente:

- Cats&Dogs (Dataset500) y 3Scenes: desde los *releases* del repositorio del curso.
- VisDrone2019-DET: mediante Ultralytics (`data="VisDrone.yaml"`, ~2 GB).

Cada notebook monta Google Drive y guarda sus resultados en una carpeta `resultados/`;
ajuste la ruta `OUT` de la celda de Drive a su propia carpeta.

**Hardware usado:** retos 1 y 2 en GPU NVIDIA T4; reto 3 en una máquina G4 de Google Cloud
(NVIDIA RTX PRO 6000 Blackwell). Versiones: TensorFlow 2.20, PyTorch 2.11, Ultralytics 8.4.166.

## Datos

Los conjuntos de datos no se incluyen en el repositorio; los notebooks los descargan de sus
fuentes originales. Las etiquetas de clase originales de 3Scenes y VisDrone están en inglés;
en el artículo se usan sus nombres en español.
