# Instrucciones para Claude Code — Proyecto Final de Ecuaciones Diferenciales 1

## 0. Contexto

Proyecto final del curso Ecuaciones Diferenciales 1, **Alternativa 2: métodos numéricos para resolver EDs**.
El grupo debe implementar **dos métodos numéricos iterativos** en Python y ponerlos a prueba con:

1. Una ED de primer orden (con solución analítica).
2. Una ED de segundo orden (con solución analítica).
3. Un sistema lineal 2×2 (con solución analítica).
4. Un sistema no lineal 2×2 **sin** solución analítica (aquí se estudia la convergencia).

**Tu tarea es SOLO el código en Python**, las gráficas y las tablas de resultados. No escribas el informe, no hagas LaTeX y no deduzcas soluciones analíticas (el grupo las hace a mano; tú solo usas las fórmulas finales dadas en la sección 3).

---

## 1. Estilo del código (importante)

- Código **ordenado, claro y de nivel universitario**: debe verse como lo escribiría un estudiante cuidadoso, no un ingeniero de software senior.
- Usa **funciones simples**. Nada de clases, decoradores, herencia, type hints complejos, `dataclasses` ni patrones de diseño.
- **Comentarios y docstrings en español**. Cada función lleva un docstring corto que diga qué hace, qué recibe y qué devuelve.
- Nombres de variables en español y descriptivos (`paso`, `t_final`, `error_maximo`), salvo la notación matemática habitual (`t`, `y`, `h`, `f`, `k1`…`k4`).
- Prioriza lo **simple y directo** sobre lo "elegante". Si algo se puede hacer con un `for` legible, hazlo con un `for`.
- Librerías permitidas: `numpy`, `matplotlib` y `scipy` (solo `scipy.integrate.solve_ivp` para la referencia de Van der Pol). No uses pandas ni otras librerías.
- Python 3.10 o superior.

---

## 2. Métodos numéricos a implementar

Ambos deben funcionar de forma **genérica para sistemas** (vector `y`), así sirven para las EDs de primer orden, las de segundo orden convertidas a sistema y los sistemas 2×2.

Problema de valor inicial: `y' = f(t, y)`, `y(t0) = y0`, con paso fijo `h`.

### 2.1 Método de Euler (orden 1)

```
y_{n+1} = y_n + h · f(t_n, y_n)
```

### 2.2 Método de Runge-Kutta de cuarto orden, RK4 (orden 4)

```
k1 = f(t_n,       y_n)
k2 = f(t_n + h/2, y_n + h/2 · k1)
k3 = f(t_n + h/2, y_n + h/2 · k2)
k4 = f(t_n + h,   y_n + h · k3)
y_{n+1} = y_n + (h/6) · (k1 + 2k2 + 2k3 + k4)
```

### 2.3 Firma común de ambas funciones

```python
def euler(f, t0, y0, t_final, h):
    ...
    return t, y   # t: arreglo (n+1,), y: arreglo (n+1, m)

def rk4(f, t0, y0, t_final, h):
    ...
    return t, y
```

- `f(t, y)` recibe un escalar `t` y un arreglo `y` y devuelve un arreglo de NumPy del mismo tamaño.
- `y0` puede venir como lista o número; conviértelo a `np.array(..., dtype=float)` y asegúrate de que sea 1D (un problema escalar se trata como sistema de tamaño 1).
- Calcula el número de pasos como `n = round((t_final - t0) / h)` y construye `t` con `np.linspace(t0, t_final, n + 1)` para que la malla termine exactamente en `t_final`.
- Implementa el ciclo de iteración **a mano** (no uses `solve_ivp` aquí).

---

## 3. Problemas a resolver

Se eligió **un problema de cada tipo**, seleccionando los que aportan algo distinto al análisis.

### 3.1 ED de primer orden — Ley de enfriamiento de Newton

```
dT/dt = -0.2 (T - 25),    T(0) = 80
```

- Intervalo: `t ∈ [0, 20]`
- Paso base para las gráficas: `h = 0.5`
- Solución analítica (la usa el código para comparar): `T(t) = 25 + 55·e^(-0.2 t)`
- **Por qué este**: es el caso "bien comportado". Sirve como referencia para ver el orden de convergencia limpio de cada método.

### 3.2 ED de segundo orden — Masa-resorte sin amortiguamiento

```
x'' + 4x = 0,    x(0) = 1,   x'(0) = 0
```

- Se convierte a sistema con `y1 = x`, `y2 = x'`:
  `y1' = y2`, `y2' = -4·y1`
- Intervalo: `t ∈ [0, 10]` (un poco más de 3 periodos; el periodo es π)
- Paso base para las gráficas: `h = 0.1`
- Solución analítica: `x(t) = cos(2t)`, `x'(t) = -2·sin(2t)`
- Cantidad conservada (energía por unidad de masa): `E(t) = (x')²/2 + 2x²`, con valor exacto `E = 2` para todo `t`.
- **Por qué este**: muestra la **limitación más importante de Euler**: la amplitud y la energía crecen artificialmente con el tiempo, mientras RK4 conserva la oscilación casi perfecta. Además ilustra cómo una ED de 2.º orden se reescribe como sistema.

