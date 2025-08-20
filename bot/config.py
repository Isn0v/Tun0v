import os

telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if telegram_bot_token == '':
  raise Exception('TELEGRAM_BOT_TOKEN is not set')

