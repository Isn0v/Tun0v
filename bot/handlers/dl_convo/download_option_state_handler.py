from bot.handlers.constants import STATES
from bot.handlers.constants import DOWNLOAD_OPTIONS
from bot.logger import logger


from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler


async def download_option_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download option handler')

  HANDLER_STATE = 1
  logger.debug(f"HANDLER_STATE: {HANDLER_STATE}")

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download option handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением. Давай начнем сначала"
    await update.message.reply_text(reply)
    return STATES[HANDLER_STATE]

  user_response = update.message.text
  logger.info(f'User option response is {user_response}')

  # TODO: search song by download url
  reply = f'Введи название песни 🌐'
  await update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())

  option_number = DOWNLOAD_OPTIONS.index(user_response) + 1
  state_number = 2*option_number
  logger.info(f'User option number is {option_number}. Setting state to {state_number}')
  return STATES[state_number]