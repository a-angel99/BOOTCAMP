""" Esta es la libreria con todas las funciones para realizar los calculos y reportes de nomina
"""
# Importar librerias
import os
from colorama import init, Fore, Style
init(autoreset=True)
import tabulate
import matplotlib
import pickle

# CONSTANTES:
SMLV = 1423500
LIMITE_TRANSPORTE = 2 * SMLV
AUXILIO_TRANSPORTE_MENSUAL = 200000
PORCENTAJE_SALUD = 0.04
PORCENTAJE_PENSION = 0.04
ARCHIVO_DATOS = "datos_nomina.pkl"

# --- VARIABLES GLOBALES 
# (Estas variables mantendrán el estado mientras el programa corre. Se cargan al inicio y se guardan al salir o tras cambios)
