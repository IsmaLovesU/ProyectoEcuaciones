# analisis.py
# Funciones para analizar los resultados numéricos: errores, error máximo,
# orden observado, energía del masa-resorte, solución de referencia con SciPy
# (solo para Van der Pol) y diferencias entre pasos sucesivos.

import numpy as np
from scipy.integrate import solve_ivp

from metodos import euler, rk4


def resolver(metodo, problema, h):
    """
    Resuelve un problema con el método indicado ("Euler" o "RK4").

    Recibe: el nombre del método, el diccionario del problema y el paso h.
    Devuelve: t y y calculados por el método.
    """
    if metodo == "Euler":
        funcion_metodo = euler
    else:
        funcion_metodo = rk4

    return funcion_metodo(problema["f"], problema["t0"], problema["y0"],
                          problema["t_final"], h)


def referencia_scipy(problema, t):
    """
    Calcula una solución de referencia "casi exacta" con solve_ivp (DOP853).
    Se usa solo para Van der Pol, que no tiene solución analítica.

    Recibe: el diccionario del problema y la malla de tiempos t.
    Devuelve: arreglo (n+1, m) con la solución de referencia en esos tiempos.
    """
    solucion = solve_ivp(problema["f"], (problema["t0"], problema["t_final"]),
                         problema["y0"], method="DOP853",
                         rtol=1e-12, atol=1e-12, t_eval=t)
    return solucion.y.T


def solucion_exacta(problema, t):
    """
    Devuelve la solución "exacta" en la malla t: la analítica si existe y,
    si no, la referencia de SciPy.

    Recibe: el diccionario del problema y la malla t.
    Devuelve: arreglo (n+1, m).
    """
    if problema["solucion_analitica"] is not None:
        return problema["solucion_analitica"](t)
    return referencia_scipy(problema, t)


def error_por_punto(y_numerica, y_exacta):
    """
    Calcula el error en cada punto de la malla como la norma euclidiana del
    vector de error (en un problema escalar es simplemente el valor absoluto).

    Recibe: dos arreglos (n+1, m).
    Devuelve: arreglo (n+1,) con el error en cada t_n.
    """
    return np.linalg.norm(y_numerica - y_exacta, axis=1)


def error_relativo_por_punto(y_numerica, y_exacta):
    """
    Calcula el error relativo ||error|| / ||y_exacta|| en cada punto.

    Recibe: dos arreglos (n+1, m).
    Devuelve: arreglo (n+1,) con el error relativo en cada t_n.
    """
    return error_por_punto(y_numerica, y_exacta) / np.linalg.norm(y_exacta, axis=1)


def orden_observado(errores):
    """
    Calcula el orden observado p = log2(E(h) / E(h/2)) entre pasos consecutivos.

    Recibe: lista de errores máximos, ordenada de paso grande a paso pequeño
    (cada paso es la mitad del anterior).
    Devuelve: lista del mismo tamaño; el primer valor es None.
    """
    ordenes = [None]
    for i in range(1, len(errores)):
        ordenes.append(np.log2(errores[i - 1] / errores[i]))
    return ordenes


def estudio_convergencia(problema, pasos):
    """
    Resuelve el problema con Euler y RK4 para cada paso h y guarda el error
    máximo global contra la solución exacta (analítica o referencia SciPy).

    Recibe: el diccionario del problema y la lista de pasos.
    Devuelve: dos listas con los errores máximos de Euler y de RK4.
    """
    errores_euler = []
    errores_rk4 = []

    for h in pasos:
        t, y_euler = resolver("Euler", problema, h)
        t, y_rk4 = resolver("RK4", problema, h)
        y_exacta = solucion_exacta(problema, t)

        errores_euler.append(np.max(error_por_punto(y_euler, y_exacta)))
        errores_rk4.append(np.max(error_por_punto(y_rk4, y_exacta)))

    return errores_euler, errores_rk4


def diferencias_sucesivas(problema, pasos):
    """
    Compara la solución con paso h contra la solución con paso h/2 en los
    tiempos de la malla gruesa y guarda la diferencia máxima. No usa SciPy.

    Recibe: el diccionario del problema y la lista de pasos h.
    Devuelve: dos listas con las diferencias máximas de Euler y de RK4.
    """
    diferencias_euler = []
    diferencias_rk4 = []

    for h in pasos:
        for metodo, lista in [("Euler", diferencias_euler), ("RK4", diferencias_rk4)]:
            t_grueso, y_grueso = resolver(metodo, problema, h)
            t_fino, y_fino = resolver(metodo, problema, h / 2)

            # La malla fina tiene el doble de puntos: tomamos uno de cada dos
            y_fino_en_malla_gruesa = y_fino[::2]
            lista.append(np.max(error_por_punto(y_grueso, y_fino_en_malla_gruesa)))

    return diferencias_euler, diferencias_rk4


def energia_masa_resorte(y):
    """
    Calcula la energía por unidad de masa E = (x')^2 / 2 + 2 x^2.

    Recibe: arreglo (n+1, 2) con columnas [x, x'].
    Devuelve: arreglo (n+1,) con la energía en cada t_n.
    """
    posicion = y[:, 0]
    velocidad = y[:, 1]
    return velocidad**2 / 2 + 2 * posicion**2
