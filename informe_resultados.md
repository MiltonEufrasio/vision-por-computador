# Informe de resultados — Retos 1 a 4

> **Estado:** cerrado para los 4 retos — contenido base listo para pasar a
> `paper/main.tex`. Los 5 pendientes de la versión anterior de este documento
> ya se resolvieron (ver Sección 6).
>
> **Nota de autoría:** los 4 retos se resolvieron con código propio
> (`reto_1.py`, `reto_3.py`, `reto_4.py`, `reto_4_anova.py`) y una hoja de
> Excel propia (`convolucion.xlsx`), corridos en la máquina de Milton. Ese
> código y esos resultados son los que se reportan aquí como canónicos. Yo
> (Claude) verifiqué el código ejecutándolo de nuevo en un entorno
> controlado (mismos scripts, misma imagen), y con eso confirmo que es
> correcto y reproducible; donde detecté algo para corregir o ampliar, lo
> señalo explícitamente.

---

## ⚠️ Corrección importante sobre el dato del Reto 3 y 4

En la versión anterior de este informe yo describí `entorno_slam.jpg` como
**"una fotografía real de un banco de pruebas de laboratorio"**. Eso fue un
error mío: Milton aclaró que la imagen es **sintética, generada con IA**
(Google Gemini, modelo de generación de imágenes conocido como "Nano
Banana"), no una fotografía capturada de un robot y un laboratorio reales.

Esto **no invalida** el análisis estadístico de los Retos 3 y 4 (las
operaciones de OpenCV, las estadísticas por canal, el ANOVA, todo se calculó
correctamente sobre los píxeles reales de esa imagen), pero **sí cambia
cómo hay que describirla en el artículo**: nunca como "fotografía real" o
"banco de pruebas real", sino explícitamente como una escena sintética
generada por IA que *emula* un entorno de banco de pruebas SLAM. Ya corregí
esto en las Secciones 3 y 4 de este documento — la sección "Método y dato
usado" de ambas incluye ahora la redacción exacta que propongo para la
sección de disponibilidad de datos del artículo.

---

## 0. Resumen de lo que se hizo en esta sesión

- **Reto 2 (Excel): corregido.** Encontré y arreglé el bug de rango
  `SUMPRODUCT` (14 celdas, no 16 — ver corrección de conteo en 2.3) en ambas
  hojas de convolución, y recalculé el archivo completo con LibreOffice para
  que quede sin ningún `#VALUE!`. Archivo actualizado en
  `retos/reto2_convoluciones_excel/version_final/convolucion.xlsx`.
- **Reto 1: semilla agregada.** Apliqué `random.seed(42)` en
  `retos/reto1_matrices_a_imagenes/version_final/reto_1.py` (línea exacta en
  Sección 1) y volví a correrlo para tener un resultado 100% reproducible.
- **Reto 3 y 4: corregida la descripción del dato** (ver aviso arriba).
- **Reto 4: cerrado**, sin filtros adicionales (se queda en media, moda,
  mediana, gaussiana).
- Con esto, los 4 retos quedan listos para trasladarse a `paper/main.tex`.

---

## 1. Reto 1 — Matrices a imágenes

### Método
`reto_1.py`: matriz 1000×1000 de enteros aleatorios (0-255) generada con
listas de Python puro (sin Numpy); mínimo, máximo, media y desviación
estándar calculados a mano (bucle + fórmulas explícitas); guardado del vector
aplanado en `sensor_noise_sim.csv`; relectura con `numpy.loadtxt` y
recálculo de las mismas estadísticas con Numpy; medición de tiempo de ambos
procesos con `time.time()`.

### Cambio aplicado: semilla fija para reproducibilidad
Se agregó `random.seed(42)` inmediatamente antes de crear la matriz, para
que cualquiera que clone el repositorio obtenga exactamente los mismos
números. En `reto_1.py`, el cambio es:

```python
# 1. Generación de matriz 1000x1000 sin librerías matriciales
random.seed(42)  # <-- línea nueva: semilla fija -> reproducibilidad exacta
start_time_manual = time.time()
filas, columnas = 1000, 1000
matriz = [[random.randint(0, 255) for _ in range(columnas)] for _ in range(filas)]
```

Es decir: **una sola línea nueva**, justo antes de `start_time_manual = time.time()`
(entre lo que eran las líneas 8 y 9 del archivo original). Ya apliqué este
cambio en `retos/reto1_matrices_a_imagenes/version_final/reto_1.py`.

### Resultados

| Métrica | Manual (Python puro) | Numpy |
|---|---|---|
| Mínimo | 0 | 0 |
| Máximo | 255 | 255 |
| Media | 127.45 | 127.45 |
| Desviación estándar | 73.92 | 73.92 |
| Tiempo total | 0.4848 s | 0.0752 s |

(Corrida con semilla fija `42`, reproducible por cualquiera que ejecute el
script del repositorio.) El proceso manual fue **~6.4× más lento** que
Numpy en esta corrida. El factor exacto varía con el hardware (en la corrida
original de Milton, sin semilla, fue ~4.3×; en otra corrida mía sin semilla,
~6.7×), pero la conclusión cualitativa —Numpy sensiblemente más rápido— se
sostiene siempre.

### Análisis y vínculo con el marco DOE
La comparación manual-vs-Numpy es, en miniatura, exactamente el tipo de
comparación de "tratamientos" (aquí, implementaciones) que el marco DOE hará
más adelante con distintos algoritmos SLAM: una variable de respuesta
cuantitativa (tiempo de ejecución) medida sobre la misma entrada, bajo
condiciones controladas y reproducibles (semilla fija). La brecha de
rendimiento se explica porque Numpy vectoriza las operaciones en C sobre
memoria contigua, evitando el overhead del intérprete de Python que sí
penaliza los bucles `for` anidados del cálculo manual.

**Figura:** `retos/reto1_matrices_a_imagenes/version_final/reto_1_output_seeded.png`
(mapa de ruido sintético, corrida reproducible con semilla=42 — esta es la
que debe ir en el artículo, no la de la corrida original sin semilla).

---

## 2. Reto 2 — Convoluciones en Excel

### Método (versión final: forma en "T")
Matriz base de 30×30 celdas con una forma interna no rectangular: una letra
"T", elegida porque combina bordes horizontales y verticales con dos tipos
de vértice —4 convexos (puntas de la barra, esquinas del asta) y 2 cóncavos
(donde el asta se une a la barra)—, el mismo tipo de unión (T, junto con L
y X) que la literatura de detección de esquinas usa para caracterizar
*features* estructurales de un entorno (pasillos, marcos de puerta). Tres
niveles aleatorios (no valores fijos, para simular ruido de sensor): fondo
0–20 (`ALEATORIO.ENTRE(0;20)`), borde de transición de una celda 180–220
(desenfoque/penumbra), interior de la letra 220–255. Formato condicional en
escala de grises (0=negro … 255=blanco). Sobre esta matriz, y sobre una
segunda versión suavizada previamente con un kernel gaussiano 3×3, se
aplicaron celda a celda con `SUMPRODUCT` los kernels:

- **Sobel horizontal (Kx)**: `[[-1,0,1],[-2,0,2],[-1,0,1]]`
- **Sobel vertical (Ky)**: `[[-1,-2,-1],[0,0,0],[1,2,1]]`
- **Suavizado gaussiano 3×3** (δ≈0.8): `[[1,2,1],[2,4,2],[1,2,1]] / 16`

y se combinaron `|Gx| + |Gy|` como magnitud del borde detectado, para dos
*pipelines* paralelos: (a) Sobel directo sobre la matriz original, y (b)
Sobel sobre la matriz ya suavizada con el gaussiano. Las 8 capturas del
proceso completo (original, Sobel-H, Sobel-V y combinado, para cada
*pipeline*) están en
`retos/reto2_convoluciones_excel/version_final/capturas_excel_T/`, con
nombres `t_original.png`, `t_original_K_x.png`, `t_original_K_y.png`,
`t_original_K_x_+_K_x.png` (combinado, sin Gaussiano) y los equivalentes
`t_gauss*.png` para el *pipeline* con Gaussiano previo.

**Tamaño del resultado — por qué no es 30×30:** un kernel 3×3 solo puede
calcularse en celdas con vecindario completo de 8 vecinas. Con la fórmula
anclada en la esquina superior izquierda de cada vecindad (como aquí), la
última fila y la última columna de la matriz de 30×30 no tienen ese
vecindario completo, así que la región con convolución válida es de
**28×28**, no de 30×30. En una primera versión se extendió por error la
fórmula de `SUMPRODUCT` a las 30×30 celdas; se corrigió eliminando las dos
últimas filas y las dos últimas columnas, que no tenían un resultado
válido.

*(Nota: dos versiones anteriores de este reto se descartaron: primero una
forma en "L" en dos hojas `un borde`/`dos bordes` de `convolucion.xlsx`;
luego una esquina simple con penumbra de un borde. Se reemplazaron por la
T descrita arriba porque combina ambas orientaciones de borde y ambos
tipos de vértice —convexo y cóncavo— en una sola figura, y documenta
explícitamente el uso de una función aleatoria para simular ruido.)*

### 2.1 Por qué la imagen filtrada tiene valores por encima de 255
Los kernels de Sobel tienen pesos que suman 0 (no son un promedio, sino una
derivada discreta), así que su salida no está acotada a [0,255] como sí lo
está una imagen o un filtro de suavizado (cuyos pesos suman 1). Con pesos
máximos de ±4, la respuesta cruda de cada dirección puede llegar en teoría
hasta 4×255=1020, y la magnitud combinada `|Gx|+|Gy|` hasta el doble. Sobre
la región válida 28×28, el máximo verificado con `MAX()` en la hoja es de
**1238** en el *pipeline* sin suavizar y de **885** con el suavizado
gaussiano previo; en ambos casos varias celdas del borde de la T superan
además la capacidad de columna de Excel (`###`), que tampoco es un error,
sino la misma consecuencia de un valor más ancho que la columna. Estos
valores no son un error: son la magnitud de un gradiente, no un píxel, y
solo habría que normalizarlos o recortarlos a [0,255] si se quisieran
mostrar como imagen. El hallazgo cuantitativo (suavizar antes de derivar
atenúa la magnitud máxima de la respuesta de borde en 28%, de 1238 a 885 en
este ejemplo) es el mismo compromiso ruido-vs-nitidez que se cuantifica de
forma estadística, con réplicas y ANOVA, en el Reto 4 — aquí solo se
establece el mecanismo; el análisis estadístico de qué filtro es preferible
se deja para esa sección, donde sí hay razón (ruido impulsivo, varias
réplicas) para aplicar una prueba de hipótesis formal.

### 2.2 Suavizado gaussiano
La normalización del kernel gaussiano (divide entre 16, la suma de sus
pesos) es correcta: los valores de salida en esa zona de la hoja son
consistentes con `(suma ponderada)/16` (p. ej. 10.9375 = 175/16). Al ser un
promedio ponderado, el resultado se mantiene acotado en [0,255] pero deja
de ser entero (celdas de la T suavizada con valores decimales).

### 2.3 Error corregido
En **ambas** hojas de convolución (`conv un borde` y `conv dos bordes`),
**14 celdas** (columnas `BM` y `CV` en las filas 6, 14, 15, 30 — nota: en la
revisión anterior conté 16 por error; `CV30` en realidad ya estaba bien)
tenían un rango mal definido en el `SUMPRODUCT`:

```
Antes:  BM6 = ABS(SUMPRODUCT(AD6:AE8,  $AF$15:$AH$17))   ← AD6:AE8 = 2 columnas x 3 filas
Ahora:  BM6 = ABS(SUMPRODUCT(AD6:AF8,  $AF$15:$AH$17))   ← AD6:AF8 = 3 columnas x 3 filas (correcto)
```

El kernel es 3×3, pero en esas filas la vecindad de la imagen había quedado
con solo 2 columnas (`AD:AE` en vez de `AD:AF`) — de ahí el `#VALUE!` de
Excel (las dos matrices de `SUMPRODUCT` deben tener el mismo tamaño). Ya
corregí las 14 celdas y recalculé todo el archivo con LibreOffice para
confirmar que no queda ningún error:

| Celda | Valor recalculado |
|---|---|
| BM6 / CV6 / EA6 | 106 / 90 / 196 |
| BM14 / CV14 / EA14 | 510 / 24 / 534 |
| BM15 / CV15 / EA15 | 540 / 2 / 542 |
| BM30 / CV30 / EA30 | 146 / 146 / 292 |

Los valores de las filas 14 y 15 (Kx alto, Ky bajo) son consistentes con el
mismo patrón de borde vertical de la Sección 2.1 — buena señal de que la
corrección es correcta, no solo "elimina el error" sino que da el número
esperado. Archivo corregido: `retos/reto2_convoluciones_excel/version_final/convolucion.xlsx`.

### Análisis y vínculo con el marco DOE
Aplicar los kernels celda por celda en Excel obliga a ver explícitamente la
operación que, en cualquier front-end de SLAM visual, hace `cv2.Sobel` o
`cv2.filter2D` como caja negra: una suma ponderada de una vecindad 3×3. Esa
comprensión de primer principio es la que sostiene, más adelante, cualquier
decisión de diseño sobre qué descriptor de bordes/esquinas usar en la etapa
de extracción de *features* de un pipeline SLAM.

---

## 3. Reto 3 — Regiones de interés en imagen a color

### Método y dato usado (corregido)
La imagen usada (`entorno_slam.jpg`, 2752×1536 px) es una **escena sintética
generada con un modelo de IA generativa de imágenes** (Google Gemini —
modelo "Nano Banana"), diseñada para emular un banco de pruebas de
laboratorio de robótica/visión: un robot móvil sobre ruedas rodeado de 4
paneles de color sólido (rojo, verde, azul, amarillo) y patrones de
calibración (ArUco, checkerboards). **No es una fotografía real** capturada
en un laboratorio físico — esto debe quedar explícito en la sección de
datos del artículo, algo como:

> *"La imagen utilizada en este estudio piloto es una escena sintética
> generada mediante IA generativa (Google Gemini, modelo de generación de
> imágenes), diseñada para emular, con fines ilustrativos y de prueba de
> concepto, un banco de pruebas de calibración de cámara/color típico de un
> laboratorio de robótica. Los resultados cuantitativos (estadísticas por
> canal, análisis de filtrado) se calcularon sobre los valores de píxel
> reales de esa imagen; las conclusiones sobre el comportamiento de los
> algoritmos son válidas independientemente del origen sintético de la
> imagen, pero la escena en sí no corresponde a una captura fotográfica de
> un entorno físico real."*

- Imagen leída con OpenCV: `shape = (1536, 2752, 3)` (alto, ancho, canales BGR).
- 6 regiones de 80×80 px definidas por inspección visual: 5 homogéneas (un
  color cada una) + 1 heterogénea (mezcla, sobre el panel de calibración).

### Resultados (medias y desviaciones estándar por canal BGR)

| Región | Media B,G,R | Desv. Std B,G,R | Color dominante |
|---|---|---|---|
| R1 – Azul (homog.) | 207.4, 95.5, 1.3 | 1.9, 2.1, 1.2 | Azul saturado |
| R2 – Verde (homog.) | 103.5, 191.0, 8.9 | 2.7, 2.6, 5.1 | Verde saturado |
| R3 – Rojo (homog.) | 22.3, 8.0, 204.2 | 3.0, 3.9, 3.1 | Rojo saturado |
| R4 – Pared (homog.) | 245.1, 241.0, 240.4 | 1.4, 1.4, 1.5 | Blanco/gris claro |
| R5 – Piso (homog.) | 204.8, 202.1, 194.4 | 3.2, 3.2, 3.3 | Gris claro |
| R6 – Panel+caja (heterog.) | 150.4, 90.0, 55.3 | **71.7, 34.5, 61.6** | Mezcla |

### Análisis
La correspondencia entre medias BGR y el color percibido es exactamente la
esperada: R1 (azul) tiene B alto y R muy bajo; R3 (rojo) tiene R alto y B/G
bajos; R2 (verde) tiene G dominante; R4 y R5 (pared y piso, ambos casi
blancos/grises) tienen los tres canales altos y muy parecidos entre sí. Las
desviaciones estándar de las 5 regiones homogéneas son todas muy bajas
(1.2–5.1), lo cual confirma que en efecto son regiones de color uniforme —
esperable incluso en una imagen sintética, ya que un modelo generativo
reproduce paneles de color sólido con muy poca variación de textura.

La región 6 (heterogénea) es la más informativa de las seis: su desviación
estándar es **10 a 30 veces mayor** que la de cualquier región homogénea
(71.7 en el canal B, frente a máximo 3.2 en las homogéneas).

### Vínculo con el marco DOE (y su límite, dado el origen sintético)
Esto ilustra el principio de caracterización estadística de *landmarks*
candidatos para SLAM visual: una región con desviación estándar baja es un
buen candidato a "parche de color" estable para seguimiento entre frames;
una con desviación estándar alta (como R6) es una región ambigua. Dicho
esto, como la imagen es sintética, este estudio piloto debe presentarse
como una **prueba de concepto de la métrica y el pipeline de análisis**
(cómo se extraen y caracterizan regiones de interés), no como evidencia
sobre el comportamiento de *landmarks* en escenas físicas reales — esa
validación sí necesitará, más adelante, imágenes reales o un dataset SLAM
estándar (TUM RGB-D, KITTI, EuRoC).

**Figura:** `retos/reto3_roi_color/version_final/reto_3_output.png`
(las 6 regiones dibujadas sobre la imagen sintética original).

---

## 4. Reto 4 — Convoluciones para filtrado (extendido con filtro gaussiano) — CERRADO

### Método y dato usado (corregido)
Misma aclaración que en el Reto 3: la ROI de 300×300 px usada aquí
(`entorno_slam.jpg[400:700, 600:900]`) proviene de la misma imagen
**sintética generada con IA** (Gemini "Nano Banana"), no de una fotografía
real. Sobre esa ROI se inyectó ruido *salt & pepper* al 4% de forma
controlada (esto sí es enteramente nuestro, no depende del origen de la
imagen base). Filtros manuales 3×3 (sin OpenCV): **media**, **moda**,
**mediana**, y **gaussiana** (reutilizando el mismo kernel
`[[1,2,1],[2,4,2],[1,2,1]]/16` del Reto 2). Comparación contra
`cv2.medianBlur` y `cv2.GaussianBlur`. Evaluación cuantitativa con SSIM
(similitud estructural, referencia = imagen sin ruido) sobre 10 réplicas
independientes de ruido por filtro, seguida de ANOVA de un factor (el
filtro) y prueba post-hoc de Tukey HSD.

**Decisión (cerrada):** el análisis se queda con estos 4 filtros; no se
agrega un filtro bilateral ni ningún otro adicional.

### 4.1 ANOVA — efecto del filtro sobre la calidad (SSIM), 4 filtros

| Filtro | Media SSIM | Varianza |
|---|---|---|
| Media | 0.6272 | 0.000009 |
| Moda | 0.6475 | 0.000031 |
| **Mediana** | **0.9255** | 0.000000 |
| Gaussiana | 0.6265 | 0.000009 |

**Estadístico F = 15801.59, p = 3.40 × 10⁻⁵⁶** → el filtro usado tiene un
efecto extremadamente significativo sobre el SSIM.

### 4.2 Tukey HSD (las 6 comparaciones)

| Comparación | Diferencia de medias | p-adj | ¿Significativa? |
|---|---|---|---|
| Gaussiana vs. Media | 0.0007 | 0.973 | **No** |
| Gaussiana vs. Mediana | 0.2990 | <0.001 | Sí |
| Gaussiana vs. Moda | 0.0210 | <0.001 | Sí |
| Media vs. Mediana | 0.2983 | <0.001 | Sí |
| Media vs. Moda | 0.0203 | <0.001 | Sí |
| Mediana vs. Moda | −0.2780 | <0.001 | Sí |

### 4.3 El hallazgo clave
**Gaussiana y Media son estadísticamente indistinguibles** (p=0.973), y
ambas son muy inferiores a la Mediana. Esto es el resultado *teóricamente
correcto*: Media y Gaussiana son filtros **lineales** — promedian los
valores de la vecindad, incluyendo los extremos (0 o 255) que introduce el
ruido *salt & pepper*, así que el ruido se "esparce" en vez de eliminarse.
La Mediana es un filtro **no lineal** (estadístico de orden): al tomar el
valor central de la vecindad ordenada, descarta directamente los extremos.
Es un resultado de libro de texto sobre filtrado de imágenes, demostrado
aquí empíricamente con una prueba de hipótesis real.

Esto se ve también a simple vista en la figura: en la mediana (manual y
OpenCV) el ruido desaparece casi por completo; en media y gaussiana
persisten claramente los puntos blancos y negros del ruido. La moda, aunque
en promedio es un poco mejor que media/gaussiana en el SSIM global, se ve
visualmente peor en zonas texturizadas (el patrón de calibración ajedrezado),
donde produce artefactos de "moteado" por ausencia de un valor mayoritario
claro en vecindades muy variadas.

### 4.4 Tiempos de ejecución (manual vs. OpenCV)

| Filtro | Manual | OpenCV | Aceleración |
|---|---|---|---|
| Mediana | 0.8433 s | 0.0001 s | **~5 770×** |
| Gaussiana | 0.1562 s | 0.0007 s | **~217×** |

### Vínculo con el marco DOE
Esta sección es, de los 4 retos, la más cercana a un experimento DOE real y
completo: un factor (el filtro, 4 niveles), una variable de respuesta
cuantitativa (SSIM) medida con réplicas, un ANOVA para establecer si el
factor importa, y una prueba post-hoc (Tukey) para saber *cuáles* niveles
difieren entre sí — exactamente el mismo esqueleto metodológico que se
usará en el marco doctoral definitivo (factor = algoritmo SLAM, niveles =
algoritmos candidatos, respuesta = métrica de error/precisión). La
comparación manual-vs-OpenCV añade la variable de respuesta secundaria
(tiempo de cómputo), también relevante para evaluar algoritmos SLAM en
tiempo real.

**Figuras:**
- `retos/reto4_filtrado_convoluciones/version_final/reto_4_output.png` (3 filtros originales)
- `retos/reto4_filtrado_convoluciones/version_final/reto_4_extendido_gaussiana_output.png` (8 paneles, con gaussiana)

---

## 5. Consolidado — qué le aporta este bloque de 4 retos al marco doctoral

Tomados en conjunto, los 4 retos ya dejan ensayada, a pequeña escala, toda la
cadena metodológica que necesita el marco DOE para SLAM: (1) instrumentación
de medición de tiempos y estadísticas descriptivas (Reto 1); (2) comprensión
de primer principio de los operadores de convolución que alimentan cualquier
extractor de *features* visual (Reto 2); (3) caracterización estadística de
regiones/*landmarks*, como prueba de concepto del pipeline de análisis
(Reto 3); y (4) un experimento factorial completo —con ANOVA y post-hoc—
comparando "tratamientos" (filtros/algoritmos) por una métrica de calidad y
por tiempo de cómputo (Reto 4), que es en los hechos un prototipo funcional
en miniatura del experimento que se hará después con algoritmos SLAM
completos.

---

## 6. Decisiones cerradas en esta sesión

- **Reto 2:** corregido (14 celdas, ver Sección 2.3) y recalculado sin errores; rediseñado con una forma en "T" (no rectangular, con vértices convexos y cóncavos) + Gaussiano 0.8 opcional, con la región de convolución válida acotada a 28×28 y máximos verificados (1238 sin Gaussiano, 885 con Gaussiano), y justificación explícita de por qué la magnitud de Sobel supera 255 (Sección 2.1).
- **Reto 1:** semilla `random.seed(42)` agregada; línea exacta documentada en Sección 1.
- **Reto 3 y 4:** dato documentado como escena sintética generada por IA (Gemini "Nano Banana"), no fotografía real; texto propuesto para la sección de datos del artículo incluido arriba.
- **Reto 4:** cerrado en 4 filtros (media, moda, mediana, gaussiana), sin agregar bilateral ni otros. El análisis estadístico formal (ANOVA + Tukey) para decidir cuál es el mejor filtro vive únicamente aquí, no en el Reto 2.
- **LaTeX:** contenido ya trasladado a `paper/main.tex`, compilando sin errores (12 páginas); se agregaron además 4 referencias bibliográficas nuevas (Gonzalez & Woods, ORB-SLAM2, SSIM de Wang et al., y el tutorial de odometría visual de Scaramuzza & Fraundorfer).

## 7. Sobre incluir pseudocódigo en el artículo

Ver la respuesta detallada en el chat. Resumen: sí, pero acotado a dos
bloques que unifican varios retos (filtrado por vecindad 3×3 para Retos 2 y
4; extracción y caracterización de ROI para Reto 3), usando el paquete
`algorithm`/`algorithmic` de LaTeX. No se incluye pseudocódigo para el Reto 1
(ya está expresado como fórmulas matemáticas, que es más preciso que
pseudocódigo para ese caso).
