import sys
import os
import logging

import gestor_rutas
import lector_archivos
import conexion_ia
import analizador_notas
import generador_resultados

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configurar logging para guardar solo WARNING y ERROR en logs/app_logs.txt
logging.basicConfig(
    filename=os.path.join("logs", "app_logs.txt"),
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Desactivar logs de requests/httpx para no ensuciar el archivo de log innecesariamente
logging.getLogger("httpx").setLevel(logging.WARNING)

def menu_agregar_ruta():
    rutas_actuales = gestor_rutas.cargar_rutas()
    nueva = input("Ingresa la ruta absoluta de la carpeta a agregar: ").strip()
    gestor_rutas.agregar_ruta(nueva, rutas_actuales)

def menu_quitar_ruta():
    rutas_actuales = gestor_rutas.cargar_rutas()
    if not rutas_actuales:
        print("No hay rutas para quitar.")
        return

    print("\nRutas configuradas:")
    for i, r in enumerate(rutas_actuales, 1):
        print(f"{i}. {r}")

    seleccion = input("Ingresa el número de la ruta a quitar (o presiona Enter para cancelar): ").strip()
    if not seleccion.isdigit():
        return

    idx = int(seleccion) - 1
    if 0 <= idx < len(rutas_actuales):
        gestor_rutas.quitar_ruta(rutas_actuales[idx], rutas_actuales)
    else:
        print("Opción inválida.")

def iniciar_analisis():
    # 1. Validar rutas
    rutas_validas, rutas_configuradas = gestor_rutas.verificar_configuracion_lista()
    if not rutas_validas:
        return

    # Preguntar qué carpeta analizar
    carpetas_a_analizar = []
    if len(rutas_configuradas) > 1:
        print("\nTienes múltiples carpetas configuradas:")
        print("0. Analizar todas")
        for i, r in enumerate(rutas_configuradas, 1):
            print(f"{i}. {r}")

        seleccion = input("Selecciona una opción: ").strip()
        if seleccion == "0":
            carpetas_a_analizar = rutas_configuradas
        elif seleccion.isdigit() and 1 <= int(seleccion) <= len(rutas_configuradas):
            carpetas_a_analizar = [rutas_configuradas[int(seleccion) - 1]]
        else:
            print("Selección inválida. Cancelando análisis.")
            return
    else:
        carpetas_a_analizar = rutas_configuradas

    print("\n[1/4] Conectando con LM Studio y obteniendo modelo activo...")
    modelo_id, limite_tokens, client = conexion_ia.obtener_modelo_activo_y_limite()

    if client is None:
        return

    print(f"[2/4] Escaneando carpetas seleccionadas...")
    todos_los_archivos = []
    for carpeta in carpetas_a_analizar:
        archivos = lector_archivos.escanear_carpeta(carpeta)
        todos_los_archivos.extend(archivos)

    if not todos_los_archivos:
        print("No se encontraron archivos .txt, .md o .docx en las rutas especificadas.")
        return

    if len(todos_los_archivos) > analizador_notas.MAX_NOTAS:
        print(f"\n[ADVERTENCIA] Se encontraron {len(todos_los_archivos)} archivos. Para evitar saturación, solo se evaluarán los primeros {analizador_notas.MAX_NOTAS}.")
        todos_los_archivos = todos_los_archivos[:analizador_notas.MAX_NOTAS]
    else:
        print(f"Se encontraron {len(todos_los_archivos)} archivos. Iniciando filtrado y lectura...")

    notas_procesadas = []

    print(f"[3/4] Analizando contenido con IA (Modelo: {modelo_id}) ...")
    print(f"[!] Puedes presionar CTRL+C en cualquier momento para cancelar el análisis y volver al menú.")

    try:
        for idx, archivo in enumerate(todos_los_archivos, 1):
            if len(notas_procesadas) >= analizador_notas.MAX_NOTAS:
                print(f"\n[INFO] Se ha alcanzado el límite máximo de {analizador_notas.MAX_NOTAS} notas procesadas. Deteniendo escaneo.")
                break

            print(f"   -> Evaluando archivo {idx}/{len(todos_los_archivos)}: {archivo}")
            texto = lector_archivos.extraer_texto(archivo)

            if not texto or not texto.strip():
                continue

            tokens_texto = lector_archivos.contar_tokens(texto)

            es_nota, resumen = analizador_notas.procesar_archivo_con_ia(
                client, modelo_id, limite_tokens, archivo, texto, tokens_texto
            )

            if es_nota and resumen:
                notas_procesadas.append({
                    "ruta": archivo,
                    "resumen": resumen
                })
    except KeyboardInterrupt:
        print("\n\n[!] Análisis interrumpido por el usuario (CTRL+C).")
        if not notas_procesadas:
            print("No se procesaron notas antes de la interrupción.")
            return

    print(f"\n[4/4] Finalizando y generando resultados...")
    generador_resultados.presentar_resultados(notas_procesadas)

def mostrar_menu():
    while True:
        print("\n" + "="*40)
        print("    ASISTENTE DE NOTAS IA (LM STUDIO)    ")
        print("="*40)
        print("1. Agregar rutas de carpetas.")
        print("2. Quitar rutas de carpetas.")
        print("3. Iniciar análisis e interacción con la IA.")
        print("4. Salir.")
        print("="*40)

        opcion = input("Selecciona una opción (1-4): ").strip()

        if opcion == '1':
            menu_agregar_ruta()
        elif opcion == '2':
            menu_quitar_ruta()
        elif opcion == '3':
            iniciar_analisis()
        elif opcion == '4':
            print("Saliendo del programa. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    mostrar_menu()
