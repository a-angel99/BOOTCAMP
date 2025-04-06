""" Esta es la libreria con todas las funciones para realizar los calculos y reportes de nomina
"""
# Importar librerias
import os
import colorama
from colorama import init, Fore, Style
from tabulate import tabulate
import matplotlib
import pickle

# Inicializar Colorama
colorama.init()
init(autoreset=True)
# CONSTANTES:
SMLV = 1423500
LIMITE_TRANSPORTE = 2 * SMLV
AUXILIO_TRANSPORTE_MENSUAL = 200000
PORCENTAJE_SALUD = 0.04
PORCENTAJE_PENSION = 0.04
ARCHIVO_DATOS = "datos_nomina.pkl"

# --- VARIABLES GLOBALES 
# ( Se cargan al inicio y se guardan al salir o tras cambios)
ultimo_id = 0
lista_empleados = []
lista_historial_nomina = []

#funcion para cargar datos con pickle
def cargar_datos ():
    global ultimo_id, lista_empleados, lista_historial_nomina
    if os.path.exists("empleados.pkl"):
        with open("empleados.pkl", "rb") as file:
            datos = pickle.load(file)
            lista_empleados = datos["empleados"]
            ultimo_id = datos["ultimo_id"]
    else:
        lista_empleados = []
        ultimo_id = 0
        
    if os.path.exists("lista_historial_nomina.pkl"):
        with open("lista_historial_nomina.pkl", "rb") as file:
            lista_historial_nomina = pickle.load(file)
    else:
        lista_historial_nomina = []
        
# Función para guardar datos con pickle
def guardar_datos():
    datos = {"empleados": lista_empleados, "ultimo_id": ultimo_id}
    with open("empleados.pkl", "wb") as file:
        pickle.dump(datos, file)
    
    with open("lista_historial_nomina.pkl", "wb") as file:
        pickle.dump(lista_historial_nomina, file)

#funcion para limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
        
# Función para generar ID
def generar_id():
    global ultimo_id
    ultimo_id += 1
    return ultimo_id

# Función para leer datos con validaciones
def leer_datos(campo, tipo="texto"):
    while True:
        valor = input(f"Ingrese {campo}: ").strip()
        if tipo == "texto":
            if valor:
                return valor
            else:
                print("Error: El campo no puede estar vacío.")
        elif tipo == "entero":
            try:
                valor = int(valor)
                if valor > 0:
                    return valor
                else:
                    print("Error: El valor debe ser un entero mayor que 0.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")

# Función para preguntar si desea continuar
def respuesta_usuario(mensaje):
    while True:
        respuesta = input(mensaje).upper()
        if respuesta == "SI":
            return True
        elif respuesta == "NO":
            return False
        else:
            print(Fore.RED + "Error: Ingrese SI o NO.")
            continue   

# Función para verificar si hay empleados registrados
def verificar_lista():
    if not lista_empleados:
        print("No hay empleados registrados.")
        return False
    return True

# Función para registrar empleado
def registrar_empleado():
    while True:
        # a. Leer nombre
        nombre = leer_datos("nombre")
        
        # b. Leer salario básico
        salario_basico = leer_datos("salario básico mensual", tipo="entero")
        
        # c. Generar ID
        id_empleado = generar_id()
        
        # Crear diccionario del empleado
        empleado = {
            "id": id_empleado,
            "nombre": nombre,
            "salario_basico": salario_basico
        }
        
        # Agregar a la lista
        lista_empleados.append(empleado)
        
        # d. Mostrar diccionario
        tabla = [[empleado["id"], empleado["nombre"], empleado["salario_basico"]]]
        encabezados = ["ID", "Nombre", "Salario Básico"]
        print("\nEmpleado registrado:")
        print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
        
        # e. ¿Desea registrar otro empleado?
        if not respuesta_usuario("¿Desea registrar otro empleado?"):
            break
    
    # Guardar datos
    guardar_datos()

# Función para mostrar la lista de empleados
def mostrar_lista_empleados():
    if not verificar_lista():
        return
    tabla = [[emp["id"], emp["nombre"], emp["salario_basico"]] for emp in lista_empleados]
    encabezados = ["ID", "Nombre", "Salario Básico"]
    print("\nLista de Empleados:")
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    