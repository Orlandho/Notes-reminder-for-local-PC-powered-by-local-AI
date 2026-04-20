# Asistente de Notas IA (Local con LM Studio)

Un programa de línea de comandos en Python que escanea tus carpetas locales en busca de notas útiles y las analiza automáticamente utilizando Inteligencia Artificial de forma **100% local y privada**.

El sistema fue diseñado pensando tanto en usuarios comunes que buscan organizar sus apuntes, como en empresas que desean analizar su base de conocimiento sin enviar datos confidenciales a la nube.

## 🚀 Características Principales

1. **Privacidad Total**: Utiliza [LM Studio](https://lmstudio.ai/) como servidor local para ejecutar la IA. Tus documentos nunca salen de tu computadora, haciéndolo ideal para información sensible.
2. **Escalable según Hardware**: Funciona con cualquier modelo alojado en LM Studio. Ya sea que tengas una tarjeta gráfica modesta (como una RTX 3050) ejecutando modelos pequeños (Gemma-2B, Phi-3), hasta hardware empresarial con GPUs de 16GB+ corriendo modelos gigantes (Qwen, LLaMa-3 de 70B).
3. **Gestión Automática de Contexto**: Incluye un catálogo con más de 50 modelos modernos. Detecta automáticamente el modelo que estás corriendo y ajusta los límites de tokens para que la IA nunca colapse por exceso de texto.
4. **Discriminador de "Basura"**: Cuenta con un prompt interno optimizado. La IA lee el documento y decide inteligentemente si es una "Nota Útil" o simplemente código basura / logs de sistema, ignorando estos últimos.
5. **Persistencia de Rutas**: Guarda tus carpetas recurrentes en un archivo de configuración, por lo que no necesitas reconfigurar tus rutas de Windows/Mac cada vez que lo inicias.
6. **Reportes Automáticos**: Si encuentra más de 20 notas útiles, automáticamente agrupa los resúmenes de manera ordenada en un archivo `.txt` para no saturar la consola.

---

## 🛠️ Requisitos e Instalación

### Requisitos previos
*   Python 3.8 o superior.
*   [LM Studio](https://lmstudio.ai/) instalado y en ejecución.

### Instalación
1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias requeridas ejecutando:
   ```bash
   pip install openai python-docx tiktoken
   ```

---

## 🖥️ Cómo usar el programa

### Paso 1: Iniciar el Servidor Local en LM Studio
1. Abre **LM Studio**.
2. Descarga y carga un modelo de tu preferencia (ej. Llama-3-8B-Instruct, Phi-3, Mistral).
3. Ve a la pestaña del **Servidor Local (Local Server)** en LM Studio.
4. Asegúrate de que el servidor esté corriendo en el puerto `1234` (esta es la configuración predeterminada). Haz clic en "Start Server".

### Paso 2: Iniciar el Asistente
En la terminal donde descargaste este programa, ejecuta:
```bash
python main.py
```

### Paso 3: Interactuar con el menú
Al abrirse, verás el menú interactivo:

1. **Agregar rutas de carpetas:** Pega la ruta de la carpeta de tu computadora donde guardas tus documentos (ej. `C:\Users\MiNombre\Documentos\Apuntes`).
2. **Quitar rutas de carpetas:** Si ya no quieres escanear una carpeta, puedes quitarla de la lista aquí.
3. **Iniciar análisis:** El programa te preguntará qué carpetas escanear. Leerá archivos `.txt`, `.md` y `.docx`, los filtrará y la IA te dará resúmenes detallados de los que considere notas útiles.
4. **Salir:** Cierra el programa de forma segura.

---

## ⚙️ Detalles Técnicos (Para Desarrolladores)

*   **Modelos Soportados:** El archivo `modelos.json` incluye una base de datos actualizada de límites de tokens de modelos populares (OpenAI, Google, Meta, Qwen, DeepSeek, etc.).
*   **Filtro de Extensiones:** Actualmente procesa rigurosamente `.txt`, `.md` y `.docx` para asegurar compatibilidad universal en la lectura del texto.
*   **Estimador de Tokens:** Utiliza `tiktoken` con fallback a cálculo matemático básico (`palabras * 1.3`) para proteger contra fallos de codificación, asegurando que los envíos a la API no superen la ventana contextual de la IA en uso.
*   **Prompting One-Shot:** La lógica en `analizador_notas.py` instruye a la IA para responder con un simple "RECHAZADO" o un resumen directo, limitando drásticamente el tiempo de inferencia y las alucinaciones en modelos con baja capacidad paramétrica.
*   **Arquitectura Modular:** Diseñado para escalar. Las futuras versiones podrán incorporar fácilmente una base de datos vectorial para implementar la función de *Chat sobre documentos (RAG)*.

---

¡Disfruta organizando tus notas con IA privada!
