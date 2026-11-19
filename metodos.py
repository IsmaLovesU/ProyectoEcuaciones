# metodos.py
# Métodos numéricos de paso fijo implementados en el proyecto:
# Euler (orden 1) y Runge-Kutta de cuarto orden, RK4 (orden 4).
# Ambos resuelven el problema de valor inicial y' = f(t, y), y(t0) = y0,
# donde y puede ser un escalar o un vector (sistema de EDs).

import numpy as np


def preparar_malla(t0, y0, t_final, h):
    """
    Construye la malla de tiempos y el arreglo donde se guardará la solución.

    Recibe: t0, y0 (número o lista), t_final y el paso h.
    Devuelve: t (arreglo de tamaño n+1), y (arreglo de ceros de tamaño (n+1, m)
    con la condición inicial en la primera fila), n (número de pasos) y el
    paso efectivo usado.
    """
    n = round((t_final - t0) / h)
    t = np.linspace(t0, t_final, n + 1)

    # Un problema escalar se trata como un sistema de tamaño 1
    y_inicial = np.atleast_1d(np.array(y0, dtype=float))
    y = np.zeros((n + 1, len(y_inicial)))
    y[0] = y_inicial

    # Paso efectivo para que la malla termine exactamente en t_final
    paso = (t_final - t0) / n
    return t, y, n, paso


def euler(f, t0, y0, t_final, h):
    """
    Resuelve y' = f(t, y) con el método de Euler.

    Recibe: la función f(t, y), el tiempo inicial t0, la condición inicial y0,
    el tiempo final t_final y el paso h.
    Devuelve: t (arreglo de tamaño n+1) y y (arreglo de tamaño (n+1, m)).
    """
    t, y, n, paso = preparar_malla(t0, y0, t_final, h)

    for i in range(n):
        y[i + 1] = y[i] + paso * f(t[i], y[i])

    return t, y


def rk4(f, t0, y0, t_final, h):
    """
    Resuelve y' = f(t, y) con el método de Runge-Kutta de cuarto orden.

    Recibe: la función f(t, y), el tiempo inicial t0, la condición inicial y0,
    el tiempo final t_final y el paso h.
    Devuelve: t (arreglo de tamaño n+1) y y (arreglo de tamaño (n+1, m)).
    """
    t, y, n, paso = preparar_malla(t0, y0, t_final, h)

    for i in range(n):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + paso / 2, y[i] + paso / 2 * k1)
        k3 = f(t[i] + paso / 2, y[i] + paso / 2 * k2)
        k4 = f(t[i] + paso, y[i] + paso * k3)
        y[i + 1] = y[i] + (paso / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return t, y
