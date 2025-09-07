from bot.handlers.constants import STATES
from bot.handlers.constants import DOWNLOAD_OPTIONS
from bot.logger import logger


from telegram import Update
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
    return STATES[1]

  user_response = update.message.text.lower()
  logger.info(f'User response is {user_response}')
  chosen_number = -1
  try:
    chosen_number = int(user_response)
    if chosen_number < 1 or chosen_number > len(DOWNLOAD_OPTIONS):
      raise ValueError(f'Chosen number {chosen_number} is out of range or incorrect')
  except ValueError as e:
    logger.warning(f'Error parsing user response {user_response}: {e}')
    await update.message.reply_text("Введен некорректный вариант. Давай еще раз")
    return STATES[HANDLER_STATE]

  assert chosen_number != -1, "Chosen number is not set"
  logger.info(f'Chosen state number is {chosen_number}')

  reply = f'Теперь тебе нужно ввести название для поиска'
  await update.message.reply_text(reply)

  return STATES[2*chosen_number]