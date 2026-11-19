# main.py
# Programa principal del proyecto. Resuelve los cuatro problemas con Euler y
# RK4, hace los estudios de error y convergencia, y guarda las figuras y
# tablas en la carpeta resultados/. Al final imprime un resumen en consola.

import os

import numpy as np

import analisis
import graficas
import tablas
from problemas import ENFRIAMIENTO, MASA_RESORTE, SISTEMA_LINEAL, VAN_DER_POL


PASOS_CONVERGENCIA = [0.2, 0.1, 0.05, 0.025, 0.0125]
PASOS_VAN_DER_POL = [0.1, 0.05, 0.025, 0.0125]


def malla_fina(problema):
    """Devuelve una malla de 1000 puntos para dibujar la solución analítica como curva suave."""
    return np.linspace(problema["t0"], problema["t_final"], 1000)


def texto_ordenes(ordenes):
    """Convierte la lista de órdenes observados en un texto corto para la consola."""
    return ", ".join(f"{p:.3f}" for p in ordenes[1:])


def convergencia_con_tabla(problema, pasos, nombre_archivo):
    """
    Hace el estudio de convergencia de un problema y guarda su tabla CSV.

    Recibe: el diccionario del problema, la lista de pasos y el nombre del CSV.
    Devuelve: errores y órdenes de Euler y de RK4.
    """
    errores_euler, errores_rk4 = analisis.estudio_convergencia(problema, pasos)
    ordenes_euler = analisis.orden_observado(errores_euler)
    ordenes_rk4 = analisis.orden_observado(errores_rk4)
    tablas.tabla_convergencia(nombre_archivo, pasos, errores_euler, ordenes_euler,
                              errores_rk4, ordenes_rk4)
    return errores_euler, ordenes_euler, errores_rk4, ordenes_rk4


def imprimir_resumen(problema, h, error_euler, error_rk4, ordenes_euler, ordenes_rk4):
    """Imprime en consola el resumen de un problema. No devuelve nada."""
    print(f"\n{problema['nombre']}")
    print(f"  Error máximo con h = {h}:  Euler = {error_euler:.4e}   RK4 = {error_rk4:.4e}")
    print(f"  Órdenes observados Euler: {texto_ordenes(ordenes_euler)}")
    print(f"  Órdenes observados RK4:   {texto_ordenes(ordenes_rk4)}")


def problema_1(resumen):
    """Enfriamiento de Newton: solución, error y convergencia. Agrega filas al resumen."""
    problema = ENFRIAMIENTO
    h = problema["h_base"]

    t, y_euler = analisis.resolver("Euler", problema, h)
    t, y_rk4 = analisis.resolver("RK4", problema, h)
    y_exacta = analisis.solucion_exacta(problema, t)
    t_fino = malla_fina(problema)
    y_fina = analisis.solucion_exacta(problema, t_fino)

    error_euler = analisis.error_por_punto(y_euler, y_exacta)
    error_rk4 = analisis.error_por_punto(y_rk4, y_exacta)

    graficas.grafica_simple(
        [(t_fino, y_fina[:, 0], "Analítica"),
         (t, y_euler[:, 0], f"Euler (h = {h})"),
         (t, y_rk4[:, 0], f"RK4 (h = {h})")],
        "Enfriamiento de Newton: solución analítica y numérica",
        "Tiempo t", "Temperatura T(t)", "p1_solucion.png")

    # Se omite t = 0, donde el error es exactamente cero (no cabe en escala log)
    graficas.grafica_simple(
        [(t[1:], error_euler[1:], f"Euler (h = {h})"),
         (t[1:], error_rk4[1:], f"RK4 (h = {h})")],
        "Enfriamiento de Newton: error absoluto",
        "Tiempo t", "Error |T_num(t) - T(t)|", "p1_error.png", escala_log=True)

    errores_euler, ordenes_euler, errores_rk4, ordenes_rk4 = convergencia_con_tabla(
        problema, PASOS_CONVERGENCIA, "p1_convergencia.csv")
    graficas.grafica_convergencia(PASOS_CONVERGENCIA, errores_euler, errores_rk4,
                                  "Enfriamiento de Newton: convergencia",
                                  "p1_convergencia.png")

    resumen.append([problema["nombre"], "Euler", h, np.max(error_euler), error_euler[-1]])
    resumen.append([problema["nombre"], "RK4", h, np.max(error_rk4), error_rk4[-1]])
    imprimir_resumen(problema, h, np.max(error_euler), np.max(error_rk4),
                     ordenes_euler, ordenes_rk4)


