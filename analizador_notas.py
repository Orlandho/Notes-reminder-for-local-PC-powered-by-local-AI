import logging

# Límite interno de tokens de respuesta y promt adicional
TOKENS_RESERVA_PROMPT = 500
MAX_NOTAS = 40

def generar_prompt_analisis(texto):
    """Genera el prompt consolidado para evaluar si es nota y obtener el resumen."""
    return f"""Eres un asistente de análisis de notas. Te voy a pasar un texto.
Debes determinar si este texto es una nota útil (como apuntes, información relevante, recordatorios, ideas) o si no lo es (como logs de sistema, código suelto sin contexto, texto basura).

REGLA ESTRICTA:
1. Si el texto NO es una nota útil, debes responder ÚNICAMENTE con la palabra: RECHAZADO
2. Si el texto SÍ es una nota útil, debes responder ÚNICAMENTE con la palabra "Resumen:" seguida de un breve resumen conciso de los puntos principales. No agregues saludos ni texto adicional.

Texto a analizar:
\"\"\"{texto}\"\"\"
"""

def procesar_archivo_con_ia(client, modelo_id, limite_tokens, ruta_archivo, texto, tokens_texto):
    """Envía el texto a la IA para su análisis si no supera el límite de contexto."""

    if tokens_texto + TOKENS_RESERVA_PROMPT > limite_tokens:
        logging.warning(f"Omitido: {ruta_archivo} (Supera la ventana de contexto. Tokens: {tokens_texto}, Límite: {limite_tokens})")
        return False, None

    prompt = generar_prompt_analisis(texto)

    try:
        response = client.chat.completions.create(
            model=modelo_id,
            messages=[
                {"role": "system", "content": "Eres un asistente estricto y conciso."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Baja temperatura para respuestas más deterministas
            max_tokens=300    # Limitar el tamaño del resumen
        )

        respuesta_ia = response.choices[0].message.content.strip()

        if respuesta_ia.upper() == "RECHAZADO" or respuesta_ia.upper().startswith("RECHAZADO"):
            return False, None

        # Si no fue rechazado, asumimos que es el resumen
        # Limpiar prefijo "Resumen:" si la IA lo incluyó
        if respuesta_ia.lower().startswith("resumen:"):
            respuesta_ia = respuesta_ia[8:].strip()

        return True, respuesta_ia

    except Exception as e:
        logging.error(f"Error al procesar con IA el archivo {ruta_archivo}: {e}")
        return False, None
