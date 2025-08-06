# Analizador PNA N5227B

Este programa permite controlar y automatizar el analizador de redes Keysight PNA N5227B a través de una conexión Ethernet, enviando comandos SCPI mediante scripts de texto. Está pensado para facilitar la gestión de macros Visual Basic ejecutables en el analizador, la ejecución de comandos personalizados y la interacción remota con el instrumento.

## Funcionalidades principales

- **Conexión remota TCP/IP** al instrumento PNA N5227B usando su dirección IP.
- **Ejecución de scripts**: Permite ejecutar archivos de texto que contienen listas de comandos SCPI.
- **Gestión de macros**: Listado, carga, ejecución y eliminación de macros en el instrumento.
- **Menú interactivo**: Acceso a todas las funciones desde un menú en terminal.
- **Modo terminal SCPI**: Permite enviar comandos SCPI manualmente y ver la respuesta en tiempo real.
- **Procesamiento flexible de comandos**: Los scripts admiten varios tipos de comandos y argumentos.

## Formato de los scripts personalizados

Además de gestionar los macros en Visual Basic se pueden crear ficheros de comandos personalizados directamente. **Recomendados únicamente** para gestiones rápidas y pruebas.

Cada línea válida debe tener el formato `[tipo];[comando]`, donde:

- `# ...` → Comentario, la línea se ignora.
- `C;archivo` → Ejecuta otro script como si fuera una llamada a función.
- `W;comando` → Envía el comando SCPI usando `write` (sin esperar respuesta).
- `Q;comando` → Envía el comando SCPI y muestra la respuesta (`query`).
- `DEBUG;` → Inicia el modo terminal interactivo SCPI.
- **Nota:** El tipo `R;` no está soportado en el PNA, ya que no existe el comando SCPI `READ`.

## Ejemplo de archivo de script personalizado

```cnf
# Este es un comentario
W;SYST:PRESET
Q;*IDN?
C;otro_script.txt
DEBUG;
```

## Uso

Puedes ejecutar scripts directamente o acceder al menú interactivo:

```bash
python3 pna_exe.py -a <IP_DEL_PNA> [-f script1.txt script2.txt ...]
```

- El parámetro `-a` indica la dirección IP del instrumento.
- El parámetro `-f` permite ejecutar uno o varios scripts antes de entrar al menú.

Una vez conectado, el menú permite:

1. Listar todos los macros disponibles en el directorio de macros.
2. Listar los 25 macros actualmente cargados en el instrumento.
3. Intercambiar/cargar macros en el instrumento.
4. Ejecutar macros cargados.
5. Ejecutar scripts personalizados.
6. Entrar en modo terminal SCPI interactivo.
7. Eliminar macros cargados.
0. Salir.

## Requisitos

- Python 3
- Módulo `instrument_ethernet.py` en el mismo directorio
- Conexión de red al instrumento PNA N5227B

## Notas

Este software se encuentra en fase de desarrollo.

## Autor

Pablo H.

