import os

AUDIO_PATH = './downloads/audio'
AUDIO_NAME = 'audio'
AUDIO_EXT = 'm4a'

METADATA_PATH = './downloads/metadata'
METADATA_NAME = 'media'
METADATA_JSON_EXT = "info.json"


telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if telegram_bot_token == '':
  raise Exception('TELEGRAM_BOT_TOKEN is not set')

