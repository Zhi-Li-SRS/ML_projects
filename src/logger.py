import logging
import os
from datetime import datetime

log_file = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_path = os.path.join(os.getcwd(), "logs", log_file)
os.makedirs(log_path, exist_ok=True)
log_file_path = os.path.join(log_path, log_file)
logging.basicConfig(
    filename=log_file_path,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
