import os
from bot.logger import logger
from ytmusicapi import YTMusic

ytmusic = YTMusic()

# Directories
AUDIO_PATH = os.environ.get('AUDIO_PATH', './downloads/audio')
logger.debug(f"AUDIO_PATH: {AUDIO_PATH}")
METADATA_PATH = os.environ.get('METADATA_PATH', './downloads/metadata')
logger.debug(f"METADATA_PATH: {METADATA_PATH}")

# File names
AUDIO_NAME = os.environ.get('AUDIO_NAME', 'audio')
logger.debug(f"AUDIO_NAME: {AUDIO_NAME}")
METADATA_NAME = os.environ.get('METADATA_NAME', 'media')
logger.debug(f"METADATA_NAME: {METADATA_NAME}")

# File extensions
AUDIO_EXT = os.environ.get('AUDIO_EXT', 'm4a')
logger.debug(f"AUDIO_EXT: {AUDIO_EXT}")
METADATA_EXT = os.environ.get('METADATA_EXT', 'info.json')
logger.debug(f"METADATA_EXT: {METADATA_EXT}")

# Telegram bot token
telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
if not telegram_bot_token:
  logger.error('TELEGRAM_BOT_TOKEN is not set')
  raise Exception('TELEGRAM_BOT_TOKEN is not set')
logger.debug(f"TELEGRAM_BOT_TOKEN: {telegram_bot_token}")

# Scripts
PYTHON_INTERPRETER = 'python'
CLEANUP_SCRIPT_PATH = os.path.abspath('./bot/scripts/cleanup.py')
logger.debug(f"CLEANUP_SCRIPT_PATH: {CLEANUP_SCRIPT_PATH}")
DOWNLOADER_SCRIPT_PATH = os.path.abspath('./bot/scripts/downloader.py')
logger.debug(f"DOWNLOADER_SCRIPT_PATH: {DOWNLOADER_SCRIPT_PATH}")

# Other
logger.debug(f"Current working directory is {os.getcwd()}")

BOT_REQUEST_READ_TIMEOUT_DEFAULT = 10
BOT_REQUEST_READ_TIMEOUT = os.environ.get('BOT_REQUEST_READ_TIMEOUT', BOT_REQUEST_READ_TIMEOUT_DEFAULT)
try:
  BOT_REQUEST_READ_TIMEOUT = int(BOT_REQUEST_READ_TIMEOUT)
except ValueError:
  logger.error(f'BOT_REQUEST_TIMEOUT is not an integer. Setting it to default value of {BOT_REQUEST_READ_TIMEOUT_DEFAULT}')
logger.debug(f"BOT_REQUEST_READ_TIMEOUT: {BOT_REQUEST_READ_TIMEOUT}")

