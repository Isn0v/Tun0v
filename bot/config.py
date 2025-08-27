import os
from ytmusicapi import YTMusic

ytmusic = YTMusic()

AUDIO_PATH = './downloads/audio'
AUDIO_NAME = 'audio'
AUDIO_EXT = 'm4a'

METADATA_PATH = './downloads/metadata'
METADATA_NAME = 'media'
METADATA_EXT = 'info.json'


telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if telegram_bot_token == '':
  raise Exception('TELEGRAM_BOT_TOKEN is not set')


SONG_URL_TEMPLATE = 'https://music.youtube.com/watch?v={}'