### 3.3 Sistema lineal 2×2 — Sistema acoplado

```
x' = 2x + y
y' = x + 2y
x(0) = 1,   y(0) = 0
```

- Intervalo: `t ∈ [0, 2]`
- Paso base para las gráficas: `h = 0.1`
- Solución analítica:
  `x(t) = (e^(3t) + e^t) / 2`
  `y(t) = (e^(3t) - e^t) / 2`
- **Por qué este**: la solución crece exponencialmente (valores propios 3 y 1), así que el error se acumula rápido. Esto permite discutir **error absoluto frente a error relativo**.
- Nota: el "Sistema 2" del anteproyecto (`x' = y`, `y' = -4x`) no se usa porque es exactamente la misma ecuación del problema 3.2 escrita como sistema.

### 3.4 Sistema no lineal 2×2 — Oscilador de Van der Pol (μ = 1)

```
x' = y
y' = (1 - x²)·y - x
x(0) = 2,   y(0) = 0
```

- Intervalo: `t ∈ [0, 20]`
- Sin solución analítica. Se estudia la **convergencia** de cada método.
- **Por qué este**: es el sistema no lineal propuesto en el anteproyecto; tiene un ciclo límite, lo que permite ver si cada método lo reproduce correctamente.

---

## 4. Análisis que debe hacer el código

### 4.1 Para los tres problemas con solución analítica (3.1, 3.2, 3.3)

1. **Comparación con paso base**: resolver con Euler y RK4 usando el `h` base indicado y compararlos con la solución analítica.
2. **Error en cada punto**: `error(t_n) = |y_numérico(t_n) - y_analítico(t_n)|`.
   - En los sistemas, trabaja con la **norma euclidiana** del vector de error en cada `t_n`.
   - En el problema 3.3 calcula también el **error relativo**: `‖error‖ / ‖y_analítico‖`.
3. **Estudio de convergencia**: resolver con los pasos
   `h = [0.2, 0.1, 0.05, 0.025, 0.0125]`
   y para cada `h` guardar el **error máximo global** (el máximo del error en toda la malla).
4. **Orden observado**: entre pasos consecutivos (`h` y `h/2`):
   `p ≈ log2( E(h) / E(h/2) )`
   Se espera `p ≈ 1` para Euler y `p ≈ 4` para RK4.
5. Solo para el problema 3.2: calcular la **energía** `E(t)` con cada método y su desviación respecto al valor exacto 2.

### 4.2 Para Van der Pol (3.4)

1. **Solución de referencia**: calcular con `scipy.integrate.solve_ivp` usando `method="DOP853"`, `rtol=1e-12`, `atol=1e-12` y `t_eval` igual a la malla de cada `h`. Se usa solo como referencia "casi exacta"; los métodos del proyecto siguen siendo los implementados a mano.
2. **Convergencia respecto a la referencia**: para `h = [0.1, 0.05, 0.025, 0.0125]`, calcular el error máximo global de Euler y de RK4 contra la referencia y el orden observado `p` igual que en 4.1.
3. **Convergencia entre pasos sucesivos** (no depende de SciPy): comparar la solución con paso `h` contra la de paso `h/2` en los tiempos comunes (los de la malla gruesa) y reportar la diferencia máxima. Si el método converge, esta diferencia debe disminuir al reducir `h`.
4. **Retrato de fase**: graficar `y` contra `x` para ver si cada método llega al ciclo límite.

---

## 5. Salidas esperadas

### 5.1 Figuras (`resultados/figuras/`, formato PNG, `dpi=200`)

Todas con título, ejes rotulados **en español con unidades o nombre de variable**, leyenda y cuadrícula suave. Colores consistentes en todo el proyecto (por ejemplo: analítica en negro, Euler en un color, RK4 en otro, referencia SciPy en gris discontinuo).

| Archivo | Contenido |
|---|---|
| `p1_solucion.png` | Enfriamiento: analítica vs Euler vs RK4 (h = 0.5) |
| `p1_error.png` | Enfriamiento: error vs t, eje y logarítmico |
| `p1_convergencia.png` | Enfriamiento: error máximo vs h, ejes log-log, con rectas de referencia de pendiente 1 y 4 |
| `p2_solucion.png` | Masa-resorte: x(t) analítica vs Euler vs RK4 (h = 0.1) |
| `p2_fase.png` | Masa-resorte: plano de fase x vs x' (la analítica es una elipse cerrada) |
| `p2_energia.png` | Masa-resorte: E(t) de cada método vs valor exacto 2 |
| `p2_error.png` | Masa-resorte: error vs t, eje y logarítmico |
| `p2_convergencia.png` | Masa-resorte: log-log como en p1 |
| `p3_solucion.png` | Sistema lineal: x(t) y y(t) analítica vs Euler vs RK4 (dos subgráficas) |
| `p3_error.png` | Sistema lineal: error absoluto y error relativo vs t (dos subgráficas, eje y log) |
| `p3_convergencia.png` | Sistema lineal: log-log como en p1 |
| `p4_solucion.png` | Van der Pol: x(t) con Euler, RK4 y referencia (h = 0.05) |
| `p4_fase.png` | Van der Pol: retrato de fase de Euler, RK4 y referencia |
| `p4_convergencia.png` | Van der Pol: error máximo vs h contra la referencia, log-log |
| `p4_diferencias_sucesivas.png` | Van der Pol: diferencia entre h y h/2 vs h, log-log |

