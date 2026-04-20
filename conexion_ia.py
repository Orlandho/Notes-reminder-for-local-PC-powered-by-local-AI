import json
import logging
from openai import OpenAI

# Definimos el límite por defecto si el modelo no está en la lista o falla
LIMITE_SEGURIDAD_DEFAULT = 4000

def obtener_catalogo_modelos():
    """Carga el catálogo de modelos desde modelos.json."""
    try:
        with open("modelos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error al cargar modelos.json: {e}")
        return {}

def obtener_modelo_activo_y_limite():
    """Se conecta a LM Studio (localhost), obtiene el modelo activo y su límite de tokens."""
    try:
        # Configurar cliente para LM Studio
        client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lm-studio" # Clave dummy requerida por el SDK
        )

        # Obtener la lista de modelos
        response = client.models.list()

        if not response.data:
            logging.error("No se detectó ningún modelo cargado en LM Studio.")
            return None, LIMITE_SEGURIDAD_DEFAULT, client

        # Tomar el primer modelo cargado
        modelo_id = response.data[0].id
        print(f"Modelo detectado: {modelo_id}")

        # Buscar en el catálogo
        catalogo = obtener_catalogo_modelos()

        # Intentar buscar coincidencia exacta o parcial (ej. si devuelve 'mixtral-8x7b-instruct', y tenemos 'mixtral-8x7b')
        limite_tokens = LIMITE_SEGURIDAD_DEFAULT
        modelo_encontrado = False

        for modelo_key, limite in catalogo.items():
            if modelo_key.lower() in modelo_id.lower() or modelo_id.lower() in modelo_key.lower():
                limite_tokens = limite
                modelo_encontrado = True
                print(f"Modelo encontrado en catálogo. Límite: {limite_tokens} tokens.")
                break

        if not modelo_encontrado:
            print(f"Modelo no encontrado en el catálogo. Usando límite de seguridad: {LIMITE_SEGURIDAD_DEFAULT} tokens.")

        return modelo_id, limite_tokens, client

    except Exception as e:
        logging.error(f"Error al conectar con LM Studio: {e}. Asegúrate de que LM Studio esté corriendo y el servidor local iniciado en el puerto 1234.")
        return None, LIMITE_SEGURIDAD_DEFAULT, None
