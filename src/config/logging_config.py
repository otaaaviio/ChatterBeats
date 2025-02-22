import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, "otabot.log")

log_handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=5)

log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log_handler,
    ],
)
