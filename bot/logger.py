import logging, logging.handlers
import os
import sys

log_levels = {
  'DEBUG': logging.DEBUG,
  'INFO': logging.INFO,
  'WARNING': logging.WARNING
}

LOG_PATH = './logs'

log_level = log_levels[os.getenv('LOG_LEVEL', 'INFO')]

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)

file_handler = logging.handlers.RotatingFileHandler(
  f"{LOG_PATH}/bot.log",
  maxBytes=1024 * 1024 * 2,
  backupCount=2,
  encoding='utf-8'
)


formatter = logging.Formatter(
  "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug(
  f"Logging level: {log_level} ({os.getenv('LOG_LEVEL', 'INFO')})"
)