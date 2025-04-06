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

#funcion para limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
    
#funcion para cargar datos empleados con pickle
def cargar_datos_empleados ():
    global ultimo_id, lista_empleados
    if os.path.exists("empleados.pkl"):
        with open("empleados.pkl", "rb") as file:
            datos = pickle.load(file)
            lista_empleados = datos["empleados"]
            ultimo_id = datos["ultimo_id"]
    else:
        lista_empleados = []
        ultimo_id = 0
        
 # Función para cargar datos del historial de nómina con pickle
def cargar_datos_historial():
    global lista_historial_nomina
    if os.path.exists("lista_historial_nomina.pkl"):
        with open("lista_historial_nomina.pkl", "rb") as file:
            lista_historial_nomina = pickle.load(file)
    else:
        lista_historial_nomina = {}


        
# Función para guardar datos empleados con pickle
def guardar_datos_empleados():
    datos = {"empleados": lista_empleados, "ultimo_id": ultimo_id}
    with open("empleados.pkl", "wb") as file:
        pickle.dump(datos, file)
    
# Función para guardar datos del historial de nómina con pickle
def guardar_datos_historial():
    with open("lista_historial_nomina.pkl", "wb") as file:
        pickle.dump(lista_historial_nomina, file)
                
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
                print(Fore.RED + "Error: El campo no puede estar vacío.")
        elif tipo == "entero":
            try:
                valor = int(valor)
                if valor > 0:
                    return valor
                else:
                    print(Fore.RED + "Error: El valor debe ser un entero mayor que 0.")
            except ValueError:
                print(Fore.RED + "Error: Ingrese un número entero válido.")

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
        print(Fore.RED + "No hay empleados registrados.")
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
        print(Fore.CYAN + "\nEmpleado registrado:")
        print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
        
        # e. ¿Desea registrar otro empleado?
        if not respuesta_usuario("¿Desea registrar otro empleado?"):
            break
    
    # Guardar datos
    guardar_datos_empleados()

# Función para mostrar la lista de empleados
def mostrar_lista_empleados():
    if not verificar_lista():
        return
    tabla = [[emp["id"], emp["nombre"], emp["salario_basico"]] for emp in lista_empleados]
    encabezados = ["ID", "Nombre", "Salario Básico"]
    print(Fore.CYAN + "\nLista de Empleados:")
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))

# Función para actualizar datos de un empleado
def actualizar_empleado():
    if not verificar_lista():
        return
    
    # Mostrar la lista de empleados para que el usuario pueda ver los IDs
    mostrar_lista_empleados()
    
    # Pedir el ID del empleado a actualizar
    id_buscar = leer_datos("ID del empleado a actualizar", tipo="entero")
    
    # Buscar el empleado en la lista
    empleado_encontrado = None
    for empleado in lista_empleados:
        if empleado["id"] == id_buscar:
            empleado_encontrado = empleado
            break
    
    if empleado_encontrado is None:
        print(Fore.RED + f"No se encontró un empleado con ID {id_buscar}.") 
        return
    
    # Mostrar los datos actuales del empleado
    print(Fore.CYAN + "\nDatos actuales del empleado:")  
    tabla = [[empleado_encontrado["id"], empleado_encontrado["nombre"], empleado_encontrado["salario_basico"]]]
    encabezados = ["ID", "Nombre", "Salario Básico"]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    # Preguntar qué desea actualizar
    print("\n¿Qué desea actualizar?")
    print("1. Nombre")
    print("2. Salario básico")
    print("3. Ambos")
    print("4. Cancelar")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1" or opcion == "3":
        nuevo_nombre = leer_datos("nuevo nombre")
        empleado_encontrado["nombre"] = nuevo_nombre
    
    if opcion == "2" or opcion == "3":
        nuevo_salario = leer_datos("nuevo salario básico", tipo="entero")
        empleado_encontrado["salario_basico"] = nuevo_salario
    
    if opcion == "4":
        print(Fore.YELLOW + "Actualización cancelada.") 
        return
    
    if opcion not in ["1", "2", "3", "4"]:
        print(Fore.RED + "Opción no válida. Actualización cancelada.") 
        return
    
    # Mostrar los datos actualizados
    print(Fore.CYAN + "\nDatos actualizados del empleado:") 
    tabla = [[empleado_encontrado["id"], empleado_encontrado["nombre"], empleado_encontrado["salario_basico"]]]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    # Guardar los cambios
    guardar_datos_empleados()
    print(Fore.GREEN + "Datos actualizados exitosamente.")

