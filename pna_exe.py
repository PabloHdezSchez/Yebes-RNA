#!/usr/bin/python3

import os
import argparse
import instrument_ethernet as it
import re

SCRIPTS_DIR = 'scripts'
INSTRUMENT_ID = ""
RUTA_MACROS = "C:\\Users\\Instrument\\Desktop\\users\\PabloH\\Macros"

def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def continuar():
    input("Continuar...")

def reemplazar_con_array(cadena, array):
    """Reemplaza %n en la cadena por el elemento n del array."""
    def reemplazo(match):
        index = int(match.group(1))
        return str(array[index]) if 0 <= index < len(array) else match.group(0)
    return re.sub(r'%(\d+)', reemplazo, cadena)

def procesar_script(cm, filename, args=[]):
    """Procesa un archivo de script y ejecuta los comandos en el instrumento."""
    resp = ""
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                partes = line.split(";", 1)
                if len(partes) != 2:
                    print(f"Línea inválida en {filename}: {line}")
                    continue
                tipo, cmd = partes[0].strip().upper(), partes[1].strip()
                if args:
                    cmd = reemplazar_con_array(cmd, args)
                if tipo == "W":
                    cm.write(cmd)
                elif tipo == "R":
                    # El comando READ no es estándar en PNA, se omite.
                    print("Comando 'R' no soportado en PNA. Usa comandos de consulta SCPI terminados en '?'.")
                elif tipo == "Q":
                    resp = cm.query(cmd)
                    print(f"Query: {cmd} -> Respuesta: {resp}", end="")
                elif tipo == "C":
                    procesar_script(cm, f'./{SCRIPTS_DIR}/{cmd}')
                elif tipo in ("DEBUG", "D"):
                    print("Entrando en modo terminal interactivo (escribe QUIT para salir)...")
                    while True:
                        user_cmd = input("PNA> ").strip()
                        if user_cmd.upper() == "QUIT":
                            print("Saliendo del modo terminal.")
                            break
                        if user_cmd:
                            resp = cm.query(user_cmd)
                            print(f"Respuesta: {resp}")
                else:
                    print(f"Tipo de comando desconocido en {filename}: {line}")
    except Exception as e:
        print(f"Error al procesar el archivo {filename}: {e}")
    return resp

def list_available_macros(cm):
    """Lista los macros disponibles en el directorio de macros."""
    print("Listando los macros disponibles")
    resp = procesar_script(cm, SCRIPTS_DIR + "/ListFiles.cmd", [RUTA_MACROS])
    print("Archivos en el directorio:")
    macros = resp.replace("\"", "").split(",")
    if not macros or macros == ['']:
        print("No se encontraron macros disponibles.")
    else:
        for idx, macro in enumerate(macros, start=1):
            if macro.strip():
                print(f"{idx}. {macro.strip()}")
    return macros

def list_curr_macros(cm):
    """Lista los macros actualmente cargados en el instrumento."""
    print("Listando los macros cargados")
    for i in range(1, 26):
        args = [i]
        check_macros_file = "CheckMacros.cmd"
        print(f"\nMacro {i} -------------------")
        procesar_script(cm, SCRIPTS_DIR + "/" + check_macros_file, args)

def change_macro(cm):
    """Permite intercambiar/cargar un macro en el instrumento."""
    print("Cambio de macros")
    macro_list = list_available_macros(cm)
    macro_number = input("Número del macro a cargar: ")
    if not macro_number.isdigit() or not (1 <= int(macro_number) <= len(macro_list)):
        print("Número de macro inválido.")
        return
    macro_title = input("Título del macro: ")
    macro_arguments = input("Argumentos del macro (separados por comas): ")
    new_macro_number = input("Número donde cargar el macro (1-25): ")
    if not new_macro_number.isdigit() or not (1 <= int(new_macro_number) <= 25):
        print("Número de macro destino inválido.")
        return
    procesar_script(
        cm,
        SCRIPTS_DIR + "/SetMacro.cmd",
        [new_macro_number, f"{RUTA_MACROS}\\{macro_list[int(macro_number)-1]}", macro_title, macro_arguments]
    )
    print(f"Macro '{macro_list[int(macro_number)-1]}' cargado como macro {new_macro_number} con título '{macro_title}' y argumentos '{macro_arguments}'.")

