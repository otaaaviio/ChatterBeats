import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

# Certifique-se de que o diretório de logs existe
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d, %H:%M.log"))

log_handler = RotatingFileHandler(
    log_filename, maxBytes=5*1024*1024, backupCount=5
)

log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log_handler,
    ]
)