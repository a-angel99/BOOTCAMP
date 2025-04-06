from funciones_nomina import *
import colorama
from colorama import Fore, Style
from tabulate import tabulate
import os
# Inicializar Colorama
colorama.init()
init(autoreset=True)

def menu():
    cargar_datos_empleados()
    cargar_datos_historial()
    while True:
        print(Fore.CYAN + "\n--- Sistema de Nómina ---")
        opciones = [
            ["1", "Registrar empleado"],
            ["2", "Consultar lista de empleados"],
            ["3", "Actualizar datos de empleado"],
            ["4", "Eliminar empleado"],
            ["5", "Calcular datos de nómina"],
            ["6", "Salir"]
        ]
        print(tabulate(opciones, headers=["Opción", "Descripción"], tablefmt="grid"))
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_empleado() 
        elif opcion == "2":
            mostrar_lista_empleados()
        elif opcion == "3":
            actualizar_empleado()
        elif opcion == "4":
            eliminar_empleado()
        elif opcion == "5":
            calcular_nomina()
        elif opcion == "6":
            if respuesta_usuario("¿Desea salir?"):
                guardar_datos_empleados()
                print(Fore.GREEN + "¡Gracias por usar el sistema!")
                break
        else:
            print(Fore.RED + "Opción no válida.")
            
if __name__ == "__main__":
    menu()
    