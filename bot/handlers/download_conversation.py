from bot import browser, config, extractor, subproc
from bot.logger import logger


from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

def prepare_conversation_handler() -> ConversationHandler:
  """
  Prepares the conversation handler for the download conversation.

  The conversation handler consists of the following states:

  1. DOWNLOAD_START: The entry point of the conversation.
  2. DOWNLOAD_OPTIONS: The state where the user is asked to select
                            what to download (song or playlist).
  3. RETRIEVE_METADATA: The state where the metadata of the
                            selected option is retrieved. 
                            Method is named as retrieve_metadata_<option_name>_state_handler
  4. DOWNLOAD: The state where the selected option is downloaded. 
                            Method is named as download_<option_name>_state_handler
  # TODO: state for choosing between search results
  5. END (reserved number): The state where the conversation ends.

  Returns:
    ConversationHandler: The prepared conversation handler.
  """

  # TODO: playlist option
  return ConversationHandler(
    entry_points=[CommandHandler('start', download_start_state_handler)],
    states={
      STATES[0]: [MessageHandler(filters.TEXT, download_start_state_handler)],
      STATES[1]: [MessageHandler(filters.TEXT, download_option_state_handler)],
      STATES[2]: [MessageHandler(filters.TEXT, retrieve_metadata_song_state_handler)],
      STATES[3]: [MessageHandler(filters.TEXT, download_song_state_handler)],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)],
  )


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

# region song option
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
    await update.message.reply_text("Песня не нашлась 😥.\nДавай попробуем еще раз, но с другим запросом")
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
  
  reply = 'Скачиваем? Да/Нет'
  await update.message.reply_text(reply)

  return STATES[HANDLER_STATE + 1]

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
  
# endregion

async def download_playlist_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download playlist handler')

  HANDLER_STATE = 3
  logger.debug(f"HANDLER_STATE: {HANDLER_STATE}")

  logger.info("Cleaning up")
  await subproc.invoke_async_subprocess(
    config.PYTHON_INTERPRETER,
    config.CLEANUP_SCRIPT_PATH
  )

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download playlist handler. Quitting the conversation...')
    return ConversationHandler.END

  if not update.message.text:
    logger.warning('No text in message')
    reply = "Возникла какая-то ошибка с сообщением.\n Напиши еще раз, какой плэйлист ты хочешь скачать"
    await update.message.reply_text(reply)
    return STATES[HANDLER_STATE]

  query = update.message.text
  logger.info(f"Searching for playlist with query: {query}")

  playlist_metadata = browser.search_playlist_metadata(query)
  if not playlist_metadata:
    logger.warning(f"Playlist with query {query} not found")
    await update.message.reply_text("Плейлист не нашелся 😥.\nДавай попробуем еще раз, но с другим запросом")
    return STATES[HANDLER_STATE]

  logger.debug(f"Found playlist with name: {extractor.get_playlist_title(playlist_metadata)}")
  reply = "Найден следующий плейлист:\n"
  await update.message.reply_text(reply)

  logger.debug(f"Extracting playlist metadata")
  reply = extractor.extract_playlist(playlist_metadata)
  await update.message.reply_text(reply, parse_mode='MarkdownV2')

  return ConversationHandler.END

  # TODO: deal with errors from async subprocess and handle them gracefully (maybe don't download tracks as playlist, but as single ones?)
  logger.info("Retrieving playlist track ids")
  video_ids = extractor.get_playlist_track_video_ids(playlist_metadata)

  # TODO: let the user choose what tracks to download from the playlist
  # TODO: unlimit the number of tracks
  logger.warning(f"For now playlist is limited to first {PLAYLIST_LIMIT} tracks. The rest will be skipped")
  video_ids = video_ids[:PLAYLIST_LIMIT]
  logger.debug(f"Playlist track video ids: {video_ids}")

  track_urls = [extractor.format_song_url(video_id) for video_id in video_ids]
  logger.debug(f"Playlist track urls: {track_urls}")

  reply = "На данный момент скачивание плейлистов не поддерживается🚧\n" + \
    "Если хотите скачать какую-то песню, начинайте диалог заново и выбирайте опцию \"Песня (1)\""
  await update.message.reply_text(reply)
  playlist_id = extractor.get_playlist_id(playlist_metadata)
  download_command = f"{config.DOWNLOADER_SCRIPT_PATH} -p {extractor.format_playlist_url(playlist_id)}"
  logger.debug(f"Invoking subprocess with command: {download_command}")
  await subproc.invoke_async_subprocess(
    config.PYTHON_INTERPRETER,
    download_command
  )
  logger.info(f"Playlist downloaded")


  media_group : list[InputMediaAudio] = []
  for track_metadata in extractor.get_playlist_track_metadata(playlist_metadata):
    logger.debug(f"Extracting track metadata")
    video_id = extractor.get_song_video_id(track_metadata)
    logger.debug(f"Track video id: {video_id}")
    title = extractor.get_song_title(track_metadata)
    logger.debug(f"Track title: {title}")
    performer = extractor.get_song_performers(track_metadata)
    logger.debug(f"Track performer: {performer}")
    duration = extractor.get_song_duration(track_metadata)
    logger.debug(f"Track duration: {duration}")
    thumbnail_url = extractor.get_song_thumbnail_url(track_metadata)
    logger.debug(f"Track thumbnail url: {thumbnail_url}")

    logger.debug(f"Adding track to media group")
    media_group.append(InputMediaAudio(
      f'{config.AUDIO_PATH}/{playlist_id}/{video_id}.{config.AUDIO_EXT}',
      title=title,
      performer=performer,
      duration=duration,
      thumbnail=thumbnail_url
    ))

  logger.debug(f"Sending playlist to user")
  await update.message.reply_media_group(media=media_group)
  logger.info(f"Playlist sent")


  return ConversationHandler.END

async def cancel_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Leaving the conversation')
  return ConversationHandler.END

STATES_NUMBER = 10
PLAYLIST_LIMIT = 10
STATES = [i for i in range(STATES_NUMBER)]

DOWNLOAD_OPTIONS = {
  'song': 'Песня',
  'playlist': 'Плейлист'
}

assert len(DOWNLOAD_OPTIONS) <= len(STATES) + 2
