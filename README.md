# Proyecto final — Ecuaciones Diferenciales 1

**Alternativa 2: métodos numéricos para resolver ecuaciones diferenciales.**

## Integrantes

| Nombre | Carné |
|---|---|
| Andrés González | 24005 |
| Jose Carlos Agustin | 24999 |
| Steven Boy | 24541 |

## Descripción

Se implementan a mano dos métodos iterativos de paso fijo:

- **Euler** (orden 1)
- **Runge-Kutta de cuarto orden, RK4** (orden 4)

y se ponen a prueba con cuatro problemas:

| # | Problema | Tipo | Solución analítica |
|---|---|---|---|
| 1 | Enfriamiento de Newton: `T' = -0.2 (T - 25)`, `T(0) = 80` | ED de 1.er orden | Sí |
| 2 | Masa-resorte: `x'' + 4x = 0`, `x(0) = 1`, `x'(0) = 0` | ED de 2.º orden | Sí |
| 3 | Sistema lineal: `x' = 2x + y`, `y' = x + 2y`, `x(0) = 1`, `y(0) = 0` | Sistema lineal 2×2 | Sí |
| 4 | Van der Pol (μ = 1): `x' = y`, `y' = (1 - x²) y - x`, `x(0) = 2`, `y(0) = 0` | Sistema no lineal 2×2 | No |

Para los problemas 1 a 3 se compara contra la solución analítica y se estudia el
orden de convergencia. Para Van der Pol se usa una solución de referencia
calculada con `scipy.integrate.solve_ivp` (DOP853, tolerancias 1e-12) y además
se comparan soluciones con pasos `h` y `h/2`.

## Estructura

```
├── metodos.py      # euler() y rk4()
├── problemas.py    # f(t, y), condiciones iniciales, intervalo y solución analítica
├── analisis.py     # errores, orden observado, energía, referencia SciPy, diferencias sucesivas
├── graficas.py     # funciones para generar las figuras
├── tablas.py       # funciones para escribir los CSV
├── main.py         # ejecuta todo y genera resultados/
└── resultados/
    ├── figuras/    # PNG (dpi = 200)
    └── tablas/     # CSV
```

## Instalación

Se necesita Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

El programa imprime un resumen por problema (error máximo con el paso base y
órdenes observados) y guarda las figuras en `resultados/figuras/` y las tablas
en `resultados/tablas/`.
