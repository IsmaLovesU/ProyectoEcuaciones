# tablas.py
# Funciones para escribir las tablas de resultados en formato CSV
# (carpeta resultados/tablas), usando el módulo estándar csv.

import csv
import os


CARPETA_TABLAS = os.path.join("resultados", "tablas")


def formatear_numero(valor):
    """
    Convierte un número a texto con 6 cifras significativas.
    Los números pequeños (o muy grandes) se escriben en notación científica.

    Recibe: un número o None.
    Devuelve: el texto para el CSV ("" si el valor es None).
    """
    if valor is None:
        return ""
    valor = float(valor)
    if valor != 0 and (abs(valor) < 1e-2 or abs(valor) >= 1e5):
        return f"{valor:.5e}"
    return f"{valor:.6g}"


def escribir_csv(nombre_archivo, encabezados, filas):
    """
    Escribe un archivo CSV en resultados/tablas.

    Recibe: el nombre del archivo, la lista de encabezados y una lista de filas
    (cada fila es una lista de valores; los números se formatean).
    No devuelve nada.
    """
    ruta = os.path.join(CARPETA_TABLAS, nombre_archivo)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        for fila in filas:
            fila_texto = []
            for valor in fila:
                if isinstance(valor, str):
                    fila_texto.append(valor)
                else:
                    fila_texto.append(formatear_numero(valor))
            escritor.writerow(fila_texto)


def tabla_convergencia(nombre_archivo, pasos, errores_euler, ordenes_euler,
                       errores_rk4, ordenes_rk4):
    """
    Escribe la tabla de convergencia de un problema.

    Recibe: el nombre del archivo, los pasos, y los errores y órdenes de cada método.
    No devuelve nada.
    """
    filas = []
    for i in range(len(pasos)):
        filas.append([pasos[i], errores_euler[i], ordenes_euler[i],
                      errores_rk4[i], ordenes_rk4[i]])

    escribir_csv(nombre_archivo,
                 ["h", "error_max_euler", "orden_euler", "error_max_rk4", "orden_rk4"],
                 filas)


def tabla_diferencias_sucesivas(nombre_archivo, pasos, diferencias_euler, diferencias_rk4):
    """
    Escribe la tabla de diferencias entre las soluciones con paso h y h/2.

    Recibe: el nombre del archivo, los pasos y las diferencias de cada método.
    No devuelve nada.
    """
    filas = []
    for i in range(len(pasos)):
        filas.append([pasos[i], diferencias_euler[i], diferencias_rk4[i]])

    escribir_csv(nombre_archivo, ["h", "dif_max_euler", "dif_max_rk4"], filas)


def tabla_energia(nombre_archivo, filas):
    """
    Escribe la tabla de energía final del masa-resorte.

    Recibe: el nombre del archivo y filas [metodo, energia_final, desviacion_final].
    No devuelve nada.
    """
    escribir_csv(nombre_archivo, ["metodo", "energia_final", "desviacion_final"], filas)


def tabla_resumen(nombre_archivo, filas):
    """
    Escribe el resumen de errores con el paso base de cada problema.

    Recibe: el nombre del archivo y filas [problema, metodo, h, error_max, error_final].
    No devuelve nada.
    """
    escribir_csv(nombre_archivo, ["problema", "metodo", "h", "error_max", "error_final"], filas)
