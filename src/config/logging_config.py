import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

__LOG_LEVEL = {
    "development": logging.DEBUG,
    "production": logging.INFO,
}

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, "cb.log")

log_handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=5)

log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logging.basicConfig(
    level=__LOG_LEVEL[ENVIRONMENT],
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log_handler,
    ],
)
