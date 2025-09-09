from bot.handlers.dl_convo.constants import DOWNLOAD_OPTIONS, DOWNLOAD_START_STATE, DOWNLOAD_OPTION_STATE, FALLBACK_DOWNLOAD_CONVERSATION_COMMAND

from bot.logger import logger


from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


async def download_start_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download start handler')

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download start handler. Quitting the conversation...')
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
    return DOWNLOAD_START_STATE

  logger.info('Sending download options')
  options = 'Выбери, что ты хочешь скачать:\n'
  
  buttons = []
  for option_number, option in enumerate(DOWNLOAD_OPTIONS):
    options += f'{option_number + 1}. {option}\n'
    buttons.append(option)
    
  buttons = [buttons, [f'/{FALLBACK_DOWNLOAD_CONVERSATION_COMMAND}']]
  markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
  await update.message.reply_text(options, reply_markup=markup)

  return DOWNLOAD_OPTION_STATE


