from bot.handlers.dl_convo.constants import OPTION_TO_STATE, DOWNLOAD_OPTION_STATE

from bot.logger import logger


from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler


async def download_option_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download option handler')

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download option handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением. Давай начнем сначала"
    await update.message.reply_text(reply)
    return DOWNLOAD_OPTION_STATE

  user_response = update.message.text
  logger.info(f'User option response is {user_response}')
  if user_response not in OPTION_TO_STATE:
    logger.warning('Invalid user response')
    reply = "Возникла какая-то ошибка с сообщением. Давай начнем сначала"
    await update.message.reply_text(reply)
    return DOWNLOAD_OPTION_STATE

  # TODO: search song by download url
  reply = f'Введи название песни 🌐'
  await update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())

  return OPTION_TO_STATE[user_response]


