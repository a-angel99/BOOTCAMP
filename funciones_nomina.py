""" Esta es la libreria con todas las funciones para realizar los calculos y reportes de nomina
"""
# Importar librerias
import os
import colorama
from colorama import init, Fore, Style
from tabulate import tabulate
import matplotlib
import matplotlib.pyplot as plt  # Importar pyplot para los gráficos
import pickle
import sys

# Inicializar Colorama
colorama.init(autoreset=True)

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
historial_nomina = {}

def cargar_datos_empleados():
    global ultimo_id, lista_empleados
    try:
        if os.path.exists("empleados.pkl"):
            with open("empleados.pkl", "rb") as file:
                datos = pickle.load(file)
                lista_empleados = datos["empleados"]
                ultimo_id = datos["ultimo_id"]
        else:
            lista_empleados = []
            ultimo_id = 0
    except (pickle.PickleError, EOFError, FileNotFoundError) as e:
        print(Fore.RED + f"Error al cargar empleados.pkl: {e}")
        lista_empleados = []
        ultimo_id = 0
        
 # Función para cargar datos del historial de nómina con pickle
def cargar_datos_historial():
    global historial_nomina
    try:
        if os.path.exists("historial_nomina.pkl"):
            with open("historial_nomina.pkl", "rb") as file:
                historial_nomina = pickle.load(file)
        else:
            historial_nomina = {}
    except (pickle.PickleError, EOFError, FileNotFoundError) as e:
        print(Fore.RED + f"Error al cargar empleados.pkl: {e}")
        historial_nomina = {}
    


        
# Función para guardar datos empleados con pickle
def guardar_datos_empleados():
    datos = {"empleados": lista_empleados, "ultimo_id": ultimo_id}
    with open("empleados.pkl", "wb") as file:
        pickle.dump(datos, file)
    
# Función para guardar datos del historial de nómina con pickle
def guardar_datos_historial():
    with open("historial_nomina.pkl", "wb") as file:
        pickle.dump(historial_nomina, file)
                
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
        if respuesta in ["SI", "SÍ", "S"]:
            return True
        elif respuesta in ["NO", "N"]:
            return False
        else:
            print(Fore.RED + "Error: Ingrese SI o NO.")
            continue   

# Función para verificar si hay empleados registrados
def verificar_lista():
    if not lista_empleados:
        print(Fore.RED + "No hay empleados registrados.")
        input("Presione Enter para continuar...")
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
        if not respuesta_usuario("¿Desea registrar otro empleado? \ SI/NO   "):
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
    input("Presione Enter para continuar...")
    
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
        input("Presione Enter para continuar...")
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
        input("Presione Enter para continuar...")
        return
    
    # Mostrar los datos actualizados
    print(Fore.CYAN + "\nDatos actualizados del empleado:") 
    tabla = [[empleado_encontrado["id"], empleado_encontrado["nombre"], empleado_encontrado["salario_basico"]]]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    # Guardar los cambios
    guardar_datos_empleados()
    print(Fore.GREEN + "Datos actualizados exitosamente.")
    input("Presione Enter para continuar...")
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
        input("Presione Enter para continuar...")
        return
    
    # Mostrar los datos del empleado a eliminar
    print(Fore.CYAN + "\nDatos del empleado a eliminar:") 
    tabla = [[empleado_encontrado["id"], empleado_encontrado["nombre"], empleado_encontrado["salario_basico"]]]
    encabezados = ["ID", "Nombre", "Salario Básico"]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    # Confirmar eliminación
    if not respuesta_usuario("¿Está seguro de que desea eliminar este empleado?  SI/NO   "):
        print(Fore.YELLOW + "Eliminación cancelada.") 
        input("Presione Enter para continuar...")
        return
    
    # Eliminar el empleado de la lista
    lista_empleados.remove(empleado_encontrado)
    
    # Guardar los cambios
    guardar_datos_empleados()
    print(Fore.GREEN + "Empleado eliminado exitosamente.")
    input("Presione Enter para continuar...")

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
    if clave_fecha in historial_nomina:
        print(Fore.YELLOW + f"Ya existe una nómina registrada para {clave_fecha}.")
        if not respuesta_usuario("¿Desea sobrescribir los datos existentes?  SI/NO   "):
            print(Fore.YELLOW + "Cálculo de nómina cancelado.")
            input("Presione Enter para continuar...")
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
        
        # asegurando que los valores sean enteros
        deduccion_salud = int(deduccion_salud)
        deduccion_pension = int(deduccion_pension)
        # Calcular salario neto
        salario_neto = (salario_basico + auxilio_transporte - (deduccion_salud + deduccion_pension))
        salario_neto = int(salario_neto)
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
    historial_nomina[clave_fecha] = nomina_mes
    
    # Guardar en el archivo
    guardar_datos_historial()
    
    # Mostrar los resultados
    print(Fore.CYAN + f"\nNómina calculada para {clave_fecha}:")
    tabla = []
    for id_empleado, datos in nomina_mes.items():
         # Asegurarse de que todos los valores sean números y enteros
        tabla.append([
            id_empleado,
            datos["nombre"],
            int(datos["salario_basico"]),
            int(datos["auxilio_transporte"]),
            int(datos["deduccion_salud"]),
            int(datos["deduccion_pension"]),
            int(datos["salario_neto"])
        ])
    encabezados = ["ID", "Nombre", "Salario Básico", "Aux. Transporte", "Ded. Salud", "Ded. Pensión", "Salario Neto"]
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    print(Fore.GREEN + "Cálculos de nómina guardados exitosamente.")
    input("Presione Enter para continuar...")
    
