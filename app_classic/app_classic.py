import logging
import time

logger = logging.getLogger("ClassicLogger")
handler = logging.FileHandler("/shared_logs/app_classic.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    while True:
        logger.info("Mensaje informativo.")
        time.sleep(1)
        logger.warning("Mensaje de advertencia.")
        time.sleep(1)
        logger.error("Mensaje de error.")
        time.sleep(5)
