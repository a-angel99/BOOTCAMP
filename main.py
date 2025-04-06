import os 
from funciones_nomina import *
import colorama
from colorama import Fore, Style
from tabulate import tabulate

# Inicializar Colorama
colorama.init()
init(autoreset=True)

#funcion para limpiar pantalla: esta funcion no esta en funciones_nomina porque estaba generando problemas
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu():
    limpiar_pantalla()
    cargar_datos_empleados()
    cargar_datos_historial()
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "\n--- Sistema de Nómina ---")
        opciones = [
            ["1", "Registrar empleado"],
            ["2", "Consultar lista de empleados"],
            ["3", "Actualizar datos de empleado"],
            ["4", "Eliminar empleado"],
            ["5", "Calcular datos de nómina"],
            ["6", "Reporte nomina de empleados"],
            ["7", "Salir"]
        ]
        print(tabulate(opciones, headers=["Opción", "Descripción"], tablefmt="grid"))
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            limpiar_pantalla()
            registrar_empleado() 
        elif opcion == "2":
            limpiar_pantalla()
            mostrar_lista_empleados()
        elif opcion == "3":
            limpiar_pantalla()
            actualizar_empleado()
        elif opcion == "4":
            limpiar_pantalla()
            eliminar_empleado()
        elif opcion == "5":
            limpiar_pantalla()
            calcular_nomina()
        elif opcion == "6":
            limpiar_pantalla()
            generar_reporte_listado_empleados()
        elif opcion == "7":
            if respuesta_usuario("¿Desea salir?"):
                guardar_datos_empleados()
                print(Fore.GREEN + "¡Gracias por usar el sistema!")
                break
        else:
            print(Fore.RED + "Opción no válida.")
            
if __name__ == "__main__":
    menu()
    