import extractor
import downloader

from telegram import Update
from telegram.ext import ContextTypes

from logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not update.message or not update.effective_user:
    logger.warning('No message or user in start handler')
    return
    
  reply = f'''
Привет, {update.effective_user.first_name}. Я бот для скачивания песен с YouTube.
Напиши мне название песни.
  '''
  
  await update.message.reply_text(reply)
    
    
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await downloader.cleanup()
  if not update.message or not update.message.text or not update.effective_user:
    logger.warning('No message or user in download_audio handler')
    return
  
  query = update.message.text
  
  logger.info(f"Searching for song with query: {query}")
  metadata = extractor.search_metadata(query, 'songs')
  downloader.dump_metadata(metadata)
  if not metadata:
    logger.info(f"Song with query {query} not found")
    await update.message.reply_text("Песня не нашлась :(")
    return
  
  logger.info(f"Found song with query: {query}")
  reply = "Найдена следующая песня:\n"
  await update.message.reply_text(reply)
  
  logger.info(f"Extracting song metadata")
  reply = extractor.extract_metadata(metadata, 'songs')
  await update.message.reply_text(reply, parse_mode='MarkdownV2')
  
  logger.info(f"Downloading song with id {metadata['videoId']}")
  reply = "Начинаю скачивание!"
  await update.message.reply_text(reply)
  
  await downloader.download_audio(extractor.format_song_url(metadata['videoId']))
  
  logger.info(f"Song {metadata['videoId']} downloaded")
  await update.message.reply_text("Скачивание завершено!")
  await update.message.reply_audio('downloads/audio/audio.m4a',
                                  duration=extractor.get_duration(metadata),
                                  performer=extractor.get_performers(metadata),
                                  title=extractor.get_title(metadata),
                                  thumbnail=extractor.get_thumbnail_url(metadata)
                                  )
  logger.info(f"Song {metadata['videoId']} sent")
