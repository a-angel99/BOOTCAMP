from funciones_nomina import *
import colorama
from colorama import Fore, Style
from tabulate import tabulate

# Inicializar Colorama
colorama.init()

def menu():
    cargar_datos()
    limpiar_pantalla()
    while True:
        print(Fore.CYAN + "\n--- Sistema de Nómina ---" + Style.RESET_ALL)
        print("1. Registrar empleado")
        print("2. Consultar lista de empleados")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            mostrar_lista_empleados()
        elif opcion == "3":
            if respuesta_usuario("¿Desea salir?"):
                guardar_datos()
                print(Fore.GREEN + "¡Gracias por usar el sistema!" + Style.RESET_ALL)
                break
        else:
            print(Fore.RED + "Opción no válida." + Style.RESET_ALL)

if __name__ == "__main__":
    menu()