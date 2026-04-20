import logging
from pathlib import Path
import docx
import tiktoken

def extraer_texto(ruta_archivo):
    """Extrae el texto de archivos .txt, .md o .docx."""
    path = Path(ruta_archivo)
    ext = path.suffix.lower()

    try:
        if ext in ['.txt', '.md']:
            # Intentar abrir con utf-8, hacer fallback a otros encodings si falla
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(path, 'r', encoding='latin-1') as f:
                    return f.read()

        elif ext == '.docx':
            doc = docx.Document(path)
            texto = [para.text for para in doc.paragraphs]
            return '\n'.join(texto)

        else:
            return None
    except Exception as e:
        logging.error(f"Error al leer el archivo {ruta_archivo}: {e}")
        return None

def contar_tokens(texto):
    """Cuenta el número aproximado de tokens del texto."""
    if not texto:
        return 0
    try:
        # Usa cl100k_base, que es un encoding común para modelos modernos
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(texto))
    except Exception as e:
        logging.error(f"Error al contar tokens: {e}")
        # Estimación cruda como fallback: ~1.3 tokens por palabra
        return int(len(texto.split()) * 1.3)

def escanear_carpeta(ruta_carpeta):
    """Escanea la carpeta y devuelve una lista de rutas de archivos soportados."""
    archivos_soportados = []
    path_carpeta = Path(ruta_carpeta)

    # En Windows real `path_carpeta.is_dir()` es lo correcto.
    # Como este código podría correr desde Linux analizando una ruta de red o montada:
    if not path_carpeta.exists() or not path_carpeta.is_dir():
        logging.warning(f"La ruta {ruta_carpeta} no existe o no es un directorio accesible en este momento.")
        # Ojo: Si el usuario usa Windows y este script corre en Windows, funcionará bien.
        return archivos_soportados

    try:
        # Escaneo no recursivo (solo el directorio raíz especificado)
        for file_path in path_carpeta.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md', '.docx']:
                archivos_soportados.append(str(file_path))
    except Exception as e:
        logging.error(f"Error al escanear carpeta {ruta_carpeta}: {e}")

    return archivos_soportados
