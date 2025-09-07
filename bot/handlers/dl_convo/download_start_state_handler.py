from bot.handlers.constants import STATES
from bot.handlers.constants import DOWNLOAD_OPTIONS
from bot.logger import logger


from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def download_start_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download start handler')

  HANDLER_STATE = 0
  logger.debug(f"HANDLER_STATE: {HANDLER_STATE}")

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download start handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    reply = "Возникла какая-то ошибка с сообщением. Давай начнем сначала"
    await update.message.reply_text(reply)
    logger.warning('No text in message')
    return STATES[HANDLER_STATE]

  logger.info('Sending download options')
  options = 'Напиши цифру того, что ты хочешь скачать:\n'
  for option_number, option in enumerate(DOWNLOAD_OPTIONS.values()):
    options += f'{option_number + 1}. {option}\n'
  await update.message.reply_text(options)

  return STATES[HANDLER_STATE + 1]