# Función para eliminar un empleado
def eliminar_empleado():
    if not verificar_lista():
        return
    
    # Mostrar la lista de empleados para que el usuario pueda ver los IDs
    mostrar_lista_empleados()
    
    # Pedir el ID del empleado a eliminar
    id_buscar = leer_datos("ID del empleado a eliminar", tipo="entero")
    
    # Buscar el empleado en la lista
    empleado_encontrado = None
    for empleado in lista_empleados:
        if empleado["id"] == id_buscar:
            empleado_encontrado = empleado
            break
    
    if empleado_encontrado is None:
        print(Fore.RED + f"No se encontró un empleado con ID {id_buscar}.") 
        return
    
    # Mostrar los datos del empleado a eliminar
    print(Fore.CYAN + "\nDatos del empleado a eliminar:") 
    tabla = [[empleado_encontrado["id"], empleado_encontrado["nombre"], empleado_encontrado["salario_basico"]]]
    encabezados = ["ID", "Nombre", "Salario Básico"]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    # Confirmar eliminación
    if not respuesta_usuario("¿Está seguro de que desea eliminar este empleado?"):
        print(Fore.YELLOW + "Eliminación cancelada.") 
        return
    
    # Eliminar el empleado de la lista
    lista_empleados.remove(empleado_encontrado)
    
    # Guardar los cambios
    guardar_datos_empleados()
    print(Fore.GREEN + "Empleado eliminado exitosamente.")

# Función para calcular datos de nómina
def calcular_nomina():
    if not verificar_lista():
        return
    
    # Pedir el año y mes para los cálculos
    while True:
        try:
            anio = int(input("Ingrese el año (por ejemplo, 2025): "))
            if anio < 2000 or anio > 2100:
                print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un año válido.")
    
    while True:
        try:
            mes = int(input("Ingrese el mes (1-12): "))
            if mes < 1 or mes > 12:
                print(Fore.RED + "Error: El mes debe estar entre 1 y 12.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un mes válido.")
    
    # Formatear la clave de año/mes (por ejemplo, "2025-04")
    clave_fecha = f"{anio}-{mes:02d}"
    
    # Cargar el historial existente
    cargar_datos_historial()
    
    # Verificar si ya existe una nómina para ese año/mes
    if clave_fecha in lista_historial_nomina:
        print(Fore.YELLOW + f"Ya existe una nómina registrada para {clave_fecha}.")
        if not respuesta_usuario("¿Desea sobrescribir los datos existentes?"):
            print(Fore.YELLOW + "Cálculo de nómina cancelado.")
            return
    
    # Crear un diccionario para los cálculos de este mes
    nomina_mes = {}
    
    # Calcular datos para cada empleado
    for empleado in lista_empleados:
        salario_basico = empleado["salario_basico"]
        
        # Calcular auxilio de transporte
        auxilio_transporte = AUXILIO_TRANSPORTE_MENSUAL if salario_basico <= LIMITE_TRANSPORTE else 0
        
        # Calcular deducciones
        deduccion_salud = salario_basico * PORCENTAJE_SALUD
        deduccion_pension = salario_basico * PORCENTAJE_PENSION
        
        # Calcular salario neto
        salario_neto = salario_basico + auxilio_transporte - (deduccion_salud + deduccion_pension)
        
        # Crear diccionario con los datos del empleado y los cálculos
        nomina_empleado = {
            "nombre": empleado["nombre"],
            "salario_basico": salario_basico,
            "auxilio_transporte": auxilio_transporte,
            "deduccion_salud": deduccion_salud,
            "deduccion_pension": deduccion_pension,
            "salario_neto": salario_neto
        }
        
        # Agregar al diccionario del mes usando el ID como clave
        nomina_mes[empleado["id"]] = nomina_empleado
    
    # Guardar los cálculos en lista_historial_nomina
    lista_historial_nomina[clave_fecha] = nomina_mes
    
    # Guardar en el archivo
    guardar_datos_historial()
    
    # Mostrar los resultados
    print(Fore.CYAN + f"\nNómina calculada para {clave_fecha}:")
    tabla = []
    for id_empleado, datos in nomina_mes.items():
        tabla.append([
            id_empleado,
            datos["nombre"],
            datos["salario_basico"],
            datos["auxilio_transporte"],
            datos["deduccion_salud"],
            datos["deduccion_pension"],
            datos["salario_neto"]
        ])
    encabezados = ["ID", "Nombre", "Salario Básico", "Aux. Transporte", "Ded. Salud", "Ded. Pensión", "Salario Neto"]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    print(Fore.GREEN + "Cálculos de nómina guardados exitosamente.")