def problema_2(resumen):
    """Masa-resorte: solución, plano de fase, energía, error y convergencia."""
    problema = MASA_RESORTE
    h = problema["h_base"]

    t, y_euler = analisis.resolver("Euler", problema, h)
    t, y_rk4 = analisis.resolver("RK4", problema, h)
    y_exacta = analisis.solucion_exacta(problema, t)
    t_fino = malla_fina(problema)
    y_fina = analisis.solucion_exacta(problema, t_fino)

    error_euler = analisis.error_por_punto(y_euler, y_exacta)
    error_rk4 = analisis.error_por_punto(y_rk4, y_exacta)

    graficas.grafica_simple(
        [(t_fino, y_fina[:, 0], "Analítica"),
         (t, y_euler[:, 0], f"Euler (h = {h})"),
         (t, y_rk4[:, 0], f"RK4 (h = {h})")],
        "Masa-resorte: posición",
        "Tiempo t", "Posición x(t)", "p2_solucion.png")

    graficas.grafica_simple(
        [(y_fina[:, 0], y_fina[:, 1], "Analítica"),
         (y_euler[:, 0], y_euler[:, 1], f"Euler (h = {h})"),
         (y_rk4[:, 0], y_rk4[:, 1], f"RK4 (h = {h})")],
        "Masa-resorte: plano de fase",
        "Posición x", "Velocidad x'", "p2_fase.png")

    # Energía por unidad de masa; el valor exacto es 2 en todo t
    energia_euler = analisis.energia_masa_resorte(y_euler)
    energia_rk4 = analisis.energia_masa_resorte(y_rk4)
    graficas.grafica_simple(
        [(t, np.full(len(t), 2.0), "Valor exacto (E = 2)"),
         (t, energia_euler, f"Euler (h = {h})"),
         (t, energia_rk4, f"RK4 (h = {h})")],
        "Masa-resorte: energía E(t) = (x')²/2 + 2x²",
        "Tiempo t", "Energía por unidad de masa E(t)", "p2_energia.png")

    tablas.tabla_energia("p2_energia.csv", [
        ["Euler", energia_euler[-1], energia_euler[-1] - 2.0],
        ["RK4", energia_rk4[-1], energia_rk4[-1] - 2.0],
    ])

    graficas.grafica_simple(
        [(t[1:], error_euler[1:], f"Euler (h = {h})"),
         (t[1:], error_rk4[1:], f"RK4 (h = {h})")],
        "Masa-resorte: norma del error",
        "Tiempo t", "Error ||y_num(t) - y(t)||", "p2_error.png", escala_log=True)

    errores_euler, ordenes_euler, errores_rk4, ordenes_rk4 = convergencia_con_tabla(
        problema, PASOS_CONVERGENCIA, "p2_convergencia.csv")
    graficas.grafica_convergencia(PASOS_CONVERGENCIA, errores_euler, errores_rk4,
                                  "Masa-resorte: convergencia",
                                  "p2_convergencia.png")

    resumen.append([problema["nombre"], "Euler", h, np.max(error_euler), error_euler[-1]])
    resumen.append([problema["nombre"], "RK4", h, np.max(error_rk4), error_rk4[-1]])
    imprimir_resumen(problema, h, np.max(error_euler), np.max(error_rk4),
                     ordenes_euler, ordenes_rk4)
    print(f"  Energía en t = {problema['t_final']:g} (exacta 2):  "
          f"Euler = {energia_euler[-1]:.4f}   RK4 = {energia_rk4[-1]:.8f}")


def problema_3(resumen):
    """Sistema lineal 2x2: solución, error absoluto y relativo, y convergencia."""
    problema = SISTEMA_LINEAL
    h = problema["h_base"]

    t, y_euler = analisis.resolver("Euler", problema, h)
    t, y_rk4 = analisis.resolver("RK4", problema, h)
    y_exacta = analisis.solucion_exacta(problema, t)
    t_fino = malla_fina(problema)
    y_fina = analisis.solucion_exacta(problema, t_fino)

    error_euler = analisis.error_por_punto(y_euler, y_exacta)
    error_rk4 = analisis.error_por_punto(y_rk4, y_exacta)
    error_relativo_euler = analisis.error_relativo_por_punto(y_euler, y_exacta)
    error_relativo_rk4 = analisis.error_relativo_por_punto(y_rk4, y_exacta)

    curvas_x = [(t_fino, y_fina[:, 0], "Analítica"),
                (t, y_euler[:, 0], f"Euler (h = {h})"),
                (t, y_rk4[:, 0], f"RK4 (h = {h})")]
    curvas_y = [(t_fino, y_fina[:, 1], "Analítica"),
                (t, y_euler[:, 1], f"Euler (h = {h})"),
                (t, y_rk4[:, 1], f"RK4 (h = {h})")]
    graficas.grafica_dos_paneles(
        curvas_x, curvas_y, ["Componente x(t)", "Componente y(t)"],
        "Tiempo t", ["x(t)", "y(t)"],
        "Sistema lineal x' = 2x + y, y' = x + 2y", "p3_solucion.png")

    graficas.grafica_dos_paneles(
        [(t[1:], error_euler[1:], f"Euler (h = {h})"),
         (t[1:], error_rk4[1:], f"RK4 (h = {h})")],
        [(t[1:], error_relativo_euler[1:], f"Euler (h = {h})"),
         (t[1:], error_relativo_rk4[1:], f"RK4 (h = {h})")],
        ["Error absoluto", "Error relativo"],
        "Tiempo t", ["||y_num(t) - y(t)||", "||y_num(t) - y(t)|| / ||y(t)||"],
        "Sistema lineal: error absoluto y relativo", "p3_error.png", escala_log=True)

    errores_euler, ordenes_euler, errores_rk4, ordenes_rk4 = convergencia_con_tabla(
        problema, PASOS_CONVERGENCIA, "p3_convergencia.csv")
    graficas.grafica_convergencia(PASOS_CONVERGENCIA, errores_euler, errores_rk4,
                                  "Sistema lineal: convergencia",
                                  "p3_convergencia.png")

    resumen.append([problema["nombre"], "Euler", h, np.max(error_euler), error_euler[-1]])
    resumen.append([problema["nombre"], "RK4", h, np.max(error_rk4), error_rk4[-1]])
    imprimir_resumen(problema, h, np.max(error_euler), np.max(error_rk4),
                     ordenes_euler, ordenes_rk4)
    print(f"  Error relativo final con h = {h}:  Euler = {error_relativo_euler[-1]:.4e}   "
          f"RK4 = {error_relativo_rk4[-1]:.4e}")


