# problemas.py
# Definición de los cuatro problemas del proyecto. Cada problema es un
# diccionario con su función f(t, y), condición inicial, intervalo, paso base
# y solución analítica (o None si no existe).

import numpy as np


# ---------------------------------------------------------------------------
# Problema 1: Ley de enfriamiento de Newton
#   dT/dt = -0.2 (T - 25),  T(0) = 80
# ---------------------------------------------------------------------------

def f_enfriamiento(t, y):
    """Lado derecho de la ED de enfriamiento. Recibe t y y = [T]; devuelve [dT/dt]."""
    temperatura = y[0]
    return np.array([-0.2 * (temperatura - 25)])


def solucion_enfriamiento(t):
    """Solución analítica T(t) = 25 + 55 e^(-0.2 t). Recibe un arreglo t; devuelve arreglo (n, 1)."""
    temperatura = 25 + 55 * np.exp(-0.2 * t)
    return np.column_stack([temperatura])


# ---------------------------------------------------------------------------
# Problema 2: Masa-resorte sin amortiguamiento
#   x'' + 4x = 0,  x(0) = 1, x'(0) = 0
#   Como sistema: y1 = x, y2 = x'  ->  y1' = y2, y2' = -4 y1
# ---------------------------------------------------------------------------

def f_masa_resorte(t, y):
    """Lado derecho del sistema masa-resorte. Recibe t y y = [x, x']; devuelve [x', x'']."""
    posicion = y[0]
    velocidad = y[1]
    return np.array([velocidad, -4 * posicion])


def solucion_masa_resorte(t):
    """Solución analítica x = cos(2t), x' = -2 sin(2t). Recibe un arreglo t; devuelve arreglo (n, 2)."""
    posicion = np.cos(2 * t)
    velocidad = -2 * np.sin(2 * t)
    return np.column_stack([posicion, velocidad])


# ---------------------------------------------------------------------------
# Problema 3: Sistema lineal 2x2 acoplado
#   x' = 2x + y,  y' = x + 2y,  x(0) = 1, y(0) = 0
# ---------------------------------------------------------------------------

def f_sistema_lineal(t, y):
    """Lado derecho del sistema lineal. Recibe t y y = [x, y]; devuelve [x', y']."""
    x = y[0]
    y2 = y[1]
    return np.array([2 * x + y2, x + 2 * y2])


def solucion_sistema_lineal(t):
    """Solución analítica x = (e^3t + e^t)/2, y = (e^3t - e^t)/2. Devuelve arreglo (n, 2)."""
    x = (np.exp(3 * t) + np.exp(t)) / 2
    y = (np.exp(3 * t) - np.exp(t)) / 2
    return np.column_stack([x, y])


# ---------------------------------------------------------------------------
# Problema 4: Oscilador de Van der Pol (mu = 1), sin solución analítica
#   x' = y,  y' = (1 - x^2) y - x,  x(0) = 2, y(0) = 0
# ---------------------------------------------------------------------------

MU = 1.0


def f_van_der_pol(t, y):
    """Lado derecho del oscilador de Van der Pol. Recibe t y y = [x, y]; devuelve [x', y']."""
    x = y[0]
    y2 = y[1]
    return np.array([y2, MU * (1 - x**2) * y2 - x])


# ---------------------------------------------------------------------------
# Diccionarios con los datos de cada problema
# ---------------------------------------------------------------------------

ENFRIAMIENTO = {
    "nombre": "Enfriamiento de Newton",
    "f": f_enfriamiento,
    "y0": [80.0],
    "t0": 0.0,
    "t_final": 20.0,
    "h_base": 0.5,
    "solucion_analitica": solucion_enfriamiento,
}

MASA_RESORTE = {
    "nombre": "Masa-resorte sin amortiguamiento",
    "f": f_masa_resorte,
    "y0": [1.0, 0.0],
    "t0": 0.0,
    "t_final": 10.0,
    "h_base": 0.1,
    "solucion_analitica": solucion_masa_resorte,
}

SISTEMA_LINEAL = {
    "nombre": "Sistema lineal 2x2",
    "f": f_sistema_lineal,
    "y0": [1.0, 0.0],
    "t0": 0.0,
    "t_final": 2.0,
    "h_base": 0.1,
    "solucion_analitica": solucion_sistema_lineal,
}

VAN_DER_POL = {
    "nombre": "Oscilador de Van der Pol (mu = 1)",
    "f": f_van_der_pol,
    "y0": [2.0, 0.0],
    "t0": 0.0,
    "t_final": 20.0,
    "h_base": 0.05,
    "solucion_analitica": None,
}
