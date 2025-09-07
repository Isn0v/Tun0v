from typing import Optional
from telegram import InputMediaAudio, Update
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

from bot.handlers.dl_convo.constants import STATES
from bot.handlers.dl_convo.constants import DOWNLOAD_OPTIONS
from bot.logger import logger


async def start(update: Update, context: CallbackContext) -> int:
  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for start handler. Quitting the conversation...')
    return ConversationHandler.END
    
  reply = f'''
Привет, {update.effective_user.first_name}. Я бот для скачивания песен с YouTube.
Напиши мне название песни.
  '''
  await update.message.reply_text(reply)

  return STATES[0]


# Just for testing. Never mind
async def test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  if not update.message or not update.effective_user:
    return ConversationHandler.END
  
  test_name = 'google \\- \\[test\\]'
  test_url = 'https://www.google.com/'
  markdown_responce = f"[{test_name}]({test_url})"
  
  await update.message.reply_text(markdown_responce, parse_mode='MarkdownV2')
  
  
  return ConversationHandler.END