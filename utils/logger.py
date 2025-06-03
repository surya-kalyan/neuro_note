import logging
import os
from logging.handlers import RotatingFileHandler

# Determine log level from environment variable or default to INFO
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# Create a custom logger
logger = logging.getLogger("neuronote_app")
logger.setLevel(LOG_LEVEL)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# File handler (optional, could be enabled by config or another env var)
# For now, let's set it up but make it easy to disable/enable
ENABLE_FILE_LOGGING = os.environ.get("ENABLE_FILE_LOGGING", "false").lower() == "true"
LOG_FILE_PATH = "app.log"

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)

if ENABLE_FILE_LOGGING:
    # Rotate logs, 1MB per file, keep 5 backup files
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"File logging enabled. Logging to {LOG_FILE_PATH}")
else:
    logger.info("File logging is disabled. Logging to console only.")

# Example usage:
# from utils.logger import logger
# logger.info("This is an info message.")
# logger.error("This is an error message.")
