import os
import utils

from yt_dlp import DownloadError
from telegram import Update
from telegram.ext import ContextTypes
from downloader import ydl

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if update.message and update.effective_user:
    reply = f'''
Hello {update.effective_user.first_name}. I am a bot for downloading audio!
Write url to download audio.
    '''
    
    await update.message.reply_text(reply)
    
    
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if update.message and update.effective_user:
    await update.message.reply_text('Downloading...')
    
    url = update.message.text
    if not url or not utils.is_valid_url(url):
      await update.message.reply_text('Invalid url')
      return
      
    
    try:
    # TODO: not an async download
      download_info = ydl.extract_info(url, download=True)
      audioname = ydl.prepare_filename(download_info)
      
      audioname, _ = os.path.splitext(audioname)
      new_ext = 'm4a'
      
      await update.message.reply_text(f'Successfully downloaded audio! Uploading...')
    except DownloadError as e:
      await update.message.reply_text(f'Download error. Reason: {e.msg}')
      return
    
    with open(f'{audioname}.{new_ext}', 'rb') as audio:
      await update.message.reply_audio(audio)