def problema_4(resumen):
    """Van der Pol: solución, retrato de fase, convergencia y diferencias sucesivas."""
    problema = VAN_DER_POL
    h = problema["h_base"]

    t, y_euler = analisis.resolver("Euler", problema, h)
    t, y_rk4 = analisis.resolver("RK4", problema, h)
    y_referencia = analisis.referencia_scipy(problema, t)

    error_euler = analisis.error_por_punto(y_euler, y_referencia)
    error_rk4 = analisis.error_por_punto(y_rk4, y_referencia)

    graficas.grafica_simple(
        [(t, y_referencia[:, 0], "Referencia (SciPy DOP853)"),
         (t, y_euler[:, 0], f"Euler (h = {h})"),
         (t, y_rk4[:, 0], f"RK4 (h = {h})")],
        "Van der Pol (μ = 1): posición",
        "Tiempo t", "Posición x(t)", "p4_solucion.png", leyenda_abajo=True)

    graficas.grafica_simple(
        [(y_referencia[:, 0], y_referencia[:, 1], "Referencia (SciPy DOP853)"),
         (y_euler[:, 0], y_euler[:, 1], f"Euler (h = {h})"),
         (y_rk4[:, 0], y_rk4[:, 1], f"RK4 (h = {h})")],
        "Van der Pol (μ = 1): retrato de fase",
        "Posición x", "Velocidad y = x'", "p4_fase.png")

    errores_euler, ordenes_euler, errores_rk4, ordenes_rk4 = convergencia_con_tabla(
        problema, PASOS_VAN_DER_POL, "p4_convergencia.csv")
    graficas.grafica_convergencia(PASOS_VAN_DER_POL, errores_euler, errores_rk4,
                                  "Van der Pol: convergencia respecto a la referencia",
                                  "p4_convergencia.png",
                                  etiqueta_y="Error máximo contra la referencia")

    diferencias_euler, diferencias_rk4 = analisis.diferencias_sucesivas(
        problema, PASOS_VAN_DER_POL)
    tablas.tabla_diferencias_sucesivas("p4_diferencias_sucesivas.csv", PASOS_VAN_DER_POL,
                                       diferencias_euler, diferencias_rk4)
    graficas.grafica_convergencia(PASOS_VAN_DER_POL, diferencias_euler, diferencias_rk4,
                                  "Van der Pol: diferencia entre soluciones con h y h/2",
                                  "p4_diferencias_sucesivas.png",
                                  etiqueta_y="Diferencia máxima entre h y h/2")

    resumen.append([problema["nombre"], "Euler", h, np.max(error_euler), error_euler[-1]])
    resumen.append([problema["nombre"], "RK4", h, np.max(error_rk4), error_rk4[-1]])
    print(f"\n{problema['nombre']}  (error contra la referencia de SciPy)")
    print(f"  Error máximo con h = {h}:  Euler = {np.max(error_euler):.4e}   "
          f"RK4 = {np.max(error_rk4):.4e}")
    print(f"  Órdenes observados Euler: {texto_ordenes(ordenes_euler)}")
    print(f"  Órdenes observados RK4:   {texto_ordenes(ordenes_rk4)}")
    print("  Diferencia máxima entre h y h/2:")
    for i in range(len(PASOS_VAN_DER_POL)):
        print(f"    h = {PASOS_VAN_DER_POL[i]:<7} Euler = {diferencias_euler[i]:.4e}   "
              f"RK4 = {diferencias_rk4[i]:.4e}")


def main():
    """Ejecuta todos los problemas en orden y guarda los resultados."""
    os.makedirs(graficas.CARPETA_FIGURAS, exist_ok=True)
    os.makedirs(tablas.CARPETA_TABLAS, exist_ok=True)

    print("Proyecto final - Ecuaciones Diferenciales 1")
    print("Métodos numéricos: Euler y Runge-Kutta de orden 4 (RK4)")

    resumen = []
    problema_1(resumen)
    problema_2(resumen)
    problema_3(resumen)
    problema_4(resumen)

    tablas.tabla_resumen("resumen_paso_base.csv", resumen)
    print("\nFiguras guardadas en resultados/figuras/ y tablas en resultados/tablas/")


if __name__ == "__main__":
    main()
