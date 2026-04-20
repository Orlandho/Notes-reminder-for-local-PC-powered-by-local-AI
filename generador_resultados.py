import os

def presentar_resultados(notas_procesadas):
    """
    Recibe una lista de diccionarios con formato:
    [{'ruta': ruta_archivo, 'resumen': texto_resumen}, ...]

    Si <= 20: Imprime en consola.
    Si > 20 (y hasta 40): Guarda en archivo resumenes_notas.txt.
    """
    cantidad = len(notas_procesadas)

    if cantidad == 0:
        print("\n[INFO] No se encontraron notas válidas para procesar.\n")
        return

    print(f"\n[INFO] Se han procesado {cantidad} notas exitosamente.")

    if cantidad <= 20:
        print("\n--- RESÚMENES DE NOTAS ---")
        for idx, nota in enumerate(notas_procesadas, 1):
            print(f"\n[{idx}] Archivo: {nota['ruta']}")
            print(f"Resumen: {nota['resumen']}")
            print("-" * 30)
    else:
        archivo_salida = "resumenes_notas.txt"
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("--- RESÚMENES DE NOTAS ---\n")
                f.write(f"Total de notas procesadas: {cantidad}\n\n")

                for idx, nota in enumerate(notas_procesadas, 1):
                    f.write(f"[{idx}] Archivo: {nota['ruta']}\n")
                    f.write(f"Resumen: {nota['resumen']}\n")
                    f.write("-" * 40 + "\n")

            print(f"\n[ÉXITO] Al ser más de 20 notas, los resúmenes se han guardado en el archivo: {os.path.abspath(archivo_salida)}\n")
        except Exception as e:
            print(f"\n[ERROR] No se pudo guardar el archivo de resultados: {e}")
            # Fallback en caso de error: imprimir de todos modos
            for idx, nota in enumerate(notas_procesadas, 1):
                print(f"[{idx}] {nota['ruta']}: {nota['resumen']}")
