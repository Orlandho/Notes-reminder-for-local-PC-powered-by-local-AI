import json
from pathlib import Path
import logging
from colorama import Fore, Style

CONFIG_FILE = "config_rutas.json"

def cargar_rutas():
    """Carga las rutas guardadas desde config_rutas.json."""
    if not Path(CONFIG_FILE).exists():
        return []
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("rutas", [])
    except Exception as e:
        logging.error(f"Error al cargar rutas: {e}")
        return []

def guardar_rutas(rutas):
    """Guarda las rutas proporcionadas en config_rutas.json."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"rutas": rutas}, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error al guardar rutas: {e}")

def agregar_ruta(nueva_ruta, rutas_actuales):
    """Agrega una nueva ruta a la lista si es válida y no existe ya."""
    path = Path(nueva_ruta)
    # Even if it's a Windows path entered on Linux/Mac, Pathlib will store it as string.
    # On actual Windows, path.is_dir() will work. Here we just validate it's not empty.
    if str(path).strip() == "":
        print(Fore.RED + "La ruta no puede estar vacía.")
        return rutas_actuales

    ruta_str = str(path)
    if ruta_str not in rutas_actuales:
        rutas_actuales.append(ruta_str)
        guardar_rutas(rutas_actuales)
        print(Fore.GREEN + f"Ruta agregada: {ruta_str}")
    else:
        print(Fore.YELLOW + "La ruta ya se encuentra configurada.")
    return rutas_actuales

def quitar_ruta(ruta_a_quitar, rutas_actuales):
    """Quita una ruta existente de la lista."""
    if ruta_a_quitar in rutas_actuales:
        rutas_actuales.remove(ruta_a_quitar)
        guardar_rutas(rutas_actuales)
        print(Fore.GREEN + f"Ruta eliminada: {ruta_a_quitar}")
    else:
        print(Fore.RED + "La ruta no se encontró en la configuración.")
    return rutas_actuales

def verificar_configuracion_lista():
    """Verifica si hay rutas configuradas, de lo contrario devuelve False."""
    rutas = cargar_rutas()
    if not rutas:
        print(Fore.YELLOW + "\n[!] ADVERTENCIA: No hay rutas configuradas.")
        print(Fore.YELLOW + "    Por favor, agrega al menos una ruta antes de iniciar el análisis.\n")
        return False, rutas
    return True, rutas
