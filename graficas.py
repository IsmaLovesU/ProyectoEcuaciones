# graficas.py
# Funciones para generar y guardar las figuras del proyecto.
# Los colores son los mismos en todas las figuras:
#   analítica / exacta -> negro, Euler -> naranja, RK4 -> azul,
#   referencia SciPy -> gris discontinuo.

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


CARPETA_FIGURAS = os.path.join("resultados", "figuras")


def estilo_de(etiqueta):
    """
    Devuelve el estilo de línea según el método que indica la etiqueta.

    Recibe: la etiqueta de la curva (por ejemplo "Euler (h = 0.1)").
    Devuelve: diccionario con color, tipo de línea y grosor para plt.plot.
    """
    if etiqueta.startswith("Euler"):
        return {"color": "tab:orange", "linestyle": "-", "linewidth": 1.6}
    if etiqueta.startswith("RK4"):
        return {"color": "tab:blue", "linestyle": "--", "linewidth": 1.8}
    if etiqueta.startswith("Referencia"):
        # Más gruesa que las demás para que se vea aunque RK4 quede encima
        return {"color": "gray", "linestyle": "--", "linewidth": 4.0, "alpha": 0.6}
    # Solución analítica o valor exacto
    return {"color": "black", "linestyle": "-", "linewidth": 2.4, "alpha": 0.8}


def dar_formato(ax, titulo, etiqueta_x, etiqueta_y, escala_log=False, leyenda_abajo=False):
    """
    Pone título, nombres de ejes, leyenda y cuadrícula suave a un eje.
    Si leyenda_abajo es True, la leyenda va debajo de la gráfica para no tapar
    las curvas. No devuelve nada.
    """
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    if escala_log:
        ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    if leyenda_abajo:
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)
    else:
        ax.legend()


def dibujar_curvas(ax, curvas):
    """
    Dibuja varias curvas en un mismo eje.

    Recibe: el eje y una lista de tuplas (x, y, etiqueta).
    No devuelve nada.
    """
    for x, y, etiqueta in curvas:
        ax.plot(x, y, label=etiqueta, **estilo_de(etiqueta))


def guardar_figura(fig, nombre_archivo):
    """Guarda la figura en resultados/figuras con dpi = 200 y la cierra. No devuelve nada."""
    fig.tight_layout()
    fig.savefig(os.path.join(CARPETA_FIGURAS, nombre_archivo), dpi=200)
    plt.close(fig)


def grafica_simple(curvas, titulo, etiqueta_x, etiqueta_y, nombre_archivo,
                   escala_log=False, leyenda_abajo=False):
    """
    Figura con un solo panel (soluciones, errores, energía o planos de fase).

    Recibe: lista de curvas (x, y, etiqueta), título, nombres de ejes, nombre
    del archivo, si el eje y es logarítmico y si la leyenda va debajo.
    No devuelve nada; guarda el PNG.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    dibujar_curvas(ax, curvas)
    dar_formato(ax, titulo, etiqueta_x, etiqueta_y, escala_log, leyenda_abajo)
    guardar_figura(fig, nombre_archivo)


def grafica_dos_paneles(curvas_izquierda, curvas_derecha, titulos, etiqueta_x,
                        etiquetas_y, titulo_general, nombre_archivo, escala_log=False):
    """
    Figura con dos subgráficas lado a lado.

    Recibe: las curvas de cada panel, una lista con los dos títulos, el nombre
    del eje x, una lista con los dos nombres del eje y, el título general,
    el nombre del archivo y si el eje y es logarítmico.
    No devuelve nada; guarda el PNG.
    """
    fig, ejes = plt.subplots(1, 2, figsize=(12, 5))
    paneles = [curvas_izquierda, curvas_derecha]

    for i in range(2):
        dibujar_curvas(ejes[i], paneles[i])
        dar_formato(ejes[i], titulos[i], etiqueta_x, etiquetas_y[i], escala_log)

    fig.suptitle(titulo_general, fontsize=13)
    guardar_figura(fig, nombre_archivo)


def grafica_convergencia(pasos, errores_euler, errores_rk4, titulo, nombre_archivo,
                         etiqueta_y="Error máximo global"):
    """
    Gráfica log-log del error (o diferencia) máximo contra el paso h, con
    rectas de referencia de pendiente 1 y 4.

    Recibe: lista de pasos, errores de Euler, errores de RK4, título, nombre
    del archivo y nombre del eje y.
    No devuelve nada; guarda el PNG.
    """
    pasos = np.array(pasos)
    errores_euler = np.array(errores_euler)
    errores_rk4 = np.array(errores_rk4)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(pasos, errores_euler, "o-", label="Euler", color="tab:orange", linewidth=1.6)
    ax.loglog(pasos, errores_rk4, "s-", label="RK4", color="tab:blue", linewidth=1.6)

    # Rectas de referencia C·h^p. Se anclan al último punto (paso más pequeño)
    # y se desplazan un poco hacia abajo para que no tapen los datos.
    desplazamiento = 0.3
    recta_orden_1 = desplazamiento * errores_euler[-1] * (pasos / pasos[-1]) ** 1
    recta_orden_4 = desplazamiento * errores_rk4[-1] * (pasos / pasos[-1]) ** 4
    ax.loglog(pasos, recta_orden_1, ":", color="black", linewidth=1.4,
              label="Referencia: pendiente 1")
    ax.loglog(pasos, recta_orden_4, "-.", color="gray", linewidth=1.4,
              label="Referencia: pendiente 4")

    # Marcas del eje x justo en los pasos usados
    ax.set_xticks(pasos)
    ax.set_xticklabels([f"{h:g}" for h in pasos])
    ax.minorticks_off()

    ax.set_title(titulo)
    ax.set_xlabel("Paso h")
    ax.set_ylabel(etiqueta_y)
    ax.grid(True, alpha=0.3)
    ax.legend()
    guardar_figura(fig, nombre_archivo)
