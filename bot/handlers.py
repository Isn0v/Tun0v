import time
import utils
import downloader
import config

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if update.message and update.effective_user:
    reply = f'''
Привет, {update.effective_user.first_name}. Я бот для скачивания аудио с YouTube.
Напиши мне URL аудио, и я скачаю его.
    '''
    
    await update.message.reply_text(reply)
    
    
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await downloader.cleanup()
  if not update.message or not update.effective_user:
    return
  
  await update.message.reply_text('Получаю URL...')
  
  url = update.message.text
  if not url or not utils.is_valid_url(url):
    await update.message.reply_text('Неверный URL!')
    return
      
  await update.message.reply_text('Получаю информацию о аудио...')
  
  try:
    await downloader.download_audio_info(url)
    await update.message.reply_text('Информация о аудио загружена! Печатаю метаданные...')
    
    metadata = downloader.load_metadata()
    output = f'''
Название: {metadata['title']}
Исполнитель: {metadata['artist']}
Альбом: {metadata['album']}
Длительность: {time.strftime('%M:%S', time.gmtime(metadata['duration']))}
    '''
    await update.message.reply_text(output)
    
    
    await update.message.reply_text('Скачиваю аудио...')
    await downloader.download_audio(url)
    
    await update.message.reply_audio(open(f'{config.AUDIO_PATH}/{config.AUDIO_NAME}.{config.AUDIO_EXT}', 'rb'))
    await update.message.reply_text('Готово!')
    
  except Exception as e:
    await update.message.reply_text(f'Error: {e}')
    return
  
  
  