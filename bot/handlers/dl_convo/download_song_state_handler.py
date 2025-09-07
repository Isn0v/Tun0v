from bot import config, extractor, subproc
from bot.handlers.constants import STATES
from bot.logger import logger


from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def download_song_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download song handler')

  HANDLER_STATE = 3
  logger.debug(f"HANDLER_STATE: {HANDLER_STATE}")

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download song handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением. Напиши еще раз, какую песню ты хочешь скачать"
    await update.message.reply_text(reply)
    return STATES[HANDLER_STATE]

  answer = update.message.text.lower()
  if answer != 'да':
    logger.info("Skipping song download")
    await update.message.reply_text("Скачивание пропущено!")
    return ConversationHandler.END

  assert context.chat_data is not None, "User data conetxt not initialized"
  assert 'song_metadata' in context.chat_data, "Song metadata not found"

  song_metadata = context.chat_data['song_metadata']
  logger.debug(f"Song metadata retrieved from user context")

  logger.info("Starting song download")

  logger.info("Cleaning up")
  await subproc.invoke_async_subprocess(
    config.PYTHON_INTERPRETER,
    config.CLEANUP_SCRIPT_PATH
  )


  song_video_id = extractor.get_song_video_id(song_metadata)
  logger.info(f"Downloading song with id {song_video_id}")
  reply = "Начинаю скачивание!"
  await update.message.reply_text(reply)

  song_url = extractor.format_song_url(song_video_id)
  logger.debug(f"Song url: {song_url}")
  download_command = f"{config.DOWNLOADER_SCRIPT_PATH} -s {song_url}"
  logger.debug(f"Invoking subprocess with command: {download_command}")
  await subproc.invoke_async_subprocess(
    config.PYTHON_INTERPRETER,
    download_command
  )
  logger.info(f"Song with id {song_video_id} downloaded")
  await update.message.reply_audio(f'{config.AUDIO_PATH}/{song_video_id}.{config.AUDIO_EXT}',
                                  title=extractor.get_song_title(song_metadata),
                                  performer=extractor.get_song_performers(song_metadata),
                                  duration=extractor.get_song_duration(song_metadata),
                                  thumbnail=extractor.get_song_thumbnail_url(song_metadata)
                                  )
  logger.info(f"Song with id {song_video_id} sent")

  await update.message.reply_text("Скачивание завершено!")
  return ConversationHandler.END