import logging
import json
import time
import sys

logger = logging.getLogger("StructuredLogger")
handler = logging.StreamHandler(sys.stdout)  # Tienen que ir a stdout!!!
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_structured(level, message):
    """
    Genera un log estructurado con nivel, timestamp y mensaje.
    """
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "message": message
    }
    log_entry_json = json.dumps(log_entry)
    if level == "INFO":
        logger.info(log_entry_json)
    elif level == "WARN":
        logger.warning(log_entry_json)
    elif level == "ERROR":
        logger.error(log_entry_json)
    sys.stdout.flush() 

if __name__ == "__main__":
    log_structured("INFO", "Mensaje informativo.")
    time.sleep(1)
    log_structured("WARN", "Mensaje de advertencia.")
    time.sleep(1)
    log_structured("ERROR", "Mensaje de error.")

