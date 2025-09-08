from bot import browser, extractor
from bot.handlers.constants import STATES
from bot.logger import logger


from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


async def retrieve_metadata_song_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the retrieve metadata song handler')

  HANDLER_STATE = 2
  logger.debug(f"HANDLER_STATE: {HANDLER_STATE}")

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download song handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением. Напиши еще раз, какую песню ты хочешь скачать"
    await update.message.reply_text(reply)
    return STATES[HANDLER_STATE]

  query = update.message.text
  logger.info(f"Searching for song with query: {query}")

  # TODO: let the user choose between tracks found by query
  song_metadata = browser.search_song_metadata(query)
  if not song_metadata:
    logger.warning(f"Song with query {query} not found")
    await update.message.reply_text("Песня не нашлась 😥.\n \
                                    Давай попробуем еще раз, но с другим запросом")
    return STATES[HANDLER_STATE]

  assert context.chat_data is not None, "User data is not initialized"
  logger.debug("Storing metadata into user context")
  context.chat_data['song_metadata'] = song_metadata

  logger.debug(f"Found song with name: {extractor.get_song_title(song_metadata)}")
  reply = "Найдена следующая песня:\n"
  await update.message.reply_text(reply)

  logger.debug(f"Extracting song metadata")
  reply = extractor.extract_song(song_metadata)
  await update.message.reply_text(reply, parse_mode='MarkdownV2')
  
  markup = ReplyKeyboardMarkup(
    [['Да', 'Нет']],
    resize_keyboard=True,
    one_time_keyboard=True
  )

  reply = 'Скачиваем? 🤔'
  await update.message.reply_text(reply, reply_markup=markup)

  return STATES[HANDLER_STATE + 1]