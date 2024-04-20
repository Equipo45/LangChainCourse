import os
import logging


def config():
    os.environ["OPENAI_API_KEY"] = "<SECRET>"
    
def setup_console_logger():
    # Configuración del logger
    logger = logging.getLogger("console_logger")
    logger.setLevel(logging.INFO)

    # Crear un manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Definir el formato de los mensajes
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Añadir el manejador de consola al logger
    logger.addHandler(console_handler)

    return logger