### 5.2 Tablas (`resultados/tablas/`, formato CSV)

Usa el módulo estándar `csv`. Números con 6 cifras significativas en notación científica cuando sea pequeño.

- `p1_convergencia.csv`, `p2_convergencia.csv`, `p3_convergencia.csv`, `p4_convergencia.csv`
  Columnas: `h, error_max_euler, orden_euler, error_max_rk4, orden_rk4` (el orden de la primera fila queda vacío).
- `p4_diferencias_sucesivas.csv`
  Columnas: `h, dif_max_euler, dif_max_rk4`.
- `p2_energia.csv`
  Columnas: `metodo, energia_final, desviacion_final` (en `t = 10`, con `h = 0.1`).
- `resumen_paso_base.csv`
  Una fila por problema y método con: `problema, metodo, h, error_max, error_final` (para Van der Pol, contra la referencia).

Estas tablas se usarán después para el informe en LaTeX, así que deben ser limpias y fáciles de leer.

### 5.3 Consola

Al ejecutar `main.py`, imprimir un resumen corto y ordenado por problema: qué se resolvió, el error máximo con el paso base y los órdenes observados. Sin mensajes de depuración.

---

## 6. Estructura del repositorio

```
proyecto_ed/
├── README.md            # Qué es el proyecto, cómo instalar y cómo ejecutar
├── requirements.txt     # numpy, matplotlib, scipy
├── metodos.py           # euler() y rk4()
├── problemas.py         # Definición de cada problema: f(t, y), condiciones iniciales,
│                        # intervalo, paso base y solución analítica (si existe)
├── analisis.py          # Errores, error máximo, orden observado, energía,
│                        # referencia con solve_ivp, diferencias sucesivas
├── graficas.py          # Funciones para generar y guardar cada tipo de figura
├── tablas.py            # Funciones para escribir los CSV
├── main.py              # Ejecuta todo en orden y genera resultados/
└── resultados/
    ├── figuras/
    └── tablas/
```

Detalles:

- `problemas.py`: cada problema puede representarse como un **diccionario** con claves como `nombre`, `f`, `y0`, `t0`, `t_final`, `h_base`, `solucion_analitica` (función o `None`). Nada de clases.
- `main.py` debe crear las carpetas de `resultados/` si no existen (`os.makedirs(..., exist_ok=True)`).
- Usa `matplotlib.use("Agg")` para que las figuras se guarden sin abrir ventanas, y cierra cada figura después de guardarla (`plt.close()`).
- Cada archivo empieza con un comentario breve que explique para qué sirve.
- No dupliques código: si las tres gráficas de convergencia son iguales, haz una sola función que reciba los datos.

---

## 7. Verificación antes de terminar

1. Ejecuta `python main.py` desde la carpeta del proyecto y confirma que se generan **todas** las figuras y tablas de la sección 5 sin errores ni advertencias.
2. Revisa los órdenes observados en los CSV:
   - Euler: valores cercanos a **1** en los problemas 1, 2 y 3.
   - RK4: valores cercanos a **4** (en los pasos más pequeños el error puede llegar al redondeo de máquina, ~1e-12 o menos; si pasa, menciónalo en el resumen final en lugar de "arreglarlo").
3. Confirma que en `p2_energia.png` la energía de Euler **crece** y la de RK4 se mantiene prácticamente en 2.
4. Abre algunas figuras y verifica que tengan título, ejes, leyenda y que nada se vea cortado o encimado.
5. Al terminar, escribe un resumen breve con: archivos creados, órdenes observados de cada método y cualquier resultado que no coincida con lo esperado.

---

## 8. Lo que NO debes hacer

- No escribir el informe ni archivos `.tex`.
- No deducir ni redactar las soluciones analíticas (solo usar las fórmulas de la sección 3).
- No usar `solve_ivp` u otras funciones de librería para resolver los problemas 1 a 3, ni como sustituto de `euler()` o `rk4()`.
- No agregar métodos extra (Heun, RK45 propio, paso adaptativo, etc.).
- No crear interfaces gráficas, notebooks, CLI con argumentos ni tests automatizados complejos.
