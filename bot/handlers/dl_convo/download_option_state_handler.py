from bot.handlers.dl_convo.constants import OPTION_TO_STATE, DOWNLOAD_OPTION_STATE, FALLBACK_DOWNLOAD_CONVERSATION_COMMAND, DOWNLOAD_OPTIONS

from bot.logger import logger


from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler


async def download_option_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download option handler')

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download option handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением. Давай начнем сначала"
    buttons = [['Давай!']]
    markup = ReplyKeyboardMarkup(
      buttons,
      resize_keyboard=True,
      one_time_keyboard=True
    )
    await update.message.reply_text(reply, reply_markup=markup)
    return DOWNLOAD_OPTION_STATE

  user_response = update.message.text
  
  logger.info(f'User option response is {user_response}')
  if user_response not in OPTION_TO_STATE:
    logger.warning('Invalid user response')
    reply = "Некорректная опция. Давай еще раз"
    buttons = [DOWNLOAD_OPTIONS, [f'/{FALLBACK_DOWNLOAD_CONVERSATION_COMMAND}']]
    markup = ReplyKeyboardMarkup(
      buttons,
      resize_keyboard=True,
      one_time_keyboard=True
    )
    await update.message.reply_text(reply, reply_markup=markup)
    return DOWNLOAD_OPTION_STATE

  # TODO: search song by download url
  reply = f'Введи название песни 🌐'
  await update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())

  return OPTION_TO_STATE[user_response]


