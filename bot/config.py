import os
from logger import logger
from ytmusicapi import YTMusic

ytmusic = YTMusic()

AUDIO_PATH = './downloads/audio'
AUDIO_NAME = 'audio'
AUDIO_EXT = 'm4a'

METADATA_PATH = './downloads/metadata'
METADATA_NAME = 'media'
METADATA_EXT = 'info.json'


telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
logger.debug(f"TELEGRAM_BOT_TOKEN: {telegram_bot_token}")
if telegram_bot_token == '':
  logger.error('TELEGRAM_BOT_TOKEN is not set')
  raise Exception('TELEGRAM_BOT_TOKEN is not set')



