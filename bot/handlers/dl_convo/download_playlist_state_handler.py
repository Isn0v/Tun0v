from bot import config, subproc
from bot.logger import logger


from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def download_playlist_state_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Entering the download playlist handler')

  HANDLER_STATE = 4
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
    return HANDLER_STATE

  reply = 'Данная функция пока не реализована 😥\n \
            Приходите позже'
  await update.message.reply_text(reply)
  return ConversationHandler.END

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