# Función para generar el reporte de listado de empleados
def generar_reporte_listado_empleados():
    # Verificar si hay datos de nómina
    if not historial_nomina:
        print(Fore.RED + "No hay datos de nómina registrados.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Mostrar opciones de filtrado
    print(Fore.CYAN + "\nOpciones de filtrado para el reporte:")
    opciones = [
        ["1", "Mes específico"],
        ["2", "Rango de meses"],
        ["3", "Reporte completo"]
    ]
    print(tabulate(opciones, headers=["Opción", "Descripción"], tablefmt="grid"))
    opcion = input("Seleccione una opción: ")
    
    # Lista de claves (meses) a mostrar
    claves_a_mostrar = []
    
    if opcion == "1":
        # Mes específico
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
        
        clave_fecha = f"{anio}-{mes:02d}"
        if clave_fecha not in historial_nomina:
            print(Fore.RED + f"No hay datos de nómina para {clave_fecha}.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
        claves_a_mostrar = [clave_fecha]
    
    elif opcion == "2":
        # Rango de meses
        print(Fore.CYAN + "\nIngrese el rango de meses (inicio):")
        while True:
            try:
                anio_inicio = int(input("Ingrese el año de inicio (por ejemplo, 2025): "))
                if anio_inicio < 2000 or anio_inicio > 2100:
                    print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un año válido.")
        
        while True:
            try:
                mes_inicio = int(input("Ingrese el mes de inicio (1-12): "))
                if mes_inicio < 1 or mes_inicio > 12:
                    print(Fore.RED + "Error: El mes debe estar entre 1 y 12.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un mes válido.")
        
        print(Fore.CYAN + "\nIngrese el rango de meses (fin):")
        while True:
            try:
                anio_fin = int(input("Ingrese el año de fin (por ejemplo, 2025): "))
                if anio_fin < 2000 or anio_fin > 2100:
                    print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un año válido.")
        
        while True:
            try:
                mes_fin = int(input("Ingrese el mes de fin (1-12): "))
                if mes_fin < 1 or mes_fin > 12:
                    print(Fore.RED + "Error: El mes debe estar entre 1 y 12.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un mes válido.")
        
        # Convertir las fechas a un formato comparable (entero: AAAAMM)
        fecha_inicio = int(f"{anio_inicio}{mes_inicio:02d}")
        fecha_fin = int(f"{anio_fin}{mes_fin:02d}")
        
        if fecha_inicio > fecha_fin:
            print(Fore.RED + "Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
        
        # Filtrar las claves dentro del rango
        for clave in sorted(historial_nomina.keys()):
            anio_mes = int(clave.replace("-", ""))
            if fecha_inicio <= anio_mes <= fecha_fin:
                claves_a_mostrar.append(clave)
        
        if not claves_a_mostrar:
            print(Fore.RED + f"No hay datos de nómina en el rango {anio_inicio}-{mes_inicio:02d} a {anio_fin}-{mes_fin:02d}.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
    
    elif opcion == "3":
        # Reporte completo
        claves_a_mostrar = sorted(historial_nomina.keys())
    
    else:
        print(Fore.RED + "Opción no válida.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Generar el reporte
    print(Fore.CYAN + "\nReporte de Listado de Empleados:")
    tabla = []
    # Añadir los encabezados con la columna "Mes"
    encabezados = ["Mes", "ID", "Nombre", "Salario Básico", "Ded. Salud", "Ded. Pensión", "Salario Neto"]
    
    # Recorrer los meses seleccionados
    for clave in claves_a_mostrar:
        nomina_mes = historial_nomina[clave]
        for id_empleado, datos in nomina_mes.items():
            tabla.append([
                clave,  # Añadir el mes como primera columna
                id_empleado,
                datos["nombre"],
                int(datos["salario_basico"]),
                int(datos["deduccion_salud"]),
                int(datos["deduccion_pension"]),
                int(datos["salario_neto"])
            ])
    
    # Mostrar la tabla
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    print(Fore.GREEN + "Reporte generado exitosamente.")
    sys.stdout.flush()
    input("Presione Enter para continuar...")

# Función para generar el reporte de aportes a seguridad social
def generar_reporte_aportes_seguridad_social():
    # Verificar si hay datos de nómina
    if not historial_nomina:
        print(Fore.RED + "No hay datos de nómina registrados.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Mostrar opciones de filtrado
    print(Fore.CYAN + "\nOpciones de filtrado para el reporte:")
    opciones = [
        ["1", "Mes específico"],
        ["2", "Rango de meses"],
        ["3", "Reporte completo"]
    ]
    print(tabulate(opciones, headers=["Opción", "Descripción"], tablefmt="grid"))
    opcion = input("Seleccione una opción: ")
    
    # Lista de claves (meses) a mostrar
    claves_a_mostrar = []
    
    if opcion == "1":
        # Mes específico
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
        
        clave_fecha = f"{anio}-{mes:02d}"
        if clave_fecha not in historial_nomina:
            print(Fore.RED + f"No hay datos de nómina para {clave_fecha}.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
        claves_a_mostrar = [clave_fecha]
    
    elif opcion == "2":
        # Rango de meses
        print(Fore.CYAN + "\nIngrese el rango de meses (inicio):")
        while True:
            try:
                anio_inicio = int(input("Ingrese el año de inicio (por ejemplo, 2025): "))
                if anio_inicio < 2000 or anio_inicio > 2100:
                    print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un año válido.")
        
        while True:
            try:
                mes_inicio = int(input("Ingrese el mes de inicio (1-12): "))
                if mes_inicio < 1 or mes_inicio > 12:
                    print(Fore.RED + "Error: El mes debe estar entre 1 y 12.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un mes válido.")
        
        print(Fore.CYAN + "\nIngrese el rango de meses (fin):")
        while True:
            try:
                anio_fin = int(input("Ingrese el año de fin (por ejemplo, 2025): "))
                if anio_fin < 2000 or anio_fin > 2100:
                    print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un año válido.")
        
        while True:
            try:
                mes_fin = int(input("Ingrese el mes de fin (1-12): "))
                if mes_fin < 1 or mes_fin > 12:
                    print(Fore.RED + "Error: El mes debe estar entre 1 y 12.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un mes válido.")
        
        # Convertir las fechas a un formato comparable (entero: AAAAMM)
        fecha_inicio = int(f"{anio_inicio}{mes_inicio:02d}")
        fecha_fin = int(f"{anio_fin}{mes_fin:02d}")
        
        if fecha_inicio > fecha_fin:
            print(Fore.RED + "Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
        
        # Filtrar las claves dentro del rango
        for clave in sorted(historial_nomina.keys()):
            anio_mes = int(clave.replace("-", ""))
            if fecha_inicio <= anio_mes <= fecha_fin:
                claves_a_mostrar.append(clave)
        
        if not claves_a_mostrar:
            print(Fore.RED + f"No hay datos de nómina en el rango {anio_inicio}-{mes_inicio:02d} a {anio_fin}-{mes_fin:02d}.")
            sys.stdout.flush()
            input("Presione Enter para continuar...")
            return
    
    elif opcion == "3":
        # Reporte completo
        claves_a_mostrar = sorted(historial_nomina.keys())
    
    else:
        print(Fore.RED + "Opción no válida.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Generar el reporte
    print(Fore.CYAN + "\nResumen de Aportes a Seguridad Social:")
    tabla = []
    # Añadir los encabezados con la columna "Mes"
    encabezados = ["Mes", "ID", "Nombre", "Ded. Salud", "Ded. Pensión"]
    
    # Recorrer los meses seleccionados
    for clave in claves_a_mostrar:
        nomina_mes = historial_nomina[clave]
        for id_empleado, datos in nomina_mes.items():
            tabla.append([
                clave,  # Añadir el mes como primera columna
                id_empleado,
                datos["nombre"],
                int(datos["deduccion_salud"]),
                int(datos["deduccion_pension"])
            ])
    
    # Mostrar la tabla
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    print(Fore.GREEN + "Reporte generado exitosamente.")
    sys.stdout.flush()
    input("Presione Enter para continuar...")

# Función para generar el reporte total de nómina del mes
def generar_reporte_total_nomina_mes():
    # Verificar si hay datos de nómina
    if not historial_nomina:
        print(Fore.RED + "No hay datos de nómina registrados.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Pedir el año y mes para el reporte
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
    
    # Verificar si existe una nómina para ese año/mes
    if clave_fecha not in historial_nomina:
        print(Fore.RED + f"No hay datos de nómina para {clave_fecha}.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return
    
    # Obtener los datos de la nómina para el mes
    nomina_mes = historial_nomina[clave_fecha]
    
    # Generar el reporte
    print(Fore.CYAN + f"\nReporte Total Nómina del Mes ({clave_fecha}):")
    tabla = []
    total_nomina = 0
    
    # Recorrer los datos del mes
    for id_empleado, datos in nomina_mes.items():
        salario_neto = int(datos["salario_neto"])
        tabla.append([
            clave_fecha,  # Fecha
            id_empleado,  # ID
            datos["nombre"],  # Nombre
            salario_neto  # Salario Neto
        ])
        total_nomina += salario_neto
    
    # Añadir la fila del total
    tabla.append(["", "", "Total Nómina", total_nomina])
    
    # Añadir los encabezados
    encabezados = ["Fecha", "ID", "Nombre", "Salario Neto"]
    
    # Mostrar la tabla
    print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    
    print(Fore.GREEN + "Reporte generado exitosamente.")
    sys.stdout.flush()
    input("Presione Enter para continuar...")

# Función para generar gráficos estadísticos de pagos por mes en un año
def generar_graficos_estadisticos():
    # Verificar si hay datos de nómina
    if not historial_nomina: 
        print(Fore.RED + "No hay datos de nómina registrados.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return

    # Pedir el año para el reporte
    while True:
        try:
            anio = int(input("Ingrese el año (por ejemplo, 2025): "))
            if 2000 <= anio <= 2100:
                break
            else:
                print(Fore.RED + "Error: El año debe estar entre 2000 y 2100.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un año válido.")

    # Filtrar los datos para el año seleccionado
    datos_anio = {}
    for clave, nomina_mes in historial_nomina.items(): # Iterar sobre claves y valores
        anio_clave = int(clave.split("-")[0])
        if anio_clave == anio:
            mes = int(clave.split("-")[1])
            total_nomina = sum(datos["salario_neto"] for datos in nomina_mes.values())
            datos_anio[mes] = total_nomina

    # Verificar si hay datos para el año
    if not datos_anio:
        print(Fore.RED + f"No hay datos de nómina para el año {anio}.")
        sys.stdout.flush()
        input("Presione Enter para continuar...")
        return

    # Mostrar opciones de tipo de gráfico
    print(Fore.CYAN + "\nOpciones de tipo de gráfico:")
    opciones_grafico = [
        ["1", "Histograma de Totales Mensuales"], 
        ["2", "Pastel de Proporción Mensual"], 
        ["3", "Líneas de Tendencia Mensual"] ]  
    print(tabulate(opciones_grafico, headers=["Opción", "Tipo de Gráfico"], tablefmt="grid"))
    opcion_elegida = input("Seleccione una opción: ")

    # Preparar los datos para el gráfico
    # Ordenar por mes para el gráfico de líneas y etiquetas consistentes
    meses_ordenados = sorted(datos_anio.keys())
    totales_ordenados = [datos_anio[mes] for mes in meses_ordenados]
    # Etiquetas de texto para los ejes/leyendas (ej. "01", "02", ...)
    etiquetas_meses_str = [f"{mes:02d}" for mes in meses_ordenados]

    # Determinar el tipo de gráfico para el nombre del archivo y título
    tipo_grafico_str = ""
    titulo_grafico = f"Año {anio}" # Título base

    fig, ax = plt.subplots(figsize=(10, 6)) 

    if opcion_elegida == "1":
        tipo_grafico_str = "histograma"
        titulo_grafico = f"Distribución de Totales de Nómina Mensual - {titulo_grafico}"
        ax.bar(etiquetas_meses_str, totales_ordenados, edgecolor='black')
        ax.set_xlabel("Mes")
        ax.set_ylabel("Total Nómina Pagada")
        ax.set_title(titulo_grafico)
      

    elif opcion_elegida == "2":
        tipo_grafico_str = "pastel"
        titulo_grafico = f"Proporción de Nómina por Mes - {titulo_grafico}"
        ax.pie(totales_ordenados, labels=etiquetas_meses_str, autopct='%1.1f%%', startangle=90)
        ax.set_title(titulo_grafico)
        ax.axis('equal') # Asegura que el pastel sea circular

    elif opcion_elegida == "3":
        tipo_grafico_str = "lineas"
        titulo_grafico = f"Tendencia de Nómina Mensual - {titulo_grafico}"
        ax.plot(etiquetas_meses_str, totales_ordenados, marker='o', linestyle='-')
        ax.set_xlabel("Mes")
        ax.set_ylabel("Total Nómina Pagada")
        ax.set_title(titulo_grafico)
        ax.grid(True)

    else:
        print(Fore.RED + "Opción no válida.")
        sys.stdout.flush() 
        input("Presione Enter para continuar...")
        plt.close(fig) # Cerrar la figura si la opción no es válida
        return 

    # Ajustar diseño y mostrar el gráfico generado
    fig.tight_layout()
    plt.show()

    # Preguntar si desea guardar el gráfico como PDF
    if respuesta_usuario("¿Desea guardar el gráfico como PDF?  SI/NO  "):
        # Crear nombre de archivo dinámico
        nombre_archivo = f"grafico_nomina_{anio}_{tipo_grafico_str}.pdf"
        try:
            # Guardar la figura que ya se mostró
            fig.savefig(nombre_archivo, format='pdf')
            print(Fore.GREEN + f"Gráfico guardado como {nombre_archivo}.")
        except Exception as e:
            print(Fore.RED + f"Error al guardar el PDF: {e}")
    else:
        print(Fore.YELLOW + "Gráfico no guardado.")

    # Cerrar explícitamente la figura después de mostrar y/o guardar
    plt.close(fig)

    sys.stdout.flush() 
    input("Presione Enter para continuar...")