def exec_macro(cm):
    """Ejecuta un macro cargado en el instrumento."""
    print("Ejecución de macros")
    macro_number = input("Número del macro a ejecutar: ")
    if not macro_number.isdigit() or not (1 <= int(macro_number) <= 25):
        print("Número de macro inválido. Debe ser un número entre 1 y 25.")
        return
    procesar_script(cm, SCRIPTS_DIR + "/ExecMacro.cmd", [macro_number])
    print(f"Macro {macro_number} ejecutado.")

def eliminar_macro(cm):
    """Elimina uno o todos los macros cargados en el instrumento."""
    print("Eliminación de macros")
    macro_number = input("Número del macro a eliminar (1-25) o 0 para eliminar todos: ")
    if not macro_number.isdigit() or not (0 <= int(macro_number) <= 25):
        print("Número de macro inválido. Debe ser un número entre 0 y 25.")
        return
    if macro_number == '0':
        for i in range(1, 26):
            procesar_script(cm, SCRIPTS_DIR + "/SetMacro.cmd", [str(i), "", "", ""])
        print("Todos los macros eliminados.")
    else:
        procesar_script(cm, SCRIPTS_DIR + "/SetMacro.cmd", [macro_number, "", "", ""])
        print(f"Macro {macro_number} eliminado.")

def menu():
    """Muestra el menú principal."""
    clear_screen()
    print(f"Trabajando con: {INSTRUMENT_ID}")
    print("Funcionalidades----------------")
    print(" 1. Listar todos los macros disponibles")
    print(" 2. Listar los 25 macros actualmente cargados")
    print(" 3. Intercambiar macros")
    print(" 4. Ejecutar macros")
    print(" 5. Ejecutar script custom")
    print(" 6. CMD interactivo")
    print(" 7. Eliminar macros")
    print(" 0. SALIR")

def menu_loop(cm):
    """Bucle principal del menú."""
    menu_actions = {
        1: list_available_macros,
        2: list_curr_macros,
        3: change_macro,
        4: exec_macro,
        5: lambda cm: procesar_script(cm, input("Fichero: ")),
        6: lambda cm: procesar_script(cm, SCRIPTS_DIR + "/Debug.cmd"),
        7: eliminar_macro
    }
    while True:
        menu()
        try:
            menu_opt = int(input("\nSelección: "))
        except ValueError:
            print("Introduce un número válido.")
            continue
        if menu_opt == 0:
            clear_screen()
            print("Bye :)")
            break
        action = menu_actions.get(menu_opt)
        if action:
            action(cm)
            continuar()
        else:
            print(f"Valor '{menu_opt}' no reconocido\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta comandos en el PNA N5227B mediante scripts.")
    parser.add_argument("-a", "--address", required=True, help="Dirección IP del instrumento PNA N5227B")
    parser.add_argument("-f", "--files", required=False, nargs="+", help="Lista de archivos de script a ejecutar")
    args = parser.parse_args()

    cm = it.Command_Ethernet(args.address)
    try:
        cm.connect()
    except Exception as e:
        print(f"Error en la conexión. Comprueba que el equipo está encendido. Detalle: {e}")
        exit(1)

    id_file = "ID.cmd"
    INSTRUMENT_ID = procesar_script(cm, SCRIPTS_DIR + "/" + id_file)

    # Ejecuta scripts pasados por línea de comandos antes de entrar al menú
    if args.files:
        for script_file in args.files:
            procesar_script(cm, script_file)

    menu_loop(cm)
