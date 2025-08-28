import extractor
import downloader

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not update.message or not update.effective_user:
    return
    
  reply = f'''
Привет, {update.effective_user.first_name}. Я бот для скачивания песен с YouTube.
Напиши мне название песни.
  '''
  
  await update.message.reply_text(reply)
    
    
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await downloader.cleanup()
  if not update.message or not update.message.text or not update.effective_user:
    return
  
  query = update.message.text
  
  metadata = extractor.search_metadata(query, 'songs')
  downloader.dump_metadata(metadata)
  if not metadata:
    await update.message.reply_text("Песня не нашлась :(")
    return
  
  reply = "Найдена следующая песня:\n"
  await update.message.reply_text(reply)
  
  reply = extractor.extract_metadata(metadata, 'songs')
  await update.message.reply_text(reply, parse_mode='MarkdownV2')
  
  reply = "Начинаю скачивание!"
  await update.message.reply_text(reply)
  
  await downloader.download_audio(extractor.format_song_url(metadata['videoId']))
  
  await update.message.reply_text("Скачивание завершено!")
  await update.message.reply_audio('downloads/audio/audio.m4a',
                                  duration=extractor.get_duration(metadata),
                                  performer=extractor.get_performers(metadata),
                                  title=extractor.get_title(metadata),
                                  thumbnail=extractor.get_thumbnail_url(metadata)
                                  )